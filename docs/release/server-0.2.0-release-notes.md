# OpenLFCP server 0.2.0: release notes

**Status:** Final. The reference server `0.2.0` (server d6cd820), 2026-10-06.
Only the server is released. sdk-ts, sdk-rs, the Obsidian plugin and the
examples stay at `0.1.0`, and no npm package is published.

## What this is

Server 0.2.0 makes the reference server fit for a public deployment with
unknown clients. It adds abuse limits and storage quotas (POST-003) and
bounds the server's memory (POST-004). Since 0.1.0 these were known
limitations: see [mvp-0.1-release-notes.md](mvp-0.1-release-notes.md)
("Known limitations") and
[security-review-mvp-0.1.md](security-review-mvp-0.1.md).

It is a minor version for three reasons:
- the default hosting mode changes;
- the configuration file gains keys that 0.1.0 rejects;
- the admin API gains endpoints.

The wire protocol is unchanged.

## Upgrade notes

Read these before upgrading a 0.1.0 server.

- **Back up the state directory first.** On its first start, 0.2.0
  applies store migration 3:
  - the `resource_usage` table, filled from the stored objects;
  - the `quota_overrides` table.

  The migration is not reversible, and 0.1.0 cannot open the migrated
  database.
- **Quota mode becomes the default.** A server that never set a hosting
  policy now runs in quota mode instead of open mode. Any authenticated
  Principal may host, within per-Principal and per-Resource quotas:
  - 20 Resources per hosting Principal;
  - 256 MiB per hosting Principal;
  - 128 MiB per Resource;
  - 10 new Resources per client IP per day.

  Existing Resources count toward their host's quota. A host already over
  it can still read, but new writes are refused (`QUOTA_EXCEEDED`).
  - `PUT /admin/hosting {"mode": "open"}` restores the 0.1.0 behaviour.
  - A server that set the allow-list or open mode keeps it.
- **Storage floor.** By default writes are refused when the state
  directory's disk has less than 2 GiB free (`min_free_bytes`); below
  512 MiB every write is refused. On a small disk, lower
  `min_free_bytes`, or set it to `0` to turn the check off.
- **New configuration keys.** All of them are optional, with defaults.
  See the table in server `README.md`, "Running", and the sections
  "Abuse limits" and "Memory".
  - Client IP and per-IP limits: `trusted_proxies`, `client_ip_header`,
    `max_connections_per_ip`, `connections_per_ip_per_minute`,
    `admin_requests_per_ip_per_minute`, `max_tracked_ips`.
  - Message rate: `ws_messages_per_second`, `ws_message_burst`.
  - Quotas: `quota_resources_per_principal`, `quota_bytes_per_principal`,
    `quota_bytes_per_resource`, `hosts_per_ip_per_day`,
    `quota_control_reserve_bytes`.
  - Storage: `max_total_bytes`, `min_free_bytes`,
    `disk_check_interval_ms`.
  - Memory and timeouts: `max_outbound_bytes`,
    `max_total_outbound_bytes`, `write_timeout_ms`,
    `admin_body_timeout_ms`.
- **A 0.2.0 configuration does not go back.** The configuration rejects
  unknown fields, so 0.1.0 refuses to start with a file that uses any of
  the new keys. To roll back, restore both the 0.1.0 configuration and
  the backup of the state directory.
- **Behind a reverse proxy, set `trusted_proxies`.** Otherwise every
  client is the proxy's address, and the per-IP limits apply to all
  clients together. `deploy/` sets this up for Caddy.
- **Admin challenges are stateless.** A challenge is its expiry, a nonce
  and an HMAC tag; issuing one stores nothing. A proof that opened a
  session is remembered until its challenge expires, so it cannot be
  replayed. A refused proof leaves nothing behind, so its challenge can be
  used again until it expires. Challenges do not survive a restart.

## What changed

**Abuse limits and quotas** (POST-003; server e825c30 to 24f013d):
- the client IP is read from a trusted proxy's header (9b5c85f, 98ad245);
- open and new WebSockets are capped per client IP (9b5c85f, 9de1db1);
- messages are rate-limited per WebSocket connection (126c65a);
- admin requests are rate-limited per client IP (c8c0809);
- admin challenges are stateless (03585cb);
- stored bytes are accounted per Resource (740c377);
- quota mode is the default (bf09efe), with new Resources per client IP
  per day (0c998a6);
