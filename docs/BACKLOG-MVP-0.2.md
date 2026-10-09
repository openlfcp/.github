# BACKLOG-MVP-0.2

**Project:** OpenLFCP / Shared Tasks, by OpenLFCP  
**Date:** 2026-10-08  
**Status:** Reviewed, 2026-10-08: the planning batch of 2026-10-07 with the owner-approved review  
**Size:** 116 tasks in 13 epics, across seven milestones  
**Machine-readable companion:** BACKLOG-MVP-0.2.json

## 1. How to execute this backlog

Use IDs **LFCP-02-001…LFCP-02-109**. Tasks 083-105 come from the review; each names its source in the review summary. Task 106 came from the W0 recovery drill, 107 from the spec baseline work, 108 and 109 from the corpus work of task 010. They belong to MVP 0.2 and do not rename, replace or imply completion of legacy LFCP-NNN tasks. No GitHub issues, assignments, PRs or deployments have been created by preparing this backlog.

The MVP 0.1 facts are recorded in MVP-0.2-ROADMAP §2 (Starting evidence). A task is NOT_STARTED unless its card carries a status note with evidence. First inspect and reuse existing code. Where behavior already meets a task, close it with exact implementation/test evidence rather than rewriting it. Server audit tasks may legitimately end with verified no-change results.

Dependencies, not numeric order, determine execution. Each card names one primary repository, its accepted inputs, measurable outcome, tests and deliverables. Cross-repository defects need linked companion tasks; do not fix a server problem inside the Obsidian plugin. Exact paths, package names, owners and build commands are resolved by task 001 and the baseline audits, not invented here.

P0 and P1 are both required for release. P0 marks safety/foundation/technical qualification; P1 marks required product, documentation, pilot or release work. P1 does not mean optional or a future MVP. Read the task dependencies before choosing work by priority.

## 2. Authority and shared definition of done

Read AGENT-OPERATING-GUIDE.md and MVP-0.2-SCOPE.md once, then the task's smallest named reading set. The specification drafts SHARED-SECTIONS-PROFILE-01, SHARED-SECTIONS-TEST-VECTORS-01, MARKDOWN-SECTIONS-01, MARKDOWN-SECTIONS-FIXTURES-01, MVP-0.2-COMPATIBILITY-AND-MIGRATION and the Obsidian drafts (OBSIDIAN-SECTIONS-ARCHITECTURE-02, OBSIDIAN-SHARED-SECTIONS-UX-01, OBSIDIAN-SYNC-INDICATORS-01) are to be published with LFCP-02-007/083; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN is not published, its change groups RP00-RP12 are folded into this backlog. Use current canonical revisions pinned by task 007. Protocol/profile/Markdown contracts take precedence over planning text. Resolve a true contract gap in its owning draft and fixtures before relying on new behavior in code.

A task is DONE when its acceptance criteria are met, required checks ran on the relevant pinned inputs, and its deliverables include exact changed files/commits, commands/results, evidence locations, compatibility impact and remaining issues. A passing generated reference model is not independent implementation evidence. No screenshots-only proof of source, security or clipboard invariants.

Use NOT_STARTED, IN_PROGRESS, BLOCKED, IN_REVIEW and DONE. The release record separately uses PASS/FAIL/NOT_RUN/BLOCKED for evidence. A completed audit or pilot observation may have findings: it closes the investigation, not the failed product gate. Tasks 056, 069, 073, 077 and 082 cannot claim qualifying success while relevant inherited/new required blockers remain open.

When a baseline gap or pilot defect needs code, append focused tasks starting at LFCP-02-110, with one owning repository and a regression test. Update affected dependency and gate links. Do not bury unknown work under an already-DONE audit, reuse old IDs or assume a blanket remediation task was implemented. Task 076 coordinates this process; actual repairs remain separately reviewable.

Every implementation change preserves the secure 0.1 subset, legacy Task support, private-source boundaries, actor/nonce safety, retained deleted content and explicit new-profile import. No protocol crypto in the plugin, plaintext Task logic in the server, per-node ACL, read receipts, silent legacy dual-write, arbitrary Markdown support or unapproved physical CRDT garbage collection.

Prepare artifacts and tests before release actions. Publication/deployment tasks use the project's recorded authorization and actual execution-time requirements; this document does not perform or preapprove those external actions.

## 3. Owner decisions (fixed facts for every task)

Approved by the project owner on 2026-10-08 with the review of the planning batch. Tasks implement them; reopening one needs an owner decision, not a task-level choice.

| ID | Decision |
| --- | --- |
| R1 | ADR 0008: adopt (c), bidirectional reconciliation with relay plus the server refusing a dangling `previous`; (d) deferred. Shipped as 0.1.x sustaining before 0.2: `mvp-0.1-baseline.9`, server 0.3.0 (with `lfcp-admin`), sdk-ts 0.1.3, plugin 0.3.2 (088). |
| R2 | POST-001 hold-and-retry goes into the same baseline.9 (089). |
| R3 | Forward compatibility in 0.3.2: the profile is checked before the claim (`acceptInvitation` option, 086); another profile is never opened; the user is told a newer version is needed (087). |
| P1 | New profile `org.openlfcp.shared-sections.v1` (ADR 0009, 083); NEXT-001 is closed. Legacy clients do not see sections; migration is by copy. |
| P2 | Violations visible in the change are rejected at admission; other invalid history is isolated per subtree, not per section. |
| P3 | Import as several changes with a readiness marker; long Text inserts split; the 0.1 limits are not raised (084). |
| P4 | Baseline series `mvp-0.2-baseline.N` from baseline.8 (.9 after W0); SOP §§7-18 and §74.1 imported; a diagnostics registry; exact shared admission limits (090). |
| P5 | Two moves into one parent stay a conflict; revisit after the pilot. |
| P6 | Corpus engine: Automerge 3.5.0, the project's real pin. |
| M1 | Revised by the orchestrator on 2026-10-08, pending the owner's review: inside sections too, Task refs are child-line, as for standalone Tasks; Enter keeps the ref with its Task through CodeMirror transactions (obsidian ADR 0001, accepted for sections). The approved text was inline refs inside sections. |
| M2 | Tabs in indentation are supported as in 0.1. |
| M3 | Sections write through CodeMirror transactions in open notes and `vault.process` in closed ones; legacy Tasks stay on the file path; an obsidian ADR records it. |
| M4 | The start marker sits right after the heading. |
| M5 | A marker on every node, hidden in Live Preview by default; the website's "one invisible comment" promise is rewritten. |
| M6 | Tables, callouts, fences and blockquotes travel as raw blocks; no nested headings in 0.2 (share offers to split). |
| M7 | Tasks-local tokens (🔁 🛫 ➕ ❌ 🔼) stay local, shown in preview; a recurring-Task fixture is added. |
| M8 | A double check means "shared"; synchronization state has separate icons. |
| M9 | One Resource and one invitation per section. |
| M10 | POST-018 commands and Detach are disabled or redirected inside sections, unchanged outside (100). |
| V1 | Versions: plugin 0.4.0, `@openlfcp/*` 0.2.0, sdk-rs and examples v0.2.0, spec `mvp-0.2-baseline.N`, server only if changed. Release notes say "MVP 0.2" with a version table. |
| V2 | Betas `0.4.0-beta.N` through BRAT; manifest.json on main moves only at GA. Early dogfood 2-3 pairs (105); pilot 3-5 pairs with at least two non-developers, 7 days. |
| V3 | Mobile: sections read-only or marked unsupported; `isDesktopOnly` stays false (095). |
| V4 | Native checks on macOS; the CI harness on three systems; manual smoke on Windows and Linux; p95 budgets on macOS only, Windows/Linux "functional, not performance-qualified". |
| V5 | During development obsidian takes sdk-ts by a commit pin (`sdk-ts.lock`); betas use `0.2.0-rc.N` on npm `next`. |
| V6 | SCOPE, ROADMAP, BACKLOG and TEST-PLAN are published in `.github/docs/`, specification drafts in spec (101); agent prompts, the narrative and the review reports stay private. |
| V7 | sdk-ts is published by CI: a pushed tag `vX.Y.Z` runs `release.yml`, which publishes with npm Trusted Publishing (OIDC, provenance) after the owner's approval in the GitHub environment `npm-publish`; the manual checklist is the fallback. A final release goes to `latest`, a prerelease to `next`; `next` is not moved to final versions. |
| V8 | W0 ships sdk-ts 0.1.3, not 0.1.2: 0.1.2 went to npm without build output and is deprecated (`latest` and `next` back on 0.1.1 until 0.1.3); 0.1.3 is the same code, published by CI. Shared Tasks 0.3.2 pins 0.1.3 and sets `minAppVersion` 1.13.4. |

## 4. Modules, workers and waves

TypeScript and Rust models are written by different workers. One writer per module; reserve modules with the orchestrator before each bundle.

| Module | Worker | Repositories |
| --- | --- | --- |
| A | worker A | sdk-ts, examples, release tooling (.github/scripts); later possibly the obsidian UI zone `src/ui/` |
| B | worker B | spec, sdk-rs, server |
| C | worker C | obsidian |

| Wave | Tasks | Owner releases |
| --- | --- | --- |
| W0 | 086-089 (ADR 0008 (c), POST-001, profile check before claim, 0.3.2); 100 as analysis only | baseline.9, server 0.3.0, sdk-ts 0.1.3 (CI), plugin 0.3.2; LAUNCH-003 (a)(b) |
| W1 (M02-0) | 101, 001-006 (narrowed to recorded facts), spike of 096 | push |
| W2 (M02-1) | 083 -> 084 -> 007-010 -> 090; 085; parser 034-035 on the fixed M1-M6 | tag `mvp-0.2-baseline.1` |
| W3-W4 | TS models 011-018, Rust 019-022, interop 023-024, durability 025-033, 097, 098 | `0.2.0-rc.1` on `next` when needed |
| W5 (M02-2) | editor 036-048 | one-vault demo |
| W6 (M02-3/4) | two vaults 049-056, UX 057-066, then 105 (dogfood) | beta.1 through BRAT; server deploy if changed |
| W7 (M02-5) | 067-074, 094, 099, 102 | `0.2.0-rc.N`, `0.4.0-beta.N` |
| W8 (M02-6) | 075-082, 091-093, 103, 104 | pilot, go/no-go, publications |

Brief tasks in bundles of one session each, for example 011-013, 014-016, 017-018, 019-020, 021-022, 025-026, 027-028, 029-030, 034-035, 041-042, 043-044, 045-046, 057-059, 061-062. A bundle keeps every task's own acceptance and evidence.

## 5. Brief overrides (project rules over the batch prompts)

The planning batch's agent prompts assume branches, PRs and agent-run publications. Every brief adds these rules; they win over the prompt text.

| Topic | Batch prompt | Project rule |
| --- | --- | --- |
| Branches and PRs | Isolated branches/worktrees, draft PRs | Work on `main`; branches and PRs only on request; `.worktrees/` if the owner asks |
| Commits | Not defined | `committer "type(scope): ..." paths...` or `--patch`; atomic Conventional Commits; no `git add`, `--amend`, `--no-verify`; after the commit `git show --stat HEAD` and a clean `git status` |
| External actions | 078-082: the agent publishes with "recorded authorization" | Push, tags, npm publish, GitHub releases and deploys are the owner's; the agent prepares the runbook and exact commands |
| Gates | "Commands actually executed" | The gate checks the commit (hash-gated); candidates run `rc-verify.py` from a manifest; fresh clones share one `CARGO_TARGET_DIR` |
| Neighbour dependencies | "Pinned candidate packages" | Build siblings at their lock commit: `spec.lock`, `sdk-rs.lock`, `server.lock`, `conformance/pins.json`, and `sdk-ts.lock` during 0.2 development (V5); move a lock in the same change |
| Deletion and scratch | Not defined | `trash` only; scratch outside the tree; no debugging leftovers in commits |
| Documentation | "Existing docs convention" | kebab-case under `docs/` (except established UPPER-case artifact names), a `docs/NAVIGATOR.md` row, `doccheck.py` before committing |
| Load | 100 seeds, W2000, 200-sample p95 | `CARGO_BUILD_JOBS=4`, at most two test threads; heavy runs only with the orchestrator's consent |
| Project rules | "Applicable AGENTS.md" | There is no AGENTS.md: use `.github/docs/AGENT-OPERATING-GUIDE.md`, `engineering-conventions.md` and the workers' rule files |
| Language | English | Code, commits and repository docs in English; reports to the orchestrator in Russian |

## 6. Planning references and granularity

M02-0…M02-6 are roadmap milestones; RP00…RP12 are repository-plan change groups; G01…G12 are scope gates; T01…T12 are test families. None is a replacement issue number. Milestone labels on tasks indicate review targets, not a ban on earlier preparation.

Repository:examples owns the initial cross-component harness where no dedicated interop repository is established. The website source is kept privately by the project, the organization profile is .github/profile/README.md and the public server runs on the owner's server stack and is deployed only by the owner. Logical responsibility can be implemented in an existing appropriate package; do not create infrastructure solely to match a label.

Some qualification/release tasks coordinate several environments or defects, but their output is a concrete report/build/decision. Model and editor implementation tasks are split by invariant and failure boundary. Further splits may be appropriate after baseline inspection; preserve parent IDs and traceability.

No calendar durations, story-point estimates, assignee names or task completion claims are fabricated. The machine-readable graph supports later estimation and prompt generation. Mock UI preparation can begin early, but only production integration evidence completes the related task.

## 7. Epic index

| Epic | Tasks | Focus | Review milestone |
| --- | --- | --- | --- |
| E00 | 086, 087, 088, 089, 113 | Sustaining 0.1.x before 0.2 (wave W0) | M02-0 |
| E01 | 001, 002, 003, 004, 005, 006, 101 | Baseline and inherited obligations | M02-0 |
| E02 | 007, 008, 009, 010, 083, 084, 090, 107, 108 | Pinned contracts and corpus | M02-1 |
| E03 | 011, 012, 013, 014, 015, 016, 017, 018, 085, 114 | TypeScript section model | M02-1 |
| E04 | 019, 020, 021, 022, 023, 024, 109, 111 | Rust and independent interoperability | M02-1 |
| E05 | 025, 026, 027, 028, 029, 030, 097, 098, 106, 110, 115 | Durability and SDK evidence | M02-2 |
| E06 | 031, 032, 033, 116 | Opaque server compatibility | M02-3 |
| E07 | 034, 035, 036, 037, 038, 039, 040, 041, 042 | Markdown ownership and reconciliation | M02-2 |
| E08 | 043, 044, 045, 046, 047, 048, 095, 096 | Native editor lifecycle | M02-2 |
| E09 | 049, 050, 051, 052, 053, 054, 055, 056, 100 | Secure sharing, join and import | M02-3 |
| E10 | 057, 058, 059, 060, 061, 062, 063, 064, 065, 066 | Status, access and recovery UX | M02-4 |
| E11 | 067, 068, 069, 070, 071, 072, 073, 074, 091, 094, 099, 102, 105, 112 | Qualification and candidate | M02-5 |
| E12 | 075, 076, 077, 078, 079, 080, 081, 082, 092, 093, 103, 104 | Pilot and public release | M02-6 |

## 8. Task index

