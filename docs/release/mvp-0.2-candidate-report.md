# MVP 0.2 release-candidate report (rc11)

**Task:** LFCP-02-073 (end-to-end verification of the final candidate).
**Date:** 2026-10-12. **Host:** Darwin 25.5.0 arm64.
**Candidate status:** `NOT_QUALIFIED` — the scope gates, the owner's manual
checks and the pilot are reviewed by people; this report is the local,
automated evidence that every release-blocking gate is green for one pinned
set of commits.

**Supersession:** rc11 is the candidate at spec `mvp-0.2-baseline.9`. After
this run, rw found three sdk-rs issues (E1, E2, F1), fixed at spec
`mvp-0.2-baseline.10` (prepared, 91 cases) and sdk-rs `cf8dcb6`; sdk-ts already
behaved correctly. The final candidate will be **rc12 at baseline.10** —
rc11 is superseded by it. The gate evidence here still stands for the .9 set.

Pins: [rc11-manifest.json](rc11-manifest.json). Evidence record:
[mvp-0.2-release-evidence-rc11.json](mvp-0.2-release-evidence-rc11.json).
Tooling: [rc-verification.md](rc-verification.md).

## Candidate commits

| Repository | Commit | Version / tag |
| --- | --- | --- |
| spec | `369c22b` | mvp-0.2-baseline.9 |
| sdk-rs | `82901af` | — |
| server | `4ea72f0` | 0.3.1 |
| sdk-ts | `f04703f` | 0.2.0-beta.4 (npm, dist-tag `beta`) |
| examples | `e38184e` | — |
| obsidian | `c004843` | plugin 0.4.0-beta.4 |
| .github | `e1800e6` | — |

Pins are **consistent**: every `spec.lock`, `server.lock`, `sdk-rs.lock` and
`conformance/pins.json` names the candidate commit, and each obsidian
`@openlfcp/*` dependency is sdk-ts's `0.2.0-beta.4`, published on npm. Two pins
lag their repository HEAD by one commit, both after the candidate and neither
normative: examples' sdk-ts pin trails `a64d8ba` (README to baseline.9), and
obsidian trails `8fa41c8` (a native UX09 focus-test fix). Spec HEAD carries no
commit after the baseline.9 tag.

## Gates

All eight rc-verify gates are **green** for rc11. The first full run is
`report-20261011T213247Z`; two gates needed a tooling fix and a reused-worktree
cleanup, re-run green with the patched tool (see Issues).

| Gate | Result | Proven by |
| --- | --- | --- |
| spec | PASS | full run (263 s) |
| .github | PASS | full run |
| docs | PASS | full run |
| sdk-rs | PASS | full run (113 s) |
| server | PASS | full run (83 s) |
| sdk-ts | PASS | patched tool `report-20261011T220310Z` (238 s) |
| examples | PASS | full run (157 s) |
| obsidian | PASS | patched tool `report-20261011T215749Z` (23 s) |

Every gate ran with `LFCP_REQUIRE_LIVE=1` (live tests may not skip),
`CARGO_BUILD_JOBS=4`, two Rust test threads, one shared Cargo/server target in
`~/Library/Caches` (not `$TMPDIR`). The obsidian gate fails if any test is
skipped; it ran 1214/1214 with no skips.

## What did not run, and why

- **obsidian native harness** (`pnpm run native`, real Obsidian, LFCP-02-096):
  one run only, by the plugin author (3d), on Obsidian 1.13.4 — 57 pass, the
  UX09 window-focus check the exception; that check pre-exists on `8fa41c8` and
  is unrelated to the candidate (it was then fixed on `8fa41c8`, after the
  candidate). Not part of the default rc-verify gates (desktop session, long).
- **Owner manual checks** (`mvp-0.2-owner-checklist.md`): NOT RUN — the owner's.
- **Pilot** (real two-vault field use): NOT RUN — the owner's.
- **`--assemble` candidate artifacts** (npm tarballs, server binaries, plugin
  files, `--repro`): NOT RUN this pass; the owner assembles the immutable
  artifacts at release. beta.4 is already published to npm under `beta`.

