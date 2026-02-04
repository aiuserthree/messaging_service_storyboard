#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단계별 작업 수행내용에 대한 예상 결과(6번째 컬럼)를 검증 가능한 문구로 정리합니다.
- 함수명/코드가 들어간 예상 결과 → 사용자 관점 검증 문구로 치환
- .html 파일명 → 한글 페이지명으로 치환
"""

import re

FP = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

# 예상 결과(6번째 컬럼) 내 치환 규칙 (패턴 -> 검증 문구). 순서 유의.
REPLACEMENTS = [
    (r'\bviewDetail\(id\) 호출\b', '클릭 시 상세보기 모달이 열리고 상세 정보가 표시되는지 확인'),
    (r'\bviewDetail\(id\)\b', '클릭 시 상세보기 모달이 열리는지 확인'),
    (r'\bcloseModal\(\s*$', '모달이 닫히고 화면이 이전 상태로 복귀하는지 확인'),
    (r'\bcloseModal\(\s*\<br\>.*취소.*모달', '모달이 닫히고 입력 내용이 초기화되는지 확인'),
    (r'\bcloseModal\(', '모달이 닫히는지 확인'),
    (r'\bfilterStatus\(\s*$', '선택한 상태별로 목록이 필터링되어 표시되는지 확인'),
    (r'\bfilterStatus\(', '선택한 상태별로 목록이 필터링되는지 확인'),
    (r'\bopenRegisterModal\(\) 호출\b', '클릭 시 발신번호 등록 모달이 열리는지 확인'),
    (r'\bcheckDuplicateNumber\(\) 호출\b', '발신번호 중복 여부가 조회되고 결과가 표시되는지 확인'),
    (r'\bnextStep\(\) 호출\b', '유효성 검증 후 다음 단계로 진행되는지 확인'),
    (r'\bdownloadDocument\(fileName\) 호출\b', '해당 서류 파일이 다운로드되는지 확인'),
    (r'\bopenFaq\(\s*\<br\>.*클릭 시 해당 FAQ', '클릭 시 해당 FAQ로 스크롤 이동 및 답변이 펼쳐지는지 확인'),
    (r'\bopenFaq\(', '클릭 시 해당 FAQ 항목이 펼쳐지는지 확인'),
    (r'\bswitchInquiryTab\(\s*\<br\>.*클릭 시 문의 작성', '클릭 시 문의 작성 폼이 표시되는지 확인'),
    (r'\bswitchInquiryTab\(\s*\<br\>.*클릭 시 문의 내역', '클릭 시 문의 내역 테이블이 표시되는지 확인'),
    (r'\bswitchInquiryTab\(', '클릭 시 해당 탭 화면이 표시되는지 확인'),
    (r'\bhandleEmailDomainChange\(\) 호출\b', '선택한 도메인에 따라 이메일 입력 필드가 갱신되는지 확인'),
    (r'\bdeleteCallerNumber\(id\) 호출\b', '확인 후 해당 발신번호가 삭제되는지 확인'),
    (r'\bviewRejectionReason\(id\) 호출\b', '반려 사유가 알림 또는 모달로 표시되는지 확인'),
    (r'\bopenPhoneAuth\(\) 호출\b', '본인인증 창이 열리고 완료 시 화면에 반영되는지 확인'),
    (r'\bfilterCategory\(\s*$', '선택한 카테고리별로 FAQ 목록이 필터링되는지 확인'),
    (r'\bfilterCategory\(', '선택한 카테고리별로 FAQ 목록이 필터링되는지 확인'),
    (r'\btoggleFaq\(element\) 호출\b', '클릭 시 해당 FAQ 답변이 펼쳐지거나 접히는지 확인'),
    (r'대량발송 견적 상담 신청 모달 호출', '클릭 시 상담 신청 모달이 열리는지 확인'),
    (r'대량 발송 견적 상담 신청 모달 호출', '클릭 시 상담 신청 모달이 열리는지 확인'),
    (r'아이디 찾기 기능 호출', '클릭 시 아이디 찾기 모달 또는 페이지가 표시되는지 확인'),
    (r'비밀번호 찾기/재설정 기능 호출', '클릭 시 비밀번호 찾기 모달 또는 페이지가 표시되는지 확인'),
    (r'브랜드메시지 M,N 타깃 사용 신청 모달 열기 및 API 호출', '클릭 시 브랜드메시지 신청 모달이 열리고 API 호출 후 안내가 표시되는지 확인'),
    (r'\bselectGroup\(groupId\) 호출\b', '클릭 시 해당 그룹이 선택되고 우측 목록에 해당 그룹 주소록만 표시되는지 확인'),
    (r'\btoggleGroupMenu\(groupId\) 호출\b', '클릭 시 해당 그룹의 드롭다운 메뉴가 표시되는지 확인'),
    (r'\beditGroupName\(groupId,\s*name\) 호출\b', '클릭 시 그룹명 수정 모달이 열리는지 확인'),
    (r'\bopenAddAddressModal\(\) 호출\b', '클릭 시 주소 추가 모달이 열리는지 확인'),
    (r'\bdownloadSampleFile\(\) 호출\b', '주소록 샘플 파일이 다운로드되는지 확인'),
    (r'\bsendMessage\(\) 호출\b', '선택 시 문자발송 페이지로 이동되는지 확인, 미선택 시 경고가 표시되는지 확인'),
    (r'\btoggleAll\(this\) 호출\b', '클릭 시 전체 선택/해제가 토글되는지 확인'),
    (r'\beditAddress\(id\) 호출\b', '클릭 시 주소 수정 모달이 열리는지 확인'),
    (r'\bdownloadAddressBookSampleFile\(\) 호출\b', '주소록 샘플 파일이 다운로드되는지 확인'),
    (r'\baddAddressBookRow\(\) 호출\b', '입력 행이 추가되는지 확인'),
    (r'\bdeleteSelectedAddressBookRows\(\) 호출\b', '선택된 행이 삭제되는지 확인'),
    (r'\bdeleteAllAddressBookRows\(\) 호출\b', '모든 행이 삭제되는지 확인'),
    (r'\bremoveDuplicateAddressBookNumbers\(\) 호출\b', '중복 전화번호가 제거되는지 확인'),
    (r'\bremoveRejectAddressBookNumbers\(\) 호출\b', '수신거부 번호가 제거되는지 확인'),
    (r'\bsaveAddressBookFromTable\(\) 호출\b', '주소록이 저장되는지 확인'),
    (r'\bdownloadExcel\(\) 호출\b', '조회된 목록이 엑셀 파일로 다운로드되는지 확인'),
    (r'\bdownloadSample\(\) 호출\b', '샘플/양식 파일이 다운로드되는지 확인'),
    (r'\bhandleExcelUpload\(event\) 호출\b', '선택한 엑셀 파일이 업로드되고 목록에 반영되는지 확인'),
    (r'\bgoToSuccessPage\(rowId,\s*page\) 호출\b', '성공 내역 페이지로 이동되는지 확인'),
    (r'\btoggleAllFailedCheckboxes\(rowId,\s*checked\) 호출\b', '실패 항목 전체 선택/해제가 토글되는지 확인'),
    (r'\bselectAllFailed\(id\) 호출\b', '해당 건의 실패 항목이 전부 선택되는지 확인'),
    (r'\bdownloadResultReport\(id\) 호출\b', '결과 리포트가 다운로드되는지 확인'),
    (r'\bresendFromDetail\(\) 호출\b', '모달이 닫히고 재발송 페이지로 이동되는지 확인'),
    (r'클릭 시 send-result\.html로 이동', '클릭 시 발송결과 페이지로 이동되는지 확인'),
    (r'send-result\.html로 이동', '발송결과 페이지로 이동되는지 확인'),
    (r'\bcancelReservation\(id\) 호출\b', '확인 후 예약이 취소되는지 확인'),
    (r'\bcopyAndSend\(\) 호출\b', '예약 내용이 복사되어 새 발송 페이지로 이동되는지 확인'),
    (r'\bhandleReset\(\) 호출\b', '입력 내용이 초기화되는지 확인'),
    (r'\baddGroupRow\(\) 호출\b', '입력 행이 추가되는지 확인'),
    (r'\bdeleteSelectedGroupRows\(\) 호출\b', '선택된 행이 삭제되는지 확인'),
    (r'\bdeleteAllGroupRows\(\) 호출\b', '모든 행이 삭제되는지 확인'),
    (r'\bremoveDuplicateGroupNumbers\(\) 호출\b', '중복 전화번호가 제거되는지 확인'),
    (r'\bremoveRejectGroupNumbers\(\) 호출\b', '수신거부 번호가 제거되는지 확인'),
    (r'message-send-general\.html 페이지로 이동', '일반문자 발송 페이지로 이동되는지 확인'),
    (r'message-send-general\.html로 이동', '일반문자 발송 페이지로 이동되는지 확인'),
    (r'message-send-ad\.html 페이지로 이동', '광고문자 발송 페이지로 이동되는지 확인'),
    (r'message-send-ad\.html로 이동', '광고문자 발송 페이지로 이동되는지 확인'),
    (r'template-message\.html 페이지로 이동', '일반문자 템플릿 페이지로 이동되는지 확인'),
    (r'template-message\.html로 이동', '일반문자 템플릿 페이지로 이동되는지 확인'),
    (r'message-send-election\.html 페이지로 이동', '선거문자 발송 페이지로 이동되는지 확인'),
    (r'message-send-election\.html로 이동', '선거문자 발송 페이지로 이동되는지 확인'),
    (r'addressbook-reject\.html 페이지로 이동', '수신거부관리 페이지로 이동되는지 확인'),
    (r'addressbook-reject\.html로 이동', '수신거부관리 페이지로 이동되는지 확인'),
    (r'addressbook\.html로 이동', '주소록 관리 페이지로 이동되는지 확인'),
    (r'send-reservation\.html로 이동', '예약내역 페이지로 이동되는지 확인'),
    (r'support-notice\.html로 이동', '공지사항 페이지로 이동되는지 확인'),
    (r'support-event\.html로 이동', '이벤트 페이지로 이동되는지 확인'),
    (r'support-faq\.html로 이동', 'FAQ 페이지로 이동되는지 확인'),
    (r'support-inquiry\.html로 이동', '1:1문의 페이지로 이동되는지 확인'),
    (r'mypage-profile\.html로 이동', '내 정보 수정 페이지로 이동되는지 확인'),
    (r'mypage-password\.html로 이동', '비밀번호 변경 페이지로 이동되는지 확인'),
]

def process_line(line: str) -> str:
    if not line.strip().startswith("|") or "TS-" not in line or line.strip().startswith("| ---"):
        return line
    parts = line.split(" | ", 6)
    if len(parts) < 6:
        return line
    cell6 = parts[5]
    for pattern, replacement in REPLACEMENTS:
        cell6 = re.sub(pattern, replacement, cell6)
    parts[5] = cell6
    return " | ".join(parts[:6]) + (" | " + parts[6] if len(parts) > 6 else "")

def main():
    with open(FP, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = [process_line(ln) for ln in lines]
    with open(FP, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("예상 결과 컬럼 수정을 반영해 저장했습니다.")

if __name__ == '__main__':
    main()
