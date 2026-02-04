# -*- coding: utf-8 -*-
"""
1. 영어 표현 한글화 (localStorage, html경로, 괄호 영어 등)
2. 모든 섹션에서 단계별작업 vs 예상결과 구분 (예상결과를 검증 문장으로)
3. 시나리오 간소화 (정상/비정상 케이스 나열 축약, 과다 상세 삭제)
"""
import re
import sys

INPUT_PATH = "FO_테스트시나리오_상세.md"
OUTPUT_PATH = "FO_테스트시나리오_상세.md"

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # === 1. 영어 한글화 치환 ===
    replacements = [
        (r"localStorage", "브라우저 로컬 저장소"),
        (r"\(Primary Action\)", "(주요 동작)"),
        (r"storyboard/wireframe-spec-\*\.html", "화면설계 문서"),
        (r"`storyboard/wireframe-spec-\*\.html`", "화면설계 문서"),
        (r"message-send-general\.html", "일반문자 발송 페이지"),
        (r"message-send-ad\.html", "광고문자 발송 페이지"),
        (r"template-message\.html", "일반문자 템플릿 페이지"),
        (r"message-send-election\.html", "선거문자 발송 페이지"),
        (r"addressbook-reject\.html", "수신거부관리 페이지"),
        (r"addressbook\.html", "주소록 관리 페이지"),
        (r"send-reservation\.html", "예약내역 페이지"),
        (r"send-result\.html", "발송결과 페이지"),
        (r"mypage-profile\.html", "내 정보 수정 페이지"),
        (r"mypage-password\.html", "비밀번호 변경 페이지"),
        (r"support-notice\.html", "공지사항 페이지"),
        (r"support-event\.html", "이벤트 페이지"),
        (r"support-inquiry\.html", "1:1문의 페이지"),
        (r"autocomplete=username", "자동완성 허용"),
        (r"Submit 이벤트", "제출 이벤트"),
        (r"\(date picker\)", "(날짜 선택)"),
        (r"Step 1:", "1단계:"),
        (r"Step 2:", "2단계:"),
        (r"Step 3:", "3단계:"),
        (r"Step 1 ", "1단계 "),
        (r"Step 2 ", "2단계 "),
        (r"Step 3 ", "3단계 "),
        (r"\.active 클래스", "활성 클래스"),
        (r"display: flex", "보임 처리"),
        (r"Toast 알림", "토스트 알림"),
        (r"Toast 메시지", "토스트 메시지"),
        (r"Toast:", "토스트:"),
        (r"Alert 메시지", "알림 메시지"),
        (r"Confirm 메시지", "확인 메시지"),
        (r"Alert:", "알림:"),
        (r"placeholder:", "안내 문구:"),
        (r"value:\s*<br>", "기본값: "),
        (r"onsubmit 이벤트로 handleSubmit\(\) 함수 호출", "폼 제출 시 제출 처리 함수 호출"),
        (r"toggleAll\(this\) 호출", "전체 선택/해제 처리"),
        (r"selectGroup\(groupId\) 호출", "그룹 선택 처리"),
        (r"toggleGroupMenu\(groupId\) 호출", "그룹 메뉴 열기/닫기"),
        (r"editAddress\(id\) 호출", "주소 수정 처리"),
        (r"viewDetail\(id\) 호출", "상세보기 처리"),
        (r"viewRejectionReason\(id\) 호출", "반려사유 보기 처리"),
        (r"handleExcelUpload\(event\) 호출", "엑셀 업로드 처리"),
        (r"downloadResultReport\(id\) 호출", "결과 리포트 다운로드"),
        (r"cancelReservation\(id\) 호출", "예약 취소 처리"),
        (r"selectAllFailed\(id\) 호출", "실패 항목 전체 선택"),
        (r"deleteCallerNumber\(id\) 호출", "발신번호 삭제 처리"),
        (r"downloadDocument\(fileName\) 호출", "문서 다운로드 처리"),
        (r"toggleFaq\(element\) 호출", "FAQ 펼침/접기 처리"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # HTML 파일 경로 패턴 (클릭 시 xxx.html로 이동 등)
    text = re.sub(r"클릭 시 ([a-z\-]+)\.html로 이동", r"클릭 시 해당 페이지로 이동", text)
    text = re.sub(r"([a-z\-]+)\.html 페이지로 이동", "해당 페이지로 이동", text)
    text = re.sub(r"→ ([a-z\-]+)\.html", "→ 해당 페이지", text)

    # (영문) 괄호 안 영어 → 한글 또는 삭제
    text = re.sub(r"\(Enter\) 키", "엔터 키", text)
    text = re.sub(r"엔터\(Enter\) 키", "엔터 키", text)
    text = re.sub(r"쉼표\(,\)", "쉼표", text)
    text = re.sub(r"줄바꿈\(\\n\)", "줄바꿈", text)
    text = re.sub(r"\(SMS\)", "문자", text)  # 문맥에 따라 보존할 수도 있음 → "문자(SMS)" 유지하는 게 나을 수 있음. 취소
    # SMS/LMS/MMS, API, PDF 등 약어는 유지

    # 테스트용 예시 이메일 (예시로 두고 한글 설명만 추가할지, 전부 한글 예시로 바꿀지)
    # 'test@example.com' → 유지하되 괄호로 (예시) 추가는 사용자 요청이 "영어 삭제 또는 한글"이므로
    # "테스트용 이메일 입력 시" 로 바꿀 수 있음
    text = re.sub(r"'test@example\.com' 입력 시 정상 처리", "올바른 이메일 형식 입력 시 정상 처리", text)
    text = re.sub(r"'test@example\.com' 입력 시 정상 처리 확인", "올바른 이메일 형식 입력 시 정상 처리 확인", text)
    text = re.sub(r"tok\*\*\*@example\.com", "아이디 일부 마스킹 예시(예: abc***@xx.xx)", text)

    # === 2. 단계별 작업 vs 예상 결과 구분 ===
    # 컬럼: 0빈 1순번 2테스트ID 3테스트케이스명 4페이지/팝업 5단계별 6예상결과 7~
    # 예상결과가 단계별 요약과 동일한 행만, "동작·노출 검증" 관점 문장으로 보정
    lines = text.split("\n")
    out_lines = []
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 7 and re.match(r"^\s*\d+\s*$", (parts[1] or "").strip()):
            step = (parts[5] or "").strip()
            expected = (parts[6] or "").strip()
            name = (parts[3] or "").strip()
            # 단계별 첫 줄만 추출 (br 기준)
            first_line = re.sub(r"<br>.*", "", step).replace("- ", "").strip()[:60]
            # 예상결과가 비었거나, 단계별 첫 줄과 거의 같으면 검증 문장으로 교체
            if not expected or expected == first_line or expected in step or (len(expected) < 25 and first_line.startswith(expected)):
                new_expected = f"{name}이(가) 정상 노출·동작함" if name else "해당 기능 정상 노출·동작 확인"
                parts[6] = " " + new_expected + " "
                line = "|".join(parts)
        out_lines.append(line)
    text = "\n".join(out_lines)

    # === 3. 간소화: 정상/비정상 케이스 나열 → 한 줄 요약 ===
    # "정상 케이스: ... 비정상 케이스: ... (반복)" 블록을 "이메일·전화번호 형식 검증 확인" 등으로
    def shorten_validation_blocks(t):
        # 전화번호 검증 나열
        p1 = r"<br>- 전화번호 최소 9자리 이상 입력 확인<br>- 정상 케이스: '[^']+' 입력 시 정상 처리 확인<br>- 정상 케이스: '[^']+' 입력 시 자동 하이픈 포맷팅 확인<br>- 비정상 케이스: 9자리 미만 입력 시 '[^']+' 알림 메시지 노출 확인<br>- 비정상 케이스: 숫자가 아닌 문자 입력 시 자동 제거 또는 알림 메시지 노출 확인"
        t = re.sub(p1, "<br>- 전화번호 9자리 이상·숫자만 허용 검증 및 하이픈 자동 포맷 확인", t)

        # 이메일 검증 나열 (긴 블록)
        p2 = r"<br>- 정상 케이스: '[^']+' 입력 시 정상 처리 확인<br>- 비정상 케이스: '@'와 '.'이 없는 경우 '[^']+' 알림 메시지 노출 확인<br>- 비정상 케이스: @앞에 영문텍스트가 없는 경우 알림 메시지 노출 확인<br>- 비정상 케이스: \.앞과 뒤에 영문텍스트가 없는 경우 알림 메시지 노출 확인<br>- 비정상 케이스: 한글 텍스트가 입력된 경우 알림 메시지 노출 확인<br>- 비정상 케이스: 입력값이 100자 이상인 경우 알림 메시지 노출 확인"
        t = re.sub(p2, "<br>- 이메일 형식 검증 및 허용 길이(100자) 확인", t)

        # 비밀번호 검증 나열
        p3 = r"<br>- 비밀번호 입력\(영문,숫자,특수문자 포함 8~20자 이내\) 조건에 따른 알림 메시지 노출/숨김 확인<br>- 입력조건 불충족 시 '[^']+' 알림 메시지 노출, 20자 이상 입력불가<br>- 정상 케이스: '[^']+' 입력 시 정상 처리 확인<br>- 비정상 케이스: 7자 이하 입력 시 알림 메시지 노출 확인<br>- 비정상 케이스: 21자 이상 입력 시 입력 불가 확인<br>- 비정상 케이스: 영문만 입력 시 알림 메시지 노출 확인<br>- 비정상 케이스: 숫자만 입력 시 알림 메시지 노출 확인"
        t = re.sub(p3, "<br>- 비밀번호 8~20자, 영문·숫자·특수문자 조합 검증 확인", t)

        # 이름 바이트
        p4 = r"<br>- 이름 입력 시 바이트 수 확인<br>- 최대 100바이트 \(한글 약 50자, 영문 100자\) 제한 확인<br>- 정상 케이스: '홍길동' 입력 시 '[^']+' 표시 확인<br>- 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인"
        t = re.sub(p4, "<br>- 이름 최대 100바이트 제한 및 바이트 표시 확인", t)

        # 그룹명 바이트 등 중복 패턴
        p5 = r"<br>- 그룹명 입력 시 바이트 수 확인<br>- 최대 50바이트[^<]*<br>- 정상 케이스:[^<]+<br>- 비정상 케이스:[^<]+"
        t = re.sub(p5, "<br>- 그룹명 최대 50바이트 제한 확인", t)

        return t

    text = shorten_validation_blocks(text)

    # 추가: "빈 값 시<br>- 에러" 등 불완전한 문장 정리
    text = re.sub(r"빈 값 시<br>- 에러", "빈 값 시 오류 메시지 표시", text)
    text = re.sub(r"빈 값 시<br>- 에러 메시지", "빈 값 시 오류 메시지 표시", text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Done. Wrote", OUTPUT_PATH)

if __name__ == "__main__":
    main()
