#!/usr/bin/env python3
"""Execute captures.yaml with Playwright (async)."""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def load_captures(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    raise SystemExit("PyYAML required: pip install pyyaml")


def resolve_url(base_url: str, url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return urljoin(base_url, url)


async def run_captures(
    config: dict[str, Any],
    output_dir: Path,
    *,
    verbose: bool = True,
) -> None:
    from playwright.async_api import async_playwright

    output_dir.mkdir(parents=True, exist_ok=True)
    base_url = config["base_url"]
    viewport = config.get("viewport", {"width": 1920, "height": 1080})

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport=viewport)

        for step in config.get("steps", []):
            action = step["action"]

            if action == "goto":
                target = resolve_url(base_url, step.get("url", "/"))
                wait_until = step.get("wait_until", "networkidle")
                await page.goto(target, wait_until=wait_until)

            elif action == "click":
                await page.click(step["selector"])

            elif action == "scroll":
                if "scroll" in step:
                    x, y = step["scroll"]
                    await page.evaluate(f"window.scrollTo({x}, {y})")
                elif "selector" in step:
                    block = step.get("block", "nearest")
                    sel = step["selector"]
                    await page.evaluate(
                        """([selector, block]) => {
                          const el = document.querySelector(selector);
                          if (el) el.scrollIntoView({block});
                        }""",
                        [sel, block],
                    )
                else:
                    raise ValueError(f"scroll step needs scroll or selector: {step}")

            elif action == "wait":
                await page.wait_for_timeout(int(step.get("ms", 0)))

            elif action == "screenshot":
                ms = int(step.get("ms", 700))
                await page.wait_for_timeout(ms)
                out = output_dir / step["file"]
                await page.screenshot(path=str(out))
                if verbose:
                    print("capture:", out)

            elif action == "screenshot_locator":
                locator = page.locator(step["selector"])
                if step.get("first"):
                    locator = locator.first
                await locator.scroll_into_view_if_needed()
                ms = int(step.get("ms", 300))
                await page.wait_for_timeout(ms)
                out = output_dir / step["file"]
                await locator.screenshot(path=str(out))
                if verbose:
                    print("capture:", out)

            else:
                raise ValueError(f"Unknown action: {action}")

        await browser.close()


async def main_async(captures_path: Path, output_dir: Path) -> None:
    config = load_captures(captures_path)
    await run_captures(config, output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Playwright capture script from YAML")
    parser.add_argument("captures", type=Path, help="Path to captures.yaml")
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("captures"),
        help="Directory for PNG outputs (default: ./captures)",
    )
    args = parser.parse_args()
    asyncio.run(main_async(args.captures, args.output_dir))


if __name__ == "__main__":
    main()
