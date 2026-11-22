# -*- coding: utf-8 -*-
# Humani 아임웹 상품 이미지 만들기 (성균관컨설팅 skkc.co.kr 상품용)
# python3 _src/shop/render.py
#   -> _src/shop/out/hm-<id>-1x1.jpg (1200x1200), hm-tokens-guide.png (1080x1350)
#   -> docs/assets/product/ 에도 복사 (사이트 Product 구조화 데이터 · OG 에서 씀)
# 전후 AI 작성률 숫자는 _src/demo.json(Humani 엔진 실측값)의 논문 예시를 그대로 씀
import asyncio, json, os, shutil
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC)
OUT = os.path.join(HERE, "out")
PROD = os.path.join(ROOT, "docs", "assets", "product")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PROD, exist_ok=True)
FONT = "file://" + os.path.join(HERE, "pretendard.css")

DEMO = json.load(open(os.path.join(SRC, "demo.json"), encoding="utf-8"))
S = {s["k"]: s for s in DEMO["samples"]}
T = S.get("thesis") or DEMO["samples"][0]
B_RATE, A_RATE = T["before"]["rate"], T["after"]["rate"]
DEMO_CAP = "실측 · %s 한 번 휴머나이징" % T.get("label", "논문")

PACKS = [
    {"id": "lt", "name": "라이트", "tok": "100", "price": "9,900원", "list": "19,800원", "per": "토큰당 99원", "save": "", "badge": "", "fit": "짧은 과제 · 자기소개서 한두 문항"},
    {"id": "pl", "name": "플러스", "tok": "350", "price": "19,900원", "list": "39,800원", "per": "토큰당 약 57원", "save": "", "badge": "", "fit": "레포트 여러 편 · 자소서 한 세트"},
    {"id": "pr", "name": "프로", "tok": "1,000", "price": "39,900원", "list": "79,800원", "per": "토큰당 약 40원", "save": "플러스 대비 토큰당 약 30% 절약", "plus": "56,857원", "pct": "약 30% 절약", "badge": "BEST 추천", "fit": "학기 과제 전체 · 논문 한 장(章)"},
    {"id": "mx", "name": "맥스", "tok": "2,000", "price": "69,900원", "list": "139,800원", "per": "토큰당 약 34원", "save": "플러스 대비 토큰당 약 40% 절약", "plus": "113,714원", "pct": "약 40% 절약", "badge": "최고 혜택", "fit": "학위논문 전체 · 팀 · 여러 명"},
]


import base64, io
from PIL import Image
ROBOT = Image.open(os.path.join(HERE, "robot_full.png")).convert("RGBA")
HEAD = ROBOT.crop((95, 0, 835, 640))


def uri(im, w):
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


