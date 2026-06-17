from __future__ import annotations


def render(scene: dict) -> str:
    return """
<div class="pad" style="justify-content:center;align-items:center;text-align:center">
  <div style="font-size:120px;font-weight:800;color:#fff;animation:pop .5s cubic-bezier(.16,1,.3,1) both">847 lines</div>
  <div style="display:flex;gap:14px;justify-content:center;margin-top:28px;flex-wrap:wrap">
    <span style="padding:10px 18px;border-radius:20px;border:1px solid var(--red);color:#FFB3BC;background:rgba(234,0,30,.15);font-weight:700;animation:fadeUp .5s .15s both">No tests</span>
    <span style="padding:10px 18px;border-radius:20px;border:1px solid var(--orange-70);color:#FFE2C8;background:rgba(254,147,57,.15);font-weight:700;animation:fadeUp .5s .25s both">Schema drift</span>
    <span style="padding:10px 18px;border-radius:20px;border:1px solid #CFE9FE;color:#CFE9FE;font-weight:700;animation:fadeUp .5s .35s both">FIXME</span>
  </div>
  <p style="font-size:28px;color:#CFE9FE;margin-top:40px;animation:fadeUp .5s .4s both">Five portals <span style="color:var(--orange-70)">→</span> <strong style="color:var(--cloud-60)">one editor</strong></p>
</div>"""