<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark-dark.svg"><img src="https://raw.githubusercontent.com/openlfcp/.github/main/docs/assets/brand/openlfcp-mark.svg" width="96" height="96" alt="OpenLFCP"></picture></p>
<h1 align="center">OpenLFCP</h1>

**Shared tasks inside your private notes.**

**Website:** [openlfcp.org](https://openlfcp.org)

OpenLFCP (Open Local-First Collaboration Protocol) is an open protocol
and reference stack for **local-first
collaboration**. It starts with Obsidian. You keep your vault on your own
device and choose single objects to share, such as one task. The same task
can then live in different notes, in different people's vaults. Only that
task leaves the device, end-to-end encrypted and signed. The sync server
relays the changes and cannot read them.

```text
 Alice's vault                                         Bob's vault
 ┌──────────────────────┐                            ┌──────────────────────┐
 │ private notes …      │   encrypted, signed        │ … his own notes      │
 │ - [ ] API contract ◄─┼──── changes ──► server ◄───┼─► - [x] API contract │
 │ more private text    │   (relays, can't read)     │ private text         │
 └──────────────────────┘                            └──────────────────────┘
```

## What works today: MVP 0.1

[Release notes](https://github.com/openlfcp/.github/blob/main/docs/release/mvp-0.1-release-notes.md)

- Share a task from a note, invite someone with a one-time link, and see
  their changes in your own note.
- Encryption is always on, and access is capability-based: no accounts,
  revocation rotates the key.
- It works offline. Conflicts are shown next to the task, never written
  into your text.
- The TypeScript and Rust SDKs pass the same conformance vectors.

This is early reference software and the specifications are Working Drafts.
**Don't use it yet for data you need to protect.** The release notes list
what was verified and what is still open.

## Two ways in

**Obsidian users:** [`obsidian`](https://github.com/openlfcp/obsidian).
- Try the [two-vault demo](https://github.com/openlfcp/obsidian/blob/main/docs/demos/two-vault-demo.md)
  with a server you run yourself.
- The plugin is not in the Community Plugins directory yet. A beta is
  coming.

**Developers:**
- [`spec`](https://github.com/openlfcp/spec): the LFCP protocol, the Shared
  Objects profile and the test vectors.
- [`sdk-ts`](https://github.com/openlfcp/sdk-ts), published as
  [`@openlfcp/*`](https://www.npmjs.com/org/openlfcp) on npm, and
  [`sdk-rs`](https://github.com/openlfcp/sdk-rs).
- [`server`](https://github.com/openlfcp/server): a self-hosted sync server
  (Docker and Caddy).
- [`examples`](https://github.com/openlfcp/examples): a CLI demo and the
  TS↔Rust conformance harness.

## Feedback

Bug reports and ideas go in the issues of the repository concerned. Read
[CONTRIBUTING](https://github.com/openlfcp/.github/blob/main/CONTRIBUTING.md)
before you start. Report vulnerabilities privately, as described in
[SECURITY](https://github.com/openlfcp/.github/blob/main/SECURITY.md).
Everything is licensed under Apache-2.0.
