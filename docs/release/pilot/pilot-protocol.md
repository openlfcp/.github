# MVP 0.2 pilot protocol (draft)

**Status:** DRAFT (LFCP-02-103, materials for LFCP-02-075), not run. The
thresholds below are the frozen values of
[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../../MVP-0.2-TEST-AND-RELEASE-PLAN.md)
§13; the counts drafted there for 5–10 pairs are re-derived for 3–5 pairs by
LFCP-02-005 before the pilot. `<…>` marks a value the owner settles.

## Purpose

Collect ordinary-user evidence that the approved MVP 0.2 flow — sharing a
section, joining, co-editing, offline, conflicts and access — works and is
understood, before the public release. This is a small product check, not
statistical proof of market fit. Repeated attempts by one expert do not
substitute for independent usability evidence.

## Participants

- **3–5 opt-in pairs** (decision V2), at least **two pairs with
  non-developer users**.
- At least **two pairs** use **W100/W200-scale real workflows**: a section
  of about **100–200 tasks** with their notes.
- An earlier dogfood of 2–3 pairs precedes this pilot (LFCP-02-105); it is
  not part of these outcomes.
- Do not require anyone to share sensitive personal notes. Use the
  participant's own non-sensitive notes or the supplied synthetic content.

## Build and window

- **Build:** a BRAT pre-release `0.4.0-beta.18` (LFCP-02-094), installed as
  in [pilot-install-guide.md](pilot-install-guide.md). The community
  directory and Obsidian's own updates keep offering 0.3.x; `manifest.json`
  on `main` moves to `0.4.0` only at the public release.
- **Window:** at least **7 days** of ordinary usage per pair.
- **Server:** `<the project server sync.openlfcp.org, or a server the owner
  names for the pilot>`.

## Daily workflows each pair runs

Over the window, each pair completes, at least once, and reports the
outcome:

1. **Share and join** — one person runs "Share section…", invites the
   other with a one-time link; the other runs "Join collaboration" then
   "Insert shared section…" in a note of their own.
2. **Co-edit** — both add and change tasks, subtasks, paragraphs and list
   items inside the section; child content added later is shared too.
3. **Offline and reconnect** — one person edits offline, then reconnects;
   the two-vault edit/reconnect cycle completes with no unexplained missing
   or duplicated content.
4. **Status and access** — both read the status marks (the ✓✓ "shared" mark
   and the separate sync icon) and open "Open shared section details" to see
   who has access, as last verified with the server.
5. **Review conflicts** — run the synthetic conflict exercise below and
   resolve it with "Review conflicts…".
6. **Copy and detach** — use "Copy readable text (without sharing
   metadata)", and "Detach this section" on one of the two projections.
7. **Remove access** — the owner of one section runs "Remove access…" and
   both observe the result on each side.

## Synthetic conflict exercise

Run during onboarding, on **synthetic content only** — never induce a
conflict in valuable notes. Suggested script:

1. Both people open the same shared section and go offline.
2. Each moves the **same task** under a **different parent**.
3. Both reconnect. Each side shows "Needs your attention"; the line shows
   "Needs attention".
4. One person opens "Review conflicts…", answers the single question and
   clicks **Apply**; the other side follows.
5. Confirm nothing was lost while the choice was open.

## Frozen outcome thresholds

From the test plan §13. `<LFCP-02-005 re-derives the exact counts for 3–5
pairs; the owner freezes them at M02-0/M02-1. Never adjust a threshold
silently to turn a failing result green.>`

- At least **10 observed end-to-end onboarding attempts** across the pilot;
  at least **8 completed without developer intervention** using the supplied
  instructions.
- **Every participating pair** completes a two-vault edit/reconnect cycle.
  Unexplained missing or duplicated content is investigated as a **blocker**.
- At least **8 of 10 short comprehension checks** correctly distinguish:
  the **shared boundary**, **local-save vs. server-acceptance**, **detach**,
  and **access removal**. Record which concept failed, not just a
  satisfaction score.
- **No unresolved blocker or major defect**; **no private-content
  publication** and **no unrecoverable data loss**.

If a target fails, fix the cause and repeat the affected observation.
Unmet targets become explicit blockers for final qualification
(LFCP-02-076).

## What is recorded per pair

Anonymised and minimal (see [pilot-consent.md](pilot-consent.md) and
[pilot-feedback-form.md](pilot-feedback-form.md)):

- **Anonymised pair ID** (e.g. `P1`, `P2`), and a per-person tag within it.
- **Build ID**: the exact build each person ran (`0.4.0-beta.18`, or a later
  beta if the facilitator gave one).
- **OS and Obsidian version** per person.
- Per workflow: outcome, elapsed time, whether intervention was needed, and
  an issue code if any.
- Comprehension-check results (which concept, pass/fail).
- Optional sanitised free-text feedback, and user-previewed "Export
  diagnostics…" output when a defect needs it.

**Never collected:** vault content, note text, file names or paths,
invitation links or secrets, keys, or a participant directory. No automatic
vault upload.

## Roles and support

- **Facilitator:** `<owner or named helper>` runs onboarding, records
  observations, and gives help only when a pair is blocked (recording that
  help counts against the "without developer intervention" target).
- **Support channel:** `<support contact placeholder>` (see
  pilot-install-guide.md).
- **Safety:** on any suspected unsafe projection or publication, stop the
  affected path with a tested mechanism and show an honest blocked state;
  do not wipe caches or regenerate identity to make the UI look healthy
  (test plan §15).

## Output

A **sanitised pilot report** per
[pilot-report-template.md](pilot-report-template.md), plus actionable
findings. Completion records observation, not release approval.
