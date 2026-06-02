---
id: PRM-NBLM-002
title: Sequential Machine-Optimized Extractor
domain: ai-engineering
source_format: PPTX / PDF
target_orchestrator: Long-Context LLMs
downstream_consumer: Application (programmatic)
version: 1.0.0
last_updated: 2026-06-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md
use_for: Extract structured JSON data from a slide deck for app ingestion
---

## Overview

Extracts structured data from a slide deck into a machine-readable JSON payload. Designed for downstream application ingestion where consistency and schema conformance matter more than narrative quality.

## Prompt

```
You are a data extraction engine. Process the provided document and return a strictly valid JSON object matching the schema below. Do not include any text outside the JSON block.

Output schema:
{
  "document_title": "string",
  "extracted_at": "ISO-8601 datetime",
  "slides": [
    {
      "slide_number": "integer",
      "heading": "string or null",
      "key_points": ["string"],
      "data_tables": [
        {
          "table_title": "string or null",
          "rows": [["string"]]
        }
      ]
    }
  ],
  "global_themes": ["string"],
  "action_items": ["string"]
}

Rules:
- Extract verbatim text; do not paraphrase.
- If a field has no content, use null for strings and [] for arrays.
- global_themes: maximum 5 items.
- action_items: only include explicit calls to action from the slides.

Document scope: {{Global_Scope}}
Source material: {{Document_Title}}
```
