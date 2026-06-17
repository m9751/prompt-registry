from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    image = scene_image(scene)
    return f"""
<div class="pad" style="justify-content:center">
  <div style="display:flex;flex-direction:column;gap:18px;margin-bottom:24px;align-items:center">
    <span style="font-size:32px;font-weight:800;background:var(--blue-50);color:#fff;padding:18px 36px;border-radius:8px;animation:pop .4s both">PICK TAB</span>
    <span style="font-size:32px;font-weight:800;background:#fff;color:var(--blue-20);padding:18px 36px;border-radius:8px;border:2px solid #0176D3;animation:pop .4s .12s both">RUN SETUP</span>
    <span style="font-size:32px;font-weight:800;background:var(--orange-70);color:#032D60;padding:18px 36px;border-radius:8px;animation:pop .4s .24s both">PROVE EXCHANGE</span>
  </div>
  <div style="flex:1;animation:fadeUp .5s .3s both"><img src="{image}" style="width:100%;border-radius:8px;border:1px solid #CFE9FE"/></div>
</div>"""