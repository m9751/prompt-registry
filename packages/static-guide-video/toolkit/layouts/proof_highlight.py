from __future__ import annotations

from ._helpers import scene_image


def render(scene: dict) -> str:
    title = scene.get("title", "")
    subtitle = scene.get("subtitle", "")
    image = scene_image(scene)
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
    return f"""
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