| ID | Task | Primary repository | Priority | Depends on |
| --- | --- | --- | --- | --- |
| LFCP-02-001 | Inventory repositories, releases and ownership | .github | P0 | 101 |
| LFCP-02-002 | Verify inherited client security and durability gates | sdk-ts | P0 | 001 |
| LFCP-02-003 | Audit server ACK, persistence and configured limits | server | P0 | 001 |
| LFCP-02-004 | Audit legacy client and unknown-profile behavior | obsidian | P0 | 001 |
| LFCP-02-005 | Pin editor environments and qualification budgets | obsidian | P0 | 001 |
| LFCP-02-006 | Publish baseline gaps and integration entry conditions | .github | P0 | 002, 003, 004, 005 |
| LFCP-02-007 | Pin section specifications and compatibility authority | spec | P0 | 006, 083, 084 |
| LFCP-02-008 | Integrate reproducible corpus and conformance entry points | spec | P0 | 007 |
| LFCP-02-009 | Freeze SDK receipt/status and parser integration contracts | spec | P0 | 003, 007, 088 |
| LFCP-02-010 | Expand missing semantic and Markdown edge fixtures | spec | P0 | 007, 008 |
| LFCP-02-011 | Add TypeScript section profile dispatch and schema | sdk-ts | P0 | 007, 008, 085, 090 |
| LFCP-02-012 | Implement section and Task/node creation intents | sdk-ts | P0 | 011, 084 |
| LFCP-02-013 | Implement immutable placement insertion and moves | sdk-ts | P0 | 012 |
| LFCP-02-014 | Derive effective tree and structural conflict facts | sdk-ts | P0 | 013 |
| LFCP-02-015 | Implement lifecycle, ancestor hiding and restoration | sdk-ts | P0 | 012, 014 |
| LFCP-02-016 | Implement collaborative Text and split/join operations | sdk-ts | P0 | 012, 013, 015, 010 |
| LFCP-02-017 | Harden TypeScript profile validation | sdk-ts | P0 | 010, 014, 015, 016 |
| LFCP-02-018 | Run production TypeScript conformance adapter | sdk-ts | P0 | 008, 017 |
| LFCP-02-019 | Implement independent Rust schema and actor dispatch | sdk-rs | P0 | 007, 008, 085, 090 |
| LFCP-02-020 | Implement Rust node, placement and tree behavior | sdk-rs | P0 | 019 |
| LFCP-02-021 | Implement Rust lifecycle and collaborative Text | sdk-rs | P0 | 010, 020 |
| LFCP-02-022 | Validate Rust history and consume the full corpus | sdk-rs | P0 | 008, 021 |
| LFCP-02-023 | Build bidirectional TS/Rust exchange harness | examples | P0 | 018, 022 |
| LFCP-02-024 | Add deterministic concurrency schedules and minimized regressions | examples | P0 | 010, 023 |
| LFCP-02-025 | Add durable intent-to-commit receipt correlation | sdk-ts | P0 | 009, 012, 089 |
| LFCP-02-026 | Persist outbound batches and honest status attribution | sdk-ts | P0 | 003, 009, 025 |
| LFCP-02-027 | Expose validated access and control freshness | sdk-ts | P0 | 009, 011 |
| LFCP-02-028 | Integrate snapshots and safe restart continuation | sdk-ts | P0 | 025, 026, 012 |
| LFCP-02-029 | Upgrade local SDK storage alongside legacy Resources | sdk-ts | P0 | 025, 027, 028 |
| LFCP-02-030 | Qualify SDK failure and status recovery | sdk-ts | P0 | 026, 027, 028, 029, 089 |
| LFCP-02-031 | Verify section transport limits and opaque persistence | server | P0 | 003, 007, 012 |
| LFCP-02-032 | Prove ACK and server restart guarantees | server | P0 | 003, 031, 088 |
| LFCP-02-033 | Retain authorization and negative secure-ingest behavior | server | P0 | 002, 031, 032 |
| LFCP-02-034 | Parse lexical section boundaries and reserved markers | obsidian | P0 | 007, 008, 090 |
| LFCP-02-035 | Parse supported Task, item and paragraph trees | obsidian | P0 | 034 |
| LFCP-02-036 | Map owned spans, field tokens and Unicode offsets | obsidian | P0 | 035, 009 |
| LFCP-02-037 | Infer safe semantic intents from trusted projection bases | obsidian | P0 | 009, 036 |
| LFCP-02-038 | Persist projection bases, candidates and journals | obsidian | P0 | 009, 025, 029, 036, 098 |
| LFCP-02-039 | Commit local section edits through the SDK journal | obsidian | P0 | 017, 026, 027, 037, 038 |
| LFCP-02-040 | Apply remote changes with minimal revision-checked patches | obsidian | P0 | 014, 028, 036, 038 |
| LFCP-02-041 | Coordinate open editors, closed files and external changes | obsidian | P0 | 039, 040 |
| LFCP-02-042 | Prevent generated-write feedback without losing user edits | obsidian | P0 | 039, 040, 041 |
| LFCP-02-043 | Integrate native edits, selection and IME | obsidian | P0 | 041, 042, 096 |
| LFCP-02-044 | Bridge native undo/redo to compensating intents | obsidian | P0 | 015, 043 |
| LFCP-02-045 | Maintain multiple projections and rebuild safely | obsidian | P0 | 038, 043 |
| LFCP-02-046 | Implement context-aware delete, detach, duplicate and cut/paste | obsidian | P0 | 015, 037, 044, 045 |
| LFCP-02-047 | Run production Markdown fixtures and extraction canaries | obsidian | P0 | 010, 039, 040, 046 |
| LFCP-02-048 | Render safe boundaries and minimal states in all editor modes | obsidian | P0 | 034, 043, 045 |
| LFCP-02-049 | Build exact-range share preview and preflight | obsidian | P0 | 035, 047, 048 |
| LFCP-02-050 | Journal dedicated section creation and hosting readiness | obsidian | P0 | 025, 026, 031, 032, 049, 084 |
| LFCP-02-051 | Integrate secure invitation and join retry states | obsidian | P0 | 027, 033, 050, 086, 087 |
| LFCP-02-052 | Insert only fully loaded section projections | obsidian | P0 | 028, 045, 048, 051, 097 |
| LFCP-02-053 | Preflight legacy-to-section explicit copy/import | obsidian | P0 | 004, 027, 049 |
| LFCP-02-054 | Persist import phases and non-destructive rollback | obsidian | P0 | 029, 050, 052, 053 |
| LFCP-02-055 | Integrate dual-profile upgrade and downgrade UX | obsidian | P0 | 004, 029, 045, 054 |
| LFCP-02-056 | Qualify the secure two-vault section slice | examples | P0 | 006, 023, 030, 033, 044, 046, 047, 052, 055, 097 |
| LFCP-02-057 | Implement pure status reducer and race handling | obsidian | P0 | 009, 026, 027 |
| LFCP-02-058 | Implement compact badges and quiet row aggregation | obsidian | P1 | 048, 057 |
| LFCP-02-059 | Build tooltip and section details card | obsidian | P1 | 057, 058 |
| LFCP-02-060 | Add validated access, invitations and revocation actions | obsidian | P1 | 027, 051, 059 |
| LFCP-02-061 | Build scalar, structure and deletion recovery views | obsidian | P1 | 014, 015, 016, 040, 059 |
| LFCP-02-062 | Build boundary, base-loss and unsupported-content repair | obsidian | P1 | 037, 038, 047, 059 |
| LFCP-02-063 | Implement and verify native/readable/shared clipboard paths | obsidian | P0 | 046, 058, 059, 096 |
| LFCP-02-064 | Complete keyboard, focus and accessible visual behavior | obsidian | P1 | 058, 059, 060, 061, 062, 063 |
| LFCP-02-065 | Provide sanitized local diagnostics and export preview | obsidian | P1 | 030, 038, 059, 060, 098 |
| LFCP-02-066 | Execute complete native UX and status acceptance | obsidian | P0 | 056, 060, 061, 062, 063, 064, 065, 096, 100 |
| LFCP-02-067 | Generate scale workloads and instrument performance | obsidian | P0 | 005, 010, 043, 048, 056, 096 |
| LFCP-02-068 | Meet performance budgets without changing semantics | obsidian | P0 | 058, 059, 067, 096 |
| LFCP-02-069 | Qualify the supported desktop and plugin matrix | obsidian | P0 | 005, 055, 063, 064, 066, 068, 095, 096 |
| LFCP-02-070 | Qualify integrated crash, access and compatibility recovery | examples | P0 | 024, 030, 033, 054, 055, 056, 066, 106 |
| LFCP-02-071 | Publish secure headless section examples | examples | P1 | 023, 028, 033, 056 |
| LFCP-02-072 | Document the two-vault demonstration and recovery workflow | examples | P1 | 056, 066, 071 |
| LFCP-02-073 | Assemble immutable candidate builds and full evidence record | .github | P0 | 006, 018, 022, 024, 066, 069, 070, 071, 072, 098, 099, 102 |
| LFCP-02-074 | Rehearse compatible rollback and demo restore | server | P0 | 032, 055, 073, 088 |
| LFCP-02-075 | Run the opt-in pair pilot and record outcomes | obsidian | P1 | 072, 073, 074, 091, 094, 103, 105 |
| LFCP-02-076 | Close pilot defects and requalify the final candidate | obsidian | P0 | 075 |
| LFCP-02-077 | Record concrete release go/no-go | .github | P1 | 076 |
| LFCP-02-078 | Update website installation, limits and release claims | website | P1 | 077, 080, 081, 104 |
| LFCP-02-079 | Update organization profile for the released milestone | .github | P1 | 078 |
| LFCP-02-080 | Publish approved plugin release artifacts | obsidian | P1 | 074, 077, 092, 104, 081 |
| LFCP-02-081 | Roll out or verify unchanged demo sync service | server | P1 | 074, 077 |
| LFCP-02-082 | Close release evidence and record follow-up ownership | .github | P1 | 078, 079, 080, 081, 093 |
| LFCP-02-083 | ADR 0009: shared sections profile | spec | P0 | — |
| LFCP-02-084 | Normative multi-change import and exact profile admission limits | spec | P0 | 083 |
| LFCP-02-085 | Shared 0.1 admission module for both profiles | sdk-ts (companion: sdk-rs, by another worker) | P0 | 007 |
| LFCP-02-086 | acceptInvitation checks the Data Profile before the claim | sdk-ts | P0 | — |
| LFCP-02-087 | Plugin 0.3.2: forward compatibility with unknown profiles | obsidian | P0 | 086, 088, 089 |
| LFCP-02-088 | ADR 0008 (c): recovery after server data loss | spec + sdk-ts + sdk-rs + server (split per repository at dispatch) | P0 | — |
| LFCP-02-089 | POST-001: hold and retry (actor, seq) collisions | spec + sdk-ts + sdk-rs (split per repository at dispatch) | P0 | — |
| LFCP-02-090 | Tag mvp-0.2-baseline.N and move consumer spec.lock pins | spec | P0 | 007, 008, 010, 084 |
| LFCP-02-091 | Publish @openlfcp/* 0.2.0-rc.N on next | sdk-ts | P1 | 018, 030 |
| LFCP-02-092 | Publish @openlfcp/* 0.2.0 on latest and pin it in obsidian | sdk-ts | P1 | 077 |
| LFCP-02-093 | Tag v0.2.0 and publish the MVP 0.2 release notes | .github | P1 | 077, 092 |
| LFCP-02-094 | Pre-release beta channel for the plugin | obsidian | P0 | 087 |
| LFCP-02-095 | Section behaviour on mobile | obsidian | P0 | 048 |
| LFCP-02-096 | Native Obsidian harness in CI on three systems | obsidian | P0 | 005 |
| LFCP-02-097 | POST-007: the plugin publishes Snapshots | obsidian | P0 | 028 |
| LFCP-02-098 | POST-006: local state encrypted at rest | sdk-ts | P0 | 029 |
| LFCP-02-099 | POST-010: deterministic engine-trap test | sdk-ts | P0 | — |
| LFCP-02-100 | Legacy commands inside sections (POST-018, Detach) | obsidian | P0 | 046, 049 |
| LFCP-02-101 | Import the MVP 0.2 documents into the public repositories | .github | P0 | — |
| LFCP-02-102 | Generalize rc-verify for MVP 0.2 | .github | P0 | 090 |
| LFCP-02-103 | Pilot operations: recruiting, consent and support | .github (owner) | P1 | — |
| LFCP-02-104 | README, user guide and access disclosure for sections | obsidian | P1 | 066 |
| LFCP-02-105 | Early BRAT dogfood of share, insert and edit | obsidian | P1 | 048, 049, 052, 087, 091, 094 |
| LFCP-02-106 | A member refused before its grant is re-supplied recovers by itself | sdk-ts (companion: obsidian) | P1 | 088 |
| LFCP-02-107 | Move the shared-sections vectors to lfcp-vector-format/1 | spec | P1 | 010 |
| LFCP-02-108 | A6: refuse a non-concurrent ID reuse across categories at admission | spec (companions: sdk-ts, sdk-rs) | P2 | 024, 075 |
| LFCP-02-109 | Linear-time retained concurrent edits in the Rust section model | sdk-rs | P2 | 010 |
| LFCP-02-110 | Journal a capability claim before it is sent | sdk-ts (companion: obsidian) | P1 | 051 |
| LFCP-02-111 | Linear-time section admission and authoring in the Rust model | sdk-rs | P1 | 109 |
| LFCP-02-112 | Section history growth policy | obsidian (companions: spec, sdk-ts) | P1 | 067 |
| LFCP-02-113 | Patch release 0.1.4 and plugin 0.3.3 with the SPEC-PATCH-10 admission | sdk-ts (companions: obsidian, sdk-rs) | P1 | 090 |
| LFCP-02-114 | SPEC-PATCH-10 admission in sdk-ts (F2-F4) | sdk-ts | P0 | 090 |
| LFCP-02-115 | A revoked member learns the refusal and reports it honestly | sdk-ts (companion: obsidian) | P0 | 027, 106 |
| LFCP-02-116 | The server refuses a store written by a newer server | server | P1 | 074 |

Dependency numbers in the index abbreviate the same LFCP-02 namespace; full IDs are used in every card and JSON. The forward dependencies of 078 on 080/081 are intentional: public website claims follow actual distribution/demo verification.

## E00. Sustaining 0.1.x before 0.2 (wave W0)

### LFCP-02-086 — acceptInvitation checks the Data Profile before the claim

**Primary repository:** sdk-ts  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** implementation / P0 / DONE — Released: @openlfcp/*@0.1.3 on npm (CI trusted publishing, 2026-10-08; tag sdk-ts v0.1.3 on 7e9462f) and Shared Tasks 0.3.2 (obsidian tag 0.3.2 on 1cfce1e).  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); LFCP-WIRE-01.md  
**Gate / test trace:** G11 / T08

**Goal:** Stop a one-time invitation from being spent by a client that cannot open the Resource.

**Acceptance:**

1. acceptInvitation takes dataProfiles?: readonly string[]; when the Genesis profile is not in it, the result is { kind: "profile-unsupported", resourceId, code: "PROFILE_UNSUPPORTED", dataProfile }.
2. The check runs after the chain is fetched and the link secret is verified, before KEY_PACKAGE_GET and the claim; nothing is stored and the invitation stays usable.
3. Without the option the behaviour is unchanged; CHANGELOG records the additive union member.

**Required checks:** Live test against the Rust server: another-profile joiner stores nothing, then a claim through the same one-time link succeeds; client unit tests.

**Deliverables:** sdk-ts change, live test and CHANGELOG; ships in sdk-ts 0.1.3 (0.1.2 went to npm without build output and is deprecated).

### LFCP-02-087 — Plugin 0.3.2: forward compatibility with unknown profiles

**Primary repository:** obsidian  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** release / P0 / DONE — Released as Shared Tasks 0.3.2 (obsidian tag 0.3.2 on 1cfce1e; audit a2f48de); docs/releases/0.3.2.md.  
**Depends on:** LFCP-02-086, LFCP-02-088, LFCP-02-089  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; obsidian: docs/devel/release.md  
**Gate / test trace:** G11 / T08

**Goal:** Make released clients refuse section Resources clearly before any section invitation exists.

**Acceptance:**

1. Join passes dataProfiles: [PROFILE_ID]; profile-unsupported shows that a newer Shared Tasks version is needed and writes nothing.
2. A stored Resource of another profile is never opened or merged as Shared Objects.
3. Released as 0.3.2 through the catalog with the eight @openlfcp/* packages at exactly 0.1.3 from npm (never 0.1.2, deprecated without dist/) and minAppVersion 1.13.4, before the first section beta (094/105).

**Required checks:** Unit and live tests for join of another profile; the existing suite; eslint-plugin-obsidianmd 0 errors.

**Deliverables:** Plugin 0.3.2 release candidate, release notes and the owner runbook.

### LFCP-02-088 — ADR 0008 (c): recovery after server data loss

**Primary repository:** spec + sdk-ts + sdk-rs + server (split per repository at dispatch)  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** implementation / P0 / DONE — Released: @openlfcp/*@0.1.3 on npm (CI trusted publishing, 2026-10-08; tag sdk-ts v0.1.3 on 7e9462f) and Shared Tasks 0.3.2 (obsidian tag 0.3.2 on 1cfce1e).  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); spec: adr/0008-recovery-after-server-data-loss.md; LFCP-WIRE-01.md; .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G07 / T01, T07

**Goal:** Heal a restored server and its clients without the NO_PROGRESS wedge.

**Acceptance:**

1. spec: ADR 0008 accepted with (c) and (d) deferred; SPEC-PATCH for bidirectional anti-entropy with relay and the server refusal of a dangling previous; open questions 2-4 answered and approved by the orchestrator; baseline mvp-0.1-baseline.9.
2. sdk-ts and sdk-rs: a client re-uploads accepted units, Control Records and Key Packages the server lacks; server: refuses a dangling previous with the agreed code.
3. A live interop test reproduces the 2026-10-06 drill (back up, write, restore, write) and a second client catches up; released as the 0.1.x sustaining set (server 0.3.0, sdk-ts 0.1.3 published by CI through npm Trusted Publishing, sdk-rs and examples tags).

**Required checks:** Spec vectors, both SDK suites, server tests and the live drill test; rc-verify on the sustaining set.

**Deliverables:** SPEC-PATCH and baseline.9, code in three repositories, release notes and owner commands.

### LFCP-02-089 — POST-001: hold and retry (actor, seq) collisions

**Primary repository:** spec + sdk-ts + sdk-rs (split per repository at dispatch)  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** implementation / P0 / DONE — Released: @openlfcp/*@0.1.3 on npm (CI trusted publishing, 2026-10-08; tag sdk-ts v0.1.3 on 7e9462f) and Shared Tasks 0.3.2 (obsidian tag 0.3.2 on 1cfce1e).  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/open-decision-actor-seq-collision.md; SHARED-OBJECTS-PROFILE-01.md; .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G06, G07 / T02, T07

**Goal:** Converge in the equivocation corner instead of silently dropping a collaborator.

**Acceptance:**

1. SHARED-OBJECTS-PROFILE-01 §14.1 holds the later change and retries it after a rebuild that removes changes; vectors added; in baseline.9 with 088.
2. sdk-ts and sdk-rs hold instead of profile-rejected and retry after exclude/rebuild; the held state is visible to the application.
3. A live interop case converges once the replica learns of the equivocation; a malicious writer still affects only its own history.

**Required checks:** Vectors in both SDKs and the live interop case.

**Deliverables:** Spec patch, SDK changes and the application-visible held state documented for the plugin.

### LFCP-02-113 — Patch release 0.1.4 and plugin 0.3.3 with the SPEC-PATCH-10 admission

**Primary repository:** sdk-ts (companions: obsidian, sdk-rs)  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** release / P1 / IN_PROGRESS — Decided yes (owner: "you decide", orchestrator). sdk-ts 0.1.4 candidate 21c7fe3 on branch release-0.1.4 (from v0.1.3): the SPEC-PATCH-10 admission at mvp-0.1-baseline.10; verified by the orchestrator on a fresh clone; the owner tags v0.1.4 and publishes. Plugin 0.3.3 follows the npm 0.1.4 release (3d).  
**Depends on:** LFCP-02-090  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/npm-publish-checklist.md  
**Gate / test trace:** G11 / T08

**Goal:** Give 0.1.x clients the §11.3 and §11.4 admission (ADR 0010) before 0.2, if the owner wants it.

**Acceptance:**

1. The owner decides whether 0.1.x gets a patch release with the canonical-change and operation-reference checks.
2. If so: sdk-ts 0.1.4 and Shared Tasks 0.3.3 pin mvp-0.1-baseline.10 and pass its vectors.
3. Released through the CI publication of V7 and the plugin release runbook; the 0.2 line is not delayed by it.

**Required checks:** The release gates of the 0.1 line, if released.

**Deliverables:** An owner decision; then the patch release runbook.

## E01. Baseline and inherited obligations

### LFCP-02-001 — Inventory repositories, releases and ownership

**Primary repository:** .github  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** audit / P0 / DONE — .github 204af26: release/mvp-0.2-baseline-inventory.md and mvp-0.2-baseline-manifest.json (rc-verify --from-heads, 2026-10-08).  
**Depends on:** LFCP-02-101  
**Read first:** AGENT-OPERATING-GUIDE.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.1-PROTOCOL-SCOPE.md; BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/rc-verification.md  
**Gate / test trace:** G01 / T01

**Goal:** Establish the actual execution baseline without rebuilding the existing stack.

**Acceptance:**

1. Record canonical URLs, base commits, versions, locks, artifact digests, owners and actual build/test commands for each component.
2. Resolve the real website, organization-profile and demo-deployment sources; mark missing access/metadata explicitly.
3. Retain old LFCP issue IDs; record which current documents and artifacts supersede historical patches.
4. Narrowed by the review: record the facts already established (MVP-0.2-ROADMAP §2: rc7/rc8 manifests, tags, npm versions, CI, release workflows) as an rc-verify --from-heads manifest instead of rediscovering them.

**Required checks:** Validate commands and artifact references against actual checkouts/releases; no production mutation.

**Deliverables:** Baseline manifest and repository/path map.

### LFCP-02-002 — Verify inherited client security and durability gates

**Primary repository:** sdk-ts  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** audit / P0 / DONE — .github bea437a: release/mvp-0.2-client-baseline.md; rc9 sdk-ts gate PASS at 777f36e, full suite PASS at e9cdb43; no defect opened.  
**Depends on:** LFCP-02-001  
**Read first:** MVP-0.1-PROTOCOL-SCOPE.md; LFCP-WIRE-01.md; LFCP-TEST-VECTORS-01.md; AGENT-OPERATING-GUIDE.md; .github: docs/release/mvp-0.1-release-notes.md; .github: docs/release/security-review-mvp-0.1.md  
**Gate / test trace:** G01 / T01

**Goal:** Identify actual 0.1 client gaps before section integration.

**Acceptance:**

1. Run the existing secure Task and Wire checks for signatures, AEAD, keys, control, capabilities, epoch cutoff, snapshots and actor persistence.
2. Report exact commands/builds and classify PASS/FAIL/NOT_RUN independently from historical issue status.
3. Create precise owning-layer defect records for failures; do not replace crypto with mocks to pass the baseline.
4. Read the release notes for the H1/H7/M1 SDK alignment: the security-review summary table still says "pending" although sdk-ts 68ce58d/af6e6f1 and sdk-rs 50cb6bf shipped it.

**Required checks:** Existing Wire vectors and secure Task integration on isolated state.

**Deliverables:** Client baseline evidence and linked remediation requirements.

### LFCP-02-003 — Audit server ACK, persistence and configured limits

**Primary repository:** server  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** audit / P0 / DONE — server ad84496.  
**Depends on:** LFCP-02-001  
**Read first:** LFCP-WIRE-01.md; MVP-0.1-PROTOCOL-SCOPE.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G01 / T01

**Goal:** Determine which server facts the SDK/UI can honestly expose.

**Acceptance:**

1. Identify exact ACK/NACK and holdings/catch-up semantics and whether acceptance guarantees persistence.
2. Record object/frame/storage limits and restart/backup behavior on the actual build; there is no server profile allowlist to audit (the server is profile-agnostic).
3. Give a version-pinned evidence mapping; if evidence is insufficient, require an unknown-confirmation UI state rather than inventing a message.
4. Established facts: ACK carries durable: true at durability 2, the SDK emits an ack event, and itemId = hash32(unitId); the remaining work is batch-to-unit mapping and its persistence.

**Required checks:** Isolated ingest/restart/lost-ACK probes and configuration inspection.

**Deliverables:** Server semantics/limits report and narrow defect list.

### LFCP-02-004 — Audit legacy client and unknown-profile behavior

**Primary repository:** obsidian  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** audit / P0 / DONE — obsidian a2f48de; the fix (087) ships in 0.3.2.  
**Depends on:** LFCP-02-001  
**Read first:** MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; MARKDOWN-REFS-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G01, G11 / T08

**Goal:** Verify upgrade assumptions against the actual supported legacy build.

**Acceptance:**

1. Test legacy Tasks, new-profile encounter, stored refs and local storage-version rejection on pinned old artifacts.
2. Identify unsafe profile mutation or unsupported downgrade behavior and prescribe a compatibility patch or explicit minimum-version requirement.
3. Do not claim safe rejection solely because the compatibility specification requires it.
4. Known fact: 0.3.1 spends the one-time claim before checking the profile and would open another profile as Shared Objects; the output is a link to 086/087, verified on the 0.3.1 artifact.

**Required checks:** Isolated old/candidate fixture vaults; preserve source and compare attempted outbound writes.

**Deliverables:** Legacy compatibility report and required remediation links.

### LFCP-02-005 — Pin editor environments and qualification budgets

**Primary repository:** obsidian  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** qualification / P0 / DONE — obsidian 03c4aff.  
**Depends on:** LFCP-02-001  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md  
**Gate / test trace:** G01, G12 / T05, T11, T12

**Goal:** Make host/platform and performance acceptance reproducible.

**Acceptance:**

1. Record actual macOS, Windows and Linux host/hardware/Obsidian/Tasks/toolchain builds and required editor modes.
2. Review and freeze proposed performance/pilot targets with named owners; record changes without pretending measurements exist.
3. Identify inherited platform claims that require additional regression coverage and configure isolated fixture vaults.
4. Measure 0.3.1 baselines: share of 200 Tasks, save-to-render path and plugin start.
5. Record in Obsidian 1.13.1: the default of "Indent using tabs", HTML comment visibility in Live Preview and heading drag in Outline; record the Tasks plugin version.
6. Platform matrix per V4: native on macOS, the CI harness (096) on three systems, manual smoke on Windows and Linux; p95 budgets on macOS only, Windows/Linux claimed "functional, not performance-qualified".

**Required checks:** Build/install smoke on the recorded environments; instrumentation availability check.

**Deliverables:** Environment matrix, reviewed budgets and native test entry points.

### LFCP-02-006 — Publish baseline gaps and integration entry conditions

**Primary repository:** .github  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** contract / P0 / DONE — .github 0c40604: release/mvp-0.2-baseline-gaps.md, gaps B1-B19 and the blocking predicates.  
**Depends on:** LFCP-02-002, LFCP-02-003, LFCP-02-004, LFCP-02-005  
**Read first:** AGENT-OPERATING-GUIDE.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.1-PROTOCOL-SCOPE.md  
**Gate / test trace:** G01 / T01

**Goal:** Separate completed audits from unresolved baseline defects.

**Acceptance:**

1. Link every missing inherited requirement to a named owning repository and executable acceptance condition.
2. Append implementation/remediation tasks for real gaps; retain their IDs and required gate links instead of silently broadening existing tasks.
3. Define blocking issue predicates for secure integration and release; audit completion must not clear open safety/security gaps.

**Required checks:** Review baseline coverage and unresolved issues against G01 and the inherited 0.1 completion gate.

**Deliverables:** Baseline decision record and blocker register; existing code is not presumed broken.

### LFCP-02-101 — Import the MVP 0.2 documents into the public repositories

**Primary repository:** .github  
**Milestone / group:** M02-0 / RP00  
**Type / priority / status:** contract / P0 / DONE — .github b92fe19, 63b8454: the scope, roadmap, test plan, backlog and execution map published.  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); AGENT-OPERATING-GUIDE.md  
**Gate / test trace:** G01 / T12

**Goal:** Make the approved plan readable where the code is (V6).

**Acceptance:**

1. SCOPE, ROADMAP, BACKLOG (this revision) and TEST-AND-RELEASE-PLAN go to .github/docs/ like BACKLOG-MVP-0.1; specification drafts go to spec.
2. AGENT-OPERATING-GUIDE §4.6 points to the 0.2 backlog; NAVIGATOR rows; doccheck passes.
3. Agent prompts, the narrative and review reports stay private.

**Required checks:** doccheck across the repositories.

**Deliverables:** Docs commits in .github and spec.

## E02. Pinned contracts and corpus

### LFCP-02-007 — Pin section specifications and compatibility authority

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec 0a17f17, d72ff2b, 3a13ba2, 2d1a829, 0927440 (SSP WD 0.3, MARKDOWN-SECTIONS-01, ADR 0009).  
**Depends on:** LFCP-02-006, LFCP-02-083, LFCP-02-084  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; MARKDOWN-SECTIONS-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md  
**Gate / test trace:** G02 / T02, T04

**Goal:** Provide one reviewed contract revision for model and editor work.

**Acceptance:**

1. Pin profile, Task contract, Markdown grammar, scope, compatibility and Obsidian companions by revision/hash.
2. Preserve new/legacy profile separation, canonical refs, explicit import and fresh lifecycle intent semantics.
3. Resolve normative contradictions in canonical Working Drafts with corresponding fixture changes; do not create competing errata.
4. Pins start from mvp-0.1-baseline.8 (.9 after W0), not the batch spec-baseline snapshot (spec 8f1cc79).
5. Import SHARED-OBJECTS-PROFILE-01 §§7-18 and §74.1 admission rules; a portable diagnostics registry; ImmutableString; the #section: and whitespace rule.
6. Fix the Markdown decisions M1-M7: child-line refs inside sections as for standalone Tasks, Enter handled through CodeMirror transactions (M1 as revised, obsidian ADR 0001); tabs as in 0.1; start marker right after the heading; a marker on every node hidden in Live Preview by default; tables/callouts/fences/blockquotes as raw blocks and no nested headings in 0.2; Tasks-local tokens stay local.

**Required checks:** Cross-document review; all resolved differences link to updated regression cases.

**Deliverables:** Pinned integration specification baseline.

### LFCP-02-008 — Integrate reproducible corpus and conformance entry points

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec 0927440: test-vectors/shared-sections-01 with its generator, checked in spec CI.  
**Depends on:** LFCP-02-007  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; MARKDOWN-SECTIONS-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md  
**Gate / test trace:** G02 / T02, T04

**Goal:** Make the published reference data a stable test dependency.

**Acceptance:**

1. Import both JSON suites, schemas, hashes, source pins, generators and lockfile using existing repository conventions.
2. Run deterministic regeneration and integrity/schema checks without changing expected data to match an implementation.
3. Document exact-byte versus logical comparisons and the limits of the shared reference inspector.
4. Layout test-vectors/shared-sections-01/; the generator runs on Automerge 3.5.0 (P6) and records the engine version from the package; CI in spec/.github/workflows/ci.yml; a new baseline document (P4).

**Required checks:** Published reference validation/reproducibility commands; clean checkout repeat.

**Deliverables:** Versioned corpus with CI and adapter instructions.

### LFCP-02-009 — Freeze SDK receipt/status and parser integration contracts

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec b184dda: integration/SDK-SECTIONS-INTEGRATION-01.md (sections-integration/1: commit and Receipt, receiptOf, batch statuses, events, canWrite, the local codes).  
**Depends on:** LFCP-02-003, LFCP-02-007, LFCP-02-088  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MARKDOWN-SECTIONS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G02, G07, G10 / T07, T09

**Goal:** Prevent editor code from inventing durable or synchronization evidence.

**Acceptance:**

1. Define durable intent/commit correlation, batch-to-unit/node attribution, access/control freshness and event-gap recovery interfaces.
2. Define parser/source-map/base/candidate/patch boundaries without assuming conceptual type names are existing SDK APIs.
3. Assign unknown/unsupported evidence behavior and minimal version requirements; no new Wire ACK is introduced.
4. Established facts: ACK carries durable: true at durability 2, the SDK emits an ack event, and itemId = hash32(unitId); the remaining work is batch-to-unit mapping and its persistence.

**Required checks:** Provider/consumer contract examples for crash ambiguity, lost ACK, stale revision and partial batch acceptance.

**Deliverables:** Reviewed integration interfaces and provider/consumer versioning plan.

### LFCP-02-010 — Expand missing semantic and Markdown edge fixtures

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec 33c4544: SHARED-SECTIONS-TEST-VECTORS-01 with 56 cases (admission A1-A5 and SOP negatives, ready and import, isolation, collisions, split/join, budgets, Text history at the Snapshot floor) and 47 Markdown fixtures; both SDKs pin it in spec-sections.lock (sdk-ts b81066b, sdk-rs f5407a4).  
**Depends on:** LFCP-02-007, LFCP-02-008  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; MARKDOWN-SECTIONS-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md  
**Gate / test trace:** G02 / T02, T04

**Goal:** Cover known gaps before dependent implementations choose their own policy.

**Acceptance:**

1. Add concurrent split/join, malicious map/history mutations, depth/limit overflow and transient edit/recovery cases missing from the current corpus.
2. Keep 28 existing SS and 29 existing Markdown fixture identities stable; give additions new IDs with explicit authority/rationale.
3. Define expected preserved private text, retained content and semantic intents for every new boundary/identity case.
4. Admission negatives: a change above §11.1, depth, a compressed chunk, a bad checksum, an actor mismatch and a sequence gap; subtree isolation cases (P2); multi-change import and an insert above 16,384 characters (P3); Text history at the snapshot floor. Rewrite SS13/19/20/21 expectations after P2 with a written rationale, never as a silent regeneration.
5. Markdown fixtures: Enter after a Task with a child-line ref, tabs and mixed indentation, a line without a marker under a Task, fold, heading embed and Outline drag, Tasks completing a recurring Task inside a section, %%…%% context, and Detach inside a section.

**Required checks:** Generator/schema checks and human review of new expected values; implementation validation follows separately.

**Deliverables:** Additional fixtures and traceable specification clarifications.

### LFCP-02-083 — ADR 0009: shared sections profile

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec eb054d6: ADR 0009 accepted.  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G02 / T02

**Goal:** Record the owner-approved profile decisions before the contracts are pinned.

**Acceptance:**

1. ADR 0009 records P1 (a new profile org.openlfcp.shared-sections.v1, one Resource per section; legacy clients do not see sections; migration only by explicit copy), P2 (admission rejects violations visible in the change itself; other invalid history is isolated per subtree, not the whole section), P3 (multi-change import with a readiness marker and split long Text inserts; the 0.1 admission limits stay) and P5 (two moves into one parent remain a conflict; revisit after the pilot).
2. NEXT-001 in .github: docs/BACKLOG-MVP-0.1.md is closed with a link to ADR 0009 and the reason the in-profile list design was not taken.
3. The owner approval is recorded in the ADR (Status: Accepted, with date), as for ADRs 0001-0007.

**Required checks:** ADR review against SHARED-OBJECTS-PROFILE-01 §114-§115 and the batch profile; doccheck on spec and .github.

**Deliverables:** spec: adr/0009-shared-sections-profile.md; the NEXT-001 update.

### LFCP-02-084 — Normative multi-change import and exact profile admission limits

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P0 / DONE — spec f595dd4: import in several changes under the 0.1 limits, the authoring budgets.  
**Depends on:** LFCP-02-083  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; LFCP-WIRE-01.md  
**Gate / test trace:** G02, G04, G07 / T02

**Goal:** Make a 100-200 Task import and long Text edits fit the unchanged 0.1 admission limits.

**Acceptance:**

1. SHARED-SECTIONS-PROFILE-01 specifies import and creation as several changes with a readiness marker; a reader never shows a partially imported section as complete.
2. Long Text inserts are split into changes within §11.1; the split rule is normative so both SDKs author compatible histories.
3. Exact admission limits of the profile are stated and shared with the 0.1 limits (§11.1, §11.2, §30, §31); none is raised.

**Required checks:** Worked examples at the limit and one above it; vectors added through task 010.

**Deliverables:** Profile text and the limit table, with the cases handed to 010.

### LFCP-02-090 — Tag mvp-0.2-baseline.N and move consumer spec.lock pins

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** release / P0 / DONE — For N=2: spec tag mvp-0.2-baseline.2 (4198c43); spec.lock moved: sdk-rs c05309b, server 7f7eb99, sdk-ts b92f701, obsidian 6b1aa45; examples pins b4cbc61; .github c5e491a (compatibility matrix). rc-verify --from-heads --consistency-only (2026-10-09, report 20261009T051056Z): pins consistent at mvp-0.2-baseline.2; spec 4aa9491 awaits baseline.3. The card repeats for N=3 (spec 8076d89 prepared).  
**Depends on:** LFCP-02-007, LFCP-02-008, LFCP-02-010, LFCP-02-084  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/rc-verification.md; SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G02 / T02

**Goal:** Give implementations one immutable contract revision.

**Acceptance:**

1. Tag mvp-0.2-baseline.N from the W0 baseline (.9) plus the section files, with MVP-0.1-BASELINE-style change log and migrations listing.
2. spec.lock moves in sdk-ts, sdk-rs, server and obsidian in the same change as the code that needs it.
3. rc-verify consistency passes with the new tag pattern (102).

**Required checks:** spec gate (validate.sh, CDDL) at the tag; rc-verify --consistency-only.

**Deliverables:** Tag (owner), baseline document and lock commits.

### LFCP-02-107 — Move the shared-sections vectors to lfcp-vector-format/1

**Primary repository:** spec  
**Milestone / group:** M02-1 / RP01  
**Type / priority / status:** contract / P1 / DONE — spec f5e5bb0: the sections corpus in lfcp-vector-format/1; both SDKs read it (sdk-ts a4bdb03, sdk-rs 723fd4d).  
**Depends on:** LFCP-02-010  
**Read first:** SHARED-SECTIONS-TEST-VECTORS-01.md; SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G02 / T02

**Goal:** Check the section corpus with the project's one vector tooling.

**Acceptance:**

1. test-vectors/shared-sections-01 (SHARED-SECTIONS-TEST-VECTORS-01) is expressed in lfcp-vector-format/1 instead of its own schema (schemas/section-vectors.schema.json).
2. scripts/validate-vectors.mjs checks the directory: it is removed from OWN_FORMAT, and scripts/check-shared-sections-corpus.mjs is retired or reduced to what the format cannot say.
3. No expected value changes without an entry in migrations/; the case identities and hashes of task 010 are kept.

**Required checks:** spec validate.sh on a fresh clone; both SDK conformance runners read the moved corpus.

**Deliverables:** Moved corpus, schema and validator changes, migrations entry.

### LFCP-02-108 — A6: refuse a non-concurrent ID reuse across categories at admission

**Primary repository:** spec (companions: sdk-ts, sdk-rs)  
**Milestone / group:** M02-6 / RP01  
**Type / priority / status:** contract / P2 / NOT_STARTED — Candidate, after G02; decision after the pilot. Readers do not check cross-category reuse in v1 (sdk-ts 4dcb56b, sdk-rs 1b55b6e).  
**Depends on:** LFCP-02-024, LFCP-02-075  
**Read first:** SHARED-SECTIONS-TEST-VECTORS-01.md; SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G12 / T02

**Goal:** Close the writer-only rule of SHARED-SECTIONS-PROFILE-01 §3 without giving any writer a way to take out another's content.

**Acceptance:**

1. Candidate rule A6 in §14.1: a change that creates a node, placement or object under an ID its causal history already uses in another category (a node ID equal to a PlacementId or the SectionId, say; a Task node and its Task excepted) is refused at admission, decided from the change and its history like A1-A5.
2. Readers keep not isolating cross-category reuse (§14.2, the v1 decision): concurrent reuse stays undetected by A6 and is left to the writer rule of §3.
3. Vectors in test-vectors/shared-sections-01; sdk-ts and sdk-rs refuse the same changes with the same diagnostic.
4. Decided after the pilot (075): adopt, defer or drop, recorded in ADR 0009 or a successor.

**Required checks:** Corpus cases for reuse of each category pair, refused, and concurrent reuse accepted; both SDK conformance runs.

**Deliverables:** Profile text, vectors and both SDK admissions, if adopted.

## E03. TypeScript section model

### LFCP-02-011 — Add TypeScript section profile dispatch and schema

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts c6b4f34, d6fc6d3, 4dcb56b: @openlfcp/shared-objects/sections, dispatch by Genesis profile, the section actor, schema validation (§3, §4, §14.2). Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-007, LFCP-02-008, LFCP-02-085, LFCP-02-090  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Load/create the new profile without mutating legacy Resources.

**Acceptance:**

1. Dispatch from validated Genesis profile; enforce canonical IDs, root/schema types and section actor derivation.
2. Represent Task strings as scalar values and paragraph/item bodies as Text; preserve unknown extensions.
3. Unknown profiles produce an explicit non-mutating result; standalone Task refs select their Resource model.

**Required checks:** SS01, SS18, scalar/type/actor negatives and legacy dispatch regression.

**Deliverables:** Profile module, schema validation entry and tests.

### LFCP-02-012 — Implement section and Task/node creation intents

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 9aee4cb, a1b0556: SectionReplica and the section and creation intents; SS01 authored reaches the reference state. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-011, LFCP-02-084  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Create nested content with a single authority for Task fields.

**Acceptance:**

1. Create section/title, Tasks, ordinary items and paragraphs through validated intents with stable identities.
2. Task node ID equals Task ID; initial node and placement creation is atomic and metadata is excluded from content.
3. Unrepresented Task fields/extensions survive unrelated edits; retries accept retained allocated IDs through the integration contract.
4. Several intents of one reconcile batch commit as one unit.

**Required checks:** Creation/nesting/field-edit cases including SS01, SS03 and SS11.

**Deliverables:** Creation/field intent API and semantic tests.

### LFCP-02-013 — Implement immutable placement insertion and moves

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 6cc0e22: node.move through fresh placements; SS02 and SS09 authored reach the reference state. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-012  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Preserve node identity and invisible ordering anchors when moving.

**Acceptance:**

1. Moves create fresh immutable slots and update placement registers; old slots remain insert-only anchors.
2. Reorder/reparent preserves descendants and Task authority; reject duplicate slot insertion and illegal slot mutation.
3. Sibling sequence order converges without using wall-clock or UUID time as conflict precedence.

**Required checks:** SS02, SS09, SS13, SS19 and SS21; repeated sibling and subtree moves.

**Deliverables:** Placement intent API and invariant tests.

### LFCP-02-014 — Derive effective tree and structural conflict facts

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts fd4a7fe, 5862560: the effective tree, structural facts and resolution intents; SS15 and SS26 authored. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-013  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Expose ambiguity without choosing a destructive hidden winner.

**Acceptance:**

1. Inspect all concurrent placement assignments, including same-parent moves; detect strongly connected parent cycles.
2. Propagate blocked structure to dependent descendants while retaining all model content and alternatives.
3. Expose deterministic resolution inputs and recovery facts; invalid or blocked nodes are never silently treated as deleted.

**Required checks:** SS04, SS05, SS15, SS22 and SS26; iterative/depth-limit adversarial graphs.

**Deliverables:** Tree derivation, conflict facts and resolution intents.

### LFCP-02-015 — Implement lifecycle, ancestor hiding and restoration

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts fd41e16: node.delete and node.restore, hidden nodes and retained concurrent edits; SS07, SS08, SS24, SS25, SS27 authored. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-012, LFCP-02-014  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Delete/restore shared content without losing concurrent descendant work.

**Acceptance:**

1. Task deletion uses Task.lifecycle; paragraph/item deletion uses node.lifecycle; Task-node lifecycle stays active.
2. Ancestor deletion hides descendants without recursively tombstoning them; moved-out children and independently deleted descendants behave correctly.
3. Explicit restore/resolution creates a fresh causal write even when the visible value already matches; rendering emits no lifecycle writes.

**Required checks:** SS06–SS08, SS24, SS25 and SS27; deletion versus child edit/add/move-out.

**Deliverables:** Lifecycle/recovery intents and conflict tests.

### LFCP-02-016 — Implement collaborative Text and split/join operations

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 725a06c: text.edit with base rebasing, split and join; SS06, SS14, SS16, SS17, SS40, SS47-SS51 authored. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-012, LFCP-02-013, LFCP-02-015, LFCP-02-010  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Edit existing Text safely from versioned Unicode-scalar positions.

**Acceptance:**

1. Apply insert/delete to the existing Text object; scalar Task fields do not become Text.
2. Require a base revision and rebase/reject stale indices; preserve Cyrillic/emoji without normalization or surrogate corruption.
3. Implement specified split/join identity and retained-tombstone rules; uncertain concurrent transformations follow reviewed fixtures.

**Required checks:** SS14, SS16, SS17, SS20 and additions from task 010.

**Deliverables:** Text/structural transform APIs and Unicode/concurrency tests.

### LFCP-02-017 — Harden TypeScript profile validation

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts b97e166, 7e9f83f, e202a66, b1033e9: receiveChanges with the inherited and the section admission (§14.1); refused, held and heads match every corpus case. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-010, LFCP-02-014, LFCP-02-015, LFCP-02-016  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Separate valid CRDT bytes from valid LFCP section history.

**Acceptance:**

1. Enforce full schema, authorship/identity, immutable placement history, unique slots and allowed node/Task relations.
2. Diagnose malformed/missing dependencies and unsafe conflicting values without deleting source/received evidence.
3. Implement documented safe depth/size handling and preserved unknown extension behavior; reference inspector coverage is not treated as exhaustive.
4. Admission checks the operations of the change itself; the model checks the merged graph; comparisons use the portable diagnostics, not message strings.

**Required checks:** Negative corpus, targeted malicious histories and limit overflow; verify no application of rejected semantic state.

**Deliverables:** Production validator and negative/regression tests.

### LFCP-02-018 — Run production TypeScript conformance adapter

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** integration / P0 / DONE — sdk-ts 4b217eb, f9df270: the corpus adapter; the reference verifier with the sdk-ts adapter passes 56/56 at mvp-0.2-baseline.1; three deliveries in sdk-ts. Evidence: .github b59bb1b.  
**Depends on:** LFCP-02-008, LFCP-02-017  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G04, G05, G06 / T02

**Goal:** Prove the actual SDK consumes the full reference suite.

**Acceptance:**

1. Connect production model/validator to the independent-adapter interface without reading expected results as implementation inputs.
2. Pass all 28 existing cases and approved additions, including snapshot/tail, reversed delivery and duplicates.
3. Compare logical states/conflicts/retained work separately from normative byte/identity hashes; rerun legacy Task regression.

**Required checks:** SS01–SS28 plus additions on exact project pins; save report and build hashes.

**Deliverables:** SDK adapter and version-pinned conformance evidence.

### LFCP-02-085 — Shared 0.1 admission module for both profiles

**Primary repository:** sdk-ts (companion: sdk-rs, by another worker)  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — TS: sdk-ts 5b409f0, @openlfcp/shared-objects/admission (framing, limits, actor binding, sequence admission). Rust: sdk-rs 01f536f, the section profile reuses the shared_objects admission engine as is (SharedObjects::apply_change) with the section actor domain and A1-A5 on top; no separate public module.  
**Depends on:** LFCP-02-007  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-PROFILE-01.md; LFCP-WIRE-01.md  
**Gate / test trace:** G02, G07, G08 / T02, T03

**Goal:** Apply the 0.1 admission rules to section changes without copying code between profiles.

**Acceptance:**

1. sdk-ts: chunk limits, Automerge byte checks, actor binding and the sequence check move into a module both profile handlers call; Shared Objects behaviour and its vectors are unchanged.
2. sdk-rs: the same for expansion, depth and framing, written independently by the Rust worker (TS/Rust independence).
3. Each SDK runs the 0.1 vector suites unchanged and the admission negatives of task 010 for both profiles.

**Required checks:** Shared Objects conformance suites and admission negatives in both SDKs; no change to expected values.

**Deliverables:** Admission modules and tests in both SDKs; a note of the shared surface.

### LFCP-02-114 — SPEC-PATCH-10 admission in sdk-ts (F2-F4)

**Primary repository:** sdk-ts  
**Milestone / group:** M02-1 / RP02  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 8ef791e (§11.3), 62e2efd (§11.4), f2b526d; sdk-rs d2a2b77, pinned at c05309b. CAN-*/REF-* 36/36 and SS57-SS59 12/12 at the baseline.2 pins (.github 3c045fd).  
**Depends on:** LFCP-02-090  
**Read first:** SHARED-OBJECTS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md  
**Gate / test trace:** G02, G06 / T02

