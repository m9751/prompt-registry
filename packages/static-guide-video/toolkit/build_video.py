#!/usr/bin/env python3
"""Generic static-guide overview video build engine (extracted from pilot build_demo.py)."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# Allow running as script: python3 build_video.py from toolkit/ or repo
_TOOLKIT = Path(__file__).resolve().parent
if str(_TOOLKIT) not in sys.path:
    sys.path.insert(0, str(_TOOLKIT))

from capture_runner import load_captures, run_captures  # noqa: E402
from layouts import LAYOUT_WAITS, body_class, render_inner  # noqa: E402

DEFAULT_BASE_CSS = """
:root{--blue-20:#032D60;--blue-50:#0176D3;--blue-95:#EEF4FF;--cloud-60:#0D9DDA;--orange-70:#FE9339;--red:#EA001E;
--font:'Salesforce Sans','SF Pro Display',Arial,sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:scale(.92)}to{opacity:1;transform:scale(1)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 6px rgba(65,182,88,.55)}50%{box-shadow:0 0 0 14px rgba(65,182,88,.2)}}
@keyframes slideL{from{opacity:0;transform:translateX(-24px)}to{opacity:1;transform:none}}
body{width:1920px;height:1080px;overflow:hidden;font-family:var(--font);position:relative}
body.dark{background:var(--blue-20);color:#fff}
body.light{background:var(--blue-95);color:var(--blue-20)}
.accent-bar{position:absolute;top:0;left:0;right:0;height:6px;background:ACCENT_BAR;z-index:5}
.logo{position:absolute;top:40px;right:56px;height:40px;z-index:10}
body.dark .logo{filter:brightness(0) invert(1)}
.pad{padding:56px 72px;height:100%;display:flex;flex-direction:column}
"""

class BuildContext:
    def __init__(
        self,
        root: Path,
        manifest: dict[str, Any],
        brand: dict[str, Any] | None = None,
    ) -> None:
        self.root = root.resolve()
        self.repo = self.root.parent
        self.manifest = manifest
        self.brand = brand
        self.scenes_dir = self.root / "scenes"
        self.captures_dir = self.root / "captures"
        self.narration_dir = self.root / "narration"
        self.frames_dir = self.root / "frames"
        self.audio_dir = self.root / "audio"
        self.clips_dir = self.root / "clips"
        self.output_full = self.root / "output.mp4"
        self.output_hero = self.root / "output-hero-silent.mp4"
        self.voice = manifest.get("voice", "en-US-AndrewNeural")
        self.scenes = manifest["scenes"]
        self.hero = manifest.get("hero_silent")
        self.base_css = self._build_base_css()
        self.logo_src = (brand or {}).get("logo", "../../mulesoft-logo.png") if brand else "../../mulesoft-logo.png"
        if brand and brand.get("logo") is None:
            self.logo_src = ""

    def _build_base_css(self) -> str:
        accent = "linear-gradient(90deg, var(--cloud-60), var(--orange-70))"
        if self.brand:
            css_vars = self.brand.get("css_vars", {})
            vars_block = "".join(f"{k}:{v};" for k, v in css_vars.items())
            accent = self.brand.get("accent_bar", accent)
            return (
                f":root{{{vars_block}}}"
                + DEFAULT_BASE_CSS.split("}", 1)[1]
            ).replace("ACCENT_BAR", accent)
        css = DEFAULT_BASE_CSS.replace(
            "ACCENT_BAR", "linear-gradient(90deg, var(--cloud-60), var(--orange-70))"
        )
        return css

    def ensure_dirs(self) -> None:
        for d in (
            self.scenes_dir,
            self.captures_dir,
            self.narration_dir,
            self.frames_dir,
            self.audio_dir,
            self.clips_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)


def write_scene_html(ctx: BuildContext, scene: dict) -> None:
    body = body_class(scene)
    inner = render_inner(scene)
    logo_tag = f'<img class="logo" src="{ctx.logo_src}" alt=""/>' if ctx.logo_src else ""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"/><style>{ctx.base_css}</style></head>
<body class="{body}"><div class="accent-bar"></div>
{logo_tag}{inner}</body></html>"""
    (ctx.scenes_dir / f"{scene['id']}.html").write_text(html, encoding="utf-8")


async def render_frames(ctx: BuildContext) -> None:
    from playwright.async_api import async_playwright

    ctx.frames_dir.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        for scene in ctx.scenes:
            sid = scene["id"]
            write_scene_html(ctx, scene)
            await page.goto(
                (ctx.scenes_dir / f"{sid}.html").resolve().as_uri(),
                wait_until="networkidle",
            )
            w = LAYOUT_WAITS.get(scene.get("layout"), 950)
            await page.wait_for_timeout(w)
            out = ctx.frames_dir / f"{sid}.png"
            await page.screenshot(path=str(out), type="png")
            print("frame:", out)
        await browser.close()


def run(cmd: list) -> None:
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def edge_tts(ctx: BuildContext, text: str, mp3: Path) -> None:
    env_edge = os.environ.get("EDGE_TTS")
    if env_edge:
        edge = Path(env_edge)
        if edge.exists():
            run([str(edge), "--voice", ctx.voice, "--text", text, "--write-media", str(mp3)])
            return
    hardcoded = Path("/Users/mbusacca/Library/Python/3.9/bin/edge-tts")
    if hardcoded.exists():
        run([str(hardcoded), "--voice", ctx.voice, "--text", text, "--write-media", str(mp3)])
    else:
        run(["python3", "-m", "edge_tts", "--voice", ctx.voice, "--text", text, "--write-media", str(mp3)])


def probe_duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(path),
            ],
            text=True,
        ).strip()
    )


