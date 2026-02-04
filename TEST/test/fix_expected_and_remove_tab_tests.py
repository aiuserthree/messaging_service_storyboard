# -*- coding: utf-8 -*-
"""
1. "○○이(가) 정상 노출·동작함" → 괄호 없이 이/가 올바르게, 노출/동작 명확히
2. 단순 "탭 눌러서 페이지 열리는" 테스트 행 삭제
"""
import re

def has_batchim(c):
    """한글 마지막 글자 받침 여부. 있으면 True(이), 없으면 False(가)"""
    if not ('\uac00' <= c <= '\ud7a3'):
        return True  # 한글 아니면 기본 "이"
    return (ord(c) - 0xAC00) % 28 != 0

def particle(name):
    if not name:
        return "가"
    name = str(name).strip()
    last_char = name[-1] if name else ""
    return "이" if has_batchim(last_char) else "가"

def expect_display_or_action(case_name, step_content):
    """노출 vs 동작: 노출이면 노출됨, 동작이면 동작함. 굳이 동작 안 붙여도 되면 노출."""
    n = (case_name or "").strip()
    s = (step_content or "").strip()
    action_keywords = (
        "버튼", "입력", "선택", "링크", "발송", "저장", "삭제", "제출", "등록", "닫기", "초기화",
        "내보내기", "검색 버튼", "추가", "전환", "클릭", "이동"
    )
    display_keywords = (
        "헤더", "섹션", "영역", "카드", "모달", "폼", "그룹", "목록", "컨테이너", "미리보기",
        "요약", "경고", "내용", "필터", "인디케이터", "통계", "타입", "메뉴"
    )
    for k in action_keywords:
        if k in n or k in s[:80]:
            if "표시" in n or "노출" in s[:60]:
                continue
            return "동작함"
    for k in display_keywords:
        if k in n:
            return "노출됨"
    if "표시" in s[:80] or "노출" in s[:80] or "표시" in n:
        return "노출됨"
    return "노출됨"  # 기본은 노출로 (동작이라고 하지 말라고 함)

def is_trivial_tab_nav(case_name, step_content):
    """단순 "탭 눌러서 페이지 열리는" 테스트면 True → 제거"""
    n = (case_name or "").strip()
    s = (step_content or "").replace("<br>", " ").replace("\n", " ")
    # "탭 메뉴" 이고 내용이 탭 클릭 시 해당 페이지로 이동이 핵심인 경우
    if n == "탭 메뉴" and "탭 클릭 시 해당 페이지로 이동" in s:
        return True
    if not n:
        return False
    # "○○ 탭" (일반문자 탭, 광고문자 발송 탭 등) 이고 내용이 페이지 이동만인 경우
    if re.search(r".*\s+탭\s*$", n) and "메뉴" not in n:
        if re.search(r"페이지\s*(페이지)?로\s*이동|현재 페이지\s*\(\s*활성", s) and len(s) < 200:
            return True
    return False

def main():
    path = "FO_테스트시나리오_상세.md"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out = []
    for line in lines:
        # 테이블 데이터 행: | 순번 | TS-... | 케이스명 | 페이지/팝업 | 단계별... | 예상결과... |
        if not line.strip().startswith("|") or line.strip() == "|---":
            out.append(line)
            continue
        parts = line.split("|")
        if len(parts) < 7:
            out.append(line)
            continue
        try:
            num = (parts[1] or "").strip()
            if not re.match(r"^\d+$", num):
                out.append(line)
                continue
        except Exception:
            out.append(line)
            continue
        case_name = (parts[3] or "").strip()
        step_content = (parts[5] or "").strip()
        expected = (parts[6] or "").strip()

        # 삭제: 단순 탭→페이지 이동 테스트
        if is_trivial_tab_nav(case_name, step_content):
            continue

        # 수정: "○○이(가) 정상 노출·동작함" → "○○이/가 정상 노출됨" 또는 "○○이/가 정상 동작함"
        if "이(가) 정상 노출·동작함" in expected or "가(가) 정상 노출·동작함" in expected:
            base = expected.split("이(가) 정상")[0].split("가(가) 정상")[0].strip()
            if not base:
                base = case_name
            josa = particle(base)
            verb = expect_display_or_action(case_name, step_content)
            new_exp = f"{base}{josa} 정상 {verb}"
            parts[6] = " " + new_exp + " "
            line = "|".join(parts)
        out.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("Done.")

if __name__ == "__main__":
    main()
