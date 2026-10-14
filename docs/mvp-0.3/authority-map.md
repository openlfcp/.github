# MVP 0.3 authority map

**Task:** LFCP-03-001 (M03-0, gate G03-A). **Date:** 2026-10-15.
**Baseline:** the commits in [baseline-manifest.md](baseline-manifest.md)
(obsidian `ce0660a`, sdk-ts `2a34beb`, spec `mvp-0.2-baseline.12`).

This map says which document decides each question in MVP 0.3. It also
says which code is the single provider of journals, status, the registry
and actions. MVP 0.3 work reuses these providers. It adds no second journal,
no second registry and no second status path.

## Documents: which one decides what

Order of precedence: when two documents disagree, the one listed first for
that area wins. An MVP 0.3 package document never overrides a normative
spec document. A real contract gap goes to the spec through its owning
task, as an issue first.

| Area | Authority | Where |
| --- | --- | --- |
| Wire protocol, Control Records, invitations, claims, access | LFCP-WIRE-01 at `mvp-0.2-baseline.12` | spec `wire/LFCP-WIRE-01.md` |
| Shared Sections data model: nodes, placements, lifecycle, deletion, conflicts | SHARED-SECTIONS-PROFILE-01 | spec `profiles/SHARED-SECTIONS-PROFILE-01.md` |
| Legacy 0.1 Task profile (`resolve-shared-conflict`, task refs) | SHARED-OBJECTS-PROFILE-01; MARKDOWN-REFS-01 | spec `profiles/SHARED-OBJECTS-PROFILE-01.md`, `integration/MARKDOWN-REFS-01.md` |
| Markdown binding of sections: boundaries, raw blocks (§4.4), comments (§4.5), supported syntax (§5), first share (§8), copy/cut/detach/delete (§10) | MARKDOWN-SECTIONS-01 | spec `integration/MARKDOWN-SECTIONS-01.md` |
| SDK ↔ adapter contract for sections: receipts, operation IDs, status snapshot | SDK-SECTIONS-INTEGRATION-01 | spec `integration/SDK-SECTIONS-INTEGRATION-01.md` |
| Decisions behind the profile and canonical changes | ADR 0009, ADR 0010 | spec `adr/` |
| Conformance fixtures (MS, SS, CM cases) | The spec corpus at the tag | spec `test-vectors/` |
| Working rules for agents and contributors | Agent operating guide; engineering conventions | [AGENT-OPERATING-GUIDE.md](../AGENT-OPERATING-GUIDE.md), [engineering-conventions.md](../engineering-conventions.md) |
| What 0.2 promised and excluded | MVP 0.2 scope, test and release plan | [MVP-0.2-SCOPE.md](../MVP-0.2-SCOPE.md), [MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) |
| What was released, under which waivers | Go/no-go record; release close-out | [mvp-0.2-go-no-go.md](../release/mvp-0.2-go-no-go.md), [mvp-0.2-release-close.md](../release/mvp-0.2-release-close.md) |
| Plugin behaviour and limits as shipped | Shared Tasks 0.4.0 release notes and compatibility notes | obsidian `docs/releases/0.4.0.md`, `docs/releases/0.4-compatibility.md` |
| MVP 0.3 scope, UX, architecture, gates G03-A–H, backlog LFCP-03-001–030 | The MVP 0.3 package, revision 0.2 (2026-10-12) | The owner's workbook. It is proposed, not normative, and is not yet published in this repository |
| Current pins and the delta from the researched beta.8 | This task | [baseline-manifest.md](baseline-manifest.md), [gap-register.md](gap-register.md) |

### Questions the package left open, with their answers from the spec

