#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서 기반 최종 보완:
1. 누락된 기능 설명 추가 (참고 문서 01-20.md 기반)
2. 같은 영역의 세분화된 항목 통합
"""

import re

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

def add_email_autocomplete_to_line(line, section_num):
    """이메일 자동완성 설명을 라인에 추가"""
    if '이메일' not in line and '아이디 입력' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    # 이미 포함되어 있는지 확인
    if '7개' in step_content and 'naver.com' in step_content:
        return line
    
    # 추가할 설명
    email_desc = "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {email_desc}"
    else:
        step_content = f"- {email_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def add_password_validation_to_line(line, section_num):
    """비밀번호 조건 설명을 라인에 추가"""
    if '비밀번호 입력' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    # 이미 포함되어 있는지 확인
    if '8~20자' in step_content or '8-20자' in step_content:
        if '영문' in step_content and '숫자' in step_content:
            return line
    
    # 추가할 설명
    password_desc = "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {password_desc}"
    else:
        step_content = f"- {password_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def add_message_bytes_to_line(line, section_num, message_type):
    """메시지 바이트 제한 설명을 라인에 추가"""
    if message_type == 'SMS' and 'SMS 선택' not in line:
        return line
    if message_type == 'LMS' and 'LMS 선택' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    if message_type == 'SMS':
        if '90바이트' in step_content and '한글 약 30자' in step_content:
            return line
        bytes_desc = "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환"
    else:  # LMS
        if '2000바이트' in step_content and '한글 약 666자' in step_content:
            return line
        bytes_desc = "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {bytes_desc}"
    else:
        step_content = f"- {bytes_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def add_title_limit_to_line(line, section_num):
    """제목 40자 제한 설명을 라인에 추가"""
    if '제목 입력' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    if '40자' in step_content:
        return line
    
    title_desc = "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {title_desc}"
    else:
        step_content = f"- {title_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def add_name_variable_limit_to_line(line, section_num):
    """이름/변수 100바이트 제한 설명을 라인에 추가"""
    if '이름' not in line and '변수' not in line and '추가 정보' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    if '100바이트' in step_content:
        return line
    
    limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {limit_desc}"
    else:
        step_content = f"- {limit_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def add_template_name_limit_to_line(line, section_num):
    """템플릿명 50바이트 제한 설명을 라인에 추가"""
    if '템플릿명' not in line:
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    step_content = parts[5].strip()
    
    if '50바이트' in step_content:
        return line
    
    limit_desc = "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
    
    if step_content:
        if not step_content.startswith('-'):
            step_content = f"- {step_content}"
        step_content = f"{step_content}<br>- {limit_desc}"
    else:
        step_content = f"- {limit_desc}"
    
    parts[5] = f' {step_content} '
    return '|'.join(parts)

def process_section(content, section_num):
    """섹션별로 누락된 기능 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # 섹션별로 적절한 설명 추가
        if section_num in [2, 3, 20]:
            # 이메일 자동완성
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력.*정상 입력', line):
                line = add_email_autocomplete_to_line(line, section_num)
            # 비밀번호 조건
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력.*정상 입력', line):
                line = add_password_validation_to_line(line, section_num)
        
        if section_num in [5, 6]:
            # SMS/LMS 바이트 제한
            if re.match(r'^\|\s*\d+\s*\|\s*TS-0[56]-\d+\s*\|\s*\d+\s*\|\s*SMS 선택', line):
                line = add_message_bytes_to_line(line, section_num, 'SMS')
            if re.match(r'^\|\s*\d+\s*\|\s*TS-0[56]-\d+\s*\|\s*\d+\s*\|\s*LMS 선택', line):
                line = add_message_bytes_to_line(line, section_num, 'LMS')
            # 제목 40자 제한
            if re.match(r'^\|\s*\d+\s*\|\s*TS-0[56]-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
                line = add_title_limit_to_line(line, section_num)
            # 이름/변수 100바이트 제한
            if re.match(r'^\|\s*\d+\s*\|\s*TS-0[56]-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
                line = add_name_variable_limit_to_line(line, section_num)
        
        if section_num in [7, 8]:
            # 템플릿명 50바이트 제한
            if re.match(r'^\|\s*\d+\s*\|\s*TS-0[78]-\d+\s*\|\s*\d+\s*\|\s*템플릿명', line):
                line = add_template_name_limit_to_line(line, section_num)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def consolidate_email_cases(content, section_num):
    """이메일 입력 관련 세분화된 케이스 통합"""
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

def consolidate_inquiry_type_cases_final(content):
    """문의유형 선택 관련 세분화된 케이스 통합"""
    section_pattern = r'(^## 31\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^---|$)'
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
        if re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', line):
            type_cases = [line]
            j = i + 1
            
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', lines[j]):
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

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup6'
    
    print("=" * 80)
    print("참고 문서 기반 최종 보완")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 섹션별로 누락된 기능 설명 추가
    print("\n[1] 누락된 기능 설명 추가 중...")
    for section_num in [2, 3, 5, 6, 7, 8, 20]:
        content = process_section(content, section_num)
    
    # 같은 영역의 세분화된 항목 통합
    print("[2] 같은 영역의 세분화된 항목 통합 중...")
    for section_num in [2, 3, 20, 31]:
        content = consolidate_email_cases(content, section_num)
    
    content = consolidate_inquiry_type_cases_final(content)
    
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
