# spec/README.md — prompt-registry navigation index

| File / path | Purpose |
|---|---|
| `README.md` | Cold-start identity, reading-order table, quick start, two-artifact model |
| `AGENTS.md` | Agent router — authority pointer, add-prompt procedure, NEVER rules |
| `CLAUDE.md` | Runtime behavioral stub — points to AGENTS.md |
| `STATUS.md` | Current phase and resumable open items |
| `Makefile` | Front door: `bootstrap`, `build`, `verify`, `lint` |
| `spec/architecture.md` | Compiler model, artifact layout, CI contract (significant spec) |
| `spec/lessons.md` | Running log of expensive mistakes — read before changing compile/CI |
| `spec/cold-agent-nav-test.md` | Step 5 + 5b cold-agent navigation test evidence |
| `scripts/compile_prompts.py` | Compiler — smallest documented build command |
| `scripts/prompt_schema.json` | Frontmatter JSON Schema |
| `scripts/ci-verify-footer.sh` | Footer guard — matches CI validate job |
| `.github/workflows/compile-and-deploy.yml` | CI: compile + footer check + Pages deploy |
| `docs/CONTRIBUTING.md` | Full contributor guide (detail behind front door) |
| `docs/SECURITY.md` | PAT scope and external access |
| `docs/rca-divergence-2026-06-02.md` | Orphan-main initialization RCA |
| `docs/PRM-CDXP-002-iterations.md` | PRM-CDXP-002 prompt iteration log |
| `prompts/<domain>/AGENTS.md` | Per-domain routing intent (feeds `domains.json`) |
