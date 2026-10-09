# MVP 0.2 pilot operations (LFCP-02-103)

> **DRAFT for the owner's review.** Placeholders in angle brackets
> (`<SUPPORT_CHANNEL>`, `<FEEDBACK_FORM>`, `<COORDINATOR>`, dates and
> durations) are for the owner to fill in. No participant, name or contact
> appears in this document, and none should be added to it: the pilot
> keeps its participant list privately (section 2).

This is the protocol and the materials for the opt-in pair pilot of shared
sections:

- recruiting;
- the consent text;
- what is collected and what never is;
- the feedback form;
- installing the beta;
- the support channel;
- how a participant sends diagnostics;
- the support runbook.

The pilot itself, with its outcome targets, is
[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md)
§13 (decision V2). Running it and reporting on it is LFCP-02-075.

## 1. Shape of the pilot

- **3 to 5 pairs.** Each pair is two people, each with their own vault and
  their own computer. At least two of the participants are not developers.
- **At least 7 days** of ordinary use per pair, after an onboarding session.
- **At least two pairs** use a section of real size, roughly 100 to 200
  tasks with notes under them.
- **A pre-release build** of Shared Tasks, installed through BRAT (LFCP-02-094).
  An early dogfood of 2 to 3 pairs comes first (LFCP-02-105).
- **The default sync server**, or `<PILOT_SERVER>` if the owner chooses a
  separate one.
- **A small product check**, not a statistical study. Nobody is asked to
  share sensitive personal notes.

Each pair works through the flows of plan §13:

- share a section, and join it;
- add content under it;
- edit offline, then reconnect;
- look at the status and at who has access;
- copy readable text;
- detach one copy.

During onboarding, each pair also works through one conflict and its
recovery on a synthetic note, never on a valuable one.

## 2. Recruiting

**Who:** people who already use Obsidian with tasks, in pairs that really
share work: colleagues, a household, a club, a study group. A pair can be a
developer and a non-developer.

**What we ask of them:**

- an onboarding session of about `<ONBOARDING_MINUTES>` minutes;
- ordinary use for 7 days;
- a short feedback form at the end, and one optional mid-point check-in;
- reporting problems through `<SUPPORT_CHANNEL>`.

**Before the pilot, the coordinator records for each pair, outside any
repository:**

- a pair label (`P1` to `P5`);
- each participant's role (developer or not);
- the OS, and the Obsidian and plugin versions;
- the start date.

Contact details stay with the coordinator, in `<PARTICIPANT_LIST_LOCATION>`.
They never go into an issue, a report or this repository. Reports name
pairs only by their label.

**The invitation to participate** (to adapt, then send privately):

> We are testing a new feature of the Shared Tasks plugin for Obsidian:
> sharing a whole section of a note (a heading with its tasks and notes)
> with one other person, end-to-end encrypted. We are looking for pairs who
> would use it for a week on real but non-sensitive work. It takes about
> `<ONBOARDING_MINUTES>` minutes to set up together with us, then ordinary
> use, and a short form at the end. The plugin is beta software: keep a
> backup of your vault, and don't use it for data you need to protect. Your
> notes never leave your devices unencrypted, and we never ask for them.

## 3. Consent text

The participant reads this before onboarding and agrees to it in writing:
`<CONSENT_RECORD_METHOD>`, for example a reply to the coordinator.

> **Shared Tasks pilot: what you agree to**
>
> 1. **This is a test of beta software.** It may have bugs. Keep a backup
>    of your vault, and don't put data you need to protect in a shared
>    section during the pilot.
> 2. **What is shared, and with whom.** A section you share goes, end-to-end
>    encrypted, to the sync server and to the person you invite. The server
>    cannot read it. The server's privacy note
>    ([sync-server-privacy.md](sync-server-privacy.md)) says what the server
>    does see: encrypted data, public keys, sizes, and your IP address
>    when you connect.
> 3. **What we collect from you.** Only what you choose to tell us: your
>    answers to the feedback form, what you tell the support channel, and a
>    diagnostics report when you choose to send one. You see its full text
>    before it leaves your computer.
> 4. **What we never collect.** Your notes, your task text, file or note
>    names, your vault, your keys, your invitation links. Never send them
>    to us, not even to explain a problem. If you do by mistake, tell us,
>    and we will delete it.
> 5. **No tracking.** The plugin has no telemetry. Nothing is sent to us
>    automatically.
> 6. **How long we keep it.** Pilot records are kept until
>    `<RETENTION_END>`, then deleted. Results are reported only in summary,
>    by pair label (P1 to P5), never by name.
> 7. **You can stop at any time,** without giving a reason. Stopping does
>    not delete your notes. To stop sharing, remove the other person's
>    access, or detach the section in your note. To have your pilot
>    records deleted, tell `<SUPPORT_CHANNEL>`.

## 4. What is collected, and what never is

| Collected (only with consent, only what the participant sends) | Never collected |
| --- | --- |
| Pair label, role (developer or not), OS, Obsidian and plugin versions | Names or contacts in any record outside the coordinator's private list |
| Workflow outcome per step (done / needed help / failed), elapsed time | Note or task text, titles, section or collaboration names, file paths |
| Help given during onboarding (what, how long) | Vaults or any vault file, automatically or on request |
| Issue codes and status states, as the diagnostics report shows them | Invitation links or their secrets, keys, server credentials |
| Answers to the feedback form, optional free text | Screenshots of private notes; only synthetic notes may be shown |
| A diagnostics report the participant previewed and chose to send | Anything gathered automatically: there is no telemetry |

If a participant sends forbidden content anyway, follow the runbook
(section 8, "Private content received").

## 5. Minimal feedback form

`<FEEDBACK_FORM>` (a form or a plain message, at the end of the 7 days).
Every question is optional.