**Goal:** Refuse non-canonical changes and changes that refer outside their history in the TypeScript admission, as sdk-rs does.

**Acceptance:**

1. SHARED-OBJECTS-PROFILE-01 §11.3 (C1-C9) and §11.4 (R1-R7) at the Shared Objects and section admission, before the engine; a refused change leaves a document that saves and loads.
2. The corpus sections canonical and references and SS57-SS59 pass; conformance/shared-objects/admission-pending.json and conformance/shared-sections/pending.json become empty.
3. Written from the specification and the corpus, without reading sdk-rs (the independence rule).

**Required checks:** The corpus at mvp-0.2-baseline.2 or later through the sdk-ts conformance run.

**Deliverables:** The sdk-ts admission change and its tests.

## E04. Rust and independent interoperability

### LFCP-02-019 — Implement independent Rust schema and actor dispatch

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** implementation / P0 / DONE — sdk-rs f8b0204: the section schema and actor dispatch.  
**Depends on:** LFCP-02-007, LFCP-02-008, LFCP-02-085, LFCP-02-090  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Load/create section-profile state using the actual Rust binding.

**Acceptance:**

1. Use the same canonical IDs, profile actor domain and scalar-versus-Text distinctions as the pinned contract.
2. Preserve legacy dispatch and extensions without routing the implementation through JavaScript.
3. Decode supplied change/save bytes and distinguish unsupported profile from profile-invalid history.
4. Sources are only SHARED-SECTIONS-PROFILE-01 and the JSON corpus; no TypeScript code is read (independence).

