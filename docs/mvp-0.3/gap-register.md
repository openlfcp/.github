# MVP 0.3 gap register: beta.8 → 0.4.0

**Task:** LFCP-03-001 (M03-0, gate G03-A). **Date:** 2026-10-15.
**Range:** obsidian `5c7f44bc72bda06d8bb725ee1ce5ec8eecdbe936` (0.4.0-beta.8,
researched) → `ce0660a519cdce089630e63e1d390009c6148284` (0.4.0, released),
168 commits. sdk-ts `d213de8` (0.2.0-beta.6) → `2a34beb` (0.2.0). spec
`mvp-0.2-baseline.10` → `.12`. Pins: [baseline-manifest.md](baseline-manifest.md).
Providers: [authority-map.md](authority-map.md).

**Labels:** `FIXED`: the researched defect no longer occurs; the commit,
release and test are named. `PARTIAL`: the observed symptom is fixed, but
part of the MVP 0.3 acceptance is still open. `OPEN`: unchanged since
beta.8. `VERIFIED_IN_CODE`: read at `ce0660a`. `REPRODUCED`: run by this
task. "First release" is the first tag that contains the fix.

## Baseline defects F-03, F-04, F-05

| Finding | Status | Owner |
| --- | --- | --- |
| F-03 second Share → extra Resource and "stopped syncing" | **PARTIAL**: the C09 symptom is FIXED (0.4.0-beta.10, 0.4.0-beta.15); MVP 0.3 acceptance is open | LFCP-03-002 |
| F-04 held source shown as "No local changes waiting" / "Current" | **PARTIAL**: card, badge and editor are FIXED (0.4.0-beta.10, beta.11); persistence and pane facts are open | LFCP-03-003 (then 005, 018) |
| F-05 `resolve-shared-conflict` inside a section says "update the plugin" | **OPEN**: the code path is identical at 0.4.0 | LFCP-03-004 |

### F-03: second Share

**Fixed by:**

- `7070d5fc59459ffe95e931a377eed0c8cfd59b38` "one share flow per note; a
  stale creation leaves no Resource" (first release 0.4.0-beta.10):
  - `src/core/in-flight.ts` adds `InFlight`. `SectionsHost#oneFlow`
    (`src/obsidian/sections-host.ts`) runs share (preview and creation
    together), import and insert one per note, with the key
    `note:<path>`. A second start meanwhile shows "this note already has
    a section being shared or inserted. Finish that first." and opens
    nothing.
  - `CollabCommands#joining` gives join the same guard (F-C04).
  - `SectionCreation` (`src/core/sections/create.ts`) checks the note
    before it makes anything, so a stale preview creates no Resource. A
    creation found stale or cancelled after its Resource exists calls
    `LfcpRuntime.discardUnhosted`. That Resource is then not listed, not
    opened, and its events stay quiet.
  - A new Resource counts as hosting-pending before its first
    `RESOURCE_OPEN`, so an early `RESOURCE_NOT_HOSTED` is not announced.
- `181930d6dd689d71415c3419b13513dca36936b1` (first release
  0.4.0-beta.15): a discarded Resource that was **never sent** is deleted
  through the SDK's `deleteUnsentResource` (sdk-ts `9871a48`, 0.2.0-beta.7).
  `#forgetDiscarded` finishes the deletion at the next start.
- Tests:
  - `test/core/in-flight.test.ts`;
  - `test/core/sections/create.test.ts`;
  - `test/core/lfcp/discard.test.ts`;
  - `test/core/sections/live-discard.test.ts` (live server);
  - native `test/native/specs/section-share-held.e2e.mjs`
    (`481111637a38f6f8d5e1b0721d87b3d3297e4fbc`): two Share commands on
    one note make and host one Resource, with no "stopped syncing" notice.

**Open for LFCP-03-002:**

1. A repeated start is refused with a notice. It does not reveal the open
   flow, but 0.3 AC1 says "повтор раскрывает текущий flow".
