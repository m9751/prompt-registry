from __future__ import annotations

from ._helpers import scene_image, scene_image2


def render(scene: dict) -> str:
    image = scene_image(scene)
    img2 = scene_image2(scene)
    return f"""
<div class="pad">
  <p style="font-size:30px;font-weight:700;animation:fadeUp .45s both">Script → Flow · Salesforce architecture</p>
  <div style="flex:1;position:relative;margin-top:16px;animation:fadeUp .5s .15s both">
    <img src="{image}" style="width:100%;max-height:620px;border-radius:8px;border:1px solid #CFE9FE"/>
    <img src="{img2}" style="position:absolute;top:12px;right:12px;width:34%;border-radius:8px;border:2px solid var(--orange-70);
      box-shadow:0 6px 20px rgba(3,45,96,.2);animation:pop .5s .35s both"/>
  </div>
</div>"""