**Required checks:** SS01, SS18 and malformed/type/actor cases on pinned Rust dependencies.

**Deliverables:** Rust profile schema/dispatch module and tests.

### LFCP-02-020 — Implement Rust node, placement and tree behavior

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** implementation / P0 / DONE — sdk-rs 1c76ebb, 208f66e: the effective tree, structural facts, nodes, moves and placement resolution.  
**Depends on:** LFCP-02-019  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Author nested content and moves with independent tree/conflict derivation.

**Acceptance:**

1. Create/rename Task and non-Task nodes through the normative model and preserve immutable slot history.
2. Author reorder/reparent operations without ID recreation; inspect concurrent location alternatives.
3. Detect cycles/blocked descendants and expose explicit resolution with no arbitrary winner.

**Required checks:** Sibling insert, repeated move, same/different-parent conflict and cycle cases authored in Rust.

**Deliverables:** Rust intent/tree implementation with authoring fixtures.

### LFCP-02-021 — Implement Rust lifecycle and collaborative Text

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** implementation / P0 / DONE — sdk-rs ff3ed0f, 1ea55d9: lifecycle and collaborative Text.  
**Depends on:** LFCP-02-010, LFCP-02-020  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Provide independent deletion/restore and Unicode Text authoring.

**Acceptance:**

1. Implement ancestor hiding, moved-out children, retained edits and independent child deletion under restored parents.
2. Produce fresh explicit lifecycle assignments and causal conflict resolution even for same visible values.
3. Edit/split/join Text according to the pinned index/base and identity rules; no whole-Text replacement.
4. Check that automerge 0.12 does not suppress a same-value write that the explicit lifecycle intent requires.

**Required checks:** Rust-authored delete/edit/restore, split/join and Cyrillic/emoji cases.

**Deliverables:** Rust lifecycle/Text APIs and tests.

### LFCP-02-022 — Validate Rust history and consume the full corpus

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** integration / P0 / DONE — sdk-rs 01f536f, 7e24a3a, 1b55b6e, b345fbc, f5407a4: admission, collisions and the full corpus at spec 33c4544.  
**Depends on:** LFCP-02-008, LFCP-02-021  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Verify the independent production implementation against positive and invalid histories.

**Acceptance:**

1. Enforce full profile/history constraints and non-destructive invalid/over-limit handling.
2. Consume all 28 existing binary cases and approved additions, snapshots/tails and sequence continuation.
3. Keep implementation error strings out of the portable comparison contract; preserve extensions and retained hidden state.
4. Admission checks the operations of the change itself; the model checks the merged graph; comparisons use the portable diagnostics, not message strings.

**Required checks:** SS01–SS28 plus task 010 additions and legacy Rust regression.

**Deliverables:** Rust conformance runner/report.

### LFCP-02-023 — Build bidirectional TS/Rust exchange harness

**Primary repository:** examples  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** integration / P0 / DONE — Rust: sdk-rs a64c59b, examples 7fb6a37; TypeScript: examples conformance/src/sections-ts.ts (bd); all four directions pass (examples 558b555).  
**Depends on:** LFCP-02-018, LFCP-02-022  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Prove both implementations author changes the other consumes.

**Acceptance:**

1. Run TS→Rust and Rust→TS authored scenarios, concurrent branches, snapshots and post-snapshot actor continuation.
2. Compare full logical state, identity, order, conflict alternatives and hidden content, not only visible winner values.
3. Use independently authored output and actual exchanged bytes; no private expected-state input into either implementation.

**Required checks:** All authored scenario families in test-plan section 5; exact component/toolchain pins.

**Deliverables:** Reproducible interop harness and per-direction reports.

### LFCP-02-024 — Add deterministic concurrency schedules and minimized regressions

**Primary repository:** examples  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** qualification / P0 / DONE — sdk-rs 9c6e639, b86c204; examples bd63f7b, 558b555, 167fe51, 664f277: 100 seeds in all four directions; seed 2 found the lifecycle-conflict difference, fixed in sdk-ts f408430 and specified in spec 4aa9491 (SS60).  
**Depends on:** LFCP-02-010, LFCP-02-023  
**Read first:** SHARED-SECTIONS-PROFILE-01.md; SHARED-SECTIONS-TEST-VECTORS-01.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G02, G05, G06 / T03

**Goal:** Broaden merge/race coverage beyond hand-picked examples.

**Acceptance:**

1. Run the initial 100 recorded seeds for three actors, partitions, duplicate delivery and reorder using valid intents.
2. Assert convergence only after identical valid history; preserve meaningful conflicts and retained work.
3. Minimize every failure into a deterministic fixture; invalid-history tests remain separate from valid-intent generation.

**Required checks:** Seeded runs on both SDKs and replay of minimized failures; no byte-equality demand for different histories.

**Deliverables:** Schedule generator, reproducible reports and regression fixtures.

