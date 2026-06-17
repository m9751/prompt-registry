# static-guide-video

Reusable toolkit extracted from the [mulesoft-claude-onboarding](https://github.com/m9751/mulesoft-claude-onboarding) pilot.

| Artifact | Location |
|----------|----------|
| Agent prompt | `PRM-PDLV-006` in prompt-registry |
| Packaging blueprint | `docs/static-guide-video-packaging.md` |
| Scene schema | `schema/scenes.schema.json` |
| Capture schema | `schema/captures.schema.json` |
| Brand example | `schema/brand.example.json` |
| Build engine | `toolkit/build_video.py` |
| Capture runner | `toolkit/capture_runner.py` |
| Pilot captures | `pilots/mulesoft-claude-onboarding/captures.yaml` |
| Layout modules | `toolkit/layouts/` (one file per layout type) |
| Smoke test template | `templates/smoke-test.sh` |

## Quick start (pilot rebuild)

From the pilot `demo-output/` directory:

```bash
python3 /path/to/prompt-registry/packages/static-guide-video/toolkit/build_video.py   --root .   --manifest scenes.json   --brand ../path/to/brand.json   --captures ../path/to/prompt-registry/packages/static-guide-video/pilots/mulesoft-claude-onboarding/captures.yaml
```

Or symlink/copy `captures.yaml` into `demo-output/` and omit `--captures`.

## CLI (`build_video.py`)

| Flag | Default | Purpose |
|------|---------|---------|
| `--root` | cwd | `demo-output` working directory |
| `--manifest` | `<root>/scenes.json` | Scene story SSOT |
| `--brand` | (none) | Inject CSS vars + logo from `brand.json` |
| `--captures` | `<root>/captures.yaml` if present | Live Playwright capture script |
| `--skip-captures` | off | Skip capture stage |
| `--hero-only` | off | Captures + silent hero only |

Outputs (under `--root`):

- `captures/*.png` — live guide screenshots
- `frames/*.png` — rendered scene stills
- `audio/*.mp3` — edge-tts narration
- `clips/*.mp4` — per-scene segments
- `output.mp4` — full narrated video (ffmpeg concat **re-encode**, never stream-copy)
- `output-hero-silent.mp4` — optional silent hero from `hero_silent` in manifest

### edge-tts resolution

1. `EDGE_TTS` env var (path to binary)
2. Hardcoded fallback path (pilot machine)
3. `python3 -m edge_tts`

## Capture runner (`capture_runner.py`)

Runs `captures.yaml` independently:

```bash
python3 toolkit/capture_runner.py pilots/mulesoft-claude-onboarding/captures.yaml -o /tmp/captures
```

Supported actions: `goto`, `click`, `scroll`, `wait`, `screenshot`, `screenshot_locator`.

## Post-deploy smoke test

```bash
./templates/smoke-test.sh
./templates/smoke-test.sh https://my-guide.vercel.app https://smokin-territory.vercel.app/api/beacon my-proposal-id
```

## Dependencies

- Python 3.9+
- `playwright` (+ `playwright install chromium`)
- `pyyaml` (for captures.yaml)
- `edge-tts`
- `ffmpeg` / `ffprobe`

Pilot reference: `mulesoft-claude-onboarding/demo-output/`.
