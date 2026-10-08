# BACKLOG-MVP-0.2-EXECUTION-MAP

**Date:** 2026-10-08  
**Status:** Planned dependencies and coverage of revision 0.2; no completion claims  
**Canonical task definitions:** BACKLOG-MVP-0.2.md / BACKLOG-MVP-0.2.json

## 1. Start and integration rules

Start with LFCP-02-001. Once actual repositories/artifacts are resolved, 002–005 can be assigned independently to the owning layers. Task 006 consolidates findings; 007–010 pin contracts/fixtures. Review tasks 083-105 are integrated; their waves are in BACKLOG-MVP-0.2.md section 4. Baseline remediation discovered by audit is appended from 108 onward and explicitly blocks affected qualification gates.

TypeScript and Rust are independent implementations; neither must copy the other's model code. Shared fixtures/contracts are common inputs. Parser and status preparation can overlap model work where inputs are pinned. The hard dependency graph below describes what must be complete to close a task, not a prohibition on safe scaffolding or draft preparation.

The qualification candidate requires the full integrated slice and native UX, not only headless tests. After pilot and defect requalification, 077 records go/no-go. Plugin release (080) and demo rollout/no-change verification (081) follow the recorded decision. Website (078) and profile (079) then refer to actual outputs, and 082 closes the release record. Numeric IDs are not a serial execution order.

These are logical dependencies, not a personnel schedule or promise that all independent tasks can run at once. Shared-file/API ownership, reviewer availability, access and release authorization still constrain execution. No calendar or cost estimate is inferred from dependency depth.

## 2. Suggested ownership boundaries

One active writer per shared package/module avoids collisions; use the project rules of BACKLOG-MVP-0.2.md section 5. Separate model/intents, validation/interop, parser/reconciliation, editor rendering/UX and release verification where capacity permits. A consumer can prepare against a pinned provider interface, but must integrate the tested provider before completion.

No agent prompt pack is defined here. Future packs should respect the graph and task reading sets instead of blindly grouping consecutive numbers. Every handoff names exact spec/corpus/package commits and test evidence; no consumer depends on an uncommitted working tree.

## 3. Repository index

| Primary repository | Tasks | Count |
| --- | --- | --- |
| .github | 001, 006, 073, 077, 079, 082, 093, 101, 102 | 9 |
| sdk-ts | 002, 011, 012, 013, 014, 015, 016, 017, 018, 025, 026, 027, 028, 029, 030, 086, 091, 092, 098, 099 | 20 |
| server | 003, 031, 032, 033, 074, 081 | 6 |
| obsidian | 004, 005, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 047, 048, 049, 050, 051, 052, 053, 054, 055, 057, 058, 059, 060, 061, 062, 063, 064, 065, 066, 067, 068, 069, 075, 076, 080, 087, 094, 095, 096, 097, 100, 104, 105 | 48 |
| spec | 007, 008, 009, 010, 083, 084, 090, 107 | 8 |
| sdk-rs | 019, 020, 021, 022 | 4 |
| examples | 023, 024, 056, 070, 071, 072 | 6 |
| website | 078 | 1 |
| sdk-ts (companion: sdk-rs, by another worker) | 085 | 1 |
| spec + sdk-ts + sdk-rs + server (split per repository at dispatch) | 088 | 1 |
| spec + sdk-ts + sdk-rs (split per repository at dispatch) | 089 | 1 |
| .github (owner) | 103 | 1 |
| sdk-ts (companion: obsidian) | 106 | 1 |

All abbreviated IDs in this map use the LFCP-02 namespace. A primary repository identifies the accountable deliverable; integration reports may consume several components. It does not authorize changing another layer without its own reviewed task.

## 4. RP change-group coverage

