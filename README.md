# 🏛️ Enterprise Prompt Registry

Welcome to the central command center for our organization's engineered AI prompts. This repository is the Single Source of Truth (SSOT). Prompts here are version-controlled, performance-tested, and optimized for both human copy-pasting and direct programmatic application calls.

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
| `PRM-PDLV-006` | [Static Guide Overview Video — Agent System Prompt](prompts/product-delivery/PRM-PDLV-006_static-guide-overview-video.md) | Build or rebuild a narrated overview video embedded in a static HTML product guide | HTML guide URL + scene spec (JSON/YAML) + image captures | Claude Code / Cursor Agent | `1.0.0` | [View File](prompts/product-delivery/PRM-PDLV-006_static-guide-overview-video.md) |

### 🧠 AI & Integration Engineering
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-MMLM-006` | [Presentation Slide Visual and Textual Markdown Extractor](prompts/ai-engineering/PRM-MMLM-006_presentation-markdown-extractor.md) | Analyzing presentation screenshots to extract literal text hierarchies alongside deep visual-narrative interpretations into clean Markdown. | PNG / JPG | Multimodal LLM (e.g., GPT-4o, Claude 3.5 Sonnet) | `1.0.0` | [View File](prompts/ai-engineering/PRM-MMLM-006_presentation-markdown-extractor.md) |
| `PRM-NBLM-002` | [Sequential Machine-Optimized Extractor](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) | Extract structured JSON data from a slide deck for app ingestion | PPTX / PDF | Long-Context LLMs | `1.0.0` | [View File](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) |
| `PRM-VISION-001` | [Presentation Visual Layout and Relationship to Markdown Extractor](prompts/ai-engineering/PRM-VISION-001_presentation-to-markdown.md) | Extract literal text, implied icon relationships, and layout structures from presentation screenshots into clean Markdown. | PNG / JPEG | Multimodal LLM (Vision-capable) | `1.0.1` | [View File](prompts/ai-engineering/PRM-VISION-001_presentation-to-markdown.md) |

### 🛠️ Systems Architecture
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-003` | [HTML-Aware Slide Parser](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) | Transform an HTML slide deck into clean XML for downstream parsing | HTML DOM | NotebookLM / Claude | `1.0.0` | [View File](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) |
| `PRM-NBLM-004` | [Architecture Semantic Compressor](prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md) | Extract system boundaries, data flows, and gaps from an HTML architecture deck | HTML DOM | NotebookLM / Long-Context LLMs | `1.1.0` | [View File](prompts/systems-architecture/PRM-NBLM-004_architecture-semantic-compressor.md) |

### 💼 Sales & Architecture
| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-005` | [Discovery-to-Architecture Extractor](prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) | Transform discovery transcripts and notes into a structured brief for architecture diagram and proposal generation | Meeting Transcript / Notes / Architecture Document | Claude / Gemini | `1.0.0` | [View File](prompts/sales-architecture/PRM-NBLM-005_discovery-to-architecture-extractor.md) |
| `PRM-NBLM-006` | [6-Slide Enterprise CIO Presentation Generator](prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) | Transform a PRM-NBLM-005 Structured Technical Brief into a 6-slide CIO-ready architecture presentation | Structured Technical Brief (PRM-NBLM-005 output) | Claude (Advanced Chat / Claude Code) | `1.1.0` | [View File](prompts/sales-architecture/PRM-NBLM-006_6-slide-cio-presentation-generator.md) |
| `PRM-NBLM-006-STANDALONE` | [6-Slide Enterprise CIO Presentation Generator (Standalone / Template Mode)](prompts/sales-architecture/PRM-NBLM-006-STANDALONE_6-slide-cio-presentation-standalone.md) | Generate a 6-slide CIO architecture presentation from freeform notes or no input — all statistics are benchmark placeholders requiring customer validation before use | Freeform discovery notes, verbal brief, or no input (template mode) | Claude (Advanced Chat / Claude Code) | `1.0.0` | [View File](prompts/sales-architecture/PRM-NBLM-006-STANDALONE_6-slide-cio-presentation-standalone.md) |

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
