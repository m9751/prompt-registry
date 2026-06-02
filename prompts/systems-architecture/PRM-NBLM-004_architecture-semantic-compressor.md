---
id: PRM-NBLM-004
title: Architecture Semantic Compressor
domain: systems-architecture
source_format: HTML DOM
target_orchestrator: NotebookLM / Long-Context LLMs
downstream_consumer: Application (XML payload) / LLM downstream analysis
version: 1.1.0
last_updated: 2026-06-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md
---

## Overview

Parses an HTML architecture deck into an ultra-dense, token-compressed semantic payload for downstream LLM analysis. Groups output by architectural component, system, or logical domain — not by literal slide sequence — to prevent output truncation and maximize analytical density. Data flows are grouped by system boundary, not step number.

Validated against a MuleSoft + Informatica MDM + Salesforce Data Cloud healthcare identity resolution architecture deck. Version 1.0.0 produced sequential step output; v1.1.0 adds system-boundary grouping instruction to [DATA_FLOWS], which surfaced additional findings (Escalation_Tail_Overhead) and improved MDM layer detail in live testing.

## Prompt

```
Parse the uploaded HTML architecture deck into an ultra-dense, token-compressed semantic payload for downstream LLM analysis. Group data by architectural component, system, or logical domain rather than literal sequential slides to prevent output truncation. Group [DATA_FLOWS] by system boundary (e.g., MuleSoft layer, MDM layer, engagement layer) rather than sequential step numbers.

Formatting Constraints: Use minimal XML wrappers. Avoid prose, introductory filler, and markdown formatting inside the tags. Use compact key-value pairs. Start the payload immediately.

Payload Structure:

<core_logic>
[IDENTITY_RULES]: [Exact logic, matching rules, or reconciliation criteria mentioned]
[DATA_FLOWS]: [Group by system boundary, not step number. Each group: SYSTEM_NAME=flow description]
</core_logic>

<gaps_and_risks>
[Explicit architectural blind spot, missing system requirement, or unaddressed constraint]
</gaps_and_risks>
```
