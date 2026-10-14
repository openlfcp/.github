# MVP 0.2 pilot report (template)

**Status:** TEMPLATE for LFCP-02-075. Fill with actual observations; replace
every `<…>`. This records **observation, not release approval**
(LFCP-02-076 acts on it). Keep it **sanitised**: no note content, file
names, paths, invitation links or keys. The thresholds are those frozen in
[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../../MVP-0.2-TEST-AND-RELEASE-PLAN.md)
§13; the protocol is [pilot-protocol.md](pilot-protocol.md).

## 1. Summary

- **Outcome:** `<thresholds met / not met; which are open>`
- **Blockers found:** `<count and one-line each, or none>`
- **Recommendation to LFCP-02-076:** `<fix-and-requalify / proceed / …>`

## 2. Scope and builds

- **Pilot window:** `<start>` – `<end>` (`<days>` days per pair).
- **Build IDs used:** `0.4.0-beta.19` `<list every build; note any
  mid-pilot update>`.
- **Server:** `<project server / named pilot server>`.
- **Distribution:** BRAT pre-release (`openlfcp/obsidian`, "Latest
  version"); `manifest.json` on `main` stayed at `<version>` (no catalog
  release during the pilot).

## 3. Participants (anonymised)

| Pair | Person | Developer? | OS | Obsidian | Build ID |
| --- | --- | --- | --- | --- | --- |
| P1 | a | `<y/n>` | `<…>` | `<…>` | `0.4.0-beta.19` |
| P1 | b | `<…>` | `<…>` | `<…>` | `<…>` |
| … | | | | | |

- Pairs: `<n>` (target 3–5). Non-developer pairs: `<n>` (target ≥2).
- Pairs on W100/W200-scale sections (~100–200 tasks): `<n>` (target ≥2).

## 4. Outcomes against frozen thresholds

| Threshold | Target | Observed | Met? |
| --- | --- | --- | --- |
| End-to-end onboarding attempts | ≥10 | `<…>` | `<y/n>` |
| …completed without developer intervention | ≥8 | `<…>` | `<y/n>` |
| Pairs completing two-vault edit/reconnect | all | `<…>` | `<y/n>` |
| Comprehension checks correct | ≥8/10 | `<…>` | `<y/n>` |
| Unresolved blocker / major defect | none | `<…>` | `<y/n>` |
| Private-content publication / unrecoverable loss | none | `<…>` | `<y/n>` |

`<If LFCP-02-005 re-derived the counts for 3–5 pairs, state the re-derived
targets here and use them above.>`

## 5. Workflow results

Per workflow (share/join, co-edit, offline/reconnect, status/access, review
conflicts, copy, detach, remove access): attempts, successes, help given,
elapsed-time range, issue codes.

- Share and join: `<…>`
- Co-edit (child content): `<…>`
- Offline and reconnect: `<…>` (any missing/duplicated content → blocker)
- Status and access comprehension: `<…>`
- Synthetic conflict exercise: `<…>` (anything lost while a choice was open?)
- Copy readable text / detach one projection: `<…>`
- Remove access (both sides observed): `<…>`

## 6. Comprehension detail

Which concept failed, not just a score: shared **boundary**,
**local-save vs. server-acceptance**, **detach**, **access removal**.

- `<concept>` — `<correct/partly/incorrect counts; common misunderstanding>`

## 7. Defects and findings

| ID | Severity | Summary (sanitised) | Build | Recoverable? | Status |
| --- | --- | --- | --- | --- | --- |
| P?-?? | `<…>` | `<…>` | `<…>` | `<y/n>` | `<open/fixed/…>` |

Each defect becomes an actionable finding for LFCP-02-076.

## 8. Intervention and attempt distribution

Record help provided and the distribution of attempts; repeated attempts by
one expert do not count as independent usability evidence.

- `<…>`

## 9. What ran and what did not

Name what was exercised, on which builds, and what did not run and why — no
entry that says only "it worked".

- Ran: `<…>`
- Did not run / not reached: `<…>` and why.

## 10. Owner decisions and open items

- `<decisions taken during the pilot, with dates>`
- `<open thresholds, re-observations needed, carry-over to LFCP-02-076>`

## 11. Evidence handling

- Diagnostics attached were **user-previewed**; no vault content, links or
  keys are included here.
- Raw per-pair records are kept privately per
  [pilot-consent.md](pilot-consent.md) retention; this report quotes only
  anonymised, aggregated results.
