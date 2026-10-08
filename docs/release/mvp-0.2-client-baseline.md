# MVP 0.2 client baseline (LFCP-02-002)

**Status:** Evidence for LFCP-02-002, 2026-10-08. The inherited client
security and durability checks of sdk-ts, run on the W0 release set; no
crypto is mocked. Statuses come from these runs, not from the state of the
0.1 issues.

## 1. Runs

| Run | Build | Command | Result |
| --- | --- | --- | --- |
| rc9 (release gates) | sdk-ts 777f36e on spec `mvp-0.1-baseline.9` (f42533c), server 09c9132, sdk-rs 259a688 ([rc9-manifest.json](rc9-manifest.json)) | rc-verify sdk-ts gate: `pnpm install --frozen-lockfile`, `build`, `typecheck`, `lint`, `test` with `LFCP_REQUIRE_LIVE=1`, `release:check` | **PASS**, 146.8 s, 96 files, 1638 tests, Darwin 25.5.0 arm64 ([rc-verification.md](rc-verification.md), rc9) |
| Local full suite | sdk-ts e9cdb43 (0.1.3 plus the engine-trap isolation, LFCP-02-099), same pins | `pnpm test` with `LFCP_REQUIRE_LIVE=1`, two workers | **PASS**, 1638 tests; engine-trap last, 68.1 s |
| CI | sdk-ts 777f36e, ubuntu-latest | `.github/workflows/ci.yml` | **FAIL** on attempt 1: one live test, a race in the test itself (the reader opened before the owner re-supplied its grant); fixed by 1d00993, product code unchanged; the remaining behaviour is LFCP-02-106 |

## 2. Checks by area

| Area | Where (sdk-ts) | Status |
| --- | --- | --- |
| Signatures (COSE, strict Ed25519, signer binding) | `packages/wire/test/cose.test.ts`, `packages/crypto/test/ed25519-strict.test.ts`, `conformance/wire` vectors (`validation/*` signature cases) | PASS |
| AEAD (Data Units, Snapshots) | `packages/crypto/test/aead.test.ts`, `packages/wire/test/data-unit.test.ts`, `packages/wire/test/snapshot.test.ts`, wire vectors `bytes/data_unit`, `bytes/snapshot` and their negatives | PASS |
| Keys (DEK, actor keys, HPKE Key Packages, invitation secret) | `packages/crypto/test/keys.test.ts`, `hpke.test.ts`, `invitation.test.ts`, `packages/wire/test/key-package.test.ts`, wire vectors `bytes/key_package`, `bytes/dek_commitment` | PASS |
| Control Plane (chain, transitions, CAS) | `packages/wire/test/chain.test.ts`, `control.test.ts`, `transition.test.ts`, `control-sync.test.ts`, `transfer.test.ts`, wire vectors `bytes/control_record`, `validation/control_put` | PASS |
| Capabilities and authority | `packages/wire/test/capability.test.ts`, `conformance/wire/authority.test.ts`, live `conformance/interop/rust-server-invite.test.ts` (one-time claim, races) | PASS |
| Epoch rotation and strict cutoff | `packages/wire/test/epoch.test.ts`, `packages/crypto/test/epoch.test.ts`, `conformance/wire/epoch.test.ts`, `conformance/shared-objects/own-unit-rebuild.test.ts`, `snap-ep.test.ts` | PASS |
| Snapshots (codec, load, publish, cutoff) | `packages/wire/test/snapshot.test.ts`, `packages/client/test/snapshot.test.ts`, live `conformance/interop/rust-server-snapshot.test.ts` | PASS |
| Actor persistence and restarts | `packages/storage/test/sequence.test.ts`, `packages/storage-node/test/crash.test.ts`, `conformance/persistence/restart-state.test.ts`, `crash-points.test.ts`, `conformance/storage/outbound-restart.test.ts`, `writer-previous-restart.test.ts`, live `rust-server-restart.test.ts` (no sequence reuse across kills) | PASS |
| Recovery after server data loss (ADR 0008) and held collisions (POST-001) | live `conformance/interop/rust-server-recovery.test.ts`, `chaos.test.ts` (seeds 1–3), `conformance/shared-objects/data-unit-apply.test.ts` (POST-001), the collision corpus | PASS |
| Hostile input (ReDoS, decompression, depth, engine trap) | `conformance/security/redos.test.ts`, `packages/shared-objects/test/chunk-limits.test.ts`, `depth.test.ts`, `engine-safety.test.ts`, `conformance/security/engine-trap.test.ts` | PASS |
| Wire vectors as a whole | `conformance/wire/vectors.test.ts` and `conformance/shared-objects/vectors.test.ts` at baseline.9, no pending entry; cross-language: examples `conformance/dist/run.js --strict`, 0 blocking | PASS |

## 3. H1, H7 and M1 alignment

The summary table of [security-review-mvp-0.1.md](security-review-mvp-0.1.md)
still reads "SDK alignment pending" for H1, H7 and M1. The release notes
([mvp-0.1-release-notes.md](mvp-0.1-release-notes.md), "Hardening") and the
code show them shipped in 0.1.0: the change and Snapshot expansion checks
(sdk-ts f135410 with the baseline.7 vectors), the 256-level depth bound
(sdk-ts 68ce58d, af6e6f1; sdk-rs 50cb6bf) and the client's own receive
limit (sdk-ts 9b61644, sdk-rs b1d08bd). The tests above run them at
baseline.9. The table is only stale.

## 4. Not run, and what remains

| Item | Status | Owner |
| --- | --- | --- |
| Native editor and IME paths | NOT_RUN here (not an SDK check) | obsidian, LFCP-02-096, ADR 0001 IME condition |
| Windows and Linux client runs | NOT_RUN locally; CI ubuntu covers sdk-ts, obsidian platform smoke covers three systems | — |
| G-EP7 cross-check between the SDKs | NOT_RUN: examples `conformance/known-gaps.json` defers it | LFCP-02-023/024 |

No check failed, so this audit opens no defect. The known open items stay
with their tasks: plaintext local checkpoints (M10, POST-006: LFCP-02-098),
Snapshot publishing by the plugin (POST-007: LFCP-02-097), a member
refused before its grant is re-supplied (LFCP-02-106), and the stale
security-review table (a docs fix, §3).
