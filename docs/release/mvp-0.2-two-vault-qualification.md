# Secure two-vault qualification of shared sections (LFCP-02-056)

**Date:** 2026-10-09
**Status:** Evidence for MVP 0.2 task LFCP-02-056, headless, at the
`mvp-0.2-baseline.2` pins; no open item (see "Findings"). The native Obsidian run of
the same plan is LFCP-02-066.

[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §7
was run on production code: the released SDK packages from sdk-ts, the Rust
reference server, and two independent Principals with separate keys, sealed
storage and secret stores. No actor or key state was cloned between them.
Every Data Unit is signed and encrypted, and the server sees ciphertext only.
The machine-readable record is
[mvp-0.2-two-vault-qualification.json](mvp-0.2-two-vault-qualification.json).

## What ran

The run used fresh clones at the commits below, which are the pins of every
lock. The server was built from its clone against sdk-rs at the commit in
its `sdk-rs.lock`.

The server binary is byte-identical to the one in the first run of this
report, at `e1ba366` with sdk-rs `5b2a3b9` (sha256 in the record). Cargo had
nothing to rebuild, for two reasons:

- the server commits in between change only tests, the README and the locks;
- every sdk-rs source change in between is behind the `shared-objects` and
  `shared-sections` features, which the server does not build
  (`default-features = false`).

| Item | Value |
| --- | --- |
| examples | `d77e4643ea90` (`qualification/` unchanged since `b3c763f`) |
| sdk-ts | `b92f70177a4d` |
| server | `7f7eb997a72f`, sdk-rs `c05309ba2588` (its lock) |
| spec | `mvp-0.2-baseline.2` (`4198c43ea89d`): the sdk-ts, sdk-rs and server lock, and the examples conformance pin |
| Toolchain | Node.js v24.4.0, pnpm 10.33.4, rustc 1.99.0, macOS arm64 |
| Load | tests one at a time, `CARGO_BUILD_JOBS=4`, `LFCP_REQUIRE_LIVE=1` |

Commands:

- `pnpm build` in sdk-ts.
- `pnpm typecheck && pnpm lint` in examples.
- `vitest run qualification/` in examples, with `LFCP_SERVER_DIR` set to the
  server clone.

The vaults are `SqliteLfcpStorage.openSealed` databases with a
`FileSecretStore` each. Steps 1–4 also run with in-memory stores, once for W20
and once for W200.

## Results: §7 steps 1–11

All five live tests pass (`qualification-vitest.json` in the record).

| Step | Test | What is shown | Gates |
| --- | --- | --- | --- |
| 1 | `two-vault.test.ts` (W20, W200) | A writes a section of W tasks, each with a paragraph, as one batch with one receipt. It creates and hosts a dedicated Resource, and the batch is `accepted`. W200 is split into 2 Data Units within the change budgets. | G03, G04 |
| 2 | same | One invitation. B joins through the real one-time claim and HPKE key delivery (`claimed`). | G03, G09 |
| 3 | same | B is LIVE and converges to A's revision with all 2·W nodes. Only the section Resource syncs. | G03, G08 |
| 4 | same | B creates a task, A sets a status and edits a paragraph. Both see each other's changes, every batch is `accepted`, and neither side has errors. | G04, G05 |
| 5 | `partition.test.ts` | Both sides go offline. Each edits independent fields and Text, and both move the same Task to different parents (a selected conflict). | G06 |
| 6 | same | B restarts with 2 pending batches: the vault is closed and reopened, and the profile comes from its sealed checkpoint. The actor sequence is preserved, the receipts are durable, and the queue is intact. After reconnecting, both sides reach the same revision. Both show `STRUCTURAL_ATTENTION` with `PLACEMENT_CONFLICT` and both candidate parents, and no node is duplicated. | G06, G07 |
| 7 | same | A resolves the placement causally (`node.resolve_placement`). Both end `VALID` with the Task under the section, and B's batches are accepted after its restart. | G06 |
| 8 | `restart-revoke.test.ts` | A publishes a Snapshot and writes a tail, then the server restarts on its persisted state. C, a third Principal, joins afterwards: it loads the Snapshot and applies fewer units than A wrote, then reaches A's revision. B also converges. | G07 |
| 9 | same | B goes offline and writes. A revokes B, which rotates to epoch 1, and writes at the new epoch. C reads the new content, and B never receives it. B's stale batch is not merged by A or C and is not accepted, while B keeps it locally (the candidate is not erased). B's client reports the refusal: access `allowed: false` with reason `server-refused`, and the stale batch `blocked`. | G09 |
| 10 | same | C detaches (stops). Nothing shared follows, and A carries on: its next batch is accepted. | G05 |
| 11 | `opacity.test.ts` | Opacity scan and a re-run of the legacy secure smoke (below). | G08 |

### Step 11: opacity and the legacy Resource

Both vaults joined a section Resource over tapped WebSockets and edited it.
Each vault also kept a private note: the local state of a local-only
projection, written as a sealed profile checkpoint. On the same vaults and
server, A then created a legacy Shared Objects Resource. B joined it, and both
edited a Task. The legacy smoke passed, and each vault holds the control logs
of both Resources.

The scan covered:

- 101 frames that either client sent or received;
- every server file (`server.sqlite3` with its WAL and SHM, `server-id`,
  `setup-code`) and the server log;
- every file of both vault databases (`lfcp.sqlite` with its WAL and SHM). The
  secret stores were excluded, because they hold the keys by design.

It searched for 8 plaintexts: both private notes, a task title, paragraph
text, B's task, A's edit, and both legacy titles. It also searched for both
DEKs and all four private keys. **No match anywhere.**

A positive control shows the scan finds metadata, which is not claimed hidden:
A's Principal ID on the wire and in the server's files, and the Resource ID in
the vaults.

## Negative security tests (§7, retained 0.1 obligations)

Existing sdk-ts tests ran on the same clones. Live tests used the same server
binary.

| Obligation | Evidence (sdk-ts `b92f701`) | Result |
| --- | --- | --- |
| Invalid signature | `chaos.test.ts` 7 (live), `data-unit-apply.test.ts` (refused before the profile), wire vectors `tampered_D1`, `invalid_signature_D1`, `wrong_kid_D1` | PASS |
| Invalid AEAD | `chaos.test.ts` 8: the server accepts sealed garbage (N3) and the client fails it locally, never applying it | PASS |
| Unauthorized writer or control record | `chaos.test.ts` security assertions (2, live), `data-unit-apply.test.ts`, wire vectors `grant_escalation_C9`, `extension_type_non_owner_C1` | PASS |
| Wrong epoch or cutoff | `chaos.test.ts` 9: a revoked writer beyond the cutoff gets `STALE_DATA_EPOCH` and never merges; `rust-server-revoked-refusal.test.ts`: the revoked member's client reports server-refused access and a blocked batch; step 9 above | PASS |
| Equivocation | `chaos.test.ts` 10 (`ACTOR_EQUIVOCATION`), `data-unit-apply.test.ts` | PASS |
| Invalid Key Package or commitment | wire `key-package.test.ts`, client `sync-client.test.ts` (a DEK that does not match its commitment is never adopted), vector `hpke_recipient_mismatch_KP0` | PASS (no spec vector for a commitment mismatch) |
| Replay and duplicates | `chaos.test.ts` 1, 2, 10 and seeds 1–3 | PASS |
| One-time invitation double claim | `rust-server-invite.test.ts` (claims once, refuses every other claim), `rust-server-claim-journal.test.ts` (2) | PASS (no spec vector) |
| Duplicates, holes, reordering (step 6) | `chaos.test.ts` 2, 3, 4, 11–15 and seeds 1–3 on a Shared Objects Resource | PASS; not injected into the two-vault section run itself |
| Non-canonical changes, references outside history | `canonical-encoding.test.ts` (4), `operation-references.test.ts` (5), the corpus cases `CAN-*`/`REF-*` (36) and SS57–SS59 (12) | PASS |

Counts:

- Live: 25 of 25 tests pass (`chaos`, `e2e-two-clients`, `rust-server-invite`,
  `rust-server-claim-journal`, `rust-server-revoked-refusal`).
- Wire vectors, CDDL fixtures, the admission and sections corpora, and the
  wire, client and admission tests cited above: 995 of 995 pass. Every
  pending list is empty, and no corpus section reports "not in this
  baseline".

## Findings

The first run of this report, at the `mvp-0.2-baseline.1` pins, raised three
items. Two are closed in this run; the third is a boundary of the storage
contract.

1. **A revoked member was not told** (LFCP-02-115). It is closed in this run.
   Before the fix, B's client kept reporting access `allowed` and `current`,
   and its stale batch stayed `pending`. Now step 9 records access
   `allowed: false` with reason `server-refused`, and the batch `blocked`.
2. **The F2–F4 corpus cases were not at the pins.** It is closed in this run.
   `mvp-0.2-baseline.1` had no `CAN-*`/`REF-*` cases and stopped at SS56. At
   `mvp-0.2-baseline.2` they run at the pins and pass.
3. **Vault metadata is not sealed.** This is by design. `openSealed` seals
   profile checkpoints. Resource labels, IDs, sequences and queue metadata
   stay in the clear, as the storage contract states ("labels: public, never
   secrets"), so an application must not put user text in labels. The
   Obsidian plugin no longer stores collaboration or section names there.

## Not covered here

- Native UX: the private preview, inserting the section into a host note,
  extraction and source boundaries in a vault. These belong to the Obsidian
  run (LFCP-02-066). Here the "private note" is local-only sealed state, and
  "insert" is B's projection of the section Resource.
- Timings and budgets (§8 and the performance families) are not measured.
