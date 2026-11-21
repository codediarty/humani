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
    {"id": "pl", "name": "플러스", "tok": "300", "price": "19,900원", "list": "39,800원", "per": "토큰당 약 66원", "save": "", "badge": "", "fit": "레포트 여러 편 · 자소서 한 세트"},
    {"id": "pr", "name": "프로", "tok": "750", "price": "39,900원", "list": "79,800원", "per": "토큰당 약 53원", "save": "플러스보다 토큰당 20% 절약", "badge": "BEST 추천", "fit": "학기 과제 전체 · 논문 한 장(章)"},
    {"id": "mx", "name": "맥스", "tok": "1,500", "price": "69,900원", "list": "139,800원", "per": "토큰당 약 47원", "save": "플러스보다 토큰당 30% 절약", "badge": "최고 혜택", "fit": "학위논문 전체 · 팀 · 여러 명"},
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

# 2026.11.21 새 로고(로봇) · 사이트와 같은 색(얼굴 화면 남색 · 파랑) · 검사기 이름은 적지 않음
THUMB_CSS = """
body{width:1200px;height:1200px;position:relative;overflow:hidden;background:#eef2fb}
.hero{position:absolute;left:0;top:0;width:1200px;height:800px;overflow:hidden;
 background:radial-gradient(520px 420px at 82% 32%,rgba(8,168,250,.42),transparent 66%),
 radial-gradient(120% 90% at 18% 0%,rgba(52,98,196,.55) 0%,transparent 55%),
 linear-gradient(165deg,#132b62 0%,#0c1e43 52%,#1b2788 100%)}
.hero:before{content:"";position:absolute;inset:0;background-image:linear-gradient(to bottom,rgba(255,255,255,.045) 1px,transparent 1px);background-size:100% 40px}
.brand{position:absolute;left:80px;top:66px;display:flex;align-items:center;gap:14px;z-index:2}
.brand img{height:76px}
.brand b{display:block;font-size:50px;font-weight:860;letter-spacing:-.04em;color:#fff;line-height:1}
.brand small{display:block;font-size:20px;font-weight:650;color:#a9bdf0;margin-top:6px;letter-spacing:-.01em}
.badge{position:absolute;right:80px;top:80px;height:58px;padding:0 28px;border-radius:29px;display:flex;align-items:center;font-size:28px;font-weight:850;z-index:4;letter-spacing:-.02em}
.badge.best{background:linear-gradient(180deg,#fcd34d,#fbbf24);color:#1a1205;box-shadow:0 10px 24px -8px rgba(251,191,36,.7)}
.badge.top{background:#fff;color:#0e1d44;box-shadow:0 10px 24px -10px rgba(255,255,255,.6)}
.badge.sale{background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.3);color:#fff}
.kick{position:absolute;left:84px;top:206px;display:flex;align-items:center;gap:12px;color:#dbe6ff;font-size:31px;font-weight:750;z-index:2}
.pills{position:absolute;left:82px;top:272px;display:flex;gap:14px;z-index:2}
.pill{height:58px;padding:0 26px;border-radius:29px;display:flex;align-items:center;font-size:29px;font-weight:850}
.pill.n{background:linear-gradient(180deg,#2a72ff,#1a63f2);color:#fff;box-shadow:0 10px 22px -10px rgba(26,99,242,.9)}
.pill.o{border:2px solid rgba(255,255,255,.34);color:#fff;font-weight:750}
.big{position:absolute;left:72px;top:342px;display:flex;align-items:flex-end;color:#fff;z-index:2}
.big b{font-size:@BIGPX@px;font-weight:880;letter-spacing:-.065em;line-height:.9;text-shadow:0 18px 40px rgba(0,0,0,.35);font-variant-numeric:tabular-nums}
.big span{font-size:62px;font-weight:850;margin:0 0 16px 16px}
.robot{position:absolute;right:58px;top:150px;width:@RW@px;z-index:2;filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))}
.meter{position:absolute;right:80px;top:516px;width:330px;padding:20px 24px 18px;border-radius:26px;z-index:3;color:#cfe0ff;
 background:linear-gradient(165deg,rgba(22,48,106,.92),rgba(12,30,67,.94) 52%,rgba(27,39,136,.94));border:1.5px solid rgba(255,255,255,.16);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 26px 50px -22px rgba(0,0,0,.7);transform:rotate(-2deg)}
.meter .t{font-size:19px;font-weight:700;color:#a9bdf0}
.meter .v{display:flex;align-items:baseline;gap:12px;margin:6px 0 12px}
.meter .v s{font-size:46px;font-weight:860;color:#ff94ae;text-decoration:none}
.meter .v i{font-style:normal;font-size:30px;color:#5fe3ff}
.meter .v b{font-size:62px;font-weight:880;color:#f2fffd;letter-spacing:-.04em;text-shadow:0 0 22px rgba(2,198,252,.95),0 0 4px rgba(2,198,252,.7)}
.bar{height:10px;border-radius:5px;background:rgba(255,255,255,.1);position:relative;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;border-radius:5px}
.bar .w{width:@BW@%;background:repeating-linear-gradient(135deg,rgba(255,148,174,.45) 0 5px,rgba(255,148,174,.18) 5px 10px)}
.bar .n{width:@AW@%;min-width:12px;background:#2fc2ff;box-shadow:0 0 12px rgba(8,168,250,.9)}
.meter .c{font-size:16.5px;color:#94abdc;margin-top:10px;font-weight:650}
.save{position:absolute;left:84px;top:634px;height:54px;padding:0 22px;border-radius:14px;border:2px solid rgba(251,191,36,.8);background:rgba(251,191,36,.1);color:#fcd34d;font-size:25px;font-weight:850;display:flex;align-items:center;z-index:2}
.fit{position:absolute;left:86px;top:646px;color:rgba(255,255,255,.86);font-size:26px;font-weight:650;z-index:2}
.panel{position:absolute;left:56px;right:56px;top:728px;height:416px;border-radius:40px;background:#fff;box-shadow:0 30px 60px -30px rgba(14,29,68,.45);z-index:3}
.ttl{position:absolute;left:52px;top:44px;font-size:50px;font-weight:860;letter-spacing:-.045em;color:#0e1d44;line-height:1.2}
.chips{position:absolute;left:52px;top:200px;display:flex;gap:12px}
.chip{height:50px;padding:0 18px 0 12px;border-radius:25px;background:#f3f6fc;border:1.5px solid #dde4f2;display:flex;align-items:center;gap:8px;font-size:23px;font-weight:750;color:#1c2540}
.dom{position:absolute;left:54px;bottom:44px;font-size:30px;font-weight:850;color:#1a63f2;letter-spacing:-.02em}
.dom small{font-size:21px;font-weight:650;color:#8592b3;margin-left:12px;letter-spacing:-.01em}
.price{position:absolute;right:52px;bottom:34px;text-align:right}
.price del{display:block;font-size:28px;font-weight:650;color:#8592b3;text-decoration-thickness:2px}
.price .row{display:flex;align-items:baseline;gap:16px;justify-content:flex-end}
.price .off{font-size:50px;font-weight:880;color:#ef3a6b;letter-spacing:-.03em}
.price b{font-size:78px;font-weight:880;letter-spacing:-.045em;color:#0e1d44}
"""


