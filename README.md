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

## Validate from a clean checkout

```sh
./scripts/validate.sh
```

Requires Ruby (for YAML parsing; preinstalled on GitHub-hosted runners).

## License

Apache License 2.0. See [LICENSE](LICENSE).
