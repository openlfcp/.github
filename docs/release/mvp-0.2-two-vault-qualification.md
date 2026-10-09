# Secure two-vault qualification of shared sections (LFCP-02-056)

**Date:** 2026-10-09
**Status:** Evidence for MVP 0.2 task LFCP-02-056, headless; three open items
(below). The native Obsidian run of the same plan is LFCP-02-066.

[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §7
was run on production code: the released SDK packages from sdk-ts, the Rust
reference server, and two independent Principals with separate keys, sealed
storage and secret stores. No actor or key state was cloned between them.
Every Data Unit is signed and encrypted, and the server sees ciphertext only.
The machine-readable record is
[mvp-0.2-two-vault-qualification.json](mvp-0.2-two-vault-qualification.json).

## What ran

The run used fresh clones at the commits below. The server was built from its
clone against sdk-rs at the commit in its `sdk-rs.lock`, and the binary was
linked during the run.

| Item | Value |
| --- | --- |
| examples | `b3c763ff352a` (`qualification/`) |
| sdk-ts | `f2b526ddb34e` |
| server | `e1ba366323af`, sdk-rs `5b2a3b9257cf` (its lock) |
| spec | `mvp-0.2-baseline.1` (`96e21d62b97a`), the sdk-ts and server lock |
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
| 9 | same | B goes offline and writes. A revokes B, which rotates to epoch 1, and writes at the new epoch. C reads the new content, and B never receives it. B's stale batch is not merged by A or C and is not accepted, while B keeps it locally (the candidate is not erased). | G09 |
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

| Obligation | Evidence (sdk-ts `f2b526d`) | Result |
| --- | --- | --- |
| Invalid signature | `chaos.test.ts` 7 (live), `data-unit-apply.test.ts` (refused before the profile), wire vectors `tampered_D1`, `invalid_signature_D1`, `wrong_kid_D1` | PASS |
| Invalid AEAD | `chaos.test.ts` 8: the server accepts sealed garbage (N3) and the client fails it locally, never applying it | PASS |
| Unauthorized writer or control record | `chaos.test.ts` security assertions (2, live), `data-unit-apply.test.ts`, wire vectors `grant_escalation_C9`, `extension_type_non_owner_C1` | PASS |
| Wrong epoch or cutoff | `chaos.test.ts` 9: a revoked writer beyond the cutoff gets `STALE_DATA_EPOCH` and never merges; step 9 above | PASS |
| Equivocation | `chaos.test.ts` 10 (`ACTOR_EQUIVOCATION`), `data-unit-apply.test.ts` | PASS |
| Invalid Key Package or commitment | wire `key-package.test.ts`, client `sync-client.test.ts` (a DEK that does not match its commitment is never adopted), vector `hpke_recipient_mismatch_KP0` | PASS (no spec vector for a commitment mismatch) |
| Replay and duplicates | `chaos.test.ts` 1, 2, 10 and seeds 1–3 | PASS |
| One-time invitation double claim | `rust-server-invite.test.ts` (claims once, refuses every other claim), `rust-server-claim-journal.test.ts` (2) | PASS (no spec vector) |
| Duplicates, holes, reordering (step 6) | `chaos.test.ts` 2, 3, 4, 11–15 and seeds 1–3 on a Shared Objects Resource | PASS; not injected into the two-vault section run itself |
| Non-canonical changes, references outside history | `canonical-encoding.test.ts` (4), `operation-references.test.ts` (5) at the pin. Corpus `CAN-*`/`REF-*` (36) and SS57–SS59 (12) at `mvp-0.2-baseline.2` | PASS; see open item 2 |

Counts:

- Live: 24 of 24 tests pass (`chaos`, `e2e-two-clients`, `rust-server-invite`,
  `rust-server-claim-journal`).
- Wire vectors, CDDL fixtures, and the wire and client tests cited above: 447
  of 447 pass, and the wire pending list is empty.
- Admission and sections suites at the pin: 502 of 502 pass, and both pending
  lists are empty.
- The same suites with the spec at `mvp-0.2-baseline.2` (`4198c43ea89d`): 548 of
  548 pass.

## Open items

1. **A revoked member is not told.** After the revocation, B's client still
   reports access `allowed` and `current` at control sequence 4. Its stale
   batch stays `pending` with no NACK, and the session ends in `CLOSED` with
   `AUTHORIZATION_FAILED`. The work is kept out correctly, but the user is not
   shown that it was refused. This is tracked as LFCP-02-115.
2. **The F2–F4 corpus cases are not at the pins.** sdk-ts and the server lock
   `mvp-0.2-baseline.1`, which has no `CAN-*`/`REF-*` cases and stops at SS56.
   At those pins only the package tests exercise them. They pass at
   `mvp-0.2-baseline.2`. The pin move to baseline.2 is in progress, and this
   item closes when the evidence is re-run at the new pins.
3. **Vault metadata is not sealed.** `openSealed` seals profile checkpoints.
   Resource labels, IDs, sequences and queue metadata stay in the clear, as
   the storage contract states ("labels: public, never secrets"). An
   application must not put user text in labels. This was raised for the
   Obsidian plugin, which stores a collaboration or section name there.

## Not covered here

- Native UX: the private preview, inserting the section into a host note,
  extraction and source boundaries in a vault. These belong to the Obsidian
  run (LFCP-02-066). Here the "private note" is local-only sealed state, and
  "insert" is B's projection of the section Resource.
- Timings and budgets (§8 and the performance families) are not measured.
- LFCP-02-115's live test is not at the sdk-ts pin and did not run.