def thumb_html(p):
    small = len(p["tok"]) > 3
    css = (THUMB_CSS.replace("@BIGPX@", str(196 if small else 246)).replace("@RW@", str(330 if small else 360))
           .replace("@BW@", str(max(8, min(100, B_RATE)))).replace("@AW@", str(max(3, min(100, A_RATE)))))
    if p["badge"] == "BEST 추천":
        badge = '<div class="badge best">BEST 추천</div>'
    elif p["badge"]:
        badge = '<div class="badge top">%s</div>' % p["badge"]
    else:
        badge = '<div class="badge sale">정가의 50%</div>'
    low = ('<div class="save">%s</div>' % p["save"]) if p["save"] else ('<div class="fit">%s</div>' % p["fit"])
    chips = "".join('<div class="chip">%s%s</div>' % (CHECK, t) for t in ("월 구독 없음", "쓴 만큼만 차감", "5년 사용", "결제 30초"))
    body = """
<div class="hero">
 <div class="brand"><img src="%s" alt=""><div><b>Humani</b><small>한국어 AI 휴머나이저 · 휴머나이</small></div></div>%s
 <div class="kick">%s AI 휴머나이저 토큰</div>
 <div class="pills"><div class="pill n">%s</div><div class="pill o">%s</div></div>
 <div class="big"><b>%s</b><span>토큰</span></div>
 <img class="robot" src="%s" alt="">
 <div class="meter"><div class="t">변환 전 → 후 AI 작성률</div><div class="v"><s>%d%%</s><i>→</i><b>%d%%</b></div>
  <div class="bar"><i class="w"></i><i class="n"></i></div><div class="c">%s</div></div>
 %s
</div>
<div class="panel">
 <div class="ttl">AI 작성률은 낮추고,<br>원문의 의미는 그대로.</div>
 <div class="chips">%s</div>
 <div class="dom">humanai.io.kr<small>Humani(휴머나이)</small></div>
 <div class="price"><del>정가 %s</del><div class="row"><span class="off">50%%</span><b>%s</b></div></div>
</div>""" % (HEAD_URI, badge, SPARK, p["name"], p["per"], p["tok"], ROBOT_URI, B_RATE, A_RATE, DEMO_CAP, low, chips, p["list"], p["price"])
    return BASE % (css, body)


