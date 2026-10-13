# MVP 0.2: the server needs no change (evidence)

**Task:** LFCP-02-081. **Date:** 2026-10-14.

MVP 0.2 (sdk-ts `0.2.0`, Shared Tasks `0.4.0`) runs on the reference
server already deployed. The deployed version is `0.3.2`, as stated by
the owner. This page records the evidence that no server change or
redeploy is needed for the release.

## What the server is

- **Deployed:** `wss://sync.openlfcp.org/v1/ws`, version 0.3.2 (the
  owner's record).
  - The only production request made for this page was one public `GET
    https://sync.openlfcp.org/health` on 2026-10-13 at 20:42 UTC. It
    answered `200 {"status":"ok"}`.
  - The health endpoint names no version (see
    [mvp-0.2-baseline-inventory.md](mvp-0.2-baseline-inventory.md)).
- **The tag:** `server v0.3.2` (`7afa509`, 2026-10-12, [release
  notes](server-0.3.2-release-notes.md)). It pins `sdk-rs` at `d31d4d8`
  and the spec at `mvp-0.2-baseline.11`.
- **server `main`:** `138030a` is `v0.3.2` plus one pin-only commit. It
  changes four files:
  - `spec.lock` moves to `mvp-0.2-baseline.12`;
  - `sdk-rs.lock` moves to `0a8239b`;
  - a README paragraph about the pins;
  - one spec-vectors test line.

  No server code differs. Baseline.12's changes bind clients: the §47
  writer rule for pending Control Records, plus Shared Objects and
  shared sections rules that the server does not read.

## How it was tested

The `v0.3.2` binary was built locally from the tag, not from `main`:

- a server worktree at `v0.3.2`, with `sdk-rs` beside it at `d31d4d8`
  (its `sdk-rs.lock`);
- `cargo build --locked -p lfcp-server` (dev profile; rustc 1.99.0),
  which reports `lfcp-server v0.3.2`;
- the server's `sdk_rs_lock` test passes, so the build used the locked
  `sdk-rs`;
- binary sha256 `1cfd682eba1dc6d1…`.

The clients ran on Node 24.15:

1. **The Obsidian plugin's live suite.**
   - Shared Tasks at obsidian `main` `4187949`, on `@openlfcp/*`
     `0.2.0-beta.8`, the code of `0.2.0`.
   - Command: `LFCP_REQUIRE_LIVE=1 LFCP_SERVER_BIN=<the v0.3.2 binary>
     pnpm test`.
   - With `LFCP_REQUIRE_LIVE=1`, a live test without a server fails
     instead of skipping.
   - Result: **148 files, 1598 tests, all passed.**
2. **sdk-ts, its interop with the Rust server included.**
   - sdk-ts `main` `091f1a9` (`0.2.0-beta.8`; the `0.2.0` release
     commit changes only versions).
   - Command: `LFCP_REQUIRE_LIVE=1 LFCP_SERVER_DIR=<the v0.3.2
     worktree> LFCP_SERVER_TARGET_DIR=<its target> pnpm test`.
   - Every interop file passed against `v0.3.2`, 15 files:
     - invite, claim journal, access recovery (6 tests), restart, revoke
       (2), not hosted, recovery (2);
     - two clients end to end, section Snapshot, chaos (20), Snapshot,
       stale first unit (the 0.2.0-beta.8 §26.2 fix);
     - revoked refusal, sync, orphan.
   - Overall: 2455 of 2458 tests passed in the full run.
   - The 3 others timed out under a load average of 10 from other test
     suites on the machine. None of the three touches the server: a
     seeded property test, the sections corpus and a fake-server client
     test. Run again on their own, they passed (3 files, 141 tests).

## Conclusion

The MVP 0.2 clients pass their live and interop suites against server
`0.3.2` as tagged, so the release needs no server change and no
redeploy. Server `main` (`138030a`) differs from the tag only in its
pins and docs, so it would behave the same.

**Not covered here:**

- the deployed instance itself: no test traffic was sent to production,
  by design;
- an optimized (release-profile) build;
- the operator's configuration (quotas, proxy).

The owner's beta and pilot checks on sync.openlfcp.org cover the
deployed instance.
