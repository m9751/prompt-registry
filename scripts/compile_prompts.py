#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compile_prompts.py — PromptOps Registry Compiler

Responsibilities:
  1. Crawl prompts/ for *.md files
  2. Parse YAML frontmatter (safe_load) + extract exactly one fenced code block
  3. Validate frontmatter against scripts/prompt_schema.json
  4. Check for duplicate IDs across all files
  5. Write dist/prompts_latest.json and dist/prompts_v{version}.json
  6. Regenerate README.md catalog table between sentinel comments
  7. Append feedback footer to every compiled prompt_text

Exit codes:
  0 = success
  1 = validation error (printed to stderr)
"""

import json
import os
import re
import sys
from pathlib import Path
import datetime

import yaml
import jsonschema

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
DIST_DIR = REPO_ROOT / "dist"
SCHEMA_PATH = REPO_ROOT / "scripts" / "prompt_schema.json"
README_PATH = REPO_ROOT / "README.md"

CATALOG_START = "<!-- PROMPT_CATALOG_START -->"
CATALOG_END = "<!-- PROMPT_CATALOG_END -->"

GITHUB_RAW_BASE = "https://m9751.github.io/prompt-registry"

# Feedback footer injected into every compiled prompt_text.
# Agents and humans pulling from the JSON see this after the primary response.
FEEDBACK_FOOTER = (
    "\n\n---\n"
    "⬆️ Primary response above.\n"
    "Score this prompt: 1 (poor) / 2 (adequate) / 3 (excellent)\n"
    "What did it miss or get wrong? (one line)"
)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def extract_frontmatter_and_prompt(filepath: Path) -> tuple[dict, str]:
    """
    Parse YAML frontmatter and extract exactly one fenced code block.
    Raises SystemExit on malformed input.
    """
    content = filepath.read_text(encoding="utf-8")

    # Extract YAML frontmatter between first --- pair
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        _fail(f"{filepath}: missing or malformed YAML frontmatter (expected --- delimiters)")

    try:
        frontmatter = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as exc:
        _fail(f"{filepath}: YAML parse error: {exc}")

    if not isinstance(frontmatter, dict):
        _fail(f"{filepath}: frontmatter parsed to non-dict type")

    # pyyaml parses bare ISO dates (2026-06-02) as datetime.date objects.
    # Coerce date/datetime values to ISO string so jsonschema validation passes.
    import datetime
    for key, val in frontmatter.items():
        if isinstance(val, (datetime.date, datetime.datetime)):
            frontmatter[key] = val.isoformat()

    # Extract fenced code blocks (``` ... ```)
    body = content[fm_match.end():]
    fence_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", body, re.DOTALL)

    if len(fence_blocks) == 0:
        _fail(f"{filepath}: no fenced code block found — prompt text must live in a ``` block")
    if len(fence_blocks) > 1:
        _fail(f"{filepath}: {len(fence_blocks)} fenced code blocks found — exactly 1 required")

    return frontmatter, fence_blocks[0].strip(), body


def _fail(message: str) -> None:
    print(f"VALIDATION ERROR: {message}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Fence boundary check (R4)
# ---------------------------------------------------------------------------

# Matches CSS hex color tokens: #RGB, #RRGGBB, #RGBA, #RRGGBBAA
_HEX_TOKEN_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")


def check_fence_boundary(filepath: Path, body: str, prompt_text: str) -> None:
    """
    R4: Verify that every hex color token in the Overview (outside the fence)
    also appears inside the fenced code block (prompt_text).

    If a token is referenced in the Overview but absent from prompt_text, agents
    consuming prompt_text from the compiled JSON will not see it — the reference
    is broken. Exit 1 on violation so CI catches this class of error automatically.
    """
    # Extract the overview portion: everything before the first fence block
    overview = body.split("```")[0] if "```" in body else body

    overview_tokens = set(_HEX_TOKEN_RE.findall(overview))
    fence_tokens = set(_HEX_TOKEN_RE.findall(prompt_text))

    missing = overview_tokens - fence_tokens
    if missing:
        _fail(
            f"{filepath}: [FENCE BOUNDARY] Hex token(s) {sorted(missing)} "
            f"referenced in Overview but absent from prompt_text — "
            f"agents consuming the compiled JSON cannot see them. "
            f"Move these tokens inside the fenced code block."
        )


# ---------------------------------------------------------------------------
# Domain AGENTS.md parser
# ---------------------------------------------------------------------------

def parse_domain_agents_md(domain_path: Path) -> dict:
    """
    Parse the ## Routing section from a domain's AGENTS.md.
    Returns dict with description, use_when, not_when (all str).
    Returns empty strings if AGENTS.md is missing or malformed — never fails the build.
    """
    agents_path = domain_path / "AGENTS.md"
    if not agents_path.exists():
        return {"description": "", "use_when": "", "not_when": ""}

    content = agents_path.read_text(encoding="utf-8")

    routing_match = re.search(r"## Routing\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not routing_match:
        return {"description": "", "use_when": "", "not_when": ""}

    routing_block = routing_match.group(1)

    def extract_key(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+?)(?=\n\w[\w_]*:|\Z)", routing_block, re.MULTILINE | re.DOTALL)
        return m.group(1).strip() if m else ""

    return {
        "description": extract_key("description"),
        "use_when": extract_key("use_when"),
        "not_when": extract_key("not_when"),
    }


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        _fail(f"Schema file not found: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate_frontmatter(frontmatter: dict, schema: dict, filepath: Path) -> None:
    try:
        jsonschema.validate(instance=frontmatter, schema=schema)
    except jsonschema.ValidationError as exc:
        field = " -> ".join(str(p) for p in exc.absolute_path) or exc.validator_value
        _fail(f"{filepath}: {exc.message}")


# ---------------------------------------------------------------------------
# Main compilation
# ---------------------------------------------------------------------------

def compile_registry() -> None:
    schema = load_schema()

    if not PROMPTS_DIR.exists():
        _fail(f"prompts/ directory not found at {PROMPTS_DIR}")

    prompt_files = sorted(f for f in PROMPTS_DIR.rglob("*.md") if f.name != "AGENTS.md")
    if not prompt_files:
        _fail("No prompt files found in prompts/")

    prompts = []
    seen_ids: dict[str, Path] = {}

    for filepath in prompt_files:
        frontmatter, prompt_text, body = extract_frontmatter_and_prompt(filepath)
        validate_frontmatter(frontmatter, schema, filepath)
        check_fence_boundary(filepath, body, prompt_text)

        pid = frontmatter["id"]
        if pid in seen_ids:
            _fail(f"DUPLICATE ID: {pid} found in {seen_ids[pid]} and {filepath}")
        seen_ids[pid] = filepath

        # Inject hosted_url if not already present or if it's a placeholder
        rel_path = filepath.relative_to(REPO_ROOT)
        computed_url = f"{GITHUB_RAW_BASE}/{rel_path.as_posix()}"
        if not frontmatter.get("hosted_url"):
            frontmatter["hosted_url"] = computed_url

        prompts.append({
            **frontmatter,
            "prompt_text": prompt_text + FEEDBACK_FOOTER,
            "source_file": rel_path.as_posix(),
        })

    # Sort by ID
    prompts.sort(key=lambda p: p["id"])

    # Write dist artifacts
    DIST_DIR.mkdir(exist_ok=True)

    payload = {"schema_version": "1.0", "prompts": prompts}
    payload_json = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

    latest_path = DIST_DIR / "prompts_latest.json"
    latest_path.write_text(payload_json, encoding="utf-8")
    print(f"  Written: {latest_path.relative_to(REPO_ROOT)}")

    # Versioned artifacts — one per unique version string
    versions_seen: set[str] = set()
    for prompt in prompts:
        v = prompt["version"]
        if v not in versions_seen:
            versions_seen.add(v)
            versioned_path = DIST_DIR / f"prompts_v{v}.json"
            versioned_path.write_text(payload_json, encoding="utf-8")
            print(f"  Written: {versioned_path.relative_to(REPO_ROOT)}")

    # Regenerate README catalog
    regenerate_readme(prompts)

    # Generate HTML wrapper for AI agents that cannot fetch raw JSON
    generate_html_wrapper(payload_json)
    generate_domains_catalog(prompts)

    print(f"\nCompilation complete: {len(prompts)} prompt(s) processed.")


# ---------------------------------------------------------------------------
# HTML wrapper for AI agent consumers (Gemini etc.)
# ---------------------------------------------------------------------------

def generate_html_wrapper(payload_json: str) -> None:
    pretty = json.dumps(json.loads(payload_json), indent=2, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html>
<head><title>Enterprise Prompt Registry</title></head>
<body>
<h1>Enterprise Prompt Registry</h1>
<p>Machine-readable registry payload. For AI agents that cannot fetch raw JSON directly.</p>
<pre id="registry">
{pretty}
</pre>
</body>
</html>"""
    html_path = DIST_DIR / "registry.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"  Written: {html_path.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# Domain catalog (domains.json)
# ---------------------------------------------------------------------------

def generate_domains_catalog(prompts: list[dict]) -> None:
    """
    Emit dist/domains.json — machine-readable catalog of all prompt domains.
    Reads each domain's AGENTS.md ## Routing section for description/use_when/not_when.
    prompt_count is computed from the already-compiled prompts list (authoritative).
    """
    counts: dict[str, int] = {}
    for p in prompts:
        counts[p["domain"]] = counts.get(p["domain"], 0) + 1

    domain_order = [
        "product-delivery",
        "ai-engineering",
        "systems-architecture",
        "sales-architecture",
    ]

    # Warn if any compiled domain is not in domain_order (would be silently omitted)
    for discovered in counts:
        if discovered not in domain_order:
            print(f"  WARNING: domain '{discovered}' has compiled prompts but is not in domain_order — add it to generate_domains_catalog()", file=sys.stderr)

    domains = []
    for domain_name in domain_order:
        domain_path = PROMPTS_DIR / domain_name
        routing = parse_domain_agents_md(domain_path)
        domains.append({
            "name": domain_name,
            "path": f"prompts/{domain_name}",
            "description": routing["description"],
            "use_when": routing["use_when"],
            "not_when": routing["not_when"],
            "prompt_count": counts.get(domain_name, 0),
        })

    catalog = {
        "schema_version": "1.0",
        "generated_at": datetime.date.today().isoformat(),
        "domains": domains,
    }

    catalog_path = DIST_DIR / "domains.json"
    catalog_path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  Written: {catalog_path.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# README catalog regeneration
# ---------------------------------------------------------------------------

def regenerate_readme(prompts: list[dict]) -> None:
    if not README_PATH.exists():
        print(f"  WARNING: README.md not found at {README_PATH} — skipping catalog update", file=sys.stderr)
        return

    readme = README_PATH.read_text(encoding="utf-8")

    if CATALOG_START not in readme or CATALOG_END not in readme:
        print(f"  WARNING: sentinel comments not found in README.md — skipping catalog update", file=sys.stderr)
        return

    # Group by domain for section headers
    by_domain: dict[str, list[dict]] = {}
    domain_labels = {
        "product-delivery": "🚀 Product & Delivery",
        "ai-engineering": "🧠 AI & Integration Engineering",
        "systems-architecture": "🛠️ Systems Architecture",
        "sales-architecture": "💼 Sales & Architecture",
    }
    for prompt in prompts:
        by_domain.setdefault(prompt["domain"], []).append(prompt)

    table_lines = []
    for domain_key, label in domain_labels.items():
        domain_prompts = by_domain.get(domain_key, [])
        if not domain_prompts:
            continue
        table_lines.append(f"\n### {label}")
        table_lines.append("| ID | Prompt Title | Use This For | Source Format | Target Model | Version | Link |")
        table_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for p in domain_prompts:
            link = f"[View File]({p['source_file']})"
            title_link = f"[{p['title']}]({p['source_file']})"
            use_for = p.get("use_for", "")
            table_lines.append(
                f"| `{p['id']}` | {title_link} | {use_for} | {p['source_format']} | {p['target_orchestrator']} | `{p['version']}` | {link} |"
            )

    catalog_block = "\n".join(table_lines) + "\n"

    # Replace content between sentinel comments
    new_readme = re.sub(
        rf"{re.escape(CATALOG_START)}.*?{re.escape(CATALOG_END)}",
        f"{CATALOG_START}\n{catalog_block}\n{CATALOG_END}",
        readme,
        flags=re.DOTALL,
    )

    README_PATH.write_text(new_readme, encoding="utf-8")
    print(f"  Updated: README.md catalog ({len(prompts)} prompts)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("PromptOps Compiler — starting...\n")
    compile_registry()
