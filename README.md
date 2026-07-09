# 🏛️ Enterprise Prompt Registry

Welcome to the central command center for our organization's engineered AI prompts. This repository is the Single Source of Truth (SSOT). Prompts here are version-controlled, performance-tested, and optimized for both human copy-pasting and direct programmatic application calls.

---

## Reading order

| If you are asking… | Start here |
|---|---|
| "How do I compile and verify a prompt change?" | **Quick start** below → `make verify` |
| "How do I add or edit a prompt?" | [`AGENTS.md`](AGENTS.md) |
| "Am I about to break the compile pipeline?" | [`spec/lessons.md`](spec/lessons.md) — STOP |
| "What's the architecture / CI contract?" | [`spec/architecture.md`](spec/architecture.md) |
| "What's current state?" | [`STATUS.md`](STATUS.md) |
| "Full contributor detail?" | [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) |
| "Security / PAT access?" | [`docs/SECURITY.md`](docs/SECURITY.md) |

## Quick start

```bash
git clone https://github.com/m9751/prompt-registry.git ~/repos/prompt-registry
cd ~/repos/prompt-registry
make bootstrap
make verify          # compile + footer check — exit 0 = healthy
```

| Command | When |
|---|---|
| `make bootstrap` | First clone — install Python deps |
| `make build` | Compile prompts → `dist/` only |
| `make verify` | **Default healthy path** — build + footer guard (CI parity) |
| `make lint` | Alias for `make verify` |



Production JSON: `https://m9751.github.io/prompt-registry/prompts_latest.json`

## For Claude landing here (read before editing)

1. **Read `AGENTS.md` first** — authority pointer and add-prompt procedure live there.
2. **Two-artifact rule:** edit `prompts/**/*.md`, then `make verify` — agents consume JSON, not markdown alone.
3. **Never add feedback footer to `.md`** — compiler injects it; verify in `dist/prompts_latest.json`.
4. **Branch from `origin/main`** — see `spec/lessons.md` for orphan-main RCA.
5. **Open a PR** — CI runs the same path as `make verify`.

## Boundary — what is NOT here

