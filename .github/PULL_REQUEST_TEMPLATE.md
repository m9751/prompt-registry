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

- [ ] `python scripts/compile_prompts.py` ran locally with no errors
- [ ] `dist/prompts_latest.json` updated in this PR
- [ ] README catalog auto-regenerated (no manual edits to the catalog section)
- [ ] `version` field incremented in frontmatter per SemVer rules
- [ ] `last_updated` date set to today