GUIDE_STEPS = [
    ("결제하면 메일로 토큰 코드가 옵니다", "결제가 확인되면 보통 1분 안에, 주문할 때 적은 이메일로 16자리 코드를 보내 드립니다. 보내는 이름은 'Humani'입니다. 받은편지함에 없으면 스팸함과 프로모션함을 확인해 주세요."),
    ("메일의 <em>바로 이어서 하기</em>를 누르면 끝", "코드가 들어간 채로 Humani가 열립니다. 충전하러 가기 전에 하던 글은 같은 기기에서 24시간 보관돼 그대로 이어집니다. 다른 기기에서는 '토큰 코드 넣기'에 코드를 넣으면 됩니다."),
    ("쓴 만큼만 빠집니다", "AI 작성률 요약은 0토큰, 문장별 전체 결과는 1,000자당 4토큰, 휴머나이징은 1,000자당 8토큰입니다. 남은 토큰은 위쪽 토큰 단추에서 언제든 확인합니다."),
    ("남은 토큰은 5년 동안 이어서", "같은 코드에 더 충전할 수 있고, 여러 기기에서 같은 코드를 씁니다. 코드를 아는 사람은 누구나 쓸 수 있으니 메일을 지우지 말고 잘 보관해 주세요."),
]


def guide_html():
    steps = "".join('<div class="st"><div class="n">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, h, t) for i, (h, t) in enumerate(GUIDE_STEPS))
    css = """
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#f3f6fc}
.top{position:absolute;left:0;top:0;width:1080px;height:430px;overflow:hidden;
 background:radial-gradient(420px 340px at 86% 40%,rgba(8,168,250,.42),transparent 66%),radial-gradient(120% 90% at 18% 0%,rgba(52,98,196,.55) 0%,transparent 55%),linear-gradient(165deg,#132b62 0%,#0c1e43 52%,#1b2788 100%)}
.top:before{content:"";position:absolute;inset:0;background-image:linear-gradient(to bottom,rgba(255,255,255,.045) 1px,transparent 1px);background-size:100% 40px}
.brand{position:absolute;left:76px;top:64px;display:flex;align-items:center;gap:14px}
.brand img{height:66px}
.brand b{display:block;font-size:44px;font-weight:860;letter-spacing:-.04em;color:#fff;line-height:1}
.brand small{display:block;font-size:18px;font-weight:650;color:#a9bdf0;margin-top:6px}
h1{position:absolute;left:76px;top:172px;font-size:80px;font-weight:880;letter-spacing:-.05em;color:#fff}
.lead{position:absolute;left:78px;top:282px;font-size:28px;color:#cfdcff;font-weight:650}
.robot{position:absolute;right:56px;top:40px;width:270px;filter:drop-shadow(0 24px 30px rgba(0,0,0,.35))}
.list{position:absolute;left:64px;top:352px;width:952px;display:flex;flex-direction:column;gap:16px}
.st{display:flex;gap:26px;background:#fff;border:1px solid #dde4f2;border-radius:28px;padding:24px 32px;box-shadow:0 14px 30px -20px rgba(14,29,68,.35)}
.n{flex:none;width:60px;height:60px;border-radius:50%;background:linear-gradient(180deg,#2a72ff,#1a63f2);color:#fff;font-size:29px;font-weight:850;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px -8px rgba(26,99,242,.8)}
h3{font-size:34px;font-weight:850;letter-spacing:-.035em;margin:6px 0 10px;color:#0e1d44}
h3 em{font-style:normal;color:#1a63f2}
p{font-size:23px;line-height:1.58;color:#3a4669;font-weight:550}
.ft{position:absolute;left:78px;right:78px;bottom:40px;border-top:1px solid #dde4f2;padding-top:22px;display:flex;justify-content:space-between;align-items:flex-end;color:#69759a;font-size:22px;line-height:1.6}
.ft b{color:#1a63f2;font-size:30px;font-weight:850}
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
