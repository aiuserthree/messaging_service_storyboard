#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA 직원 관점 최종 종합 개선:
1. 참고 문서(01-20.md) 기반 정합성 체크 및 누락 기능 설명 추가
2. HTML 파일 기반 기능 설명 확인 및 반영 (글자수 제한 포함)
3. 같은 영역의 세분화된 항목 통합 및 간소화
4. 개발자 용어 제거 및 한글 용어로 통일
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

def add_email_autocomplete_from_reference(content, section_num):
    """참고 문서 기반 이메일 자동완성 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # 아이디 입력 - 정상 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력.*정상 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '7개' not in step_content or 'naver.com' not in step_content:
                    email_desc = "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출, 지원도메인 선택 시 알림 노출되지 않도록 처리"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {email_desc}"
                    else:
                        step_content = f"- {email_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_password_validation_from_reference(content, section_num):
    """참고 문서 기반 비밀번호 조건 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # 비밀번호 입력 - 정상 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력.*정상 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '8~20자' not in step_content and '8-20자' not in step_content:
                    password_desc = "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내), 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 알림 메시지 노출, 20자 이상 입력불가"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {password_desc}"
                    else:
                        step_content = f"- {password_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_message_bytes_from_html(content, section_num):
    """HTML 파일 기반 메시지 바이트 제한 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # SMS 선택 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*SMS 선택', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '90바이트' not in step_content or '한글 약 30자' not in step_content:
                    bytes_desc = "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        # LMS 선택 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*LMS 선택', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '2000바이트' not in step_content or '한글 약 666자' not in step_content:
                    bytes_desc = "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        # 제목 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '40자' not in step_content:
                    title_desc = "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {title_desc}"
                    else:
                        step_content = f"- {title_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        # 이름/변수 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '100바이트' not in step_content:
                    limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        # (광고) 옆 문구 입력 케이스 (섹션 5)
        if section_num == 5 and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*\(광고\).*옆.*문구', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '20자' not in step_content:
                    ad_desc = "(광고) 옆 문구: 최대 20자까지 입력 가능, 필수 입력 항목, placeholder: '업체명/서비스명', 미입력 시 '(광고) 옆에 표시될 문구를 입력해주세요' 오류 메시지 표시"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {ad_desc}"
                    else:
                        step_content = f"- {ad_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        # 템플릿명 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*템플릿명', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '50바이트' not in step_content:
                    template_desc = "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {template_desc}"
                    else:
                        step_content = f"- {template_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def consolidate_table_edit_cases(content, section_num):
    """테이블 직접 편집 관련 케이스 통합"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 테이블 직접 편집 관련 연속 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', line):
            edit_cases = [line]
            j = i + 1
            
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', lines[j]):
                edit_cases.append(lines[j])
                j += 1
            
            # 3개 이상이면 통합
            if len(edit_cases) >= 3:
                base_parts = edit_cases[0].split('|')
                if len(base_parts) >= 6:
                    all_steps = []
                    for case in edit_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            if step and step not in all_steps:
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 테이블 직접 편집 (이름, 전화번호, 추가 정보 1/2/3) '
                        new_lines.append('|'.join(base_parts))
                        i = j
                        continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def consolidate_email_input_cases(content, section_num):
    """이메일 입력 관련 케이스 통합"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
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

def consolidate_inquiry_type_cases(content):
    """문의유형 선택 관련 케이스 통합"""
    section_pattern = r'(^## 29\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 문의유형 선택 관련 연속 케이스 (3개 이상)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-29-\d+\s*\|\s*\d+\s*\|\s*문의유형', line):
            type_cases = [line]
            j = i + 1
            
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-29-\d+\s*\|\s*\d+\s*\|\s*문의유형', lines[j]):
                type_cases.append(lines[j])
                j += 1
            
            if len(type_cases) >= 3:
                base_parts = type_cases[0].split('|')
                if len(base_parts) >= 6:
                    all_steps = []
                    for case in type_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            if step and step not in all_steps:
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 문의유형 선택 (가격문의/서비스문의/기술문의/기타) '
                        new_lines.append('|'.join(base_parts))
                        i = j
                        continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def replace_developer_terms_with_korean(content):
    """개발자 용어를 한글 용어로 변경"""
    replacements = [
        (r'\bAPI\b', '연동'),
        (r'\bURL\b', '주소'),
        (r'\bPOST\b', '전송'),
        (r'\bGET\b', '조회'),
        (r'\bmodal\b', '팝업'),
        (r'\bModal\b', '팝업'),
        (r'\balert\b', '알림'),
        (r'\bAlert\b', '알림'),
        (r'\btoast\b', '알림'),
        (r'\bToast\b', '알림'),
        (r'\bvalidation\b', '검증'),
        (r'\bValidation\b', '검증'),
        (r'\binput\b', '입력'),
        (r'\bInput\b', '입력'),
        (r'\btextarea\b', '입력'),
        (r'\bTextarea\b', '입력'),
        (r'\bselect\b', '선택'),
        (r'\bSelect\b', '선택'),
        (r'\bbutton\b', '버튼'),
        (r'\bButton\b', '버튼'),
        (r'\bcheckbox\b', '체크박스'),
        (r'\bCheckbox\b', '체크박스'),
        (r'\bradio\b', '선택'),
        (r'\bRadio\b', '선택'),
        (r'\bdropdown\b', '드롭다운'),
        (r'\bDropdown\b', '드롭다운'),
        (r'\bhover\b', '마우스 올리기'),
        (r'\bHover\b', '마우스 올리기'),
        (r'\bclick\b', '클릭'),
        (r'\bClick\b', '클릭'),
        (r'\bfocus\b', '선택'),
        (r'\bFocus\b', '선택'),
        (r'\bdisabled\b', '비활성화'),
        (r'\bDisabled\b', '비활성화'),
        (r'\benabled\b', '활성화'),
        (r'\bEnabled\b', '활성화'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final_qa'
    
    print("=" * 80)
    print("QA 직원 관점 최종 종합 개선")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 참고 문서 기반 이메일 자동완성 설명 추가
    print("\n[1] 참고 문서 기반 이메일 자동완성 설명 추가 중...")
    for section_num in [2]:
        content = add_email_autocomplete_from_reference(content, section_num)
    
    # 2. 참고 문서 기반 비밀번호 조건 설명 추가
    print("[2] 참고 문서 기반 비밀번호 조건 설명 추가 중...")
    for section_num in [2]:
        content = add_password_validation_from_reference(content, section_num)
    
    # 3. HTML 파일 기반 메시지 바이트 제한 설명 추가
    print("[3] HTML 파일 기반 메시지 바이트 제한 설명 추가 중...")
    for section_num in [4, 5]:
        content = add_message_bytes_from_html(content, section_num)
    
    # 4. 템플릿명 제한 설명 추가
    print("[4] 템플릿명 제한 설명 추가 중...")
    for section_num in [6, 7]:
        content = add_message_bytes_from_html(content, section_num)
    
    # 5. 테이블 직접 편집 케이스 통합
    print("[5] 테이블 직접 편집 케이스 통합 중...")
    for section_num in [4, 5]:
        content = consolidate_table_edit_cases(content, section_num)
    
    # 6. 이메일 입력 케이스 통합
    print("[6] 이메일 입력 케이스 통합 중...")
    for section_num in [2, 29]:
        content = consolidate_email_input_cases(content, section_num)
    
    # 7. 문의유형 선택 케이스 통합
    print("[7] 문의유형 선택 케이스 통합 중...")
    content = consolidate_inquiry_type_cases(content)
    
    # 8. 개발자 용어 제거 및 한글 용어로 통일
    print("[8] 개발자 용어 제거 및 한글 용어로 통일 중...")
    content = replace_developer_terms_with_korean(content)
    
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