- a global storage floor and an optional store cap (b9307ca);
- new admin API: `GET /admin/quotas` and `GET`, `PUT` and
  `DELETE /admin/quotas/<principal>` for per-Principal quota overrides.

**Revocation at quota** (2a4d5c7). `CONTROL_PUT` and `KEY_PACKAGE_PUT`
carry what a revocation needs: the Capability Revoke, the Key Epoch and
its Key Packages. These puts may store `quota_control_reserve_bytes`
(16 MiB) past the byte quotas, ignore `max_total_bytes`, and pass a low
disk down to the hard floor. A writer who fills a Resource therefore
cannot block their own revocation.

**Memory bounds** (POST-004):
- outbound bytes are bounded per connection (`max_outbound_bytes`) and
  for the whole server (`max_total_outbound_bytes`, 64 MiB) (850f398);
- `CONTROL_GET`, `DATA_GET` and `KEY_PACKAGE_GET` replies are read from
  the store a page at a time, and wait for room while the peer reads
  (805d800);
- waiting replies are queued in order, control replies ahead of GET pages
  (72d05bc);
- a peer that stops reading is closed after `write_timeout_ms`, and its
  memory is freed;
- an admin request body must arrive within `admin_body_timeout_ms`
  (bb9677c).

**A memory leak fixed** (6777968). tungstenite's write buffer kept the
size of the largest frame for the life of each connection: about 8 MiB
per connection, outside any bound, in 0.1.0 too. Messages over 64 KiB now
go as 64 KiB WebSocket fragments (WIRE-01 §31 allows it). Clients
reassemble them, and their size limits apply to the whole message.

Measured peak RSS, 0.1.0 → 0.2.0 (macOS arm64, release build):
- 50 concurrent readers: 750 → 41 MiB;
- one `DATA_GET` of a 256 MiB Resource: 619 → 41 MiB.

The server `README.md` ("Memory") gives the sizing rule and settings for
a 128 MB container.

**Container image** (8d3ac2c). `ghcr.io/openlfcp/lfcp-server` for
`linux/amd64` and `linux/arm64`. Each architecture is built natively and
smoke-tested before anything is tagged. A pushed `v*` tag publishes the
version (`0.2.0`) and `latest`.

## Compatibility

- The wire protocol is unchanged: LFCP-WIRE-01 at `mvp-0.1-baseline.8`
  (spec da3977f), on sdk-rs `0.1.0` (c9132b1).
- sdk-ts `0.1.0` and the Obsidian plugin `0.1.0` interoperate with
  0.2.0. The live interop and the plugin's E2E tests pass against it (rc8,
  [rc-verification.md](rc-verification.md)), an 8 MiB fragmented batch
  included.
- Clients may see new refusals: `NACK(QUOTA_EXCEEDED)` and
  `NACK(RATE_LIMITED)` with a diagnostic, `ERROR(RATE_LIMITED)` and close
  1008 past the message rate, and HTTP 429 with `Retry-After`. All of
  them are WIRE-01 §62 codes that 0.1.0 clients already handle.

## Security

From the [security review](security-review-mvp-0.1.md):
- **H5** (open hosting, no quotas): fixed (server bf09efe, 0c998a6,
  b9307ca; revocation at quota 2a4d5c7).
- **H6** (GET replies in memory, an unbounded outbound queue): fixed
  (850f398, 805d800, 72d05bc, 6777968).
- **M2** per-IP limits and rates (9b5c85f, 9de1db1, 126c65a, c8c0809) and
  **M3** stateless challenges (03585cb): fixed.
- The admin body read timeout: fixed (bb9677c).

## Known limitations

- **M5 after READY:** an authenticated peer's message is decoded in full,
  up to `max_message_bytes`. Inbound memory is bounded only by
  `max_connections` × about 3 × `max_message_bytes` (server `README.md`,
  "Memory").
- The Control Coordinator caches each hosted Resource's whole Control
  Chain in memory. Chains are small at MVP sizes.
- **Restoring from a backup can wedge clients** (POST-013 in
  [BACKLOG-MVP-0.1.md](../BACKLOG-MVP-0.1.md#post-013---recovery-after-server-data-loss-restore-wedge)).
  Data Units acknowledged after the backup are lost, and their writer
  does not send them again.
- There is no admin CLI (POST-014). The admin API needs signed proofs.
- There is no API to ban a Principal or purge its Resources (POST-015).
- The per-IP state, including the daily hosting count, is in memory and
  forgotten on restart.
- Windows: no owner-only state files, as in 0.1.0.
