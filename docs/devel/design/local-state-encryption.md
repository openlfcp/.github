# Local state encrypted at rest (LFCP-02-098, POST-006)

**Status:** design note for sdk-ts (implementation: LFCP-02-098) and the
Obsidian plugin; the project owner decides before the beta whether it ships
before it (§9). **Date:** 2026-10-08. **Base:** sdk-ts `@openlfcp/storage`,
`@openlfcp/storage-idb`, `@openlfcp/storage-node`; obsidian
`src/obsidian/lfcp-env.ts`, `src/core/lfcp/install.ts`,
`src/core/sections/journal.ts`.

## 1. What is plaintext on disk today

| Record | Where | Content | Plaintext? |
| --- | --- | --- | --- |
| Profile checkpoints (`ProfileCheckpoint.state`) | IndexedDB `openlfcp-v1-<install>` (plugin), SQLite (Node) | the Automerge save of the decrypted Shared Objects state: Task titles, fields | **yes** |
| Section journals, projection bases, pending candidates (LFCP-02-038) | the plugin's install database, when 038 lands | source snapshots, unshared local text, allocated IDs | **yes**, once written |
| SDK receipts (LFCP-02-025) | install database | operation and unit IDs, node IDs, revisions | no text; metadata |
| Data Units, Snapshots, Key Packages, outbound items | install database | signed objects, AEAD or HPKE ciphertext | no |
| Control Records | install database | signed membership records | metadata (who, which abilities) |
| Principal keys, DEKs, invitation secrets | `SecretStore`: `app.secretStorage` (plugin), `FileSecretStore` (Node) | key material | in the secret store only |
| The vault's Markdown | the vault | the user's notes, shared text included | yes, by design: out of scope |

The plugin keeps its database in the app's profile directory, outside the
vault, so no sync provider sees it; but any program or backup that reads
the profile directory reads the checkpoints.

## 2. Goal and threat model

Keep Task and section text, journals, bases and candidates off disk in
plaintext, readable only with a key held in the platform's secret store.

Protects against: a copy of the profile directory or its backups, a disk
image, another OS user, a sync or backup tool that picks up the profile
directory. Does not protect against: malware running as the same user
(it can ask the secret store, as the plugin does), the vault's own Markdown,
or metadata (IDs, sizes, counters, membership).

## 3. The device key

- One **local state key** per install: 32 random bytes, a new `SecretKind`
  `local-state-key`, referenced as `lfcp-secret:local-state-key:<install
  id>.<generation>`. In the plugin it lives in `app.secretStorage` through
  the install's `SlotSecretStore` namespace (desktop: Electron
  `safeStorage`, the OS keychain); in Node, in the `FileSecretStore`.
- Created at first run, or at migration (§6), before any encrypted row is
  written (the secret store's ordering rule: secret first, then the row).
- The `install` meta row records the current `generation` (starting at 1)
  and the scheme `lse-v1`; the key itself never enters the database.

## 4. Envelope

Every protected value is stored as an envelope in place of the plaintext:

```text
envelope = "lse1" (4 bytes) || generation (uint32 BE) || nonce (24 bytes) || ciphertext || tag (16 bytes)
```

- AEAD: **XChaCha20-Poly1305** (`@noble/ciphers`, already a dependency):
  a random 24-byte nonce per write is safe at any write count, so local
  rows need no nonce counter. (Data Units use ChaCha20-Poly1305 with a
  sequence nonce; nothing local can reuse that scheme.)
- AAD: `"openlfcp-local-v1" || install id || store name || primary key`, so
  a row cannot be swapped with another row or moved to another install.
- A value that does not start with the magic is plaintext from before the
  migration; any other read failure is a key failure (§7).

The primitives live in `@openlfcp/crypto` (`sealLocal`, `openLocal`,
`LocalStateKey`, which keeps the key bytes inside that package): the
storage packages may not depend on it (LFCP-014). `@openlfcp/storage`
defines the `LocalStateCipher` interface and the keyring; the application
passes `localStateCipher` of `@openlfcp/crypto` when it opens an adapter
(§10).

## 5. What is encrypted

- `ProfileCheckpoint.state` in `storage-idb` and `storage-node`: sealed on
  `commit`, opened on load. The checkpoint's other fields (unit IDs and
  change references) stay as they are: they are needed for rebuilds and
  hold no text.
- The plugin's section journal entries, projection bases and pending
  candidates (LFCP-02-038): the whole record value, sealed by the journal
  store with the same helper; keys (operation ID, projection ID) stay in
  clear for lookups.
- Not encrypted: rows that are already ciphertext or signed public
  metadata (§1), receipts, sequence reservations.

## 6. Migration

On open, when the `install` meta row has no `lse-v1`:

