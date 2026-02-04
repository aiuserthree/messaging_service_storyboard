# -*- coding: utf-8 -*-
"""예상 결과 컬럼 삭제 + 단계별 작업 수행내용을 테스터 조작/점검 문장으로 정리"""
import re
import sys

path = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

def remove_expected_result_column(line: str) -> str:
    """테이블 행에서 예상 결과(6번째 컬럼) 제거."""
    if "예상 결과(연계 모듈 점검사항 확인)" in line:
        return line.replace(" | 예상 결과(연계 모듈 점검사항 확인) |", " |")
    if line.strip().startswith("| ---") and "---" in line:
        return re.sub(r"(\| --- \| --- \| --- \| --- \| --- \|) --- \|", r"\1", line)
    # 데이터 행에서 6번째 파이프 구간(예상결과) 제거. 5개 컬럼 뒤의 한 셀을 지운다.
    if " | TS-" in line:
        m = re.match(r"^(\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*)\|[^|]*(\|.*)$", line)
        if m:
            return m.group(1) + m.group(2)  # 6번째 셀 제거
    return line

def normalize_step_content(text: str) -> str:
    """단계별 작업 수행내용에서 개발용어를 줄이고 테스터 조작/점검 문장으로."""
    if not text or "단계별" in text:
        return text
    t = text
    # 개발자 용어 -> 일반 표현
    t = re.sub(r"\w+\(\s*\w*\s*\)\s*호출\s*", "", t)
    t = re.sub(r"[\w.]+\s*\([^)]*\)\s*호출\s*", "", t)
    t = re.sub(r"API\s*호출\s*", "전송·반영 후 결과를 확인한다. ", t)
    t = re.sub(r"모달\s*호출\s*", "클릭 시 모달이 열리는지 확인한다. ", t)
    t = re.sub(r"모달\s*닫기\s*호출\s*", "클릭 시 모달이 닫히는지 확인한다. ", t)
    t = re.sub(r"\bToast\b", "알림", t)
    t = re.sub(r"\bAlert\b", "알림", t)
    t = re.sub(r"Confirm\s*표시", "확인 창이 뜨는지 확인", t)
    t = re.sub(r"Confirm\s*팝업", "확인 창", t)
    t = re.sub(r"#[\w-]+\s*요소\s*", " ", t)
    t = re.sub(r"[\w]+(?:FileInput|fileInput|Input)\s*클릭", "해당 버튼 클릭 시 파일 선택 창이 열리는지 확인", t, flags=re.I)
    t = re.sub(r"다이얼로그", "창", t)
    t = re.sub(r"input\s*필드", "입력란", t, flags=re.I)
    t = re.sub(r"oninput\w*\s*으로\s*숫자만\s*허용", "입력 시 숫자만 입력되는지 확인", t, flags=re.I)
    t = re.sub(r"oninput\s*으로", "입력 시", t, flags=re.I)
    t = re.sub(r"flex-shrink:\s*0", "숫자 영역 너비 고정", t)
    t = re.sub(r"download\w*\(\)\s*호출", "클릭 시 해당 파일이 다운로드되는지 확인", t, flags=re.I)
    t = re.sub(r"handle\w+\(\)\s*호출", "클릭 시 해당 동작이 수행되는지 확인", t, flags=re.I)
    t = re.sub(r"add\w+Row\(\)\s*호출", "행 추가 버튼 클릭 시 행이 추가되는지 확인", t, flags=re.I)
    t = re.sub(r"delete\w+Rows?\(\)\s*호출", "해당 버튼 클릭 시 선택 행이 삭제되는지 확인", t, flags=re.I)
    t = re.sub(r"remove\w+\(\)\s*호출", "해당 버튼 클릭 시 목록에서 제거되는지 확인", t, flags=re.I)
    t = re.sub(r"save\w+\(\)\s*호출", "저장 클릭 시 반영·닫힘 여부 확인", t, flags=re.I)
    t = re.sub(r"open\w+Modal\(\)\s*호출", "클릭 시 해당 모달이 열리는지 확인", t, flags=re.I)
    t = re.sub(r"goTo\w+\([^)]*\)\s*호출", "클릭 시 해당 페이지로 이동하는지 확인", t, flags=re.I)
    t = re.sub(r"toggle\w+\([^)]*\)\s*호출", "클릭 시 선택/해제가 바뀌는지 확인", t, flags=re.I)
    t = re.sub(r"confirm\w+\(\)\s*호출", "클릭 시 해당 처리 후 반영되는지 확인", t, flags=re.I)
    t = re.sub(r"resend\w+\(\)\s*호출", "클릭 시 재발송이 요청되는지 확인", t, flags=re.I)
    t = re.sub(r"copyAnd\w+\(\)\s*호출", "클릭 시 예약 내용이 복사된 새 발송 페이지로 이동하는지 확인", t, flags=re.I)
    t = re.sub(r"downloadExcel\(\)\s*호출", "클릭 시 조회 결과가 엑셀로 다운로드되는지 확인", t, flags=re.I)
    t = re.sub(r"downloadSample\(\)\s*호출", "클릭 시 샘플 파일이 다운로드되는지 확인", t, flags=re.I)
    return t

out = []
for line in lines:
    line = remove_expected_result_column(line)
    # 테이블 데이터 행에서 5번째 컬럼(단계별 작업 수행내용)만 정규화
    if " | TS-" in line and (" | 페이지 | " in line or " | 팝업 | " in line):
        part = line.split(" | ", 5)
        if len(part) >= 5:
            part[4] = normalize_step_content(part[4])
            line = " | ".join(part[:5]) + (" | " + part[5] if len(part) > 5 else "")
    out.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(out)

print("Done: column removed and step content normalized.")
