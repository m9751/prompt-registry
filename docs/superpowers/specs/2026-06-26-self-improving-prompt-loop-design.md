# Self-Improving Prompt Loop — Design Spec
**Date:** 2026-06-26
**Status:** Implemented

## Problem
The prompt registry compiled a feedback footer into every `prompt_text` asking for a score and a one-line critique. The question ("What did it miss or get wrong?") produced complaints, not actionable instruction changes. No mechanism existed to improve the `.md` source from that signal.

## Objective
Prompts get better over time based on real usage, without interrupting the main session and without autonomous write-back.

## Design

### Component 1 — Self-Critique Loop (inside each prompt fence)
Every prompt `.md` file contains 2–3 binary checks immediately before the closing fence. These checks are specific to that prompt's required output, procedural (not adjectival), and derived from its `use_for` field.

**Rules:**
- Maximum 3 checks — law of diminishing returns (GEPA research: 20–100 samples optimal, scaling degrades)
- Each check targets one dimension — prevents anchor bias from multi-dimension single pass
- Machine-output prompts (JSON/XML): omit "output only the corrected result" to avoid prose injection
- The model corrects failures silently before showing output — no session interruption

**Exit condition:** when a prompt passes all its own checks on first run, no corrections fire, the loop naturally decays.

### Component 2 — Updated Feedback Footer Question
Compiler (`scripts/compile_prompts.py`) injects at the end of every `prompt_text`:

```
Score this prompt: 1 (poor) / 2 (adequate) / 3 (excellent)
What one change to this prompt's instructions would have improved this output? (one line)
```

This replaces the previous "What did it miss or get wrong?" question. The new question asks for a specific instruction change — actionable input for a PR — rather than a complaint.

### Component 3 — Human-Gated Write-Back
The footer answer is read by the operator. If valid, the operator opens a PR against the `.md` source with the suggested change and a patch version bump. CI compiles and deploys automatically on merge.

No autonomous PR creation — the adversarial review (Codex) found four fatal flaws in autonomous write-back: worker self-judges, no write-access guarantee, undefined version gate, and no anti-cheat guard. Human judgment is the gate.

## Architecture Decisions
| Decision | Rationale |
|---|---|
| No cron, no scheduled digest | Crons are fragile; manual review is simpler and appropriate at 20-prompt scale |
| No `feedback.jsonl` | Removed — the footer question is the signal; storing structured feedback adds infra with no current consumer |
| No autonomous PR | Adversarial review found it unshippable — self-judging worker, no write-access guarantee |
| Checks inside fence, not a separate section | Compiler validates exactly one fence per `.md`; a second section outside the fence would require compiler changes |

## What Changed
- `scripts/compile_prompts.py` — footer question updated (line 50)
- All 20 `prompts/**/*.md` files — self-critique block added inside each fence
- `docs/CONTRIBUTING.md` — step 4a added making self-critique block mandatory for new prompts

## Research Sources
- Obsidian clipping: "The Prompt Loop Trick" (getprompted.ai) — self-imposed loop / autoregressive self-critique pattern
- Downloaded: "Transitioning to Prompt-as-Policy" — GEPA findings, length regularization, 20–100 sample optimum
- Downloaded: "Architecting Autonomous Prompt Optimization" — Worker-Judge pattern, rubric design (procedural not adjectival), anti-cheat guards
- Anthropic prompt engineering docs — self-check pattern endorsed ("Before you finish, verify your answer against [test criteria]")