1. create the key (§3) and store it in the secret store;
2. in batches inside the adapter's atomic commit, read every plaintext
   checkpoint (and, in the plugin, journal, base and candidate record),
   seal it and write it back;
3. write `lse-v1` and the generation into the meta row in the last batch.

The migration is resumable: a row already sealed (it starts with the magic)
is skipped, so a crash between batches continues on the next open. A new
install starts at step 3. Rows written after the upgrade are sealed at once.

## 7. A lost or unreadable key

A missing key, a missing generation or an authentication failure is not a
crash and never deletes rows silently:

| Record | Recovery |
| --- | --- |
| Checkpoint | treated as absent: the profile state is rebuilt from the stored accepted Data Units and their DEKs (the existing rebuild path); if the DEKs are gone as well, the Resource resynchronizes from the server |
| Projection base | treated as unknown: the projection goes through `PROJECTION_BASE_UNKNOWN` (MARKDOWN-SECTIONS-01 §11, fixture MS11) |
| Journal entry | the operation is resolved through `receiptOf` (SDK-SECTIONS-INTEGRATION-01 §3.4) where possible, else abandoned |
| Pending candidate | lost from the database; its text is still in the note's Markdown, where the user typed it. The plugin says so once ("local recovery copies could not be read") |

After a loss the SDK creates a new key at the next generation and seals
from then on; unreadable rows are replaced as they are rebuilt.

## 8. Rotation and diagnostics

- **Rotation:** an explicit command (plugin settings; an SDK call), not a
  schedule: write the key of the next generation, re-seal every row in
  batches as in §6, update the meta row, then blank the old secret (the
  Obsidian slot store has no delete; an empty value marks it deleted). Rows
  carry their generation, so a crash mid-rotation reads both.
- **Diagnostics** (default export): `local encryption: lse-v1, generation
  N, key present|missing`, counts of sealed and plaintext rows, the last
  migration or key-loss event with its time. Never key bytes, envelopes or
  plaintext.

## 9. Tests and effort

- A canary test per adapter: write Tasks and section text containing a
  unique canary through the SDK, close the database, grep the IndexedDB
  (LevelDB files) and SQLite files for the canary: no match.
- Migration from a 0.1.x/0.2.x database with plaintext checkpoints;
  resumption after a crash between batches.
- Key loss: delete the key, reopen: no crash, the checkpoint rebuilds, a
  base becomes unknown, the diagnostic reports it.
- AAD binding: a row copied to another key or install fails to open.

Effort (sdk-ts and plugin, with tests): helpers and both adapters about 2
days; migration and key-loss paths about 1.5 days; the plugin's journal
store and the IndexedDB canary test in the Obsidian harness about 1 day.
**About 4–5 days in all.** It does not change the protocol or any shared
bytes, and it can ship in any release; if it does not ship before the beta,
the beta notes state that local checkpoints are plaintext in the app's
profile directory.

## 10. Implementation

sdk-ts, LFCP-02-098:

| Commit | Part |
| --- | --- |
| `e713244` | `@openlfcp/crypto`: `LocalStateKey`, `sealLocal`, `openLocal`, `localStateCipher` (§4) |
| `540b9cc` | `@openlfcp/storage`: `LocalStateCipher`, `LocalStateKeyring` (new install, resumed migration or rotation, lost key, rotation), `reseal`, `localStateAad`, SecretKind `local-state-key` (§3, §6–§8) |
| `09cbe18` | `@openlfcp/storage-node`: `SqliteLfcpStorage.openSealed(path, { secrets, cipher })`, schema version 4 (`local_state`), `rotateLocalStateKey`, `localStateDiagnostics` |
| `28d6f4a` | `@openlfcp/storage-idb`: `IdbLfcpStorage.open(name, { localState: { secrets, cipher } })`, the same operations |
| `bf96725` | `conformance/storage/local-state.test.ts`: canaries with the real cipher (§9) |

As built:

- The install metadata is the adapter's own (`local_state` in SQLite, the
  `meta` store's `local-state` key in IndexedDB), not the plugin's install
  row: its install ID is random, distinct from the plugin's.
- A database that seals its local state refuses an open without the
  cipher and SecretStore (a plain open would hand envelopes to the client).
- SQLite: the sealed connection runs with `secure_delete`, and a finished
  migration truncates the WAL and vacuums the file, so plaintext from
  before the scheme does not linger in freed pages (the migration canary
  test fails without it).
- IndexedDB gives no way to purge old record versions from the browser's
  files (LevelDB keeps them until compaction): the plugin's harness checks
  its real files (§9), and the beta notes say so if they still hold
  plaintext after migration.
- Left to the plugin (obsidian): opening the adapter with `localState`
  (the key in `app.secretStorage`), sealing the section journal, bases and
  candidates with the keyring, the recovery texts of §7, the rotation
  command and the diagnostics line of §8, and the IndexedDB canary on disk.
