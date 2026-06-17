from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    image = scene_image(scene)
    return f"""
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