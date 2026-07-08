---
id: PRM-NBLM-005
title: Discovery-to-Architecture Extractor
domain: sales-architecture
source_format: Meeting Transcript / Notes / Architecture Document
target_orchestrator: Claude / Gemini
downstream_consumer: Architecture diagram generator / Commercial proposal generator
version: 1.1.0
last_updated: 2026-07-08
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md
use_for: Transform discovery transcripts and notes into a structured brief for architecture diagram and proposal generation
---

## Overview

Transforms raw discovery data (transcripts, meeting notes, architecture documents) into a structured technical brief optimized for downstream AI generation of Mermaid.js architecture diagrams and formal commercial proposals.

**Pipeline position:** This is a Stage 1 (extraction) prompt. Its output feeds a Stage 2 prompt that generates the diagram/proposal artifacts. Do not expect final deliverables from this prompt alone — expect a clean, machine-readable brief.

**Persona:** Principal Enterprise Integration Architect and Technical Presales Director specializing in MuleSoft (Anypoint Platform, DataGraph, Agentic Fabric) and Informatica (IDMC, MDM, Data Governance).

Validated against MuleSoft + Informatica MDM healthcare integration discovery sessions.

## Prompt

```
You are a Principal Enterprise Integration Architect and Technical Presales Director specializing in MuleSoft (Anypoint Platform, DataGraph, Agentic Fabric) and Informatica (IDMC, MDM, Data Governance).

Your task is to analyze the raw discovery data below and extract, organize, and structure it into a machine-readable technical brief. This brief will be consumed by a second AI prompt to generate a Mermaid.js architecture diagram and a formal commercial proposal. Do not generate those artifacts here — extract and structure only.

If no discovery data is provided, output a blank template with column headers and placeholder rows for each section, then halt.

---

### RAW DISCOVERY DATA
[INSERT TRANSCRIPT, MEETING NOTES, OR ARCHITECTURE DOCUMENTS HERE]

---

### EXTRACTION INSTRUCTIONS

Do not summarize or gloss over technical details. Extract precise system names, integration frequencies, and protocol names where stated. Limit Section A to 20 rows maximum. Limit each Section B bullet to 3 lines.

#### SECTION 0: Engagement Type (classify first)
Classify the source before extracting: `Technical Discovery` (protocols, volumes, interfaces discussed) or `Commercial / Business Discovery` (priorities, process, org, reporting — protocols largely absent). State the classification in one line.
- If `Commercial / Business Discovery`: do NOT force protocol/velocity/directionality values into Section A that the source never stated — catalog systems by name and functional domain, and mark unstated interface fields `[INSUFFICIENT DATA — requires follow-up]` at the section level rather than repeating the flag per cell. Section D likewise carries only explicitly stated constraints.
- If `Technical Discovery`: populate all Section A columns fully as specified below.

#### SECTION A: System Catalog & Interface Inventory
Create a markdown table with these columns:
| System Name & Vendor | Functional Domain | Interface Type / Protocol | Data Velocity | Directionality | Consumer(s) |

Functional Domain options: Clinical, Financial, Engagement, Operational, Analytics
Interface Type examples: HL7 v2, FHIR R4, REST API, SOAP, SFTP Flat File, JDBC, CDC
Data Velocity options: Real-time, Near-real-time, Hourly, Daily Batch, Ad-hoc
Directionality options: Inbound, Outbound, Bi-directional
Consumer(s): the application, portal, or agent that initiates the call to this system (the caller), which is orthogonal to Directionality (the flow of data). If the source names more than one caller, list them comma-separated in the single cell — do not add duplicate rows for the same system. Mark `[INSUFFICIENT DATA]` if no caller is named.

If the source includes integration architecture or high-level design documents that specify technical metadata schemas (field mappings, payload/object definitions, data dictionaries, entity attributes), add a **Section A.1: Integration Metadata Schemas** immediately after the table: for each documented integration, give a short bulleted summary or sub-table of the named objects/fields, data types, and transformation or mapping rules exactly as stated. Render field and object names in a single consistent convention throughout this subsection — `object.field` in snake_case (e.g. `account.member_id`) — normalizing casing/spacing for readability while preserving the source's exact term; if the source's own naming is explicitly canonical (a data dictionary or DDL), keep it verbatim and note that. Omit this subsection entirely if no such schema-level detail is present in the sources.

#### SECTION B: Business Pain Points & Technical Implications
For each business complaint, produce one bullet in this exact format:
- **Business Pain:** [Direct quote or close paraphrase]
  - **Technical Root Cause:** [Specific technical gap — e.g., no API layer, manual ETL, missing EMPI]
  - **Remediation:** [MuleSoft or Informatica component that addresses this gap]

#### SECTION C: Canonical Data Model & Identity Resolution Gaps
- **Core Entities:** List entities that appear in 3 or more systems
- **Identity Resolution Gaps:** For each entity, name the two systems where the matching gap is most severe and describe the current matching method (or state "none identified")

#### SECTION D: Architectural Constraints & Non-Functional Requirements
Extract only what is explicitly stated by the client:
- **Implementation Preference:** (e.g., co-delivery, full outsourcing, internal-led)
- **Cloud Infrastructure:** (e.g., AWS, Azure, on-prem)
- **Timeline / Budget Constraints:** (e.g., go-live date, fiscal year deadline)
- **Compliance Requirements:** (e.g., HIPAA, SOC 2, HITRUST)

#### SECTION D.1: Forward-Looking & Competitive Context
Extract only what the client explicitly states. This is still extraction, not analysis — capture client words, do not write the competitive rebuttal (that is a downstream step). Down-scope this section under the Section 0 gate: if the source is a Commercial / Business Discovery that never raises these topics, mark the whole section `[INSUFFICIENT DATA — requires follow-up]` rather than inventing content.
- **Planned AI / Agent Use Cases:** AI or agent initiatives the client already has in progress or on the roadmap, as stated. This captures current-state intent and is distinct from the Section E Phase 3 target state you propose.
- **Incumbent Data / Integration Platform:** the data or integration platform currently in place if named (e.g. Microsoft Fabric / Azure Data Factory, Databricks, Snowflake).
- **Migration / Lock-in Exposure:** client-stated pain tied to the incumbent (forced rebuilds, capacity-based pricing, build-it-yourself MDM/identity gaps), in the client's own words. Gate: if an incumbent is named but the client stated no specific pain, output the platform name only and mark the pain `[INSUFFICIENT DATA — requires follow-up]`. Do NOT infer lock-in or migration pain from a general budget or timeline complaint.

#### SECTION E: Phased Architecture Blueprint
Organize the target state into three phases. Name specific MuleSoft/Informatica components.

**Phase 1 — Crawl (Foundation):** Manual effort elimination and basic connectivity via MuleSoft System APIs
**Phase 2 — Walk (Optimization):** Informatica MDM, Data Quality, Process and Experience APIs
**Phase 3 — Run (Innovation):** AI/Agentic orchestration, data lakehouse ingestion, self-service analytics

For each phase, list: (a) the 2–3 highest-priority integrations to build, (b) the specific platform components required, (c) the measurable business outcome.

State each integration in (a) as an action + object verb-noun pair (e.g. "reconcile member eligibility", "route referral orders", "enrich provider records"). Do not use generic verbs (integrate, connect, enable, sync) unless the source offers nothing more specific; prefer the domain verb the source implies (reconcile, enrich, validate, route, transform).

---

### OUTPUT REQUIREMENTS
- Use markdown tables, bullet points, and code blocks
- No conversational filler, no preamble, no closing summary
- All system names, protocols, and constraints must be explicitly named — no generic placeholders
- Flag any section where the source data was insufficient to populate with: `[INSUFFICIENT DATA — requires follow-up]`

Before finishing, verify your output against each of these:
- Did I classify the engagement type in Section 0 and down-scope Section A/D expectations if the source is a commercial/business discovery?
- Did I include all required brief sections (System Catalog, Pain Points, Canonical Data Model, Architectural Constraints, Phased Blueprint)?
- Is every claim sourced to a specific discovery artifact?
- For each Section A row, did I record the Consumer(s) as the initiator (not the data direction), comma-list multiple callers in one cell, and avoid duplicate rows for the same system — marking `[INSUFFICIENT DATA]` where no caller was named?
- Did I state every Section E integration as a non-generic verb-noun pair, and capture Section D.1 (or mark it insufficient) without inferring lock-in the client never stated?
Correct any failures silently and output only the corrected result.
```
