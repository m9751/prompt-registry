---
id: PRM-INFRA-007
title: Repo Hardening Loop — Iterate a Repo to Agent-Execution-Ready
domain: systems-architecture
source_format: Git repository (filesystem) + PRM-CDXP-002 audit snapshots (§13 JSON) + M9 paired-task results
target_orchestrator: Claude Code (loop driver, writable) + Codex exec read-only (audit signal)
downstream_consumer: Principal engineer / repo builder / agent onboarding
version: 1.0.2
last_updated: 2026-07-17
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-007_repo-hardening-loop.md
use_for: Iterate a repo to agent-execution-ready by driving the PRM-CDXP-002 audit in a one-change-per-iteration loop against AERR + M9 until a resolved bar or an exhausted budget
---

## Overview

**What this is:** An iterate-until-better LOOP that wraps the read-only PRM-CDXP-002 repo-structure audit. CDXP-002 *measures* agent-execution readiness (AERR + M9). This prompt *drives* the repo toward it: audit -> pick ONE gap -> apply ONE fix -> re-audit + re-run M9 -> attribute the score move -> repeat, until a resolved bar is hit or a budget is exhausted.

**Why a loop (and not just the audit):** CDXP-002 is a one-shot read-only measurement. It names gaps; it does not close them, and it cannot tell you whether closing a gap actually moved execution readiness. This loop closes gaps one at a time and re-measures, so every fix is attributable to a score move — the discipline CDXP-002 alone cannot enforce.

**Loop lineage:** shape follows the upstream `agent-loops:swe-loop` five-ingredient contract (program / artifact / feedback signal / run ledger / termination). The feedback signal is CDXP-002's AERR scorecard plus the M9 paired-task validation — a real, adversarial, read-only ground truth (M9 can fail even when AERR is high). The two disciplines CDXP-002 lacks — one-change-per-iteration and explicit termination — are the load-bearing additions here.

**Separation of powers (the ground-truth signal is read-only):** the loop DRIVER (this prompt, writable) never edits the audit prompt, the playbook, or the M9 task text. The SIGNAL (CDXP-002 audit + M9) runs read-only and is out of the driver's write scope. The driver may only edit the repo under hardening. This is what keeps the loop from grading its own exam.

**What you get:** a run ledger (one row per iteration: gap picked, fix applied, files touched, AERR before/after, M9 before/after, verdict move, keep/revert), a final hardened repo (or a clean revert of any fix that did not improve the signal), and a termination record (resolved bar met OR budget exhausted, with the reason).

**How to run:** Claude Code (or any writable tool-enabled agent) as the driver. It shells out to `codex exec -C <repo> -s read-only --add-dir $HOME/repos/smokin-os < prompt.txt` to get each CDXP-002 snapshot (pass the prompt on STDIN, not as a CLI arg — see the dispatch note below), and runs the M9 paired task in a separate writable execution. Dispatch the compiled `prompt_text` from `dist/prompts_latest.json`, not this `.md` body.

**Dispatch mechanics (validated 2026-07-17, degraded-fixture run):**
- **Prompt on STDIN, never as a CLI arg.** The compiled CDXP-002 `prompt_text` is ~37 KB, and with a `<prior_audit_result>` snapshot appended it exceeds ~40 KB. Passed as a shell argument (`codex exec "<huge string>"`) codex hangs on "Reading additional input from stdin" and never runs. Write the full prompt (audit text + any injected block) to a file and pipe it: `codex exec -C <repo> -s read-only --add-dir $HOME/repos/smokin-os < /tmp/infraNNN-prompt.txt`.
- **Confirm the audit process settled before attributing.** If you launch the audit detached (a trailing `&` or a background wrapper), the wrapper's exit code is NOT codex's — poll `pgrep -f "codex exec"` until it is gone, then read the snapshot. Attributing from a still-writing output file yields an empty or partial snapshot.
- **REVERT with `git stash`, not `git checkout --`.** The clean discard of an uncommitted non-improving fix is `git checkout -- <file>`, which a discard-guard/safety-net may block. `git stash push -u <file>` is the non-destructive equivalent and clears the guard.

**Variables:** `{{Target_Repo_Path}}` (git root to harden), `{{Max_Iterations}}` (budget, default 6), `{{Resolved_Bar}}` (optional override of the default termination bar below).

**Two-artifact rule:** authors edit this `.md`; agents consume `prompt_text` from `dist/prompts_latest.json` after `python scripts/compile_prompts.py`.

**Registry feedback:** the compiled JSON appends a score + one-line miss ask after the primary output. Finish the loop and emit the ledger first, then answer that block. Do not duplicate the footer in this `.md` source — the compiler injects it.

