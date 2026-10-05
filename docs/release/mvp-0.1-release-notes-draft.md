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

## Demos

- **Two vaults in real Obsidian** (obsidian 3a4f935): Alice and Bob share
  one Task between two vaults through the reference server. Walkthrough:
  `obsidian: docs/demos/two-vault-demo.md`. `node scripts/demo-vaults.mjs`
  (0a9ad70) prepares both vaults outside the repository. The same
  storyline runs as the two-vault E2E, and prints a narrated reference
  transcript with:

  ```sh
  LFCP_REQUIRE_LIVE=1 LFCP_E2E_NARRATE=1 pnpm vitest run test/e2e/two-vaults.test.ts --reporter=verbose
  ```
- **Headless Todo** (examples 2ca182f): one command runs the whole
  storyline with `lfcp-todo`, prints a readable transcript and checks the
  outcome. See `examples: docs/demos/headless-todo.md`.

## Security notes

- A crafted Automerge change that skipped its actor's next sequence number
  could crash an sdk-rs receiver, and corrupt a JS document. It is now
  rejected before the engine (Shared Objects §14.1, baseline.6) in both
  SDKs.
- Hardening from the pre-release review:
  - a `DATA_HAVE` announcing a huge span of sequences no longer hangs a
    client: Have ranges stay intervals end to end (H2; sdk-ts 9d5edf7,
    sdk-rs 6aab900);
  - a received change nesting maps thousands deep no longer overflows the
    sdk-rs stack. An object's values nest at most 64 levels; a deeper one
    is `INVALID_FIELD_TYPE` (M7; sdk-rs bb43a78);
  - merging another replica in sdk-rs goes through the same §14.1
    admission and engine guard as received changes (M8; sdk-rs b99f85c).
- Server hardening (the full list is in the security review, "Follow-up:
  server hardening"):
  - `DATA_GET` with more than 256 ranges and `KEY_PACKAGE_GET` with more
    than 256 distinct epochs are refused (`MALFORMED_MESSAGE`) before any
    lookup. Repeated epochs and overlapping ranges are read once (H4;
    server eb1323f).
  - A connection that is not `READY` within `handshake_timeout_ms`
    (default 10 s) is closed, and `PING` does not extend the deadline.
    Before `READY`, a connection may send at most 16 messages, none of
    them decoded beyond 64 KiB. HTTP headers have a read timeout (M2, M5;
    server 65f148d).
  - `max_connections` (default 1024) caps concurrent connections. Past
    it, the server answers HTTP 503 with `Retry-After` (M2; server
    625dbd9).
  - At most 1024 admin challenges are outstanding, each for 5 minutes;
    past that, the server answers 429 (M3; server a7f3461).
  - Coordinator slots exist only for hosted Resources (M4; server
    11e1fb2).
  - The first-run pairing code is written to `<state_dir>/setup-code`
    (mode 0600), never to stdout or the Docker logs (M6; server 7e61710).
    Under Docker, read it with:

    ```sh
    docker compose -f deploy/compose.yaml cp lfcp-server:/var/lib/lfcp/setup-code - | tar -xO
    ```
- The server is a synchronization peer, not the root of trust. Clients
  verify signatures, capabilities, epochs and AEAD themselves.
- The pre-release security review is
  [security-review-mvp-0.1.md](security-review-mvp-0.1.md): findings by
  severity, what was fixed, what is routed, and the dependency audit.
  H2 and H4 are fixed, and H5 and H6 are accepted as known limitations
  (below). _TBD_: H1 and H3 are fixed or accepted before release.

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
- sdk-rs copies a document once per apply call as rollback insurance; a
  batch of changes counts once, but a Data Unit applied on its own costs a
  copy. This is fine at MVP sizes.
- Invitations are copied as links; there is no QR code. A copied link
  stays on the system clipboard.
- The reference server is for known users. Run it with the allow-list
  hosting policy, behind the Caddy proxy (see the security review):
  - Hosting is open by default, and there are no storage quotas (H5).
  - Replies to `DATA_GET`, `KEY_PACKAGE_GET` and `CONTROL_GET` are built
    fully in memory, not streamed. The outbound queue counts messages, not
    bytes: up to 256 × `max_message_bytes` per connection (H6).
  - After `READY`, a message is decoded in full, up to
    `max_message_bytes` (M5).
  - There are no rate limits on WebSocket sessions or the admin HTTP API.
    The connection cap is global, not per IP; use the proxy's limits.
  - Admin request bodies (at most 16 KiB) have no read timeout of their
    own.
  - An unauthenticated flood can fill the admin challenge cap and delay an
    administrator's login by up to 5 minutes.
  - The database files are not restricted to the owner (L5).
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
