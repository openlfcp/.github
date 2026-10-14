# MVP 0.2 release close-out checklist (draft)

**Status:** DRAFT (LFCP-02-082), not run. Run **after** the public release
(a signed GO in [mvp-0.2-go-no-go.md](mvp-0.2-go-no-go.md) and the tag/publish
steps of [mvp-0.2-owner-checklist.md](mvp-0.2-owner-checklist.md) §6). It
confirms that what went out matches what was approved, that the public
surfaces are correct, and that someone owns every loose end. `<…>` marks a
value the release settles.

## 1. Installed assets vs. checksums

Confirm the published artifacts are the exact ones in the final candidate's
evidence record (rc-verify `--assemble --repro`; the record of
[mvp-0.2-go-no-go.md](mvp-0.2-go-no-go.md)).

- [ ] Plugin `main.js`, `manifest.json`, `styles.css` on the GitHub release
      match the candidate checksums. `<sha256 per file>`
- [ ] npm tarball digests for each `@openlfcp/*` 0.2.0 match the record
      (`npm view @openlfcp/<pkg>@0.2.0 dist.integrity`). `<…>`
- [ ] Server image digest (if a server was released) matches
      `ghcr.io/openlfcp/lfcp-server:<tag>`. `<expected: no server release;
      main is 0.3.2 + pin-only>`
- [ ] The git tags point at the candidate commits
      (`git -C <repo> rev-list -n1 <tag>` = the commit in
      [rc13-manifest.json](rc13-manifest.json)) for spec, sdk-rs, examples
      and .github, and the plugin tag on its 0.4.0 commit. `<…>`

## 2. Public links

- [ ] [Release notes](mvp-0.2-release-notes.md) published and linked from the
      org profile.
- [ ] Organization profile updated from the draft
      (`docs/release/mvp-0.2-org-profile-draft.md`, LFCP-02-079) → live
      `profile/README.md`.
- [ ] Website (`openlfcp.org`) updated to MVP 0.2 (LFCP-02-078) and
      deployed. `<deploy confirmed>`
- [ ] Obsidian repo release page for the plugin version is public with its
      notes. `<…>`
- [ ] No link points at a draft branch or an unpublished path (run doccheck
      on `main` after merges).

## 3. Demo / sync server state

- [ ] `sync.openlfcp.org` is on the intended server version (observable from
      outside, B17). `<version>`
- [ ] Backup/restore for Control/Data/Key Packages/snapshots and config was
      verified before rollout
      ([sync-server-restore-test.md](../operations/sync-server-restore-test.md)).
- [ ] Legacy 0.1 Resources and hosting state preserved; no secrets copied
      into logs or evidence.
- [ ] Quotas match what the release notes and 0.4.0 notes state (B15).
      `<200 collab / 50 per day per network / 256 MiB / 128 MiB, or final>`

## 4. npm view

- [ ] `@openlfcp/*` 0.2.0 is on dist-tag **`latest`**
      (`npm view @openlfcp/<pkg> dist-tags`). `<…>`
- [ ] Each package has provenance and the expected files (a fresh
      `npm install` then import works;
      [npm-publish-checklist.md](npm-publish-checklist.md)).
- [ ] No accidental `0.2.0` on `beta` only, and no empty tarball (the 0.1.2
      lesson: pack must contain `dist`).

## 5. Catalog listing

- [ ] Community-plugins directory shows the plugin at `0.4.0`
      (`manifest.json` and `versions.json` on `main` moved to 0.4.0 in the
      tag step, or catalog users never get it).
- [ ] `obsidian.md/plugins?id=shared-tasks` resolves and shows the new
      version. `<…>`
- [ ] BRAT pre-release channel still works for later betas (unchanged).

## 6. Post-release smoke

On the released artifacts and the live server (test plan §14):

- [ ] Encrypted shared-section smoke on the public server (two vaults,
      share/join/edit/reconnect). `<result>`
- [ ] Legacy 0.1 shared-task smoke still works beside sections. `<result>`
- [ ] A durable reconnect after a dropped connection. `<result>`
- [ ] A fresh install from the directory onboards with the published guides.
      `<result>`

## 7. Minor issues and owners

Every known issue carried into GA (see
[mvp-0.2-go-no-go.md](mvp-0.2-go-no-go.md) "Known issues") has a named owner
and a tracking item.

| Issue | Owner | Tracking | Target |
| --- | --- | --- | --- |
| Rejoin after removal | `<…>` | MVP 0.3 (rejoin-after-removal design note) | `<…>` |
| History growth policy | `<…>` | LFCP-02-112 follow-ups | `<…>` |
| "Needs attention" right after sharing | `<…>` | `<issue>` | `<…>` |
| Windows/Linux performance qualification | `<…>` | `<issue>` | `<…>` |
| `<other>` | `<…>` | `<…>` | `<…>` |

## 8. Incident process

- [ ] The incident and rollback process is linked and current:
      [MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md)
      §15 and
      [mvp-0.2-rollback-and-restore.md](../operations/mvp-0.2-rollback-and-restore.md).
- [ ] The last known-good **section-capable** build and its storage/schema
      manifest are recorded (a 0.1 downgrade is not a safe rollback for
      section data).
- [ ] On a suspected unsafe projection/publication: pause the affected path
      with a tested mechanism, preserve queues/replicas, show an honest
      blocked state — never wipe caches or regenerate identity to make the UI
      look healthy.
- [ ] Security reports go to `security@openlfcp.org`, never a public issue.

## Close

- Release closed by: `<name>`  **Date:** `<date>`
- Outstanding items handed to: `<owner / tracker>`
