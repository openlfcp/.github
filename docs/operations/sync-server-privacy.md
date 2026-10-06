# Privacy note: sync.openlfcp.org

**Status:** DRAFT, pending owner review. Not yet published. Bracketed
`[owner: …]` items are decisions the owner still has to make.

This note covers the public OpenLFCP sync server at
`wss://sync.openlfcp.org` and what it can learn about you. The server runs
the OpenLFCP reference server (`server`, version 0.1.0 at the time of
writing) behind nginx, on a small machine operated by the OpenLFCP project.
Contact: **abuse@openlfcp.org** (privacy and abuse).

Every claim below cites the code or the specification it comes from:
`server@v0.1.0: <path>:<line>` is the server repository at tag `v0.1.0`,
and `WIRE-01 §n` is `spec: wire/LFCP-WIRE-01.md` at `mvp-0.1-baseline.8`.
If a later server version changes any of this, this note changes with it.

## In one paragraph

Your tasks are end-to-end encrypted on your device before they leave it.
The server stores and forwards ciphertext it cannot decrypt, plus the
protocol metadata it needs to do its job: public keys, Resource IDs,
who may do what, sequence numbers and sizes. It also sees your IP address
when you connect. It never sees task text, the keys that decrypt it, or the
notes you did not share.

## What the server cannot see

- **Task content.** Changes travel as Data Units whose payload (field 6)
  is ChaCha20-Poly1305 ciphertext (WIRE-01 `data-unit-payload`,
  `spec: wire/LFCP-WIRE-01.md:1170-1180`). The server never decrypts and
  never holds a Data Encryption Key; Data Unit, Key Package and Snapshot
  ciphertexts stay opaque (`server@v0.1.0: crates/lfcp-server/src/ingest.rs:1-4`).
  The DEK is never stored in plaintext on the server (WIRE-01,
  `spec: wire/LFCP-WIRE-01.md:470`).
- **The keys.** Keys reach other members sealed by HPKE to their own
  public key (Key Packages); the server stores them but cannot open them
  (WIRE-01 §§ on Key Packages, `spec: wire/LFCP-WIRE-01.md:1097-1107`).
  Private keys stay on your device
  (`.github: docs/release/security-review-mvp-0.1.md:280-283`).
- **Invitation secrets.** The `#secret=` part of an invitation link must
  never be sent to the server (`spec: wire/LFCP-WIRE-01.md:848`); the server
  sees only the invitation's public key and the claim made with it
  (see below).
- **Everything you did not share.** Only the tasks you choose leave your
  vault; the rest of your notes stays local
  (`.github: docs/release/mvp-0.1-release-notes.md:9-12`). Names you give
  collaborations stay on your device too: the headless demo checks that no
  list name or item title appears in any server file
  (`examples: todo-cli/demo/demo.mjs:127`).

## What the server stores

The server keeps one SQLite database. Every protocol object is stored as
the exact signed bytes it received, next to index columns derived from
those bytes (`server@v0.1.0: crates/lfcp-server/src/store.rs:16-19`). The
tables (`server@v0.1.0: crates/lfcp-server/src/store/schema.rs`):

| What | Stored in the clear | Opaque | Where |
| --- | --- | --- | --- |
| Resources (a shared list or collaboration) | Resource ID, the ID of its first Control Record | — | `schema.rs:20-23` |
| Control Records (the signed membership chain) | issuer Principal ID, sequence number, type; and the whole body: the owner's and each member's **public keys**, their abilities (read, write, invite …), revocations, key-epoch numbers, the coordinator and endpoint URLs | — | `schema.rs:28-45`; bodies: `spec: wire/LFCP-WIRE-01.md:625-633, 701-709, 730-734, 781-789, 868-886` |
| Data Units (your changes) | Resource ID, author Principal ID, sequence number, key epoch, the previous unit's ID | the change itself (ciphertext) | `schema.rs:49-58` |
| Key Packages | Resource ID, epoch, sender and recipient Principal IDs | the sealed key | `schema.rs:64-72` |
| Snapshots | Resource ID, epoch, publisher Principal ID, sequence number | the snapshot itself (ciphertext) | `schema.rs:75-83` |
| Hosting | which Principal asked the server to host each Resource | — | `schema.rs:89-93` |
| Administrators | the operator's Principal ID and public keys, and when they were paired | — | `schema.rs:108-112` |
| Settings | the hosting policy (allowed Principal IDs; hosting credentials only as SHA-256 hashes) | — | `schema.rs:116-119` |