def make_clip(frame: Path, audio: Path | None, out: Path, dur: float, *, ken_burns: bool = False) -> None:
    if ken_burns:
        vf = (
            f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            f"zoompan=z='min(zoom+0.0009,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={max(int(dur*25),1)}:s=1920x1080:fps=25"
        )
        tmp = out.with_suffix(".vid.mp4")
        run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(frame), "-vf", vf, "-t", f"{dur:.2f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(tmp),
        ])
        if audio:
            run([
                "ffmpeg", "-y", "-i", str(tmp), "-i", str(audio),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-t", f"{dur:.2f}", str(out),
            ])
            tmp.unlink(missing_ok=True)
        else:
            tmp.rename(out)
    else:
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xEEF4FF"
        )
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(frame)]
        if audio:
            cmd += ["-i", str(audio)]
        cmd += ["-vf", vf, "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p"]
        if audio:
            cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-t", f"{dur:.2f}", str(out)]
        run(cmd)


def build_full(ctx: BuildContext) -> None:
    ctx.clips_dir.mkdir(exist_ok=True)
    clips = []
    for scene in ctx.scenes:
        sid = scene["id"]
        text = scene["narration"]
        (ctx.narration_dir / f"{sid}.txt").write_text(text + "\n")
        audio = ctx.audio_dir / f"{sid}.mp3"
        edge_tts(ctx, text, audio)
        dur = max(float(scene["duration"]), probe_duration(audio) + 0.35)
        make_clip(
            ctx.frames_dir / f"{sid}.png",
            audio,
            ctx.clips_dir / f"{sid}.mp4",
            dur,
            ken_burns=scene.get("ken_burns", False),
        )
        clips.append(ctx.clips_dir / f"{sid}.mp4")
    lst = ctx.root / "concat-full.txt"
    lst.write_text("\n".join(f"file '{c.resolve()}'" for c in clips) + "\n")
    # Re-encode (never -c copy): concat copy causes non-monotonic DTS → playback hiccups
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-vf", "fps=25,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-g", "25", "-keyint_min", "25",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1",
        "-af", "aresample=async=1:first_pts=0",
        "-movflags", "+faststart",
        "-max_muxing_queue_size", "1024",
        str(ctx.output_full),
    ])
    words = sum(len(s["narration"].split()) for s in ctx.scenes)
    print("Done full:", ctx.output_full, round(probe_duration(ctx.output_full), 1), "s,", words, "words")


def build_hero_silent(ctx: BuildContext) -> None:
    if not ctx.hero:
        print("No hero_silent in manifest; skipping hero build")
        return
    default_dur = float(ctx.hero.get("duration_per_beat", 5))
    clips = []
    for beat in ctx.hero["beats"]:
        raw = beat["image"]
        img = (ctx.repo / raw[3:]) if raw.startswith("../") else (ctx.root / raw)
        dur = float(beat.get("duration", default_dur))
        out = ctx.clips_dir / f"hero-{beat['id']}.mp4"
        make_clip(img, None, out, dur, ken_burns=beat.get("ken_burns", True))
        clips.append(out)
    lst = ctx.root / "concat-hero.txt"
    lst.write_text("\n".join(f"file '{c.resolve()}'" for c in clips) + "\n")
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-vf", "fps=25,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-g", "25", "-keyint_min", "25",
        "-movflags", "+faststart",
        str(ctx.output_hero),
    ])
    print("Done hero:", ctx.output_hero, round(probe_duration(ctx.output_hero), 1), "s")


async def run_captures_from_file(ctx: BuildContext, captures_path: Path) -> None:
    config = load_captures(captures_path)
    await run_captures(config, ctx.captures_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build static-guide overview video from scenes.json manifest",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="demo-output directory (default: cwd)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to scenes.json (default: <root>/scenes.json)",
    )
    parser.add_argument(
        "--brand",
        type=Path,
        default=None,
        help="Optional brand.json for CSS vars and logo",
    )
    parser.add_argument(
        "--captures",
        type=Path,
        default=None,
        help="Optional captures.yaml for live Playwright screenshots",
    )
    parser.add_argument(
        "--skip-captures",
        action="store_true",
        help="Skip live capture stage even if --captures is set",
    )
    parser.add_argument(
        "--hero-only",
        action="store_true",
        help="Captures + hero silent only (no frames or full narrated video)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    manifest_path = (args.manifest or root / "scenes.json").resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    brand = None
    if args.brand:
        brand = json.loads(args.brand.read_text(encoding="utf-8"))

    ctx = BuildContext(root, manifest, brand)
    ctx.ensure_dirs()

    captures_path = args.captures
    if captures_path is None and not args.skip_captures:
        default_yaml = root / "captures.yaml"
        if default_yaml.exists():
            captures_path = default_yaml

    if captures_path and not args.skip_captures:
        print("=== Captures ===")
        asyncio.run(run_captures_from_file(ctx, captures_path.resolve()))
    elif not args.skip_captures:
        print("=== Captures skipped (no captures.yaml; use --captures or --skip-captures) ===")

    if args.hero_only:
        print("=== Hero silent ===")
        build_hero_silent(ctx)
        return

    print("=== Frames ===")
    asyncio.run(render_frames(ctx))
    print("=== Full sell-first ===")
    build_full(ctx)
    print("=== Hero silent ===")
    build_hero_silent(ctx)


if __name__ == "__main__":
    main()