- **Claude config / hooks / skills** — [`claude-config`](https://github.com/m9751/claude-config) owns `~/.claude/` mirror
- **Platform OS index** — [`smokin-os`](https://github.com/m9751/smokin-os) owns stack catalog and hook registry spec
- **Territory data / deliverables** — SmokinTerritory Supabase
- **Authoring-only without compile** — agents and apps consume `dist/prompts_latest.json`, not raw `.md` alone


---

## 📖 How to Use This Registry

### 👥 For Humans (Copy-Paste)
1. Locate your functional domain in the **Prompt Catalog Matrix** below.
2. Click the link in the **Prompt Title** column to open the file.
3. Hover over the top-right corner of the code block containing the prompt text and click the **"Copy raw contents"** button in GitHub.
4. Paste it into your target AI model interface (e.g., NotebookLM, Claude, ChatGPT).

### 🤖 For Applications (Auto-Pull)
Applications interact with the compiled registry rather than browsing individual files.

- **Production Master Endpoint:** `https://m9751.github.io/prompt-registry/prompts_latest.json`
- **Versioned Pinning Endpoint:** `https://m9751.github.io/prompt-registry/prompts_v{VERSION}.json`

To fetch programmatically:
```bash
curl -s https://m9751.github.io/prompt-registry/prompts_latest.json | jq '.prompts[] | select(.domain == "product-delivery")'
```

---

## 🗂️ Prompt Catalog Matrix

> **Auto-generated** — do not edit this section manually. Run `python scripts/compile_prompts.py` to regenerate.

<!-- PROMPT_CATALOG_START -->

### 🚀 Product & Delivery
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-001` | [Slide-to-Human Briefing Master](prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md) | Convert a slide deck into a human-readable executive summary | PPTX / PDF | NotebookLM | `1.0.0` | [View File](prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md) |
| `PRM-NBLM-010` | [NotebookLM Usage Patterns — 20 Prompt Templates](prompts/product-delivery/PRM-NBLM-010_notebooklm-usage-patterns.md) | Pick the right prompt template for a NotebookLM task across research, content creation, learning, brainstorming, and deep reading | Any (documents, PDFs, research papers, feedback, meeting notes, training materials) | NotebookLM | `1.0.0` | [View File](prompts/product-delivery/PRM-NBLM-010_notebooklm-usage-patterns.md) |
| `PRM-PDLV-006` | [Static Guide Overview Video — Agent System Prompt](prompts/product-delivery/PRM-PDLV-006_static-guide-overview-video.md) | Build or rebuild a narrated overview video embedded in a static HTML product guide | HTML guide URL + scene spec (JSON/YAML) + image captures | Claude Code / Cursor Agent | `1.1.0` | [View File](prompts/product-delivery/PRM-PDLV-006_static-guide-overview-video.md) |

### 🧠 AI & Integration Engineering
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-AENG-001` | [Self-Critique Loop Installer](prompts/ai-engineering/PRM-AENG-001_self-critique-loop-installer.md) | Add a self-critique loop to any skill or prompt — reads the artifact's use_for and required output, writes 2-3 binary checks, inserts the block at the correct location | SKILL.md or prompt .md file (pasted text) | Claude Code | `1.1.0` | [View File](prompts/ai-engineering/PRM-AENG-001_self-critique-loop-installer.md) |
| `PRM-MMLM-006` | [Presentation Slide Visual and Textual Markdown Extractor](prompts/ai-engineering/PRM-MMLM-006_presentation-markdown-extractor.md) | Analyzing presentation screenshots to extract literal text hierarchies alongside deep visual-narrative interpretations into clean Markdown. | PNG / JPG | Multimodal LLM (e.g., GPT-4o, Claude 3.5 Sonnet) | `1.0.1` | [View File](prompts/ai-engineering/PRM-MMLM-006_presentation-markdown-extractor.md) |
| `PRM-NBLM-002` | [Sequential Machine-Optimized Extractor](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) | Extract structured JSON data from a slide deck for app ingestion | PPTX / PDF | Long-Context LLMs | `1.0.0` | [View File](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) |
| `PRM-NBLM-007` | [NotebookLM Deep Research — Discovery / Gather Prompt](prompts/ai-engineering/PRM-NBLM-007_deep-research-discovery.md) | Gather best-practice and practitioner web sources on any subject into a NotebookLM notebook for AI analysis | Subject (free text) | NotebookLM | `1.0.0` | [View File](prompts/ai-engineering/PRM-NBLM-007_deep-research-discovery.md) |
| `PRM-NBLM-008` | [NotebookLM Master Synthesis — Organize-for-AI Template](prompts/ai-engineering/PRM-NBLM-008_master-synthesis.md) | Synthesize all loaded notebook sources into a definitive AI-optimized reference document | NotebookLM notebook (loaded sources) | NotebookLM | `1.1.2` | [View File](prompts/ai-engineering/PRM-NBLM-008_master-synthesis.md) |

### 🛠️ Systems Architecture
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-CDXP-001` | [PowerShell Security Audit Framework — Endpoint Discovery Design](prompts/systems-architecture/PRM-CDXP-001_ps-security-audit-framework.md) | Design a non-remediating PowerShell endpoint discovery script for auditing security posture across application control/CLM, security policy, audit policy/telemetry, and JEA endpoint configuration | Text specification (compliance control IDs + scope description) | Claude (authoring) → Codex (review against smokin-knowledge PS hard rules) | `1.0.0` | [View File](prompts/systems-architecture/PRM-CDXP-001_ps-security-audit-framework.md) |
| `PRM-CDXP-002` | [Repository Structure Audit — Skeleton, Not Content](prompts/systems-architecture/PRM-CDXP-002_repo-structure-audit.md) | Measure whether a repo enables reliable, consistent agent execution — structural readiness scorecard with AERR metrics, not business-logic review | Git repository (filesystem) | Codex exec (read-only) | `1.8.0` | [View File](prompts/systems-architecture/PRM-CDXP-002_repo-structure-audit.md) |
| `PRM-INFRA-001` | [Operational Hardening Deploy](prompts/systems-architecture/PRM-INFRA-001_operational-hardening-deploy.md) | Review code for correctness then execute a hardened deploy using the Phased Build Protocol | Code files + ADR + deploy plan | Claude Code | `2.6.0` | [View File](prompts/systems-architecture/PRM-INFRA-001_operational-hardening-deploy.md) |
| `PRM-INFRA-002` | [Make Every Derived Index Self-Healing](prompts/systems-architecture/PRM-INFRA-002_fable-derived-index-self-healing.md) | Audit every derived index in a multi-repo Claude Code operating system, wire un-triggered ones to self-heal on drift, and produce a durable register with automatic triggers and freshness invariants for each index | Derived-index register (register.md) + repo file tree | Claude Sonnet 4.6 (session-scoped; operator runs interactively) | `1.2.1` | [View File](prompts/systems-architecture/PRM-INFRA-002_fable-derived-index-self-healing.md) |
| `PRM-INFRA-003` | [Pipeline-F Finding Harvest](prompts/systems-architecture/PRM-INFRA-003_pipeline-f-harvest.md) | Harvest the latest Pipeline-F proposal into approved rule and hook changes, gating every edit behind an operator-confirmed diagnosis so false gates never ship | Pipeline-F proposal + run JSON (pipeline-f/proposals, pipeline-f/*/YYYY-MM-DD.json) | Claude Sonnet 4.6 (session-scoped; operator runs interactively) | `1.0.0` | [View File](prompts/systems-architecture/PRM-INFRA-003_pipeline-f-harvest.md) |
| `PRM-INFRA-004` | [FMD Learning-Log Harvest](prompts/systems-architecture/PRM-INFRA-004_fmd-harvest.md) | Harvest the FMD learning log into concrete still-applicable actions, finding lessons that are valid but never hardened into a rule, hook, or memory | FMD entries in smokin-coffee (FOR[Michael].md, 9-step structure) | Claude Sonnet 4.6 (session-scoped; operator runs interactively) | `1.0.0` | [View File](prompts/systems-architecture/PRM-INFRA-004_fmd-harvest.md) |
| `PRM-INFRA-005` | [Memory Drift Audit and Harvest](prompts/systems-architecture/PRM-INFRA-005_memory-harvest.md) | Audit the memory store for drift (stale, duplicate, contradicting entries) and harvest recurring corrections into rules, gating deletions and rule-promotions behind approval | MEMORY.md dashboard + Hindsight recall (memory files under ~/.claude/memory) | Claude Sonnet 4.6 (session-scoped; operator runs interactively) | `1.0.0` | [View File](prompts/systems-architecture/PRM-INFRA-005_memory-harvest.md) |
| `PRM-INFRA-006` | [Rule-Ladder and Cross-Machine Coverage Check](prompts/systems-architecture/PRM-INFRA-006_rule-ladder-coverage.md) | Verify that lessons harvested from Pipeline-F, FMD, and memory actually hardened into enforced rules and hooks and reached both machines — a coverage check, not a discovery pass | CLAUDE.md + law/ bodies + settings.json + hooks/ + cross-machine inbox (_mac-inbox / _win11-inbox) | Claude Sonnet 4.6 (session-scoped; operator runs interactively) | `1.0.0` | [View File](prompts/systems-architecture/PRM-INFRA-006_rule-ladder-coverage.md) |
| `PRM-NBLM-003` | [HTML-Aware Slide Parser](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) | Transform an HTML slide deck into clean XML for downstream parsing | HTML DOM | NotebookLM / Claude | `1.0.0` | [View File](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) |
| `PRM-NBLM-004` | [Architecture Semantic Compressor](prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md) | Extract system boundaries, data flows, and gaps from an HTML architecture deck | HTML DOM | NotebookLM / Long-Context LLMs | `1.2.0` | [View File](prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md) |

### 💼 Sales & Architecture
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-EMAL-001` | [Gmail-Safe HTML Email Builder](prompts/sales-architecture/PRM-EMAL-001_gmail-safe-email-builder.md) | Generate a Gmail-safe HTML email that drives a prospect to a tracked Vercel proposal page, with a poster+play-button linking to a click-to-play walkthrough modal; outputs a maintainable dev copy and a minified ship copy | Structured brief with required fields — ACCOUNT_NAME, PROPOSAL_URL, POSTER_IMAGE_URL, OPEN_PIXEL_URL, BODY_COPY, CTA_LABEL, HAS_WALKTHROUGH (true|false), IS_BULK_SEND (true|false); plus optional fields ALLOWED_PROPOSAL_DOMAINS and ALLOWED_TRACKING_DOMAINS (default to the host of PROPOSAL_URL / OPEN_PIXEL_URL respectively when absent); plus UNSUBSCRIBE_URL required only when IS_BULK_SEND=true | Claude Code (tool-enabled — shell required for the deterministic byte-size gate; Advanced Chat without a byte-counter tool cannot emit ship HTML, only the dev copy + a measurement-handoff note) | `1.2.0` | [View File](prompts/sales-architecture/PRM-EMAL-001_gmail-safe-email-builder.md) |
| `PRM-NBLM-005` | [Discovery-to-Architecture Extractor](prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) | Transform discovery transcripts and notes into a structured brief for architecture diagram and proposal generation | Meeting Transcript / Notes / Architecture Document | Claude / Gemini | `1.2.0` | [View File](prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) |
| `PRM-NBLM-006` | [6-Slide Enterprise CIO Presentation Generator](prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) | Transform a PRM-NBLM-005 Structured Technical Brief into a 6-slide CIO-ready architecture presentation | Structured Technical Brief (PRM-NBLM-005 output) | Claude (Advanced Chat / Claude Code) | `1.1.1` | [View File](prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) |
| `PRM-NBLM-006-STANDALONE` | [6-Slide Enterprise CIO Presentation Generator (Standalone / Template Mode)](prompts/sales-architecture/PRM-NBLM-006-STANDALONE_6-slide-cio-presentation-standalone.md) | Generate a 6-slide CIO architecture presentation from freeform notes or no input — all statistics are benchmark placeholders requiring customer validation before use | Freeform discovery notes, verbal brief, or no input (template mode) | Claude (Advanced Chat / Claude Code) | `1.0.0` | [View File](prompts/sales-architecture/PRM-NBLM-006-STANDALONE_6-slide-cio-presentation-standalone.md) |
| `PRM-NBLM-009` | [HTML Maintainability Refactor](prompts/sales-architecture/PRM-NBLM-009_html-maintainability-refactor.md) | Reorganize a large single-file HTML document to best-practice structure (indentation, section fences, component patterns) so a human or AI can edit it safely, without changing how the page renders | Single-file HTML | Claude Code / Gemini / Grok | `1.0.2` | [View File](prompts/sales-architecture/PRM-NBLM-009_html-maintainability-refactor.md) |

### 🎨 Presentation
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-PRES-001` | [HTML Slide-Ready Presentation Builder](prompts/presentation/PRM-PRES-001_html-slide-ready-presentation-builder.md) | Build a branded HTML presentation + matching Google Apps Script from a structured content brief, with auto-versioned filenames and Supabase logging | Freeform content brief (account name, slide type list, content per slide) | Claude (Claude Code / Advanced Chat) | `1.0.0` | [View File](prompts/presentation/PRM-PRES-001_html-slide-ready-presentation-builder.md) |
| `PRM-PRES-002` | [MuleSoft Gem Slide Handoff](prompts/presentation/PRM-PRES-002_mulesoft-gem-slide-handoff.md) | At the end of any customer discovery or engineering session, synthesize the full session into a dense Discovery Brief for the MuleSoft Master Deck Inventory Gem, then optionally generate a slide-by-slide Population Guide once the Gem returns its layout selections | Freeform Claude session transcript (discovery notes, engineering docs, proposal content) | Claude (Claude Code / Advanced Chat) | `1.0.0` | [View File](prompts/presentation/PRM-PRES-002_mulesoft-gem-slide-handoff.md) |
| `PRM-PRES-003` | [HTML Deck to Google Slides Re-Render](prompts/presentation/PRM-PRES-003_html-deck-to-google-slides-rerender.md) | Re-render an existing HTML page or deck into ONE branded multi-slide Google Slides deck via a single Apps Script file — no per-slide scripts, source HTML never modified | A complete HTML file (scrollytelling page, web one-pager, or multi-section HTML deck) | Claude (Claude Code / Advanced Chat) | `1.1.0` | [View File](prompts/presentation/PRM-PRES-003_html-deck-to-google-slides-rerender.md) |
| `PRM-PRES-004` | [Raw Notes to MuleSoft Google Slides (One-Shot CIO Deck)](prompts/presentation/PRM-PRES-004_notes-to-mulesoft-google-slides.md) | Turn raw discovery notes directly into ONE MuleSoft-branded 6-slide CIO architecture Google Slides deck via a single Apps Script file — no HTML detour, no separate discovery brief; unverified figures render as [BENCHMARK] placeholders | Freeform discovery notes, meeting transcript, or vendor/architecture document (no HTML, no pre-structured brief required) | Claude (Claude Code / Advanced Chat) | `1.0.0` | [View File](prompts/presentation/PRM-PRES-004_notes-to-mulesoft-google-slides.md) |
| `PRM-PRES-005` | [Notes to MuleSoft Google Slides (Flexible Layout, One-Shot Apps Script)](prompts/presentation/PRM-PRES-005_notes-to-mulesoft-slides-flexible.md) | Turn raw content into a MuleSoft-branded Google Slides deck via ONE Apps Script file, with FLEXIBLE slide layout (title/content/section/stat/quote helpers) instead of a fixed 6-slide skeleton — carries the hard Apps Script error-prevention rules so the generated .gs runs without runtime errors | Freeform notes, bullets, stats, or quotes (no HTML, no fixed structure required) | Gemini or Claude (any LLM that can write Google Apps Script) | `1.0.1` | [View File](prompts/presentation/PRM-PRES-005_notes-to-mulesoft-slides-flexible.md) |

<!-- PROMPT_CATALOG_END -->

---

## 📦 Two-Artifact Model

**A registry PR is never "just a markdown file." Always verify the compiled JSON.**

| Artifact | Who uses it |
| :--- | :--- |
| `prompts/.../*.md` | Authors, GitHub copy-paste |
| `dist/prompts_latest.json` | Agents, apps, automation |

The `.md` file is what you write. The JSON is what everything else consumes.

- **`scripts/compile_prompts.py`** generates `dist/prompts_latest.json` from the `.md` files — run it locally after every prompt change.
- **Feedback footer** — the compiler automatically appends a `Score this prompt` block to every `prompt_text` in the JSON. Do **not** add this to the `.md` source file; the compiler handles it. Open `dist/prompts_latest.json` after compiling to confirm the footer appears at the end of your prompt's `prompt_text`.
- **Review rule:** open the JSON first when reviewing consumption, not the `.md` fence alone.

---

## 🛠️ Contribution & Lifecycle Rules

Want to add a prompt or optimize an existing one? Follow the PromptOps workflow:

1. **Branching:** Always branch from latest `origin/main`: `git fetch origin && git checkout -b feat/... origin/main`
2. **Metadata:** Use the required YAML frontmatter blocks inside your file. Missing metadata fields will break the JSON compilation script during automated PR validation.
3. **Versioning:** Bump versions using Semantic Versioning rules (`Major.Minor.Patch`).
4. **Pull Requests:** Open a PR against `main`. Fill out the automated PR template entirely, attaching your before/after evaluation test runs.

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed instructions.

---

## 🔒 Security

External access uses fine-grained PATs scoped to read-only on this repository only. See [docs/SECURITY.md](docs/SECURITY.md).
