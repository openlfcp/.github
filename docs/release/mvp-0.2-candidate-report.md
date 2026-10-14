# MVP 0.2 release-candidate report (rc14)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-14. **Host:** Linux 7.0.0-38-generic x86_64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc14 is the final candidate, at spec `mvp-0.2-baseline.12`.
It supersedes **rc13** (same spec, server and sdk-rs). Since rc13: sdk-ts
0.2.0-beta.9 (a section's replica keeps one Automerge document, so memory
stays flat as the history grows; a late ACK to an expired flight is still
correlated) and the plugin's 0.4.0 candidate, 0.4.0-beta.18, with the fixes
from the plugin's soak and its peer-structure sweep (see below). 0.4.0-beta.17,
rc13's plugin, was never released.

Pins: [rc14-manifest.json](rc14-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc14.json](mvp-0.2-release-evidence-rc14.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | — |
| sdk-ts | `695cd08` | 0.2.0-beta.9 (npm, dist-tag `beta`) |
| examples | `2345c56` | — |
| obsidian | `af16007` | plugin 0.4.0-beta.18 (manifest-beta.json), the 0.4.0 candidate |
| .github | `83e5f87` | — |

Pins are **consistent**, with no lag: every `spec.lock`, `server.lock`,
`sdk-rs.lock` and `conformance/pins.json` names the candidate commit, and each
obsidian `@openlfcp/*` dependency is sdk-ts's `0.2.0-beta.9`, published on
npm. Spec HEAD is the baseline.12 tag commit. examples' release sdk-ts pin was
moved to `695cd08` for this candidate (examples `2345c56`, branch
`rw/rc14-examples-pin`; the strict run green with it).

## Gates

All eight rc-verify gates are **green** for rc14 in one full run,
`report-20261014T082452Z`.

| Gate | Result | Duration |
| --- | --- | --- |
| spec | PASS | 231.0 s |
| .github | PASS | 0.1 s |
| docs | PASS | 0.1 s |
| sdk-rs | PASS | 57.1 s |
| server | PASS | 38.2 s |
| sdk-ts | PASS | 203.8 s |
| examples | PASS | 145.5 s |
| obsidian | PASS | 48.6 s |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=2`, two Rust test threads and `BUNDLE_FROZEN=true` (the spec
gate on Linux, see [rc-verification.md](rc-verification.md#requirements)).
rc-verify builds `lfcp-server` once at the server commit and passes
`LFCP_SERVER_BIN` to the sdk-ts and obsidian gates. sdk-ts ran 2465/2465 (139
files, 0 skips) and `release:check`; obsidian ran 1638/1638 (155 files, 0
skips); examples `--strict` passed with 282 PASS, 2 N/A (known gaps), 0 FAIL;
sdk-rs (both feature sets) and server tests all passed.

## What did not run, and why

- **obsidian native harness** (real Obsidian, LFCP-02-096): run separately by
  the plugin author, not part of the default rc-verify gates (desktop
  session, long). At `af16007`: all 35 native specs on Obsidian 1.13.4 and
  1.14.4, 70/70 runs green (69 on the first pass; `acceptance-sections` on
  1.14.4 green on its one rerun, see below); the desktop support matrix
  (LFCP-02-069) is in obsidian `docs/devel/testing/support-matrix-0.2.md`.
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. 0.2.0-beta.9 is already published to npm under
  `beta`.
- **macOS and Windows**: this run is Linux. The plugin's Platform smoke
  covers macOS, Windows and Linux in CI.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc14) |
| --- | --- | --- |
| G01 | Baseline | spec gate at mvp-0.2-baseline.12 (official vectors, 49 fixtures); sdk-rs/sdk-ts/server baseline tests green |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` (282 PASS, 2 N/A), sdk-ts/sdk-rs gates |
| G03 | Onboarding | invitation/claim and handshake: sdk-ts live interop + examples E2E; obsidian native `section-remove-invite` (a newcomer after a removal loads) |
| G04 | Content | Shared Objects + Shared Sections through baseline.12 (94 vector cases): sdk-ts `conformance/shared-sections`, obsidian gate and native suite |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates; the section replica's §2 actor kept across apply and revert (sdk-ts differential test) |
| G06 | Concurrency | convergence under faults: sdk-ts live (chaos, access recovery), 2465/2465; obsidian's peer-structure property test (seeds 1–10000; seed 8501 fixed and kept as a regression), its divergence detector, and a headless soak of three plugin peers with offline periods, server restarts and a removal |
| G07 | Durability | storage, crash/restart, snapshot catch-up: sdk-ts storage + live restart; obsidian restart-mid-pass (native), the stale-epoch re-apply; the section replica's memory flat as the history grows (0.2.0-beta.9) |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto |
| G09 | Access | grants, revocation, access recovery: sdk-ts live access recovery; offline work across an access change re-applied (§19.1, §26.2); a Snapshot of the new epoch after a removal (obsidian) |
| G10 | UX | the Obsidian plugin: obsidian gate 1638/1638, 0 skips; native 70/70 on 1.13.4 and 1.14.4; the desktop support matrix |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples; obsidian upgrade-install (0.3.4 and 0.4.0-beta.15 updated to the candidate) |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.9, dist-tag `beta`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

All eight gates passed in one full run of rc14. Before it, while preparing
the candidate:

- **The spec gate in a fresh RC directory** failed before any check: the Ruby
  gems were not installed in the new spec worktree (`vendor/bundle`, as
  `.bundle/config` sets). The same gems, at the same `Gemfile.lock`, were
  copied from rc13's; the spec gate then passed (231 s). Not a spec issue.
- **examples' release sdk-ts pin** named the beta.8 commit (`091f1a9`); moved
  to `695cd08` with the strict run green (examples `2345c56`).
- **Native, `acceptance-sections` on Obsidian 1.14.4** failed one case on the
  first pass of the full suite (a different case in each of two runs: B's
  change not yet at A; a refusal notice not seen in time) while the machine
  was at a load of 9–12 on 12 cores; green on its one rerun at a load of 4,
  and green on 1.13.4 in both runs. Load timing, not the product.

Found by the plugin's soak of 0.4.0-beta.17 (three plugin peers, offline
periods, server restarts, a removal) and fixed for this candidate:

