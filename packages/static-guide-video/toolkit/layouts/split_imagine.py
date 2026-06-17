from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    title = scene.get("title", "")
    subtitle = scene.get("subtitle", "")
    image = scene_image(scene)
    return f"""
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