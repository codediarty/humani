# -*- coding: utf-8 -*-
"""Humani(휴머나이) 홈 · 공통 구역 글. build.py 가 읽음. 줄표(—)는 쓰지 않음.
{EX_...} 자리는 build.py 가 demo.json(실제 엔진 측정값)으로 바꿔 넣음"""

# ---------------- 검사 도구 화면(humanize.js 가 쓰는 id 그대로, AIMarker 도구와 같은 짜임) ----------------
TOOL_TPL = """<div class="hz12" id="hz">
  <ol class="hz12-steps" id="hzSteps" aria-label="진행 순서">
    <li class="on" data-step="1"><i>1</i><span>글 넣기</span></li>
    <li data-step="2"><i>2</i><span class="f">AI 작성률 확인</span><span class="s">검사</span></li>
    <li data-step="3"><i>3</i><span class="f">휴머나이징</span><span class="s">다듬기</span></li>
  </ol>
  <div class="hz12-card">
    <div class="hz12-in" id="hzIn">
      <div class="hz12-drop" id="hzDrop">
        <label class="k-sr" for="hzText">검사할 글</label>
        <textarea id="hzText" maxlength="200000" spellcheck="false" placeholder="AI로 쓴 글이나 과제 · 논문 · 자기소개서를 붙여 넣으세요"></textarea>
        <div class="hz12-empty" id="hzEmpty">
          <button type="button" class="hz12-up" id="hzPick">{ico_upload}<span>파일 올리기</span></button>
          <p class="dnd">또는 파일을 여기로 끌어다 놓으세요</p>
          <p class="fmt">한글(HWP, HWPX), 워드(DOCX), PDF, 텍스트</p>
        </div>
        <div class="hz12-over" aria-hidden="true">{ico_upload}<span>놓으면 글을 꺼내 옵니다</span></div>
        <div class="hz12-busy" id="hzBusy" hidden><span class="ds-spin" aria-hidden="true"></span><span id="hzBusyT">파일에서 글을 꺼내는 중</span></div>
      </div>
      <input type="file" id="hzFile" class="k-sr" tabindex="-1" aria-hidden="true" aria-label="파일 올리기" accept=".hwp,.hwpx,.docx,.pdf,.txt,.md,text/plain,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document">
      <div class="hz12-bar">
        <div class="hz12-file" id="hzFileChip" hidden></div>
        <div class="hz12-ex" id="hzEx" role="group" aria-label="예시 글로 해 보기"><span>예시</span><button type="button" data-ex="thesis">논문</button><button type="button" data-ex="journal">학술지</button><button type="button" data-ex="report">대학 과제</button><button type="button" data-ex="grad">대학원 과제</button><button type="button" data-ex="essay">자기소개서</button></div>
        <span class="hz12-cnt"><b id="hzCount">0</b>자<span class="lim" id="hzLimit"> / 무료 검사 20만 자까지</span></span>
      </div>
    </div>
    <div class="hz12-sum" id="hzSum" hidden></div>
    <div class="hz12-go" id="hzGo">
      <button class="k-btn k-btn-p k-btn-lg hz12-run" type="button" id="hzCheck">{ico_search}<span id="hzChkL">AI 작성률 무료 검사</span><em class="hz7-pill" id="hzChkTag" hidden></em></button>
      <button class="k-btn k-btn-l k-btn-lg hz12-run2" type="button" id="hzPro" hidden>{ico_pen}<span>휴머나이징<small>AI 작성률 낮추기</small></span><em class="hz7-pill" id="hzProTag"></em></button>
      <p class="hz12-note" id="hzNote">{ico_lock}<span>가입 없이 무료 · 글과 파일은 저장하지 않습니다</span></p>
      <div class="hz7-pass hz12-pass" id="hzPass" aria-live="polite"></div>
    </div>
  </div>
  <p class="k-sr" id="hzStat" role="status" aria-live="polite"></p>
  <div class="hz12-out" id="hzOut"></div>
</div>
<dialog class="hz7-dlg hz18-dlg" id="hzBuy" aria-labelledby="hzBuyT">
  <form method="dialog" class="hz7-dlg-x"><button type="submit" aria-label="닫기">{ico_x}</button></form>
  <div class="hz7-dlg-b" id="hzBuyBody">
    <p class="hz18-k">{ico_spark}Humani 토큰 충전 · 많이 충전할수록 저렴</p>
    <h2 id="hzBuyT">AI 휴머나이징 토큰 충전</h2>
    <p class="hz13-unit"><b>월 구독 없이 한 번 충전</b><span>내 문서 AI 작성률 낮추기. 반복할수록 AI 작성률은 더 낮아집니다.</span></p><style>@media (max-width:540px){{body .hz7-dlg .hz18-packs .pr s+small{{display:none}}}}</style>
    <p class="hz12-need" id="hzBuyNeed" hidden></p>
    <form id="hzBuyForm" novalidate>
      <fieldset class="hz7-to" hidden></fieldset>
      <fieldset class="hz7-prod hz18-packs"><legend class="sr">충전할 토큰</legend>{packs}<p class="hz20-pg">글자 수는 AI 작성률 검사와 휴머나이징을 한 번씩 했을 때 기준입니다</p></fieldset>
      <div class="hz19-gate" id="hzBuyPay"></div>
      <div class="hz19-fb" id="hzBuyFb" hidden>
        <div class="field"><label for="hzBuyMail">토큰 코드와 결제 안내를 받을 이메일 <em>필수</em></label><input class="inp" id="hzBuyMail" name="contact" type="email" inputmode="email" autocomplete="email" maxlength="80" placeholder="name@example.com"></div>
        <p class="hz7-dlg-n" id="hzBuyNote"></p>
        <p class="hz7-dlg-n">이메일은 주문 처리와 코드 · 결제 안내에만 씁니다(<a href="/privacy/" target="_blank" rel="noopener">개인정보처리방침</a>).</p>
      </div>
      <input class="hp" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-p btn-l hz19-go" type="submit"><span>성균관컨설팅에서 30초 결제</span>{ico_arrow}</button>
      <p class="msg" role="status"></p>
      <p class="hz7-dlg-n hz19-legal"><span id="hzBuyAmt"></span>운영 성균관컨설팅(사업자등록번호 {biz_no}) · <a href="/terms/#pass" target="_blank" rel="noopener">이용약관</a> · 문의 {mail}</p>
    </form>
  </div>
</dialog>
<dialog class="hz7-dlg" id="hzCode" aria-labelledby="hzCodeT">
  <form method="dialog" class="hz7-dlg-x"><button type="submit" aria-label="닫기">{ico_x}</button></form>
  <div class="hz7-dlg-b">
    <h2 id="hzCodeT">토큰 코드 넣기</h2>
    <form id="hzCodeForm" novalidate>
      <div class="field"><label for="hzCodeIn">메일로 받은 16자리 코드</label><input class="inp hz7-code-in" id="hzCodeIn" name="code" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="24" placeholder="XXXX-XXXX-XXXX-XXXX"></div>
      <button class="btn btn-p btn-l" type="submit">코드 넣기</button>
      <p class="msg" role="status"></p>
      <p class="hz7-dlg-n">코드는 이 브라우저에만 저장됩니다. 다른 기기에서는 코드를 한 번 더 넣어 주세요.<span class="twa-hide"> 코드가 없나요? <button type="button" class="hz7-link" data-buy="best">토큰 충전</button></span></p>
    </form>
  </div>
</dialog>"""

