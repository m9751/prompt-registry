---
id: PRM-NBLM-001
title: Slide-to-Human Briefing Master
domain: product-delivery
source_format: PPTX / PDF
target_orchestrator: NotebookLM
downstream_consumer: Human (copy-paste)
version: 1.0.0
last_updated: 2026-06-02
hosted_url: https://m9751.github.io/prompt-registry/prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md
---

## Overview

Converts a slide deck (PPTX or PDF) into a structured executive briefing document suitable for human consumption. Produces a narrative summary, key takeaways, and action items.

## Prompt

```
You are an expert business analyst. I am providing you with a slide deck.

Your task is to produce a structured executive briefing with the following sections:

1. **Executive Summary** (3-5 sentences): What is this deck about and what decision does it support?
2. **Key Findings** (bullet list, max 7 items): The most important data points and conclusions.
3. **Recommended Actions** (numbered list): Concrete next steps the reader should take.
4. **Open Questions**: Anything the deck raises but does not answer.

Rules:
- Use plain English. No jargon unless it was in the source material.
- Do not hallucinate data. If a number is not in the slides, do not include it.
- Keep the entire output under 500 words.

Source material: {{Document_Title}}
```
