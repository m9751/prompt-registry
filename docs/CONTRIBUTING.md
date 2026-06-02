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

```bash
git checkout -b feature/your-prompt-name
```

### 2. Create your prompt file

Place it in the correct domain folder under `prompts/`:

```
prompts/
├── product-delivery/       # Human-facing outputs, briefings, summaries
├── ai-engineering/         # Machine-readable outputs, structured extraction
└── systems-architecture/   # Technical parsing, transformation pipelines
```

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

Immediately after the frontmatter, add one (and only one) fenced code block containing the prompt:

````markdown
```
Your prompt text goes here.
Use {{Variable_Name}} for placeholders.
```
````

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

### 6. Bump the version (for edits to existing prompts)

If modifying an existing prompt, increment the `version` field in frontmatter:

| Change type | Version bump | Example |
| :--- | :--- | :--- |
| Minor wording tweak | Patch | `1.0.0 → 1.0.1` |
| New section or structural change | Minor | `1.0.0 → 1.1.0` |
| Complete rewrite or breaking change | Major | `1.0.0 → 2.0.0` |

### 7. Commit and open a PR

```bash
git add prompts/your-domain/your-file.md dist/ README.md
git commit -m "feat(prompts): add PRM-NBLM-005 quarterly summary extractor"
git push origin feature/your-prompt-name
gh pr create --base main --title "feat(prompts): add PRM-NBLM-005" --body "See PR template"
```

Fill out the PR template completely, including before/after LLM output samples.

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
