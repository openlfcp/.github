# Runbook: sync.openlfcp.org

**Status:** DRAFT, pending owner review (LAUNCH-003).

How the public OpenLFCP sync server is run: where it lives, how it is
watched, and how abuse is handled. Users see the
[privacy note](sync-server-privacy.md) and the
[terms](sync-server-terms.md).

## Where it runs

- **Host:** the owner's AWS EC2 box (Amazon Linux 2023, x86_64, ~1 GB
  RAM, 25 GB disk), shared with about ten other stacks and managed with
  Stackyard. The machine repository is `devbox-asstnt` (private, GitLab);
  the server is its stack `openlfcp`.
- **Stack runbook:** `devbox-asstnt: stacks/openlfcp/README.md`. It covers
  enabling, administration over an SSH tunnel, upgrades, backup, restore
  (with a rehearsal record) and Cloudflare. This page does not repeat it.
- **Image:** `ghcr.io/openlfcp/lfcp-server:<version>`, built for
  linux/amd64 and linux/arm64 by `server: .github/workflows/image.yml` on
  each `v*` tag. The box never builds Rust.
- **Path:** client → `wss://sync.openlfcp.org/v1/ws` → nginx on the box
  (TLS via getssl, rate zone `req_openlfcp`) → container `openlfcp-server`
  (128 MB). Only `/v1/ws` and `/health` are public; `/setup` and `/admin/*`
  answer 404 outside the SSH tunnel.
- **DNS:** Cloudflare, `sync.openlfcp.org` DNS only (grey cloud).
- **Contact:** abuse@openlfcp.org, forwarded by Cloudflare Email Routing to
  the owner.

## Monitoring

| What | How | Who hears it |
| --- | --- | --- |
| Container down or unhealthy, disk, inodes | `devbox-watch.timer`, every 15 minutes | Telegram (machine alerts) |
| The whole path on the box: nginx → vhost → server → WebSocket upgrade with `lfcp-1` | `stacks/openlfcp/scripts/health.sh`, run by `./stack --check` | the operator, on demand |
| The machine's monitoring itself | `devbox-heartbeat`, weekly summary on Mondays | Telegram; **no summary = monitoring is broken** |
| Reachable from the internet | an external uptime check (below) | email / push from the service |
| Backups fresh | `devbox-backup-check` / `check-backups.sh` | Telegram |

**External uptime check (recommended: UptimeRobot, free plan).** The box
cannot tell you it is unreachable from outside (DNS, security group,
certificate, the machine being off). Create one monitor:

