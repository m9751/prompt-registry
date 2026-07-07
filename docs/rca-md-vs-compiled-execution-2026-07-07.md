# RCA — Executed `.md` source instead of compiled `prompt_text`

**Date:** 2026-07-07
**Prompts involved:** PRM-NBLM-005, PRM-NBLM-006 (sales-architecture, Discovery-to-Presentation pipeline)

## What happened

An agent was asked to execute the two-stage pipeline against a discovery transcript. It read the prompt bodies from the `prompts/**/*.md` **source files** and executed those. The `.md` source deliberately does not contain the compiler-injected feedback footer (the two-artifact rule keeps the footer out of source). Running the `.md` therefore executed a prompt missing its terminal instruction block, and the self-critique / feedback loop never fired. The miss was only caught when the operator asked whether the prompts have a feedback loop.

## Root cause

The agent selected the artifact that was **easiest to read** (the `.md`, openable directly) rather than the artifact the pipeline **defines as executable** (the compiled `prompt_text` in `dist/prompts_latest.json`). AGENTS.md already stated the compiled JSON is "the artifact agents and apps consume," but that guidance was framed under *adding* a prompt, not *executing* one — there was no explicit run-surface rule. The agent had the fact available and did not consult it before executing.

## Contributing factor

The `.md` body reads as a complete prompt (persona, instructions, output requirements, verify checklist). The missing footer is an *absence*, and the agent verified *presence* (did it produce output) rather than *completeness* (did it run the whole defined artifact).

## Fix

1. AGENTS.md — added an **"Executing a prompt (run surface)"** section: execute compiled `prompt_text`, never the `.md` fenced body; confirm the run text ends with the feedback footer before claiming execution.
2. AGENTS.md `NEVER` block — added: never execute the `.md` fenced body as a prompt.
3. Corrected a stale footer-question line in AGENTS.md (`"What did it miss or get wrong?"` → the live `"What one change to this prompt's instructions would have improved this output?"`).

## Rule (durable)

**`.md` = edit surface. `dist/prompts_latest.json` `prompt_text` = run surface.** Resolve every prompt execution to the compiled artifact; the `.md` body is incomplete by design.