### LFCP-02-109 — Linear-time retained concurrent edits in the Rust section model

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** implementation / P2 / DONE — sdk-rs b6e873b, b9de91c: retained edits from the changed nodes only; Automerge optimized in debug builds.  
**Depends on:** LFCP-02-010  
**Read first:** SHARED-SECTIONS-TEST-VECTORS-01.md; SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G05 / T03

**Goal:** Keep long Text histories fast in the Rust model, as the Snapshot-floor cases need.

**Acceptance:**

1. SectionsDoc::retained_concurrent_edits no longer replays the history one change at a time reading a state snapshot at each step (quadratic on SS55/SS56); it walks the history once, or reuses the running document as the linear-history path of b345fbc does.
2. Its results are unchanged on every case of SHARED-SECTIONS-TEST-VECTORS-01.
3. The Rust corpus run in debug takes well under the current six minutes; the time before and after is recorded.

**Required checks:** The Rust corpus conformance run before and after, with timings; the full sdk-rs gate.

**Deliverables:** The sdk-rs change and its timings.

### LFCP-02-111 — Linear-time section admission and authoring in the Rust model

**Primary repository:** sdk-rs  
**Milestone / group:** M02-1 / RP03  
**Type / priority / status:** implementation / P1 / DONE — sdk-rs abff1b1, 6255f2c; .github 50150b6 (W200 admission 40.3 s to 0.43 s; typing catch-up within 6% of the engine).  
**Depends on:** LFCP-02-109  
**Read first:** SHARED-SECTIONS-TEST-VECTORS-01.md; SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G05 / T03

**Goal:** Import a W200 section and catch up on many units in time linear in what each change touches.

**Acceptance:**

1. The structural rules (§14.1) are decided from the entities a change writes into, not from every node; create_node decides visibility along one node's ancestors; text_edit skips the stale-base comparison at the current heads.
2. Nothing admitted changes: the corpus replays as before and an old-versus-new differential agrees on corpus, schedule and mutant inputs.
3. Before and after timings recorded (LFCP-02-067 report).

**Required checks:** The corpus and the differential; section_scale before and after.

**Deliverables:** The sdk-rs change, the example timings and the report section.

## E05. Durability and SDK evidence

### LFCP-02-025 — Add durable intent-to-commit receipt correlation

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts commit facade with receipts; typing coalescing fa77ba4.  
**Depends on:** LFCP-02-009, LFCP-02-012, LFCP-02-089  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G07 / T07

**Goal:** Make retries recoverable across model, actor and queue commit boundaries.

**Acceptance:**

1. Persist stable intent identity, allocated IDs and receipt with recoverable model/actor/outbound state.
2. After uncertain completion, recover the existing receipt or safe uncommitted state before retrying; no in-memory-only deduplication.
3. Expose the audited durability guarantee to consumers without claiming atomicity with Markdown files.
4. One reconcile batch is one unit; coalescing of Text edits into changes and a Data Unit budget per typing burst.

**Required checks:** Crash before/after commit and ambiguous returned result; same intended update never creates duplicate nodes.

**Deliverables:** Durable receipt integration and fault tests.

### LFCP-02-026 — Persist outbound batches and honest status attribution

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 50b865d (batch status, events, statusSnapshot), bafcf91.  
**Depends on:** LFCP-02-003, LFCP-02-009, LFCP-02-025  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G07, G10 / T07, T09

**Goal:** Track user-update batches independently from wire retries.

**Acceptance:**

1. Persist batch-to-unit and affected-node mappings through restart and coalescing.
2. Count a batch pending until all required units have real acceptance evidence; lost ACK and duplicate ACK are idempotent.
3. Expose queued/sending/accepted/rejected/evidence-unavailable facts and event-gap resynchronization; no socket-send success shortcut.
4. Batch-to-unit mapping uses the established ack event and itemId = hash32(unitId).

**Required checks:** SI04, SI05, SI10, SI11, SI19 and delayed-ACK/new-edit races.

**Deliverables:** Queue attribution/status facts and restart tests.

### LFCP-02-027 — Expose validated access and control freshness

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 9748d21 (canWrite), 35bf6fb (accessState), 05bb014 (CM12).  
**Depends on:** LFCP-02-009, LFCP-02-011  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G09, G10 / T08, T09

**Goal:** Give the UI operational identities and effective capabilities from validated state.

**Acceptance:**

1. Compute effective access across grant paths; invitations and pending control operations remain separate from active access.
2. Expose known control head, verification freshness, read-only/revoked/key-unavailable/unknown states.
3. Retain rejected offline work and enforce epoch/cutoff authorization independently of the server.

**Required checks:** SI14, SI15, SI18, CM12, stale control view and remaining-grant cases.

**Deliverables:** Access/control evidence API and integration tests.

### LFCP-02-028 — Integrate snapshots and safe restart continuation

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts a345b85, 6677e00, db52b9c, 5273916: section Snapshots, catch-up, restart, no new section over an incomplete load.  
**Depends on:** LFCP-02-025, LFCP-02-026, LFCP-02-012  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G07 / T07

**Goal:** Load section checkpoints and catch up without losing queue or actor safety.

**Acceptance:**

1. Apply profile state through the secure snapshot path and continue with exact post-frontier units.
2. Retain pending local updates during restore/catch-up; incomplete state never becomes an empty writable section.
3. Continue actor sequences safely and publish current-at-checkpoint facts only after required catch-up/model state is complete.

**Required checks:** SS12, SS28, incomplete tail, duplicate units and restart with pending work.

**Deliverables:** Section snapshot/restart integration and evidence.

### LFCP-02-029 — Upgrade local SDK storage alongside legacy Resources

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts dac706f, a388eb8: IndexedDB version 2, the 0.1.3 storage upgrade.  
**Depends on:** LFCP-02-025, LFCP-02-027, LFCP-02-028  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G07, G11 / T08

**Goal:** Add section records without resetting existing keys or pending data.

**Acceptance:**

1. Use a versioned upgrade journal and explicit unsupported-version handling.
2. Preserve legacy actors, secrets/references, exact queued units and profile dispatch; no implicit Resource conversion.
3. Resume interrupted upgrades safely and refuse unsupported old-writer access to newer storage.

**Required checks:** CM01, CM02, CM10 with pending legacy/section work and crash injection.

**Deliverables:** Storage upgrade adapter, compatibility notes and tests.

### LFCP-02-030 — Qualify SDK failure and status recovery

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** qualification / P0 / DONE — sdk-ts 194f662, f3102ff; .github aeb4706 (docs/devel/reports/sdk-fault-qualification.md).  
**Depends on:** LFCP-02-026, LFCP-02-027, LFCP-02-028, LFCP-02-029, LFCP-02-089  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SYNC-INDICATORS-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md  
**Gate / test trace:** G07, G09, G10 / T07, T09

**Goal:** Prove the production persistence/status contract under faults.

**Acceptance:**

1. Inject disk-full, unavailable key store, process death and lost delivery/ACK at specified durable boundaries.
2. No failed commit is labeled locally durable; no queue/identity reset is used as repair.
3. Correlate recovery state with stable batch/receipt IDs and expose recoverable rejection/candidate information.

**Required checks:** Test-plan section 8 SDK fault points, SI03, SI17 and legacy persistence regression.

**Deliverables:** SDK fault-injection suite and report.

### LFCP-02-097 — POST-007: the plugin publishes Snapshots

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — obsidian 817b02d, 6b35607; sdk-ts 775ef36 (committed units count toward the Snapshot policy).  
**Depends on:** LFCP-02-028  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/deferred-wire-01-features.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G07 / T06, T07

**Goal:** Let a joiner of a 200-Task section catch up from a Snapshot plus tail.

**Acceptance:**

1. The plugin publishes Snapshots through the SDK on a documented trigger, with the required writer capability.
2. A new joiner catches up from the plugin Snapshot in the two-vault E2E.
3. The deferred-features row is removed.

**Required checks:** Two-vault E2E with a Snapshot join.

**Deliverables:** Plugin change, E2E and docs.

### LFCP-02-098 — POST-006: local state encrypted at rest

**Primary repository:** sdk-ts  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts 09cbe18, 540b9cc, e713244, 28d6f4a, bf96725; obsidian 264e109, 2a72fc4, 97f661f; .github a0e8177, 4d69e14.  
**Depends on:** LFCP-02-029  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/security-review-mvp-0.1.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G08 / T10

**Goal:** Keep task text, journals and projection bases off disk in plaintext.

**Acceptance:**

1. Checkpoints, section journals, projection bases and candidates are encrypted with a device key from the secret store.
2. Existing plaintext checkpoints migrate; a lost device key means a resync, not a crash.
3. A test greps IndexedDB/SQLite files for task text and finds none.

**Required checks:** Storage tests in Node and IndexedDB adapters; migration test.

**Deliverables:** Encrypted storage and migration.

### LFCP-02-106 — A member refused before its grant is re-supplied recovers by itself

**Primary repository:** sdk-ts (companion: obsidian)  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P1 / DONE — sdk-ts 7d6b67f, 5e6c71e: access recovery after a server restore, with the live test against the Rust server.  
**Depends on:** LFCP-02-088  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); spec: adr/0008-recovery-after-server-data-loss.md; LFCP-WIRE-01.md; .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G07, G09 / T07, T08

**Goal:** After a server restore, a member whose grant the server lost reaches LIVE once the grant is re-supplied, without restarting.

**Acceptance:**

1. Today: a member that opens the Resource before a holder re-supplied the Control Records (§68.1) gets AUTHORIZATION_FAILED for RESOURCE_OPEN, which is final (POST-017), and stays CLOSED until the application opens it again or restarts.
2. Recover without a new attack surface: retry the open only when (a) the client's own validated chain grants it data/read at its head and (b) there is evidence that the server lost state (its Control Head is behind that chain, a re-host was seen, or a sibling route answered). The retry is bounded (a few attempts with backoff, then final) and per Resource; a Resource the local chain does not grant is never retried. Evaluate first whether the member can re-supply its own chain (CONTROL_PUT, §68.1, §84) instead of waiting for the owner.
3. Write the security rationale in the change: no brute-force path (the client learns nothing it does not already hold; retries count against the server's rate limits), and a revoked member stays refused (a revocation is on the chain it validates).
4. obsidian: the Resource shows "waiting for the server to recover access" while retrying, then the normal refusal if it stays refused.

**Required checks:** Live test against the Rust server: restore before the grant, member opens first, recovers once the owner re-supplies (the race of sdk-ts 1d00993, without the test reopening it); a revoked member is not retried; unit tests of the retry bounds.

**Deliverables:** SDK change with tests, the security rationale, plugin status text.

### LFCP-02-110 — Journal a capability claim before it is sent

**Primary repository:** sdk-ts (companion: obsidian)  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P1 / DONE — sdk-ts a44551b, 5c87f5d; obsidian b013e23, b8437c4 (resume and Retry/Give up).  
**Depends on:** LFCP-02-051  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); LFCP-WIRE-01.md  
**Gate / test trace:** G07, G09 / T07, T08

**Goal:** A one-time invitation whose CONTROL_PUT answer is lost is neither spent twice nor lost.

**Acceptance:**

1. Before every claim is sent, the claimant journals it (the claim record, the expected head, the validated chain to it, the epochs whose DEK it holds; the DEKs go to the SecretStore first, LFCP-034).
2. After a lost answer the same record is sent again; a coordinator answers a committed record with the same ACK (LFCP-WIRE-01 §47, §70), so the claim completes once.
3. A journaled claim is resumed after a restart without the link, refused when another claimant won, and can be abandoned.

**Required checks:** Unit tests with a fake coordinator; a live test against the Rust server losing the answer and the request.

**Deliverables:** The journal in @openlfcp/client and its tests; plugin resume UI (obsidian).

### LFCP-02-115 — A revoked member learns the refusal and reports it honestly

**Primary repository:** sdk-ts (companion: obsidian)  
**Milestone / group:** M02-2 / RP04  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts d616ed2, 9bf40d2 (found by examples 056, step 9).  
**Depends on:** LFCP-02-027, LFCP-02-106  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); OBSIDIAN-SYNC-INDICATORS-01.md  
**Gate / test trace:** G09, G10 / T08, T09

**Goal:** A member refused by the server is shown as refused, not as waiting to sync.

**Acceptance:**

1. When RESOURCE_OPEN is refused with AUTHORIZATION_FAILED and the access recovery (106) does not help, accessState, canWrite and commit report allowed false with the reason server-refused, current false and how the recovery ended; never "revoked", since the server does not say why.
2. Unaccepted batches are blocked (not accepted: access refused by the server), with their work kept; catch-up is unknown; each change is a status event; an open again clears it.
3. obsidian: the status text for a refused section.

**Required checks:** Live test against the Rust server: a member revoked while offline reconnects and is refused (the scenario of examples 056); a FakeServer test of the refusal and its clearing.

**Deliverables:** The SDK change and tests; the plugin status text.

## E06. Opaque server compatibility

### LFCP-02-031 — Verify section transport limits and opaque persistence

**Primary repository:** server  
**Milestone / group:** M02-3 / RP05  
**Type / priority / status:** integration / P0 / DONE — server dc735a8, 8193b06: a section Resource end to end and the live transport evidence.  
**Depends on:** LFCP-02-003, LFCP-02-007, LFCP-02-012  
**Read first:** LFCP-WIRE-01.md; MVP-0.1-PROTOCOL-SCOPE.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G07, G08, G09 / T01, T06

**Goal:** Confirm sections work through the existing server or fix the smallest demonstrated gap.

**Acceptance:**

1. Exercise both profiles, secure frames, snapshots and configured size limits with measured synthetic payloads.
2. Server remains application-agnostic and keyless for plaintext; no Task count/search/model parsing is added.
3. If no change is needed, deliver passing evidence; if a limit blocks complete creation, resolve client/spec transaction semantics before shipping.

**Required checks:** Opaque storage and oversize tests with actual SDK-produced units (multi-change import per 084); pre-encryption privacy tested separately.

**Deliverables:** Compatibility/limits evidence and minimal code/config patch if necessary.

### LFCP-02-032 — Prove ACK and server restart guarantees

**Primary repository:** server  
**Milestone / group:** M02-3 / RP05  
**Type / priority / status:** qualification / P0 / DONE — server a18dc4d: a section import through a kill and a lost ACK.  
**Depends on:** LFCP-02-003, LFCP-02-031, LFCP-02-088  
**Read first:** LFCP-WIRE-01.md; MVP-0.1-PROTOCOL-SCOPE.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G07, G08, G09 / T01, T06

**Goal:** Validate the durability claim consumed by the status adapter.

**Acceptance:**

1. Inject death around ingest and control CAS and reconcile after an accepted unit loses its ACK.
2. Preserve exact signed objects, Control/Data/Key Packages/snapshots and documented atomic boundaries.
3. If acceptance cannot prove durable receipt, fix the documented implementation gap or propagate uncertainty without changing Wire semantics privately.

**Required checks:** Persistent-volume restart and lost-ACK scenarios; compare actual retained IDs/frontiers.

**Deliverables:** Version-pinned acceptance mapping and fault evidence.

### LFCP-02-033 — Retain authorization and negative secure-ingest behavior

**Primary repository:** server  
**Milestone / group:** M02-3 / RP05  
**Type / priority / status:** qualification / P0 / DONE — server e1925cf: the secure ingest checks on a section Resource.  
**Depends on:** LFCP-02-002, LFCP-02-031, LFCP-02-032  
**Read first:** LFCP-WIRE-01.md; MVP-0.1-PROTOCOL-SCOPE.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G07, G08, G09 / T01, T06

**Goal:** Ensure section support does not weaken the retained secure subset.

**Acceptance:**

1. Retain hosting-policy separation, control CAS, signatures and server-side checks required by Wire.
2. Exercise malformed/unauthorized/equivocating/stale objects and one-time claim contention; clients still validate before merge.
3. Run legacy and section secure flows on the same server without plaintext profile interpretation.

**Required checks:** Actual Wire negative fixtures and client/server secure integration, not mock crypto.

**Deliverables:** Server secure regression report and scoped fixes.

### LFCP-02-116 — The server refuses a store written by a newer server

**Primary repository:** server  
**Milestone / group:** M02-3 / RP05  
**Type / priority / status:** implementation / P1 / DONE — server e49f595 (gated at mvp-0.2-baseline.3, sdk-rs 76609e5: fmt, clippy, 170/170). Found by the 074 rehearsal; in place before the first schema change.  
**Depends on:** LFCP-02-074  
**Read first:** MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; LFCP-WIRE-01.md  
**Gate / test trace:** G07 / T06, T12

**Goal:** A server rolled back across a schema change stops instead of running on a schema it does not know.

**Acceptance:**

1. Opening a store whose schema version is above every migration the server knows fails with a clear error naming both versions, before anything is written; the server exits.
2. The refused store keeps its files byte for byte (no WAL or SHM file is created); a newer version held only in the WAL is refused too.
3. Once the version is one the server knows, the store opens as before; README states that a rollback across a schema change needs a backup made by the older version.

**Required checks:** A store at schema version latest+1: refused by Store::open and by the server binary, files unchanged; the same with the version only in the WAL; reopened once the version is restored.

**Deliverables:** The store guard, its test, the README note.

## E07. Markdown ownership and reconciliation

### LFCP-02-034 — Parse lexical section boundaries and reserved markers

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 98ce92c (parser), fixes 67f2d5c, 5742557, 2abd935, 2a80c54, 517a545; test/core/sections/parser.test.ts (boundaries, fences and comments literal, overlaps, private text after the end marker).  
**Depends on:** LFCP-02-007, LFCP-02-008, LFCP-02-090  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Establish exact ownership without leaking neighboring private text.

**Acceptance:**

