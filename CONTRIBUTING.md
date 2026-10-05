# Contributing to OpenLFCP

Thanks for helping. This file is the organization default for every
`openlfcp` repository.

1. **Read the rules.**
   - [docs/AGENT-OPERATING-GUIDE.md](docs/AGENT-OPERATING-GUIDE.md): source of
     truth, repository boundaries, security rules.
   - [docs/engineering-conventions.md](docs/engineering-conventions.md):
     branches, commits, validation, labels, versioning, spec changes.
2. **Find the work.**
   [docs/BACKLOG-MVP-0.1.md](docs/BACKLOG-MVP-0.1.md) is the authoritative
   plan. Reference its `LFCP-NNN` id in every change.
3. **Follow the specification, not the code.**
   - Normative behavior is defined in `spec` (LFCP-WIRE-01, the Shared Objects
     Profile, the test vectors).
   - If the text is missing, ambiguous or contradicts a vector, open a
     "Protocol / spec gap" issue instead of choosing a behavior
     ([conventions §8](docs/engineering-conventions.md#8-specification-gaps)).
4. **Keep every commit green.** Run the repository's validation command
   before each commit
   ([conventions §4](docs/engineering-conventions.md#4-validation-commands)).
5. **Report security issues privately.** See [SECURITY.md](SECURITY.md).

By contributing you agree that your contributions are licensed under the
Apache License 2.0.
