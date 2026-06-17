from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    image = scene_image(scene)
    return f"""
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