What this reveals: which public keys collaborate on which Resource and
with which abilities; how many changes each member made (sequence
numbers); and the size of each change (ciphertext length tracks plaintext
length, plus a 16-byte tag; there is no padding). WIRE-01 lists the same:
a server can observe IP addresses, Resource IDs, message timing and sizes,
and approximate collaborator activity (§94,
`spec: wire/LFCP-WIRE-01.md:3089-3103`).

**No timestamps on your data.** No object table has a time column
(`schema.rs:20-93`); the protocol orders changes by sequence, not by clock
(WIRE-01 §96, `spec: wire/LFCP-WIRE-01.md:3115`). Optional creation times
inside a task travel inside the ciphertext. The only stored times are the
operator's pairing time and a setup code's expiry (`schema.rs:100-112`).

**No accounts.** You are a public key, not an email address or a password
(WIRE-01 §91, `spec: wire/LFCP-WIRE-01.md:3026`). The server has no
cookies and no analytics.

## What the server sees when you connect

- **Your IP address**, at every connection. nginx passes it to the server
  (`devbox-asstnt: stacks/openlfcp/nginx/06-sync.openlfcp.org.conf`), and
  the server logs it with the connection number
  (`server@v0.1.0: crates/lfcp-server/src/ws.rs:409`).
- **Your Principal ID** (your public key's ID) when the session is
  authenticated, logged with the same connection number
  (`server@v0.1.0: crates/lfcp-server/src/session.rs:292-296`). The
  connection number links your IP to your Principal ID in the log.
- **Which Resources you open and when you sync**, and the timing and size
  of your messages.
- An optional hosting credential, kept in memory only
  (`server@v0.1.0: crates/lfcp-server/src/session.rs:169-170`).

## Logs and how long they are kept

- **Server log.** At the default level (`info`,
  `server@v0.1.0: crates/lfcp-server/src/config.rs:77`) it records, with a
  timestamp: connection opened (connection number, IP address) and closed;
  session ready (Principal ID); Resource hosted (Resource ID); Control
  Record committed (Resource ID, record ID); errors. It contains no task
  content, invitation data or keys
  (`.github: docs/release/security-review-mvp-0.1.md:161-162`). It is
  rotated by size: at most 3 files of 10 MB
  (`devbox-asstnt: stacks/openlfcp/compose.yaml`), so how long a line
  survives depends on traffic.
- **nginx access log.** Each connection's IP address, time, request line
  and user agent (nginx's default `combined` format). Kept for
  **[owner: N days]**. *Today that machine does not rotate nginx logs at
  all; a retention period must be in place before this note is
  published.*
- **Backups.** The database is backed up nightly, encrypted with the
  operator's public GPG key before it leaves the machine, to object
  storage; retention **[owner: N days, per the bucket's lifecycle rule]**.
  Logs are not backed up.

## Cloudflare

DNS for `openlfcp.org` is served by Cloudflare. `sync.openlfcp.org` is
**DNS only**: your connection goes straight to our machine, and TLS ends
there. If we ever enable Cloudflare's proxy (for example against a denial
of service attack), Cloudflare will see your IP address and the TLS
connection metadata (time, size, the host name). It still cannot read your
tasks: they are end-to-end encrypted before TLS. We will update this note
before enabling the proxy.

## Deleting your data

This server version has no way for you to delete data yourself, and
deleting data from the server does not delete the copies held by your
collaborators' devices (WIRE-01 §94, "delete its own copy of data",
`spec: wire/LFCP-WIRE-01.md:3089-3103`). Write to abuse@openlfcp.org with
the Resource ID; the operator can remove a Resource's data by hand. The
operator may also delete data at any time (see the
[terms](sync-server-terms.md)).

## Who can read what

- The operator can read the database and the logs: everything in "What the
  server stores" and "Logs", none of it task content.
- Anyone you share a Resource with can read its content and copy it
  (WIRE-01 §95, `spec: wire/LFCP-WIRE-01.md:3107`).
- This is MVP reference software. Do not use it for data you need to
  protect.
