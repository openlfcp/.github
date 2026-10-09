# Integrated crash, access and compatibility recovery (LFCP-02-070)

**Date:** 2026-10-09
**Status:** Evidence for MVP 0.2 task LFCP-02-070, headless part, at the
`mvp-0.2-baseline.2` pins. Every headless check passes, and no blocking defect
was found. The native Obsidian items are NOT_RUN; they belong to the native run
(LFCP-02-066, which 070 depends on).

The task asks for multi-component faults that isolated tests miss. This run
puts them together on production code:

- the candidate SDK on sealed SQLite vaults;
- the Rust reference server, crashed, restarted and restored;
- the **released 0.1.3 client** from npm, run in its own process on the same
  vault and the same server. Its compatibility is observed, not inferred.

The machine-readable record is
[mvp-0.2-integrated-recovery-qualification.json](mvp-0.2-integrated-recovery-qualification.json).

## What ran

Fresh clones at the commits below; the server was built from its clone
against sdk-rs at its `sdk-rs.lock`, in a build directory of its own.

| Item | Value |
| --- | --- |
| examples | `5f51aa0` (`qualification/test/compat.test.ts`, `recovery.test.ts`, `legacy-0.1.3/`) |
| sdk-ts | `b92f701` |
| server | `7f7eb99`, sdk-rs `c05309b` (its lock); binary sha256 in the record |
| obsidian | `c4ab7ee` (its `sdk-ts.lock` is `b92f701`) |
| Old client | `@openlfcp/*@0.1.3` from npm, `npm ci` from the committed lock file |
| spec | `mvp-0.2-baseline.2` (`4198c43`) |
| Toolchain | Node.js v24.4.0, pnpm 10.33.4, rustc 1.99.0, macOS arm64 |
| Load | test files one at a time, `--maxWorkers=2`, `CARGO_BUILD_JOBS=4`, `LFCP_REQUIRE_LIVE=1` |

Commands:

- examples: `pnpm typecheck`, `biome check .`, then
  `vitest run --no-file-parallelism qualification/`.
- sdk-ts: `vitest run --maxWorkers=2` on the fault, upgrade and live interop
  files listed below.
- obsidian: `vitest run` on the journal, import, recovery, compatibility and
  projection tests listed below.

Each run has `LFCP_SERVER_DIR` set to the server clone.

Results:

| Run | Pass |
| --- | --- |
| examples `qualification/` (056 steps 1–11 and the new 070 tests) | 10 of 10 |
| sdk-ts lower-level fault, upgrade and live suites | 40 of 40 |
| obsidian headless journal, import, compatibility and projections | 30 of 30 |

## The fault matrix (acceptance 1)

Each new case starts its own server with two joined vaults, A and B, on a
section Resource. A server fault therefore touches nothing else.