## Scope gates G01–G12

These are reviewed by people (the evidence record's `decision` is
`NOT_REVIEWED`). The automated evidence this candidate supplies:

| Gate | Name | Automated evidence (rc11) |
| --- | --- | --- |
| G01 | Baseline | spec gate at mvp-0.2-baseline.9 (official vectors); sdk-rs/sdk-ts/server baseline tests green |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` (ts 128/128 + 31/31, rust 295/295, negatives), sdk-ts/sdk-rs gates |
| G03 | Onboarding | invitation/claim and handshake: sdk-ts live interop + examples E2E |
| G04 | Content | Shared Objects + Shared Sections through baseline.9 (re-delete §9, SS83–SS87): sdk-ts `conformance/shared-sections`, [sections-conformance](mvp-0.2-sdk-ts-sections-conformance.md), obsidian |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates |
| G06 | Concurrency | convergence under faults: sdk-ts live (chaos LFCP-057, access recovery); chaos seed 3 proven stable (below) |
| G07 | Durability | storage, crash/restart, snapshot catch-up: sdk-ts storage + live restart; [restore-rehearsal](mvp-0.2-restore-rehearsal.json), [integrated-recovery](mvp-0.2-integrated-recovery-qualification.md) |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto |
| G09 | Access | grants, revocation, access recovery: sdk-ts `rust-server-access-recovery` (6/6), examples |
| G10 | UX | the Obsidian plugin: obsidian gate 1214/1214, 0 skips; native one run (above) |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client: examples LFCP-070, [two-vault](mvp-0.2-two-vault-qualification.md) |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.4, dist-tag `beta`, pack+install+import), npm published; this report and manifest |

## Issues found and resolved

1. **obsidian live gate incompatible with rc-verify (tooling).** rc-verify
   removed `LFCP_SERVER_BIN` and relied on each gate building its own server at
   a default target path, but the obsidian live harness
   (`test/support/server-pin.mjs`) now **requires** `LFCP_SERVER_BIN` and
   refuses a default location. The obsidian gate therefore failed every run (8
   live files, 1168 non-live passing). Fix: **.github `rc-verify-server-bin`** —
   rc-verify builds `lfcp-server` once at the manifest's server commit and
   passes its path as `LFCP_SERVER_BIN` to the sdk-ts and obsidian gates. With
   the patch the obsidian gate is 1214/1214, 0 skips.

2. **sdk-ts live flakiness under load + stale dist in the reused worktree.** The
   first full run's sdk-ts gate failed with a transient `spawn … lfcp-server
   ENOENT` (a server restart racing a concurrent build in the shared target)
   and a chaos seed-3 convergence timeout under full-suite load. The patch (one
   pre-built server) removes the build race; `pnpm test` then passed, exposing a
   second, independent issue: a **stale `dist/`** (`automerge-bytes.*`,
   `chunk-limits.*`) left in the reused RC worktree from an older commit, which
   `release:check` correctly rejected. After clearing the stale `dist/`, the
   patched sdk-ts gate is green.

   **chaos seed 3 is not a correctness finding:** run 5× standalone (5/5,
   20/20 each) and 2× in the full sdk-ts live suite (2/2, 2380/2380 each) — it
   never failed off-load. The original failure was a convergence timeout under
   contention, not a protocol defect.

## Open items

- **rc-verify stale-dist hygiene (follow-up):** the reused RC sdk-ts worktree
  can carry a `dist/` from an older commit across a commit switch, which breaks
  `release:check`. A clean checkout (CI) is unaffected. Consider clearing the
  package `dist/` before the sdk-ts gate; not folded into the server-bin fix.
- **Owner:** run the manual checklist and the pilot; assemble the immutable
  artifacts (`--assemble --repro`); then the scope-gate verdicts (G01–G12) and
  the release decision.
- The two one-commit pin lags (examples→a64d8ba, obsidian→8fa41c8) are docs/
  test-only and after the candidate; fold them in at the next pin move if a
  further baseline follows.