- a member invited after a removal could not load the section (a Snapshot
  of the new epoch is now published, obsidian `05adad7`);
- a section could keep saying "1 local update waiting" after everything was
  accepted (`314fa7c`);
- a reconnect could take up to a minute after an outage (now at most 15 s,
  and at once on focus, `bdcc7d6`);
- a collaborator's delete left the section at "needs attention" with a
  phantom item in Review conflicts (`72d4c2b`, `a8ab6a0`);
- moving one's own Task by cut and paste could delete it for the others
  under load (`ff117a3`);
- a node the note showed and the model hid was not reported (`0c9ad42`);
- a section's memory grew with its history: one old Automerge document kept
  per unchanged Task (sdk-ts 0.2.0-beta.9, `e08aa7c`: 1.6 GiB of wasm memory
  at 2,000 changes with 170 Tasks before, 10 MiB after).

The peer-structure sweep of seeds 5001–10000 found one more: Review
conflicts offered a place under a deleted Task, which could never be applied
(`2f78fb0`). Two soak findings were the test harness's, not the plugin's
(fake-indexeddb kept every transaction: soak passes and memory grew with a
peer's age), fixed in the harness.

## Open items

- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- The SDK release 0.2.0 (from 0.2.0-beta.9) and the plugin's `@openlfcp/*`
  pins moving to it come with the release, after this candidate.
- LFCP-02-120 (storage-idb waits on a blocked open) is after 0.2; the plugin
  works around it on start. LFCP-02-121 (serialise receipt release in
  sdk-ts) and LFCP-02-122 (no idle IndexedDB work per resource) are after
  0.2.