| Group | Tasks |
| --- | --- |
| RP00 | 001, 002, 003, 004, 005, 006, 086, 087, 088, 089, 101 |
| RP01 | 007, 008, 009, 010, 083, 084, 090, 107 |
| RP02 | 011, 012, 013, 014, 015, 016, 017, 018, 085 |
| RP03 | 019, 020, 021, 022, 023, 024 |
| RP04 | 025, 026, 027, 028, 029, 030, 097, 098, 106 |
| RP05 | 031, 032, 033 |
| RP06 | 034, 035, 036, 037, 038, 039, 040, 041, 042 |
| RP07 | 043, 044, 045, 046, 047, 048, 095, 096 |
| RP08 | 049, 050, 051, 052, 053, 054, 055, 056, 100 |
| RP09 | 057, 058, 059, 060, 061, 062, 063, 064, 065, 066 |
| RP10 | 067, 068, 069, 070, 071, 072, 073, 074, 091, 094, 099, 102, 105 |
| RP11 | 075, 076, 077, 092, 093, 103, 104 |
| RP12 | 078, 079, 080, 081, 082 |

## 5. Scope-gate contribution and closure

A contribution is not a gate pass. The review tasks below aggregate evidence; their referenced implementation work, baseline remediation and unresolved defects remain part of the gate. Task 006 classifies baseline findings, while task 073 revalidates their closure on the candidate.

| Gate | Contributing tasks | Required closure/review tasks |
| --- | --- | --- |
| G01 | 001, 002, 003, 004, 005, 006, 101 | 006, 073 |
| G02 | 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 083, 084, 085, 090, 107 | 010, 018, 022, 023, 024 |
| G03 | 049, 050, 051, 052, 053, 054, 055, 056, 105 | 056 |
| G04 | 011, 012, 013, 014, 015, 016, 017, 018, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 047, 048, 056, 084 | 047, 056, 066 |
| G05 | 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 047, 056 | 023, 045, 046, 056 |
| G06 | 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 056, 070, 089 | 024, 056, 061, 070 |
| G07 | 009, 025, 026, 028, 029, 030, 031, 032, 033, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 047, 049, 050, 051, 052, 053, 054, 055, 056, 070, 084, 085, 088, 089, 097, 106 | 030, 032, 044, 054, 070, 088 |
| G08 | 031, 032, 033, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 047, 048, 056, 065, 070, 085, 098 | 047, 056, 063, 065, 070 |
| G09 | 027, 030, 031, 032, 033, 049, 050, 051, 052, 053, 054, 055, 056, 057, 058, 059, 060, 061, 062, 063, 064, 066, 070, 106 | 027, 033, 056, 060, 070 |
| G10 | 009, 026, 027, 030, 048, 057, 058, 059, 060, 061, 062, 063, 064, 065, 066, 096, 100 | 063, 064, 066 |
| G11 | 004, 029, 049, 050, 051, 052, 053, 054, 055, 056, 066, 070, 086, 087, 095, 100 | 055, 066, 070, 087 |
| G12 | 005, 067, 068, 069, 070, 071, 072, 073, 074, 075, 076, 077, 078, 079, 080, 081, 082, 091, 092, 093, 094, 095, 096, 099, 102, 103, 104, 105 | 069, 073, 074, 076, 077, 082 |

## 6. Test-family responsibility

| Family | Tasks requiring this evidence |
| --- | --- |
| T01 | 001, 002, 003, 006, 031, 032, 033, 056, 070, 073, 088, 099 |
| T02 | 007, 008, 010, 011, 012, 013, 014, 015, 016, 017, 018, 073, 083, 084, 085, 089, 090, 107 |
| T03 | 019, 020, 021, 022, 023, 024, 073, 085 |
| T04 | 007, 008, 010, 034, 035, 036, 037, 038, 039, 040, 041, 042, 047, 073 |
| T05 | 005, 034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046, 048, 066, 069, 073, 096 |
| T06 | 031, 032, 033, 049, 050, 051, 052, 053, 054, 055, 056, 070, 073, 097 |
| T07 | 009, 025, 026, 028, 030, 056, 070, 073, 088, 089, 097, 106 |
| T08 | 004, 027, 029, 049, 050, 051, 052, 053, 054, 055, 056, 066, 069, 070, 073, 086, 087, 095, 100, 106 |
| T09 | 009, 026, 027, 030, 048, 057, 058, 059, 060, 061, 062, 063, 064, 066, 069, 073, 100 |
| T10 | 047, 056, 057, 058, 059, 060, 061, 062, 063, 064, 065, 066, 069, 070, 073, 098 |
| T11 | 005, 067, 068, 069, 071, 072, 073, 074, 096 |
| T12 | 005, 068, 069, 071, 072, 073, 074, 075, 076, 077, 078, 079, 080, 081, 082, 091, 092, 093, 094, 101, 102, 103, 104, 105 |

