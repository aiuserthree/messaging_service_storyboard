# -*- coding: utf-8 -*-
"""
1) 표시·동작 분리: 표시면 "표시되는지 확인", 동작이면 "동작하는지 확인"만 사용. 같이 쓰지 않음.
2) 개발자 전용 영어 표현 제거·한글화 (모달→팝업, sticky, btn-, .html, placeholder, value:, API, localStorage, Toast 등)
"""
import re

FP = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

# 표시로 볼 키워드(주어/문맥에 있으면 "표시되는지")
DISPLAY_KEYWORDS = (
    "표시", "노출", "배치", "타이틀", "아이콘", "스타일", "배경", "색상", "형식", "포함", "목록", "카드", "섹션", "영역",
    "효과", "그룹핑", "가독성", "레이블", "강조 표시", "표시 내용", "표시 조건", "단가", "요금", "혜택", "슬로건",
    "원/건", "byte", "라인", "체크 아이콘", "테두리", "문구", "드롭다운 메뉴", "표시됨", "노출됨", "상단 고정", "고정"
)
# 동작으로 볼 키워드
ACTION_KEYWORDS = (
    "클릭", "이동", "실행", "저장", "전송", "선택", "변경", "입력", "제출", "호출", "닫기", "오픈", "토글", "전환",
    "초기화", "검증", "포맷팅", "롤링", "제거", "발송", "다운로드", "펼침", "접힘", "가능", "제공", "적용"
)

def is_display_side(phrase):
    """주어/구절이 '보이는 것' 위주면 True."""
    p = (phrase or "").strip()
    if not p:
        return False
    for k in DISPLAY_KEYWORDS:
        if k in p:
            return True
    for k in ACTION_KEYWORDS:
        if k in p:
            return False
    # 단가/요금 표시류 (숫자+원)
    if re.search(r"\d+원|\d+건|byte\)", p):
        return True
    return False

def fix_display_action(text):
    """'표시·동작하는지 확인' → 표시 또는 동작 중 하나로."""
    if "표시·동작하는지 확인" not in text and "표시되고 동작하는지 확인" not in text:
        return text

    def repl(m):
        subject = m.group(1).strip()
        if "표시되고 동작하는지 확인" in text and m.group(0) == "표시되고 동작하는지 확인":
            return "표시되는지 확인"
        if "영역" in subject or "유도" in subject or "섹션" in subject or "포함" in subject:
            return "표시되는지 확인"
        if is_display_side(subject):
            return "표시되는지 확인"
        return "동작하는지 확인"

    # "○○가 표시·동작하는지 확인" / "○○이 표시·동작하는지 확인"
    text = re.sub(r"([^<\n]+?)(가|이) 표시·동작하는지 확인", lambda m: m.group(1) + m.group(2) + " " + ("표시되는지 확인" if is_display_side(m.group(1)) else "동작하는지 확인"), text)
    text = re.sub(r"표시되고 동작하는지 확인", "표시되는지 확인", text)
    return text

