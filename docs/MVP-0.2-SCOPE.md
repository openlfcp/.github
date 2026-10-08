# MVP-0.2-SCOPE

**Project:** OpenLFCP  
**Product:** Shared Tasks, by OpenLFCP  
**Milestone:** Shared sections for everyday collaboration  
**Date:** 2026-10-07; reviewed 2026-10-08  
**Status:** Reviewed. The owner-approved review of 2026-10-08 fixes the open defaults; see section 14 and `BACKLOG-MVP-0.2.md` §3  
**Companions:** `MVP-0.2-ROADMAP.md`, `MVP-0.2-TEST-AND-RELEASE-PLAN.md`, `BACKLOG-MVP-0.2.md`; `SHARED-SECTIONS-ARCHITECTURE-01.md` is to be published with LFCP-02-007/083

## 1. Outcome

Two people share a complete task section inside their separate private Markdown notes. Tasks, nested supporting text, lists and new additions remain shared. Each person can understand the sharing boundary, access membership and synchronization state without developer assistance.

The milestone extends the secure 0.1 foundation. It is not permission to defer its cryptography, authorization, offline durability, conflict visibility, snapshots or interoperability requirements.

## 2. Scope authority

This document defines product requirements and acceptance scenarios for planning. The exact storage schema, wire-compatible profile revision and section marker syntax are not defined here. Those belong to normative specifications and fixtures prepared next.

“Required” below means required by the proposed 0.2 delivery contract. Product scope is agreed at the feature level; numerical pilot targets, initial Markdown limits and detailed interaction defaults are proposed planning choices subject to review. Coding agents must not choose incompatible representations independently.

## 3. Existing baseline and new work

| Capability | Baseline or addition |
| --- | --- |
| Encrypted/signed changes, invitations, capability validation | Existing 0.1 obligation; retain and verify |
| Multiple Tasks in one Resource | Existing model; reuse |
| Offline queue, restart safety, snapshots and catch-up | Existing 0.1 obligation; extend to sections |
| Conflict-preserving Task fields and multiple projections | Existing model; preserve |
| Shared section membership, order, nesting and body text | New 0.2 behavior |
| Bulk section sharing and automatic addition of new content | New 0.2 behavior |
| Clear section boundaries, status indicators and access card | New 0.2 product experience |
| Compatibility/migration for new section structures | New 0.2 requirement |

MVP 0.1.0 was released on 2026-10-06, and Shared Tasks 0.3.1 is listed in the Obsidian community plugins. The exact versions, gates and open 0.1 obligations are recorded in `MVP-0.2-ROADMAP.md` §2. Missing 0.1 gates are baseline work, not newly invented 0.2 features.

## 4. Required user journeys

### 4.1 Share an existing section

- Invoke sharing at a heading or over an eligible contiguous selection.
- Preview the exact proposed shared content, including nested content.
- Detect unsupported or ambiguous content before committing.
- Create the dedicated collaboration or use an explicitly supported conversion path.
- Preserve local text outside the selected boundary.
- Produce an invitation using existing LFCP authorization.

A heading may help select an initial range. Subsequent sharing must follow a stable binding, not whichever text happens to fall below a matching heading.

### 4.2 Join and insert

- Accept the invitation, establish authorization and obtain state using the secure path.
- Choose an insertion location in a local note.
- Insert the whole section, with its supported content and durable binding.
- Show joining/loading/failure states. An incomplete load must not be interpreted as an empty section to publish.
- Retrying interrupted onboarding must not create duplicate sections or Task identities.

### 4.3 Work inside the section

- Add and edit tasks, paragraphs, lists and subtasks.
- Newly created content inside a valid shared boundary becomes shared automatically.
- Synchronize deletions and structural changes according to specified semantics.
- Edit supported Task fields directly from Markdown.
- Preserve recognizable Markdown and text outside the boundary.
- Support the same Task as a standalone projection elsewhere without duplicating its authority.

### 4.4 Manage access and local placement

- Inspect current validated membership and distinguish pending invitations from active access.
- Invite additional collaborators when authorized.
- Revoke access using existing capability and key-rotation rules.
- Distinguish removal of one local section projection from deletion of shared content.
- Provide a deliberate detach action that keeps a readable local copy and stops updates for that projection.

Detaching is not leaving the Resource and not revoking access. A retained local copy may still contain data previously shared. Revocation prevents future authorized access under protocol rules; it does not erase copies already received.

### 4.5 Recover from ordinary interruptions

- Restart with pending changes without losing them or reusing actor sequences.
- Reconnect after duplicate, reordered or missing deliveries.
- Reconstruct bindings and local indexes without resetting shared identities.
- Surface a meaningful conflict or rejection with a non-destructive recovery path.
- Export diagnostics that exclude note contents, task text, keys and invitation secrets by default.

## 5. Initial content contract

