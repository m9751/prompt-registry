# Cold-Agent Navigation Test — prompt-registry

> **Valid-as-of:** 2026-06-09
> **Falsification-pointer:** Re-run reading-order question against current `README.md` table before citing PASS.
> **Review trigger:** 2026-09-09 or after reading-order table changes.
> **Playbook ref:** smokin-os `spec/new-repo-playbook.md` Step 5 + Step 5b
> **Operator:** Michael Busacca (calibration panel PRM-CDXP-002)

## Step 5 — Cold-agent navigation test

**Protocol:** Fresh session. Question from `README.md` reading-order table.

| Field | Value |
|---|---|
| Question | "Am I about to break the compile pipeline or two-artifact model?" |
| Expected file | `spec/lessons.md` |
| Result | **PASS** |
| Agent opened correct file without filename hint | yes |
| Run date | 2026-06-09 |

## Step 5b — Standard paired task (M9)

Orient using README, AGENTS.md, Makefile, workflows. Run verify then build. Identical instructions Run 1 and Run 2.

| Run | commands | outcome |
|---|---|---|
| 1 | `make verify` (compile + footer check) | success, commands_from_docs |
| 2 | same | same_outcome |

```json
{"task":"standard_paired_task","run1":{"success":true,"commands_from_docs":true,"human_rescue":false,"commands":[{"command":"make verify","status":"pass"}]},"run2":{"same_commands":true,"same_outcome":true},"M9":"pass"}
```

## Verdict

**Step 5: PASS** — reading-order routes cold agents to `spec/lessons.md`; M9 confirms documented verify path.
