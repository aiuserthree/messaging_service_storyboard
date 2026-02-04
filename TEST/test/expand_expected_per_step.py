#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단계별 작업 수행내용이 다수일 때, 각 수행내용에 대응하는 예상결과를 모두 나열합니다.
- 단계(5번 컬럼)을 <br> 기준으로 분리해 개별 불릿 추출
- 각 불릿 내용을 검증문구(~되는지 확인)로 변환 후 <br>- 로 이어서 6번 컬럼에 저장
"""
import re
import sys
sys.path.insert(0, r"c:\Users\ibank\Desktop\spec\TEST\test")
from normalize_same_step_expected import to_verify, josa_iga

FP = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"
GENERIC_PHRASE = "해당 기능이 정상 표시·동작하는지 확인"

def extract_bullets(step_col):
    """
    단계별 작업 셀에서 '수행내용' 불릿만 추출.
    "- ", "• ", "①②③④⑤ " 로 시작하는 줄의 본문만 수집. 【...】만 있는 줄은 제외.
    앞의 불릿 기호를 모두 제거한 순수 본문만 반환.
    """
    if not step_col or not step_col.strip():
        return []
    lines = step_col.replace("<br>", "\n").split("\n")
    bullets = []
    for line in lines:
        t = line.strip()
        if not t:
            continue
        # 【제목】만 있는 줄은 제외 (본문이 없으면 스킵)
        if re.match(r"^【[^】]+】\s*$", t):
            continue
        # "- 내용" or "• 내용" or "① 내용" 등 → 앞의 기호 제거 후 본문만
        content = re.sub(r"^[\s\-\•①②③④⑤]+", "", t).strip()
        if not content or len(content) < 2:
            continue
        if re.match(r"^【[^】]+】\s*$", content):
            continue
        bullets.append(content)
    return bullets

# 예상결과 문구 보정 (어색한 조사/표현 치환)
_EXPECTED_FIXES = [
    ("수동이 전환되는지", "수동 전환이 되는지"),
    ("직접으로 이동되는지", "직접 이동되는지"),
]

def bullet_to_specific_verify(bullet):
    """
    불릿 문장을 구체적인 검증문으로 변환.
    to_verify가 '해당 기능이 정상 표시·동작하는지 확인'을 줄 때만 구체화 fallback 적용.
    """
    b = (bullet or "").strip()
    if not b or len(b) < 2:
        return None
    v = to_verify(b)
    if v == GENERIC_PHRASE:
        # 불릿 내용을 그대로 써서 구체적인 검증문으로 만든다
        v = b + josa_iga(b) + " 표시·동작하는지 확인"
    return v

def build_expected_from_bullets(bullets):
    """불릿 리스트를 검증문구로 바꾼 뒤 '<br>- ' 로 연결"""
    if not bullets:
        return None
    verified = []
    for b in bullets:
        v = bullet_to_specific_verify(b)
        if v:
            for old, new in _EXPECTED_FIXES:
                v = v.replace(old, new)
            verified.append(v)
    if not verified:
        return None
    return "<br>- ".join(verified)

def process_line(line):
    if not line.strip().startswith("|") or "TS-" not in line or line.strip().startswith("| ---"):
        return line
    parts = line.split(" | ", 6)
    if len(parts) < 6:
        return line
    step_col = (parts[4] or "").strip()
    bullets = extract_bullets(step_col)
    # 수행내용이 1개 이상이면 각각 예상결과 생성(구체화 fallback 적용)
    if len(bullets) >= 1:
        new_exp = build_expected_from_bullets(bullets)
        if new_exp:
            parts[5] = new_exp
    # 1개 이하면 기존 예상결과 유지(또는 원하면 to_verify(bullets[0]) 적용 가능)
    return " | ".join(parts[:6]) + (" | " + parts[6] if len(parts) > 6 else "")

def main():
    with open(FP, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = [process_line(ln) for ln in lines]
    with open(FP, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("다수 단계에 대해 예상결과를 각 수행내용별로 펼쳐 반영했습니다.")

if __name__ == "__main__":
    main()
