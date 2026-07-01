# Contributing to the Prompt Registry

This document explains how to add, edit, and publish prompts in the registry.

---

## Prerequisites

```bash
git clone https://github.com/m9751/prompt-registry.git
cd prompt-registry
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Adding a New Prompt

### 1. Create a branch

Always branch from the latest `origin/main` — a stale local main is the most common cause of missing compiler output in PRs:

```bash
git fetch origin && git checkout -b feat/your-prompt-name origin/main
```

### 2. Create your prompt file

Place it in the correct domain folder under `prompts/`:

```
prompts/
├── product-delivery/       # Human-facing outputs, briefings, summaries
├── ai-engineering/         # Machine-readable outputs, structured extraction
├── systems-architecture/   # Technical parsing, transformation pipelines
├── sales-architecture/     # Discovery extraction, solution architecture, sales assets
└── presentation/           # Slide decks (HTML, Google Slides, deck re-render)
```

The authoritative domain enum is defined in `AGENTS.md` (§ frontmatter `domain` field) — keep this list in sync with it.

File naming convention: `PRM-<MODEL>-<NNN>_<slug>.md`

Example: `PRM-NBLM-005_quarterly-summary-extractor.md`

### 3. Add required frontmatter

Every prompt file **must** begin with this YAML block. All fields are required.

```yaml
---
id: PRM-NBLM-005
title: Quarterly Summary Extractor
domain: product-delivery
source_format: PPTX / PDF
target_orchestrator: NotebookLM
downstream_consumer: Human (copy-paste)
version: 1.0.0
last_updated: 2026-06-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/product-delivery/PRM-NBLM-005_quarterly-summary-extractor.md
use_for: Convert a quarterly slide deck into an executive summary
---
```

### 4. Add the prompt text in a fenced code block

Add one (and only one) fenced code block containing the prompt. By convention it follows the frontmatter and any human-facing `## Overview` / branding-token section (see PRM-PRES-001/003, PRM-NBLM-006-STANDALONE) — the fence need not be the first element after the frontmatter, but it must be the sole fenced block:

````markdown
```
Your prompt text goes here.
Use {{Variable_Name}} for placeholders.
```
````

### 4a. Add a self-critique block inside the fence (mandatory)

Every prompt must end its fenced block with a self-critique block — 2 to 3 binary checks specific to what this prompt is required to produce. Place it immediately before the closing ` ``` `.

```
Before finishing, verify your output against each of these:
- [Binary check 1 derived from this prompt's required output]
- [Binary check 2 derived from this prompt's required output]
- [Binary check 3 — optional, only if genuinely distinct]
Correct any failures silently and output only the corrected result.
```

Rules:
- Each check must be binary (pass/fail), procedural, and specific to this prompt's output — not generic
- Maximum 3 checks — more degrades model attention
- For strict machine-output prompts (JSON, XML): omit "and output only the corrected result" to avoid injecting prose into the output
- Do NOT add the feedback footer here — the compiler injects it automatically

### 5. Run the compiler locally

```bash
python scripts/compile_prompts.py
```

This will:
- Validate your frontmatter against the JSON Schema
- Check for duplicate IDs
- Regenerate `dist/prompts_latest.json`
- Update the README catalog table

Fix any `VALIDATION ERROR` messages before proceeding.

**After running, open `dist/prompts_latest.json` and spot-check your prompt's `prompt_text` field.** It must end with the feedback footer (`Score this prompt: 1 / 2 / 3`). The compiler injects this automatically — do not add it to the `.md` source. If it's missing, you likely have a compile error or are reading a stale artifact.

### 6. Bump the version (for edits to existing prompts)

If modifying an existing prompt, increment the `version` field in frontmatter:

| Change type | Version bump | Example |
| :--- | :--- | :--- |
| Minor wording tweak | Patch | `1.0.0 → 1.0.1` |
| New section or structural change | Minor | `1.0.0 → 1.1.0` |
| Complete rewrite or breaking change | Major | `1.0.0 → 2.0.0` |

### 7. Log to Supabase

After the PR merges, log the prompt to `build.deliverables` on smokin-ops:

```python
# Via Claude Code MCP (execute_sql, project_id: xuvdcygqyuajtlpavafr)
INSERT INTO build.deliverables (title, type, url, description, source, trigger_phrase, status, build_state, build_state_changed_at, metadata)
VALUES (
  'PRM-XXX-NNN Title',
  'prompt',
  'https://m9751.github.io/prompt-registry/prompts_latest.json',
  'use_for value from frontmatter',
  'prompt-registry',
  'PRM-XXX-NNN',
  'shipped', 'complete', now(),
  jsonb_build_object('version', '1.0.0', 'prompt_id', 'PRM-XXX-NNN')
);
```

This keeps the prompt findable via `/find` and the territory deliverables audit.

### 8. Commit and open a PR

```bash
git add prompts/your-domain/your-file.md dist/ README.md
git commit -m "feat(prompts): add PRM-NBLM-005 quarterly summary extractor"
git push origin feature/your-prompt-name
gh pr create --base main --title "feat(prompts): add PRM-NBLM-005" --body "See PR template"
```

Fill out the PR template completely, including before/after LLM output samples.

---

## Two-Artifact Rule

Registry PRs always touch two artifacts, not one:

| Artifact | What it is | Who uses it |
| :--- | :--- | :--- |
| `prompts/.../*.md` | Authorable source | Authors, GitHub copy-paste |
| `dist/prompts_latest.json` | Compiled contract | Agents, apps, automation |

The `.md` is what you write. The JSON is what everything else consumes. A PR that only modifies the `.md` without regenerating the JSON is incomplete — CI will catch this, but catch it yourself first by running the compiler and reading the output.

---

## Prompt Feedback (Self-Improvement)

Every compiled `prompt_text` in `dist/prompts_latest.json` ends with an automatically injected feedback footer:

```
---
⬆️ Primary response above.
Score this prompt: 1 (poor) / 2 (adequate) / 3 (excellent)
What did it miss or get wrong? (one line)
```

**Do not add this to the `.md` source.** The compiler appends it during every compile run. This design means:
- The `.md` file stays clean and authorable
- Every agent or app that pulls the JSON always gets the feedback request
- Feedback footers stay consistent without per-prompt maintenance

If a prompt spec says "produce no other prose" (like strict output-format prompts), add one line in the prompt's Overview section:

> *Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory checklist.*

This prevents agents from treating the footer as contradictory to the output rules.

---

## Updating the Catalog

The README catalog is **auto-generated** by `compile_prompts.py`. Never edit the section between `<!-- PROMPT_CATALOG_START -->` and `<!-- PROMPT_CATALOG_END -->` manually.

---

## Variable Substitution

Prompts can include `{{Variable_Name}}` placeholders. At runtime, applications use `utils/variable_parser.py`:

```python
from utils.variable_parser import parse_prompt

prompt = parse_prompt(
    open("prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md").read(),
    {"Document_Title": "Q3 Board Deck"}
)
```
