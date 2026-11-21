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
DEMO_CAP = "실측 예시 · %s 한 번 휴머나이징" % T.get("label", "논문")

PACKS = [
    {"id": "lt", "name": "라이트", "tok": "100", "price": "9,900원", "list": "19,800원", "per": "토큰당 99원", "save": "", "badge": "", "fit": "짧은 과제 · 자기소개서 한두 문항"},
    {"id": "pl", "name": "플러스", "tok": "300", "price": "19,900원", "list": "39,800원", "per": "토큰당 약 66원", "save": "", "badge": "", "fit": "레포트 여러 편 · 자소서 한 세트"},
    {"id": "pr", "name": "프로", "tok": "750", "price": "39,900원", "list": "79,800원", "per": "토큰당 약 53원", "save": "플러스보다 토큰당 20% 절약", "badge": "BEST 추천", "fit": "학기 과제 전체 · 논문 한 장(章)"},
    {"id": "mx", "name": "맥스", "tok": "1,500", "price": "69,900원", "list": "139,800원", "per": "토큰당 약 47원", "save": "플러스보다 토큰당 30% 절약", "badge": "최고 혜택", "fit": "학위논문 전체 · 팀 · 여러 명"},
]


def mark(size, uid):
    return ('<svg viewBox="0 0 40 40" width="%d" height="%d"><defs><linearGradient id="%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1730"/><stop offset="1" stop-color="#1b3266"/></linearGradient></defs>'
            '<rect width="40" height="40" rx="11" fill="url(#%s)"/><path d="M12.5 11v18M27.5 11v18" stroke="#fff" stroke-width="3.3" stroke-linecap="round"/><path d="M12.5 19.6q7.5 3.8 15 0" stroke="#fff" stroke-width="3.3" fill="none" stroke-linecap="round"/>'
            '<circle cx="31.6" cy="31.6" r="5.6" fill="#10b981" stroke="#0b1730" stroke-width="2"/><path d="m29.2 31.7 1.6 1.6 3.1-3.3" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>') % (size, size, uid, uid)


