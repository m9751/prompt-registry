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
| ID | Prompt Title | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-001` | [Slide-to-Human Briefing Master](prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md) | PPTX / PDF | NotebookLM | `1.0.0` | [View File](prompts/product-delivery/PRM-NBLM-001_slide-to-human-brief.md) |

### 🧠 AI & Integration Engineering
| ID | Prompt Title | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-002` | [Sequential Machine-Optimized Extractor](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) | PPTX / PDF | Long-Context LLMs | `1.0.0` | [View File](prompts/ai-engineering/PRM-NBLM-002_sequential-machine-extractor.md) |

### 🛠️ Systems Architecture
| ID | Prompt Title | Source Format | Target Model | Version | Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PRM-NBLM-003` | [HTML-Aware Slide Parser](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) | HTML DOM | NotebookLM / Claude | `1.0.0` | [View File](prompts/systems-architecture/PRM-NBLM-003_html-aware-slide-parser.md) |

<!-- PROMPT_CATALOG_END -->

---

## 🛠️ Contribution & Lifecycle Rules

Want to add a prompt or optimize an existing one? Follow the PromptOps workflow:

1. **Branching:** Create a feature branch off `main` (`feature/your-prompt-name`).
2. **Metadata:** Use the required YAML frontmatter blocks inside your file. Missing metadata fields will break the JSON compilation script during automated PR validation.
3. **Versioning:** Bump versions using Semantic Versioning rules (`Major.Minor.Patch`).
4. **Pull Requests:** Open a PR against `main`. Fill out the automated PR template entirely, attaching your before/after evaluation test runs.

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed instructions.

---

## 🔒 Security

External access uses fine-grained PATs scoped to read-only on this repository only. See [docs/SECURITY.md](docs/SECURITY.md).