1. Recognize canonical matching start/end references and immediate title heading only in valid lexical contexts.
2. Diagnose missing/mismatched/overlapping/nested/invalid boundaries without extending to a guessed heading or file end.
3. Keep marker-shaped fenced/inline examples literal and return exact source spans plus diagnostics.

**Required checks:** MS05, MS06 and malformed boundary fixtures with private canaries.

**Deliverables:** Boundary scanner and parser tests.

### LFCP-02-035 — Parse supported Task, item and paragraph trees

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 98ce92c and the fixes of 034; test/core/sections/parser.test.ts (nodes: child-line refs and content-column nesting, tabs, raw nodes, unsupported headings, continuation lines, MS17, MS22, MS31, MS41).  
**Depends on:** LFCP-02-034  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; SHARED-OBJECTS-PROFILE-01.md; MARKDOWN-REFS-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Represent the complete supported section body and preserve source fidelity.

**Acceptance:**

1. Handle nested Tasks/items/paragraphs, ordered/unordered list styles, blank lines, soft breaks and both Task ref forms.
2. Preserve supported Task fields and unknown source tokens according to the adopted adapter contract; exclude all binding metadata from content.
3. Unsupported tables/fences/callouts/headings/embeds and unsafe indentation produce non-destructive diagnostics.

**Required checks:** MS01, MS02, MS13, MS16, MS17 and actual fixture inventory.

**Deliverables:** Supported tree parser and fidelity tests.

### LFCP-02-036 — Map owned spans, field tokens and Unicode offsets

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 0a8245c; wired in fbcd6ac, e29d5c4.  
**Depends on:** LFCP-02-035, LFCP-02-009  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Make source/model diffs precise and version-aware.

**Acceptance:**

1. Map node IDs, Task fields and layout/ref spelling to source ranges without using titles as identity.
2. Translate UTF-16 editor offsets to SDK Unicode-scalar positions against the matching revision.
3. Preserve CRLF/LF, emoji and unrelated source bytes; stale offsets cannot target a newly merged Text silently.

**Required checks:** MS02, MS09, MS12 and selected-range Unicode edits.

**Deliverables:** Source-map/token API and round-trip tests.

### LFCP-02-037 — Infer safe semantic intents from trusted projection bases

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian a4253fd; wired in 8347610.  
**Depends on:** LFCP-02-009, LFCP-02-036  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Distinguish real user edits from lost bindings or stale projections.

**Acceptance:**

1. Allocate one retained identity for proven insertion inside a healthy loaded authorized section; outside text remains private.
2. Detect duplicate/foreign/orphan/lost markers and ambiguous cuts instead of inventing new nodes or global deletion.
3. Diff only owned semantics against a trusted base; classify whole-projection loss separately from body-node deletion.

**Required checks:** MS03, MS04, MS08, MS10 variants, MS11 and MS18.

**Deliverables:** Semantic differ with explicit ambiguous/candidate outcomes.

### LFCP-02-038 — Persist projection bases, candidates and journals

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 803034b, de0cb39.  
**Depends on:** LFCP-02-009, LFCP-02-025, LFCP-02-029, LFCP-02-036, LFCP-02-098  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Retain enough local information to recover without guessing causality.

**Acceptance:**

1. Store per-projection base revisions, source snapshots/maps, pending candidates and journal phases locally.
2. Keep private snapshots/paths out of shared payloads and default diagnostics; retain unresolved recovery copies.
3. Index rebuilding recovers identity/ranges but does not manufacture a missing causal base or overwrite newer files.

**Required checks:** MS11, CM11 and crashes at local journal boundaries; storage errors preserve user candidates.

**Deliverables:** Local projection store and recovery tests.

### LFCP-02-039 — Commit local section edits through the SDK journal

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 12eeaec, e4e6c16, fbcd6ac.  
**Depends on:** LFCP-02-017, LFCP-02-026, LFCP-02-027, LFCP-02-037, LFCP-02-038  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Connect safe source intents to durable shared updates exactly once per recorded intent.

**Acceptance:**

1. Capture/revalidate source, persist allocated IDs, submit intents through durable receipts and record semantic outcomes.
2. Insert metadata/projection updates under guarded phases; uncertain SDK completion queries the receipt rather than duplicating changes.
3. Keep read-only/revoked/unsupported or incomplete edits as labeled local candidates, never unauthorized writes.

**Required checks:** Crash before commit, after commit before marker insertion and after source write; SI02/SI17.

**Deliverables:** Local reconciliation controller and integration tests.

### LFCP-02-040 — Apply remote changes with minimal revision-checked patches

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian babef99, 6b81f66.  
**Depends on:** LFCP-02-014, LFCP-02-028, LFCP-02-036, LFCP-02-038  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Project model changes without overwriting concurrent local text.

**Acceptance:**

1. Patch only changed owned spans while preserving formatting, private bytes and current ref placement.
2. Recheck document revision/ranges immediately before applying; rebase or retain comparison if stale.
3. Freeze destructive structural projection on conflict/invalid/broken state; never delete blocked nodes just because a derived tree omits them.

**Required checks:** MS02, MS12, MS14 and remote patch versus typing/candidate races.

**Deliverables:** Projection planner/writer and stale-patch tests.

### LFCP-02-041 — Coordinate open editors, closed files and external changes

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian db6067f, 301a1c8.  
**Depends on:** LFCP-02-039, LFCP-02-040  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Use one coherent source revision across file and view events.

**Acceptance:**

1. Route open-file writes through editor transactions and closed-file writes through the guarded host path.
2. Coalesce by file/Resource without holding locks over network waits; coordinate multiple views of one note.
3. Reconcile external/third-party edits against a trusted base instead of treating a stale file as authoritative shared state.
4. An obsidian ADR reverses the 0.1 decision to defer to the file path over editor transactions for sections (M3): CodeMirror transactions for open notes, vault.process for closed ones; legacy Tasks stay on the file path.

**Required checks:** External write during local typing/remote patch, split views, rename and repeated file events.

**Deliverables:** File/view coordinator and race tests.

### LFCP-02-042 — Prevent generated-write feedback without losing user edits

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP06  
**Type / priority / status:** implementation / P0 / DONE — obsidian 4174dc0.  
**Depends on:** LFCP-02-039, LFCP-02-040, LFCP-02-041  
**Read first:** MARKDOWN-SECTIONS-01.md; MARKDOWN-SECTIONS-FIXTURES-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T05

**Goal:** Suppress only events attributable to exact generated changes.

**Acceptance:**

1. Track operation IDs and expected revisions/spans rather than ignoring all events while an async write runs.
2. Metadata insertion and remote patches create no duplicate semantic intents.
3. Interleaved user/Tasks-plugin writes and repeated notifications are still reconciled correctly.

**Required checks:** Fault/race traces with multiple file events, generated patches and overlapping user edits.

**Deliverables:** Mutation provenance guard and regression tests.

## E08. Native editor lifecycle

### LFCP-02-043 — Integrate native edits, selection and IME

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian 7733c6b, e29d5c4 (typing and IME scheduling in the editor).  
**Depends on:** LFCP-02-041, LFCP-02-042, LFCP-02-096  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G05, G07, G08 / T05

**Goal:** Use actual editor transactions without disrupting normal typing.

**Acceptance:**

1. Observe supported edits/composition and defer ambiguous transient syntax while preserving local input.
2. Map cursor/selection through safe generated patches and avoid publishing incomplete structures.
3. Expose processing/blocked states immediately enough that prior healthy success is not misleading.

**Required checks:** Native Source/Live Preview typing, IME, emoji selections and incoming edits on pinned hosts.

**Deliverables:** Editor transaction bridge and native tests.

### LFCP-02-044 — Bridge native undo/redo to compensating intents

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian 8bb2559, wired in the editor engine.  
**Depends on:** LFCP-02-015, LFCP-02-043  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G05, G07, G08 / T05

**Goal:** Reverse user actions safely without rewinding shared history.

**Acceptance:**

1. Undo of committed work emits a new causal intent against current state; actor/history counters never rewind.
2. Group/annotate metadata insertion so undo does not detach only an ID and recreate the same visible item.
3. Remote projection and status-only updates do not enter history as new local authored edits.

**Required checks:** Undo/redo after local creation, remote update, acknowledged edit, cut and same-value lifecycle resolution.

**Deliverables:** Undo bridge and model/source/history assertions.

### LFCP-02-045 — Maintain multiple projections and rebuild safely

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian db6067f, 8347610: one source per note across projections, one pass per note.  
**Depends on:** LFCP-02-038, LFCP-02-043  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G05, G07, G08 / T05

**Goal:** Keep each view tied to its own trusted base.

**Acceptance:**

1. Complete section copy creates another projection with the same identities; standalone Task edits never delete omitted children.
2. File rename/move and line shifts preserve identity; update only local locators and indexes.
3. After base/index loss or plugin-disabled editing, preserve comparison candidates rather than upload a stale whole section.
4. Plugin start filters notes by "lfcp-", not "lfcp-ref".

**Required checks:** MS07, MS11, CM11; two section projections plus standalone Tasks and restart.

**Deliverables:** Projection registry/rebuild behavior and tests.

### LFCP-02-046 — Implement context-aware delete, detach, duplicate and cut/paste

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian 299d23b, 16e145d.  
**Depends on:** LFCP-02-015, LFCP-02-037, LFCP-02-044, LFCP-02-045  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G05, G07, G08 / T05

**Goal:** Make structural edits and local removal have distinct effects.

**Acceptance:**

1. Reliable body deletion uses recoverable lifecycle intents; whole projection/file deletion removes only the local view.
2. Detach retains current readable source and strips only that projection bindings without revoke or shared deletion.
3. Duplicate-as-new allocates new identities explicitly; same-session bound-unit cut/paste can restore/move retained identity; ambiguous/cross-Resource actions diagnose or invoke explicit copy/import.

**Required checks:** MS10 variants, MS18, UX11/UX12 and interrupted cut/paste with concurrent child edits.

**Deliverables:** Context commands and shared-versus-local effect tests.

### LFCP-02-047 — Run production Markdown fixtures and extraction canaries

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** qualification / P0 / DONE — obsidian 0178195: the Markdown fixtures through a product adapter.  
**Depends on:** LFCP-02-010, LFCP-02-039, LFCP-02-040, LFCP-02-046  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G05, G07, G08 / T04, T10

**Goal:** Prove actual parser/reconciler behavior against the published corpus.

**Acceptance:**

1. Provide the implementation adapter for all 29 Markdown fixtures and approved additions without consuming expected outputs as inputs.
2. Assert exact private-byte preservation, semantic intents, bindings and no publication for damaged/ambiguous ranges.
3. Inspect shared plaintext before encryption; ciphertext scans alone cannot prove extraction privacy.

**Required checks:** Full fixture manifest, private canaries for two Resources and supported/unsupported copy/paste cases.

**Deliverables:** Production fixture adapter and privacy report.

### LFCP-02-048 — Render safe boundaries and minimal states in all editor modes

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian 6a20168, 0592545, 6f70c41.  
**Depends on:** LFCP-02-034, LFCP-02-043, LFCP-02-045  
**Read first:** OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; MARKDOWN-SECTIONS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G04, G08, G10 / T05, T09

**Goal:** Make sharing and blocked reconciliation discoverable from the first local slice.

**Acceptance:**

1. Register Source/Live Preview decorations and idempotent Reading post-processing using source identity mappings.
2. Show exact boundaries and minimal loading/attention without guessing DOM identity from title text.
3. Handle fragments, folds, viewport changes, split views and cleanup; missing exact mapping gives an honest fallback and a compatibility issue.
4. Per-node metadata is hidden in Live Preview by default (M5).
5. Provide a "Show sharing metadata" command and declarative setting: the caret never reaches a hidden binding line by arrow keys (spike obsidian 003e50a, docs/devel/reports/marker-hiding-spike.md). Use a state field with block replace decorations in Live Preview only; Reading view needs no hiding code (host fact H7). Show the section boundary independently of hidden markers.

**Required checks:** Three native modes, folded conflict and lifecycle cleanup; source bytes unchanged by decoration.

**Deliverables:** Native rendering adapters and minimal boundary/attention UI.

### LFCP-02-095 — Section behaviour on mobile

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / NOT_STARTED  
**Depends on:** LFCP-02-048  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G11, G12 / T08

**Goal:** Keep mobile users safe without dropping them from the catalog.

**Acceptance:**

1. On Platform.isMobile, sections are read-only or marked unsupported (V3); legacy Tasks keep working.
2. isDesktopOnly stays false.
3. No section write path can run on mobile.

**Required checks:** Unit tests with the platform flag; manual check on one mobile device if available.

**Deliverables:** Mobile guard and tests.

### LFCP-02-096 — Native Obsidian harness in CI on three systems

**Primary repository:** obsidian  
**Milestone / group:** M02-2 / RP07  
**Type / priority / status:** implementation / P0 / DONE — obsidian 771f298 (the native harness), a098ff6 (CI on three systems, dispatch only).  
**Depends on:** LFCP-02-005  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); MVP-0.2-TEST-AND-RELEASE-PLAN.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G10, G12 / T05, T11

**Goal:** Give native editor, clipboard and timing evidence a reproducible runner.

**Acceptance:**

1. A harness drives real Obsidian (Source, Live Preview, Reading) with the plugin and asserts source bytes and selection.
2. CI runs it on macOS, Windows and Linux; p95 budgets are measured on macOS only (V4).
3. Manual smoke records for Windows and Linux close POST-002.

**Required checks:** Harness self-test and one section scenario on three systems.

**Deliverables:** Harness, CI job and smoke records.

## E09. Secure sharing, join and import

### LFCP-02-049 — Build exact-range share preview and preflight

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian ec36e27, 9f47730, cb5a622.  
**Depends on:** LFCP-02-035, LFCP-02-047, LFCP-02-048  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Let users share a large supported section in one deliberate action.

**Acceptance:**

1. Preview exact selected content and all child text, plus newly shared future-addition meaning; no 200 per-Task confirmations.
2. Use a heading only to propose initial range; reject unsupported/partial/cross-boundary content and refresh stale source revisions.
3. Detect legacy/foreign refs and route to explicit import rather than silently granting access to an old Resource.
4. One Resource and one invitation per section (M9); share offers to split a section that contains nested headings (M6).

**Required checks:** UX01, UX02, UX05, UX13/UX14 with private canaries and unsupported nested headings.

**Deliverables:** Share preview/preflight with native range checks.

### LFCP-02-050 — Journal dedicated section creation and hosting readiness

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian f62b9dc, cf72031; 07f9a0e (hosting).  
**Depends on:** LFCP-02-025, LFCP-02-026, LFCP-02-031, LFCP-02-032, LFCP-02-049, LFCP-02-084  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Create one recoverable section Resource from the approved range.

**Acceptance:**

1. Persist target identities and creation phase before effects; retries reuse the existing operation/Resource.
2. Only complete durably prepared content is projected/published through the secure SDK path.
3. Invitations remain unavailable until required hosting/control/data readiness; cancel retains original text and recorded partial target state.

**Required checks:** Crash at prepared/local/hosted/projection phases, lost ACK and source edit during preview.

**Deliverables:** Creation orchestrator/journal and idempotent recovery tests.

### LFCP-02-051 — Integrate secure invitation and join retry states

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian 2ea194c, 5e63411, b013e23, b8437c4; sdk-ts a44551b (claim journal, 110).  
**Depends on:** LFCP-02-027, LFCP-02-033, LFCP-02-050, LFCP-02-086, LFCP-02-087  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Join the complete section through existing one-time authorization.

**Acceptance:**

1. Show validation, claim, key delivery and load stages separately; pending invitation is not active membership.
2. Resume uncertain claim with recorded identities and baseline protocol reconciliation; no new identity bypass.
3. Unknown profile, unavailable key/server and failed claim preserve local notes and present actionable distinct errors.

**Required checks:** UX03, second claim rejection, interruption after claim and unsupported client flow.

**Deliverables:** Join/invitation state adapter and secure integration tests.

### LFCP-02-052 — Insert only fully loaded section projections

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian d6bd61a, 74d1455, 9cf210c.  
**Depends on:** LFCP-02-028, LFCP-02-045, LFCP-02-048, LFCP-02-051, LFCP-02-097  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Choose local placement without empty-state publication or duplicate retry.

**Acceptance:**

1. Preview loaded supported content and insert a complete binding at a valid block boundary.
2. Retrying one insertion operation reuses its ID; a deliberate new insertion creates another projection intentionally.
3. Join cancellation and insertion cancellation are distinct; neither overwrites private selection or publishes an empty model.

**Required checks:** Interrupted load/insert, two projections, read-only loaded section and stale target document.

**Deliverables:** Insertion command/journal and tests.

### LFCP-02-053 — Preflight legacy-to-section explicit copy/import

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian ce56a22, 6affde8.  
**Depends on:** LFCP-02-004, LFCP-02-027, LFCP-02-049  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Capture explicit target values without pretending identity-preserving migration.

**Acceptance:**

1. Show newly shared child text and new identities; source collaboration and future edits remain independent.
2. Capture source heads/revision, conflicts and unknown extensions; block unsafe/unresolved remapping rather than silently discard fields.
3. Handle repeated Task occurrences explicitly; copied assignees do not grant access or fabricate participant identities.

**Required checks:** CM04, CM08, CM09, CM12 and UX17.

**Deliverables:** Import preflight/value mapping and tests.

### LFCP-02-054 — Persist import phases and non-destructive rollback

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian ce56a22 (import with rollback), 6affde8.  
**Depends on:** LFCP-02-029, LFCP-02-050, LFCP-02-052, LFCP-02-053  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Make target creation and local replacement resumable across failures.

**Acceptance:**

