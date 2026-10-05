# OpenLFCP MVP 0.1: release notes (draft)

**Status:** DRAFT for LFCP-072. Not published; the owner decides wording,
date and version numbers. Items marked _TBD_ depend on work still open.

## What this is

OpenLFCP MVP 0.1 is a secure vertical slice of the Local-First
Collaboration Protocol. Two people share tasks from their Obsidian vaults:
- only the tasks they choose leave the vault;
- the tasks travel as end-to-end encrypted, signed LFCP Data Units through a
  self-hosted reference server that never sees their content;
- everything else in the notes stays local.

It implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01 at
`spec: mvp-0.1-baseline.6`. It is not a full LFCP-WIRE-01 implementation; the
deferred features are listed in
[deferred-wire-01-features.md](deferred-wire-01-features.md). The
specifications remain Working Drafts.

> MVP reference software: not for data you need to protect.

## Components

| Repository | Version | What it provides |
| --- | --- | --- |
| `spec` | `mvp-0.1-baseline.6` (c13aef1) | LFCP-WIRE-01, SHARED-OBJECTS-PROFILE-01 and MARKDOWN-REFS-01 (Working Drafts); test vectors, the Automerge reference corpus, schemas; ADRs 0001–0005 |
| `sdk-ts` | _TBD_ (c074ed0 or later) | The TypeScript SDK: core, crypto, wire, storage (memory, IndexedDB, Node), Shared Objects on Automerge, the sync client with invitations, Key Packages, Snapshots and epoch rotation |
| `sdk-rs` | _TBD_ (7ae47c4 or later) | An independent Rust implementation of the protocol core and the Shared Objects profile (feature `shared-objects`) |
| `server` | _TBD_ (6e2dce6 or later) | The reference LFCP server in Rust: WebSocket sessions, Control Coordinator, durable SQLite store, first-run pairing; never decodes Shared Objects |
| `obsidian` | _TBD_ | The Obsidian plugin: Markdown ↔ Shared Object projection and the collaboration commands |
| `examples` | _TBD_ | `lfcp-todo` (a headless client) and the cross-language conformance harness |

## Highlights

- **No plaintext mode.** Every change travels as a Data Unit:
  - ChaCha20-Poly1305 under a per-actor key derived from the Resource's
    DEK;
  - signed with Ed25519 (strict verification), in canonical COSE.
  The server stores and forwards opaque bytes, and tests check that task
  text never appears in what it stores.
- **Signed Control Plane.** Genesis, grants, revocations, Key Epochs and
  claims form a linear signed chain. Clients evaluate every capability
  themselves, and forks are detected and block security-sensitive actions.
- **Invitations.**
  - One-time `lfcp://join/…` links with Read or Read + Write.
  - The joining device claims access through the coordinator and receives
    the key by HPKE.
  - The link is a bearer secret, and the UI never logs or stores it.
- **Revocation and key rotation.** Revoking a reader starts a new Data
  Epoch. Writes from beyond the cutoff are quarantined everywhere.
- **Local-first.** Edits work offline and sync when the server is
  reachable. Restarts never reuse an actor sequence.
- **Markdown stays Markdown.**
  - A shared task is an ordinary task line with an `lfcp-ref` comment, on a
    child line by default.
  - Only owned fields sync: title, status, dates, priority, tags.
  - Edits change the smallest possible span, line endings are kept, and
    conflicts show beside the text, never inside it.
- **Two interoperable SDKs.** sdk-ts and sdk-rs pass the official vectors
  and exchange fresh objects in every direction. The compatibility matrix
  is `docs/conformance/compatibility-matrix.md`.

## Obsidian commands

Create collaboration · Join collaboration · Share task under cursor ·
Insert shared object · Invite collaborator · Resource status · Detach
shared task · Resolve shared task conflict

## Security notes

- A crafted Automerge change that skipped its actor's next sequence number
  could crash an sdk-rs receiver, and corrupt a JS document. It is now
  rejected before the engine (Shared Objects §14.1, baseline.6) in both
  SDKs.
- The server is a synchronization peer, not the root of trust. Clients
  verify signatures, capabilities, epochs and AEAD themselves.
- The pre-release security review is
  [security-review-mvp-0.1.md](security-review-mvp-0.1.md): findings by
  severity, what was fixed, what is routed, and the dependency audit.
  _TBD_: the high findings still open (H1–H6) are fixed or accepted before
  release.

## Known limitations

- Not full LFCP-WIRE-01. See
  [deferred-wire-01-features.md](deferred-wire-01-features.md).
- Several protocol decisions in ADR 0004 and ADR 0005 are orchestrator
  decisions pending the owner's review.
- Desktop platform smoke (macOS, Windows, Linux): _TBD_, LFCP-068. The CI
  matrix and the manual checklist exist; results are pending.
- The Docker deployment of the server is not yet verified end to end
  (_TBD_, LFCP-055).
- Mobile (iOS, Android) is not tested.
- sdk-rs copies a document once per received change as rollback insurance.
  This is fine at MVP sizes; optimizing it is a follow-up.
- Invitations are copied as links; there is no QR code. A copied link
  stays on the system clipboard.
- The reference server has no connection limits, rate limits or storage
  quotas yet, and hosting is open by default. Run it for known users with
  the allow-list hosting policy, behind the Caddy proxy (see the security
  review).
- Decrypted shared tasks are stored unencrypted on each device (IndexedDB
  or SQLite), and Obsidian's `secretStorage` is shared by every plugin on
  the device.

## Upgrading

This is the first release; there is nothing to upgrade from. Pins are
explicit everywhere:
- `spec.lock` in each implementation;
- `sdk-ts.lock` in the plugin;
- `sdk-rs.lock` in the server;
- `server.lock` in the plugin's CI.

A later spec baseline (`mvp-0.1-baseline.7` …) is adopted deliberately,
never by moving a tag.
