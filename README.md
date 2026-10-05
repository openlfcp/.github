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

Requires Ruby (for YAML parsing; preinstalled on GitHub-hosted runners).

## License

Apache License 2.0. See [LICENSE](LICENSE).
