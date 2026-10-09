# SDK fault qualification: persistence and status under faults

**Task:** LFCP-02-030, for sdk-ts (the TypeScript SDK). **Date:** 2026-10-09.
**Audience:** obsidian (the adapter's fault points), sdk-ts, release review.
**sdk-ts:** `f3102ff` (fault suite), on `775ef36`…`194f662` and the
LFCP-02-025 to -029 work before them.

## 1. What is qualified

The production persistence and status contract of the SDK
(SDK-SECTIONS-INTEGRATION-01 §3–§6), under the fault points of the MVP 0.2
test and release plan §8 that the SDK owns. Every test runs on isolated
temporary stores. Unless a row says otherwise, these are SQLite
(`@openlfcp/storage-node`) with a file key store, or IndexedDB on
fake-indexeddb. Failures are injected deterministically. No test resets a
store to pass.

The invariants checked at every fault:

- A failed commit has no receipt, no batch status and no "saved" claim,
  and the model is not half applied (SI17).
- Nothing is reset to recover. Queued Data Units keep their exact bytes
  and IDs, and actor sequences, key references and receipts stay.
- Recovery is correlated by the caller's operation ID. A retry returns the
  existing receipt or commits once; it never commits twice.
- Status comes only from evidence: accepted needs a correlated, durable
  ACK from a durability-2 server on the route set.

## 2. Fault points and evidence

| Fault point (plan §8) | Result | Evidence (sdk-ts) |
| --- | --- | --- |
| Disk full or write error at the commit's durable boundary | PASS: rejected, no receipt, status or model change; queue unchanged; the retry commits once with a fresh, unique sequence | `conformance/faults/sdk-faults.test.ts` "a full disk at commit" |
| Key store unavailable | PASS: `key-unavailable` in access and commit (`NotWritableError`); nothing written; key and reference kept; works again when the store is back | same file, "an unavailable key store" (fixed in `194f662`: the lookup used to throw) |
| Client restart during queued send | PASS: queue, receipts and pending statuses kept; Automerge actor and Data Unit sequence continue | `conformance/shared-sections/sync-commit.test.ts` "restart with pending section work"; `conformance/persistence/crash-points.test.ts` (SIGKILL at every step of a local write); `conformance/interop/rust-server-restart.test.ts` |
| Process death after the commit, before the caller saw its result | PASS: `receiptOf` answers; the retry under the same operation returns the receipt and adds nothing | `sdk-faults.test.ts` "an offline durable batch …"; `conformance/shared-sections/commit.test.ts` |
| Server persisted the unit, ACK lost | PASS: same bytes sent again; the batch stays pending until a correlated durable ACK, then accepted once | `packages/client/test/section-status.test.ts` "is pending until a correlated durable ACK"; `conformance/interop/rust-server-claim-journal.test.ts` (Control) |
| Server lost acknowledged units (restore) | PASS: reported `reoffered` with the first signal (`unknown-previous`, `have-gap`, `rehost`); pending again; accepted again once | `section-status.test.ts` "pending again" and "the loss signal's reason" |
| ACK without evidence (not durable, durability < 2, off the route set) | PASS: `evidence-unavailable`, never accepted | `section-status.test.ts` "evidence-unavailable", "off the Resource's route set" |
| Terminal NACK | PASS: `rejected` with code, units and operation ID; the content stays local | `section-status.test.ts` "rejected by a terminal NACK" |
| Snapshot loaded with a missing tail | PASS: the tail waits for its dependency; catch-up is `current-at-checkpoint` only once live; a Snapshot holding a refused change is rejected | `packages/shared-objects/test/section-snapshot.test.ts`; `section-status.test.ts` "catch-up"; `conformance/interop/rust-server-section-snapshot.test.ts` |
| Incomplete load before a write | PASS: `section.create` is refused (`SECTION_EXISTS`) while units are stored, or for a non-owner not yet live | `sync-commit.test.ts` "no new section over an incomplete load" |
| Access revoked during offline editing | PASS: queued work and receipts kept; new commits refused locally, whatever a server answers (SI15) | `sync-commit.test.ts` "retains queued work and refuses new work" |
| Storage written by the previous release | PASS: legacy queue, sequence, keys and model kept; a section added beside; a 0.1.x client refuses the upgraded store | `conformance/upgrade/upgrade-0.1.3.test.ts` (fixtures made with the v0.1.3 build) |

SI03, a durable batch offline and not accepted, is `pending` with
`catchUp: not-started`. It keeps that status under the same receipt across
a restart (`sdk-faults.test.ts`). SI17 is the first row.

The legacy persistence regression is the whole sdk-ts suite. It runs at
every commit above, in a fresh clone: `conformance/persistence`, the
storage contract on both adapters, and the live interop against the Rust
server at `server.lock`.

## 3. Not run here

| Fault point | Status | Why, and where it belongs |
| --- | --- | --- |
| A filesystem actually out of space | NOT_RUN | The suite injects the error SQLite returns (`SQLITE_FULL`) at `commit`. The suite does not fill a real filesystem, which needs a dedicated volume. The adapter boundary is the same. |
| Journal prepared before the SDK commit; source patch before journal finalization; remote patch over local source changes; import target hosted before source replacement; index or base metadata lost | NOT_RUN in sdk-ts | These are adapter fault points (OBSIDIAN-SECTIONS-ARCHITECTURE-02): the obsidian repository owns them. The SDK side they rely on is above: `receiptOf`, idempotent commit and the `section.create` guard. |
| Server restart during ingest or a Control compare-and-set | NOT_RUN in sdk-ts | Server atomicity is qualified in the server repository. The SDK side, never accepting without a durable ACK, is above. |

## 4. Changes made while qualifying

- `194f662`: an unreadable key store made `canWrite` and `commit` throw from
  the DEK lookup. It is now `key-unavailable`.
- `775ef36`: units committed through `SyncClient.commit` did not count
  toward `snapshotPolicy`, so a section's only writer never published a
  Snapshot. Found by the plugin (LFCP-02-097).
- `dac706f`: IndexedDB opened at version 1 after checkpoints could be
  sealed, so a 0.1.x client would have read sealed rows as plaintext. It
  now opens at version 2, which 0.1.x refuses (LFCP-02-029).
