# Lessons — Running Log

> **Valid-as-of:** 2026-06-09
> **Falsification-pointer:** Verify `docs/rca-divergence-2026-06-02.md` and `AGENTS.md` anti-patterns before citing git workflow lessons.
> **Review trigger:** 2026-09-09 or after any compile/CI incident.

**STOP.** Read this before changing the compiler, CI workflow, or git branching model.

| Date | Lesson | Evidence |
|---|---|---|
| 2026-06-02 | Never create `main` as orphan — always merge scaffold branch. Orphan roots cause permanent divergence. | `docs/rca-divergence-2026-06-02.md` |
| 2026-06-09 | Two-artifact rule: `.md` is source; `dist/prompts_latest.json` is what agents consume. PR without compile is incomplete. | `AGENTS.md`, CI validate job |
| 2026-06-09 | Feedback footer is compiler-injected — never add to `.md` source. | `scripts/compile_prompts.py` |

**Full RCA archive:** `docs/rca-divergence-2026-06-02.md`
