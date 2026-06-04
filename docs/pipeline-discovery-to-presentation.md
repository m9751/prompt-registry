# Discovery-to-Presentation Pipeline
## Inter-Agent Transfer Specification

**Pipeline:** `PRM-NBLM-005` → `PRM-NBLM-006`  
**Last updated:** 2026-06-04

---

## Overview

This document describes the two-step decoupled pipeline for transforming raw enterprise discovery materials into a production-grade 6-slide technical architecture presentation.

When handling large volumes of unstructured enterprise discovery data — client meeting transcripts, architecture diagrams, legacy systems documentation — standard LLM generation patterns frequently suffer from context rot, structural collapse, and technical hallucination. This pipeline mitigates those risks by isolating the **Data Ingestion & Synthesis** phase from the **Code Generation & Presentation Layout** phase.

```
 [Raw Info Stack: Transcripts/Docs]
               │
               ▼
   [STEP 1: NotebookLM / Claude]  ◄── PRM-NBLM-005 (Discovery-to-Architecture Extractor)
               │
               ▼
  [Structured Technical Brief]   ◄── Sections A through E
               │
               ▼
     [STEP 2: Claude Chat]        ◄── PRM-NBLM-006 (6-Slide CIO Presentation Generator)
               │
               ▼
 [Final Presentation Code & Layout]
```

---

## Step 1 — Discovery-to-Architecture Extractor

**Prompt ID:** `PRM-NBLM-005`  
**Target orchestrator:** NotebookLM or Claude (long-context mode)  
**Input:** Raw discovery notes, meeting transcripts, vendor documents

### How to run

1. Upload your unstructured source materials into NotebookLM or a clean Claude context window.
2. Inject the `PRM-NBLM-005` prompt.
3. The AI evaluates the source materials and generates a **Structured Technical Brief** broken into five sections:

| Section | Contents |
| :--- | :--- |
| **Section A** | System Catalog & Interface Inventory (up to 20 rows) |
| **Section B** | Business Pain Points & Technical Implications |
| **Section C** | Canonical Data Model & Identity Resolution Gaps |
| **Section D** | Architectural Constraints & Non-Functional Requirements |
| **Section E** | Phased Architecture Blueprint (Crawl / Walk / Run) |

If source data is insufficient for any section, PRM-NBLM-005 flags it: `[INSUFFICIENT DATA — requires follow-up]`

---

## Step 2 — 6-Slide CIO Presentation Generator

**Prompt ID:** `PRM-NBLM-006`  
**Target orchestrator:** Claude (Advanced Chat or Claude Code)  
**Input:** The Structured Technical Brief from Step 1

### How to run

1. Open a fresh Claude session.
2. Paste the Structured Technical Brief from Step 1.
3. Immediately follow it with the `PRM-NBLM-006` prompt text.
4. Declare your `TARGET_ENGINE` at the top of your message: `marp` | `html` | `pptx` (default: `marp`).

Use this opening directive:

> "You are executing Step Two of the compilation pipeline. Using the Structured Technical Brief provided above as your exclusive factual grounding source, generate the complete text, layout blueprints, and typesetting code for the 6-slide presentation."

---

## Section-to-Slide Handoff

The table below maps each Section from Step 1's output to its target slide in Step 2's generator.

| Step 1 Output | Target Slide | Functional Role |
| :--- | :--- | :--- |
| **Section A & B** (System Catalog + Business Pain) | **Slide 1:** Current State Architecture Friction | Systemic bottlenecks → metric data cards (abandonment rate, wallet share leakage) |
| **Section B** (Technical Tool Boundaries) | **Slide 2:** Target State Reference Architecture | 4-Tier Horizontal Block Diagram (CARRY IT → INSPECT IT → MINT IT → ACTIVATE IT) |
| **Section E** (Runtime Topology / Phased Blueprint) | **Slide 3:** Runtime Execution & Integration Fabric | O(N²) P2P vs O(N) Facade Topology comparative matrix |
| **Section C & D** (MDM + Compliance) | **Slide 4:** Identity Resolution & Master Data Domain | ML resolution parameters, survivorship rules, compliance guardrails |
| **Section B & D** (Engagement + Privacy) | **Slide 5:** Engagement & Agentic Activation Layer | Front-office orchestration panel + bidirectional writeback compliance shield |
| **All Sections** | **Slide 6:** Architectural Decision Matrix | Platform-to-value map (Integration Complexity, Identity Accuracy, Compliance, Time-to-Value, Agentic Readiness) |

---

## Architectural Recommendations

### 1. Token minimization via semantic XML tagging

When passing Step 1 output into Step 2, wrap data points in explicit semantic XML tags:

```xml
<metric_abandonment>42%</metric_abandonment>
<compliance_tags>HIPAA, 42 CFR Part 2</compliance_tags>
```

Claude parses XML tags natively, preventing the layout generator from missing technical data points in long prompts.

### 2. Standardize the output target

Explicitly set `TARGET_ENGINE` in your Step 2 prompt:

- `marp` — Marp Markdown for terminal/programmatic generation
- `html` — HTML5 with MuleSoft CSS variables (baked into `PRM-NBLM-006`)
- `pptx` — python-pptx script for PowerPoint automation

### 3. RE-LAYOUT PROTOCOL

If generated content exceeds 4 bullet points in a single column or violates the Slide 1 60/40 split, `PRM-NBLM-006` automatically invokes `[RE-LAYOUT_PROTOCOL]` to split the text block dynamically. No human intervention required.

---

## Prompt Registry Links

| Prompt | Registry Entry | Raw Prompt |
| :--- | :--- | :--- |
| PRM-NBLM-005 | [View](../prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) | [Raw](https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) |
| PRM-NBLM-006 | [View](../prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) | [Raw](https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) |
| Compiled JSON | [prompts_latest.json](https://m9751.github.io/prompt-registry/prompts_latest.json) | — |
