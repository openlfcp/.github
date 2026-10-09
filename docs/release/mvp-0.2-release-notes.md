# OpenLFCP MVP 0.2: release notes

**Status:** DRAFT (LFCP-02-093), not released. `<TBD>` marks what the final
candidate (LFCP-02-073) and the owner still have to settle: commits, the
spec tag, the server version and the release date.

## What this is

MVP 0.2 adds **shared sections** to OpenLFCP. Two people share a whole part
of a note: a heading and everything under it, its tasks, subtasks,
paragraphs and lists, in order. Each keeps the section in a note of their
own, and both edit it. What either of them adds inside it is shared too,
and the text around it stays private.

As in MVP 0.1:

- every change travels as an end-to-end encrypted, signed LFCP Data Unit;
- the sync server relays changes it cannot read;
- the shared tasks of MVP 0.1 keep working unchanged, beside the sections.

It implements the OpenLFCP MVP 0.2 subset of LFCP-WIRE-01 at
`spec: mvp-0.2-baseline.<N>` `<TBD: N, currently 3>`. That is MVP 0.1's
`mvp-0.1-baseline.10` unchanged, plus the shared sections profile. MVP 0.2
adds no Wire feature. The specifications remain Working Drafts; the deferred
Wire features are in
[deferred-wire-01-features.md](deferred-wire-01-features.md).

> MVP reference software: not for data you need to protect.

## Components

| Repository | Version | What it provides |
| --- | --- | --- |
| `spec` | `mvp-0.2-baseline.<N>` (`<TBD: commit>`) | SHARED-SECTIONS-PROFILE-01 (ADR 0009), MARKDOWN-SECTIONS-01, SDK-SECTIONS-INTEGRATION-01, the canonical change encoding and operation references (ADR 0010), the shared sections corpus and the Markdown fixtures; MVP 0.1's files unchanged |
| `sdk-ts` | npm `0.2.0` (`<TBD: commit>`) | The shared sections profile (`@openlfcp/shared-objects/sections`), batches with durable receipts and statuses (`SyncClient.commit`), status events and access state, local state encrypted at rest |
| `sdk-rs` | `v0.2.0` (`<TBD: commit>`) | The shared sections profile (feature `shared-sections`), the canonical change and reference checks, admission fuzzers |
| `obsidian` | Shared Tasks `0.4.0` (`<TBD: commit>`) | Shared sections in notes, beside 0.3's shared tasks: [0.4.0 notes](https://github.com/openlfcp/obsidian/blob/main/docs/releases/0.4.0.md) |
| `examples` | `v0.2.0` (`<TBD: commit>`) | `lfcp-todo` with section commands, the secure two-vault qualification, the two-vault demonstration and its reviewer checklist, the cross-language conformance run |
| `server` | `<TBD: 0.3.0 unchanged, or 0.3.1>` | The reference server. It never decodes sections. Since 0.3.0 its only code change is LFCP-02-116: it refuses a store written by a newer server instead of opening it (server e49f595). Whether that ships as 0.3.1 with MVP 0.2 is the owner's question (V1: "server only if changed") |

The pins of the final candidate are in `<TBD: rcN-manifest.json>`. Its
evidence is the release evidence record exported by rc-verify (LFCP-02-073).

## Highlights

- **Share a section, not a note.** "Share section…" previews exactly what
  will be shared, and what under the heading stays private. It then creates
  a collaboration of its own, with its own key: one Resource and one
  invitation per section (M9).
- **Nested content.** Tasks, subtasks, paragraphs and list items are shared
  with their order and nesting. Tables, callouts, fences and blockquotes
  travel as raw blocks (M6). Tasks keep the Obsidian Tasks syntax. A few
  Tasks-only tokens (🔁 🛫 ➕ ❌ 🔼) stay local (M7).
- **Markdown stays Markdown.** A section carries one comment after its
  heading, one at its end and one beside each item. Live Preview hides
  them; Source mode shows them (M5).
- **Status you can read.** A double tick next to a shared heading means
  "shared". A separate icon shows sync progress: saved here, sending,
  accepted, offline, or needs attention (M8). A details card shows who has
  access, as last verified with the server.
- **Conflicts are kept, not guessed.** A task moved to two places, or a
  field changed on both sides, shows as a choice in "Review conflicts…".
  Nothing is lost while it waits.
- **Access you can take back.** "Remove access…" removes someone's future
  access and rotates the key. A removed member's device says so, and their
  new edits stay with them (LFCP-02-115).
- **Local state encrypted at rest** on each device (LFCP-02-098).
- **Snapshots from the plugin.** A new member catches up from a Snapshot
  plus the tail, instead of the whole history (LFCP-02-097).
- **Diagnostics without your notes.** "Export diagnostics…" shows a report of
  versions, states and codes before anything leaves the device. It has no
  note text, names, paths, keys or invitation links (LFCP-02-065).
