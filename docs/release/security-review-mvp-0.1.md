# Pre-release security review: MVP 0.1

**Status:** review of 2026-10-06, read-mostly. It covers sdk-ts, obsidian,
server and sdk-rs at their main branches of that date:
- sdk-ts 017d9c1;
- obsidian 770832c;
- server and sdk-rs at their HEADs.

Findings are ranked critical / high / medium / low / info. Each one is
either **fixed** (a commit) or **routed** (not fixed here, for a decision or
a follow-up task). The DoS-class items that are not fixed are listed as known
limitations in the release notes.

**Method.**
- Four parallel read-only audits, one per area: secret flow (TS);
  randomness, constant time and input limits (TS); server; sdk-rs.
- Every high finding was confirmed by hand, either by reading the code
  path or by running a timing or memory experiment. The experiment
  results are quoted below.
- `pnpm audit` for the JS repositories; a version inventory for the Rust
  lockfiles.

## Summary

| ID | Severity | Area | Finding | State |
| --- | --- | --- | --- | --- |
| H1 | high | sdk-ts, sdk-rs, spec | Automerge decompression bomb: compressed change chunks (§11) and Snapshot columns inflate without an output cap | routed: spec decision |
| H2 | high | sdk-ts client | A server-supplied Have range is expanded one sequence at a time: one `DATA_HAVE` hangs the client | routed |
| H3 | high | obsidian | Task-suffix regex (recurrence) is super-linear: a collaborator's long title freezes the editor | routed |
| H4 | high | server | `DATA_GET` / `KEY_PACKAGE_GET` load every requested range/epoch before deduplicating, with no count cap | routed |
| H5 | high | server | Open hosting by default and no quotas: any keypair can host Resources and fill the disk | routed (known limitation) |
| H6 | high | server | GET replies are built fully in memory; the outbound queue can hold about 2 GiB per connection | routed |
| M1 | medium | sdk-ts, sdk-rs | A client adopts the server's `READY.maxMessageBytes` with no local upper bound | routed |
| M2 | medium | server | No connection cap, no HTTP header timeout, no handshake deadline; PING before AUTH keeps a connection alive | routed (known limitation) |
| M3 | medium | server | `POST /admin/challenge` is unauthenticated and its map is unbounded | routed |
| M4 | medium | server | The coordinator's per-Resource slot map grows for any requested Resource ID | routed |
| M5 | medium | server | Full CBOR decode of every frame before AUTH: about 30× memory amplification | routed (known limitation) |
| M6 | medium | server | The pairing code is printed to stdout, the same stream as the tracing log (so `docker logs` keeps it) | routed |
| M7 | medium | sdk-rs | `values::read` recursion has no depth limit (stack overflow on deeply nested `extensions`) | routed |
| M8 | medium | sdk-rs | `SharedObjects::merge` has no §14.1 sequence check and no panic guard | routed |
| M9 | medium | obsidian | Other task-suffix regexes are quadratic on long whitespace runs | routed (with H3) |
| M10 | medium | sdk-ts storage | Decrypted Shared Objects state (checkpoints) is stored unencrypted on the device | known limitation |
| L1 | low | sdk-ts core | A base64url error quoted the bad character; a corrupted key slot could show one key character in a Notice | **fixed: sdk-ts 017d9c1** |
| L2 | low | sdk-ts | Hosting credentials are plain `Uint8Array` fields with no redaction wrapper (none are logged today) | routed |
| L3 | low | sdk-ts, sdk-rs | Copies of exported key bytes are not zeroed | known limitation |
| L4 | low | sdk-ts storage-node | Secrets in 0600 files; a crash can leave a `.tmp-*` file holding a secret | routed |
| L5 | low | server | The setup-code hash is unsalted (about 40-bit code); the database files use the default umask (only `server-id` is 0600) | routed |
| L6 | low | server | Anyone can burn the five pairing attempts; pairing then needs a restart | routed |
| L7 | low | sdk-ts, sdk-rs, server | No count caps on objects per batch, Have entries or held/pending/quarantined units (bounded by message size and authorization) | known limitation |
| L8 | low | obsidian | The invitation link stays on the OS clipboard after "Copy link" | known limitation |
| L9 | low | sdk-rs | `HostingCredential` derives `PartialEq` (not constant time) and `Clone` | routed |

Also fixed by this pre-release work (earlier commits):
- **sdk-ts 27ab3e4:** a revoked member saw "NACK 4" instead of the
  AUTHORIZATION_FAILED explanation. Found by the LFCP-071 gate.
- **SPEC-PATCH-06 item 7, sdk-ts 57152f9 and eced057:** a change that
  skips its actor's sequence number corrupted a JS document and panicked
  automerge-rs. It is now rejected before the engine in both SDKs, and the
  JS replica restores itself after any engine error.

