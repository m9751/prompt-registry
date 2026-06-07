## Prompt ID(s) Affected

<!-- List all prompt IDs being added or modified. Example: PRM-NBLM-001, PRM-NBLM-004 -->

---

## Problem / Optimization Rationale

<!-- What problem does this change solve? What behavior are you improving?
     Be specific: "The previous prompt hallucinated table headers when slides had no data tables."
     Not acceptable: "Improved the prompt." -->

---

## Version Bump

| Prompt ID | Previous Version | New Version | Bump Type |
| :--- | :--- | :--- | :--- |
| PRM-NBLM-XXX | `x.x.x` | `x.x.x` | Patch / Minor / Major |

**SemVer justification:** <!-- Why this bump level? What changed structurally? -->

---

## Before: LLM Output Sample (old prompt)

<!-- Paste a real output from the OLD prompt here. Use a realistic test input.
     Do not fabricate output — if you don't have a before sample, explain why. -->

```
[paste before output here]
```

**Test input used:** <!-- Describe the input document/context -->

---

## After: LLM Output Sample (new prompt)

<!-- Paste a real output from the NEW prompt here, using the same test input. -->

```
[paste after output here]
```

---

## Compilation Checklist

- [ ] Branched from latest `origin/main` (not stale local main): `git fetch origin && git checkout -b feat/... origin/main`
- [ ] `python scripts/compile_prompts.py` ran locally with zero errors
- [ ] Spot-checked: opened `dist/prompts_latest.json`, confirmed this prompt's `prompt_text` ends with the feedback footer (`Score this prompt: 1 / 2 / 3`)
- [ ] `dist/prompts_latest.json` included in this PR
- [ ] README catalog auto-regenerated (no manual edits to the catalog section)
- [ ] **If adding a new domain:** added domain to `domain_order` in `compile_prompts.py`, `domain_labels` dict, `AGENTS.md` enum list, and `prompt_schema.json` enum — compiler will hard-fail CI if any of these are missing
- [ ] `version` field incremented in frontmatter per SemVer rules
- [ ] `last_updated` date set to today
- [ ] Prompt logged to `build.deliverables` on smokin-ops Supabase (`project_id: xuvdcygqyuajtlpavafr`) with `source='prompt-registry'` and `prompt_id` in metadata — use `execute_sql` after merge

> **Note for reviewers:** JSON consumers automatically receive the feedback footer appended to every `prompt_text`. This is injected by the compiler and is not present in the `.md` source file.
