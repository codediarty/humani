# -*- coding: utf-8 -*-
"""Humani 로고 · 파비콘 · 앱 아이콘 · 공유 이미지(og.png) 만들기.  python3 _src/brand.py

로고는 대표가 준 로봇 마스코트(_src/shop/robot_src.png, 흰 배경)를 배경 없이 딴 _src/shop/robot_full.png 로 만듭니다.
(배경 따기: _src/shop/robot_cut.py)  머리 부분은 작은 로고 · 파비콘, 전신은 첫 화면 · 공유 이미지 · 조직 로고에 씁니다.
"""
import asyncio, base64, io, json, os, sys
from PIL import Image, ImageFilter, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "docs", "assets", "img")
os.makedirs(IMG, exist_ok=True)
SHOP = os.path.join(HERE, "shop")
FONT = "file://" + os.path.join(SHOP, "pretendard.css")
DEMO = json.load(open(os.path.join(HERE, "demo.json"), encoding="utf-8"))
S = {s["k"]: s for s in DEMO["samples"]}
T = S.get("thesis") or DEMO["samples"][0]

ROBOT = Image.open(os.path.join(SHOP, "robot_full.png")).convert("RGBA")   # 854 x 914, 투명 배경
HEAD_BOX = (95, 0, 835, 640)   # 안테나 공부터 얼굴 아래까지(귀 H 포함)


def head():
    return ROBOT.crop(HEAD_BOX)


def fit(im, w, h=None, sharpen=0):
    h = h or round(im.height * w / im.width)
    out = im.resize((w, h), Image.LANCZOS)
    if sharpen:
        out = out.filter(ImageFilter.UnsharpMask(radius=0.6, percent=sharpen, threshold=1))
    return out


def square(im, size, pad=0.0, bg=None, radius=0):
    """정사각형 가운데에 앉히기. pad = 바깥 여백 비율. bg = (위 색, 아래 색) 그라데이션"""
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if bg:
        top, bot = bg
        g = Image.new("RGBA", (1, size))
        for y in range(size):
            k = y / max(1, size - 1)
            g.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)) + (255,))
        g = g.resize((size, size))
        if radius:
            m = Image.new("L", (size, size), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
            c.paste(g, (0, 0), m)
        else:
            c = g
    inner = int(size * (1 - 2 * pad))
    k = min(inner / im.width, inner / im.height)
    t = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    if size <= 64:
        t = t.filter(ImageFilter.UnsharpMask(radius=0.5, percent=60, threshold=1))
    c.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2))
    return c


def save_png(im, name):
    p = os.path.join(IMG, name)
    im.save(p, optimize=True)
    return p


def save_webp(im, name, q=88):
    p = os.path.join(IMG, name)
    im.save(p, "WEBP", quality=q, method=6)
    return p


BASE = ("<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s'>"
        "<style>*{box-sizing:border-box;margin:0;padding:0}html,body{font-family:'Pretendard Variable',sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.02em;color:#0e1d44}</style>%%s</head><body>%%s</body></html>") % FONT