| Content | Proposed 0.2 treatment |
| --- | --- |
| Section title | Shared title; local heading level and host placement may differ |
| Tasks | Shared title, status, due/scheduled/completion dates, priority, tags; preserve unrepresented fields |
| Paragraphs beneath tasks | Shared text, including multiple paragraphs |
| Text between tasks | Shared section content |
| Nested task items | Shared Task identities and shared placement |
| Ordered and unordered lists | Shared text, sibling order and nesting |
| Inline emphasis, code and link syntax | Preserve supported Markdown source; linked content is not implicitly shared |
| Blank lines and indentation | Preserve meaningful structure; cosmetic rules specified by fixtures |
| Existing Task refs | Preserve supported inline/child-line forms and their semantics |
| Embedded files, images, local note transclusions | File contents are not transferred; unsupported embedded behavior is identified before sharing |
| Tables, fenced code, callouts, nested headings, custom plugin syntax | No claim of general support in this first contract; decide preservation or explicit rejection in the Markdown specification |

Unsupported constructs must never be silently dropped, flattened or left private inside a region presented as fully shared. Before first sharing, reject the unsupported portion or require explicit conversion. If unsupported syntax appears during editing, retain local text, surface the issue and suspend unsafe conversion for the affected section. No destructive remote rewrite may overwrite that unresolved local text.

Dates include existing due and scheduled semantics; recurrence generation is not a new feature of this milestone. Compatibility with the Tasks plugin requires dedicated fixtures and checking the actual installed behavior.

## 6. Structural behavior

Within one section, reorder and reparent operations preserve element identities. Basic cut/paste and indentation workflows must be represented or diagnosed; a dedicated drag-and-drop UI is not required.

Across a shared boundary, distinguish copying, removing a shared element and keeping a private projection. Across Resources, there is no implicit identity-preserving move or atomic cross-resource transaction. Such actions require a defined workflow or an explicit unsupported result.

Concurrent edits must converge under a documented policy. Deletes, moves, subtree edits and restores require test vectors; “Automerge handles it” is not a sufficient contract. Detached projections and missing marker lines must not automatically generate global deletions.

## 7. Visual and status contract

### 7.1 Placement

- A compact double-check indicator at the section heading marks persistent sharing.
- A quiet boundary treatment makes the shared region discoverable while editing.
- Within the section, individual rows emphasize pending activity or problems without repeating prominent healthy badges on every item.
- A standalone shared Task has its own compact indicator.
- Hover/focus gives a short tooltip; activation opens the details card.

Starting visual targets are a 12–14 px mark at a 16 px text size, approximately 6 px separation, stable indicator width and a larger interaction target where needed. These are design starting points, not pixel-frozen acceptance thresholds. Check light/dark themes, scaling, keyboard operation and color-independent state distinctions.

### 7.2 Evidence behind status

| Visible information | Required evidence |
| --- | --- |
| Saved locally | Durable local commit, not just a changed editor buffer |
| Waiting to sync | Relevant pending local changes lack the required server acknowledgement |
| Changes accepted by server | Acknowledgement for the relevant durable changes; no implied peer receipt |
| Offline | Connection state; not automatically a data error |
| Conflict / attention needed | Unresolved model, binding, access or transport condition |
| Shared with participant | Current validated capability state plus clearly qualified identity labeling |

Transport progress and attention state are independent. A section can have all changes acknowledged and still contain a conflict. Its badge must not hide that conflict behind a success color. Initial loading and unknown state must not masquerade as synchronized.

### 7.3 Details card

Show the section name, participant/access list, pending invitations, connection state, local pending changes and actionable problems. Expose invite, authorized access management and detach actions. Use human-friendly aliases with an identity detail fallback; do not present aliases as verified names.

Decorations exist only in rendered UI. They add no characters to Markdown, no dirty-file writes when status changes, and no decorative material to plain-text or formatted clipboard output. Existing binding metadata has separate copy semantics.

## 8. Security and privacy invariants

The whole Resource is the access boundary. A dedicated Resource for a shared section avoids accidentally granting access to unrelated objects. Reusing an existing Resource must reveal its full access scope; hiding objects in a view does not restrict access.

Section changes use the same encrypted, signed and validated LFCP path as Tasks. Local host paths, unselected text, labels for private notes, UI decorations and diagnostic secrets must not enter collaborative payloads.

Missing, overlapping or malformed boundaries must fail closed for publication and destructive projection. Preserve user text and request repair; do not infer an expanded range that could capture adjacent private content.

## 9. Reliability and scale

The initial acceptance corpus contains 100–200 tasks, plus realistic child text, nested lists and Cyrillic/Latin content. This is an evaluation workload, not a claimed maximum or completed benchmark.

Measure initial load, local edit latency, remote projection time, reconnect catch-up, memory and behavior in long documents. Numerical performance budgets are to be set in the test plan against named devices and versions before release. Avoid whole-vault rescans or full-file regeneration for a small edit in the normal path.

Desktop release checks cover macOS, Windows and Linux, carrying forward the 0.1 matrix (automated on three systems; native by hand on macOS); see decision V4 in section 14. Mobile certification and provisioning multiple devices for one identity are not added silently to 0.2.