# 개발자 영어 → 한글(또는 제거) 치환 목록. (패턴, 치환) 순서 유의.
DEV_REPLACEMENTS = [
    (r"\(sticky\)", ""),
    (r"상단 고정 \(\)", "상단 고정"),
    (r"\(Primary CTA\)", ""),
    (r"\(Primary Action\)", ""),
    (r"\(btn-outline\)", ""),
    (r"\(btn-primary\)", ""),
    (r"support-notice-detail\.html", "공지 상세 페이지"),
    (r"\([^)]*\.html\)", ""),  # (xxx.html) 제거
    (r"placeholder\s*:\s*", "입력 안내 문구: "),
    (r"placeholder:", "입력 안내 문구: "),
    (r"\s*\(value:\s*[^)]+\)", ""),  # (value: sms) 등 괄호 통째 제거
    (r"입력 타입:\s*textarea(?=\s|가|이|을|를|)", "여러 줄 글자 입력"),  # text보다 먼저
    (r"입력 타입:\s*text(?=\s|가|이|을|를|)", "한 줄 글자 입력"),
    (r"입력 타입:\s*tel(?=\s|가|이|을|를|)", "전화번호 입력"),
    (r"입력 타입:\s*email(?=\s|가|이|을|를|)", "이메일 주소 입력"),
    (r"\(resize:\s*vertical\)", "(세로로만 크기 조절)"),
    (r"\.active 클래스 추가로 display:\s*flex 전환", "팝업 표시 전환"),
    (r"Submit 이벤트 가로채기\s*\(preventDefault\)", "폼 제출 시 처리"),
    (r"\(preventDefault\)", ""),
    (r"API 호출", "서버 전송"),
    (r"API 확인", "서버 확인"),
    (r"localStorage에", "저장 공간에"),
    (r"localStorage 초기화", "저장 정보 초기화"),
    (r"토스트 표시", "잠깐 뜨는 알림 표시"),
    (r"완료 토스트", "완료 알림"),
    (r"다운로드 완료 토스트 알림", "다운로드 완료 알림"),
    (r"Alert 메시지", "알림 메시지"),
    (r"Confirm\b", "확인 창"),
    (r"모달 호출", "팝업 띄우기"),
    (r"모달 오픈", "팝업 열기"),
    (r"모달 닫기", "팝업 닫기"),
    (r"모달 닫힘", "팝업 닫힘"),
    (r"모달이 닫히고", "팝업이 닫히고"),
    (r"상담 신청 모달", "상담 신청 팝업"),
    (r"상담 신청서 모달", "상담 신청서 팝업"),
    (r"완료 모달", "완료 팝업"),
    (r"모달 구성", "팝업 구성"),
    (r"모달 또는 페이지", "팝업 또는 페이지"),
    (r"모달 또는 페이지로", "팝업 또는 페이지로"),
    (r"모달 또는 페이지 이동", "팝업 또는 페이지 이동"),
    (r"모달 호출", "팝업 띄우기"),
    (r"accent-color로 강조", "선택 시 강조 표시"),
    (r"onsubmit 이벤트로 handleSubmit\(\) 함수 호출", "제출 시 서버 전송"),
    (r"handleSubmit\(\)", ""),
    (r"타입:\s*button(?=\s|가|이|을|를|)", "버튼 유형: 일반"),
    (r"타입:\s*submit(?=\s|가|이|을|를|)", "버튼 유형: 제출"),
    (r"타입:\s*a 태그 \(링크\)", "링크 버튼"),
    (r"Secondary \(회색 배경\)", "보조(회색 배경)"),
    (r"Primary \(파란색 그라데이션", "주요(파란색 그라데이션"),
    (r"autocomplete=username", "아이디 자동완성"),
    (r"type=password", "비밀번호 칸"),
    (r"\.active 클래스 추가로 display:\s*flex\s+가\s*전환되는지 확인", "팝업이 표시되는지 확인"),
    (r"\.active 클래스 추가로 display:\s*flex[^<]*전환", "팝업 표시 전환"),
    (r"완료 알림 알림", "완료 알림"),
    (r"모달이\s", "팝업이 "),
    (r"모달에서\s", "팝업에서 "),
    (r"모달이 닫히는지", "팝업이 닫히는지"),
    (r"모달이 노출", "팝업이 노출"),
    (r"모달이 동작", "팝업이 동작"),
    (r"모달\b", "팝업"),  # 남은 모달 전부 팝업으로
    (r"\(#[\w-]+\)", ""),  # (#phoneOnlyInputModal) 등
    (r"\s*\(openAddRecipientModal\)", ""),
    (r"closeModal\s*\(\s*<br>\s*-\s*\)\s*호출", "팝업 닫기"),
    (r"closeModal\s*\(\s*\)\s*호출", "닫기 동작"),
    (r"closeModal\s*\(", "팝업 닫기"),
    (r"closeModal\s*\(\s*가 동작하는지 확인<br>- \)\s*호출이 동작하는지 확인", "닫기가 동작하는지 확인"),
    (r"closeModal\s*\(\s*가 동작", "닫기가 동작"),
    (r"\)\s*호출이 동작하는지 확인", "닫기가 동작하는지 확인"),
    (r"한 줄 글자 입력area", "여러 줄 글자 입력"),
    (r"팝업 표시 전환되는지 확인", "팝업이 표시되는지 확인"),
    (r"confirmAddRecipients\s*\(\s*\)\s*호출", "추가 확인 동작"),
    (r"Toast 메시지", "알림 메시지"),
    (r"Toast 알림", "알림"),
    (r"Toast:", "알림:"),
    (r"Toast가", "알림이"),
    (r"Toast\b", "알림"),
    (r"Alert\b", "알림 창"),
    (r"플레이스홀더:", "입력 안내 문구:"),
    (r"oninput으로 숫자만 허용", "숫자만 입력 가능"),
]

def apply_dev_replacements(s):
    for pat, repl in DEV_REPLACEMENTS:
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    return s

def process_line(line):
    if not line.strip().startswith("|") or " | " not in line or line.strip().startswith("|---"):
        return line
    parts = line.split(" | ", maxsplit=13)
    if len(parts) < 6:
        return line
    # parts[0]=|순번, 1=테스트ID, 2=테스트케이스명, 3=페이지/팝업, 4=단계, 5=예상결과
    step_col = 4
    expect_col = 5
    if len(parts) <= expect_col:
        return line

    step = parts[step_col]
    expect = parts[expect_col]
    name = parts[2] if len(parts) > 2 else ""

    # 1) 예상결과에서 표시·동작 분리
    expect = fix_display_action(expect)
    # 2) 단계·예상결과·테스트케이스명에서 개발자 영어 제거
    step = apply_dev_replacements(step)
    expect = apply_dev_replacements(expect)
    name = apply_dev_replacements(name)

    parts[2] = name
    parts[step_col] = step
    parts[expect_col] = expect

    return " | ".join(parts)

def main():
    with open(FP, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = [process_line(ln) for ln in lines]
    with open(FP, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("Done: display/action split + dev English removed.")

if __name__ == "__main__":
    main()
