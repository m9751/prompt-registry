---
id: PRM-NBLM-004
title: Architecture Semantic Compressor
domain: systems-architecture
source_format: HTML DOM
target_orchestrator: NotebookLM / Long-Context LLMs
downstream_consumer: Application (XML payload) / LLM downstream analysis
version: 1.2.0
last_updated: 2026-07-08
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md
use_for: Extract system boundaries, data flows, and gaps from an HTML architecture deck
---

## Overview

Parses an HTML architecture deck into an ultra-dense, token-compressed semantic payload for downstream LLM analysis. Groups output by architectural component, system, or logical domain — not by literal slide sequence — to prevent output truncation and maximize analytical density. Data flows are grouped by system boundary, not step number.

Validated against a MuleSoft + Informatica MDM + Salesforce Data Cloud healthcare identity resolution architecture deck. Version 1.0.0 produced sequential step output; v1.1.0 adds system-boundary grouping instruction to [DATA_FLOWS], which surfaced additional findings (Escalation_Tail_Overhead) and improved MDM layer detail in live testing. Version 1.2.0 adds three fixes from a 2026-07-08 live run: (1) a `[PLATFORM_BOUNDARIES]` bucket so a can/cannot capability matrix has a home instead of being smeared across [DATA_FLOWS] and gaps; (2) a split of `<gaps_and_risks>` into `[DOCUMENTED_LIMITS]` (limits the deck states about itself) vs `[UNADDRESSED_RISKS]` (blind spots the deck never raises), so a reader can tell architectural honesty from oversight; (3) a preserve-qualifiers instruction so compression does not strip legally load-bearing hedges (e.g. FCA reckless-disregard, "not a single mismatch alone").

## Prompt

```
Parse the uploaded HTML architecture deck into an ultra-dense, token-compressed semantic payload for downstream LLM analysis. Group data by architectural component, system, or logical domain rather than literal sequential slides to prevent output truncation. Group [DATA_FLOWS] by system boundary (e.g., MuleSoft layer, MDM layer, engagement layer) rather than sequential step numbers.

Formatting Constraints: Use minimal XML wrappers. Avoid prose, introductory filler, and markdown formatting inside the tags. Use compact key-value pairs. Start the payload immediately. When compressing, preserve legally or clinically load-bearing qualifiers verbatim (e.g. liability standards, scope hedges like "not a single X alone", regulatory conditions) — density must not strip a qualifier that changes what a claim means.

Payload Structure:

<core_logic>
[IDENTITY_RULES]: [Exact logic, matching rules, or reconciliation criteria mentioned]
[DATA_FLOWS]: [Group by system boundary, not step number. Each group: SYSTEM_NAME=flow description]
[PLATFORM_BOUNDARIES]: [Capability matrix. One entry per system: SYSTEM_NAME=can [what it does] / cannot [what it explicitly does not do]. This is where comparison tables and capability-coverage claims live — not [DATA_FLOWS] and not gaps.]
</core_logic>

<gaps_and_risks>
[DOCUMENTED_LIMITS]: [Constraints the deck states about ITSELF — limits it openly acknowledges. Each: short label = the stated limit.]
[UNADDRESSED_RISKS]: [Blind spots the deck never raises — missing requirements, unstated failure modes, or constraints it glosses over. Each: short label = the risk.]
</gaps_and_risks>

Before finishing, verify your output against each of these:
- Did I group data flows by system boundary, not by slide sequence?
- Did I put capability can/cannot claims in [PLATFORM_BOUNDARIES], not in [DATA_FLOWS] or gaps?
- Did I separate limits the deck acknowledges ([DOCUMENTED_LIMITS]) from blind spots it never raises ([UNADDRESSED_RISKS])?
- Did I preserve every load-bearing qualifier rather than compressing it away?
- Is every system boundary named and scoped?
Correct any failures silently.
```