1. Journal source copy/revision, target IDs, mapping and exact progress; reuse targets after unknown network outcome.
2. Replace source only after target readiness and revision checks; preserve source/target edits during cancellation or rollback.
3. Already-issued invitations/disclosure cannot be undone by restoring a local view; no history relabeling or dual-write bridge.

**Required checks:** CM05–CM07, CM13–CM14 and crashes at every declared import phase.

**Deliverables:** Import/resume/rollback implementation and evidence.

### LFCP-02-055 — Integrate dual-profile upgrade and downgrade UX

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian 550cde8, 08777d2, 31f81f1, 7b6f099; sdk-ts dac706f (IndexedDB version 2).  
**Depends on:** LFCP-02-004, LFCP-02-029, LFCP-02-045, LFCP-02-054  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G07, G09, G11 / T06, T08

**Goal:** Preserve working legacy Tasks alongside section Resources.

**Acceptance:**

1. Upgrade pending state and dispatch each Resource by validated profile; no vault-wide conversion.
2. Unsupported storage/client versions fail visibly without writes or source deletion; apply the audited minimum-version policy.
3. Compatible reinstall reconciles changes made while disabled/old instead of overwriting or publishing them blindly.

**Required checks:** CM01–CM03, CM10–CM11 on actual pinned legacy/candidate builds.

**Deliverables:** Upgrade/compatibility UI, matrix and release constraints.

### LFCP-02-056 — Qualify the secure two-vault section slice

**Primary repository:** examples  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** qualification / P0 / DONE — .github 3c045fd: release/mvp-0.2-two-vault-qualification.md and .json at the mvp-0.2-baseline.2 pins (first run 8f0ae42); examples qualification/ (10d6162, 4b67dc5, 36a7005, b3c763f).  
**Depends on:** LFCP-02-006, LFCP-02-023, LFCP-02-030, LFCP-02-033, LFCP-02-044, LFCP-02-046, LFCP-02-047, LFCP-02-052, LFCP-02-055, LFCP-02-097  
**Read first:** OBSIDIAN-SHARED-SECTIONS-UX-01.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G03, G04, G05, G06, G07, G08, G09, G11 / T01, T06, T07, T08, T10

**Goal:** Prove the full model/editor/server path with independent test identities.

**Acceptance:**

1. Run creation, invite/join, nested additions, partitioned edits/conflicts, reconnect and causal resolution through actual crypto.
2. Exercise client/server restart, snapshots plus tail, revocation/epoch cutoff and retained rejected work.
3. Check pre-encryption private canaries, server opacity, legacy coexistence and durable state; unresolved baseline safety blockers prevent completion.
4. Before full recovery UI lands, the test harness may invoke an explicit SDK resolution action; this does not close native UX acceptance in task 066.

**Required checks:** Test-plan section 7 on pinned builds, W20 and W200; G03–G09 evidence.

**Deliverables:** Reproducible secure two-vault harness and report.

### LFCP-02-100 — Legacy commands inside sections (POST-018, Detach)

**Primary repository:** obsidian  
**Milestone / group:** M02-3 / RP08  
**Type / priority / status:** implementation / P0 / DONE — obsidian 88edfb4: legacy commands inside sections.  
**Depends on:** LFCP-02-046, LFCP-02-049  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); OBSIDIAN-SHARED-SECTIONS-UX-01.md; .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G10, G11 / T08, T09

**Goal:** Stop legacy per-Task commands from fighting section ownership (M10).

**Acceptance:**

1. Inside a section, Detach, Repair moved ref, Share task under cursor, Share selected tasks and Insert all tasks are disabled or redirected to the section action.
2. Outside sections they behave as in 0.3.x.
3. Analysis in W0; implementation after 046 and 049.

**Required checks:** Command tests inside and outside sections.

**Deliverables:** Command routing and tests.

## E10. Status, access and recovery UX

### LFCP-02-057 — Implement pure status reducer and race handling

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P0 / DONE — obsidian 989ddcb, a5d6c79.  
**Depends on:** LFCP-02-009, LFCP-02-026, LFCP-02-027  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Derive display state from independent verified facts.

**Acceptance:**

1. Use documented priority across durability/access/source/model/catch-up/outbound conditions; ACK never hides a conflict.
2. Distinguish local commit, exact server acceptance, no-local-writes, unknown evidence and current-at-checkpoint; no peer-read implication.
3. Handle event gaps, stale session/revision updates, partial batches, duplicate ACK and a new edit after an old ACK.

**Required checks:** SI01–SI19 pure reducer tests plus delayed event races; no product-state mutations.

**Deliverables:** Reducer/view-model API and deterministic tests.

### LFCP-02-058 — Implement compact badges and quiet row aggregation

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian fc2028f, 6f70c41.  
**Depends on:** LFCP-02-048, LFCP-02-057  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Show sharing and exceptions without a wall of healthy icons.

**Acceptance:**

1. Persistent heading/standalone-Task mark; internal healthy rows quiet; pending/issues aggregate across hidden descendants.
2. Use stable-width approved-logo geometry, distinct non-color states and meaningful hit targets without replacing Task checkboxes.
3. Source/Live Preview/Reading agree on identity/state; update only UI, not source or text history.
4. Double check means shared; synchronization state uses separate icons (M8); declarative settings.

**Required checks:** SI12, SI13, SI20; folded/offscreen/zoom/theme cases and Task done versus sync pending.

**Deliverables:** Scoped styles/vector adaptation and native renderer tests.

### LFCP-02-059 — Build tooltip and section details card

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian e0274f9, 5cf23ce.  
**Depends on:** LFCP-02-057, LFCP-02-058  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Explain current state and expose actions without polluting note content.

**Acceptance:**

1. Show qualified sync/durability/catch-up facts, pending count units and projection-specific problems.
2. Expose short hover/focus tooltip and keyboard-activated card with technical details secondary.
3. Mount card outside selectable note content, render shared text safely and bind actions to stable refs with revalidation.

**Required checks:** Native focus/activation/close, stale facts, repeated titles, malicious text markup and selection near card.

**Deliverables:** Tooltip/card components and interaction tests.

### LFCP-02-060 — Add validated access, invitations and revocation actions

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian 4ece485, 27de0c4, 79a4361, 8d86d8e, 5029186, f2a73fa; sdk-ts cf77a5a, ec31e31 (revokeAccess).  
**Depends on:** LFCP-02-027, LFCP-02-051, LFCP-02-059  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Make who has access visible without false identity or freshness claims.

**Acceptance:**

1. Display operational Principals with local aliases/identity details; pending invitations and stale offline control views are separate.
2. Invite/revoke only when authorized; pending removal remains pending until required validated control/epoch transition.
3. Consider remaining grants, disclose retained prior copies and never send invitations automatically.
4. Estimated as a new access UI, not an extension of the 0.3 status view.

**Required checks:** UX07/UX08, SI14/SI15/SI18, effective-grant and offline-action cases.

**Deliverables:** Access card/actions and actual-control integration tests.

### LFCP-02-061 — Build scalar, structure and deletion recovery views

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian 8f89fd5, 5e81fb0, 2a82688.  
**Depends on:** LFCP-02-014, LFCP-02-015, LFCP-02-016, LFCP-02-040, LFCP-02-059  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Resolve conflicts with explicit causal choices while retaining local work.

**Acceptance:**

1. Show complete known alternatives for Task/title, placement/cycle/lifecycle and hidden edits under deletion.
2. Revalidate current model/access before resolution; preserve pending candidates and do not apply whole-section server-wins replacement.
3. Restore/resolution uses SDK fresh causal intents; authors/times appear only when supported by actual metadata.

**Required checks:** UX15, SS08/SS15/SS26/SS27 through native UI; new remote change during an open recovery form.

**Deliverables:** Conflict/recovery surfaces and integration tests.

### LFCP-02-062 — Build boundary, base-loss and unsupported-content repair

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian 6cff429, 1164773, e4076b4.  
**Depends on:** LFCP-02-037, LFCP-02-038, LFCP-02-047, LFCP-02-059  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Help users repair local bindings without exposing private text.

**Acceptance:**

1. Show exact range/content candidates and affected IDs; never expand a broken boundary automatically.
2. Base-unknown/diverged source requires explicit comparison; all local text is retained until a safe action is chosen.
3. Unsupported content remains visible and blocks unsafe reconciliation for affected projections only; unrelated sections continue.

**Required checks:** UX13/UX14, MS05/MS11/MS16, stale range during repair and two independent Resources.

**Deliverables:** Repair/comparison actions and private-canary tests.

### LFCP-02-063 — Implement and verify native/readable/shared clipboard paths

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P0 / DONE — obsidian 26a33f8, fd8c3d7.  
**Depends on:** LFCP-02-046, LFCP-02-058, LFCP-02-059, LFCP-02-096  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Exclude decorative UI from both plain and rich clipboard output.

**Acceptance:**

1. Native source copy preserves selected binding metadata; readable copy strips only specified LFCP metadata; shared copy preserves complete identity binding.
2. Selection-aware serialization removes plugin-owned decorations/cards without damaging mixed private/shared text or normal formatting.
3. Actual copy/cut produces no SVG/check/status/participant material and no extra shared delete intent; CSS exclusion alone is insufficient.
4. Copying a selection that spans hidden binding lines: native copy keeps the bindings (§10), the readable copy strips them; check text/plain and text/html.

**Required checks:** UX10, MS15, SI20 in all modes and target OSes, with partial/mixed/whole-section selections.

**Deliverables:** Clipboard integration and MIME inspection evidence.

### LFCP-02-064 — Complete keyboard, focus and accessible visual behavior

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / IN_PROGRESS — obsidian: keyboard, focus and accessible visuals under way.  
**Depends on:** LFCP-02-058, LFCP-02-059, LFCP-02-060, LFCP-02-061, LFCP-02-062, LFCP-02-063  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10 / T09, T10

**Goal:** Make all important actions usable without hover or color.

**Acceptance:**

1. Provide commands, Enter/Space activation, predictable card navigation, Escape/focus restoration and meaningful accessible labels.
2. Avoid 200 compulsory Tab stops and repeated announcements per retry; hidden issues remain reachable.
3. Check actual light/dark/high-contrast, zoom, non-color cues and reduced-motion behavior without suppressing errors.

**Required checks:** UX09/UX16, keyboard-only section flow and contrast/focus checks on native builds.

**Deliverables:** Accessibility fixes and recorded manual/automated checks.

### LFCP-02-065 — Provide sanitized local diagnostics and export preview

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** implementation / P1 / DONE — obsidian 5865fc5 (local report without notes or secrets), 727caf3 (previewed export); test/core/diagnostics.test.ts, diagnostics-collect.test.ts (canaries, secrets, paths).  
**Depends on:** LFCP-02-030, LFCP-02-038, LFCP-02-059, LFCP-02-060, LFCP-02-098  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G08, G10 / T10

**Goal:** Make failures diagnosable without leaking notes or secrets.

**Acceptance:**

1. Default export excludes note/Task text, paths, source candidates, keys, invite fragments and hosting secrets.
2. Include versions, error codes, aggregates and safe state transitions; detailed identifiers/routes require deliberate previewed inclusion.
3. Export is local and user-initiated; no automatic sending or telemetry service is introduced.

**Required checks:** Synthetic private/secret canaries in logs/export across error paths; readable local failure if export fails.

**Deliverables:** Diagnostic bundle/preview and leakage tests.

### LFCP-02-066 — Execute complete native UX and status acceptance

**Primary repository:** obsidian  
**Milestone / group:** M02-4 / RP09  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-056, LFCP-02-060, LFCP-02-061, LFCP-02-062, LFCP-02-063, LFCP-02-064, LFCP-02-065, LFCP-02-096, LFCP-02-100  
**Read first:** OBSIDIAN-SYNC-INDICATORS-01.md; OBSIDIAN-SHARED-SECTIONS-UX-01.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md  
**Gate / test trace:** G09, G10, G11 / T05, T08, T09, T10

**Goal:** Validate the 38 UX/SI requirements in the actual plugin.

**Acceptance:**

1. Run UX01–UX18 and SI01–SI20 against production SDK/server facts rather than mock-only screenshots.
2. Cover all three modes, folds/split views, readonly/revoked typing, copy/detach and source/history purity.
3. Record unexecuted/failed conditions explicitly and link regression fixes before claiming G10/G11 completion.

**Required checks:** Full native acceptance matrix with actual clipboard MIME/source hashes and case-level evidence.

**Deliverables:** 38-case execution report and defect links.

## E11. Qualification and candidate

### LFCP-02-067 — Generate scale workloads and instrument performance

**Primary repository:** obsidian  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-005, LFCP-02-010, LFCP-02-043, LFCP-02-048, LFCP-02-056, LFCP-02-096  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T11

**Goal:** Measure the declared workloads reproducibly on real hosts.

**Acceptance:**

1. Generate W20/W100/W200/W200-P/W200-H/W2000 with recorded seeds, nesting, source and encoded payload sizes.
2. Instrument key-to-paint, durable commit, remote patch, cached open, card, catch-up, memory and view cleanup using the defined measurement boundaries.
3. Record per-platform baselines/raw samples/percentiles; cold/warm and clean/lossy network results remain separate.
4. Add a long Text history against the §13.1 snapshot floor, two users typing in one section with the remote-edit latency metric, and the Automerge document and checkpoint sizes.

**Required checks:** Test-plan sections 9–10 sampling protocol, actual supported-depth and depth+1 cases.

**Deliverables:** Workload fixtures, instrumentation and initial measurements.

### LFCP-02-068 — Meet performance budgets without changing semantics

**Primary repository:** obsidian  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-058, LFCP-02-059, LFCP-02-067, LFCP-02-096  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T11, T12

**Goal:** Remove measured latency/leak problems in the owning editor paths.

**Acceptance:**

1. Use affected-range parsing, viewport widgets, batched projection and cleanup only where measurements justify changes.
2. Meet frozen W200/W200-P budgets and investigate W200-H growth; stress/overflow remains non-destructive.
3. No tombstone/anchor GC, silent truncation or reduced privacy checks; SDK/server bottlenecks get linked owning-repository remediation tasks.

**Required checks:** Repeat the same samples after changes; source/privacy/concurrency regression for affected code. No-change completion requires all budgets already met.

**Deliverables:** Measured fixes or verified no-change result with comparative report.

### LFCP-02-069 — Qualify the supported desktop and plugin matrix

**Primary repository:** obsidian  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-005, LFCP-02-055, LFCP-02-063, LFCP-02-064, LFCP-02-066, LFCP-02-068, LFCP-02-095, LFCP-02-096  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T05, T08, T09, T10, T11, T12

**Goal:** Verify release claims on exact native environments.

**Acceptance:**

1. Run recorded macOS/Windows/Linux, Tasks on/off, required host versions, themes, modes and split-view axes.
2. Retain broader inherited claims only with required regression evidence; failed required environments block release.
3. Run upgrade/install/disable/re-enable and final native source/clipboard/focus behavior on candidate inputs.
4. Catalog gate: eslint-plugin-obsidianmd 0 errors, a clean-clone build and the main.js size recorded.

**Required checks:** T05/T08/T09/T10/T11 native matrix; link reusable unchanged evidence rather than duplicate tests blindly.

**Deliverables:** Platform/version matrix with evidence and unresolved issues.

### LFCP-02-070 — Qualify integrated crash, access and compatibility recovery

**Primary repository:** examples  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-024, LFCP-02-030, LFCP-02-033, LFCP-02-054, LFCP-02-055, LFCP-02-056, LFCP-02-066, LFCP-02-106  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G06, G07, G08, G09, G11, G12 / T01, T06, T07, T08, T10

**Goal:** Close multi-component fault cases missed by isolated tests.

**Acceptance:**

1. Run the fault matrix across SDK receipts, editor journals, server ACK/CAS, snapshot tails and revocation.
2. Execute CM01–CM14 on pinned builds with pending state; retain identity/candidates through all required recovery paths.
3. Confirm client-side authorization, private extraction and legacy security remain passing; no resets hide failed recovery.

**Required checks:** T01/T06/T07/T08/T10 integration with deterministic faults; reuse verified lower-level reports where inputs match.

**Deliverables:** Integrated recovery report and blocking defect list.

### LFCP-02-071 — Publish secure headless section examples

**Primary repository:** examples  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** implementation / P1 / DONE — examples 660d5e1: lfcp-todo section commands, todo-cli/test/sections.test.ts and sections-live.test.ts, todo-cli/README.md "Shared sections".  
**Depends on:** LFCP-02-023, LFCP-02-028, LFCP-02-033, LFCP-02-056  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T11, T12

**Goal:** Teach the real section API without weakening the protocol.

**Acceptance:**

1. Use public SDK APIs to create nested sections, exchange secure changes, partition/reconnect and resolve a representative conflict.
2. Pin dependencies and fixture identities; no real secrets/invitations are committed.
3. Demonstrate legacy coexistence and distinguish ref copying from capability grants.

**Required checks:** Clean checkout execution against isolated reference server and exact dependency pins.

**Deliverables:** Headless example, runnable commands and expected outcomes.

### LFCP-02-072 — Document the two-vault demonstration and recovery workflow

**Primary repository:** examples  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** implementation / P1 / DONE — examples d77e464, e4c96e6: docs/demos/two-vault-sections.md, two-vault/prepare.mjs and its test. The reviewer run of the script belongs to 066.  
**Depends on:** LFCP-02-056, LFCP-02-066, LFCP-02-071  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T11, T12

**Goal:** Make product acceptance repeatable by a reviewer.

**Acceptance:**

1. Provide exact fixture preparation, independent identities, share/join/edit/offline and recovery steps.
2. Include 200-Task nested content, private canaries, checkmark meaning, readable copy and detach.
3. Show version/limit prerequisites and distinguish tested behavior from deferred protocol/editor features.

**Required checks:** Reviewer follows instructions from clean fixture vaults; records deviations and artifact versions.

