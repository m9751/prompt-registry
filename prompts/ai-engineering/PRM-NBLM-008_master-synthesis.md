---
id: PRM-NBLM-008
title: NotebookLM Master Synthesis — Organize-for-AI Template
domain: ai-engineering
source_format: NotebookLM notebook (loaded sources)
target_orchestrator: NotebookLM
downstream_consumer: AI (Claude/Grok)
version: 1.2.0
last_updated: 2026-07-10
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/ai-engineering/PRM-NBLM-008_master-synthesis.md
use_for: Synthesize all loaded notebook sources into a definitive AI-optimized reference document
---

## Overview

The ORGANIZE half of a two-prompt pipeline. Paste into a NotebookLM chat (after PRM-NBLM-007 has gathered and the operator has imported sources). Notebook-only (strict grounding, no web crawl): it extracts and organizes everything already loaded into a single deep, structured reference optimized for downstream AI analysis — content-driven sections, exact metrics, practitioner intel, and official-vs-real-world conflicts surfaced side by side. Substitute `{{Subject}}` before running. Output is large on rich corpora.

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory output.*

## Prompt

```
# SYSTEM INSTRUCTION: Comprehensive Research Synthesis & Structural Deep-Dive

You are executing a master research synthesis on the following subject: {{Subject}}.

Your goal is to extract, organize, and synthesize every piece of relevant data within this notebook regarding this subject into a single, definitive reference document.

## Phase 1: Source Qualification Rules
1. Prioritize data extraction using this strict hierarchy:
   - (Tier 1) Official documentation, authoritative guides, and primary technical specifications.
   - (Tier 2) Hands-on practitioner content, real-world case studies, and public forum posts (e.g., Reddit, Stack Overflow, named engineering blogs) containing specific data, hard numbers, or named findings.
   - (Tier 3) The most recent sources where chronological relevance matters.
2. Conflict Resolution Rule: When official documentation and public forum/Reddit posts disagree on features, limitations, or behavior, document BOTH perspectives side-by-side (e.g., "Official Spec vs. Real-World Behavior"). Do not omit practitioner complaints in favor of pristine documentation, and vice versa.
3. Source Relevance Rule: A source may bundle content about unrelated third parties. Extract ONLY passages concerning {{Subject}}; silently discard unrelated entities — do not let them bleed into sections, metrics, or quotes. Extract from every relevant source, including slides, diagrams, screenshots, and architecture images — read on-slide labels, boxes, arrows, and printed metrics, and route them into the matching theme section. Do not skip an image-based source and do not quarantine slides in a separate section.

## Phase 2: Core Document Generation
### Step 1 — Content-Driven Architecture
Auto-discover the 8–12 major sub-topics or themes regarding {{Subject}} from the actual source content. Do not use generic, filler, or invented headings.
### Step 2 — Granular Section Development
For each discovered topic, write an exhaustive deep-dive section using this structure: ### [Discovered Topic Heading], then Core Specifications; Granular Metrics (exact numbers, dates, prices, explicit limits, preserved precisely); Proper Nouns; Comparison Tables (markdown, wherever sources present competing options or variations); Real-World Practitioner Intel (tips, "in-the-trenches" learnings, best practices from forums); Risk Mitigation (Things to Avoid, common pitfalls, anti-patterns, troubleshooting); Verbatim Quotes (where they add critical precision); Tradeoffs & Constraints.
SUBSECTION OMISSION RULE: if a subsection has no grounded content in the sources, OMIT that subsection heading entirely — do NOT print a placeholder, and do NOT pad it with restated facts or soft non-risks to fill the slot. If Tier-2 practitioner/forum sources are absent entirely, state that ONCE at the top of the document, then omit the empty subsections.
### Step 3 — Advanced Synthesis & Analytical Overlays
Append exactly three closing sections, and no others: 1. Gaps, Contradictions & Disconnects (esp. where real-world findings contradict official documentation); 2. Surprising Insights (non-obvious, counter-intuitive findings, clever workarounds, hidden patterns); 3. Missing Information & Blind Spots (what the sources fail to answer — the exact boundaries of the current data pool). The document ends after "Missing Information & Blind Spots."

## Execution Rules
- No Condensing or Summarizing: match source depth; vague descriptions or rounded numbers are useless.
- Strict Grounding: base every claim, metric, and finding strictly on the source text; do not use outside training data or assumptions.
- Format: output a single continuous Markdown document, zero preamble, zero conversational intro, zero outro. Start immediately with the first section header.
```
