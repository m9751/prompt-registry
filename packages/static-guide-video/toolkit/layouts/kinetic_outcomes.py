from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    image = scene_image(scene)
    return f"""
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