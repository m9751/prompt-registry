# prompt-registry — Architecture

> **Valid-as-of:** 2026-06-09
> **Falsification-pointer:** Verify `.github/workflows/compile-and-deploy.yml` and `scripts/compile_prompts.py` before citing CI or compile behavior.
> **Review trigger:** 2026-09-09 or after compiler schema/workflow change.

## Role

Version-controlled prompt SSOT with dual delivery: human copy-paste (`prompts/**/*.md`) and programmatic consumption (`dist/prompts_latest.json` on GitHub Pages).

## Command authority

| Command | Purpose | CI parity |
|---|---|---|
| `make bootstrap` | `pip install -r requirements.txt` | yes (validate job step) |
| `make build` | `python scripts/compile_prompts.py` | yes |
| `make verify` | build + `scripts/ci-verify-footer.sh` | yes |
| `make lint` | alias for `make verify` | yes |

Local healthy path: `make verify`. Exit 0 = compile + footer guard passed.

## Artifact layout

| Path | Kind |
|---|---|
| `prompts/<domain>/*.md` | Source prompts (YAML frontmatter + fenced prompt body) |
| `dist/prompts_latest.json` | Generated master registry (gitignored locally; CI produces) |
| `dist/domains.json` | Generated domain routing catalog |
| `dist/prompts_v*.json` | Version-pinned snapshots |

## CI contract

`.github/workflows/compile-and-deploy.yml` — `validate` job runs compile + footer check on PR and push. `deploy` job publishes `dist/` to Pages on push to `main`.

No `.env` required for build/verify.
