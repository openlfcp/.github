# MVP 0.2 release-candidate report (rc12)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-12. **Host:** Darwin 25.5.0 arm64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc12 is the final candidate, at spec `mvp-0.2-baseline.10`.
It supersedes **rc11** (spec `mvp-0.2-baseline.9`): after rc11, rw found three
sdk-rs issues — E1 (§14.1 holds a change at a taken sequence number before the
structural rules), E2 (A5 refuses a scalar written to a node's `text` whatever
its kind) and F1 (§14.1 names a chunk whose dependencies or actor do not read).
All three are made explicit at baseline.10 (SS88–SS91, 91 cases) and fixed in
sdk-rs; the sdk-ts production already behaved correctly, so only its conformance
adapter changed (SS88's held-at-taken-sequence refusal). rc12 is the first run
where every gate passes on the first full pass, with no patched-tool reruns.

Pins: [rc12-manifest.json](rc12-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc12.json](mvp-0.2-release-evidence-rc12.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `a3161f7` | mvp-0.2-baseline.10 |
| sdk-rs | `74c3a71` | — |
| server | `814e913` | 0.3.1 |
| sdk-ts | `a40347c` | 0.2.0-beta.5 (npm, dist-tag `beta`) |
| examples | `1bfd20e` | — |
| obsidian | `3780ca3` | plugin 0.4.0-beta.5 (manifest-beta.json) |
| .github | `b0b2ac1` | — |

Pins are **consistent**: every `spec.lock`, `server.lock`, `sdk-rs.lock` and
`conformance/pins.json` names the candidate commit, and each obsidian
`@openlfcp/*` dependency is sdk-ts's `0.2.0-beta.5`, published on npm. One pin
lags its repository HEAD, neither normative and both after the candidate:
examples' sdk-ts pin trails `3cd3b61` (README to baseline.10) and `d2a68d6`
(the chaos interop-timer determinization, test-only). Spec HEAD is the
baseline.10 tag commit.

## Gates

All eight rc-verify gates are **green** for rc12 on the first full run,
`report-20261012T063313Z` — no patched-tool rerun was needed (the server-bin
and dist-clean fixes from rc11 are now in `.github` main).

| Gate | Result | Duration |
| --- | --- | --- |
| spec | PASS | 267.0 s |
| .github | PASS | 0.3 s |
| docs | PASS | 0.8 s |
| sdk-rs | PASS | 82.6 s |
| server | PASS | 79.0 s |
| sdk-ts | PASS | 200.6 s |
| examples | PASS | 170.3 s |
| obsidian | PASS | 30.6 s |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=2`, two Rust test threads, one shared Cargo/server target in
`~/Library/Caches` (not `$TMPDIR`); rc-verify builds `lfcp-server` once at the
server commit and passes `LFCP_SERVER_BIN` to the sdk-ts and obsidian gates.
sdk-ts ran 2396/2396 (134 files, 0 skips); obsidian ran 1215/1215 (0 skips);
examples `--strict` passed with rust 299/299 and ts 128/128 + 31/31.

## What did not run, and why

- **obsidian native harness** (`pnpm run native`, real Obsidian, LFCP-02-096):
  run separately by the plugin author (3d), not part of the default rc-verify
  gates (desktop session, long).
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. beta.5 is already published to npm under `beta`.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc12) |
| --- | --- | --- |
| G01 | Baseline | spec gate at mvp-0.2-baseline.10 (official vectors); sdk-rs/sdk-ts/server baseline tests green |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` (ts 128/128 + 31/31, rust 299/299, negatives), sdk-ts/sdk-rs gates |
| G03 | Onboarding | invitation/claim and handshake: sdk-ts live interop + examples E2E |
| G04 | Content | Shared Objects + Shared Sections through baseline.10 (SS88–SS91 making §14.1/A5 explicit, E1/E2/F1): sdk-ts `conformance/shared-sections`, [sections-conformance](mvp-0.2-sdk-ts-sections-conformance.md), obsidian |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates |
| G06 | Concurrency | convergence under faults: sdk-ts live (chaos LFCP-057, access recovery); chaos recovery timers determinized (below) — full suite 2396/2396 |
| G07 | Durability | storage, crash/restart, snapshot catch-up: sdk-ts storage + live restart; [restore-rehearsal](mvp-0.2-restore-rehearsal.json), [integrated-recovery](mvp-0.2-integrated-recovery-qualification.md) |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto |
| G09 | Access | grants, revocation, access recovery: sdk-ts `rust-server-access-recovery` (6/6), examples |
| G10 | UX | the Obsidian plugin: obsidian gate 1215/1215, 0 skips; native one run (above) |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples LFCP-070, [two-vault](mvp-0.2-two-vault-qualification.md) |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.5, dist-tag `beta`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

None in rc12 — every gate passed on the first full run.

**chaos seed 3, resolved since rc11.** rc11's one off-nominal result was a
chaos seed-3 convergence timeout under full-suite load (not a protocol defect;
it passed in isolation). Diagnosis: the interop harness had lowered only the
pull-path anti-entropy timer for tests, leaving the push-path request timeout
(`OutboundQueue`, 10→60 s) and the request-timeout re-issue (15 s) at their
production values, so recovery after a dropped put or lost ACK waited out those
production timers — a 10 s-to-41 s swing. Fixed test-only in sdk-ts `d2a68d6`
(the chaos recovery timers are now tuned per side; scenarios 13–15 still prove a
retransmit-after-timeout, with anti-entropy turned off where they must). In rc12
the sdk-ts full live suite is 2396/2396 with no off-load failure.

## Open items

- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- The one-commit examples sdk-ts pin lag (→`3cd3b61`, `d2a68d6`) is docs/
  test-only and after the candidate; fold it in at the next pin move if a
  further baseline follows.
