# openlfcp/.github

Organization-wide GitHub metadata and reusable CI for the OpenLFCP project.

This repository holds shared GitHub configuration only. It contains no
protocol specification and no implementation code.

## Repositories

| Repository | Purpose |
| --- | --- |
| `spec` | Normative specifications, profiles, interoperability vectors, registries, ADR/RFC material |
| `sdk-ts` | Reusable TypeScript LFCP implementation (no Obsidian dependency) |
| `sdk-rs` | Independent Rust LFCP implementation |
| `server` | Application-agnostic reference LFCP server |
| `obsidian` | Obsidian editor adapter and product UI |
| `examples` | Small protocol examples and interoperability demonstrations |

## Project documents

| Document | Purpose |
| --- | --- |
| [docs/BACKLOG-MVP-0.1.md](docs/BACKLOG-MVP-0.1.md) | **Authoritative planning source**: MVP 0.1 issue numbers, dependencies and acceptance criteria |
| [docs/MVP-0.1-PROTOCOL-SCOPE.md](docs/MVP-0.1-PROTOCOL-SCOPE.md) | Which parts of LFCP Wire the secure MVP requires, and what is deferred |
| [docs/AGENT-OPERATING-GUIDE.md](docs/AGENT-OPERATING-GUIDE.md) | Source-of-truth hierarchy, repository boundaries and rules for agents and contributors |
| [docs/PROJECT-NARRATIVE.md](docs/PROJECT-NARRATIVE.md) | Project history, vision and architecture narrative |
| [docs/ARTIFACTS-INDEX.md](docs/ARTIFACTS-INDEX.md) | Catalog of every current artifact and the repository it lives in |
| [docs/engineering-conventions.md](docs/engineering-conventions.md) | Branches, commits, validation, labels, versioning and the spec-change process |

## Organization defaults

[CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), the issue
forms in [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) and the
[pull request template](.github/pull_request_template.md) are served by
GitHub to every `openlfcp` repository that has none of its own, so they are
not copied into the other repositories. Labels
([.github/labels.yml](.github/labels.yml)) and
[CODEOWNERS](.github/CODEOWNERS) are not inherited and are set up per
repository.

The backlog is planning authority only. It does not override the normative
specifications, which live in `spec` (see `spec: README.md` for the
source-of-truth table): `spec: wire/LFCP-WIRE-01.md`,
`spec: profiles/SHARED-OBJECTS-PROFILE-01.md`,
`spec: integration/MARKDOWN-REFS-01.md` and the vectors under
`spec: test-vectors/`. Obsidian architecture lives in
`obsidian: docs/OBSIDIAN-ARCHITECTURE-01.md`.

## Validate from a clean checkout

```sh
./scripts/validate.sh
```

Requires Ruby (for YAML parsing; preinstalled on GitHub-hosted runners). It
checks every YAML file, the labels file and the issue forms.

## License

Apache License 2.0. See [LICENSE](LICENSE).