1. Pair label, and your role (developer or not).
2. For each flow, say whether you did it without help, did it with help,
   or could not do it: share a section, join, add content, edit offline and
   reconnect, look at status and access, copy readable text, detach one
   copy.
3. Comprehension check. Please answer in your own words:
   - a. What part of your note is shared, and what stays private?
   - b. What does the double tick next to the heading mean, and what does
     the sync icon beside it tell you?
   - c. What happens to the other person's copy when you detach the section
     in your note?
   - d. What changes when you remove someone's access, and what does it not
     undo?
4. Did anything go missing, appear twice, or change unexpectedly? When,
   and what did you do?
5. Did you ever have to ask for help? With what?
6. Anything else (optional, no note content please).

The answers to question 3 are scored against plan §13: which concept was
misunderstood, not a single score.

## 6. Installing the beta, and onboarding

Installing (each participant, in their own vault):

1. Make a backup of the vault.
2. Install the pre-release through BRAT: the plugin
   [README](https://github.com/openlfcp/obsidian#install), "Pre-release
   builds, with BRAT". The pilot build is `<PILOT_BUILD_VERSION>`.
3. Turn on shared sections: the
   [shared sections guide](https://github.com/openlfcp/obsidian/blob/main/docs/guides/shared-sections.md),
   section 1.
4. In Settings → Shared Tasks, check that "Identity on this device" reads
   "Ready".

Onboarding happens together, in a call or in person. It uses a synthetic
note created for the session, never a real one:

1. Share a heading's section from the synthetic note, invite the partner,
   who joins and inserts it.
2. Both add and edit content, and watch the other's changes arrive.
3. One goes offline, both edit, then reconnect.
4. Make a conflict on purpose: both move the same task to different places
   while offline. Resolve it with "Review conflicts…".
5. Look at the details card: status, and who has access.
6. Copy readable text. Detach one copy, in a second note, and see that the
   other copy keeps syncing.

The coordinator records each step's outcome and the help given.

## 7. Support, and sending diagnostics

**Support channel:** `<SUPPORT_CHANNEL>`, watched by `<COORDINATOR>`, with
a first answer within `<RESPONSE_TARGET>` on working days. Security
problems go to the security contact in the plugin README, never to a
public channel.

**Sending diagnostics, for the participant:**

1. In Obsidian, run **"Export diagnostics…"** from the command palette.
2. Read the report in the preview. It holds versions, states, codes and
   counts. It leaves out note and task text, titles, names, paths, keys and
   invitation links; collaborations and sections are numbered, not named.
3. Leave **"Include identifiers and server addresses" unticked**, unless
   support asks for it.
4. Press **Copy** and paste the text into `<SUPPORT_CHANNEL>`, or **Save as
   file** and attach the `.txt` file.

Never send invitation links, note text, screenshots of real notes, or vault
files, even when asked by someone claiming to be support.

## 8. Support runbook

For the coordinator, for each report:

1. **Acknowledge** within `<RESPONSE_TARGET>`. Assign the report an ID
   (`P<n>-<k>`).
2. **Classify it:**

   | Class | Examples | Response |
   | --- | --- | --- |
   | Blocker | Content lost, duplicated or appearing where it should not; private text published; the plugin does not start | Same day; ask the pair to stop using the shared section and keep their vaults as they are |
   | Major | A flow cannot be completed; a conflict cannot be resolved; access removal does not take effect | Within `<MAJOR_TARGET>` |
   | Minor | Confusing wording, slow but working, a cosmetic issue | Collected for the end-of-pilot report |

3. **Ask for a diagnostics report** if the problem is not obvious (section
   7). Ask only for codes, states and steps, never for content.
4. **Reproduce with synthetic content**, on the coordinator's own vaults,
   from the steps and the codes.
5. **Record the outcome** in the pilot record, by pair label and report ID:
   - the issue code;
   - the help given;
   - whether the participant could continue.
6. **Escalate defects:** open an issue in the repository concerned, with
   synthetic reproduction steps only. A blocker or major defect becomes an
   explicit blocker for final qualification (LFCP-02-075, 076).

**Private content received** (note text, an invitation link, a key, a
vault file):

1. Delete it from the channel and from any copy, at once.
2. Tell the participant what was received and that it was deleted.
3. If it was an invitation link that has not been used, ask the inviter to
   remove that invitation's access and create a new one.
4. Record the incident in the pilot record without its content, and
   mention it in the pilot report.

**Stopping rule.** Pause the pilot for every pair if any of these happens:

- private content is published to someone who should not see it;
- data is lost and cannot be recovered;
- the same blocker appears in two pairs.

Fix the cause, then resume. Plan §13 asks to repeat the affected
observation.

## 9. Records, retention and the end of the pilot

- The pilot record is `<PILOT_RECORD_LOCATION>`, private. It holds:
  - per pair, its label, roles, versions and dates;
  - per flow, its outcome and the help given;
  - the comprehension answers;
  - the support report IDs, with their classes and codes.

  It holds no names, contacts or content.
- At the end, the coordinator writes the sanitized pilot report (LFCP-02-075),
  by pair label only.
- Participants are told when the pilot ends, and how to keep or stop
  sharing. Their records are deleted at `<RETENTION_END>`.

## 10. Before the pilot starts (owner)

- [ ] Fill in every placeholder in this document.
- [ ] Approve the consent text (section 3) and the feedback form (section 5).
- [ ] Choose the support channel and who watches it.
- [ ] Publish the BRAT pre-release (LFCP-02-094), and record its version.
- [ ] Create the synthetic onboarding note and the coordinator's two test
      vaults.
- [ ] Re-derive the outcome targets of plan §13 for 3 to 5 pairs
      (LFCP-02-005).
- [ ] Record the pairs privately, then start.
