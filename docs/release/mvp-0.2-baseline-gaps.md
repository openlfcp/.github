# MVP 0.2 baseline gaps and integration entry conditions

**Task:** LFCP-02-006 (M02-0, gate G01). **Date:** 2026-10-08.
**Inputs:**
- LFCP-02-001: [mvp-0.2-baseline-inventory.md](mvp-0.2-baseline-inventory.md);
- LFCP-02-002: [mvp-0.2-client-baseline.md](mvp-0.2-client-baseline.md);
- LFCP-02-003: `server: docs/devel/reports/section-transport-evidence.md`;
- LFCP-02-004: `obsidian: docs/devel/reports/legacy-client-and-other-profiles.md`;
- LFCP-02-005: `obsidian: docs/devel/reports/host-and-platform-baseline.md`.

The five audits found no defect in the released 0.1 protocol, SDKs or
server beyond what is listed below. Existing code is not presumed broken:
every gap names its owning task, and a gap that is already fixed names the
commit and the release that still has to carry it.

## 1. Gap register

Status: **fixed** (in a commit, not yet released), **released**, **open**,
or **owner** (a decision or an operation only the project owner makes).

| # | Gap | Found by | Owner task | Repository | Acceptance | Status |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | Plugin 0.3.1 spends a one-time invitation before it checks the Data Profile | review, 004 | 086, 087 | sdk-ts, obsidian | A foreign-profile invitation is refused before the claim; the link stays usable (sdk-ts live test `rust-server-invite`) | fixed: sdk-ts 0e9676e; ships in npm 0.1.3 and plugin 0.3.2 |
| B2 | Plugin 0.3.1 opens a Resource of another profile as Shared Objects | 004 | 087 | obsidian | Such a Resource is never opened or merged; the user is told to update | fixed: obsidian 35f7f83, 4490550; ships in 0.3.2 |
| B3 | A projection pass without bases can revert a peer's concurrent change | 005 (native) | 087 | obsidian | Deterministic race test and native spec `projection-race` pass | fixed: obsidian 0fd0e6b, 2e0d8a2; ships in 0.3.2 |
| B4 | Recovery after server data loss (ADR 0008) | POST-013 | 088 | spec, sdk-rs, server, sdk-ts | Live drill (lost unit, lost Resource) green against server 0.3.0 | released: spec `mvp-0.1-baseline.9`, server 0.3.0; sdk-ts in npm 0.1.3 |
| B5 | Two changes with one actor and sequence number (POST-001) | POST-001 | 089 | spec, sdk-rs, sdk-ts | Corpus section `collision`; held change applies after the rebuild | released in spec and sdk-rs; sdk-ts in npm 0.1.3 |
| B6 | npm `@openlfcp/*@0.1.2` published without build output | release | V8, 091 | sdk-ts | `release:check` packs the checkout; CI trusted publishing; fresh-install check | fixed: sdk-ts 702c061, b6bb405; 0.1.2 deprecated, `latest` on 0.1.1 until 0.1.3 |
| B7 | A member refused before its grant is re-supplied after a restore stays stopped | CI of 777f36e | 106 | sdk-ts, obsidian | The race of `rust-server-recovery` passes without the test reopening the reader; security rationale recorded | open |
| B8 | Local checkpoints and journals are plaintext at rest (M10, POST-006) | security review, OP-23 | 098 | sdk-ts, obsidian | Checkpoints, journals and pending candidates encrypted at rest | open |
| B9 | The plugin does not publish Snapshots (POST-007) | review | 097 | obsidian | A 200-Task section is joined from Snapshot plus tail | open |
| B10 | Engine-trap test timed out under load (POST-010) | POST-010 | 099 | sdk-ts | Trap test runs alone, named timeouts; three runs and a full suite green | fixed: sdk-ts e9cdb43 |
| B11 | No automated native Obsidian checks in CI | 005 | 096 | obsidian | `pnpm native` in a CI workflow on three systems | open: harness local (obsidian 771f298), CI proposal in the 005 report |
| B12 | Manual smoke on Windows and Linux never run (POST-002) | 005 | 069 | obsidian | Recorded manual runs on both systems | open |
| B13 | IME input in sections not testable by WebDriver | 005 | 069 | obsidian | Manual checklist `obsidian: docs/devel/testing/ime-checklist.md` run before the first 0.4 beta | owner |
| B14 | A plugin release updates every catalog user; no beta channel | review | 094 | obsidian | Prerelease tags through BRAT; `manifest.json` on `main` unchanged until GA | open |
| B15 | Public server quotas (20 Resources per Principal, 10 new per IP per day) against one Resource per section | 003 | 003, ADR 0009 | server (operations) | Owner sets the public limits or states them in the release notes | owner |
| B16 | Restore test of the public server and backup retention (LAUNCH-003 (a), (b)) | inventory | 088 | operations | Runbook `operations/sync-server-restore-test.md` run on the public server | owner |
| B17 | Version running on sync.openlfcp.org not observable from outside | 001 | 081 | operations | Deployed version recorded by the owner with each deploy | owner |
| B18 | Remaining section vectors: inherited negatives with the section domain, split and join, hostile maps, Text history at the Snapshot floor | 010 | 010, 107 | spec | Cases in `test-vectors/shared-sections-01`, then the shared vector format | open |
| B19 | Cross-language check of epoch cutoff (G-EP7) in `known-gaps.json` | 002 | 023, 024 | examples | Gap removed from `known-gaps.json` | open |

## 2. Blocking predicates

An audit closing does not clear any open safety or security gap. These
predicates decide when work may cross a boundary.

**Before the first public invitation to a section, including any beta:**
1. Plugin 0.3.2 is released on npm `@openlfcp/*` 0.1.3 (B1, B2, B3, B4,
   B5), so a 0.3.x user cannot spend a section invitation or open a section
   as Shared Objects.
2. The beta channel exists (B14): a section build never reaches catalog
   users before GA.
3. The owner decided the public server quotas (B15).
4. Plaintext at rest (B8) is either fixed or explicitly accepted by the
   owner for the beta, because sections keep private note text in
   journals and pending candidates.

**Before integration of the secure two-vault slice (M02-3):**
1. Contracts frozen (G02): B18 closed, both SDKs pass the corpus (011-018,
   019-022) and the cross-language comparison (023, 024; B19).
2. The shared admission module (085) exists in both SDKs.

**Before the 0.4.0 release (M02-6):**
1. B7, B9, B11, B12, B13 closed.
2. B16 run at least once on the public server.
3. G01 to G12 revalidated on the exact candidate (073) with `rc-verify`.

## 3. Audits closed without a gap

- Server: ACK after commit, profile-agnostic, all-or-nothing `DATA_PUT`,
  limits and sizes fit sections (003). No server change is needed for
  sections.
- Client: signatures, AEAD, keys, Control, capabilities, Snapshots, actor
  persistence and hostile input pass at sdk-ts 777f36e and e9cdb43 (002).
- Plugin and host facts H1 to H6, CodeMirror transactions (ADR 0001
  accepted), Tasks plugin 8.4.0 next to Shared Tasks (005).
