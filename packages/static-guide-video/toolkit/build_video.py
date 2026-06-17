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

LAYOUT_WAITS = {
    "kinetic_pain": 1500,
    "kinetic_outcomes": 1200,
    "cta_inguide": 1300,
    "editor_tabs": 1100,
    "proof_highlight": 1400,
    "depth_tabs": 1200,
    "cta_steps": 1200,
}


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
        self.logo_src = (brand or {}).get("logo", "../../mulesoft-logo.png")

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


def img_src(path: str) -> str:
    if not path:
        return ""
    if path.startswith("../screenshots"):
        return "../../screenshots/" + path.split("/", 2)[-1]
    if path.startswith("../"):
        return path
    return f"../{path}"


def write_scene_html(ctx: BuildContext, scene: dict) -> None:
    layout = scene.get("layout", "image")
    kind = scene.get("kind", "content")
    dark = kind == "title" or layout in ("kinetic_pain", "cta_inguide")
    body = "dark" if dark else "light"
    title = scene.get("title", "")
    subtitle = scene.get("subtitle", "")
    image = img_src(scene.get("image", ""))

    inner = ""
    if layout == "kinetic_pain":
        inner = """
<div class="pad" style="justify-content:center;align-items:center;text-align:center">
  <div style="font-size:120px;font-weight:800;color:#fff;animation:pop .5s cubic-bezier(.16,1,.3,1) both">847 lines</div>
  <div style="display:flex;gap:14px;justify-content:center;margin-top:28px;flex-wrap:wrap">
    <span style="padding:10px 18px;border-radius:20px;border:1px solid var(--red);color:#FFB3BC;background:rgba(234,0,30,.15);font-weight:700;animation:fadeUp .5s .15s both">No tests</span>
    <span style="padding:10px 18px;border-radius:20px;border:1px solid var(--orange-70);color:#FFE2C8;background:rgba(254,147,57,.15);font-weight:700;animation:fadeUp .5s .25s both">Schema drift</span>
    <span style="padding:10px 18px;border-radius:20px;border:1px solid #CFE9FE;color:#CFE9FE;font-weight:700;animation:fadeUp .5s .35s both">FIXME</span>
  </div>
  <p style="font-size:28px;color:#CFE9FE;margin-top:40px;animation:fadeUp .5s .4s both">Five portals <span style="color:var(--orange-70)">→</span> <strong style="color:var(--cloud-60)">one editor</strong></p>
</div>"""
    elif layout == "split_imagine":
        inner = f"""
<div class="pad" style="flex-direction:row;gap:40px;align-items:center">
  <div style="flex:1;animation:slideL .6s cubic-bezier(.16,1,.3,1) both">
    <h1 style="font-size:52px;font-weight:700;line-height:1.1">{title}</h1>
    <p style="font-size:28px;color:#5C6A7F;margin-top:16px">{subtitle}</p>
    <p style="font-size:22px;color:var(--blue-50);margin-top:28px;font-weight:600">EHRs · Claims · Legacy APIs → one editor</p>
  </div>
  <div style="flex:1.2;animation:fadeUp .6s .2s both">
    <img src="{image}" style="width:100%;border-radius:8px;border:1px solid #CFE9FE;box-shadow:0 4px 16px rgba(3,45,96,.14)"/>
  </div>
</div>"""
    elif layout == "kinetic_outcomes":
        inner = f"""
<div class="pad">
  <div style="display:flex;gap:20px;margin-bottom:24px;flex-wrap:wrap">
    <span style="font-size:28px;font-weight:800;color:var(--blue-20);background:#fff;padding:14px 22px;border-radius:8px;border:1px solid #CFE9FE;animation:pop .4s both">Search Exchange</span>
    <span style="font-size:28px;font-weight:800;color:var(--blue-20);background:#fff;padding:14px 22px;border-radius:8px;border:1px solid #CFE9FE;animation:pop .4s .1s both">Scaffold flows</span>
    <span style="font-size:28px;font-weight:800;color:var(--blue-20);background:#fff;padding:14px 22px;border-radius:8px;border:1px solid #CFE9FE;animation:pop .4s .2s both">Deploy</span>
  </div>
  <div style="flex:1;display:flex;align-items:center;justify-content:center;animation:fadeUp .55s .3s both">
    <img src="{image}" style="max-height:720px;max-width:100%;border-radius:8px;border:1px solid #CFE9FE;box-shadow:0 4px 16px rgba(3,45,96,.14)"/>
  </div>
</div>"""
    elif layout == "editor_tabs":
        inner = f"""
<div class="pad" style="justify-content:center">
  <p style="font-size:32px;font-weight:700;margin-bottom:20px;animation:fadeUp .5s both">Pick your editor</p>
  <div style="display:flex;gap:16px;margin-bottom:28px;animation:fadeUp .5s .12s both">
    <span style="background:var(--blue-50);color:#fff;padding:14px 28px;border-radius:8px;font-size:22px;font-weight:700">Claude Code</span>
    <span style="background:var(--orange-70);color:#032D60;padding:14px 28px;border-radius:8px;font-size:22px;font-weight:700">Cursor</span>
    <span style="background:#fff;color:var(--blue-20);padding:14px 22px;border-radius:8px;font-size:18px;font-weight:600;border:1px solid #CFE9FE">Same 18 tools</span>
  </div>
  <div style="flex:1;display:flex;align-items:flex-start;animation:fadeUp .55s .22s both">
    <img src="{image}" style="width:100%;border-radius:8px;border:1px solid #CFE9FE;box-shadow:0 4px 16px rgba(3,45,96,.14)"/>
  </div>
</div>"""
    elif layout == "proof_highlight":
        badges = scene.get("badges", [])
        badge_html = "".join(
            f'<span style="padding:12px 20px;border-radius:8px;font-size:20px;font-weight:700;'
            f'animation:pop .45s {0.12+i*0.1:.2f}s both;{b.get("style","")}">{b["text"]}</span>'
            for i, b in enumerate(badges)
        )
        cursor = ""
        if scene.get("faux_cursor"):
            cursor = """<div style="position:absolute;left:32%;top:42%;width:32px;height:32px;border-radius:50%;
              background:#41B658;border:3px solid #fff;animation:pulse 1.4s ease-in-out infinite;z-index:5"></div>"""
        scan = ""
        if scene.get("scan_highlight"):
            scan = """<div style="position:absolute;left:8%;right:8%;top:35%;height:38%;
              border:3px solid var(--orange-70);border-radius:6px;animation:fadeUp .4s .25s both;pointer-events:none"></div>"""
        inner = f"""
<div class="pad" style="justify-content:flex-start">
  <h1 style="font-size:42px;font-weight:700;animation:fadeUp .45s both">{title}</h1>
  <p style="font-size:22px;color:#5C6A7F;margin-top:8px;animation:fadeUp .45s .08s both">{subtitle}</p>
  <div style="display:flex;gap:14px;margin:14px 0 10px;flex-wrap:wrap">{badge_html}</div>
  <div style="flex:1;position:relative;display:flex;align-items:center;justify-content:center;background:#fff;
    border-radius:8px;border:2px solid var(--blue-50);padding:14px;box-shadow:0 8px 28px rgba(3,45,96,.18);
    animation:fadeUp .5s .12s both;min-height:520px">
    <img src="{image}" style="max-height:100%;max-width:100%;display:block"/>
    {cursor}{scan}
  </div>
</div>"""
    elif layout == "depth_tabs":
        img2 = img_src(scene.get("image2", ""))
        inner = f"""
<div class="pad">
  <p style="font-size:30px;font-weight:700;animation:fadeUp .45s both">Script → Flow · Salesforce architecture</p>
  <div style="flex:1;position:relative;margin-top:16px;animation:fadeUp .5s .15s both">
    <img src="{image}" style="width:100%;max-height:620px;border-radius:8px;border:1px solid #CFE9FE"/>
    <img src="{img2}" style="position:absolute;top:12px;right:12px;width:34%;border-radius:8px;border:2px solid var(--orange-70);
      box-shadow:0 6px 20px rgba(3,45,96,.2);animation:pop .5s .35s both"/>
  </div>
</div>"""
    elif layout == "cta_steps":
        inner = f"""
<div class="pad" style="justify-content:center">
  <div style="display:flex;flex-direction:column;gap:18px;margin-bottom:24px;align-items:center">
    <span style="font-size:32px;font-weight:800;background:var(--blue-50);color:#fff;padding:18px 36px;border-radius:8px;animation:pop .4s both">PICK TAB</span>
    <span style="font-size:32px;font-weight:800;background:#fff;color:var(--blue-20);padding:18px 36px;border-radius:8px;border:2px solid #0176D3;animation:pop .4s .12s both">RUN SETUP</span>
    <span style="font-size:32px;font-weight:800;background:var(--orange-70);color:#032D60;padding:18px 36px;border-radius:8px;animation:pop .4s .24s both">PROVE EXCHANGE</span>
  </div>
  <div style="flex:1;animation:fadeUp .5s .3s both"><img src="{image}" style="width:100%;border-radius:8px;border:1px solid #CFE9FE"/></div>
</div>"""
    elif layout == "cta_inguide":
        inner = f"""
<div class="pad" style="justify-content:center;align-items:center;text-align:center">
  <div style="font-size:56px;font-weight:800;animation:pop .5s both">You are in the guide.</div>
  <div style="display:flex;gap:20px;margin-top:32px;animation:fadeUp .55s .15s both">
    <span style="background:var(--blue-50);color:#fff;padding:16px 24px;border-radius:8px;font-size:24px;font-weight:700">Pick tab</span>
    <span style="background:rgba(255,255,255,.12);border:1px solid #CFE9FE;padding:16px 24px;border-radius:8px;font-size:24px">Run setup</span>
    <span style="background:rgba(255,255,255,.12);border:1px solid #CFE9FE;padding:16px 24px;border-radius:8px;font-size:24px">Prove with Exchange</span>
  </div>
  <div style="margin-top:36px;width:100%;animation:fadeUp .6s .28s both">
    <img src="{image}" style="width:100%;max-height:420px;object-fit:cover;object-position:top;border-radius:8px;opacity:.95"/>
  </div>
</div>"""
    else:
        inner = f"""
<div class="pad">
  <h1 style="font-size:48px;font-weight:700;animation:fadeUp .5s both">{title}</h1>
  <p style="font-size:26px;color:#5C6A7F;margin-top:12px;animation:fadeUp .5s .1s both">{subtitle}</p>
  <div style="flex:1;display:flex;align-items:center;justify-content:center;margin-top:20px;animation:fadeUp .55s .2s both">
    <img src="{image}" style="max-height:740px;max-width:100%;border-radius:8px;border:1px solid #CFE9FE;box-shadow:0 4px 16px rgba(3,45,96,.14)"/>
  </div>
</div>"""

    logo = ctx.logo_src
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"/><style>{ctx.base_css}</style></head>
<body class="{body}"><div class="accent-bar"></div>
<img class="logo" src="{logo}" alt=""/>{inner}</body></html>"""
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
