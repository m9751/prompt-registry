#!/usr/bin/env bash
set -euo pipefail
# CI/local parity: verify feedback footer on all compiled prompts.
missing=$(jq -r '.prompts[] | select(.prompt_text | contains("Score this prompt") | not) | .id' dist/prompts_latest.json)
if [ -n "$missing" ]; then
  echo "FOOTER MISSING on: $missing"
  exit 1
fi
echo "All prompts have feedback footer."
