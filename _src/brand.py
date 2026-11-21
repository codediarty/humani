# -*- coding: utf-8 -*-
"""Humani 로고 · 파비콘 · 공유 이미지(og.png) 만들기. python3 _src/brand.py (Playwright + 로컬 Pretendard)"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
IMG = os.path.join(os.path.dirname(HERE), "docs", "assets", "img")
os.makedirs(IMG, exist_ok=True)
FONT = "file://" + os.path.join(HERE, "shop", "pretendard.css")
DEMO = json.load(open(os.path.join(HERE, "demo.json"), encoding="utf-8"))
S = {s["k"]: s for s in DEMO["samples"]}
T = S.get("thesis") or DEMO["samples"][0]


def mark(size, uid="m", ring=True):
    return ('<svg viewBox="0 0 40 40" width="%d" height="%d"><defs><linearGradient id="%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1730"/><stop offset="1" stop-color="#1b3266"/></linearGradient></defs>'
            '<rect width="40" height="40" rx="11" fill="url(#%s)"/><path d="M12.5 11v18M27.5 11v18" stroke="#fff" stroke-width="3.3" stroke-linecap="round"/><path d="M12.5 19.6q7.5 3.8 15 0" stroke="#fff" stroke-width="3.3" fill="none" stroke-linecap="round"/>'
            '<circle cx="31.6" cy="31.6" r="5.6" fill="#10b981" stroke="#0b1730" stroke-width="2"/><path d="m29.2 31.7 1.6 1.6 3.1-3.3" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>') % (size, size, uid, uid)


FAVICON_SVG = mark(40).replace('width="40" height="40"', '').replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')

BASE = "<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s'><style>*{box-sizing:border-box;margin:0;padding:0}html,body{font-family:'Pretendard Variable',sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.02em;color:#0b1220}</style>%%s</head><body>%%s</body></html>" % FONT


def icon_html(px, pad):
    return BASE % ("<style>body{width:%dpx;height:%dpx;background:transparent;display:grid;place-items:center}</style>" % (px, px), mark(px - pad * 2, "i"))


def og_html():
    b, a = T["before"]["rate"], T["after"]["rate"]
    return BASE % ("""<style>
body{width:1200px;height:630px;position:relative;overflow:hidden;background:radial-gradient(800px 500px at 100% 0%,rgba(124,58,237,.22),transparent 60%),radial-gradient(700px 480px at 0% 100%,rgba(16,185,129,.22),transparent 60%),#0b1730;color:#fff}
body:before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.08) 1px,transparent 1.3px);background-size:24px 24px}
.br{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px}
.br b{font-size:42px;font-weight:860;letter-spacing:-.035em}
.br small{display:block;font-size:13px;font-weight:700;letter-spacing:.26em;color:#94a3b8;margin-top:2px}
h1{position:absolute;left:72px;top:176px;font-size:66px;line-height:1.18;font-weight:860;letter-spacing:-.045em}
h1 u{text-decoration:none;background:linear-gradient(transparent 78%,rgba(225,29,72,.85) 78%,rgba(225,29,72,.85) 92%,transparent 92%)}
h1 em{font-style:normal;color:#34d399}
.sub{position:absolute;left:74px;top:350px;font-size:25px;color:#cbd5e1;font-weight:600}
.meter{position:absolute;left:72px;bottom:66px;display:flex;align-items:center;gap:22px}
.m{padding:18px 24px;border-radius:20px;border:1.5px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06)}
.m small{display:block;font-size:16px;color:#94a3b8;font-weight:700}
.m b{font-size:52px;font-weight:860;letter-spacing:-.04em}
.m.bad b{color:#fb7185}.m.good b{color:#34d399}
.ar{font-size:40px;color:#94a3b8}
.dom{position:absolute;right:72px;bottom:74px;font-size:28px;font-weight:800;color:#34d399}
.tag{position:absolute;right:72px;top:72px;padding:10px 18px;border-radius:999px;background:#10b981;color:#fff;font-size:20px;font-weight:800}
</style>""", """<div class="br">%s<div><b>Humani</b><small>AI HUMANIZER</small></div></div><div class="tag">무료 AI 작성률 검사</div>
<h1><u>AI 작성률</u>에 걸리는 문장만<br><em>사람 문장</em>으로 바꿉니다</h1>
<div class="sub">한국어 AI 휴머나이징 전문 서비스 · 카피킬러 · GPT킬러 대응</div>
<div class="meter"><div class="m bad"><small>휴머나이징 전 AI 작성률</small><b>%s%%</b></div><span class="ar">→</span><div class="m good"><small>한 번 휴머나이징 뒤</small><b>%s%%</b></div></div>
<div class="dom">humanai.io.kr</div>""" % (mark(64, "o"), b, a))


async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await br.new_page(device_scale_factor=1)
        async def shot(html, w, h, path, omit_bg=False, typ="png"):
            f = os.path.join(HERE, "shop", "_t_brand.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.set_viewport_size({"width": w, "height": h})
            await pg.goto("file://" + f)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(200)
            await pg.screenshot(path=path, omit_background=omit_bg, type=typ)
        await shot(icon_html(512, 0), 512, 512, os.path.join(IMG, "logo-512.png"), True)
        await shot(icon_html(192, 0), 192, 192, os.path.join(IMG, "logo-192.png"), True)
        await shot(icon_html(180, 14).replace("background:transparent", "background:#ffffff"), 180, 180, os.path.join(IMG, "apple-touch-icon.png"))
        await shot(icon_html(48, 0), 48, 48, os.path.join(HERE, "shop", "_fav48.png"), True)
        await shot(og_html(), 1200, 630, os.path.join(IMG, "og.png"))
        await br.close()
    open(os.path.join(IMG, "favicon.svg"), "w", encoding="utf-8").write(FAVICON_SVG)
    from PIL import Image
    im = Image.open(os.path.join(HERE, "shop", "_fav48.png")).convert("RGBA")
    im.save(os.path.join(os.path.dirname(HERE), "docs", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    print("ok", sorted(os.listdir(IMG)))

asyncio.run(main())
