# MVP 0.2 release-candidate report (rc17)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-14. **Host:** Darwin 25.5.0 arm64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc17 is the final candidate, at spec `mvp-0.2-baseline.12`,
and carries the release versions: sdk-ts `@openlfcp/*` **0.2.0** (npm,
dist-tag `latest`) and Shared Tasks **0.4.0** on it. It supersedes **rc16**
(the same spec, sdk-rs and server; sdk-ts 0.2.0-beta.10, plugin
0.4.0-beta.20). Since rc16: sdk-ts 0.2.0 is the code of 0.2.0-beta.10 with
only the versions, dist-tag and CHANGELOG changed; the plugin is 0.4.0 on
`@openlfcp/*` 0.2.0; examples' release sdk-ts pin moves to the 0.2.0
commit.

Pins: [rc17-manifest.json](rc17-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc17.json](mvp-0.2-release-evidence-rc17.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | 0.3.2 plus pin-only commits (`main` is `b96721f`: deploy configuration only) |
| sdk-ts | `2a34beb` | 0.2.0, tag `v0.2.0` (npm, dist-tag `latest`) |
| examples | `e7c3d27` | — |
| obsidian | `ce0660a` | plugin 0.4.0 on `@openlfcp/*` 0.2.0 (branch `rw/plugin-0.4.0`) |
| .github | `1be6b96` | — (branch `rw/mvp-0.2-release-docs`) |

Pins are **consistent**: every `spec.lock`, `server.lock`, `sdk-rs.lock` and
`conformance/pins.json` names the candidate commit, and each obsidian
`@openlfcp/*` dependency is sdk-ts's `0.2.0`, published on npm. Spec HEAD is
the baseline.12 tag commit. The only lag is server `main`, one commit past the
pinned `138030a` (`b96721f`, the deploy configuration; no code). examples'
release sdk-ts pin was moved to `2a34beb` for rc17 (examples `e7c3d27`).

## Gates

All eight rc-verify gates are **green** for rc17 on the first full run,
`report-20261014T191116Z`.

| Gate | Result | Duration |
| --- | --- | --- |
| spec | PASS | 272.9 s |
| .github | PASS | 1.9 s |
| docs | PASS | 0.6 s |
| sdk-rs | PASS | 116.7 s |
| server | PASS | 86.1 s |
| sdk-ts | PASS | 300.1 s |
| examples | PASS | 166.3 s |
| obsidian | PASS | 110.5 s |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=4` and two vitest workers. rc-verify builds `lfcp-server`
once at the server commit and passes `LFCP_SERVER_BIN` to the sdk-ts and
obsidian gates. sdk-ts ran 2470/2470 (140 files, 0 skips) and
`release:check` (version 0.2.0, dist-tag `latest`, pack, install and
import); obsidian ran 1652/1652 (157 files, 0 skips); examples `--strict`
passed with 282 PASS, 2 N/A (known gaps), 0 FAIL, and its tests 33/33 (the
restore rehearsal, run by hand per phase, skips without
`LFCP_REHEARSAL_PHASE`); sdk-rs (both feature sets, 515 passed, 4 ignored)
and server (171 passed, 2 ignored) tests all passed.

## What did not run, and why

- **obsidian native harness** (real Obsidian, LFCP-02-096): run separately by
  the plugin author, not part of the default rc-verify gates (desktop
  session, long). Last run at `4ce8e77` (0.4.0-beta.20, rc16): all 37
  native specs on Obsidian 1.13.4 and 1.14.4, 74/74 runs green on the first
  pass. Since then the plugin changed only its release notes, its version
  (0.4.0) and its `@openlfcp/*` pins (0.2.0, the same code); the desktop
  support matrix
  (LFCP-02-069) is in obsidian `docs/devel/testing/support-matrix-0.2.md`.
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. `@openlfcp/*` 0.2.0 is already published to npm
  under `latest`.
- **Linux and Windows**: this run is macOS. The plugin's Platform smoke
  covers macOS, Windows and Linux in CI.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc17) |
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
| G10 | UX | the Obsidian plugin: obsidian gate 1652/1652, 0 skips; native 74/74 on 1.13.4 and 1.14.4, with real keyboard and mouse moves (Shift+Down, a line selected with the mouse); the desktop support matrix |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples; obsidian upgrade-install (0.3.4 and 0.4.0-beta.15 updated to the candidate) |
| G12 | Release | rc-verify green, `release:check` (0.2.0, dist-tag `latest`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

All eight gates passed on the first full run of rc17. Before it, the pin
check found examples' release sdk-ts pin still at 0.2.0-beta.10
(`d473907`); examples `e7c3d27` moves it to `2a34beb`, and the manifest pins
that commit.

Found by the owner's manual round on 0.4.0-beta.19 and fixed in rc16
(obsidian, in 0.4.0-beta.20), and so in this candidate:

- **Moving a task by cut and paste could damage its binding line.** In
  Live Preview, Shift+Down from a task's line start ends after the next
  line's indentation when that task is nested: the cut took the
  indentation, and the paste gave it to the line it landed on, both
  bindings damaged (`f04c5e3`). A task's line selected with the mouse
  exactly (its hidden binding line below it) was cut without that line,
  left alone and damaged (`a9f14dd`). Both now keep the task whole; a
  delete of such a selection removes the task.
- Native specs `section-shift-down-cut` and `section-whole-line-cut` (real
  keys and mouse): before the fixes they show the owner's damage, with them
  they pass on 1.13.4 and 1.14.4.

The plugin's final acceptance soak of 0.4.0-beta.19 (two hours, offline
periods, server restarts, a removal and a new member) kept pass p50 flat at
98–126 ms through 4,979 changes and every reconnect under 13 s (obsidian
`docs/devel/reports/soak-0.4.0-beta.17.md` §7).

The fixes of rc14, rc15 and rc16 are in this candidate too; see their rows in
[rc-verification.md](rc-verification.md).

## Open items

- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- obsidian `main` is still `4ce8e77`: `ce0660a` (`rw/plugin-0.4.0`) goes to
  `main` with the plugin's `0.4.0` tag, so the catalog sees `manifest.json`
  and `versions.json` at 0.4.0
  ([mvp-0.2-tag-commands.md](mvp-0.2-tag-commands.md)).
- LFCP-02-120 (storage-idb waits on a blocked open) is after 0.2; the plugin
  works around it on start. LFCP-02-121 (serialise receipt release in
  sdk-ts), LFCP-02-122 (no idle IndexedDB work per resource), LFCP-02-123
  (insert a section that has an open conflict) and LFCP-02-124 (Repair
  re-renders bindings) are after 0.2.