| Layer | Fault | Evidence | Result |
| --- | --- | --- | --- |
| SDK receipts | An ACK is lost, then the client restarts. The server holds B's batch and A applied it, but B saw no ACK. B's vault is closed and reopened with the batch still queued. | `recovery.test.ts` F1 | PASS. The batch is sent again on a new connection, the server answers the repeat (§47), and it is `accepted` under the same durable receipt. B's actor sequence continues, and A holds each unit once (sequences 1, 2). |
| Server ACK and CAS | The server crashes after it commits a Control Record (the invitation's grant), before its ACK reaches A. | `recovery.test.ts` F4 | PASS. A sends the record again after the restart, the server answers the repeat (§70), and the invitation admits C, who converges. |
| Server data loss | The server's store is replaced by a copy taken before B's accepted batch (ADR 0008). | `recovery.test.ts` F2 | PASS. B emits `reoffered` (reason `have-gap`) for the lost unit and sends it again. C, who joins after the restore, receives it from the server. |
| Snapshot tails | The server restarts after a Snapshot and a tail. | reused: 056 step 8 (`restart-revoke.test.ts`, rerun here); sdk-ts `rust-server-section-snapshot.test.ts` | PASS |
| Revocation | B is revoked while offline with a batch queued, then restarts twice. | `recovery.test.ts` F3; reused: 056 step 9, sdk-ts `rust-server-revoked-refusal`, `rust-server-revoke`, `rust-server-access-recovery` | PASS. After each restart B reports access `server-refused` (recovery `still-refused`), the batch `blocked` and catch-up `unknown`. The queue, the receipt and the local candidate are byte-equal to before; nothing is reset. A never receives the batch. |
| Client process crash | A client process is SIGKILLed mid-sync and mid-write. | reused: sdk-ts `rust-server-restart.test.ts` (legacy profile) | PASS |
| SDK durable boundary | A full disk at commit, an unavailable key store, an offline batch across a restart. | reused: sdk-ts `faults/sdk-faults.test.ts` (LFCP-02-030) | PASS |
| Editor journals | Journal phases, crash-table recovery, kept candidates, and a rebuild from the note alone. | obsidian `test/core/sections/journal.test.ts`, `recovery.test.ts` (headless plugin core) | PASS, headless only. In a native vault: NOT_RUN. |

## CM01–CM14 (acceptance 2)

"Live, actual builds" means the released 0.1.3 client and the candidate ran
against the Rust server in this run. "Headless plugin core" means the
obsidian tests run on the candidate SDK without Obsidian.

| Case | Evidence | Level | Result |
| --- | --- | --- | --- |
| CM01 Upgrade with legacy pending edits | `compat.test.ts`: 0.1.3 hosts a Task and exits with 2 edits queued (sequences 3, 4). The candidate opens the vault, which upgrades and seals it, and sends both. A member applies sequences 1–4 exactly. Also obsidian `compatibility.test.ts` CM01 (same identity, same queued bytes). | Live, actual builds; headless plugin core | PASS |
| CM02 New section beside legacy Tasks | `compat.test.ts`: a section Resource on the upgraded vault. The legacy member keeps syncing and has no trace of the section. Also obsidian CM02. | Live; headless | PASS |
| CM03 Legacy-only client meets a section | `compat.test.ts`: 0.1.3 returns `profile-unsupported` (`PROFILE_UNSUPPORTED`) and does not claim. The same invitation then admits a candidate client. | Live, actual builds | PASS |
| CM04 Import a legacy Task with private child notes | obsidian `legacy-import.test.ts` CM04 | Headless plugin core | PASS; native preview NOT_RUN |
| CM05 Retry after the server accepted but the ACK was lost | obsidian CM05/CM14 (same target after a crash); F1 above for the SDK and the server | Headless; live | PASS |
| CM06 Source changes during the import | obsidian CM06 | Headless | PASS |
| CM07 Target edited after the replacement | obsidian CM07 | Headless | PASS |
| CM08 Import a conflicted Task | obsidian CM08 | Headless | PASS |
| CM09 Unknown extension | obsidian CM09 | Headless | PASS |
| CM10 Downgrade and local text edits | `compat.test.ts`: 0.1.3 opens the upgraded vault and refuses it ("schema version 4, newer than this code (3)"). Every vault file is byte-identical afterwards. obsidian CM10: edits made while the plugin was off merge later. | Live, actual builds; headless | PASS; the native downgrade UX is NOT_RUN |
| CM11 Rebuild after local index loss | obsidian `projections.test.ts` MS11/CM11, `journal.test.ts` (the base is reported unknown) | Headless | PASS |
| CM12 Assignee without target capability | obsidian CM12 | Headless | PASS |
| CM13 Mixed refs and private paragraphs | obsidian CM13 | Headless | PASS |
| CM14 Failed or abandoned staged target | obsidian CM05/CM14 (the journal keeps the identity; cancel keeps the note) | Headless | PASS |

## Security retained (acceptance 3)

The following were rerun at the same pins:

- sdk-ts `chaos.test.ts`: 20 of 20, live. It covers invalid signatures and
  AEAD, unauthorized writers, a stale epoch after a cutoff, equivocation,
  replay and duplicates.
- `rust-server-claim-journal.test.ts`: one-time claims.
- 056 step 11 (`opacity.test.ts`): no plaintext or key on the wire, on the
  server or in the sealed vaults.

No case recovers by resetting storage. F3 restarts a refused member twice and
checks that the queue, the receipt and the candidate are unchanged. CM10 checks
that a refused downgrade changes no byte.

## Blocking defects

None.

## Not covered here

- **Native Obsidian:** the editor journal under a real editor, the import
  preview, the downgrade UX and the status UI. These are NOT_RUN here and
  belong to LFCP-02-066.
- **Concurrent Control Record CAS conflicts** (two writers racing for one
  head) are not injected in this run; F4 covers a crash around one commit.
- **Old plugin builds:** the old side is the 0.1.3 SDK, which Shared Tasks
  0.3.2 ships. Plugin 0.3.x as a whole is not run headless.
- **Timings:** not measured. A related observation from the plugin's W200
  measurement (3d, 2026-10-09) is that section validation in sdk-ts (about
  400 ms per pass) blocks the §10 latency budgets. That goes to a sdk-ts
  remediation task under LFCP-02-068, not to this task.
