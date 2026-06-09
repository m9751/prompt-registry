# systems-architecture

Technical parsing and transformation: architecture deck parsing, semantic compression, structured technical payloads for architect audiences.

## Routing

description: Prompts that parse, compress, or transform technical architecture artifacts — diagrams, decks, specs — into structured payloads for technical consumers (architects, engineers, downstream models).
use_when: The input is a technical artifact (architecture deck, HTML diagram, system spec) and the output is a structured technical payload, semantic extract, or compressed representation for an architect or engineering audience.
not_when: The output is a sales or executive presentation — use sales-architecture instead. The output is a plain human summary for non-technical readers — use product-delivery instead.

## Model Codes in this domain

- `NBLM` — NotebookLM / long-context LLM targets
- `CDXP` — Codex dispatch prompts (dispatched via Claude Code Agent tool, subagent_type="codex:codex-rescue")
- `INFRA` — Infrastructure and deploy hardening prompts (Claude Code orchestration)

## Prompts in this domain

- `PRM-NBLM-003` — HTML-Aware Slide Parser
- `PRM-NBLM-004` — Architecture Semantic Compressor
- `PRM-CDXP-001` — PowerShell Security Audit Framework — Endpoint Discovery Design
- `PRM-CDXP-002` — Repository Structure Audit — Skeleton, Not Content
- `PRM-INFRA-001` — Operational Hardening Deploy