| Question | Answer | Authority |
| --- | --- | --- |
| Are tables and fences unsupported (old draft)? | **No.** Fences, tables, callouts, blockquotes and HTML blocks are shared verbatim as raw nodes. Only an unclosed fence and a heading inside the region fail closed (`SECTION_UNSUPPORTED_SYNTAX`). A heading blocks the first share | MARKDOWN-SECTIONS-01 §4.4, §5, §8; fixtures MS16, MS33, MS34 |
| Are comments in a section shared? | By the **sender's** `section comments` setting, `local` by default. Under `local`, a new `%%…%%` or non-LFCP `<!--…-->` comment is not extracted and stays on the device. Under `shared` it becomes a raw node. A comment that already has a `raw` marker stays shared under either value. A plain paragraph under a Task is not a comment | MARKDOWN-SECTIONS-01 §4.5; fixtures MS38–MS41 |
| Is deleting text the same as deleting the copy? | **No.** Deleting visible node content in a healthy section is a shared delete (a lifecycle tombstone, retained and restorable). Removing a whole projection, or deleting the host file, removes **local projections only**. Detach strips the bindings with no shared mutation. The profile defines **no section deletion or Resource tombstoning** | MARKDOWN-SECTIONS-01 §10; SHARED-SECTIONS-PROFILE-01 §4 ("does not define section deletion or Resource tombstoning"), §9 |
| Does ✓✓ or CURRENT mean a peer received it? | No. Acceptance is a durable server ACK only. There is no peer delivery contract, and delivery is out of 0.3 scope | SDK-SECTIONS-INTEGRATION-01; MVP 0.3 scope "Не входит" |

## Code providers

The paths are inside each repository, at the baseline commits. Symbols are
named because line numbers drift.

### Operation journals and receipts

| Concern | Provider | Path |
| --- | --- | --- |
| Section operation journal: `JournalEntry`, `PHASES` captured → ids-allocated → committed → projected → done/abandoned, `advance`, `recovery`, `abandonOnce` | obsidian | `src/core/sections/journal.ts` |
| Commit and resume of a pass ("the receipt decides") | obsidian | `src/core/sections/commit.ts` (`commitPass`, `resumeOperation`) |
| Persistent stores: journal, bases, candidates, the per-note projection index | obsidian | `src/core/sections/stores.ts` (`KeyValueSectionJournalStore`, `KeyValueSectionBaseStore.projectionsOf`); interfaces in `src/core/sections/base.ts` |
| Section creation (share) journal and effects: prepare → local → projected → hosted; a stale creation is cancelled before or after its Resource exists | obsidian | `src/core/sections/create.ts` (`SectionCreation`) |
| Section insertion journal and the duplicate-insert guard | obsidian | `src/core/sections/insert.ts` (`SectionInsertion`) |
| SDK receipts and idempotent commit per (Resource, operationId); `OPERATION_ID_REUSED` | sdk-ts | `packages/client/src/receipts.ts` (`receiptOf`), `packages/client/src/storage.ts` (`commitOperation`) |
| Invitation claim journal (one-time link never spent twice) | sdk-ts | `packages/client/src/claim-journal.ts`; `packages/client/src/invite.ts` |
| Control re-proposal after a head race | sdk-ts | `packages/client/src/repropose.ts` (`reproposeControlRecords`) |
| Deleting a Resource that was never sent | sdk-ts → obsidian | `packages/storage/src/delete-resource.ts` (`deleteUnsentResource`) → obsidian `src/core/lfcp/runtime.ts` (`discardUnhosted`) |

### Status, held edits and access