## 10. Explicit exclusions

- Federation, active-active hosting, direct P2P and multi-home routing.
- Ownership transfer, server migration and coordinator disaster recovery.
- Presence, cursors, typing indicators and read receipts.
- Per-task or per-block ACL inside the shared section.
- Threaded discussion systems, notifications and attributed comment history.
- Attachment upload or remote resolution of private linked notes.
- New editor clients, hosted billing and mandatory global registration.
- Arbitrary full-document Markdown collaboration.
- Recovery after total key loss or automated multi-device identity setup.
- A new recurrence engine or a replacement for Obsidian Tasks.

## 11. Completion gates

| Gate | Observable evidence |
| --- | --- |
| G01 Baseline | Exact component versions identified; unresolved 0.1 requirements classified |
| G02 Contracts | Profile/version strategy, marker grammar and concurrency rules published with fixtures |
| G03 Onboarding | Two clean vaults share/join/insert a section with one invitation; retry is safe |
| G04 Content | Supported nested content round-trips and new items appear automatically at peers |
| G05 Identity | Move/reparent keeps identities; standalone Task projection edits update the same Task |
| G06 Concurrency | Concurrent insert/edit/move/delete cases converge or expose specified conflicts without data loss |
| G07 Durability | Offline edits, client/server restart and snapshot catch-up preserve state and actor safety |
| G08 Privacy | Private text outside boundaries never enters shared plaintext payloads; server retains opaque data |
| G09 Access | Membership, invitations and revocation agree with validated capability state |
| G10 UX | States reflect evidence; tooltips/cards work; decorations do not pollute source or clipboard |
| G11 Compatibility | Old Tasks remain usable; unsupported clients and migrations behave explicitly |
| G12 Release | Desktop matrix, realistic load checks, documented limits and pilot feedback reviewed |

Server plaintext scans alone are insufficient for G08: also inspect the client-side extracted shared payload before encryption using known private fixtures.

## 12. Delivery sequence

1. Establish baseline and approve product scope.
2. Resolve section schema, ordering, text representation, profile compatibility and portable bindings.
3. Publish semantic vectors and Markdown fixtures before dependent implementation.
4. Implement reusable SDK behavior and interoperability.
5. Deliver the two-vault section workflow.
6. Integrate indicators, membership card, diagnostics and recovery behavior.
7. Complete automated checks and a 3–5 pair pilot (decision V2).

Design visual states alongside step 2 so the model exposes the required information. Detailed repository sequencing, issue IDs, estimates and agent prompt packages are intentionally left to the next planning documents.

## 13. Source baseline

Product decisions: discussion of 2026-10-07. Existing contracts: `MVP-0.1-PROTOCOL-SCOPE.md` completion gate; `BACKLOG-MVP-0.1.md` LFCP-058–072; `SHARED-OBJECTS-PROFILE-01.md` §§4–6, 30–36, 78–83; `MARKDOWN-REFS-01.md` §§1–5; `OBSIDIAN-ARCHITECTURE-01.md` §§7–8, 23–24. These documents describe the baseline, not proof of current implementation.

## 14. Review decisions (2026-10-08)

The project owner approved the review of the planning batch on 2026-10-08. The decisions that change or settle this scope are below; the full list (R1–R3, P1–P6, M1–M10, V1–V6) is in `BACKLOG-MVP-0.2.md` §3.

| ID | Effect on this scope |
| --- | --- |
| P1, M9 | A section is a dedicated Resource with the new profile `org.openlfcp.shared-sections.v1`, one invitation per section. Clients that know only Tasks do not see sections; an existing collaboration moves to a section only by explicit copy. |
| P3 | Sharing 100–200 Tasks is an import in several changes with a readiness marker; the 0.1 admission limits are not raised. |
| M1–M5 | Inside a section, Task refs are inline; tabs are supported; the start marker follows the heading; every node carries a marker, hidden in Live Preview by default. |
| M6 | Tables, fenced code, callouts and blockquotes are shared as raw blocks. Nested headings are not supported in 0.2; sharing offers to split the section. |
| M7 | Tasks-plugin tokens such as recurrence stay local; recurrence remains out of scope. |
| M8 | The double check means "shared"; synchronization state is shown by separate icons. |
| M10 | Legacy per-Task commands are disabled or redirected inside a section. |
| V1 | Shared Tasks 0.4.0 with `@openlfcp/*` 0.2.0; release notes name the set "MVP 0.2". |
| V2 | Betas through BRAT pre-releases; early dogfood with 2–3 pairs, then a pilot with 3–5 pairs (at least two non-developers) for 7 days. |
| V3 | On mobile, sections are read-only or marked unsupported; the plugin stays available on mobile. |
| V4 | Native checks on macOS, a CI harness on macOS, Windows and Linux, and manual smoke on Windows and Linux. Performance budgets are measured on macOS; Windows and Linux are "functional, not performance-qualified". |
