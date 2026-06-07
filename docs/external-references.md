# External Prompt References

Curated external prompt libraries and resources. These are **not** owned or versioned here — they are read-only references for patterns you haven't yet engineered into the registry.

When you find a pattern from one of these worth keeping, register it as a proper `PRM-*` entry.

---

## NotebookLM Asset Generation

**NotebookLM Learner Pack** — DrMultivac / Christian Pean, MD
`https://github.com/DrMultivac/notebooklm-learner-pack`

29 copy-paste prompt patterns across 5 asset types, 6 audience lenses each:

| Asset Type | Count | Output feeds |
|---|---|---|
| Infographics | 10 | Napkin, Ideogram, Midjourney |
| Slide Decks | 5 | PPTX skill, Gamma |
| Audio Overviews | 5 | NotebookLM native Audio Overview |
| Video Storyboards | 4 | Veo3, Runway |
| Knowledge Tests | 5 | NotebookLM Flashcards + Quiz |

Audience lenses: ELI5, Newbie, Clinical, Operator, Finance, Deep Dive.

**When to use:** You've ingested a corpus into NotebookLM and want to generate explainer assets or knowledge tests. Check this pack before inventing prompts from scratch.

**Key files to read:**
- `SKILL.md` — workflow and grounding rules
- `references/prompt-architecture.md` — the 29 slot scaffolds
- `references/audience-lenses.md` — lens suffix patterns