WAND = ('<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#6ee7b7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m15 4 5 5L9 20H4v-5z"/><path d="M13 6l5 5"/><path d="M19 2v3M17.5 3.5h3M5 3v2M4 4h2"/></svg>')
CHECK = ('<svg viewBox="0 0 24 24" width="26" height="26" fill="none"><circle cx="12" cy="12" r="11" fill="#e7f8f1"/>'
         '<path d="m7.5 12.3 3 3 6-6.3" stroke="#0e9f6e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

BASE = ("<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s'><style>"
        "*{box-sizing:border-box;margin:0;padding:0}html,body{font-family:'Pretendard Variable',Pretendard,sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.02em;color:#0b1220;word-break:keep-all}"
        "%%s</style></head><body>%%s</body></html>") % FONT

THUMB_CSS = """
body{width:1200px;height:1200px;position:relative;overflow:hidden;background:#eef2f8}
.hero{position:absolute;left:0;top:0;width:1200px;height:800px;overflow:hidden;
 background:radial-gradient(640px 440px at 96% 0%,rgba(124,58,237,.62),transparent 64%),
 radial-gradient(700px 520px at 0% 100%,rgba(16,185,129,.55),transparent 66%),
 linear-gradient(160deg,#08122b 0%,#0c1c3f 55%,#0a2b3e 100%)}
.hero:before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.09) 1.2px,transparent 1.5px);background-size:28px 28px}
.brand{position:absolute;left:84px;top:74px;display:flex;align-items:center;gap:18px;z-index:2}
.brand svg{filter:drop-shadow(0 6px 14px rgba(0,0,0,.35));border-radius:16px;outline:2px solid rgba(255,255,255,.14);outline-offset:-1px}
.brand b{display:block;font-size:50px;font-weight:860;letter-spacing:-.035em;color:#fff;line-height:1}
.brand small{display:block;font-size:15px;font-weight:700;letter-spacing:.28em;color:#94a3b8;margin-top:8px}
.badge{position:absolute;right:84px;top:86px;height:58px;padding:0 28px;border-radius:29px;display:flex;align-items:center;font-size:28px;font-weight:850;z-index:2;letter-spacing:-.02em}
.badge.best{background:linear-gradient(180deg,#fcd34d,#fbbf24);color:#1a1205;box-shadow:0 10px 24px -8px rgba(251,191,36,.7)}
.badge.top{background:#fff;color:#0b1730;box-shadow:0 10px 24px -10px rgba(255,255,255,.6)}
.badge.sale{background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.28);color:#fff}
.kick{position:absolute;left:86px;top:214px;display:flex;align-items:center;gap:12px;color:#e2e8f0;font-size:31px;font-weight:750;z-index:2}
.pills{position:absolute;left:84px;top:282px;display:flex;gap:14px;z-index:2}
.pill{height:58px;padding:0 26px;border-radius:29px;display:flex;align-items:center;font-size:29px;font-weight:850}
.pill.n{background:#10b981;color:#fff;box-shadow:0 10px 22px -10px rgba(16,185,129,.9)}
.pill.o{border:2px solid rgba(255,255,255,.34);color:#fff;font-weight:750}
.big{position:absolute;left:74px;top:352px;display:flex;align-items:flex-end;color:#fff;z-index:2}
.big b{font-size:@BIGPX@px;font-weight:880;letter-spacing:-.065em;line-height:.9;text-shadow:0 18px 40px rgba(0,0,0,.35)}
.big span{font-size:66px;font-weight:850;margin:0 0 18px 18px}
.meter{position:absolute;right:84px;top:300px;width:356px;padding:26px 28px 24px;border-radius:28px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.2);color:#fff;z-index:2;backdrop-filter:blur(6px);box-shadow:0 24px 50px -24px rgba(0,0,0,.6)}
.meter .t{font-size:20px;font-weight:750;color:rgba(255,255,255,.78)}
.meter .v{display:flex;align-items:baseline;gap:12px;margin:8px 0 16px}
.meter .v s{font-size:46px;font-weight:860;color:#c4b5fd;text-decoration-thickness:4px;text-decoration-color:rgba(251,113,133,.9)}
.meter .v i{font-style:normal;font-size:30px;color:rgba(255,255,255,.6)}
.meter .v b{font-size:64px;font-weight:880;color:#34d399;letter-spacing:-.04em}
.bar{height:12px;border-radius:6px;background:rgba(255,255,255,.13);margin:8px 0;position:relative;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;border-radius:6px}
.bar.a i{width:@BW@%;background:linear-gradient(90deg,#7c3aed,#a78bfa)}
.bar.b i{width:@AW@%;min-width:12px;background:linear-gradient(90deg,#10b981,#34d399)}
.meter .c{font-size:16.5px;color:rgba(255,255,255,.62);margin-top:12px;font-weight:650}
.save{position:absolute;left:86px;top:640px;height:54px;padding:0 22px;border-radius:14px;border:2px solid rgba(251,191,36,.8);background:rgba(251,191,36,.1);color:#fcd34d;font-size:25px;font-weight:850;display:flex;align-items:center;z-index:2}
.fit{position:absolute;left:88px;top:652px;color:rgba(255,255,255,.86);font-size:26px;font-weight:650;z-index:2}
.panel{position:absolute;left:56px;right:56px;top:724px;height:420px;border-radius:40px;background:#fff;box-shadow:0 30px 60px -30px rgba(11,23,48,.45),0 2px 0 rgba(255,255,255,.8) inset;z-index:3}
.ttl{position:absolute;left:52px;top:46px;font-size:48px;font-weight:880;letter-spacing:-.04em;color:#0b1730;line-height:1.2}
.ttl2{position:absolute;left:54px;top:112px;font-size:30px;font-weight:700;color:#475569}
.chips{position:absolute;left:52px;top:190px;display:flex;gap:12px}
.chip{height:50px;padding:0 18px 0 12px;border-radius:25px;background:#f6f8fb;border:1.5px solid #e2e8f0;display:flex;align-items:center;gap:8px;font-size:23px;font-weight:750;color:#1e293b}
.dom{position:absolute;left:54px;bottom:44px;font-size:30px;font-weight:850;color:#0e9f6e;letter-spacing:-.02em}
.dom small{font-size:21px;font-weight:650;color:#94a3b8;margin-left:12px;letter-spacing:-.01em}
.price{position:absolute;right:52px;bottom:34px;text-align:right}
.price del{display:block;font-size:28px;font-weight:650;color:#94a3b8;text-decoration-thickness:2px;margin-bottom:0}
.price .row{display:flex;align-items:baseline;gap:16px;justify-content:flex-end}
.price .off{font-size:50px;font-weight:880;color:#f43f5e;letter-spacing:-.03em}
.price b{font-size:78px;font-weight:880;letter-spacing:-.045em;color:#0b1730}
"""


def thumb_html(p):
    small = len(p["tok"]) > 3
    css = THUMB_CSS.replace("@BIGPX@", str(210 if small else 252)).replace("@BW@", str(max(8, min(100, B_RATE)))).replace("@AW@", str(max(3, min(100, A_RATE))))
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
 <div class="brand">%s<div><b>Humani</b><small>AI HUMANIZER</small></div></div>%s
 <div class="kick">%s AI 휴머나이징 토큰</div>
 <div class="pills"><div class="pill n">%s</div><div class="pill o">%s</div></div>
 <div class="big"><b>%s</b><span>토큰</span></div>
 <div class="meter"><div class="t">휴머나이징 전 → 후 AI 작성률</div><div class="v"><s>%d%%</s><i>→</i><b>%d%%</b></div>
  <div class="bar a"><i></i></div><div class="bar b"><i></i></div><div class="c">%s</div></div>
 %s
</div>
<div class="panel">
 <div class="ttl">카피킬러 AI 작성률 낮추기</div>
 <div class="ttl2">AI 휴머나이징 · AI 글 인간화 토큰</div>
 <div class="chips">%s</div>
 <div class="dom">humanai.io.kr<small>Humani(휴머나이)</small></div>
 <div class="price"><del>정가 %s</del><div class="row"><span class="off">50%%</span><b>%s</b></div></div>
</div>""" % (mark(76, "a"), badge, WAND, p["name"], p["per"], p["tok"], B_RATE, A_RATE, DEMO_CAP, low, chips, p["list"], p["price"])
    return BASE % (css, body)


GUIDE_STEPS = [
    ("결제하면 메일로 토큰 코드가 옵니다", "결제 확인 뒤 보통 5분 안에, 주문할 때 적은 이메일로 16자리 코드를 보내 드립니다. 보내는 이름은 'Humani'입니다. 받은편지함에 없으면 스팸함과 프로모션함을 확인해 주세요."),
    ("메일의 <em>바로 이어서 하기</em>를 누르면 끝", "코드가 들어간 채로 Humani가 열립니다. 충전하러 가기 전에 하던 글은 같은 기기에서 24시간 보관돼 그대로 이어집니다. 다른 기기에서는 '토큰 코드 넣기'에 코드를 넣으면 됩니다."),
    ("쓴 만큼만 빠집니다", "AI 작성률 요약은 0토큰, 문장별 전체 결과는 1,000자당 4토큰, 휴머나이징은 1,000자당 8토큰입니다. 남은 토큰은 위쪽 토큰 단추에서 언제든 확인합니다."),
    ("남은 토큰은 5년 동안 이어서", "같은 코드에 더 충전할 수 있고, 여러 기기에서 같은 코드를 씁니다. 코드를 아는 사람은 누구나 쓸 수 있으니 메일을 지우지 말고 잘 보관해 주세요."),
]


def guide_html():
    steps = "".join('<div class="st"><div class="n">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, h, t) for i, (h, t) in enumerate(GUIDE_STEPS))
    css = """
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#f4f6fb}
.top{position:absolute;left:0;top:0;width:1080px;height:420px;overflow:hidden;
 background:radial-gradient(560px 380px at 100% 0%,rgba(124,58,237,.55),transparent 64%),radial-gradient(620px 420px at 0% 100%,rgba(16,185,129,.5),transparent 66%),linear-gradient(160deg,#08122b,#0c1c3f 60%,#0a2b3e)}
.top:before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.09) 1.2px,transparent 1.5px);background-size:26px 26px}
.brand{position:absolute;left:80px;top:70px;display:flex;align-items:center;gap:16px}
.brand b{display:block;font-size:44px;font-weight:860;letter-spacing:-.035em;color:#fff;line-height:1}
.brand small{display:block;font-size:14px;font-weight:700;letter-spacing:.28em;color:#94a3b8;margin-top:8px}
h1{position:absolute;left:80px;top:178px;font-size:82px;font-weight:880;letter-spacing:-.05em;color:#fff}
.lead{position:absolute;left:82px;top:290px;font-size:29px;color:#cbd5e1;font-weight:650}
.list{position:absolute;left:64px;top:368px;width:952px;display:flex;flex-direction:column;gap:18px}
.st{display:flex;gap:26px;background:#fff;border:1px solid #e6ebf2;border-radius:28px;padding:28px 34px;box-shadow:0 14px 30px -20px rgba(11,23,48,.35)}
.n{flex:none;width:60px;height:60px;border-radius:50%;background:linear-gradient(180deg,#10b981,#0e9f6e);color:#fff;font-size:29px;font-weight:850;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px -8px rgba(14,159,110,.8)}
h3{font-size:34px;font-weight:850;letter-spacing:-.035em;margin:6px 0 10px;color:#0b1730}
h3 em{font-style:normal;color:#0e9f6e}
p{font-size:23.5px;line-height:1.62;color:#475569;font-weight:550}
.ft{position:absolute;left:80px;right:80px;bottom:52px;border-top:1px solid #e2e8f0;padding-top:22px;display:flex;justify-content:space-between;align-items:flex-end;color:#64748b;font-size:22px;line-height:1.6}
.ft b{color:#0e9f6e;font-size:30px;font-weight:850}
"""
    body = """<div class="top"><div class="brand">%s<div><b>Humani</b><small>AI HUMANIZER</small></div></div>
<h1>토큰 이용 안내</h1><div class="lead">월 구독 없이 한 번 충전하고, 쓴 만큼만 빠집니다</div></div>
<div class="list">%s</div>
<div class="ft"><div>문의 contact@skkc.co.kr<br>판매 성균관컨설팅 · 서비스 Humani(휴머나이)</div><b>humanai.io.kr</b></div>""" % (mark(66, "g"), steps)
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