# ---------------- 홈 ----------------
# 메인화면에는 특정 검사기 이름(상표)을 적지 않습니다(2026.11.21 대표 지시). 'AI 탐지기'처럼 일반 표현으로.
HOME = {
    "title": "AI 휴머나이저 · AI 작성률 낮추기 · AI 휴머나이징 | Humani(휴머나이)",
    "desc": "AI 작성률은 낮추고 원문의 의미는 그대로. Humani(휴머나이)는 AI 탐지기가 감지하는 문장 패턴을 분석해 AI 작성 흔적이 있는 문장만 사람 문장으로 바꾸는 한국어 AI 휴머나이저입니다. 20만 자 무료 검사.",
    "eyebrow": "<b>무료</b> 한국어 AI 휴머나이저 · 가입 없이 20만 자 검사",
    "h1": "AI 작성률은 낮추고,<br>원문의 의미는 그대로.",
    "lead": "AI&nbsp;탐지기가 감지하는 문장 패턴을 정밀 분석합니다. AI&nbsp;작성&nbsp;흔적이 발견된 문장을 집중적으로 변환하고, 원문의&nbsp;의미와 핵심&nbsp;내용은 유지합니다. 변환&nbsp;전후 AI&nbsp;작성률까지 직접 비교해 보세요.",
    "pts": ["회원가입 없이 바로", "한글 · 워드 · PDF 그대로", "넣은 글은 저장하지 않음"],
    "faq": [
        ("AI 휴머나이저는 어떤 서비스인가요?", "AI가 쓴 글에서 탐지기가 잡아내는 말버릇(번역투, 판에 박힌 연결어, 내용 없는 꾸밈말, 일정한 문장 리듬)을 찾아 사람이 쓴 문장으로 바꾸는 서비스입니다. Humani(휴머나이)는 한국어만 다루는 엔진으로 바꾸고, 바꾼 뒤 AI 작성률을 같은 기준으로 다시 재서 결과를 숫자로 보여 드립니다."),
        ("AI 탐지기의 AI 작성률을 정말 낮출 수 있나요?", "AI 탐지기는 문장마다 AI가 쓴 글과 닮은 정도를 보고, 기준을 넘는 문장을 AI 작성으로 표시합니다. 휴머나이는 실제 검사 결과와 문장 단위로 대조해 맞춘 엄격한 기준으로 걸릴 만한 문장을 먼저 찾고, 그 문장을 집중적으로 고친 뒤 다시 잽니다. 예시 레포트는 AI 작성률 {EX_R_B}%에서 한 번의 휴머나이징으로 {EX_R_A}%가 됐습니다(Humani 판정 기준). 탐지기마다 모델이 달라 같은 숫자를 약속하지는 않습니다."),
        ("어디까지 무료인가요?", "AI 작성률 검사는 가입 없이 무료이고 한 번에 20만 자까지 됩니다. 전체 AI 작성률, 판정(안전 · 고위험 · 부적합), 가장 뚜렷한 AI 문장 2개를 바로 보여 드립니다. 휴머나이징은 앞부분을 무료로 먼저 보고, 글 전체는 토큰으로 이용합니다."),
        ("휴머나이징하면 내용이 바뀌지 않나요?", "뜻이 바뀌지 않게 만든 엔진입니다. 숫자, 이름, 인용, 전문 용어는 건드리지 않고 문장의 짜임과 말투만 바꿉니다. 출시 기준 시험(583만 자)에서 사실 · 부정 표현 보존 100%를 확인했습니다. 그래도 제출하기 전에 한 번 읽어 보시길 권합니다."),
        ("한글 · 워드 파일을 그대로 올려도 되나요?", "네. 한글(HWP · HWPX), 워드(DOCX), PDF, 텍스트 파일을 올리면 글을 꺼내 바로 검사합니다. 다듬은 글은 올린 형식 그대로 받을 수 있고, 한글 · 워드 파일은 바뀐 문단만 고쳐 원래 서식을 지킵니다."),
        ("제가 넣은 글은 저장되나요?", "저장하지 않습니다. 넣은 글과 파일은 검사와 휴머나이징에만 쓰고 서버에 남기지 않습니다. 파일에서 글을 꺼내는 일도 이용자의 브라우저 안에서 하고, 회원가입도 없습니다."),
        ("결제는 어떻게 하고, 코드는 언제 오나요?", "토큰을 고르면 운영사 성균관컨설팅의 결제 페이지가 열립니다. 이메일만 적고 카드 · 토스페이 · 계좌이체로 결제하면 보통 1분 안에 16자리 토큰 코드가 메일로 오고, 메일의 단추를 누르면 하던 글 그대로 이어서 휴머나이징됩니다."),
        ("여러 AI 탐지기에 함께 대비할 수 있나요?", "AI 탐지기들은 대체로 비슷한 신호를 봅니다. 번역투, 판에 박힌 연결어, 내용 없는 꾸밈말, 일정한 문장 리듬 같은 것들입니다. 휴머나이는 특정 탐지기 하나에 맞춘 꼼수가 아니라 이런 AI 문장 패턴 자체를 고치므로 여러 탐지기에 함께 대비할 수 있습니다."),
    ],
}
HOW_STEPS = [
    ("글 넣기", "글을 붙여 넣거나 한글 · 워드 · PDF 파일을 올립니다. 파일 속 글은 브라우저 안에서 꺼내고, 어디에도 저장하지 않습니다."),
    ("AI 작성률 확인", "문장마다 앞뒤 문맥과 함께 판별해 AI 작성률, 판정(안전 · 고위험 · 부적합), AI로 검출된 문장을 보여 드립니다. 여기까지 무료입니다."),
    ("휴머나이징", "검출된 문장 위주로 번역투 · 판에 박힌 연결어 · 빈말을 사람 문장으로 바꾸고, 같은 기준으로 다시 재서 내려간 AI 작성률을 보여 드립니다."),
]