- **Recovery after a server restore.** A member refused before its grant was
  re-supplied recovers on its own (LFCP-02-106). The ADR 0008 repair of
  MVP 0.1's sustaining releases carries over.
- **Stricter admission.** A change must be in its canonical encoding and
  refer only to its own history (SPEC-PATCH-10, ADR 0010). Both SDKs refuse
  the rest, and the corpus checks it.

## Evidence

`<TBD: final candidate>` The reports so far, at the pins they name:

- Secure two-vault qualification, headless, at `mvp-0.2-baseline.2`: plan
  §7 steps 1–11, the negatives, server opacity
  ([mvp-0.2-two-vault-qualification.md](mvp-0.2-two-vault-qualification.md)).
- Integrated crash, access and compatibility recovery, headless part
  ([mvp-0.2-integrated-recovery-qualification.md](mvp-0.2-integrated-recovery-qualification.md)).
- Cross-language conformance, strict, in all four directions
  ([compatibility matrix](../conformance/compatibility-matrix.md)).
- sdk-ts against the full shared sections corpus
  ([mvp-0.2-sdk-ts-sections-conformance.md](mvp-0.2-sdk-ts-sections-conformance.md)).
- Plugin performance, headless, on macOS: W200 meets every budget of plan
  §10 (obsidian `docs/devel/reports/section-performance-headless.md`, §5).
- `<TBD>` Native acceptance in Obsidian (LFCP-02-066), the desktop matrix
  (LFCP-02-069), the restore rehearsal (LFCP-02-074) and the pilot
  (LFCP-02-075): results of the final candidate.

## Limits

- **Section size.** A section has no fixed size limit; a large one is
  shared in several parts. The qualified size is about 200 tasks with their
  notes (W200), on macOS. A section of 2,000 tasks works but blocks the
  editor for seconds per edit, and is not supported.
- **Long history.** A section after many thousands of edits (W200-H) is
  slower: an edit takes about half a second. The history growth policy is
  the owner's decision `<TBD: LFCP-02-112>`.
- **Mobile.** Sections are read-only on mobile (V3, LFCP-02-095): they are
  received and shown, and local edits stay on the device. Sharing, inviting
  and removing access are not offered there. The plugin stays available on
  mobile for shared tasks.
- **Platforms.** Performance budgets are measured on macOS only. Windows and
  Linux are functional but not performance-qualified (V4).
- **No nested headings** in a section in 0.2: sharing offers to split it.
- **Two moves into one parent** stay a conflict for a person to resolve (P5).
- **Public server quotas.** The public sync server limits each identity to
  20 collaborations, and 10 new ones per IP address per day. With one
  collaboration per section, this bounds how many sections one person
  shares there. `<TBD: B15, the owner sets or states the limits>`

## Known limitations

- **Removing access cannot erase copies** a person already received. It
  stops their future access, and the key rotates.
- **Shared tasks of 0.3 are not converted.** Moving them into a section is an
  explicit copy: the copy gets new identities, and the old collaboration
  continues separately (P1).
- **Gaps still open in the register**
  ([mvp-0.2-baseline-gaps.md](mvp-0.2-baseline-gaps.md)), `<TBD: status at
  release>`:
  - B12: manual smoke on Windows and Linux;
  - B13: IME input in sections, manual checklist;
  - B14: the plugin's beta channel;
  - B15: public server quotas;
  - B16: the restore test of the public server;
  - B17: the deployed server version, observable from outside;
  - B18: remaining section vectors;
  - B19: cross-language check of the epoch cutoff.
- The pair pilot is a small product check, not a statistical one
  (LFCP-02-075).

## Upgrading

- **From Shared Tasks 0.3.x.** Your shared tasks keep working as before.
  The first time 0.4 starts, it upgrades its sync data on the device: it is
  encrypted at rest, and earlier versions can no longer open it. The notes
  themselves are not changed.
- **Going back.** After updating to 0.4, a device cannot go back to 0.3.x,
  because its local sync data is upgraded and encrypted. Downgrade only to
  0.4.x or later. Your notes are not affected. If a 0.3.x plugin shows
  "Shared Tasks could not start: VersionError", that is why: install 0.4.x
  again, and its data is intact.
- **Mixed versions in a pair.** A 0.3.x device cannot join a shared section.
  It refuses before using the invitation and says a newer version is
  needed, so the link still works after updating. `<TBD: a 0.3.x and a 0.4
  device sharing the same 0.1 tasks, not yet recorded as tested>`
- **SDK users.** `@openlfcp/*` 0.2.0 reads and writes the storage of 0.1.x,
  and upgrades it to database version 2, which 0.1.x cannot open.
  `<TBD: confirm against the sdk-ts 0.2.0 changelog>`
- **Pins.** Pins are explicit everywhere:
  - `spec.lock` in each implementation;
  - `sdk-ts.lock` in the plugin during development, exact npm versions at
    release;
  - `sdk-rs.lock` in the server;
  - `server.lock` in the plugin and sdk-ts.

  A later spec baseline is adopted deliberately, never by moving a tag.