2. The guard key is the note path. Renaming the note during the flow gives
   a new key. The pane and context-menu entry paths do not exist yet, so the
   "different entry paths" case cannot be tested until LFCP-03-010/012.
   Those entries must reach the same `SectionsHost` `InFlight`.
3. A stale Resource that was already **sent** (attempted, acknowledged or
   received) is kept for good, only marked discarded. The SDK refuses with
   `RESOURCE_SENT`. A recoverable-draft or cleanup contract for it is not
   decided.
4. A crash after the Resource exists but before the discarded mark is
   stored has no named test.

### F-04: held source

**Fixed by:**

- `d94831fd3b33794e35afde4f5487d18ce6c9b105` "held edits are counted,
  named and marked, never shown as synced" (first release
  0.4.0-beta.10):
  - New `src/core/status/held.ts`: `HeldEdits` with cause
    (`unsupported` | `binding` | `boundary` | `read-only` | `revoked` |
    `refused` | `rejected` | `base-unknown`), `count` (null when it
    cannot be counted), `line` and `nodeIds`.
  - `card.ts` prints "N edits not sent: <cause> (<note>, line L)". It never
    says "No local changes waiting." or "Current as last checked" while
    edits are held. It offers "Go to line" and "Repair shared sections in
    this note".
  - A held projection is never CURRENT (`reducer.ts`).
  - Held rows are marked in the editor. A read-only section blocks typing.
  - `StatusFacts.access` keeps `not-member` apart from `revoked` and
    carries `verifiedAt`/`current` (part of F-C05).
- `9f368a92b434427bd6f970df75ddd2d09fc21d82` (first release
  0.4.0-beta.11): moved Tasks count as held and are named.
- Related, against false CURRENT:
  - `1aa1bbd` (first release beta.15): a note whose tree is not the model's
    is "diverged", never CURRENT.
  - `0befb80` (first release beta.17): a remote change deferred for an edit
    that nothing sends is a divergence.
- Pending batches and held edits are separate lines on the card. Held
  edits are not added to "local updates waiting".
- Tests:
  - `test/core/status/held.test.ts`;
  - `test/obsidian/section-status.test.ts`;
  - `test/core/sections/diverged.test.ts`;
  - `test/core/sections/stale-content-diverged.test.ts`;
  - native `section-share-held.e2e.mjs`, which covers the heading inside the
    section, a damaged binding line and a read-only copy.

**Open for LFCP-03-003:**

1. Held state lives **in memory** (`ProjectionStatus#held`,
   `src/core/status/projections.ts`). It is recomputed by the next pass of
   that note. There is no evidence for a held copy after a restart, or in
   a closed note, before its next pass.
2. There are no facts shaped for the pane, and no vault-wide aggregate
   that keeps queue batches, held projections and unknown counts apart.
   The card does this per section only.
3. Held edits returning to the peer after a repair is NOT_RUN on a real
   host. The research says the same.

### F-05: legacy resolver inside a section

The code path is **identical** at `5c7f44b` and `ce0660a`
(VERIFIED_IN_CODE; the function bodies hash the same):

1. `plugin.ts` wires `"resolve-shared-conflict"` to
   `CollabCommands.resolveConflictUnderCursor`
   (`src/core/collab/commands.ts`). That function has no `#refuseInSection`
   or `sectionContext` check, unlike the other 0.1 commands.
2. `taskAt` finds the `lfcp-ref` of a Task line inside a section.
3. `Collaboration.conflicts` calls `runtime.profileOf(R)`, and
   `LfcpRuntime.#local` throws `UnsupportedProfileError`
   (`NEEDS_NEWER_VERSION`) for the section profile.
4. `#run` shows: "Shared Tasks: Resolving the conflict failed. This
   collaboration needs a newer version of Shared Tasks. Update the plugin
   in Settings → Community plugins".

