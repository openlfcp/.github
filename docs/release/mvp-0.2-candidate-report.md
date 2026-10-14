# MVP 0.2 release-candidate report (rc15)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-14. **Host:** Linux 7.0.0-38-generic x86_64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc15 is the final candidate, at spec `mvp-0.2-baseline.12`.
It supersedes **rc14** (same spec, server and sdk-rs). Since rc14: sdk-ts
0.2.0-beta.10 (a section with deleted tasks stays fast as its history grows)
and the plugin's 0.4.0 candidate, 0.4.0-beta.19 (new tasks next to an
unresolved conflict are saved; a new member is told what to do when a
conflict blocks inserting a section). 0.4.0-beta.18, rc14's plugin, was never
released; 0.4.0-beta.17 (rc13's) was.

Pins: [rc15-manifest.json](rc15-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc15.json](mvp-0.2-release-evidence-rc15.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | — |
| sdk-ts | `d473907` | 0.2.0-beta.10 (npm, dist-tag `beta`) |
| examples | `ae36811` | — |
| obsidian | `43c7ce2` | plugin 0.4.0-beta.19 (manifest-beta.json), the 0.4.0 candidate |
| .github | `e02f6d1` | — |

Pins are **consistent**, with no lag: every `spec.lock`, `server.lock`,
`sdk-rs.lock` and `conformance/pins.json` names the candidate commit, and each
obsidian `@openlfcp/*` dependency is sdk-ts's `0.2.0-beta.10`, published on
npm. Spec HEAD is the baseline.12 tag commit. examples' release sdk-ts pin was
moved to `d473907` for this candidate (examples `ae36811`, branch
`rw/rc15-examples-pin`; the strict run green with it).

## Gates

All eight rc-verify gates are **green** for rc15 on the first full run,
`report-20261014T134136Z`.

| Gate | Result | Duration |
| --- | --- | --- |
| spec | PASS | 228.4 s |
| .github | PASS | 0.1 s |
| docs | PASS | 0.1 s |
| sdk-rs | PASS | 76.6 s |
| server | PASS | 89.2 s |
| sdk-ts | PASS | 206.5 s |
| examples | PASS | 148.3 s |
| obsidian | PASS | 49.5 s |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=2`, two Rust test threads and `BUNDLE_FROZEN=true` (the spec
gate on Linux, see [rc-verification.md](rc-verification.md#requirements)).
rc-verify builds `lfcp-server` once at the server commit and passes
`LFCP_SERVER_BIN` to the sdk-ts and obsidian gates. sdk-ts ran 2470/2470 (140
files, 0 skips) and `release:check`; obsidian ran 1642/1642 (156 files, 0
skips); examples `--strict` passed with 282 PASS, 2 N/A (known gaps), 0 FAIL;
sdk-rs (both feature sets) and server tests all passed.

## What did not run, and why

- **obsidian native harness** (real Obsidian, LFCP-02-096): run separately by
  the plugin author, not part of the default rc-verify gates (desktop
  session, long). At `43c7ce2`: all 35 native specs on Obsidian 1.13.4 and
  1.14.4, 70/70 runs green on the first pass; the desktop support matrix
  (LFCP-02-069) is in obsidian `docs/devel/testing/support-matrix-0.2.md`.
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. 0.2.0-beta.10 is already published to npm under
  `beta`.
- **macOS and Windows**: this run is Linux. The plugin's Platform smoke
  covers macOS, Windows and Linux in CI.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc15) |
| --- | --- | --- |
| G01 | Baseline | spec gate at mvp-0.2-baseline.12 (official vectors, 49 fixtures); sdk-rs/sdk-ts/server baseline tests green |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` (282 PASS, 2 N/A), sdk-ts/sdk-rs gates |
| G03 | Onboarding | invitation/claim and handshake: sdk-ts live interop + examples E2E; obsidian native `section-remove-invite` (a newcomer after a removal loads) |
| G04 | Content | Shared Objects + Shared Sections through baseline.12 (94 vector cases): sdk-ts `conformance/shared-sections`, obsidian gate and native suite |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates; the section replica's §2 actor kept across apply and revert (sdk-ts differential test) |
| G06 | Concurrency | convergence under faults: sdk-ts live (chaos, access recovery), 2470/2470; obsidian's peer-structure property test (seeds 1–10000; seed 8501 fixed and kept as a regression), its divergence detector, and a headless soak of three plugin peers with offline periods, server restarts and a removal |
| G07 | Durability | storage, crash/restart, snapshot catch-up: sdk-ts storage + live restart; obsidian restart-mid-pass (native), the stale-epoch re-apply; the section replica's memory flat as the history grows (0.2.0-beta.9) and its passes fast with deleted tasks (0.2.0-beta.10) |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto |
| G09 | Access | grants, revocation, access recovery: sdk-ts live access recovery; offline work across an access change re-applied (§19.1, §26.2); a Snapshot of the new epoch after a removal (obsidian) |
| G10 | UX | the Obsidian plugin: obsidian gate 1642/1642, 0 skips; native 70/70 on 1.13.4 and 1.14.4; the desktop support matrix |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples; obsidian upgrade-install (0.3.4 and 0.4.0-beta.15 updated to the candidate) |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.10, dist-tag `beta`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

All eight gates passed on the first full run of rc15. Before it: examples'
release sdk-ts pin named the beta.9 commit (`695cd08`); moved to `d473907`
with the strict run green (examples `ae36811`). The spec worktree's Ruby
gems (`vendor/bundle`) were copied from rc14's, at the same `Gemfile.lock`.

Found by the plugin's acceptance soak of 0.4.0-beta.18 and fixed for this
candidate:

- **A section with deleted tasks got slower as its history grew**: each
  read of its tree compared every change with all its ancestors (pass p50
  ~1 s and p95 4–6 s after ~3,000 changes). sdk-ts 0.2.0-beta.10 (`35b4c7f`)
  decides concurrency with vector clocks, reuses the decoded history between
  revisions and derives the tree once per revision: at 6,000 changes with
  300 deleted tasks, a pass takes 200 ms against 746 ms, and a status read
  no longer derives the tree again. The results are identical to beta.9's
  (300 random histories).
- **New tasks next to an unresolved conflict failed to save** ("Local save
  failed", INVALID_PREDECESSOR): the batch is now planned around a
  predecessor the SDK refuses (obsidian `01231e4`).
- **A new member could not tell why a section would not insert** while it
  had a conflict: the notice now says who can resolve it and how
  (`0c87bc3`; LFCP-02-123 lifts the refusal itself).

The fixes of rc14 (a newcomer after a removal, the stuck "waiting", the
reconnect, the false "needs attention", cut and paste, a hidden node,
memory flat with history, the Review conflicts dead end) are in this
candidate too; see rc14's row in [rc-verification.md](rc-verification.md).

## Open items

- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- The SDK release 0.2.0 (from 0.2.0-beta.10) and the plugin's `@openlfcp/*`
  pins moving to it come with the release, after this candidate.
- LFCP-02-120 (storage-idb waits on a blocked open) is after 0.2; the plugin
  works around it on start. LFCP-02-121 (serialise receipt release in
  sdk-ts), LFCP-02-122 (no idle IndexedDB work per resource) and LFCP-02-123
  (insert a section that has an open conflict) are after 0.2.
