# -*- coding: utf-8 -*-
"""Humani 엔진 실측(HMB 줄, 편집기 hmDemoPick 실행 로그)을 예시 화면 데이터(demo.json)로.
python3 _src/make_demo.py _src/demo_raw_hmb.txt"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
META = {"thesis": ("논문", "학위논문_결론.hwp"), "report": ("대학 레포트", "환경문제_레포트.docx"),
        "resume": ("자기소개서", "자기소개서_성격_장점.docx"), "blog": ("블로그 글", "블로그_재테크.txt")}
ORDER = ["thesis", "report", "resume", "blog"]
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "demo_raw_hmb.txt")
raw = {}
for line in open(src, encoding="utf-8"):
    m = re.search(r"HMB (\{.*\})\s*$", line.strip())
    if not m:
        continue
    o = json.loads(m.group(1))
    raw[o["k"]] = o
out = []
for k in ORDER:
    if k not in raw:
        print("빠짐", k)
        continue
    o = raw[k]
    if not o.get("after"):
        print("휴머나이징 결과 없음", k)
        continue
    out.append({"k": k, "label": META[k][0], "file": META[k][1], "src": o["src"], "dst": o["dst"],
                "ai": [i for i, s in enumerate(o["sc"]) if s[1]], "scores": {str(i): s[0] for i, s in enumerate(o["sc"]) if s[1]},
                "after_scores": {str(i): s[0] for i, s in enumerate(o.get("afterSc", []))},
                "before": {"rate": o["before"]["rate"], "band": o["before"]["band"], "n": o["before"]["n"]},
                "after": {"rate": o["after"]["rate"], "band": o["after"]["band"], "n": o["after"]["n"]}, "applied": o.get("ch", 0)})
json.dump({"samples": out, "date": "2026-11-21",
           "measured": "2026.11.21 Humani 엔진 실측값(Humani 판정 기준 1.6 · 인간화 엔진 HUM 2.5, 한 번의 휴머나이징). 글마다 결과는 다릅니다."},
          open(os.path.join(HERE, "demo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("samples", [(s["k"], s["before"]["rate"], s["after"]["rate"], s["applied"]) for s in out])