| Concern | Provider | Path |
| --- | --- | --- |
| SDK facts: acceptance (durable ACK), pending, catch-up, epoch | sdk-ts | `packages/client/src/sync-client.ts` (`statusSnapshot`), `packages/client/src/batch-status.ts`, `packages/client/src/section-status.ts` |
| SDK access: `canWrite` → `WriteAccess`, `accessState` (`current`, `verifiedAt`) | sdk-ts | `packages/client/src/write-access.ts`, `packages/client/src/sync-client.ts` |
| Adapter facts from the SDK and the projection | obsidian | `src/core/status/facts.ts` (`observedFacts`, `accessFact`), `src/core/status/sdk-status.ts`, `src/core/status/collect.ts` |
| **Held edits per projection** (cause, count or unknown, line, nodes, moved Tasks) | obsidian | `src/core/status/held.ts` (`heldEdits`, `HeldEdits`, `HELD_CAUSE`) |
| Per-projection facts (held, diverged, forget on detach); in memory | obsidian | `src/core/status/projections.ts` (`ProjectionStatus`) |
| One status view from the facts (CURRENT, ATTENTION, offline, server-refused) | obsidian | `src/core/status/reducer.ts` (`statusView`) |
| Rendering: badge, card, access rows | obsidian | `src/core/status/badge.ts`, `src/core/status/card.ts` (`sectionCard`), `src/core/status/access.ts` (`accessView`) |
| Section under the cursor; range classification (outside/inside/crossing/damaged) | obsidian | `src/obsidian/section-status.ts` (`sectionAtLine`), `src/core/sections/context.ts` (`sectionContext`) |
| Connection liveness (operational only) | obsidian | `src/core/lfcp/liveness.ts` (`LivenessProbe`), wired in `src/core/lfcp/runtime.ts` |

### Registry: which sections exist on this device

There is no separate global table, and 0.3 must not add one.

| Concern | Provider | Path |
| --- | --- | --- |
| Every Resource on this device, discarded ones excluded | obsidian over the SDK storage | `src/core/lfcp/runtime.ts` (`LfcpRuntime.registry()`), filtered by `SECTIONS_PROFILE_ID` for sections |
| Resource → notes that hold it | obsidian | `src/obsidian/sections-host.ts` (`SectionsHost.#notes`, built by `#index`) |
| Note → its projections (bases) | obsidian | `src/core/sections/stores.ts` (`projectionsOf`) |
| Watched Resource → status view | obsidian | `src/obsidian/sections-host.ts` (`#statuses`) |
| Model snapshot of a section | obsidian | `src/core/lfcp/section-port.ts` (`SdkSectionPort.snapshot`, `exclusive`) |

### Actions and commands

| Concern | Provider | Path |
| --- | --- | --- |
| Command list (ids and names) | obsidian | `src/core/commands.ts` (`COMMANDS`) |
| Command wiring; the only entry surfaces in 0.4.0 are the palette and the section badge → card | obsidian | `src/obsidian/plugin.ts` (`onload`, the `handlers` map) |
| 0.1 task actions and invite/join/status/resolve, behind the `Prompter` seam | obsidian | `src/core/collab/commands.ts` (`CollabCommands`; `#refuseInSection`; `resolveConflictUnderCursor`) over `src/core/collab/service.ts` (`Collaboration`) |
| Single-flight guards | obsidian | `src/core/in-flight.ts` (`InFlight`, used by `SectionsHost#oneFlow` with key `note:<path>` for share/import/insert); `CollabCommands#oneInvitation`/`#inviting`; `CollabCommands#joining` |
| Section share/insert/detach/card/repair orchestration (still bound to Obsidian `Editor`/`Modal`/`Notice`) | obsidian | `src/obsidian/sections-host.ts` (`share`, `shareSection`, `createSection`, `insertSection`, `detachSectionAt`, `openCard`, `repairNote`) |
| Pure section cores | obsidian | `src/core/sections/share.ts` (preview, including the `local-comments` warning), `create.ts`, `insert.ts`, `rules.ts` (`detachAt`), `clipboard.ts` |
| Conflict and repair resolvers | obsidian | `src/core/sections/recovery.ts` (`recoveryItems`, stable `RecoveryItem.key`, `applyRecovery`), `src/core/sections/repair.ts`; UI `src/obsidian/ui/recovery.ts`, `src/obsidian/ui/repair.ts` |
| Prompter (dialog) implementation | obsidian | `src/obsidian/ui/prompter.ts` (`ObsidianPrompter`) |
| Settings: `sectionComments` (`local` default), default server, kill switch | obsidian | `src/core/settings.ts`; UI `src/obsidian/settings-tab.ts` |

The code map from the research cites `obsidian/prompter.ts`. At 0.4.0 that
file is `src/obsidian/ui/prompter.ts`. Every other path in the table exists at
`ce0660a`.
