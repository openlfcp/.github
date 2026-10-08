# npm trusted publishing: one-time setup

**For:** the project owner. Done once; after it, a pushed `vX.Y.Z` tag of
sdk-ts publishes the eight `@openlfcp/*` packages from GitHub Actions
(`sdk-ts: .github/workflows/release.yml`) with npm Trusted Publishing
(OIDC): no npm token, no one-time code, provenance attached. The release
steps are in [npm-publish-checklist.md](npm-publish-checklist.md),
"Trusted publishing".

Field names follow npm's documentation
(<https://docs.npmjs.com/trusted-publishers>). npm does not check the
settings when you save them: a mistake shows only at the first publish,
as a refused `npm publish` in the workflow log.

## 1. GitHub: the environment `npm-publish`

In <https://github.com/openlfcp/sdk-ts>: **Settings → Environments → New
environment**.

1. Name: `npm-publish` (exactly; the workflow's publish job names it).
2. **Configure environment**:
   - **Required reviewers**: tick it and add yourself. Each release then
     waits for your approval (**Review deployments → Approve and deploy**
     on the run page).
   - **Deployment branches and tags**: **Selected branches and tags** →
     **Add deployment branch or tag rule** → **Ref type: Tag**, name
     pattern `v*`. Only a tag can then run the publish job.
3. **Save protection rules**.

No secret is needed: the job gets its OIDC token from GitHub
(`permissions: id-token: write`).

## 2. npm: a trusted publisher for each of the eight packages

On <https://www.npmjs.com>, logged in as an owner of the `@openlfcp`
packages, for each of `@openlfcp/core`, `@openlfcp/crypto`,
`@openlfcp/storage`, `@openlfcp/wire`, `@openlfcp/storage-node`,
`@openlfcp/storage-idb`, `@openlfcp/shared-objects` and
`@openlfcp/client` (all exist already):

1. Open the package, then **Settings → Trusted publishing**.
2. In **Trusted Publisher**, under **Select your publisher**, choose
   **GitHub Actions**.
3. Fill in:

   | Field | Value |
   | --- | --- |
   | Organization or user | `openlfcp` |
   | Repository | `sdk-ts` |
   | Workflow filename | `release.yml` (the file name only) |
   | Environment name | `npm-publish` |
   | Allowed actions | tick direct **`npm publish`** (the workflow runs `npm publish`; `npm stage publish` alone is not enough). Leave `npm dist-tag` unticked. |

4. Save.

Every package's `package.json` names
`https://github.com/openlfcp/sdk-ts.git` as `repository.url`, as npm
requires.

## 3. npm: disallow tokens (after the first CI release)

Once a release went out through the workflow, for each of the eight
packages: **Settings → Publishing access → Require two-factor
authentication and disallow tokens → Update Package Settings**. Trusted
publishing keeps working (it uses OIDC, not a token); a leaked token can
then publish nothing. The manual path of the checklist still works with
your login and a one-time code.

## 4. Check before the first release

- In GitHub, **Actions → Release → Run workflow** on `main` with
  **dry_run** ticked (the default), or
  `gh workflow run release.yml -R openlfcp/sdk-ts --ref main -f dry_run=true`.
  It builds, runs `release:check`, packs the eight packages and runs
  `npm publish --dry-run` on each: no approval is asked and nothing is
  published.
- The dry run does not exercise OIDC: the trusted-publisher settings are
  tested by the first real release, whose publish job waits for your
  approval.

## What CI does not do

- **The dist-tag `next`.** CI only publishes. A final release goes to
  `latest`, a prerelease (`X.Y.Z-rc.N`) to `next`; `next` is no longer
  moved to a final version.
- **Deprecations and unpublishing** stay manual (`npm deprecate`, with
  your login).
