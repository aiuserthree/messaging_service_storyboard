#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA 직원 관점에서 종합적인 테스트 시나리오 개선:
1. 메뉴 순서에 맞춰 섹션 번호 및 테스트ID 재정리
2. 참고 문서 기반 정합성 체크 및 누락 기능 설명 추가
3. HTML 파일 기반 기능 설명 확인 및 반영 (글자수 제한 포함)
4. 같은 영역의 세분화된 항목 통합 및 간소화
5. 개발자 용어 제거 및 한글 용어로 통일
"""

import re
import os

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

# 메뉴 순서 매핑 (현재 섹션 번호 -> 새로운 섹션 번호)
MENU_ORDER_MAP = {
    2: 1,   # 랜딩페이지 (TS-01)
    3: 2,   # 로그인 (TS-02)
    4: 3,   # 대시보드 (TS-03)
    5: 4,   # 일반문자 발송 (TS-04)
    6: 5,   # 광고문자 발송 (TS-05)
    7: 6,   # 일반문자 템플릿 (TS-06)
    8: 7,   # 광고문자 템플릿 (TS-07)
    9: 8,   # 선거문자 발송 (TS-08)
    10: 9,  # 선거문자 템플릿 (TS-09)
    11: 10, # 알림톡 발송 (TS-10)
    12: 11, # 브랜드 메시지 발송 (TS-11)
    13: 12, # 카카오톡 발신 프로필 (TS-12)
    14: 13, # 알림톡 템플릿 (TS-13)
    15: 14, # 브랜드 메시지 템플릿 (TS-14)
    18: 15, # 주소록 관리 (TS-15)
    19: 16, # 수신거부관리 (TS-16)
    16: 17, # 발송결과 (TS-17)
    17: 18, # 예약내역 (TS-18)
    21: 19, # 충전하기 (TS-19)
    22: 20, # 충전 내역 (TS-20)
    23: 21, # 환불 (TS-21)
    24: 22, # 세금계산서 발행 (TS-22)
    25: 23, # 내 정보 수정 (TS-23)
    26: 24, # 비밀번호 변경 (TS-24)
    27: 25, # 발신번호 관리 (TS-25)
    28: 26, # 공지사항 (TS-26)
    29: 27, # 이벤트 (TS-27)
    30: 28, # FAQ (TS-28)
    31: 29, # 1:1문의 (TS-29)
}

# 섹션 제목 매핑
SECTION_TITLES = {
    1: "랜딩페이지",
    2: "로그인",
    3: "대시보드",
    4: "일반문자 발송",
    5: "광고문자 발송",
    6: "일반문자 템플릿",
    7: "광고문자 템플릿",
    8: "선거문자 발송",
    9: "선거문자 템플릿",
    10: "알림톡 발송",
    11: "브랜드 메시지 발송",
    12: "카카오톡 발신 프로필",
    13: "알림톡 템플릿",
    14: "브랜드 메시지 템플릿",
    15: "주소록 관리",
    16: "수신거부관리",
    17: "발송결과",
    18: "예약내역",
    19: "충전하기",
    20: "충전 내역",
    21: "환불",
    22: "세금계산서 발행",
    23: "내 정보 수정",
    24: "비밀번호 변경",
    25: "발신번호 관리",
    26: "공지사항",
    27: "이벤트",
    28: "FAQ",
    29: "1:1문의"
}

def reorganize_sections_and_testids(content):
    """섹션 번호와 테스트ID를 메뉴 순서에 맞춰 재정리"""
    lines = content.split('\n')
    new_lines = []
    current_section = None
    new_section_num = None
    
    for line in lines:
        # 섹션 헤더 찾기
        section_match = re.match(r'^## (\d+)\.\s+(.+)$', line)
        if section_match:
            old_section_num = int(section_match.group(1))
            section_title = section_match.group(2).strip()
            
            # 메뉴 순서 매핑 확인
            if old_section_num in MENU_ORDER_MAP:
                new_section_num = MENU_ORDER_MAP[old_section_num]
                if new_section_num:
                    new_title = SECTION_TITLES.get(new_section_num, section_title)
                    line = f"## {new_section_num}. {new_title}"
                    current_section = new_section_num
                else:
                    continue
            else:
                current_section = None
                new_section_num = None
        
        # 테스트ID 변경 (테이블 행에서)
        if current_section and new_section_num:
            # TS-XX-YYY 형식의 테스트ID 찾기
            test_id_pattern = r'\b(TS-)(\d+)(-\d+)\b'
            def replace_test_id(match):
                old_section = int(match.group(2))
                if old_section in MENU_ORDER_MAP:
                    new_sec = MENU_ORDER_MAP[old_section]
                    if new_sec:
                        return f"TS-{new_sec:02d}{match.group(3)}"
                return match.group(0)
            
            line = re.sub(test_id_pattern, replace_test_id, line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def add_missing_features_from_html(content):
    """HTML 파일 기반 누락된 기능 설명 추가"""
    
    # 섹션별로 처리
    fixes = {
        4: {  # 일반문자 발송
            'sms_bytes': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_bytes': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_limit': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_limit': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
        },
        5: {  # 광고문자 발송
            'sms_bytes': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_bytes': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_limit': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_limit': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시",
            'ad_prefix': "(광고) 옆 문구: 최대 20자까지 입력 가능, 필수 입력 항목, placeholder: '업체명/서비스명', 미입력 시 '(광고) 옆에 표시될 문구를 입력해주세요' 오류 메시지 표시"
        },
        6: {  # 일반문자 템플릿
            'template_name': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
        },
        7: {  # 광고문자 템플릿
            'template_name': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시",
            'ad_prefix': "(광고) 옆 문구: 최대 20자까지 입력 가능, 필수 입력 항목"
        },
        2: {  # 로그인
            'email_autocomplete': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출",
            'password_validation': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
        }
    }
    
    for section_num, fix_info in fixes.items():
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # SMS 선택 케이스
            if 'sms_bytes' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*SMS 선택', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['sms_bytes'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['sms_bytes']}"
                        else:
                            step_content = f"- {fix_info['sms_bytes']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # LMS 선택 케이스
            if 'lms_bytes' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*LMS 선택', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['lms_bytes'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['lms_bytes']}"
                        else:
                            step_content = f"- {fix_info['lms_bytes']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 제목 입력 케이스
            if 'title_limit' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['title_limit'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['title_limit']}"
                        else:
                            step_content = f"- {fix_info['title_limit']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 이름/변수 입력 케이스
            if 'name_limit' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['name_limit'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['name_limit']}"
                        else:
                            step_content = f"- {fix_info['name_limit']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 템플릿명 입력 케이스
            if 'template_name' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*템플릿명', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['template_name'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['template_name']}"
                        else:
                            step_content = f"- {fix_info['template_name']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # (광고) 옆 문구 입력 케이스
            if 'ad_prefix' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*\(광고\).*옆.*문구', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['ad_prefix'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['ad_prefix']}"
                        else:
                            step_content = f"- {fix_info['ad_prefix']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 이메일 자동완성 케이스
            if 'email_autocomplete' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['email_autocomplete'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['email_autocomplete']}"
                        else:
                            step_content = f"- {fix_info['email_autocomplete']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 비밀번호 조건 케이스
            if 'password_validation' in fix_info and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if fix_info['password_validation'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {fix_info['password_validation']}"
                        else:
                            step_content = f"- {fix_info['password_validation']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def consolidate_similar_cases(content):
    """같은 영역의 세분화된 항목 통합"""
    
    # 이메일 입력 관련 통합
    for section_num in [2, 29]:
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 이메일 입력 관련 연속 케이스 (3개 이상)
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', line):
                email_cases = [line]
                j = i + 1
                
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', lines[j]):
                    email_cases.append(lines[j])
                    j += 1
                
                if len(email_cases) >= 3:
                    base_parts = email_cases[0].split('|')
                    if len(base_parts) >= 6:
                        all_steps = []
                        for case in email_cases:
                            case_parts = case.split('|')
                            if len(case_parts) >= 6:
                                step = case_parts[5].strip()
                                if step and step not in all_steps:
                                    all_steps.append(step)
                        
                        if all_steps:
                            base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                            if len(base_parts) >= 4:
                                base_parts[3] = ' 이메일 입력 (아이디, 도메인 선택/직접입력) '
                            new_lines.append('|'.join(base_parts))
                            i = j
                            continue
            
            new_lines.append(line)
            i += 1
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def replace_developer_terms(content):
    """개발자 용어를 한글 용어로 변경"""
    replacements = {
        r'\bAPI\b': '연동',
        r'\bURL\b': '주소',
        r'\bPOST\b': '전송',
        r'\bGET\b': '조회',
        r'\bmodal\b': '팝업',
        r'\bModal\b': '팝업',
        r'\balert\b': '알림',
        r'\bAlert\b': '알림',
        r'\btoast\b': '알림',
        r'\bToast\b': '알림',
        r'\bvalidation\b': '검증',
        r'\bValidation\b': '검증',
        r'\binput\b': '입력',
        r'\bInput\b': '입력',
        r'\btextarea\b': '입력',
        r'\bTextarea\b': '입력',
        r'\bselect\b': '선택',
        r'\bSelect\b': '선택',
        r'\bbutton\b': '버튼',
        r'\bButton\b': '버튼',
        r'\bcheckbox\b': '체크박스',
        r'\bCheckbox\b': '체크박스',
        r'\bradio\b': '선택',
        r'\bRadio\b': '선택',
        r'\bdropdown\b': '드롭다운',
        r'\bDropdown\b': '드롭다운',
        r'\bhover\b': '마우스 올리기',
        r'\bHover\b': '마우스 올리기',
        r'\bclick\b': '클릭',
        r'\bClick\b': '클릭',
        r'\bfocus\b': '선택',
        r'\bFocus\b': '선택',
        r'\bdisabled\b': '비활성화',
        r'\bDisabled\b': '비활성화',
        r'\benabled\b': '활성화',
        r'\bEnabled\b': '활성화',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_qa_fix'
    
    print("=" * 80)
    print("QA 직원 관점 종합 테스트 시나리오 개선")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 섹션 번호 및 테스트ID 재정리
    print("\n[1] 메뉴 순서에 맞춰 섹션 번호 및 테스트ID 재정리 중...")
    content = reorganize_sections_and_testids(content)
    
    # 2. HTML 파일 기반 누락 기능 설명 추가
    print("[2] HTML 파일 기반 누락 기능 설명 추가 중...")
    content = add_missing_features_from_html(content)
    
    # 3. 같은 영역 통합
    print("[3] 같은 영역의 세분화된 항목 통합 중...")
    content = consolidate_similar_cases(content)
    
    # 4. 개발자 용어 제거 및 한글 용어로 통일
    print("[4] 개발자 용어 제거 및 한글 용어로 통일 중...")
    content = replace_developer_terms(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