**Deliverables:** Two-vault demo script and reviewer checklist.

### LFCP-02-073 — Assemble immutable candidate builds and full evidence record

**Primary repository:** .github  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-006, LFCP-02-018, LFCP-02-022, LFCP-02-024, LFCP-02-066, LFCP-02-069, LFCP-02-070, LFCP-02-071, LFCP-02-072, LFCP-02-098, LFCP-02-099, LFCP-02-102  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md; MVP-0.2-ROADMAP.md  
**Gate / test trace:** G12 / T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12

**Goal:** Cut a reproducible candidate eligible for an opt-in pilot.

**Acceptance:**

1. Pin component/spec/corpus commits, locks/toolchains and installable asset checksums; no floating main dependencies.
2. Fill technical G01–G11 and G12 qualification evidence, status semantics/limits and known issues against that build set.
3. No unresolved inherited or new blocking safety/security/required-platform defect; no passing claim from superseded changed inputs.
4. Built on rc-verify (102) and its manifests in .github/docs/release; RELEASE-EVIDENCE is exported from it, not kept as a second source.

**Required checks:** Full mandatory candidate matrix plus clean install/build reproducibility.

**Deliverables:** Candidate assets, manifest and technical qualification report.

### LFCP-02-074 — Rehearse compatible rollback and demo restore

**Primary repository:** server  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-032, LFCP-02-055, LFCP-02-073, LFCP-02-088  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-COMPATIBILITY-AND-MIGRATION.md; OBSIDIAN-SECTIONS-ARCHITECTURE-02.md; LFCP-WIRE-01.md  
**Gate / test trace:** G12 / T11, T12

**Goal:** Prepare recovery before exposing the candidate to users.

**Acceptance:**

1. Identify the last good section-capable build and compatible storage schema; unsafe 0.1 downgrade is excluded.
2. Rehearse isolated server state/config restore and client reconciliation without actor/nonce reuse or queue loss.
3. Document pause/forward-fix/rollback choices, actual deployment ownership and whether any server change is needed.
4. Staging is the local server/deploy compose (compose.check.yaml, check.sh) with a persistent volume, never the public stack; restore uses the 088 recovery.

**Required checks:** T12 restore rehearsal, legacy+section encrypted smoke after recovery; no production state modified.

**Deliverables:** Operational rollback/restore runbook and rehearsal evidence.

### LFCP-02-091 — Publish @openlfcp/* 0.2.0-rc.N on next

**Primary repository:** sdk-ts  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-018, LFCP-02-030  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/npm-publish-checklist.md; .github: docs/release/rc-verification.md  
**Gate / test trace:** G12 / T12

**Goal:** Let beta plugin builds take the section SDK from npm.

**Acceptance:**

1. Versions of the eight packages set together; CHANGELOG; pnpm release:check passes at the commit.
2. Published by the sdk-ts release workflow on a tag vX.Y.Z-rc.N (npm Trusted Publishing, the owner approves in the GitHub environment npm-publish) to dist-tag next, never latest (V7).
3. Repeatable per rc; each rc is pinned by an exact version in obsidian (V5).

**Required checks:** release:check, the sdk-ts gate of rc-verify at the commit.

**Deliverables:** Version commit, checklist run and owner command list.

### LFCP-02-094 — Pre-release beta channel for the plugin

**Primary repository:** obsidian  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** release / P0 / NOT_STARTED  
**Depends on:** LFCP-02-087  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); obsidian: docs/devel/release.md  
**Gate / test trace:** G12 / T12

**Goal:** Run betas and the pilot without updating catalog users.

**Acceptance:**

1. release.yml accepts X.Y.Z-beta.N tags and creates a GitHub pre-release with the same three attested assets.
2. manifest.json on main keeps the catalog version until GA; release-assets.mjs checks the beta tag against its own manifest asset.
3. docs/devel/release.md documents the BRAT install of a beta.
4. The first beta with a section build waits for: 087 released (0.3.2 on @openlfcp/* 0.1.3, B1-B5); the owner's decision on the public server quotas (B15); 098 fixed or explicitly accepted by the owner for the beta (B8).

**Required checks:** A dry run of release-assets for a beta tag; workflow syntax check; doccheck.

**Deliverables:** Workflow, script and documentation changes.

### LFCP-02-099 — POST-010: deterministic engine-trap test

**Primary repository:** sdk-ts  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** implementation / P0 / DONE — sdk-ts e9cdb43: the engine-trap test runs alone with named timeouts.  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/BACKLOG-MVP-0.1.md  
**Gate / test trace:** G12 / T01

**Goal:** Keep a flaky security test out of candidate gates.

**Acceptance:**

1. engine-trap.test.ts no longer depends on machine load; on timeout it says it timed out.
2. The trap is still proved.
3. 20 consecutive runs under the capped load pass (run only with the orchestrator's consent).

**Required checks:** The test alone and the security suite.

**Deliverables:** Test change.

### LFCP-02-102 — Generalize rc-verify for MVP 0.2

**Primary repository:** .github  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P0 / DONE — .github 26e09db, 7d09c23: rc-verify for MVP 0.2 (baseline series, optional gates, release evidence, the spec-sections.lock dev pins).  
**Depends on:** LFCP-02-090  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/rc-verification.md  
**Gate / test trace:** G12 / T12

**Goal:** Qualify 0.2 candidates with the existing release tool.

**Acceptance:**

1. The baseline tag pattern is a parameter (mvp-0.1 and mvp-0.2 series); sdk-ts.lock commit pins in obsidian are checked (V5).
2. Gates for the native harness (096) and website links are added; the report exports the RELEASE-EVIDENCE fields.
3. Old manifests still verify.

**Required checks:** rc-verify on rc8 and on a 0.2 dev manifest; consistency-only runs.

**Deliverables:** rc-verify changes and docs.

### LFCP-02-105 — Early BRAT dogfood of share, insert and edit

**Primary repository:** obsidian  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** qualification / P1 / NOT_STARTED  
**Depends on:** LFCP-02-048, LFCP-02-049, LFCP-02-052, LFCP-02-087, LFCP-02-091, LFCP-02-094  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G03, G12 / T12

**Goal:** Find onboarding defects before the full pilot.

**Acceptance:**

1. 2-3 pairs use a 0.4.0-beta.N through BRAT after the two-vault slice.
2. Findings are classified and appended as tasks; no catalog release.
3. Synthetic conflict exercise only; no valuable notes.

**Required checks:** Dogfood record with build IDs.

**Deliverables:** Dogfood report.

### LFCP-02-112 — Section history growth policy

**Primary repository:** obsidian (companions: spec, sdk-ts)  
**Milestone / group:** M02-5 / RP10  
**Type / priority / status:** decision / P1 / BLOCKED — Waits for the owner's decision between (a), (b) and (c); measurements in .github docs/devel/reports/section-scale-measurements.md.  
**Depends on:** LFCP-02-067  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); SHARED-SECTIONS-PROFILE-01.md  
**Gate / test trace:** G12 / T11

**Goal:** Decide what happens when a section's history nears the Snapshot floor (about 262,000 inserted characters, LFCP-02-067).

**Acceptance:**

1. The owner chooses one: (a) show the section's history size and suggest starting a new section past about 200,000 characters; (b) raise the Snapshot floor in a spec change; (c) automatic compaction after 0.2.
2. The chosen option gets its own tasks; history is never pruned without a protocol rule (SSP §16.4).
3. Until the decision, the plugin may show the history size but takes no automatic action on it.

**Required checks:** The decision record.

**Deliverables:** An owner decision and the follow-up tasks.

## E12. Pilot and public release

### LFCP-02-075 — Run the opt-in pair pilot and record outcomes

**Primary repository:** obsidian  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** qualification / P1 / NOT_STARTED  
**Depends on:** LFCP-02-072, LFCP-02-073, LFCP-02-074, LFCP-02-091, LFCP-02-094, LFCP-02-103, LFCP-02-105  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Collect ordinary-user evidence for the approved 0.2 flow.

**Acceptance:**

1. Run the reviewed pilot size/window and workflows, including larger sections and some non-developer users.
2. Record onboarding assistance, comprehension of boundary/status/detach/access, pair reconnect success and defects against frozen thresholds.
3. Use consented minimal feedback and user-previewed diagnostics; no automatic vault upload. Unmet targets become explicit blockers for final qualification.
4. Pilot on a BRAT pre-release (094), 3-5 pairs with at least two non-developer users, 7 days (V2).

**Required checks:** Pilot protocol in test-plan section 13; synthetic conflict exercise; actual candidate IDs and pair distribution recorded.

**Deliverables:** Sanitized pilot report and actionable findings; completion records observation, not release approval.

### LFCP-02-076 — Close pilot defects and requalify the final candidate

**Primary repository:** obsidian  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** qualification / P0 / NOT_STARTED  
**Depends on:** LFCP-02-075  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Make observed failures actionable without unbounded scope expansion.

**Acceptance:**

1. Route each defect to an appended owning-repository task with regression and severity; no speculative feature additions.
2. Rerun affected families and mandatory integrated security/legacy smoke on new inputs; document any evidence reuse.
3. Repeat affected pilot observations until reviewed targets pass; no unresolved blocker/major remains. If no fixes are needed, record a verified no-change result.

**Required checks:** Defect regressions, current build matrix and repeated failed pilot observations; signed-off limits remain explicit.

**Deliverables:** Final candidate manifest, remediation evidence and pilot qualification outcome.

### LFCP-02-077 — Record concrete release go/no-go

**Primary repository:** .github  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-076  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Review actual evidence and authorize the specific release set through the project process.

**Acceptance:**

1. Review every G01–G12 gate, T-family result, compatibility limit, remaining minor issue and rollback target.
2. Require all dynamically discovered blockers to be closed with evidence; audit/task completion alone does not satisfy a failed gate.
3. Record named product/technical/release decision owners, exact candidate and allowed claims; no automatic approval or publication in this task.
4. The decision is the owner's, on the orchestrator's evidence report.

**Required checks:** Evidence/manifest consistency review; reproduce any material unverified claim before go.

**Deliverables:** Go/no-go decision and final release evidence record.

### LFCP-02-078 — Update website installation, limits and release claims

**Primary repository:** website  
**Milestone / group:** M02-6 / RP12  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-077, LFCP-02-080, LFCP-02-081, LFCP-02-104  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Describe the released build and actual demo state accurately.

**Acceptance:**

1. Publish version-pinned install/upgrade requirements, supported Markdown/platform matrix and known limits in the actual website source.
2. Explain sections, local/server checkmarks, explicit import and copy/detach/access semantics.
3. Link tested assets/demo; no full-Wire, arbitrary-Markdown, read-receipt or automatic migration claims. Drafting may precede release, publication may not.
4. Covers the website copy, its meta and og descriptions, and the positioning copy, including the "one invisible comment" claim on the site; MVP 0.2 named with the component version table (V1).

**Required checks:** Check actual links/assets, instructions and version claims against the final manifest.

**Deliverables:** Website changes and publication/link evidence.

### LFCP-02-079 — Update organization profile for the released milestone

**Primary repository:** .github  
**Milestone / group:** M02-6 / RP12  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-078  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Keep the concise organization entry point consistent with the real product.

**Acceptance:**

1. Update capability summary and installation/demo/docs links without duplicating normative specs.
2. Use approved branding and current release claims from the website/manifest.
3. Preserve unrelated organization content and keep unsupported future features clearly separate.

**Required checks:** Rendered README/link check against actual released assets and website.

**Deliverables:** Profile change and checked public links.

### LFCP-02-080 — Publish approved plugin release artifacts

**Primary repository:** obsidian  
**Milestone / group:** M02-6 / RP12  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-074, LFCP-02-077, LFCP-02-092, LFCP-02-104, LFCP-02-081  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Distribute only the exact approved candidate using the project release process.

**Acceptance:**

1. Confirm current distribution requirements at execution time and publish immutable assets/checksums with accurate versions.
2. The plugin is already listed in the catalog: a bare X.Y.Z tag with manifest.json on main updates every user. Betas use 094; GA is 0.4.0 (V1).
3. Follow recorded release authorization and supported upgrade/rollback notes; do not silently substitute a rebuilt artifact.
4. The server goes first when it changed (081); the SDK is on npm latest (092); 0.3.2 (087) and the README (104) are out.

**Required checks:** Clean installation of downloaded assets, checksum verification and secure legacy/section smoke.

**Deliverables:** Released artifacts, release notes and distribution-state evidence.

### LFCP-02-081 — Roll out or verify unchanged demo sync service

**Primary repository:** server  
**Milestone / group:** M02-6 / RP12  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-074, LFCP-02-077  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Keep the demo compatible while protecting existing Resources.

**Acceptance:**

1. If a server/config change is required, stage and deploy the approved version through the actual owner/process with tested backup/restore.
2. If no change is required, retain the existing deployment and record compatibility evidence; no gratuitous deployment.
3. Preserve legacy hosting/control/data/key state and verify encrypted section onboarding/reconnect after the action.
4. Runs before 080 when the server changed; deployment on the owner's stack is an owner action from a prepared runbook.

**Required checks:** Post-action or unchanged-service legacy+section secure smoke on dedicated test Resources; no user-data cleanup.

**Deliverables:** Deployment or no-change record with image/config and smoke evidence.

### LFCP-02-082 — Close release evidence and record follow-up ownership

**Primary repository:** .github  
**Milestone / group:** M02-6 / RP12  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-078, LFCP-02-079, LFCP-02-080, LFCP-02-081, LFCP-02-093  
**Read first:** MVP-0.2-TEST-AND-RELEASE-PLAN.md; MVP-0.2-ROADMAP.md; MVP-0.2-REPOSITORY-IMPLEMENTATION-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Reconcile published outputs with approved evidence and retained support limits.

**Acceptance:**

1. Confirm installed assets, public links, demo state and release manifest refer to the approved build set.
2. Record post-release smoke and minor-issue owners; release regression triggers the documented incident process.
3. Close G12 only with the actual distribution/operational evidence; later feature requests are a separate scope decision.
4. The decision is the owner's, on the orchestrator's evidence report.

**Required checks:** Final manifest/link/checksum/smoke consistency check; no rerun of unrelated unchanged suites.

**Deliverables:** Completed release record and bounded maintenance follow-up list.

### LFCP-02-092 — Publish @openlfcp/* 0.2.0 on latest and pin it in obsidian

**Primary repository:** sdk-ts  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-077  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/npm-publish-checklist.md  
**Gate / test trace:** G12 / T12

**Goal:** Release the approved SDK before the plugin that bundles it.

**Acceptance:**

1. The approved rc content is released as 0.2.0 (latest) by the release workflow on the tag v0.2.0 of the commit recorded in 077, after the owner's approval (V7).
2. obsidian pins the eight packages at 0.2.0 exactly; the release build reproduces from npm.
3. npm view shows 0.2.0 latest; the 0.0.0-stage placeholders are deprecated (POST-012) if still open.

**Required checks:** release:check; obsidian clean-clone build from npm.

**Deliverables:** npm release (owner) and the obsidian pin commit.

### LFCP-02-093 — Tag v0.2.0 and publish the MVP 0.2 release notes

**Primary repository:** .github  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** LFCP-02-077, LFCP-02-092  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); .github: docs/release/rc-verification.md; .github: docs/release/mvp-0.1-release-notes.md  
**Gate / test trace:** G12 / T12

**Goal:** Name one consistent MVP 0.2 release set.

**Acceptance:**

1. Tags v0.2.0 on spec (with the baseline), sdk-rs, examples and .github; server only if it changed; plugin 0.4.0 by its own tag.
2. rcN-manifest of the released set; release notes called "MVP 0.2" with a component version table (not "server 0.2.0").
3. The owner runs the tag commands from the prepared list.

**Required checks:** rc-verify on the manifest; doccheck.

**Deliverables:** Manifest, release notes and owner tag commands.

### LFCP-02-103 — Pilot operations: recruiting, consent and support

**Primary repository:** .github (owner)  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** release / P1 / NOT_STARTED  
**Depends on:** None  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); MVP-0.2-TEST-AND-RELEASE-PLAN.md  
**Gate / test trace:** G12 / T12

**Goal:** Prepare 3-5 pilot pairs with at least two non-developer users (V2).

**Acceptance:**

1. Participants, consent text and the minimal feedback form are ready.
2. A support channel and the BRAT beta instructions exist.
3. No vault content or invitation secrets are collected.

**Required checks:** Owner review of the materials.

**Deliverables:** Pilot protocol and materials.

### LFCP-02-104 — README, user guide and access disclosure for sections

**Primary repository:** obsidian  
**Milestone / group:** M02-6 / RP11  
**Type / priority / status:** release / P1 / DONE — obsidian c420a7e, 557bb9d (docs/guides/shared-sections.md), 6030ed7 (README: shared sections, what is shared, per-node markers hidden in Live Preview, what the plugin accesses).  
**Depends on:** LFCP-02-066  
**Read first:** BACKLOG-MVP-0.2.md §3 (owner decisions); OBSIDIAN-SHARED-SECTIONS-UX-01.md  
**Gate / test trace:** G12 / T12

**Goal:** Keep the trust document true for sections.

**Acceptance:**

1. README "What is shared" table, "What the plugin accesses" and the user guide part on sections.
2. The "one invisible comment" promise is rewritten for per-node markers hidden in Live Preview (M5).
3. Every claim is backed by a test, smoke record or release note.

**Required checks:** Link and claim check against the candidate.

**Deliverables:** Docs changes.

## Next handoff

Use BACKLOG-MVP-0.2-EXECUTION-MAP.md for dependencies, repository routing and scope/test coverage. Brief workers from these cards with the overrides of section 5; the batch prompt packs predate this revision and do not contain tasks 083-105 or the edits.