ROBOT_URI = uri(ROBOT, 720)
HEAD_URI = uri(HEAD, 220)
SPARK = ('<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#5fe3ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>')
CHECK = ('<svg viewBox="0 0 24 24" width="26" height="26" fill="none"><circle cx="12" cy="12" r="11" fill="#e1ebff"/>'
         '<path d="m7.5 12.3 3 3 6-6.3" stroke="#1a63f2" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

BASE = ("<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s'><style>"
        "*{box-sizing:border-box;margin:0;padding:0}html,body{font-family:'Pretendard Variable',Pretendard,sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.02em;color:#0e1d44;word-break:keep-all}"
        "%%s</style></head><body>%%s</body></html>") % FONT

# 2026.11.21 고급형: 밝은 바탕 · 절제된 글자 · 로봇 마스코트(빛 번짐 · 기울임 같은 장식 없음) · 검사기 이름은 적지 않음
THUMB_CSS = """
body{width:1200px;height:1200px;position:relative;overflow:hidden;background:linear-gradient(160deg,#f5f8ff 0%,#eef3fc 100%)}
body:before{content:"";position:absolute;inset:0;background-image:linear-gradient(to right,rgba(16,24,40,.04) 1px,transparent 1px),linear-gradient(to bottom,rgba(16,24,40,.04) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(ellipse 80% 60% at 30% 20%,#000 30%,transparent 100%)}
.brand{position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:14px}
.brand img{height:62px}
.brand b{display:block;font-size:42px;font-weight:750;letter-spacing:-.04em;color:#101828;line-height:1}
.brand small{display:block;font-size:19px;font-weight:600;color:#667085;margin-top:6px;letter-spacing:-.01em}
.badge{position:absolute;right:80px;top:84px;height:52px;padding:0 24px;border-radius:26px;display:flex;align-items:center;font-size:24px;font-weight:700;letter-spacing:-.02em}
.badge.best{background:#155eef;color:#fff}
.badge.top{background:#101828;color:#fff}
.badge.sale{background:#fff;color:#344054;border:1.5px solid #d0d5dd}
.kick{position:absolute;left:84px;top:280px;font-size:28px;font-weight:650;color:#155eef;letter-spacing:-.02em}
.name{position:absolute;left:82px;top:322px;font-size:54px;font-weight:700;color:#101828;letter-spacing:-.04em}
.big{position:absolute;left:72px;top:416px;display:flex;align-items:flex-end;color:#101828}
.big b{font-size:@BIGPX@px;font-weight:700;letter-spacing:-.06em;line-height:.88;font-variant-numeric:tabular-nums}
.big span{font-size:58px;font-weight:650;margin:0 0 14px 14px;color:#344054}
.per{position:absolute;left:84px;top:@PERTOP@px;font-size:27px;font-weight:600;color:#5d6b82}
.per b{color:#067647;font-weight:650;margin-left:12px}
.robot{position:absolute;right:52px;top:214px;width:@RW@px}
.panel{position:absolute;left:56px;right:56px;bottom:56px;height:340px;border-radius:32px;background:#fff;border:1.5px solid #e4e7ec;box-shadow:0 24px 48px -16px rgba(16,24,40,.14)}
.ttl{position:absolute;left:52px;top:46px;font-size:40px;font-weight:700;letter-spacing:-.04em;color:#101828;line-height:1.25}
.chips{position:absolute;left:52px;bottom:48px;display:flex;flex-direction:column;gap:10px}
.chip{display:flex;align-items:center;gap:10px;font-size:23px;font-weight:600;color:#344054}
.chip svg{flex:none}
.price{position:absolute;right:52px;bottom:40px;text-align:right}
.price .row1{display:flex;align-items:baseline;gap:14px;justify-content:flex-end;font-size:26px;font-weight:600;color:#98a2b3}
.price .row1 del{text-decoration-thickness:2px}
.price .row1 em{font-style:normal;color:#067647;font-weight:700}
.price b{display:block;font-size:84px;font-weight:700;letter-spacing:-.045em;color:#101828;line-height:1.05;font-variant-numeric:tabular-nums}
.dom{position:absolute;right:52px;top:52px;font-size:22px;font-weight:650;color:#155eef;letter-spacing:-.01em}
"""
CHECK2 = ('<svg viewBox="0 0 24 24" width="26" height="26" fill="none"><circle cx="12" cy="12" r="11" fill="#ecfdf3" stroke="#abefc6"/>'
          '<path d="m7.6 12.2 2.9 2.9 5.9-6.1" stroke="#079455" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def thumb_html(p):
    small = len(p["tok"]) > 3
    css = (THUMB_CSS.replace("@BIGPX@", str(196 if small else 232)).replace("@RW@", str(420 if small else 460))
           .replace("@PERTOP@", str(612 if small else 642)))
    if p["badge"] == "BEST 추천":
        badge = '<div class="badge best">BEST 추천</div>'
    elif p["badge"]:
        badge = '<div class="badge top">%s</div>' % p["badge"]
    else:
        badge = ""   # 2026.11.22 대표: 정가 · 50% 표시는 빼고 카피휴먼처럼 프로 · 맥스만 플러스 단가 기준 금액
    save = ('<b>%s</b>' % p["save"]) if p["save"] else ""
    chips = "".join('<div class="chip">%s%s</div>' % (CHECK2, t) for t in ("월 구독 없이 한 번 충전", "쓴 만큼 차감 · 기한 무제한", "결제 후 즉시 메일로 코드 발송"))
    body = """
<div class="brand"><img src="%s" alt=""><div><b>Humani</b><small>한국어 AI 휴머나이저</small></div></div>%s
<div class="kick">AI 휴머나이저 토큰</div>
<div class="name">%s</div>
<div class="big"><b>%s</b><span>토큰</span></div>
<div class="per">%s%s</div>
<img class="robot" src="%s" alt="">
<div class="panel">
 <div class="ttl">AI 작성률은 낮추고,<br>원문의 의미는 그대로.</div>
 <div class="dom">humanai.io.kr</div>
 <div class="chips">%s</div>
 <div class="price">%s<b>%s</b></div>
</div>""" % (HEAD_URI, badge, p["name"], p["tok"], p["per"], save, ROBOT_URI, chips,
       ('<div class="row1"><del>플러스 단가 기준 %s</del><em>%s</em></div>' % (p["plus"], p["pct"])) if p.get("plus") else "", p["price"])
    return BASE % (css, body)


GUIDE_STEPS = [
    ("결제하면 메일로 토큰 코드가 옵니다", "결제가 확인되면 보통 1분 안에, 주문할 때 적은 이메일로 16자리 코드를 보내 드립니다. 보내는 이름은 'Humani'입니다. 받은편지함에 없으면 스팸함과 프로모션함을 확인해 주세요."),
    ("메일의 <em>바로 이어서 하기</em>를 누르면 끝", "코드가 들어간 채로 Humani가 열립니다. 충전하러 가기 전에 하던 글은 같은 기기에서 24시간 보관돼 그대로 이어집니다. 다른 기기에서는 '토큰 코드 넣기'에 코드를 넣으면 됩니다."),
    ("쓴 만큼만 빠집니다", "AI 작성률 요약은 0토큰, 문장별 전체 결과는 1,000자당 2토큰, 휴머나이징은 1,000자당 4토큰입니다. 남은 토큰은 위쪽 토큰 단추에서 언제든 확인합니다."),
    ("남은 토큰은 기한 없이 이어서", "같은 코드에 더 충전할 수 있고, 여러 기기에서 같은 코드를 씁니다. 코드를 아는 사람은 누구나 쓸 수 있으니 메일을 지우지 말고 잘 보관해 주세요."),
]


def guide_html():
    steps = "".join('<div class="st"><div class="n">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, h, t) for i, (h, t) in enumerate(GUIDE_STEPS))
    css = """
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#f8fafc}
.top{position:absolute;left:0;top:0;width:1080px;height:400px;overflow:hidden;background:linear-gradient(180deg,#f5f8ff,#eef3fc);border-bottom:1px solid #e4e7ec}
.brand{position:absolute;left:76px;top:64px;display:flex;align-items:center;gap:14px}
.brand img{height:58px}
.brand b{display:block;font-size:40px;font-weight:750;letter-spacing:-.04em;color:#101828;line-height:1}
.brand small{display:block;font-size:18px;font-weight:600;color:#667085;margin-top:6px}
h1{position:absolute;left:76px;top:170px;font-size:72px;font-weight:700;letter-spacing:-.045em;color:#101828}
.lead{position:absolute;left:78px;top:272px;font-size:27px;color:#5d6b82;font-weight:600}
.robot{position:absolute;right:60px;top:56px;width:250px}
.list{position:absolute;left:64px;top:440px;width:952px;display:flex;flex-direction:column;gap:16px}
.st{display:flex;gap:24px;background:#fff;border:1.5px solid #e4e7ec;border-radius:24px;padding:24px 30px}
.n{flex:none;width:52px;height:52px;border-radius:14px;background:#eff4ff;border:1.5px solid #d1e0ff;color:#155eef;font-size:26px;font-weight:700;display:flex;align-items:center;justify-content:center}
h3{font-size:31px;font-weight:700;letter-spacing:-.035em;margin:4px 0 8px;color:#101828}
h3 em{font-style:normal;color:#155eef}
p{font-size:22.5px;line-height:1.6;color:#475467;font-weight:500}
.ft{position:absolute;left:78px;right:78px;bottom:40px;border-top:1px solid #e4e7ec;padding-top:20px;display:flex;justify-content:space-between;align-items:flex-end;color:#667085;font-size:21px;line-height:1.6}
.ft b{color:#155eef;font-size:28px;font-weight:700}
"""
    body = """<div class="top"><div class="brand"><img src="%s" alt=""><div><b>Humani</b><small>한국어 AI 휴머나이저 · 휴머나이</small></div></div>
<h1>토큰 이용 안내</h1><div class="lead">월 구독 없이 한 번 충전하고, 쓴 만큼만 빠집니다</div><img class="robot" src="%s" alt=""></div>
<div class="list">%s</div>
<div class="ft"><div>문의 contact@skkc.co.kr<br>판매 성균관컨설팅 · 서비스 Humani(휴머나이)</div><b>humanai.io.kr</b></div>""" % (HEAD_URI, ROBOT_URI, steps)
    return BASE % (css, body)


async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await br.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=1)
        for p in PACKS:
            f = os.path.join(HERE, "_t_%s.html" % p["id"])
            open(f, "w", encoding="utf-8").write(thumb_html(p))
            await pg.goto("file://" + f)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(OUT, "hm-%s-1x1.jpg" % p["id"]), type="jpeg", quality=92)
        await pg.set_viewport_size({"width": 1080, "height": 1350})
        f = os.path.join(HERE, "_t_guide.html")
        open(f, "w", encoding="utf-8").write(guide_html())
        await pg.goto("file://" + f)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=os.path.join(OUT, "hm-tokens-guide.png"))
        await br.close()
    for n in sorted(os.listdir(OUT)):
        shutil.copy(os.path.join(OUT, n), os.path.join(PROD, n))
    print("ok", sorted(os.listdir(OUT)), "before/after", B_RATE, A_RATE)

asyncio.run(main())
