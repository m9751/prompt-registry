# ai-engineering

Machine-readable outputs: structured extracts, sequential parsers, semantic compressors for LLM pipelines.

## Routing

description: Prompts that produce structured, machine-readable outputs consumed by downstream AI systems, pipelines, or automation — not human readers.
use_when: The output is JSON, a structured extract, a compressed semantic payload, or any artifact consumed programmatically by another model or system. The downstream consumer is a model or pipeline, not a human.
not_when: The output is a human-readable briefing or summary — use product-delivery instead. The output involves architecture parsing for a presentation — use systems-architecture instead.

## Prompts in this domain

- `PRM-NBLM-002` — Sequential Machine Extractor
