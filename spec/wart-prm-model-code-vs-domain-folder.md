# WART: `PRM-<MODEL>` ID code does not match the domain-folder filing system

> Status: KNOWN ISSUE — documented 2026-06-16, deferred to a dedicated future session.
> Not blocking. Do not fix inline during unrelated work.

## The wart in one line
The prompt ID convention is `PRM-<MODEL>-<NNN>_<slug>.md`, implying the middle code is a model/tool. But prompts are actually filed by **domain folder** (`prompts/<domain>/`), and the `<MODEL>` code is used loosely as a family tag — so the ID scheme and the folder system disagree.

## Evidence (verified 2026-06-16)
The `NBLM` code is spread across **four different domains**:

| File | Folder (= domain) |
| :--- | :--- |
| PRM-NBLM-001 | product-delivery |
| PRM-NBLM-002 | ai-engineering |
| PRM-NBLM-003 | systems-architecture |
| PRM-NBLM-004 | systems-architecture |
| PRM-NBLM-005 | sales-architecture |
| PRM-NBLM-006 | sales-architecture |
| PRM-NBLM-007 | ai-engineering |
| PRM-NBLM-008 | ai-engineering |

So "NBLM" tells you nothing about where the prompt lives or what domain it serves. The folder is the real organizing axis; the ID prefix is decorative.

Note: every file's `domain:` frontmatter DOES match its folder (checked all 18 prompts). So the repo is internally consistent on folder↔frontmatter — the mismatch is specifically **ID-code ↔ domain**, not file-placement.

## Second-order symptom
Because the ID code is not the domain, a reader (or the skill router) cannot infer domain from the ID, and the per-folder `AGENTS.md` "Prompts in this domain" lists drift easily — two were already stale on 2026-06-16 (sales-architecture was missing PRM-NBLM-006-STANDALONE and PRM-EMAL-001 until this session fixed it).

## Third-order symptom (surfaced by PRM-EMAL-001)
There is **no domain for outbound email / outreach**. The 5-domain enum is: product-delivery, ai-engineering, systems-architecture, sales-architecture, presentation. A Gmail-email-builder prompt fits none cleanly; it was placed in `sales-architecture` as the "cleanest dirty shirt" (operator decision 2026-06-16). The taxonomy gap is real.

## What a future session should decide (do NOT pick one here)
1. **Is `<MODEL>` meaningful at all?** Options: (a) keep it but enforce it actually = model/tool; (b) replace it with a domain-derived code (e.g. `PRM-SALES-NNN`); (c) drop the code, use `PRM-NNN` global sequence + domain folder only.
2. **Renumber or leave legacy?** Any change to the code touches all 18 IDs + dist JSON + the README catalog + every memory/handoff that cites a PRM ID by name. High blast radius — likely "leave legacy, apply new scheme going forward."
3. **Add an `outreach`/`email` domain?** Or broaden `sales-architecture`'s `use_when` to cover non-presentation sales artifacts. Either resolves the EMAL-001 placement.

## Blast-radius warning for the fixer
Changing the ID scheme is NOT a rename-the-files job. Check, in order: `scripts/compile_prompts.py` (does it parse the code?), `scripts/prompt_schema.json` (is there an `id` pattern?), `dist/*.json` consumers, the README catalog generator, `domains.json` routing, and every external citation of a PRM ID. Read the producer + grep code consumers before touching anything (same discipline as FMD-059 / the catalog blast-radius lesson).

## Source
Surfaced during the PRM-EMAL-001 build (2026-06-16) when the operator asked "what is that folder and why are those PRM in it." Folder/domain mapping and the NBLM spread were verified live against the repo, not memory.
