#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
섹션 31 최종 데이터 수정 스크립트
원본 HTML 파일을 참고하여 올바른 예상 결과 작성
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 섹션 31 수정
section31_pattern = r'(## 31\. .*?\n.*?)(?=\n---|$)'
match = re.search(section31_pattern, content, re.DOTALL)

if match:
    section_content = match.group(1)
    lines = section_content.split('\n')
    new_lines = []
    
    # 예상 결과 매핑
    expected_map = {
        '페이지 로드 확인': '1:1 문의 페이지가 정상적으로 표시되고, 페이지 제목 "고객센터"와 설명 "궁금하신 점이나 문의사항을 남겨주시면 빠르게 답변드리겠습니다."가 표시되어야함',
        '페이지 설명 확인': '페이지 설명 "궁금하신 점이나 문의사항을 남겨주시면 빠르게 답변드리겠습니다."가 표시되어야함',
        '탭 구성 확인': '공지사항, 이벤트, FAQ, 1:1 문의 4개 탭이 표시되어야함',
        '현재 탭 활성 상태': '"1:1 문의" 탭이 활성 상태(파란색 하단 테두리)로 표시되어야함',
        '공지사항 탭 클릭': '공지사항 페이지로 이동되어야함',
        '이벤트 탭 클릭': '이벤트 페이지로 이동되어야함',
        'FAQ 탭 클릭': 'FAQ 페이지로 이동되어야함',
        '탭 화면 확인': '1:1 문의하기, 1:1 문의내역 2개 탭이 표시되어야함',
        '초기 탭 상태': '"1:1 문의하기" 탭이 활성 상태로 표시되고, 문의 폼 영역이 표시되어야함',
        '문의하기 탭 클릭': '문의 폼 영역이 표시되고, 문의내역 영역이 숨겨져야함',
        '문의내역 탭 클릭': '문의내역 영역이 표시되고, 문의 폼 영역이 숨겨져야함',
        '폼 화면 확인': '문의 입력 폼 카드가 표시되어야함',
        '아이디 필드': '아이디 입력 필드가 읽기전용으로 표시되고, 로그인 사용자 아이디가 자동 입력되어야함',
        '아이디 수정 불가': '아이디 입력 필드가 수정 불가 상태여야함',
        '이메일 아이디': '이메일 @ 앞부분 입력 필드가 표시되어야함',
        '이메일 도메인': '이메일 @ 뒷부분 입력 필드가 표시되어야함',
        '도메인 선택': '네이버, Gmail, 다음, 직접입력 옵션이 표시되어야함',
        '네이버 선택': '이메일 도메인이 "naver.com"으로 자동 입력되고 읽기전용으로 변경되어야함',
        'Gmail 선택': '이메일 도메인이 "gmail.com"으로 자동 입력되고 읽기전용으로 변경되어야함',
        '다음 선택': '이메일 도메인이 "daum.net"으로 자동 입력되고 읽기전용으로 변경되어야함',
        '직접입력 선택': '이메일 도메인 입력 필드가 활성화되고, 직접 입력이 가능해야함',
        '선택 입력 필드 확인': '문의유형 선택 드롭다운이 표시되고, 필수 표시(*)가 있어야함',
        '가격 문의 선택': '문의유형이 "가격 문의"로 선택되어야함',
        '서비스 문의 선택': '문의유형이 "서비스 문의"로 선택되어야함',
        '기술 문의 선택': '문의유형이 "기술 문의"로 선택되어야함',
        '기타 선택': '문의유형이 "기타"로 선택되어야함',
        '입력 필드 확인': '제목 입력 필드가 표시되고, 필수 표시(*)와 placeholder "제목을 입력해주세요"가 있어야함',
        '제목 입력': '입력한 제목이 표시되어야함',
        '입력 필드 확인': '문의내용 텍스트 영역이 표시되고, 필수 표시(*)와 placeholder "문의 내용을 입력해주세요"가 있어야함',
        '내용 입력': '입력한 문의내용이 표시되어야함',
        '파일 경로 필드': '파일 경로 표시 필드가 읽기전용으로 표시되고, placeholder "파일을 선택해주세요"가 있어야함',
        '찾아보기 버튼': '파일 선택 다이얼로그가 열려야함',
        '파일 선택': '선택한 파일명이 파일 경로 필드에 표시되어야함',
        '허용 파일 형식': 'jpg, jpeg, gif, png, bmp, docx, xlsx, xls, csv, pdf 파일만 선택 가능해야함',
        '파일 용량 제한': '"5MB 이하의 파일만 업로드 가능합니다." 오류 메시지가 표시되어야함',
        '화면 확인': '개인정보 동의 영역이 표시되어야함',
        '체크박스': '개인정보 동의 체크박스가 표시되고, 필수 표시(*)가 있어야함',
        '상세 내용': '수집 항목, 목적, 기간 안내가 표시되어야함',
        '버튼 영역': '다시쓰기, 문의하기 버튼이 우측 정렬로 표시되어야함',
        '버튼 클릭': '모든 입력 내용이 초기화되고, 기본값이 복원되어야함',
        '초기화 내용': '아이디/이메일 기본값이 복원되고, 나머지 필드는 비워져야함',
        '버튼 클릭': '유효성 검사가 실행되어야함',
        '필수 항목 미입력': '각 필수 항목에 대한 오류 메시지가 표시되어야함',
        '제목 미입력': '"제목을 입력해주세요" 오류 메시지가 표시되어야함',
        '내용 미입력': '"문의 내용을 입력해주세요" 오류 메시지가 표시되어야함',
        '개인정보 미동의': '"개인정보 수집 및 이용에 동의해주세요." 오류 메시지가 표시되어야함',
        '등록 성공': '"문의가 접수되었습니다. 빠른 시일 내에 답변드리겠습니다." 완료 메시지가 표시되고, 폼이 초기화되어야함',
        '테이블 영역': '문의내역 테이블이 표시되어야함',
        '테이블 헤더': '번호, 문의유형, 제목, 답변여부, 등록일 열이 표시되어야함',
        '빈 상태': '"문의하신 내역이 없습니다." 안내 메시지가 표시되어야함',
    }
    
    for line in lines:
        if not line.strip() or not line.startswith('|'):
            new_lines.append(line)
            continue
        
        if '---' in line or '순번' in line or '테스트ID' in line:
            new_lines.append(line)
            continue
        
        # 데이터 라인 파싱 및 수정
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) < 8:
            new_lines.append(line)
            continue
        
        seq = parts[0] if parts[0].isdigit() else ''
        test_id = parts[1] if len(parts) > 1 else ''
        order = parts[2] if len(parts) > 2 else ''
        test_case = parts[3] if len(parts) > 3 else ''
        page_popup = parts[4] if len(parts) > 4 else '페이지'
        steps = parts[5] if len(parts) > 5 else ''
        test_data = parts[6] if len(parts) > 6 else '별도 테스트 아이디 없이 진행'
        expected = parts[7] if len(parts) > 7 else ''
        
        # steps와 expected가 뒤바뀌어 있는 경우 수정
        expected_patterns = ['되어야함', '표시됨', '이동됨', '확인됨', '작동됨', '완료됨', '처리됨', '생성됨', '업데이트됨', '열려야함', '닫혀야함']
        
        if steps and not steps.startswith('-'):
            if any(pattern in steps for pattern in expected_patterns):
                steps, expected = expected, steps
            elif '접속' in steps or '클릭' in steps or '입력' in steps or '확인' in steps:
                if expected and not any(pattern in expected for pattern in expected_patterns):
                    steps, expected = expected, steps
        
        # steps가 "- "로 시작하지 않으면 추가
        if steps and not steps.startswith('-') and steps.strip():
            steps = f"- {steps}"
        
        # 예상 결과가 비어있거나 잘못된 경우 매핑에서 찾기
        if not expected or len(expected) < 10 or expected in ['#supportTabs 확인', '#inquiryTabs 확인', '#inquiryFormWrapper 확인', '#emailId 확인', '#emailDomain 확인', '#emailDomainSelect 확인', '#inquiryType 확인', '#subject 확인', '#content 확인', '#filePath 확인', '#privacyAgree 확인', '.privacy-agreement 확인', '.privacy-details 확인', '.form-actions 확인', '#inquiryHistory 확인', 'thead 확인']:
            if test_case in expected_map:
                expected = expected_map[test_case]
            elif '접속' in test_case or '로드' in test_case:
                expected = '페이지가 정상적으로 표시되어야함'
            elif '클릭' in test_case:
                expected = '해당 기능이 정상적으로 작동되어야함'
            elif '입력' in test_case:
                expected = '입력한 내용이 정상적으로 표시되어야함'
            elif '확인' in test_case:
                expected = '해당 항목이 정상적으로 표시되어야함'
            else:
                expected = '정상적으로 작동되어야함'
        
        # 표준 형식으로 재구성
        new_line = f"| {seq} | {test_id} | {order} | {test_case} | {page_popup} | {steps} | {test_data} | {expected} |  |  |  |  |  |  |  |  |  |  |"
        new_lines.append(new_line)
    
    new_section = '\n'.join(new_lines)
    content = content[:match.start()] + new_section + content[match.end():]
    
    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("섹션 31 최종 데이터 수정 완료!")