def og_html(robot_uri, head_uri):
    b, a = T["before"]["rate"], T["after"]["rate"]
    return BASE % ("""<style>
body{width:1200px;height:630px;position:relative;overflow:hidden;background:
 radial-gradient(620px 420px at 86% 30%,rgba(8,168,250,.20),transparent 62%),
 radial-gradient(520px 360px at 8% 100%,rgba(118,80,240,.10),transparent 60%),
 linear-gradient(180deg,#f7f9fe 0%,#eaf0fc 100%)}
.br{position:absolute;left:76px;top:62px;display:flex;align-items:center;gap:14px}
.br img{height:58px}
.br b{display:block;font-size:40px;font-weight:850;letter-spacing:-.04em;line-height:1}
.br small{display:block;font-size:17px;font-weight:650;color:#5b6b8f;margin-top:5px;letter-spacing:-.01em}
h1{position:absolute;left:76px;top:168px;font-size:70px;line-height:1.14;font-weight:850;letter-spacing:-.05em;color:#0e1d44}
.sub{position:absolute;left:78px;top:350px;font-size:25px;color:#43517a;font-weight:600;letter-spacing:-.02em}
.visor{position:absolute;left:76px;bottom:62px;display:flex;align-items:center;gap:26px;padding:22px 30px;border-radius:26px;
 background:linear-gradient(160deg,#16306a 0%,#0c1e43 46%,#1f2a8f 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 24px 50px -24px rgba(14,29,68,.55)}
.visor small{display:block;font-size:16px;font-weight:700;color:#9fb6e8;letter-spacing:-.01em}
.visor b{display:block;font-size:56px;font-weight:850;letter-spacing:-.04em;line-height:1.05;font-variant-numeric:tabular-nums}
.visor .from b{color:#ff8aa8}
.visor .to b{color:#e9fdf9;text-shadow:0 0 18px rgba(2,198,252,.85),0 0 4px rgba(2,198,252,.6)}
.visor .ar{width:46px;height:2px;background:linear-gradient(90deg,#ff8aa8,#5fe3ff);position:relative}
.visor .ar:after{content:"";position:absolute;right:-2px;top:-6px;border:7px solid transparent;border-left:10px solid #5fe3ff;border-right:0}
.dom{position:absolute;right:70px;bottom:44px;font-size:24px;font-weight:800;color:#1d64f2;letter-spacing:-.01em}
.robot{position:absolute;right:46px;top:44px;height:500px}
</style>""", """<div class="br"><img src="%s" alt=""><div><b>Humani</b><small>한국어 AI 휴머나이저 · 휴머나이</small></div></div>
<h1>AI 작성률은 낮추고,<br>원문의 의미는 그대로.</h1>
<div class="sub">AI 작성 흔적이 있는 문장만 사람 문장으로 바꿉니다</div>
<div class="visor"><div class="from"><small>휴머나이징 전 AI 작성률</small><b>%s%%</b></div><span class="ar"></span><div class="to"><small>한 번 휴머나이징 뒤</small><b>%s%%</b></div></div>
<img class="robot" src="%s" alt="">
<div class="dom">humanai.io.kr</div>""" % (head_uri, b, a, robot_uri))


def data_uri(im, fmt="PNG"):
    buf = io.BytesIO()
    im.save(buf, fmt)
    return "data:image/%s;base64,%s" % (fmt.lower(), base64.b64encode(buf.getvalue()).decode())


async def render_og(path):
    from playwright.async_api import async_playwright
    robot_uri = data_uri(fit(ROBOT, 520))
    head_uri = data_uri(fit(head(), 140))
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await br.new_page(device_scale_factor=1, viewport={"width": 1200, "height": 630})
        f = os.path.join(SHOP, "_t_brand.html")
        open(f, "w", encoding="utf-8").write(og_html(robot_uri, head_uri))
        await pg.goto("file://" + f)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(250)
        await pg.screenshot(path=path, type="png")
        await br.close()


def main():
    H = head()
    # 머리글 로고(머리 · 안테나 · 귀 H): 화면 40px 높이 기준 3배
    hl = fit(H, round(H.width * 120 / H.height), 120)
    save_png(hl, "humani-head.png")
    save_webp(hl, "humani-head.webp", 90)
    # 전신 마스코트(첫 화면 · 마지막 권유): 1x 300 · 2x 600
    for w in (300, 600):
        r = fit(ROBOT, w)
        save_png(r, "humani-robot-%d.png" % w)
        save_webp(r, "humani-robot-%d.webp" % w, 88)
    # 파비콘(머리)
    for s in (32, 96, 192):
        save_png(square(H, s, pad=0.0), "favicon-%d.png" % s)
    ico = [square(H, s, pad=0.0) for s in (16, 32, 48)]
    ico[2].save(os.path.join(ROOT, "docs", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    svg = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64"><image width="64" height="64" xlink:href="%s"/></svg>' % data_uri(square(H, 64))
    open(os.path.join(IMG, "favicon.svg"), "w").write(svg)
    # 앱 아이콘(홈 화면): 옅은 하늘색 바탕 + 머리, 가장자리 안전 영역 확보
    bg = ((246, 249, 255), (219, 232, 255))
    save_png(square(H, 180, pad=0.12, bg=bg).convert("RGB"), "apple-touch-icon.png")
    for s in (192, 512):
        save_png(square(H, s, pad=0.16, bg=bg), "icon-%d.png" % s)
    # 조직 로고(검색 결과 · 구조화 데이터): 전신, 투명 배경
    for s in (192, 512):
        save_png(square(ROBOT, s, pad=0.04), "logo-%d.png" % s)
    asyncio.run(render_og(os.path.join(IMG, "og.png")))
    Image.open(os.path.join(IMG, "og.png")).convert("RGB").save(os.path.join(IMG, "og.jpg"), quality=90, optimize=True, progressive=True)
    print("ok", sorted(os.listdir(IMG)))


if __name__ == "__main__":
    main()
