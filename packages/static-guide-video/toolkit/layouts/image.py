from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    title = scene.get("title", "")
    subtitle = scene.get("subtitle", "")
    image = scene_image(scene)
    return f"""
<div class="pad">
  <h1 style="font-size:48px;font-weight:700;animation:fadeUp .5s both">{title}</h1>
  <p style="font-size:26px;color:#5C6A7F;margin-top:12px;animation:fadeUp .5s .1s both">{subtitle}</p>
  <div style="flex:1;display:flex;align-items:center;justify-content:center;margin-top:20px;animation:fadeUp .55s .2s both">
    <img src="{image}" style="max-height:740px;max-width:100%;border-radius:8px;border:1px solid #CFE9FE;box-shadow:0 4px 16px rgba(3,45,96,.14)"/>
  </div>
</div>"""