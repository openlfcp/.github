# MVP 0.3 go/no-go: gate review of Shared Tasks 0.5.0

**Task:** LFCP-03-029 (M03-5). **Date:** 2026-10-19. **Tracker:**
[#1](https://github.com/openlfcp/.github/issues/1).
**Verdict:** **GO_WITH_OWNER_WAIVERS** (see [Verdict](#verdict)).
**Owner confirmation: pending.**

This document records the state of the release as it is. It does not
authorise anything: Shared Tasks 0.5.0 was already published by the owner on
2026-10-19 (tag `0.5.0`, obsidian commit `f50e064`, release workflow run
[39241767276](https://github.com/openlfcp/obsidian/actions/runs/39241767276),
green; website PR [openlfcp/website#1](https://github.com/openlfcp/website/pull/1)
merged). The review checks the gates of the MVP 0.3 scope against primary
evidence (CI runs, merged pull requests, reports in the plugin repository), not
against task status: a task marked done is not a PASS.

**Method.** The gate definitions, the acceptance corpus U03-01..30 and the
severity rules come from the MVP 0.3 scope and test-and-release plan.
Evidence was read at its source: the CI run results and job lists were queried
with `gh run view`; the published `main.js`, `manifest.json` and `styles.css`
were downloaded and hashed; `gh attestation verify` was run on `main.js`
(exit 0); the diff of `src/`, `styles.css`, `pnpm-lock.yaml` and `test/`
between the qualified commit `1eda57a` and the tag commit `f50e064` was
checked (empty; the delta is CHANGELOG, notes and reports). The reviewer did
not re-run the test suites. Reports are those on obsidian `main`
(`docs/devel/reports/`), cited by name below.

**Status words.** `PASS`; `PASS_WITH_FINDINGS` (the gate condition holds, named
findings remain); `WAIVED_BY_OWNER` (the condition is not met and the owner
decided to ship without it, decision number given); `FAIL`. No gate is FAIL.

## Release identity

| Item | Value |
| --- | --- |
| Plugin | Shared Tasks 0.5.0, tag `0.5.0` = `f50e064`; qualified build `1eda57a`, same `src/`, styles and lockfile |
| `main.js` sha256 | `35fb226f28ddb6378ef85a425014873dbc96a63b0e6dcf348e8ed932ab9bae31` (release page, notes and candidate manifest agree; re-hashed here) |
| `manifest.json` sha256 | `5500adc55a32565311a9ad93745946540501045bf2c1eb6715ab84eed9139667` (agrees) |
| `styles.css` sha256 | `373028272ef8c3ed42c2c6b3b3c45ffaec3d030ee3ddd6b6163366d5f91a67c1` (agrees) |
| Provenance | build attestation verified; release run 39241767276 success |
| Pins | `@openlfcp/*` 0.2.2, spec `mvp-0.2-baseline.12`, server lock `138030a` (reference server 0.3.2), Tasks 8.4.0, Obsidian 1.13.4 and 1.14.4 |
| Baseline | plugin 0.4.0 (`ce0660a`), `@openlfcp/*` 0.2.0, spec `mvp-0.2-baseline.12`, server 0.3.2 |

## Gate matrix

| Gate | Requirement (short) | Evidence | Status | Residual risk |
| --- | --- | --- | --- | --- |
| G03-A | Pins, authority and baseline repairs F-03, F-04, F-05 confirmed | Baseline manifest, authority map and gap register (this folder). F-03 second Share: LFCP-03-002 (obsidian#4) and the second race, LFCP-03-058 (#71); U03-09 by `create`, `share-reservation` and live-discard tests and native `section-share-reservation`. F-04 held source: 003 (#2), 005 (#5), 047 (#44), 057 (#70); U03-25. F-05 legacy resolver: 004 (#1); U03-24. Native confirmation: native matrix report (025, #61) and harness in CI (031). The gap register is a 2026-10-15 snapshot and still shows F-03..F-05 as PARTIAL/OPEN; it was not updated. | PASS | 0.4.1 and 0.4.2 keep the double-creation race (no 0.4.3, listed in the release notes). Pre-damaged Resources are repaired by #77 (063). Gap register is stale and should be read with this table. |
| G03-B | Share, join, insert and problem reachable from visible entries without commands | Pane host, ribbon and card entries (012, #20-#24, #29); single handler for pane, palette, card and menu (010, 023; action-seam report); native `pane-*` specs and the two-real-Obsidian flow with the ribbon only (`two-hosts`, U03-29): PASS on Linux, macOS and Windows, Tasks on and off, 1.13.4 and 1.14.4. Beta.2 full matrix 39215441248. | PASS_WITH_FINDINGS | F7: `pane-access-copy-detach` failed once at first attempt in beta.2 (Linux 1.13.4, a dialog did not open) after the first-click fix (#74); classified "product defect or click race, not settled", log not kept. Related: #87 (duplicate Repair button in the pane). |
| G03-C | Correct selection, target and focus; no write to another note | U03-03/04/05/12/15/20/26: stable target and exact selection (009, 010), journeys (014-016), interruption qualification (024) with native `section-stable-target` and `pane-insert`; content policy per pinned spec; private canaries not in payload. | PASS | Obsidian's own "modified externally, merging changes" can drop an untouched line when two panes show one note (F3, Windows). Data stays in the model and Repair offers the line back (#70); it does not write to another note. See G03-F for the recurrence on the 0.5.0 build. |
| G03-D | Journals, receipts and restart keep identity, source and result | U03-09..14, 16, 21 (interruption and durable-journey report, 024; resume of share, join, insert, 017); upgrade and rollback rehearsed in real Obsidian: 0.4.1 -> main, 0.4.2 -> main, main -> 0.4.2 -> main, 0.3.4 and 0.4.0 -> main, on macOS and Ubuntu (upgrade/rollback report, 026); repeated on the beta.2 matrix and on the 0.5.0 build (run 39239809804: `upgrade-install`, `upgrade-rollback`, `smoke`, macOS 1.14.4, 3/3). The critical silent-divergence defect (033) and the SDK commit/listener faults (034, SDK 0.2.2) are closed. | PASS_WITH_FINDINGS | #53: after a crash that cuts the cleanup of a cancelled share, a rollback to 0.4.2 can list the never-hosted section as an ordinary one (no data lost). Not rehearsed: rollback with kept copies of a deleted note's text; a crash between sending a held deletion and recording it. |
| G03-E | Statuses, access, held source and offered actions match evidence | Status precedence, access and connection facts (005, 018, 019; U03-06, 11, 17, 25, 28), native UX and status acceptance, revoked-recipient UI in `two-hosts`; fixes since: lost line offered back (057), honest insert preview (061, #75), revoke notice names the section and one "Review conflicts" button (062, #82). | PASS_WITH_FINDINGS | #87 (open): the Repair dialog shows raw marker text, a second Repair button, and two status lines saying the same. The `lfcp-ref` line shown after Tasks completes a Task (P2/C-7) was not reproduced in #82; no regression spec was added. Forced-colors mode NOT_RUN. |
| G03-F | Native lifecycle, keyboard, modes, themes, Tasks and performance | Native matrix report (025, #61): Linux/macOS/Windows x 1.13.4/1.14.4, Source/Live Preview/Reading, popout, zoom, themes, keyboard with real keys, Tasks on and off. Beta.2 full set 6/6 (run 39215441248; one `rerun --failed` for F7). #86 full set on Linux 1.14.4 (39226996766, green). 0.5.0 build: full set 4/6 (run 39233558057; see below), then a rerun of the failing spec (39240515135, 4/4). Performance: beta.2 B1 p95 108.7-123.3 ms (39215444645); 0.5.0 B1 p95 108.1-146.5 ms, budget 150 (39233568673); B2 p95 39.6 ms, B4 32.7 ms; no full-vault scan per caret event and no status writes (B5, B6, 026). | PASS_WITH_FINDINGS (partial for the released build) | **The released 0.5.0 build has no fully green full matrix.** The first run failed two of six jobs (macOS 1.14.4 and Windows 1.13.4), both in `section-two-panes` ("a cut in one pane pasted in the other within one pass: a move, Gamma keeps its ID", expected CURRENT, received ATTENTION). The cause was not diagnosed: it resembles F3 (Obsidian's merge) and the double-move flake C-9 (#68). The rerun covered only that spec (11 of 11 passing on the Windows jobs; spec-level pass on macOS and Windows, both versions) on a docs-only descendant (`41e5b90`, `src/` identical): a pass of one spec, not a full rerun, and one pass does not prove a flake. B1 is inside the budget by 3.5 ms on one shared-runner sample. NOT_RUN: real IME, forced colors, mixed OS or version pair of real Obsidian apps, hand testing on Windows and Linux, comparison of performance with 0.4.0. Mobile is out of scope. A full matrix on 0.5.0 is scheduled after the release (owner decisions D32 and D33). |
| G03-G | Real usability pilot reached the frozen threshold | Not run. Owner decision D31 (2026-10-19): GO for MVP 0.3 without the pilot; the pilot is no longer a completion condition and may be held after release as a study. Materials exist (027). The wording of the pane was not checked with people. | WAIVED_BY_OWNER (D31) | Usability of the core flow (five pairs, 10 and 5 minute thresholds) is unmeasured; the release notes say so. Under the test plan a missed pilot threshold would be a Major finding; it is waived, not passed. |
| G03-H | Candidate, affected regression, upgrade/rollback, limits and handoff agree | Candidate manifests for beta.1, beta.2 and 0.5.0 with commit, pins and digests; reproducible build (local, native, performance and release runs print the same `main.js` hash); release dry run 39233669043 and the tag run 39241767276; release notes 0.5.0 with known limits and rollback to 0.4.2; ux-contract-0.3; observed rollback (above). Owner-only steps (tag, release, attestation) done and verified here. Handoff (LFCP-03-030) not yet done. | PASS_WITH_FINDINGS | The release notes quote the pane timing as p95 108.7-123.3 ms (beta.2); the 0.5.0 run measured up to 146.5 ms. The claim should match the candidate (U03-30): correct it in the 0.5.1 notes. Rollback gaps listed under G03-D. The 0.5.0 candidate manifest still says "nothing is published" and "not green on this build"; it is the pre-release state. |

Summary: A PASS; B, C, D, E, F, H as listed; G WAIVED_BY_OWNER (D31); F
partial for the released build. No FAIL, no open Blocker (private
publication, data loss, wrong-target write, unauthorised mutation, harmful
duplicate durable flow, false success with held data, crash of a required
flow) found in the evidence.

## Evidence for the 0.5.0 build

| What | Run | Result |
| --- | --- | --- |
| Native set, 51 specs, `release_build`, 3 OS x 2 Obsidian | [39233558057](https://github.com/openlfcp/obsidian/actions/runs/39233558057), `1eda57a` | 4/6; macOS 1.14.4 and Windows 1.13.4 failed `section-two-panes` |
| Rerun, `section-two-panes` only, same four native jobs (macOS and Windows) | [39240515135](https://github.com/openlfcp/obsidian/actions/runs/39240515135), `41e5b90` | 4/4 pass |
| Short native run, macOS 1.14.4: `upgrade-install`, `upgrade-rollback`, `smoke` | [39239809804](https://github.com/openlfcp/obsidian/actions/runs/39239809804) | 3/3 |
| Pane performance B1-B4, macOS 1.14.4 | [39233568673](https://github.com/openlfcp/obsidian/actions/runs/39233568673) | success; B1 p95 up to 146.5 ms (budget 150) |
| Release dry run | [39233669043](https://github.com/openlfcp/obsidian/actions/runs/39233669043) | success |
| Tag release | [39241767276](https://github.com/openlfcp/obsidian/actions/runs/39241767276) | success; checksums and attestation re-verified |
| Beta.2 full set | [39215441248](https://github.com/openlfcp/obsidian/actions/runs/39215441248) | 6/6 after one `rerun --failed` (F7) |
| Dialog layout fix (#86), full set on Linux 1.14.4 | [39226996766](https://github.com/openlfcp/obsidian/actions/runs/39226996766) | success |

Merged work: obsidian #20-#88 (the pane, journeys, resume, keyboard,
qualification, repairs 043..064, candidates beta.1, beta.2 and 0.5.0, launch
materials), no pull request is open.

## Unresolved

Open issues in openlfcp/obsidian at the time of review:

| Issue | Priority | What | Disposition |
| --- | --- | --- | --- |
| [#87](https://github.com/openlfcp/obsidian/issues/87) | P2 | Repair UI: raw marker text in choices, second Repair button, duplicate status lines | Not a blocker (readability, no data effect); candidate for 0.5.1 |
| [#68](https://github.com/openlfcp/obsidian/issues/68) | P2 | C-9: a move next to cut/paste recorded as two `node.move` (Windows 1.13.4, 1 in about 40). Risk: an extra move of another writer's node in a concurrent scenario. C-7, C-8 and N4 of the same issue were handled in #82 (C-7 not reproduced); the issue is stale and should be split | Known limit in the release notes ("a late move can be sent twice"); possible link to the 0.5.0 `section-two-panes` failure; 0.5.1 |
| [#81](https://github.com/openlfcp/obsidian/issues/81) | P3 | Timers handed to the sections port and `#passSoon` not cleared by `SectionsHost.stop()` | Low; same class as the fixed #78; 0.5.1 |
| [#53](https://github.com/openlfcp/obsidian/issues/53) | P3 | Upgrade/perf harness follow-ups; write the `resource-discarded` mark before the journal entry (rollback edge, no data loss) | Listed in the release notes; 0.5.1 |

Not tracked as issues but open as evidence gaps: the F7 click flake (G03-B),
the undiagnosed `section-two-panes` failure on 0.5.0 (G03-F), the stale
pane-timing figure in the release notes (G03-H).

Known limits stated in the 0.5.0 release notes (checked against evidence;
each is consistent with it): desktop first and not tested by hand on Windows,
Linux, with an IME, or on mobile; pane wording not checked with people; a
late move can be sent twice (#68); pane timing; the recurrence sign of a Task
stays local; "Put back" after a lost marker and an edit in one place can add a
second copy; 0.4.1 and 0.4.2 keep the double-creation race and the newcomer
race, with no 0.4.3 planned; project-server quotas; no read receipts,
invitation state, inbox, cancellation or expiry; beta software; about 200
tasks per section, no headings inside a section, one server per collaboration.
Rollback is supported to 0.4.2 only.

## Verdict

**GO_WITH_OWNER_WAIVERS.** Owner confirmation: pending.

Grounds:

- Every gate except G03-G has evidence from CI runs, merged and reviewed pull
  requests and reports; none is FAIL. Baseline repairs, the two-app flow,
  restart and unknown-outcome journeys, upgrade and rollback are covered by
  real-Obsidian runs, not only unit tests.
- The release artefacts are exactly what was qualified: the hashes of the
  published files equal the candidate manifest, the attestation verifies, and
  nothing under `src/` changed between the last native run and the tag.
- The test plan requires A-H PASS and zero blocker or major findings. That is
  not met literally, so the verdict is not a plain GO: G03-G was not run
  (waived, D31), and the full native matrix was not green on the released
  build (accepted, D32 and D33).

Owner waivers and decisions this verdict depends on (to be confirmed):

1. **G03-G, the pilot, waived** by owner decision D31 (2026-10-19): GO for
   MVP 0.3 without a pilot; a pilot may follow as a study.
2. **No full native matrix and no performance run required on 0.5.0 itself
   before the tag**, by owner decisions D32 and D33 (2026-10-19): the gate was
   the release workflow plus the short upgrade/rollback/smoke run; the full
   matrix on 0.5.0 is scheduled after the release; a finding there leads to
   0.5.1.
3. **Accepting the `section-two-panes` result on 0.5.0** (two of six jobs
   failed, a one-spec rerun passed four of four, cause not diagnosed) and the
   F7 click flake as known residual risk.

Recommended follow-ups (not conditions): run the full native matrix on 0.5.0
and diagnose or reproduce `section-two-panes` with logs kept; correct the
pane-timing figure in the release notes; split and re-triage #68; refresh the
gap register; fix #87, #81 and #53 in 0.5.1; then LFCP-03-030 (handoff).

Nothing in this document publishes or authorises a release, tag or rollout.