def sh(h, sub="", cls=""):
    """구역 머리: 제목은 왼쪽, 설명은 오른쪽(좁은 화면에서는 아래로)"""
    return '<div class="hsh%s"><h2 class="h2">%s</h2>%s</div>' % ((" " + cls) if cls else "", h, ('<p class="sub">%s</p>' % sub) if sub else "")


def trust_strip(ico):
    items = [("89억 개", "AI 문장 패턴 데이터로 만든 판별 엔진"), ("15,659개", "사람 글 10억 자로 만든 한국어 용언 사전"),
             ("100%", "숫자 · 사실 보존율(583만 자 시험)"), ("1분 안", "결제하면 메일로 16자리 토큰 코드")]
    return ('<section class="trust" aria-label="엔진 수치"><div class="wrap"><dl class="trust-g">%s</dl></div></section>' %
            "".join('<div class="tr"><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in items))


SEARCH_CHIPS = [("ai-humanizer/", "AI 휴머나이저"), ("humanizing/", "AI 휴머나이징"), ("lower-ai-rate/", "AI 작성률 낮추기"), ("ai-check/", "AI 작성률 검사"),
                ("ai-bypass/", "AI 탐지 우회"), ("lower-ai-rate/", "AI 표절률 낮추기"), ("natural/", "AI 티 안 나게"), ("free/", "AI 휴머나이저 무료"),
                ("ai-converter/", "AI 문장 변환"), ("guide/ai-patterns/", "AI 패턴 제거"), ("thesis/", "논문 AI 작성률 낮추기"), ("resume/", "자기소개서 AI 작성률 낮추기"),
                ("report/", "레포트 AI 탐지"), ("guide/chatgpt-tone/", "챗GPT 티 안 나게"), ("best-ai-humanizer/", "AI 휴머나이징 사이트"), ("results/", "휴머나이징 실제 측정 결과")]


def search_chips(ico):
    return ('<section class="chips-s" aria-label="많이 찾는 주제"><div class="wrap"><p class="chips-h">많이 찾는 주제</p><div class="chips">%s</div></div></section>' %
            "".join('<a href="/%s">%s</a>' % (u, t) for u, t in SEARCH_CHIPS))


def alarm_section(ico):
    stats = [("D-<small>학점</small>", "과제에 AI를 쓰고 신고하지 않았다가 확인된 학생이 받은 과목 성적입니다. 서울대 한 전공과목에서는 62명 가운데 36명이 0점이나 D-를 받았습니다.", "세계일보 2026.7.30"),
             ("64.4<small>%</small>", "AI 작성이 의심된 자기소개서 비율입니다. 한 채용 서비스에 들어온 서류 기준이며, 1년 전에는 48.5%였습니다.", "전자신문 2026.1.9"),
             ("+75.9<small>%</small>", "교수자가 과제를 AI 검사한 문서량의 1년 새 증가율입니다. 한 달 동안 57만 7천 건을 검사했습니다.", "유니콘팩토리 2026.5.26")]
    pats = [("번역투", '학생들의 진로 선택<span class="s ai">에 있어서</span> 부모의 영향은 큰 비중을 <span class="s ai">차지하고 있다</span>', "~에 있어서, ~을 통해, ~함으로써"),
            ("판에 박힌 연결어", '<span class="s ai">또한,</span> 꾸준한 운동은 스트레스 해소에도 도움이 된다. <span class="s ai">따라서</span>', "또한, 따라서, 결론적으로"),
            ("내용 없는 꾸밈말", '<span class="s ai">다양한</span> 경험을 바탕으로 <span class="s ai">효과적인</span> 해결 방안을 제시했다', "다양한, 효과적인, 체계적인"),
            ("틀에 박힌 시작과 끝", '<span class="s ai">오늘날</span> 환경 문제는 모두가 함께 풀어야 할 과제<span class="s ai">라고 할 수 있다</span>', "현대 사회에서, ~라고 할 수 있다")]
    return ('<section class="sec dark" id="why"><div class="wrap">%s'
            '<div class="wst">%s</div>'
            '<div class="pats-w"><div class="pats-hd"><h3 class="pats-h">내 글에도 있을까요? AI 탐지기가 보는 말버릇 네 가지</h3>'
            '<p class="pats-p">보라색 부분이 AI 작성률을 올립니다. 글을 넣으면 어느 문장에 남아 있는지 바로 보여 드립니다.</p></div>'
            '<div class="pats">%s</div></div>'
            '<div class="why-ft"><a class="btn btn-p btn-l" href="#tool" data-tool>%s내 글 무료로 검사하기</a>'
            '<p class="src">출처: 세계일보 2026.7.30 · 전자신문 2026.1.9(채용 서비스 공동 리포트, 2025년 제출 자기소개서) · 유니콘팩토리 2026.5.26(국내 한 교수자 평가용 서비스의 2026년 4월 검사 문서량)</p></div></div></section>') % (
        sh("학교와 기업은 이미<br>AI 탐지기로 글을 거릅니다", "부적합 판정을 받고 나면 해명할 기회가 없을 수도 있습니다. 내기 전에 확인하고, 걸리는 문장만 고치세요."),
        "".join('<div class="wst-i"><b>%s</b><p>%s</p><cite>%s</cite></div>' % s for s in stats),
        "".join('<div class="pat"><b>%s</b><p>%s</p><span>%s</span></div>' % (a, b, c) for a, b, c in pats), ico("search"))


def how_section(ico):
    steps = "".join('<li class="howi"><h3>%s</h3><p>%s</p></li>' % s for s in HOW_STEPS)
    return ('<section class="sec alt" id="how"><div class="wrap">%s'
            '<ol class="howl">%s</ol><div class="payflow" aria-label="결제 흐름"><span>토큰 고르기</span><i aria-hidden="true"></i><span>이메일만 적고 결제</span><i aria-hidden="true"></i><span>메일로 16자리 코드(보통 1분 안)</span><i aria-hidden="true"></i><span class="k">하던 글 그대로 이어서</span></div></div></section>') % (
        sh("가입도 설치도 없이,<br>세 단계면 끝납니다", "검사는 무료로 바로 하고, 결제는 필요할 때만 성균관컨설팅 결제 페이지에서 이메일 하나로 합니다."), steps)


def features_section(ico):
    F = [("cpu", "한국어만 파고든 엔진", "사람 글 10억 자로 만든 용언 사전 15,659개로 어미와 조사까지 자연스럽게 바꿉니다. 번역기를 두 번 돌린 듯한 어색함이 남지 않습니다."),
         ("target", "흔적이 있는 문장을 집중적으로", "문장마다 AI 점수를 먼저 매기고 기준을 넘는 문장 위주로 고칩니다. 멀쩡한 문장을 건드려 새로 걸리는 일을 막습니다."),
         ("shield", "의미 · 숫자 · 인용 보존", "숫자, 이름, 인용, 전문 용어는 손대지 않습니다. 출시 기준 시험 583만 자에서 사실 · 부정 표현 보존 100%, 깨진 문장 0.00%였습니다."),
         ("sliders", "말투 자동 맞춤", "논문 · 레포트는 한다체, 자기소개서 · 안내문은 습니다체처럼 원문 말투를 읽어 그대로 맞춥니다. 섞여 있던 말투도 하나로 정리합니다."),
         ("file", "파일 그대로 받기", "한글 · 워드 파일은 바뀐 문단만 고쳐 원래 서식을 지키고, PDF는 새로 조판해 드립니다. 복사해서 붙여 넣는 수고가 없습니다."),
         ("bars", "같은 기준으로 다시 측정", "변환 전과 후의 AI 작성률을 같은 기준으로 잽니다. 같은 글은 다시 검사해도 같은 값이라 전후를 정확히 비교할 수 있습니다.")]
    items = "".join('<div class="ft-i"><span class="ic">%s</span><h3>%s</h3><p>%s</p></div>' % (ico(i), a, b) for i, a, b in F)
    return '<section class="sec" id="features"><div class="wrap">%s<div class="feats">%s</div></div></section>' % (
        sh("의미는 지키고,<br>AI 흔적만 고칩니다", "번역기를 두 번 돌리거나 혼자 고치는 것과는 결과가 다릅니다. 휴머나이는 한국어 문장을 이렇게 다룹니다."), items)


def compare_table(ico):
    rows = [("한국어 문장 자연스러움", "사람마다 다름", "어색해짐", "번역투가 남음", "한국어 전용 규칙"),
            ("AI로 걸리는 문장 표시", '<span class="no">없음</span>', '<span class="no">없음</span>', "일부", '<span class="yes">문장마다</span>'),
            ("숫자 · 이름 · 인용 보존", '<span class="yes">보존</span>', "자주 틀림", "자주 틀림", '<span class="yes">100% 보존</span>'),
            ("바꾼 뒤 AI 작성률 다시 측정", '<span class="no">못 함</span>', '<span class="no">못 함</span>', "영어 기준", '<span class="yes">같은 기준으로</span>'),
            ("한글(HWP) 파일", "-", '<span class="no">안 됨</span>', '<span class="no">안 됨</span>', '<span class="yes">서식 그대로</span>'),
            ("월 구독", "-", "-", "대부분 월 결제", '<span class="yes">없음, 쓴 만큼만</span>'),
            ("걸리는 시간", "몇 시간", "몇 분", "몇 분", '<span class="yes">몇 초</span>')]
    body = "".join("<tr><td>%s</td><td class=\"me\">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0], r[4], r[1], r[2], r[3]) for r in rows)   # 휴머나이 칸을 기준 바로 옆에(모바일에서 가로로 밀지 않아도 보이게)
    return ('<section class="sec alt" id="compare"><div class="wrap">%s'
            '<div class="tbl-w"><table class="tbl"><thead><tr><th>기준</th><th class="me">휴머나이</th><th>직접 고치기</th><th>번역기 두 번 돌리기</th><th>해외 휴머나이저</th></tr></thead><tbody>%s</tbody></table></div></div></section>') % (
        sh("AI 티를 지우는 방법,<br>결과가 이렇게 다릅니다", "직접 고치면 몇 시간이 걸리고, 번역기를 돌리면 번역투가 남습니다. 해외 휴머나이저는 한국어 어미와 조사를 다루지 못합니다."), body)


def usecases_section(ico):
    U = [("cap", "논문 · 학위논문", "심사 · 투고 전 AI 작성률 점검. 본 연구, 선행연구 같은 학술 표현은 지키고 AI 말버릇만 고칩니다.", "/thesis/", "논문 AI 작성률 낮추기"),
         ("file", "과제 · 레포트", "교수님이 AI 검사로 거르는 과제, 내기 전에 낮추세요. 레포트 한 편이 몇 초면 끝납니다.", "/report/", "레포트 AI 탐지 대비"),
         ("brief", "자기소개서", "채용 서류의 AI 작성 의심 비율은 64%가 넘습니다. 습니다체 그대로, 내 경험이 살아 있는 문장으로.", "/resume/", "자기소개서 AI 작성률 낮추기"),
         ("chat", "블로그 · 마케팅 글", "AI 티가 나는 글은 독자도 먼저 알아봅니다. 사람이 쓴 듯 자연스러운 문장으로 다듬으세요.", "/natural/", "AI 티 안 나게 쓰기")]
    cards = "".join('<a class="uc" href="%s"><span class="ic">%s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></a>' % (u, ico(i), a, b, m) for i, a, b, u, m in U)
    return '<section class="sec" id="uses"><div class="wrap">%s<div class="ucs">%s</div></div></section>' % (
        sh("제출하는 한국어 글이라면<br>무엇이든", "글의 종류에 맞춰 말투와 표현을 지킵니다. 용도별로 자주 묻는 내용을 따로 정리했습니다."), cards)


def pay_section(ico):
    """결제가 쉬운 것을 보여 주는 띠(이탈을 줄이려고 요금 카드 바로 아래)"""
    S = [("tag", "토큰 고르기", "필요한 만큼 고릅니다. 프로 · 맥스는 플러스보다 토큰당 약 30% · 40% 절약됩니다."),
         ("mail", "이메일 하나로 결제", "성균관컨설팅 결제 페이지에서 회원가입 없이 이메일만 적고 카드 · 토스페이 · 계좌이체로 결제합니다."),
         ("send", "1분 안에 코드 도착", "보내는 사람 'Humani' 메일로 16자리 코드가 갑니다. 메일의 단추를 누르면 코드가 들어간 채로 열립니다."),
         ("refresh", "하던 글 그대로", "결제하러 간 동안 글은 이 브라우저에 24시간 보관됩니다. 돌아오면 바로 이어서 휴머나이징합니다.")]
    return ('<div class="pay rv"><div class="pay-h"><b>%s결제는 30초면 끝납니다</b><span>가입 없음 · 이메일만 적으면 됨 · 영수증과 카드 명세서는 성균관컨설팅</span></div><ol class="pay-s">%s</ol></div>' %
            (ico("lock"), "".join('<li><span class="pi">%s</span><b>%s</b><p>%s</p></li>' % (ico(i), a, b) for i, a, b in S)))


def pricing_detail(ico):
    rows = [("자기소개서 1문항(1,500자)", "무료", "6토큰", "6토큰 · 약 600원"), ("대학 레포트(5,000자)", "무료", "20토큰", "20토큰 · 약 2,000원"),
            ("논문 한 장(15,000자)", "무료", "60토큰", "60토큰 · 약 6,000원"), ("학위논문 본문(80,000자)", "무료", "320토큰", "320토큰 · 약 32,000원")]
    t = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in rows)
    return ('<section class="sec-s"><div class="wrap-n"><h2 class="h2">토큰은 이렇게 빠집니다</h2><p class="sub">AI 작성률 검사는 무료, AI 휴머나이징 1,000자 4토큰(최소 2토큰). 1토큰은 100원으로 셈하고, 빠질 토큰은 누르기 전에 화면에 먼저 보여 드립니다.</p>'
            '<div class="tbl-w"><table class="tbl"><thead><tr><th>글</th><th>검사</th><th>휴머나이징</th><th>합계(1토큰 100원 기준)</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="tnote">충전 상품으로 사면 토큰당 35~99원이라 위 금액보다 훨씬 적게 듭니다. 예를 들어 프로 1,000토큰(39,900원)이면 학위논문 본문 8만 자를 무료로 검사하고 두 번 다듬어도 토큰이 남습니다.</p>'
            '<div class="grid3" style="margin-top:28px"><div class="card"><span class="ic">%s</span><h3>월 구독 없음</h3><p>한 번 충전하고 쓴 만큼만 빠집니다. 자동 결제도 없습니다.</p></div>'
            '<div class="card"><span class="ic">%s</span><h3>기한 없이 그대로</h3><p>남은 토큰은 사라지지 않고 기한 없이 씁니다. 같은 코드에 더 충전해 이어 쓸 수 있습니다.</p></div>'
            '<div class="card"><span class="ic">%s</span><h3>1분 안에 코드</h3><p>결제가 확인되면 보통 1분 안에 이메일로 16자리 토큰 코드가 갑니다.</p></div></div></div></section>') % (t, ico("card"), ico("clock"), ico("mail"))


PRICE_FAQ = [
    ("토큰은 어떻게 빠지나요?", "AI 작성률 검사는 무료이고, 휴머나이징을 누를 때만 글자 수만큼 토큰이 빠집니다. AI 휴머나이징은 1,000자에 4토큰이며, 빠질 토큰은 누르기 전에 화면에 먼저 보여 드립니다. 무료 검사(요약)는 토큰이 들지 않습니다."),
    ("결제하면 코드는 언제 오나요?", "결제가 확인되면 보통 1분 안에 결제할 때 적은 이메일로 16자리 토큰 코드가 갑니다. 메일의 단추를 누르면 코드가 자동으로 들어가고, 결제하러 가기 전에 넣어 둔 글을 그대로 이어서 휴머나이징합니다. 메일이 안 보이면 스팸함도 확인해 주세요."),
    ("결제할 때 무엇을 적어야 하나요?", "토큰 코드를 받을 이메일만 적으면 됩니다. 회원가입은 없고, 카드 · 토스페이 · 계좌이체 가운데 편한 방법으로 결제합니다."),
    ("카드 명세서에는 무엇으로 찍히나요?", "Humani 운영사인 성균관컨설팅으로 표시됩니다. 영수증도 성균관컨설팅 이름으로 발행됩니다."),
    ("남은 토큰은 사라지나요?", "사라지지 않습니다. 기한 없이 쓸 수 있고, 같은 코드에 더 충전해 이어서 쓸 수 있습니다."),
    ("다른 기기에서도 쓸 수 있나요?", "네. 메일로 받은 16자리 코드를 다른 기기에서 넣으면 남은 토큰을 그대로 씁니다. 코드를 아는 사람은 누구나 쓸 수 있으니 잘 보관해 주세요."),
]
MORE_FAQ = [
    ("AI 작성률은 어떻게 계산하나요?", "문장마다 판별 모델이 AI 점수를 매기고, 그 점수를 문장의 글자 수만큼 반영해 글 전체의 AI 작성률을 냅니다. 20% 미만은 안전, 20~40%는 고위험, 40% 이상은 부적합으로 판정합니다(Humani 판정 기준). 같은 글은 다시 검사해도 같은 값이 나옵니다."),
    ("직접 쓴 글도 AI로 나올 수 있나요?", "그럴 수 있습니다. 놓치는 AI 글을 줄이려고 기준을 엄격하게 잡았기 때문에, 딱딱한 보고서체로 쓴 사람 글도 작성률이 높게 나올 수 있습니다. 이럴 때도 AI처럼 읽히는 문장만 휴머나이징하면 오해를 줄일 수 있습니다."),
    ("휴머나이징을 한 번 더 하면 더 내려가나요?", "글에 따라 그렇습니다. 다듬은 뒤 다시 검사해서 보라색 문장이 남아 있으면 그 글로 한 번 더 휴머나이징하세요. 바뀌는 곳이 줄어들수록 토큰도 덜 듭니다."),
    ("문장 하나만 고칠 수도 있나요?", "네. 결과 화면에서 문장을 누르면 600자 이하의 짧은 글은 문장 고쳐 쓰기 도우미로 후보 문장을 보여 드립니다(토큰이 있을 때 0토큰)."),
    ("어떤 브라우저에서 되나요?", "크롬, 엣지, 웨일, 사파리 같은 최신 브라우저와 휴대폰에서 모두 됩니다. 설치할 프로그램은 없습니다."),
    ("휴머나이는 생성 AI로 글을 다시 쓰나요?", "아닙니다. 휴머나이 엔진은 생성 AI를 쓰지 않는 한국어 규칙 엔진입니다. 사람 글로 만든 사전과 문장 규칙으로 바꾸기 때문에 없는 내용을 지어내지 않습니다."),
]
