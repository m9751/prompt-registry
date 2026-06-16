---
id: PRM-NBLM-007
title: NotebookLM Deep Research — Discovery / Gather Prompt
domain: ai-engineering
source_format: Subject (free text)
target_orchestrator: NotebookLM
downstream_consumer: AI (Claude/Grok)
version: 1.0.0
last_updated: 2026-06-16
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/ai-engineering/PRM-NBLM-007_deep-research-discovery.md
use_for: Gather best-practice and practitioner web sources on any subject into a NotebookLM notebook for AI analysis
---

## Overview

The GATHER half of a two-prompt pipeline. Paste into a NotebookLM chat to steer the Deep Research agent: it crawls the web (official docs + Reddit/HN/practitioner forums), ranks candidates by authority tier, and surfaces them in the source panel for the operator to import. Pair with PRM-NBLM-008 (synthesis) which organizes the imported corpus for AI analysis. Substitute `{{Subject}}` before running.

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory output.*

## Prompt

```
Run a Deep Research web search to gather the highest-signal sources on the following subject, then surface them in the source panel for me to import: {{Subject}}.

Goal: build a corpus that lets a downstream AI produce a definitive best-practices reference — how it works, what to do, and what to avoid. Prioritize implementation-grade detail over marketing.

Source priorities (gather a balanced ranked mix):
1. Official / primary (Tier 1): vendor documentation, official guides, primary technical specs, release notes, official repos.
2. Practitioner / in-the-trenches (Tier 2): Reddit threads (relevant subreddits), Hacker News discussions, named engineers' technical blogs, conference talks, and real-world case studies — specifically ones with hard numbers, named findings, gotchas, "things I wish I knew," and failure stories.
3. Recency (Tier 3): prefer the most current sources where the subject changes over time; flag anything dated.

Explicitly seek out (highest value — do not skip): best practices from people who run this in production; tips and clever workarounds from forums; things to avoid — common pitfalls, anti-patterns, footguns, and known failure modes; and disagreements between official docs and real-world practitioner experience.

Exclude: pure marketing pages, content-farm SEO listicles, and unsourced opinion with no specific findings.

Coverage target: cast a wide net (aim for 30+ candidate sources), rank by the priority tiers above, and surface them so I can import the strongest. In your reply, tell me roughly how many you found, the Tier-1 vs Tier-2 split, and any obvious gap where you could not find good sources.
```
