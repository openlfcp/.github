# MVP 0.2 release-candidate report (rc13)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-14. **Host:** Linux 7.0.0-38-generic x86_64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc13 is the final candidate, at spec `mvp-0.2-baseline.12`.
It supersedes **rc12** (spec `mvp-0.2-baseline.10`). Since rc12: baseline.11
and .12 (concurrent equal scalar values agree; the shared-sections corpus to
94 cases and 49 Markdown fixtures), the reference server at `138030a`, sdk-ts
0.2.0-beta.8 (after a member's first unit went stale, the next unit names no
previous unit, §26.2) and the plugin's 0.4.0 candidate, 0.4.0-beta.17. rc13
is the first full run on Linux; every gate passed on the first full pass.

Pins: [rc13-manifest.json](rc13-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc13.json](mvp-0.2-release-evidence-rc13.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | — |
| sdk-ts | `091f1a9` | 0.2.0-beta.8 (npm, dist-tag `beta`) |
| examples | `338a1d5` | — |
| obsidian | `b59c651` | plugin 0.4.0-beta.17 (manifest-beta.json), the 0.4.0 candidate |
| .github | `b4fa6e7` | — |

Pins are **consistent**, with no lag: every `spec.lock`, `server.lock`,
`sdk-rs.lock` and `conformance/pins.json` names the candidate commit, and each
obsidian `@openlfcp/*` dependency is sdk-ts's `0.2.0-beta.8`, published on
npm. Spec HEAD is the baseline.12 tag commit. examples' release sdk-ts pin was
moved to `091f1a9` for this candidate (examples `338a1d5`; the strict run green
before and after).

## Gates

All eight rc-verify gates are **green** for rc13 on the first full run,
`report-20261014T011503Z`.

| Gate | Result | Duration |
| --- | --- | --- |
| spec | PASS | 225.9 s |
| .github | PASS | 0.1 s |
| docs | PASS | 0.1 s |
| sdk-rs | PASS | 62.3 s |
| server | PASS | 46.0 s |
| sdk-ts | PASS | 171.0 s |
| examples | PASS | 146.5 s |
| obsidian | PASS | 39.4 s |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=2`, two Rust test threads and `BUNDLE_FROZEN=true` (the spec
gate on Linux, see [rc-verification.md](rc-verification.md#requirements)).
rc-verify builds `lfcp-server` once at the server commit and passes
`LFCP_SERVER_BIN` to the sdk-ts and obsidian gates. sdk-ts ran 2458/2458 (137
files, 0 skips) and `release:check`; obsidian ran 1609/1609 (0 skips); examples
`--strict` passed with 282 PASS, 2 N/A (known gaps), 0 FAIL; sdk-rs (both
feature sets) and server tests all passed. A dry run with obsidian at
0.4.0-beta.16 (`fe3ec6e`) was green as well (`report-20261013T224724Z`).

## What did not run, and why

- **obsidian native harness** (real Obsidian, LFCP-02-096): run separately by
  the plugin author, not part of the default rc-verify gates (desktop
  session, long). At `b59c651`: all 34 native specs on Obsidian 1.13.4 and
  1.14.4, 68/68 runs green on the first pass; the desktop support matrix
  (LFCP-02-069) is in obsidian `docs/devel/testing/support-matrix-0.2.md`.
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. 0.2.0-beta.8 is already published to npm under
  `beta`.
- **macOS and Windows**: this run is Linux. The plugin's Platform smoke
  covers macOS, Windows and Linux in CI.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc13) |
| --- | --- | --- |
| G01 | Baseline | spec gate at mvp-0.2-baseline.12 (official vectors, 49 fixtures); sdk-rs/sdk-ts/server baseline tests green |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` (282 PASS, 2 N/A), sdk-ts/sdk-rs gates |
| G03 | Onboarding | invitation/claim and handshake: sdk-ts live interop + examples E2E |
| G04 | Content | Shared Objects + Shared Sections through baseline.12 (equal concurrent values agree; 94 vector cases): sdk-ts `conformance/shared-sections`, obsidian gate and native suite |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates |
| G06 | Concurrency | convergence under faults: sdk-ts live (chaos, access recovery), 2458/2458; obsidian's peer-structure property test (seeds 1–5000 green) and its divergence detector |
| G07 | Durability | storage, crash/restart, snapshot catch-up: sdk-ts storage + live restart; obsidian restart-mid-pass (native) and the stale-epoch re-apply |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto |
| G09 | Access | grants, revocation, access recovery: sdk-ts live access recovery; offline work across an access change re-applied (§19.1, §26.2) |
| G10 | UX | the Obsidian plugin: obsidian gate 1609/1609, 0 skips; native 68/68 on 1.13.4 and 1.14.4; the desktop support matrix |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples; obsidian upgrade-install (0.3.4 and 0.4.0-beta.15 updated to the candidate) |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.8, dist-tag `beta`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

Every gate passed on the first full run of rc13. Before it, while preparing
the candidate:

- **The spec gate on Linux** failed before any check: the Ruby gems were not
  installed, and then `bundle check` added Bundler's own checksum to the
  tracked `Gemfile.lock`. Not a spec issue: rc-verify now documents
  `BUNDLE_FROZEN=true` for Linux (`.github` f318474).
- **sdk-ts** had two 5 s test timeouts while native runs loaded the machine;
  green on a quiet rerun and in every full run since.
- **examples' release sdk-ts pin** still named the baseline.12 commit
  (`95fd9ef`); moved to `091f1a9` with the strict run green (examples
  `338a1d5`).

Found by the plugin's verification for this candidate and fixed before it
(obsidian, all in 0.4.0-beta.17): the update from 0.3.4 in one Obsidian window
could leave the plugin not running (the writer lock is now taken before the
database opens, `2fa1249`); a note open only in Reading view lost a
collaborator's edit, the badge CURRENT (`547921c`); and, since rc12, the
seed race on sharing, the silent-divergence detector and the peer-structure
fixes of 0.4.0-beta.13 to .16.

## Open items

- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- The SDK release 0.2.0 (from 0.2.0-beta.8) and the plugin's `@openlfcp/*`
  pins moving to it come with the release, after this candidate.
- LFCP-02-120 (storage-idb waits on a blocked open) is after 0.2; the plugin
  works around it on start.