- type: HTTP(s) keyword; URL `https://sync.openlfcp.org/health`;
- keyword: `"status":"ok"` (the body is exactly `{"status":"ok"}`);
- interval: 5 minutes (the free plan's shortest);
- alert contact: the owner's email or the UptimeRobot app.

It also catches an expired or wrong certificate, since the check fails on
TLS errors. Any equivalent free service (Better Stack, Healthchecks with
an HTTP probe) works the same way; the point is that it runs outside the
box. Do not point it at `/v1/ws`: every probe would count against the
per-IP connection limits.

## Abuse handling

Reports arrive at abuse@openlfcp.org. The server cannot read content, so
every action works from identifiers: a **Resource ID**, a **Principal ID**,
an **IP address** and a time.

### 1. Record and assess

Keep a private log of every report and action: date, reporter, the IDs,
what was done and why. Ask the reporter for the Resource ID (clients show
it, e.g. `lfcp-todo resource info` or the plugin's "Resource status") and
the time.

### 2. Find the facts

All on the box, read-only:

```sh
# Resource ID from base64url (as clients show it) to hex (as the store keeps it)
id='ioyGQnVdM4w3lvpGcZb-mFuMlO07sWhC_FCsyD6rrBo'
hex=$(printf '%s=' "$id" | tr '_-' '/+' | base64 -d | od -An -tx1 | tr -d ' \n')

S=/mnt/data/openlfcp/server.sqlite3
sudo sqlite3 -readonly "$S" "SELECT hex(host) FROM hosting WHERE resource_id = X'$hex';"      # who hosted it
sudo sqlite3 -readonly "$S" "SELECT count(*), sum(length(bytes)) FROM data_units WHERE resource_id = X'$hex';"
sudo sqlite3 -readonly "$S" "SELECT DISTINCT hex(actor) FROM data_units WHERE resource_id = X'$hex';"   # who wrote

./dc logs openlfcp-server | grep -i "$hex"         # "hosted" lines: the connection number (conn=)
./dc logs openlfcp-server | grep "conn=<n> "       # that connection's "websocket open" and "session ready"
sudo grep '<time window>' /var/log/nginx/sync.openlfcp.org-access   # the client IP at that time
```

In server 0.1.0 the `peer` in "websocket open" is nginx's address, not the
client's; the client's IP comes from the nginx access log at the same
time. From the version with POST-003, with `trusted_proxies` set, the line
reads `conn=<n> peer=<nginx> client=<client IP>`: correlate on `client=`.
Refusals by the per-IP limits are logged as `per-IP connection limit;
refusing` with the same two fields.

### 3. Act

**Block an IP address.** In `devbox-asstnt`, add to the `location = /v1/ws`
block of `stacks/openlfcp/nginx/06-sync.openlfcp.org.conf`:

```nginx
deny 203.0.113.7;        # abuse 2026-10-xx, see the abuse log
```

Commit, push; on the box `git pull && ./stack sync` (`nginx -t`, then
reload). With the Cloudflare proxy on, block in Cloudflare's WAF instead,
before the traffic reaches the box.

**Stop a Principal from hosting.** With `lfcp-admin` (POST-014, server
after 0.2.0; stack runbook "Administration"), over the SSH tunnel, set
that Principal's quota to zero:

```sh
lfcp-admin quota get <principal hex>                       # what it hosts: Resources, bytes
lfcp-admin quota set <principal hex> --resources 0 --bytes 0
lfcp-admin quota clear <principal hex>                     # undo: back to the defaults
```

A zero quota refuses its new Resources and every new Data Unit and
Snapshot in the Resources it hosts (`QUOTA_EXCEEDED`). Stored data stays
and stays readable. Control Records and Key Packages still pass within
the control reserve (16 MiB), so revocations and key rotations in those
Resources keep working. It does not cut its existing sessions or its
access to Resources it is a member of: membership is decided by each
Resource's own signed Control Chain, not by the server. Pair it with an
IP block when the same client keeps creating new Principals (keypairs are
free; the server already limits new Resources per IP per day).

**Purge a Resource.** The server has no delete API (0.1.0 and 0.2.0;
POST-015). Purge by hand, with the server stopped.

From server 0.2.0 the store also keeps `resource_usage` (stored bytes
per Resource, for the quotas). Its row must go too:
- with foreign keys on, the delete of the Resource fails without it;
- with them off, an orphan row keeps counting the purged bytes against
  `max_total_bytes`.

The `sqlite3` shell starts with foreign keys **off** and, after an error,
runs the remaining statements, `COMMIT` included. That would leave a
half-purged Resource: its row present, its head and hosting gone. So the
script turns foreign keys on and stops at the first error (`.bail on`).
An error then rolls the whole purge back.

Rehearsed on 2026-10-06:
- On server 0.1.0, against a copy of the restore-drill database.
- On server 0.2.0 (d6cd820), with two Resources hosted, one with an
  invitation and a Key Package. The script below purged one of them.
- After the purge: every row of that Resource gone, the other tables
  intact, `integrity_check` ok, `foreign_key_check` clean, no orphan row
  in any table, `resource_usage` included.
- The server then started normally:
  - `RESOURCE_OPEN` of the purged Resource gets
    `NACK(RESOURCE_NOT_HOSTED)`;
  - the other Resource kept syncing;
  - `lfcp-admin quota get` showed the purged host at 0 Resources and
    0 bytes, and `status` showed one Resource fewer.
- A member's `lfcp-todo sync` on the purged Resource waits without an
  error message until it is stopped.

```sh
./stack disable openlfcp
S=/mnt/data/openlfcp/server.sqlite3
TS=$(date -u +%Y%m%dT%H%M%SZ)
sudo sqlite3 "$S" ".backup /mnt/data/openlfcp-before-purge-$TS.db"   # keep until the purge is confirmed
sudo sqlite3 "$S" <<SQL
.bail on
PRAGMA foreign_keys = ON;
BEGIN;
DELETE FROM control_head  WHERE resource_id = X'$hex';
DELETE FROM hosting       WHERE resource_id = X'$hex';
DELETE FROM data_units    WHERE resource_id = X'$hex';
DELETE FROM key_packages  WHERE resource_id = X'$hex';
DELETE FROM snapshots     WHERE resource_id = X'$hex';
DELETE FROM control_records WHERE resource_id = X'$hex';
DELETE FROM resource_usage  WHERE resource_id = X'$hex';   -- server 0.2.0+ (POST-003 storage accounting)
DELETE FROM resources     WHERE resource_id = X'$hex';
COMMIT;
VACUUM;
PRAGMA integrity_check;
SQL
sudo chown 65532:65532 "$S" && sudo chmod 600 "$S"
./stack enable openlfcp
```

The purge removes the server's copy only. Members keep theirs, and any of
them can host the same Resource again with its Genesis; pair the purge
with an IP block or a zero quota.

A Resource hosted again holds only its Genesis. Its clients do not send
again what the server had acknowledged (Data Units, Control Records,
Key Packages): this is the restore wedge, POST-013. A purge is therefore
final for the server's copy. Delete the `before-purge` copy once the
purge is confirmed: it holds the purged data. Encrypted nightly backups
keep it until their retention expires.

### 4. Answer

Tell the reporter what was done, without other users' identifiers. Law
enforcement requests: the server holds no content, only the metadata in
the privacy note; route them to the owner.

## Gaps for the owner

- **Admin client: `lfcp-admin` (POST-014)** ships with the server
  release after 0.2.0. Until then the server stays unpaired, or the
  owner builds it from server main (`cargo build --release -p
  lfcp-admin`).
- **No ban or purge API** in server 0.1.0; the purge above is manual.
  Proposed as backlog work.
- **nginx access logs are not rotated on the box**, so IP retention is
  unbounded until a rotation is set up (the privacy note promises a
  period).
- **Restore loses recent writes and can stall clients:** clients do not
  re-send changes the server had acknowledged before the backup (see the
  stack runbook, "Restore").
  The proposed fix and the interim guidance for operators are in
  `spec: adr/0008-recovery-after-server-data-loss.md` (POST-013).
