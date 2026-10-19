# MVP 0.3 release handoff: Shared Tasks 0.5.0 and the next backlog

**Task:** LFCP-03-030 (M03-5, gate G03-H). **Date:** 2026-10-19.
**Tracker:** [#1](https://github.com/openlfcp/.github/issues/1).
**Go/no-go:** [go-no-go.md](go-no-go.md), verdict **GO_WITH_OWNER_WAIVERS**,
confirmed by the owner on 2026-10-19 (PR [#4](https://github.com/openlfcp/.github/pull/4)).

This is the entry point for whoever takes over after the release: what is
out, where it is, how to install or roll it back, what is still open and in
what order to do it. It records state; it does not publish or authorise
anything. MVP 0.3 is **released with waivers**, not "fully green": the usability
pilot was not run (owner decision D31, 2026-10-19) and the released build has
no fully green native matrix (owner decisions D32 and D33, 2026-10-19). Both are
in [Open items](#open-items) below.

## Status words used here

| Word | Meaning |
| --- | --- |
| **published** | Public and checkable at the given link |
| **prepared, not published** | Exists, but only the owner may publish it |
| **approved** | The owner confirmed it (decision number or date given) |

| Item | Status |
| --- | --- |
| Shared Tasks 0.5.0: tag, GitHub release with three attested assets | published (2026-10-19) |
| Website openlfcp.org (website PR #1) | published |
| Community plugins catalog | follows `manifest.json` on obsidian `main` (version 0.5.0 there); the catalog listing itself is not something this repository controls, check it in Obsidian |
| Launch posts | prepared, not published; the owner publishes them |
| Go/no-go verdict and its three waivers | approved by the owner, 2026-10-19 |
| Usability pilot (G03-G) | not run; waived by owner decision D31 |

## What was released and where

| Item | Value |
| --- | --- |
| Plugin | Shared Tasks 0.5.0, plugin ID `shared-tasks`, requires Obsidian 1.13.4 or later |
| Release | [openlfcp/obsidian release 0.5.0](https://github.com/openlfcp/obsidian/releases/tag/0.5.0) (not a pre-release; assets `main.js`, `manifest.json`, `styles.css`) |
| Tag | `0.5.0` = obsidian commit `f50e064640581c1fa202aec5beb2995285b70d2e` |
| Qualified build | `1eda57ad96bcd046052bfad6fd9b2234b4ac4659`; the tag differs from it in docs only (`src/`, `styles.css`, `pnpm-lock.yaml`, `test/` identical, checked in the go/no-go) |
| Release workflow | [run 39241767276](https://github.com/openlfcp/obsidian/actions/runs/39241767276), success; build provenance attestation (`gh attestation verify main.js --repo openlfcp/obsidian`) |
| Obsidian `main` | `4ed0d17` at the time of writing: the tag plus corrected release notes (pane timing measured on the 0.5.0 build) |

### Checksums (SHA-256)

From the [candidate manifest](https://github.com/openlfcp/obsidian/blob/main/docs/devel/reports/candidate-0.5.0.md),
the release notes and the go/no-go (re-hashed from the published files there):

| Asset | SHA-256 |
| --- | --- |
| `main.js` | `35fb226f28ddb6378ef85a425014873dbc96a63b0e6dcf348e8ed932ab9bae31` |
| `manifest.json` | `5500adc55a32565311a9ad93745946540501045bf2c1eb6715ab84eed9139667` |
| `styles.css` | `373028272ef8c3ed42c2c6b3b3c45ffaec3d030ee3ddd6b6163366d5f91a67c1` |

### Pins

Read from obsidian `package.json`, `server.lock` and `spec.lock` on `main`:

| Pin | Value |
| --- | --- |
| TypeScript SDK | `@openlfcp/*` 0.2.2 (client, core, crypto, shared-objects, storage, storage-idb, wire) |
| Reference server | 0.3.2, `server.lock` commit `138030ae6582197193cd4c041726683bcc206bef` |
| Spec | `mvp-0.2-baseline.12`, `spec.lock` commit `bf1c78c596eef85e272c04a8a35661f814c23a40` |
| Lockfile | `pnpm-lock.yaml` sha256 `261fc5fbbdce3add9eed79bfbe5db5525e1b65afc3ef7a03fa67357ef0f02996` (unchanged from beta.2) |
| Hosts tested | Obsidian 1.13.4 and 1.14.4; Tasks plugin 8.4.0 |
| Baseline | plugin 0.4.0, `@openlfcp/*` 0.2.0, spec `mvp-0.2-baseline.12`, server 0.3.2 |

The Markdown format of notes and the sync protocol are unchanged: no new wire,
profile or marker format.

## Install, upgrade, rollback

- **Install.** Obsidian 1.13.4 or later: Settings, Community plugins, Browse,
  "Shared Tasks". Catalog users on 0.4.2 update from the Updates tab. Identity,
  keys, shared sections, queued edits and unfinished operations are kept; no
  tour opens. From 0.3.x straight to 0.5.0 the sync data is upgraded once and
  0.3.x cannot open it afterwards.
- **Pre-releases (BRAT).** Betas (`0.5.0-beta.1`, `0.5.0-beta.2`) were BRAT-only.
  For BRAT, add `openlfcp/obsidian` and choose the version.
- **By hand.** Put the three assets in `<vault>/.obsidian/plugins/shared-tasks/`
  and compare them with the checksums above.
- **Rollback.** To **0.4.2** only: install 0.4.2 over 0.5.0 (BRAT: choose
  version 0.4.2, or put its three files in the plugin folder). It starts on the
  data 0.5.0 wrote; the pane is not in 0.4.2. Not 0.4.1 (lacks the Task-edit
  fix), not 0.3.x (unsupported). Rehearsed on macOS and Ubuntu in real Obsidian;
  gaps listed under issue #53 below.

## Documents

| What | Link |
| --- | --- |
| Release notes 0.5.0 (what is new, fixed, install, rollback, known limits) | [docs/releases/0.5.0.md](https://github.com/openlfcp/obsidian/blob/main/docs/releases/0.5.0.md) |
| CHANGELOG | [CHANGELOG.md](https://github.com/openlfcp/obsidian/blob/main/CHANGELOG.md) |
| README (Quick start, Install, Limitations) | [README.md](https://github.com/openlfcp/obsidian/blob/main/README.md) |
| User guides | [user-guide](https://github.com/openlfcp/obsidian/blob/main/docs/guides/user-guide.md), [shared-sections](https://github.com/openlfcp/obsidian/blob/main/docs/guides/shared-sections.md), [choosing-a-server](https://github.com/openlfcp/obsidian/blob/main/docs/guides/choosing-a-server.md) |
| Candidate manifest and evidence | [candidate-0.5.0.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/reports/candidate-0.5.0.md) (still says "nothing is published": the pre-release state) |
| Native matrix, upgrade/rollback and performance reports | [mvp-0.3-native-matrix.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/reports/mvp-0.3-native-matrix.md), [upgrade-rollback-perf-0.5.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/reports/upgrade-rollback-perf-0.5.md) |
| Website | [openlfcp.org](https://openlfcp.org) (PR [openlfcp/website#1](https://github.com/openlfcp/website/pull/1)) |
| Go/no-go | [go-no-go.md](go-no-go.md) |
| Baseline, authority, gaps | [baseline-manifest.md](baseline-manifest.md), [authority-map.md](authority-map.md), [gap-register.md](gap-register.md) (2026-10-15 snapshot, stale, see item 8) |

## Known limits of the release

Stated in the release notes and consistent with the evidence: desktop first,
not tested by hand on Windows, Linux, with an IME or on mobile; pane wording
not checked with people; a late move can be sent twice (#68); pane timing p95
108.1-146.5 ms against a 150 ms goal on one shared runner; the recurrence sign
of a Task stays local by design; "Put back" after a lost marker and an edit can
add a second copy; 0.4.1 and 0.4.2 keep the double-creation race (no 0.4.3);
project-server quotas; no read receipts, invitation state, inbox, cancellation
or expiry; beta software. Rollback only to 0.4.2.

## Open items

Open issues in openlfcp/obsidian: #87, #81, #68, #53 (no pull request is open).
Two evidence gaps are not issues: the F7 click flake and the undiagnosed
`section-two-panes` failure on 0.5.0 (run
[39233558057](https://github.com/openlfcp/obsidian/actions/runs/39233558057), 4 of
6 jobs; a one-spec rerun, run
[39240515135](https://github.com/openlfcp/obsidian/actions/runs/39240515135), passed
4 of 4, which does not prove a flake). Neither is a release blocker: the
go/no-go found no FAIL and no open Blocker.

## Next backlog (0.5.1 and after)

Priorities: **P1** = do first, it decides whether 0.5.1 is needed; **P2** = fix
in 0.5.1; **P3** = low risk, batch with 0.5.1 or later. "Recommendation" is the
handoff's proposal, not a decision. No new issues are opened by this document;
the table says where one would help.

| # | P | Item | Source | Recommendation |
| --- | --- | --- | --- | --- |
| 1 | P1 | Full native matrix (51 specs, 3 OS x 2 Obsidian, `release_build`) and performance B1-B4 on **0.5.0** itself | go/no-go G03-F; D32, D33 | Run now on tag `0.5.0` / `main` (`src/` identical). A finding leads to 0.5.1. Keep all job logs and artifacts this time |
| 2 | P1 | Diagnose `section-two-panes` ("a cut in one pane pasted in the other within one pass: a move, Gamma keeps its ID", expected CURRENT, received ATTENTION; macOS 1.14.4 and Windows 1.13.4 in run 39233558057) | go/no-go G03-F | Repeat the spec on those two jobs many times with logs saved (trace of the two panes' events and of Obsidian's "modified externally" merge). Decide: harness race, F3 (Obsidian merge, Windows) or C-9. Time-box it |
| 3 | P2 | #68, **C-9**: a move next to cut/paste recorded as two `node.move` (Windows 1.13.4, about 1 in 40) | #68; known limit in notes | Likely cause of item 2. Fix in 0.5.1 if confirmed. Extra move of another writer's node in a concurrent scenario is the risk |
| 4 | P2 | #87: Repair UI shows raw marker text in choices, a second Repair button, duplicate status lines | #87 | 0.5.1. Same class as N4 (#82): `problemViews` drops the duplicate only for `review-conflicts` |
| 5 | P2 | F7 click flake: `pane-access-copy-detach` failed once at first attempt (beta.2, Linux 1.13.4, a dialog did not open); log not kept | go/no-go G03-B | Fold into item 1: if it recurs, keep the log and classify product defect or click race. Do not chase it separately |
| 6 | P2 | Rehost and blocked notices (candidate from #82) | go/no-go; #82 | Check what #82 left as a candidate against the pane wording; one small PR in 0.5.1 if it reads wrong. No issue needed unless it grows |
| 7 | P2 | Owner question, **needs a decision**: should the recurrence sign of a Task (🔁) sync? | release notes limit "Repeat signs do not sync" | Today local by design (M7 / ST-5). Syncing it is a protocol change, so it is the owner's call and, if yes, goes through the spec change process, not a plugin patch. Recommendation: leave as is for 0.5.x, record the decision either way |
| 8 | P2 | Refresh the gap register (F-03..F-05 still show PARTIAL/OPEN) | go/no-go G03-A | Docs-only PR in this repository after item 1, so it can cite 0.5.0 facts |
| 9 | P3 | #53: upgrade/perf harness follow-ups and discard-marker order (write the `resource-discarded` mark before the journal entry) | #53; notes | 0.5.1 or later. Not rehearsed: rollback with kept copies of a deleted note's text; a crash between sending a held deletion and recording it |
| 10 | P3 | #81: timers handed to the sections port and `#passSoon` not cleared by `SectionsHost.stop()` | #81 | 0.5.1. Same class as the fixed #78 |
| 11 | P3 | Forced-colors mode, real IME, mixed OS or version pair of real apps, hand testing on Windows and Linux, comparison of performance with 0.4.0 | go/no-go G03-F (NOT_RUN) | Schedule after item 1; each is a separate study or a small harness task |
| 12 | P3 | Usability pilot as a study (materials exist; waived by D31) | go/no-go G03-G | Run when the owner wants people's evidence on wording; five pairs, frozen thresholds (10 and 5 minutes). Not a gate any more |
| 13 | P3 | Deferred scope from MVP 0.3: clickable Obsidian invite wrapper, shared status-bar counter (follow-ups, not blockers); and the exclusions: cancelling an invitation, read receipts, global invite inbox, presence, mobile certification, attachment transport, per-node ACL | MVP 0.3 scope | Product tracks, not 0.5.x fixes. The next MVP is not numbered by the 0.3 package: choose it after the product observations |

### Proposed split of #68

#68 mixes four findings of the native matrix. C-7, C-8 and N4 were handled in
#82 (C-7, the `lfcp-ref` line after Tasks completes a Task, was **not
reproduced** and has no regression spec). Left open: C-9 and the remaining
notes. Proposal, for the owner to apply (the issue was not edited here):

1. Retitle #68 to **C-9 only**: the double `node.move` (Windows 1.13.4, 1 in
   about 40), with `section-two-panes` as a suspected link; P2, 0.5.1.
2. Close C-7 / C-8 / N4 as done in #82, with a note that C-7 was not
   reproduced (reopen with a reproducer if it appears again).
3. Move any remaining non-C-9 notes either into #87 (Repair UI) or into the
   rehost/blocked notice item (6), rather than a new issue.

## Not done here

No tag, release, post or deploy was made by this task. Launch posts stay
prepared, not published. The tracker [#1](https://github.com/openlfcp/.github/issues/1)
is not closed by this document; closing it is the orchestrator's decision.