None of the 168 commits touches this path. `0c87bc3` (beta.19) is about
inserting a section that has a conflict, which is a different message. The
existing tests (`test/core/collab/commands.test.ts`,
`test/e2e/two-vaults.test.ts`, `test/e2e/security-vertical-slice.test.ts`)
cover 0.1 Tasks outside sections only. The section resolver to send the
user to is `src/core/sections/recovery.ts` plus
`src/obsidian/ui/recovery.ts` ("Review conflicts…" on the card).

## Content policy against the current spec

| Question | Spec at baseline.12 | Code at 0.4.0 | Status |
| --- | --- | --- | --- |
| Tables, fences, callouts, blockquotes, HTML blocks | Raw nodes, shared verbatim (MARKDOWN-SECTIONS-01 §4.4, §5). An unclosed fence or a heading inside the region fails closed. A heading blocks the first share (§8) | Implemented. The spec MS fixtures run in obsidian `pnpm test` via `LFCP_SPEC_DIR` (`test/support/sections-fixtures.ts`), green in CI 38636817368. The research saw a table sent as raw once the heading was removed (C07) | Conforming. The old "tables are unsupported" draft rule must **not** come back |
| Comments (`%%…%%`, non-LFCP `<!--…-->`) | The sender's `section comments` setting, `local` by default; a new comment under `local` stays on the device; under `shared` it becomes a raw node; a marked comment stays shared (§4.5, MS38–MS41) | `src/core/settings.ts` (`sectionComments: "local"`), `src/core/sections/engine.ts`. The share preview warns "Comments (%% … %% and <!-- … -->) in this section stay on this device." (`share.ts`, `local-comments`) | Conforming. LFCP-03-020 must keep the preview's comment sentence exact. A paragraph under a Task is content, not a comment |

## Whole-projection deletion versus body deletion

The spec separates the two (MARKDOWN-SECTIONS-01 §10;
SHARED-SECTIONS-PROFILE-01 §4 and §9):

- deleting visible content in a healthy section is a **shared** delete: a
  lifecycle tombstone, retained and restorable;
- removing a whole local projection, or deleting the host file, removes
  **local projections only**;
- the profile defines no section deletion and no Resource tombstone.

**Targeted reproducer** (this task, scratch only, not committed). It used
obsidian at `ce0660a` with the in-repo two-vault engine harness
`test/support/section-vaults.ts`, ran
`pnpm exec vitest run <one file>`, and passed 2/2 (exit 0):

1. A deletes the heading, both markers and the body of a shared section.
   The editor's deleted-Task IDs are passed too, as a worst case.
   - A's model keeps every node `active`.
   - After a reconnect, B's note is byte-identical.
   - Result: **no shared mutation, REPRODUCED.**
2. A deletes only the body and keeps the heading and both markers.
   - The Tasks become `deleted` in the model.
   - B's note loses them.
   - Result: **shared delete, REPRODUCED.**

What this shows:

- The research's "deleting a copy's text deletes the content for
  everyone" is spec-conforming **for body deletion**.
- Deleting the whole projection does not touch the shared section.
- Two gaps remain:
  - After case 1, A's stored projection base stays (`projectionsOf`
    still lists it). Only detach calls `bases.save(id, null)` and
    `ProjectionStatus.forget`. Whether a stale projection is still counted
    on a card or in a future list is not verified at host level.
  - Nothing warns the user before a body deletion goes to everyone
    (UX, LFCP-03-019/020).

## Other researched findings at 0.4.0