## H1: decompression bomb

§11 accepts "an uncompressed or a compressed change" chunk, and Snapshots
are Automerge saves with deflate-compressed columns. Neither SDK limits the
inflated size before handing the bytes to Automerge. Automerge 0.12 and
Automerge JS 3.5.0 inflate with no cap.

**Measured** (Automerge JS 3.5.0, `A.decodeChange`): a 255 KiB
compressed-change chunk that inflates to 256 MiB of zeros took 1.8 s. Peak
RSS was 1.36 GiB, including the test's own 256 MiB buffer. Inflation
happens before any parse error.

At the default 8 MiB message limit, one Data Unit or Snapshot can demand
gigabytes. In Rust, running out of memory aborts the process, and
`catch_unwind` does not help. The sender must be an authorized writer
(units) or Snapshot publisher, because the bytes are signed and
AEAD-encrypted. So this is a malicious-collaborator attack, not a server
attack.

**Options** (a spec decision; ADR material):
1. Forbid compressed change chunks in framing version 1.
2. Require a receiver cap on inflated size.

Snapshots need option 2 in any case.

## H2: Have range expansion (sdk-ts)

`packages/client/src/sync-client.ts:1111`:

```ts
for (const r of missing)
  for (let s = r.start; s <= r.end; s++) expected = addSequence(expected, r.actor, s);
```

`missing` comes from the server's Have, which is only checked for uint64
range. A Have with `contiguous = 2^64-1`, or even `10^7`, blocks the event
loop: in Obsidian, the UI. Keep the expected ranges as intervals and cap the
span requested per round. The file is being changed by the batching work, so the fix is routed, not made here.

## H3/M9: task-suffix regexes (obsidian)

`src/core/projection/task-text.ts:132`:
`\s*🔁️?\s*([a-zA-Z0-9, !]+?)\s*$`, unanchored at the start. A lazy
class that includes the space is followed by `\s*$`.

**Measured** on `"🔁" + " " × n + "#"`:

| n | Time |
| --- | --- |
| 500 | 0.30 s |
| 1,000 | 0.47 s |
| 2,000 | 3.6 s |

The audit measured 28.8 s at n = 4,000.

Task titles have no length limit, and the renderer writes a shared title
into the local line, which is then re-parsed. So a remote collaborator
freezes the editor with a title of a few KB. `BLOCK_ID`, `TAG` and
`DATE` (lines 129-134) are quadratic on long whitespace runs. The parser
must stay byte-exact, so a linear rewrite (find the marker first, then
match an anchored suffix) belongs with the projection owner.

## Server under hostile clients (H4-H6, M2-M6)

**What exists:**
- 8 MiB default message limit, checked before decoding;
- CBOR nesting cap of 64;
- pre-allocation bounded by the remaining input;
- text frames rejected;
- outbound queue of 256 messages with a 10 s write timeout;
- idle timeout of 3× heartbeat;
- live-push overflow drops the subscriber;
- admin request bodies capped at 16 KiB;
- setup code: 5 attempts, 1 h lifetime.

**What is missing:**
- a connection cap (global or per IP);
- an HTTP header-read timeout;
- a handshake deadline or pre-AUTH message cap;
- rate limits on WebSocket and admin HTTP;
- per-principal or per-Resource quotas (the `IngestPolicy` hook exists;
  the default is `Unlimited`);
- objects per PUT capped other than by message size;
- ranges and epochs per GET (deduplicate before loading);
- streamed or paged GET replies;
- a cap on the admin challenge map;
- eviction from the coordinator slot map;
- owner-only permissions on the database.

**Deployment advice for MVP 0.1:**
- Run the server for known users.
- Set the allow-list hosting policy (`PUT /admin/hosting`).
- Keep it behind the Caddy proxy, with proxy-level connection and rate
  limits.

**Logging is clean.**
- The level comes from config or `--log-level` (default `info`).
- No macro logs payloads, ciphertext, credentials, tokens, proofs, setup
  codes or invitation data.
- `SetupCode` and `HostingCredential` are redacted in `Debug`.
- Behind Caddy the logged peer is the proxy address.

**Unauthenticated HTTP endpoints:**
- `/health` is `{"status":"ok"}`.
- `GET /setup` returns `paired` and the public `server_id`.

**Admin auth:**
- Admin sessions need a COSE_Sign1 proof over a single-use challenge
  (strict Ed25519), plus administrator membership.
- Bearer tokens are 32 OS-random bytes, kept only as a SHA-256 in memory,
  for 15 minutes. There is no logout.

**M6:** the pairing banner says "never the log", but `println!` and the
tracing subscriber share stdout. Under Docker the code stays in
`docker logs` for its one-hour lifetime. Use stderr or a file with mode
0600, or state the behaviour in the README.

## sdk-rs (M1, M7, M8, L9)