## 7. Existing corpus and acceptance inventories

| Inventory | Implementation evidence owner | Additional native/integration closure |
| --- | --- | --- |
| SS01–SS28 and approved additions | 018 TypeScript; 022 Rust | 023 bidirectional exchange; 024 randomized schedules; 056/070 secure integration |
| All 29 Markdown fixtures and additions | 047 production parser/reconciler adapter | 043–048 editor; 063 clipboard; 066/069 native qualification |
| CM01–CM14 | 004 audit; 029/053–055 implementation | 070 actual-build compatibility/fault matrix |
| UX01–UX18 | Feature owners 049–065 | 066 full native run; 069 platform matrix |
| SI01–SI19 | 057 pure reducer and relevant SDK evidence | 066 actual integration |
| SI20 / MS15 | 063 copy and 058 status rendering | 066/069 source/history/MIME checks |
| Legacy Wire/Task gates | 002/003 audits and appended owning-layer fixes | 033/056/070/073 final actual-build evidence |

The existing reference corpus counts do not include planned extensions from 010. Preserve its fixture manifest IDs, including suffixed Markdown cases. New tests get explicit new IDs; do not call them already executed or renumber existing fixture history.

## 8. Dependency levels

Each level below is computed as one plus the maximum dependency level of a task. It is a graph check and scheduling aid, not a recommended prompt-pack size or duration. Completion can unlock work earlier than completing every other task in the same level.

| Level | Tasks |
| --- | --- |
| 0 | 083, 086, 088, 089, 099, 101, 103 |
| 1 | 001, 084, 087, 106 |
| 2 | 002, 003, 004, 005, 094 |
| 3 | 006, 096 |
| 4 | 007 |
| 5 | 008, 009, 085 |
| 6 | 010 |
| 7 | 090, 107 |
| 8 | 011, 019, 034, 102 |
| 9 | 012, 020, 027, 035 |
| 10 | 013, 021, 025, 031, 036 |
| 11 | 014, 022, 026, 032, 037 |
| 12 | 015, 028, 033, 057 |
| 13 | 016, 029, 097 |
| 14 | 017, 030, 098 |
| 15 | 018, 038 |
| 16 | 023, 039, 040, 091 |
| 17 | 024, 041 |
| 18 | 042 |
| 19 | 043 |
| 20 | 044, 045 |
| 21 | 046, 048 |
| 22 | 047, 058, 095 |
| 23 | 049, 059 |
| 24 | 050, 053, 061, 062, 063, 100 |
| 25 | 051 |
| 26 | 052, 060 |
| 27 | 054, 064, 065, 105 |
| 28 | 055 |
| 29 | 056 |
| 30 | 066, 067, 071 |
| 31 | 068, 070, 072, 104 |
| 32 | 069 |
| 33 | 073 |
| 34 | 074 |
| 35 | 075 |
| 36 | 076 |
| 37 | 077 |
| 38 | 081, 092 |
| 39 | 080, 093 |
| 40 | 078 |
| 41 | 079 |
| 42 | 082 |

## 9. Extension and change control

Append LFCP-02-107 onward for discovered repairs or justified splits. Record parent task, repository, dependencies, specification authority, acceptance regression and affected G/T IDs. Update this map and the JSON atomically with the Markdown source. Do not use DONE on a parent coordination task to conceal unimplemented repairs.

If scope changes, update the owning scope/spec and acceptance corpus first. Performance thresholds remain the reviewed values from task 005; implementation convenience does not authorize loosening them. Release actions are concrete reviewed operations, not automatic side effects of an agent completing code.