| Finding | Status at 0.4.0 | Evidence | Owner |
| --- | --- | --- | --- |
| F-01 no ribbon, pane, context menu or `lfcp://` handler | OPEN | No `registerView`, `ItemView`, `addRibbonIcon`, `registerObsidianProtocolHandler` or editor-menu in `src/` | 011–013, 021 |
| F-02 no next step after share or join; joined-but-unplaced invisible | OPEN | Unchanged flow | 014, 015, 011 |
| F-06 flow bound to the mutable editor (wrong reasons after switch or rename) | OPEN | `sections-host.ts` still revalidates `editor.getValue()` and says "the section's heading is gone" | 009, 016, 017 |
| F-07 selection ignored by Share | OPEN | Share still uses `editor.getCursor().line` only | 009, 014 |
| F-08 ✓✓ looks like delivery | OPEN | Design; no delivery contract | 006, 020 |
| F-09 metadata in the insert preview | OPEN | Unchanged | 020 |
| F-10 names drift between surfaces | OPEN | Unchanged | 011, 020 |
| F-C04 single-flight for actions | PARTIAL | Invite (beta.6), share/import/insert per note and join (`7070d5f`). No shared dispatcher | 010 |
| F-C05 access facts lost on the badge | PARTIAL | `not-member` apart from `revoked`; `verifiedAt`/`current` carried (`d94831f`); UI use unverified | 005 |
| F-C06 `connecting`/`failed` never emitted | OPEN | `facts.ts` still derives connection from the session phase. Faster reconnect landed (`bdcc7d6`, beta.19), but it is operational only | 005 |
| F-C09 control re-propose | FIXED (beta.6, before the research) | sdk-ts `repropose.ts` | Reuse |
| Removed member rejoin | OPEN (owner decision) | `f23c4e0` (beta.15): a removed member is told so and its card is not current. Design: [rejoin-after-removal.md](../devel/design/rejoin-after-removal.md) | Owner decision for 0.3 |

Other changes in the range that 0.3 must keep:

- the IME and seed races (`49aaf0d`, `0b8ead7`);
- the line-move, cut and paste identity fixes (about 40 `fix(sections)`
  commits);
- the writer lock before the database (`2fa1249`, `4187949`);
- Reading-view notes (`547921c`);
- `@openlfcp/*` 0.2.0 (`ce0660a`).

These are regressions to guard, not 0.3 work.

## Proposed new tasks

These are candidates for the orchestrator. None is started.

| ID (proposed) | Title | Why | Suggested owner / place |
| --- | --- | --- | --- |
| N-01 | Clean up a projection's base and status when the whole projection leaves the note | Reproducer case 1: the base stays after a whole-section deletion. Only detach forgets it. Risk: a stale "copy" counted by the 0.3 list (011) or the card | obsidian; fold into LFCP-03-011 or 003 |
| N-02 | Contract for a stale **sent** section Resource after a cancelled share | `deleteUnsentResource` refuses with `RESOURCE_SENT`. The Resource stays marked discarded with no user-visible recovery | Decision in LFCP-03-002 (AC3); spec issue only if a shared mutation is needed |
| N-03 | Run the native harness workflow in GitHub CI | `native.yml` exists with 3 OS × 2 Obsidian versions but was never run. Native evidence is local Linux only | obsidian CI; input to LFCP-03-025 |
| N-04 | Publish the MVP 0.3 package (scope, backlog, gates) in `.github/docs` | The package is the 0.3 authority but lives only in the owner's workbook. Reviewers of PRs cannot read it | `.github`; with LFCP-03-006 |
| N-05 | Warn before a body deletion that goes to everyone | The research saw no warning. The spec semantics are correct, so this is UX only | LFCP-03-019/020 acceptance note, not a new protocol task |

## Delta for dependent tasks

- **LFCP-03-002**: start from `7070d5f` and `181930d`. Do not re-add a
  per-note lock. The work is to reveal the open flow, key by a stable
  note identity across renames, and handle sent stale Resources (N-02).
- **LFCP-03-003**: `held.ts` and `ProjectionStatus` are the shared status
  path to extend. Do not build a second one. What is missing is
  persistence and restart evidence, plus pane-shaped aggregate facts.
- **LFCP-03-004**: the defect is unchanged. Apply `sectionContext` to
  `resolveConflictUnderCursor` and route "inside" to the section's
  "Review conflicts…". Keep the 0.1 path and the real unsupported-profile
  diagnosis. Damaged or crossing context must not reach a guessed
  resolver.
- **LFCP-03-005**: the access part of F-C05 is in `d94831f`. Connection
  `connecting`/`failed` is still open.
