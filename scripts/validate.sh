#!/usr/bin/env bash
# Validation entry point for the organization .github repository.
# Checks that every workflow file is well-formed YAML.
set -euo pipefail

cd "$(dirname "$0")/.."

count=0
for file in .github/workflows/*.yml; do
  [ -e "$file" ] || continue
  ruby -ryaml -e 'YAML.safe_load(File.read(ARGV[0]), aliases: true)' "$file"
  count=$((count + 1))
done

echo ".github: ${count} workflow file(s) parsed"
