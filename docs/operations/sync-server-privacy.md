<!-- Reviewed by the project, not by a lawyer. -->

# Privacy note: sync.openlfcp.org

**Effective:** 2026-10-06. **Service status:** beta, a proof of concept.

This note explains what the public OpenLFCP sync server at
`wss://sync.openlfcp.org` learns about you, why, how long it keeps it, and
your rights under the EU General Data Protection Regulation (GDPR).

## In short

Your tasks are end-to-end encrypted on your device before they leave it.
The server stores and forwards ciphertext it cannot decrypt, plus the
protocol metadata it needs: public keys, Resource IDs, who may do what,
sequence numbers and sizes. It sees your IP address when you connect. It
never sees task text, the keys that decrypt it, or the notes you did not
share. There are no accounts, cookies, analytics or ads.

## Who is responsible

The controller is **Andrey Pankov**, an individual, Poland, who runs the
service for the OpenLFCP project. Contact:

- **privacy@openlfcp.org**: privacy questions and data protection requests;
- **abuse@openlfcp.org**: abuse of the service;
- **security@openlfcp.org**: security vulnerabilities.

No data protection officer is appointed. The operator may change in the
future; we will announce it here before it happens.

## What the server processes, why, and on what basis

| Data | Purpose | Legal basis | Kept for |
| --- | --- | --- | --- |
| Encrypted content you sync (Data Units, Key Packages, Snapshots) | providing the service | performance of the contract you enter by using it, GDPR Art. 6(1)(b) | until the Resource is removed (see "Erasure") |
| Protocol metadata stored with it: public keys and Principal IDs, Resource IDs, abilities granted to members, sequence numbers, key-epoch numbers, coordinator URLs, sizes, which key hosted each Resource, quota settings | providing the service; enforcing quotas | Art. 6(1)(b) | as the content |
| Your IP address, time of connection, request line and user agent (nginx log); connection number, IP address, Principal ID, Resource IDs hosted or changed (server log) | security, abuse prevention, troubleshooting | legitimate interest in keeping the service secure and available, Art. 6(1)(f) | 14 days |
| Per-IP counters for rate limits and quotas | abuse prevention | Art. 6(1)(f) | in memory only, as long as a limit needs them (the longest window is 24 hours); cleared on every restart |
| Encrypted backups of the server's database (not of the logs) | restoring the service after a failure | Art. 6(1)(f) | 30 days |
| Emails you send us | answering you | Art. 6(1)(f), or Art. 6(1)(c) for a legal request | as long as the matter needs |

The server code is open source. Where each item comes from: the stored
tables are in `server@v0.2.0: crates/lfcp-server/src/store/schema.rs`
(lines 20–165); the server never decrypts content and holds no decryption
key (`crates/lfcp-server/src/ingest.rs:1-4`); the log lines are
`crates/lfcp-server/src/ws.rs:547` (connection: IP address) and
`crates/lfcp-server/src/session.rs:452-456` (session: Principal ID), at
the default level `info` (`crates/lfcp-server/src/config.rs:129`); the
per-IP table is `crates/lfcp-server/src/limits.rs:16-24`. What any LFCP
server can observe is listed in the protocol itself (`spec:
wire/LFCP-WIRE-01.md` §94).

**What this metadata reveals.** Which public keys collaborate on which
Resource and with which abilities; how many changes each member made; the
size of each change (ciphertext length follows plaintext length, without
padding); when you connect. It does not reveal what you wrote. No stored
object carries a time stamp; the protocol orders changes by sequence, not
by clock (WIRE-01 §96).

**What the server cannot see.** Task text and every other shared content;
the content keys (they reach members sealed to each member's own key);
your private keys, which never leave your device; the secret part of an
invitation link (WIRE-01 §18.2: it "MUST NOT be … transmitted to the
synchronization server"); and everything in your notes that you did not
share. The operator cannot read your tasks either.

You are identified by a public key, not by your name or email. We do not
try to link keys or IP addresses to people, and we make no automated
decisions about you; quotas and rate limits are technical limits that
apply to everyone alike.

## Who else receives data

- **Amazon Web Services** hosts the server (EC2) and stores the encrypted
  backups (S3), in the **us-east-1** region (United States). This is a
  transfer outside the EEA. It is covered by AWS's Data Processing
  Addendum, which includes the EU Standard Contractual Clauses; Amazon Web
  Services, Inc. also participates in the EU-U.S. Data Privacy Framework.
  Backups are encrypted with the operator's key before they leave the
  server; AWS cannot read them.
- **Cloudflare** runs DNS for `openlfcp.org` and forwards email sent to our
  addresses (Cloudflare Email Routing). `sync.openlfcp.org` is DNS only: your
  connection goes straight to the server, and Cloudflare does not see it.
  If we ever enable Cloudflare's proxy (for example against an attack),
  Cloudflare will see your IP address and the TLS connection metadata
  (time, size, host name), but still not your tasks, which are encrypted
  before TLS. We will update this note before enabling it. Cloudflare
  provides a Data Processing Addendum with the Standard Contractual
  Clauses and participates in the EU-U.S. Data Privacy Framework.
- Anyone you share a Resource with can read its content and copy it
  (WIRE-01 §95). That is the point of sharing, and it is outside the
  operator's control.
- We disclose data to authorities only where the law requires it. We hold
  no readable content.

## Your rights

You have the right to access your data, to have it rectified or erased,
to restrict or object to its processing, and to data portability. To
exercise them, write to **privacy@openlfcp.org**. Because there are no
accounts, include what identifies your data: the Resource ID and your
Principal ID (both shown by the client), and, for logs, your IP address
and the time. We answer within one month.

How the rights work here, honestly:

- **Access and portability.** We can give you the metadata and the
  encrypted objects we hold for a Resource or Principal ID. The readable
  copy of your data is already on your own devices.
- **Erasure.** We delete the server's copy of a Resource (the encrypted
  content and its metadata). A shared Resource is one unit: removing one
  member's contributions without deleting it for every member is not
  possible, so for a shared Resource we will agree the next step with
  you. Deletion does not reach your collaborators' devices. Log entries
  age out within 14 days; encrypted backups within 30 days, and a restore
  in that period could bring a deleted Resource back, in which case we
  delete it again.
- **Objection** to log processing: logs are kept for security and only for
  14 days; we weigh any objection against that purpose.

You may also complain to the Polish supervisory authority, the President
of the Personal Data Protection Office (Prezes Urzędu Ochrony Danych
Osobowych, **uodo.gov.pl**), or to the authority of the EU country where
you live or work.

## Beta service

This is MVP software run as a proof of concept, free and without
guarantees. Data on the server can be lost, including changes made
shortly before a restore from backup (see the
[terms](sync-server-terms.md)). Keep your own copies: your devices hold the
full data of every Resource you sync. Do not use the service for data you
need to protect. The service is not directed at children under 16.

## Changes to this note

We publish changes here, with a new effective date. For material changes
(for example new recipients or longer retention) we announce them before
they take effect, in the project's repositories.
