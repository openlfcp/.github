# MVP 0.2: the owner's checklist

Everything only the project owner does between the first beta and the
public release of `@openlfcp/*` 0.2.0 and Shared Tasks 0.4.0, in order.
Each item links the page with the full steps. Tick an item here when it is
done, with the date and where its result is recorded.

Done so far: spec `mvp-0.2-baseline.6` to `.10`; npm `@openlfcp/*`
0.2.0-beta.1 to 0.2.0-beta.5 (dist-tag `beta`); plugin 0.4.0-beta.1 to
0.4.0-beta.5 (pre-releases for BRAT); server 0.3.1 released (image
`ghcr.io/openlfcp/lfcp-server:0.3.1`). The two-vault check of 0.4.0-beta.1
passed steps 0 to 5 and failed step 6 (a Task cut and pasted was lost);
fixed in 0.4.0-beta.2, with a choice to restore or keep deleted since
0.4.0-beta.4. The final candidate rc12 (spec baseline.10, npm
0.2.0-beta.5, plugin 0.4.0-beta.5) passed all eight `rc-verify` gates:
[release/mvp-0.2-candidate-report.md](mvp-0.2-candidate-report.md).
Differential fuzzing of the Rust and TypeScript SDKs finds no divergence
at baseline.10.

## 1. Betas (when the orchestrator sends the commands)

- [x] npm `@openlfcp/*` 0.2.0-beta.5 and plugin 0.4.0-beta.5, 2026-10-12.
- [ ] Any later beta: tag and approve npm in `openlfcp/sdk-ts`
      (environment `npm-publish`), then dry run and tag the plugin
      ([obsidian docs/devel/release.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/release.md),
      "The owner's steps for a beta").

## 2. Manual checks (any beta; the latest one is best)

- [ ] **Two Obsidian vaults**, 8 steps, about 30 minutes; rerun steps 6
      to 8 on 0.4.0-beta.5 in two new vaults:
      [obsidian docs/devel/testing/two-obsidian-beta-check.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/testing/two-obsidian-beta-check.md).
- [ ] **IME input** (gap B13; required before a 0.4 beta is announced):
      Japanese and Pinyin on macOS, 6 steps,
      [obsidian docs/devel/testing/ime-checklist.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/testing/ime-checklist.md).
      Record the result in its table.
- [ ] **Windows and Linux by hand** (gap B12): the platform smoke checklist
      on a real Windows and a real Linux desktop,
      [obsidian docs/devel/testing/platform-smoke.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/testing/platform-smoke.md);
      record in
      [platform-smoke-runs.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/testing/platform-smoke-runs.md).
      A cross-OS pair (one vault on each) covers checks D and E.
- [ ] **Mobile, read-only** (optional for the beta, needed for GA claims):
      one phone or tablet, checks M1 to M8,
      [obsidian docs/devel/testing/mobile-sections-checklist.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/testing/mobile-sections-checklist.md).

## 3. Public server (sync.openlfcp.org)

- [ ] Decide whether to deploy server 0.3.1 now (refuses a store from a
      newer server, reports a damaged store; same store format, rollback
      to 0.3.0 is safe):
      [release/server-0.3.1-release-notes.md](server-0.3.1-release-notes.md).
- [x] Confirm the quotas the beta notes state (gap B15): the deployed
      configuration of sync.openlfcp.org (2026-10-14) has 200
      collaborations per identity, 50 new per network per day, 256 MiB
      per identity, 128 MiB per collaboration; 3 GiB of storage in all
      with at least 2 GiB of disk free; 8 open and 20 new connections a
      minute per network address; 50 messages a second per connection
      (burst 200); messages up to 1 MiB. The server's
      `deploy/server.toml` carries the same values as its defaults.
- [ ] **Restore test** on the public server, at least once before 0.4.0
      (gap B16), three cases, about 30 minutes:
      [operations/sync-server-restore-test.md](../operations/sync-server-restore-test.md).
- [ ] Record the deployed server version with each deploy (gap B17).

## 4. Pilot (decision V2: 3 to 5 pairs, at least 7 days)

All steps are in
[operations/mvp-0.2-pilot-operations.md](../operations/mvp-0.2-pilot-operations.md);
its section 10 is the owner's list:

- [ ] Fill in the placeholders; approve the consent text (section 3) and
      the feedback form (section 5).
- [ ] Choose the support channel and who watches it.
- [ ] Record the beta version the pilot uses.
- [ ] Create the synthetic onboarding note and the two test vaults.
- [ ] Re-derive the outcome targets for 3 to 5 pairs
      ([MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §13).
- [ ] Optional: an early dogfood with 2 to 3 pairs first (LFCP-02-105).
- [ ] Run the pilot; collect the outcomes; every blocker is fixed and
      re-observed.

## 5. Release decision

- [ ] Review the release record of the final candidate (LFCP-02-073):
      `scripts/rc-verify.py` manifest and evidence, G01 to G12, what did
      not run and why
      ([MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §16,
      [release/rc-verification.md](rc-verification.md)).
- [ ] Review the open owner decisions and the rollback plan
      ([operations/mvp-0.2-rollback-and-restore.md](../operations/mvp-0.2-rollback-and-restore.md)).
- [ ] Go or no-go.

## 6. Public release (after "go"; the orchestrator sends the commands)

- [ ] Tag and approve npm `@openlfcp/*` 0.2.0 (dist-tag `latest`).
- [ ] Tag plugin 0.4.0; `manifest.json` and `versions.json` on `main` move
      to 0.4.0 in the same step, or catalog users never get it
      ([obsidian docs/devel/release.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/release.md)).
- [ ] Publish the release notes
      ([release/mvp-0.2-release-notes.md](mvp-0.2-release-notes.md)) and
      the organization profile
      ([release/mvp-0.2-org-profile-draft.md](mvp-0.2-org-profile-draft.md));
      update the website.
- [ ] After the release: the encrypted section and legacy smoke on the
      public server, and a durable reconnect (plan §14).
