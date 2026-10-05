# Security policy

## Reporting a vulnerability

Report vulnerabilities **privately** through GitHub private vulnerability
reporting. Do not open a public issue.

1. Open the affected repository on GitHub, for example
   `https://github.com/openlfcp/spec`.
2. Go to **Security → Advisories → Report a vulnerability**. The direct link
   is `https://github.com/openlfcp/<repository>/security/advisories/new`.
3. Describe the issue, the affected component and version or commit, and how
   to reproduce it.

If you are unsure which repository is affected, use `openlfcp/spec` for
protocol and specification issues, or the implementation repository for
code issues.

The project has no separate security email address. Please do not send
reports to personal addresses.

## Scope

This covers the LFCP specifications (a flaw in the protocol design itself
is in scope), the reference implementations and the reference server.

## Test material

The keys, DEKs and secrets in the published test vectors are **public test
fixtures**. They are not vulnerabilities, and they must never be used in
production or as production defaults.
