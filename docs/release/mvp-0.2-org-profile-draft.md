# Organization profile for MVP 0.2 (draft)

**Status:** DRAFT for LFCP-02-079, not published. At the MVP 0.2 release,
the owner replaces the body of `profile/README.md` with the text below the
line, once the release, the website and the links it names exist.
`profile/README.md` is what GitHub shows on the organization page, so it is
not edited before then. `<TBD>` marks what the release settles.

Changes from the current profile:

- the tagline and the summary now include sections;
- "What works today" becomes MVP 0.2, and keeps a link to the MVP 0.1 notes;
- the plugin is in the Community Plugins directory now; the current text says
  it is not;
- demo and guide links for sections are added;
- unsupported or later features are listed separately.

The Feedback section is unchanged.

---

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark-dark.svg"><img src="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark.svg" width="96" height="96" alt="OpenLFCP"></picture></p>
<h1 align="center">OpenLFCP</h1>

**Shared tasks and sections inside your private notes.**

**Website:** [openlfcp.org](https://openlfcp.org)

OpenLFCP (Open Local-First Collaboration Protocol) is an open protocol and
reference stack for **local-first collaboration**. It starts with Obsidian.
You keep your vault on your own device, and choose what to share: one task,
or a whole section of a note with its tasks, subtasks and notes. The other
person keeps it in a note of their own, and you both edit it. Only what you
shared leaves the device, end-to-end encrypted and signed. The sync server
relays the changes and cannot read them.

```text
 Alice's vault                                         Bob's vault
 ┌──────────────────────┐                            ┌──────────────────────┐
 │ private notes …      │   encrypted, signed        │ … his own notes      │
 │ ## Launch plan  ✓✓ ◄─┼──── changes ──► server ◄───┼─► ## Launch plan  ✓✓ │
 │ - [ ] API contract   │   (relays, can't read)     │ - [x] API contract   │
 │ more private text    │                            │ private text         │
 └──────────────────────┘                            └──────────────────────┘
```

## What works today: MVP 0.2

[Release notes](https://github.com/openlfcp/.github/blob/main/docs/release/mvp-0.2-release-notes.md)
· [MVP 0.1](https://github.com/openlfcp/.github/blob/main/docs/release/mvp-0.1-release-notes.md)

- **Share a task, or a whole section of a note**, with its tasks, subtasks,
  paragraphs and lists. What is added inside a section later is shared too,
  and the text around it stays private.
- Invite someone with a one-time link. They see your changes in their own
  note, and you see theirs.
- Encryption is always on, and access is capability-based: no accounts.
  Removing someone's access rotates the key. It cannot erase copies they
  already have.
- It works offline. Conflicts are shown as choices for you, never written
  into your text.
- Your device's sync data is encrypted at rest. A diagnostics report shows
  you everything before anything leaves the device.
- The TypeScript and Rust SDKs pass the same conformance vectors.

This is early reference software and the specifications are Working Drafts.
**Don't use it yet for data you need to protect.** The release notes list
what was verified and what is still open.

## Two ways in

**Obsidian users:** [`obsidian`](https://github.com/openlfcp/obsidian), the
**Shared Tasks** plugin.

- Install it from Community plugins
  ([directory page](https://obsidian.md/plugins?id=shared-tasks)).
- Read the guides:
  - the [step-by-step guide](https://github.com/openlfcp/obsidian/blob/main/docs/guides/user-guide.md);
  - [Shared sections](https://github.com/openlfcp/obsidian/blob/main/docs/guides/shared-sections.md).
- Try the [two-vault demo](https://github.com/openlfcp/obsidian/blob/main/docs/demos/two-vault-demo.md)
  with a server you run yourself.

**Developers:**

- [`spec`](https://github.com/openlfcp/spec): the LFCP protocol, the Shared
  Objects and Shared Sections profiles, and the test vectors.
- [`sdk-ts`](https://github.com/openlfcp/sdk-ts), published as
  [`@openlfcp/*`](https://www.npmjs.com/org/openlfcp) on npm, and
  [`sdk-rs`](https://github.com/openlfcp/sdk-rs).
- [`server`](https://github.com/openlfcp/server): a self-hosted sync server
  (Docker and Caddy).
- [`examples`](https://github.com/openlfcp/examples):
  - a CLI client that reads and writes shared sections;
  - the two-vault section demonstration;
  - the TS↔Rust conformance harness.

## Not yet

- Shared sections on mobile: read-only, or marked unsupported.
  `<TBD: as implemented, LFCP-02-095>`
- Moving a collaboration to another server.
- Comments and discussion threads inside a section.
- A full LFCP-WIRE-01 implementation. MVP 0.2 implements its MVP subset.

## Feedback

Bug reports and ideas go in the issues of the repository concerned. Read
[CONTRIBUTING](https://github.com/openlfcp/.github/blob/main/CONTRIBUTING.md)
before you start. Report vulnerabilities privately, as described in
[SECURITY](https://github.com/openlfcp/.github/blob/main/SECURITY.md).
Everything is licensed under Apache-2.0.