**Clean:**
- `#![forbid(unsafe_code)]`;
- every key type has a redacted `Debug` and no `Display`;
- keys are zeroized on drop (`Zeroizing`; dalek zeroize);
- errors carry no key or payload bytes;
- no logging;
- no non-CSPRNG;
- the hand-written CBOR decoder has depth 64, length checks before
  allocation, and rejects indefinite lengths, tags and floats;
- `verify_strict` plus a canonical, non-small-order public-key check;
- the §14.1 sequence pre-check exists (`document.rs:373`, `:383`), with
  `catch_unwind` and backup restore around apply and load.

**Gaps:**
- `merge` lacks both guards (M8).
- `values::read` recursion is unbounded (M7).
- A client adopts the server's `READY` maximum (M1).
- The document is cloned for every apply; this is already in the release
  notes.

## Secret flow (sdk-ts, obsidian)

No critical or high finding.

**Logging and error messages:**
- There are no console or logger calls in non-test code of either
  repository.
- About 90 interpolated error messages were reviewed. They carry
  lengths, codes, sequences, epochs or hex of public IDs. The invitation
  codec reduces every error to a code.

**Key and invitation classes:** `SigningKeyPair`, `AgreementKeyPair`,
`ResourceDEK`, `ActorDataKey`, `SnapshotKey`, `InvitationSecret` and
`InvitationLink` keep their secrets in `#private` fields. They print
`[redacted]` from `toJSON`, `toString` and the Node inspect hook.

**Events and dialogs:** `SyncEvent`, `ApplyOutcome`, `AcceptedInvitation`
and `onProgress` carry IDs, codes and stage names only. The join dialog is
a password field. The link is never written to a note, `data.json`, local
storage or IndexedDB.

**Where secrets live:** keys and DEKs are only in Obsidian's
`secretStorage` or the Node `FileSecretStore`. Storage rows hold only
secret references and DEK commitments. Actor and snapshot keys are
derived and never stored.

**Known limitations:**
- Obsidian's `secretStorage` is shared by every plugin on the device
  (M10).
- Decrypted checkpoints are stored as plaintext (M10).
- Key-byte copies are not zeroed (L3).
- The link stays on the clipboard (L8).

## Randomness and constant time

**Randomness:**
- Every key, DEK, Resource ID, Object ID, message ID, handshake nonce,
  session ID, Obsidian install ID, server ID, admin challenge or token,
  and setup code comes from a CSPRNG:
  - TS: `secureRandom`, noble, or the HPKE library;
  - Rust: `getrandom`, `OsRng`, or the `hpke` crate.
- `secureRandom` throws when no secure source exists; there is no
  fallback.
- No `Math.random` appears in non-test code, and neither does `thread_rng`
  or `rand::random`.
- The injectable random sources (TS `RandomSource`, Object ID `random`,
  sdk-rs `*_with_rng`, server `with_random`) are used only by tests.
- AEAD nonces are derived from the actor sequence by design (§26). Safety
  rests on sequences never repeating, which storage reservations and
  §9 enforce. sdk-rs leaves sequence uniqueness to its caller (doc note).

**Constant time:** no secret-dependent comparison was found.
- `bytesEqual` and Rust `==` compare only public values: IDs, heads,
  public keys and DEK commitments, which are public in the Control Chain.
- AEAD tags are checked inside the AEAD and HPKE libraries.
- The server compares SHA-256 digests of tokens, credentials and the setup
  code. That is not exploitable, given hashing first and the attempt
  limits.

## Dependency audit

| Repository | Tool | Result |
| --- | --- | --- |
| sdk-ts | `pnpm audit` | 0 advisories (94 dependencies) |
| examples | `pnpm audit` | 0 advisories (75 dependencies) |
| obsidian | `pnpm audit` | 1 moderate: `moment` 2.29.4 (GHSA-4p3w-j4w9-5jqw, path traversal via a crafted locale name), reached only through the `obsidian` typings dev dependency; not bundled (the plugin never imports it; `obsidian` is external) |
| server, sdk-rs | `cargo audit` | not run: `cargo-audit` is not installed and was not fetched. The security-relevant crates for a later check are listed below |

**Rust crates in both lockfiles:**
- `ed25519-dalek` 3.0.0, `x25519-dalek` 3.0.0, `curve25519-dalek` 5.0.0;
- `chacha20poly1305` 0.11.0, `hpke` 0.14.1, `sha2` 0.11.0;
- `rand_core` 0.10.1, `getrandom` 0.4.3;
- `subtle` 2.6.1, `zeroize` 1.9.0.

**Server only:** `tokio` 1.53.2, `tokio-tungstenite`/`tungstenite` 0.30.0,
`hyper` 1.11.1, `rusqlite` 0.40.2.

**sdk-rs only:** `automerge` 0.12.0.