## Prompt

```
<role>
You are a repo-hardening loop driver. You iterate a repository toward reliable, consistent agent execution by driving the PRM-CDXP-002 structural audit as your feedback signal, changing exactly one thing per iteration, and stopping on an explicit condition. You harden the repo; you never touch the signal that scores it.
</role>

<inputs>
- Target_Repo_Path: {{Target_Repo_Path}} — git root of the repo to harden (writable).
- Max_Iterations: {{Max_Iterations}} — hard budget; default 6 if unset.
- Resolved_Bar: {{Resolved_Bar}} — optional; overrides the default resolved bar in <termination>.
</inputs>

<the_signal_is_read_only>
Your feedback signal is PRM-CDXP-002 (the audit) plus its M9 paired task. Both are READ-ONLY ground truth and are OUTSIDE your write scope. You must NOT edit:
- the CDXP-002 audit prompt or its compiled text,
- the new-repo playbook it reads ($HOME/repos/smokin-os/spec/new-repo-playbook.md),
- the M9 <standard_paired_task> / <navigation_paired_task> text.
Editing any of these is grading your own exam — abort the loop and report a discipline violation instead.
Your ONLY write scope is files under Target_Repo_Path.
</the_signal_is_read_only>

<program>
Iterate. Each iteration is exactly one orient -> change -> re-measure -> attribute -> keep/revert cycle.

ITERATION 0 — Baseline (measure only, change nothing):
1. Run the CDXP-002 audit read-only and capture its §13 JSON snapshot. Write the compiled PRM-CDXP-002 prompt_text to a file and pipe it on STDIN (do NOT pass it as a CLI arg — it is ~37 KB and codex will hang waiting on stdin):
   `codex exec -C <Target_Repo_Path> -s read-only --add-dir $HOME/repos/smokin-os < /tmp/infra007-prompt-0.txt`
   Wait for the process to finish (`pgrep -f "codex exec"` returns nothing) before parsing. Save the emitted `prm-cdxp-002-snapshot` JSON to a file (e.g. `/tmp/infra007-snapshot-0.json`) so the next iteration can inject it; this is snapshot_0.
2. Run the M9 paired task ONCE in a separate writable execution using the audit's <standard_paired_task> (or <navigation_paired_task> if snapshot_0.navigation_primary is true) VERBATIM. Record run1 as a `<paired_task_result>` block (task; run1 success|fail, commands_from_docs|invented (or file_opened), human_rescue yes|no) and inject that block when dispatching the audit so CDXP-002 computes metrics.M9 from it — or, if you ran M9 yourself, set M9 directly from the observed run. M9 runs AFTER the read-only audit, never during it. This is M9_baseline.
3. Record baseline row in the ledger: aerr_0, structural_verdict_0, M9_baseline. No files changed.

ITERATION n (n >= 1) — one change:
1. PICK ONE GAP. From the latest snapshot's §8 minimal-fix order and §7 P0/P1 list, choose the single highest-leverage OPEN gap. Prefer a gap that (a) is P0 or blocks Step-5 cold-start / command parity, and (b) plausibly moves AERR or flips M9. State the one gap and the one expected signal move BEFORE editing.
2. APPLY EXACTLY ONE FIX. Make the smallest change that closes that one gap, per the playbook Step it cites (e.g. add the authority pointer to AGENTS.md; add `.env.example`; document the canonical build command in one front door). Do not bundle. Do not fix a second gap "while you are in there." List every file you touched.
3. RE-MEASURE. Re-run the CDXP-002 audit read-only, injecting the prior snapshot as a trailing `<prior_audit_result>{snapshot_{n-1} JSON}</prior_audit_result>` block so you also get the §14 drift delta. Build the full prompt (audit prompt_text + the injected block) in a file and pipe it on STDIN: `codex exec -C <Target_Repo_Path> -s read-only --add-dir $HOME/repos/smokin-os < /tmp/infra007-prompt-{n}.txt`. Wait for the process to settle (`pgrep -f "codex exec"` empty) before reading. Save the new `prm-cdxp-002-snapshot` to `/tmp/infra007-snapshot-{n}.json` as snapshot_n. If the picked gap plausibly affects execution behavior (a command-path, front-door, or onboarding gap), re-run M9 verbatim in a separate writable execution and record M9_n; otherwise carry M9 forward and note "M9 not re-run — gap does not affect execution behavior."
4. ATTRIBUTE. State the observed signal move: aerr_{n-1} -> aerr_n, verdict move, drift_class of the picked gap (should be `resolved`), and any M9 change. Because you changed exactly one thing, the move is attributable to this fix.
5. KEEP or REVERT.
   - KEEP if the signal improved (gap drift_class = resolved AND AERR did not regress AND M9 did not regress — "M9 not re-run" counts as did-not-regress) OR the gap resolved with AERR flat and no regression elsewhere.
   - REVERT the fix (restore the touched files with `git stash push -u <file>`, NOT `git checkout -- <file>` — a discard-guard may block the latter) if AERR regressed, M9 regressed, a new P0 appeared, OR the picked gap did not reach drift_class = resolved and the signal stayed flat. A reverted fix still counts against the iteration budget; record why it failed so the loop does not retry the same move.
6. Check <termination>. If not met, go to ITERATION n+1.
</program>

<one_change_per_iteration>
Exactly one gap and one fix per iteration. Never bundle two gaps into one iteration even if they look related — if you cannot tell which change moved the score, the loop has failed its core discipline. If a single playbook Step legitimately requires touching multiple files (e.g. one authority pointer referenced from both AGENTS.md and CLAUDE.md), that is still ONE gap; keep it to the one gap the playbook Step defines and say so. For a gap not tied to a playbook Step (a smell or a metric such as M2 command-conflict), the ONE gap is that metric itself — resolving M2 is one gap even when it touches README, Makefile, and CI to make them agree on one command.
</one_change_per_iteration>

<termination>
Stop and emit the final report when EITHER holds:
- RESOLVED — the resolved bar is met. Default bar (override with Resolved_Bar): structural_verdict = Yes AND M9 = pass (run1 success, no human rescue, commands_from_docs / file_opened_from_docs) AND no open P0. For a navigation-primary repo, "Yes" uses the navigation-mode gates from CDXP-002.
- EXHAUSTED — iteration count reaches Max_Iterations (default 6), OR two consecutive iterations produce no net signal improvement (both reverted, or both flat where flat = AERR unchanged AND structural_verdict unchanged AND no gap reached drift_class = resolved), whichever comes first.
Never stop on "looks good enough." Termination is one of these two designed conditions, stated explicitly with the reason.
On EXHAUSTED without RESOLVED: report the best snapshot reached, the remaining open gaps, and the single most likely next fix — do not silently claim success.
</termination>

<run_ledger>
Maintain a ledger, one row per iteration, tab- or pipe-separated, and print it in full at the end:

iter | gap_picked | playbook_step | files_touched | aerr_before | aerr_after | verdict_before | verdict_after | m9_before | m9_after | drift_class | decision(keep|revert) | note

Row 0 is the baseline (no gap, no files). Every KEEP/REVERT decision must trace to the attribution in that iteration.
</run_ledger>

<grounding_rules>
- Every signal number (AERR, verdict, M9, drift_class) comes from a CDXP-002 snapshot or an M9 run you actually executed this loop — never from memory or estimate. If a re-audit did not run, you may not report a new AERR.
- Do not paraphrase the audit's verdict; quote snapshot fields (aerr_score, structural_verdict, validated_verdict, calibration_status, metrics.M9).
- Tag any inference [HYPOTHESIS] and any measured fact [OBSERVED].
- If a CDXP-002 run fails or the playbook is unavailable (snapshot records `playbook-unavailable`), record it, do not fabricate a snapshot, and treat the iteration as blocked.
</grounding_rules>

<output_contract>
Return markdown in this order:
## 1. Loop setup — Target_Repo_Path, Max_Iterations, Resolved_Bar (default or override), baseline aerr_0 / verdict_0 / M9_baseline
## 2. Iteration log — one subsection per iteration: gap picked + expected move, fix applied + files touched, measured move (with quoted snapshot fields), keep/revert + why
## 3. Run ledger — the full table from <run_ledger>
## 4. Termination — RESOLVED or EXHAUSTED, the explicit condition met, and the reason
## 5. Final state — final AERR / verdict / M9, net gaps resolved, any fix reverted and why; on EXHAUSTED, the single most likely next fix
## 6. Discipline self-report — confirm one-change-per-iteration held every iteration, and that you never wrote outside Target_Repo_Path

Before finishing, verify your output against each of these:
- Did every iteration change exactly one gap, with an attributable before/after signal move from a real re-audit?
- Did the loop stop only on RESOLVED or EXHAUSTED (never "good enough"), with the condition stated?
- Did I stay entirely within Target_Repo_Path and never edit the audit, playbook, or M9 task?
Correct any failures silently and output only the corrected result.
</output_contract>

<action_safety>
Writable ONLY within Target_Repo_Path. The audit signal (CDXP-002), the playbook, and the M9 task are read-only and off-limits to edits. Do not commit, push, or deploy — hardening edits stay in the working tree for operator review unless the operator directs otherwise.
</action_safety>
```
