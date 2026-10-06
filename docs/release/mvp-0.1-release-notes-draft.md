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
`spec: mvp-0.1-baseline.8`. It is not a full LFCP-WIRE-01 implementation; the
deferred features are listed in
[deferred-wire-01-features.md](deferred-wire-01-features.md). The
specifications remain Working Drafts.

> MVP reference software: not for data you need to protect.

## Components

| Repository | Version | What it provides |
| --- | --- | --- |
| `spec` | `mvp-0.1-baseline.8` (da3977f); 509c1c1 adds the owner's ADR approvals | LFCP-WIRE-01, SHARED-OBJECTS-PROFILE-01 and MARKDOWN-REFS-01 (Working Drafts); test vectors, the Automerge reference corpus, schemas; ADRs 0001–0007 |
| `sdk-ts` | npm `0.1.0-rc.1` (98efaab) | The TypeScript SDK: core, crypto, wire, storage (memory, IndexedDB, Node), Shared Objects on Automerge, the sync client with invitations, Key Packages, Snapshots and epoch rotation |
| `sdk-rs` | 41dc532 | An independent Rust implementation of the protocol core and the Shared Objects profile (feature `shared-objects`) |
| `server` | e84fa74 | The reference LFCP server in Rust: WebSocket sessions, Control Coordinator, durable SQLite store, first-run pairing; never decodes Shared Objects |
| `obsidian` | 3cc9915 | The Obsidian plugin: Markdown ↔ Shared Object projection and the collaboration commands |
| `examples` | fe3de90 | `lfcp-todo` (a headless client) and the cross-language conformance harness |

These are the commits of release candidate rc6
([rc6-manifest.json](rc6-manifest.json)): all eight local release gates
pass ([rc-verification.md](rc-verification.md)), and GitHub CI is green
on every one of them, the server's Windows job and the plugin's platform
smoke on macOS, Windows and Linux included.

The sdk-ts packages (`@openlfcp/core`, `crypto`, `storage`, `wire`,
`storage-node`, `storage-idb`, `shared-objects`, `client`) are on npm as
`0.1.0-rc.1`, published by hand by the owner on 2026-10-06 from sdk-ts
98efaab, under the dist-tag `next`. As their first publish, npm also set
`latest` to it; `0.1.0` will take `latest` when MVP 0.1 is final. See
[npm-publish-checklist.md](npm-publish-checklist.md).

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
- Automerge input is bounded before the engine sees it, in both SDKs
  (Shared Objects §11.1, §11.2, §13.1; baseline.7 and baseline.8):
  - a change is one uncompressed chunk within exact limits (16,384
    values per column, 262,144 predecessor entries, 4 MiB of strings,
    1,024 dependencies and other actors), checked from its run headers
    without expanding them; writers send raw changes (H1);
  - a Snapshot is checked against local limits of at least 32 MiB and
    262,144 values, its deflated columns inflated under a running cap;
  - a change naming an actor the document lacks is refused;
  - no object of a document is deeper than 256 levels: Automerge JS traps
    about 6,500 levels below the root and stops for the whole process;
  - sdk-rs ca7f7f4, a3c7513, 18fe352, 50cb6bf; sdk-ts b6aa491, 68ce58d,
    and b110fdd, which stops a client from retrying content that traps
    the engine.
- A client keeps its receive limit under its own maximum (at least
  8 MiB), whatever the server's READY advertises (M1; sdk-rs b1d08bd,
  sdk-ts 9b61644), and asks for at most 256 epochs per
  `KEY_PACKAGE_GET` (sdk-ts 3069c33).
- Hardening from the pre-release review:
  - a `DATA_HAVE` announcing a huge span of sequences no longer hangs a
    client: Have ranges stay intervals end to end (H2; sdk-ts 9d5edf7,
    sdk-rs 6aab900);
  - a received change nesting maps thousands deep no longer overflows the
    sdk-rs stack. An object's values nest at most 64 levels; a deeper one
    is `INVALID_FIELD_TYPE` (M7; sdk-rs bb43a78);
  - merging another replica in sdk-rs goes through the same §14.1
    admission and engine guard as received changes (M8; sdk-rs b99f85c).
- Untrusted text is parsed in linear time. A collaborator's long Task title
  could freeze the Obsidian editor through super-linear Task-suffix
  regexes; the suffix, code spans and comments are now scanned in linear
  time (H3, M9; obsidian c73c46d, 0bded76). Writer URLs are checked in
  linear time too (sdk-ts af2954d).
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
  - A state directory the server creates is owner-only (0700), and the
    database files are 0600, tightened at every start (L5; server
    83f9a33). An existing directory, such as the Docker volume, keeps its
    mode.
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
  severity, what was fixed, what is routed, and the dependency audit:
  `pnpm audit` and `cargo audit` (RustSec, 1,290 advisories, 2026-10-06)
  find no vulnerability in sdk-ts, sdk-rs, the server or examples, and
  one moderate advisory in a development-only typings dependency of the
  plugin that is never bundled.
  H1–H4 are fixed, and H5 and H6 are accepted as known limitations
  (below).

## Known limitations

- Not full LFCP-WIRE-01. See
  [deferred-wire-01-features.md](deferred-wire-01-features.md).
- The protocol decisions in ADRs 0004 to 0007 were made by the
  orchestrator while the owner was away; the project owner approved them
  on 2026-10-06.
- Desktop platform smoke (macOS, Windows, Linux): _TBD_, LFCP-068. The CI
  matrix and the manual checklist exist; results are pending.
- The Docker deployment of the server is not yet verified end to end
  (_TBD_, LFCP-055).
- Mobile (iOS, Android) is not tested.
- sdk-rs copies a document once per apply call as rollback insurance; a
  batch of changes counts once, but a Data Unit applied on its own costs a
  copy. This is fine at MVP sizes.
- Two different Automerge changes with the same actor and sequence number
  are refused (`ACTOR_EQUIVOCATION`). That happens only after a writer
  equivocated or misbehaved. The refusal is safe: nothing is merged and
  nothing crashes. But in that rare case one replica stops showing that
  collaborator's later edits, with no notice. The project owner decided to
  ship this in MVP 0.1 and to adopt "hold and retry" in the next baseline:
  see [open-decision-actor-seq-collision.md](open-decision-actor-seq-collision.md).
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
  - **Windows: no owner-only state files.** On Windows the server does not
    tighten the permissions of its state files (server ID, setup code, the
    database): they inherit the state directory's ACL, so put the state
    directory where only the server's user can read it, such as under that
    user's profile. On Unix the directory is created 0700 and the files
    0600 (server 83f9a33; Windows start fixed in server 4cfa5f4).
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

A later spec baseline (`mvp-0.1-baseline.9` …) is adopted deliberately,
never by moving a tag.
