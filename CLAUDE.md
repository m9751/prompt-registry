# CLAUDE.md — prompt-registry

Runtime behavioral guidance for Claude Code sessions in this repo.

**Read `AGENTS.md` first** — it is the authoritative agent router for this repository.

## Quick constraints

1. **Two-artifact rule:** edit `prompts/**/*.md`, then `make verify` — never ship `.md` without compiled JSON.
2. **Footer rule:** feedback block is compiler-injected; do not add to `.md` source.
3. **Branch from `origin/main`:** `git fetch origin && git checkout -b feat/... origin/main`

Full procedure: `AGENTS.md` § How to add a prompt.
