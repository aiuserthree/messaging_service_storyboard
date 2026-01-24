#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서들을 기반으로 FO_테스트시나리오_상세.md 파일을 종합적으로 수정:
1. 누락된 기능 설명 추가 (글자수 제한 포함)
2. 중복 테스트 ID 제거 및 수정
3. 같은 영역의 세분화된 항목 통합
"""

import re
import os

def read_file(filepath):
    """파일 읽기"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def write_file(filepath, content):
    """파일 쓰기"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def fix_duplicate_test_ids(content):
    """중복된 테스트 ID 수정"""
    lines = content.split('\n')
    new_lines = []
    test_id_counter = {}  # 섹션별 테스트 ID 카운터
    current_section = None
    
    for i, line in enumerate(lines):
        # 섹션 헤더 확인
        section_match = re.match(r'^## (\d+)\.\s+(.+)$', line)
        if section_match:
            current_section = int(section_match.group(1))
            test_id_counter[current_section] = {}
            new_lines.append(line)
            continue
        
        # 테이블 행 확인
        table_match = re.match(r'^\|\s*(\d+)\s*\|\s*(TS-\d+-\d+)\s*\|', line)
        if table_match and current_section:
            seq_num = int(table_match.group(1))
            test_id = table_match.group(2)
            
            # 섹션 번호 추출
            section_from_id = int(test_id.split('-')[1])
            
            # 섹션 번호가 일치하지 않으면 수정
            if section_from_id != current_section:
                # 올바른 테스트 ID로 변경
                new_test_id = f"TS-{current_section:02d}-{test_id.split('-')[2]}"
                line = line.replace(test_id, new_test_id)
                test_id = new_test_id
            
            # 중복 체크
            if test_id in test_id_counter[current_section]:
                # 중복된 경우 순번 증가
                test_id_counter[current_section][test_id] += 1
                # 테스트 ID의 마지막 번호 증가
                parts = test_id.split('-')
                if len(parts) == 3:
                    try:
                        last_num = int(parts[2])
                        new_last_num = last_num + test_id_counter[current_section][test_id] - 1
                        new_test_id = f"{parts[0]}-{parts[1]}-{new_last_num:03d}"
                        line = re.sub(rf'\b{re.escape(test_id)}\b', new_test_id, line)
                    except ValueError:
                        pass
            else:
                test_id_counter[current_section][test_id] = 1
            
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def add_email_autocomplete_to_section(content, section_num):
    """섹션에 이메일 자동완성 설명 추가"""
    # 섹션 찾기
    pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not match:
        return content
    
    section = match.group(1)
    
    # 이미 포함되어 있는지 확인
    if '7개' in section and ('naver.com' in section or '도메인' in section):
        return content
    
    # 아이디 입력 관련 케이스 찾기
    lines = section.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # 아이디 입력 관련 테스트 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력', line):
            # 다음 줄이 테이블 행이 아니면 설명 추가
            if i + 1 < len(lines) and not re.match(r'^\|\s*\d+\s*\|', lines[i + 1]):
                # 단계별 작업 수행내용에 이메일 자동완성 추가
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '7개' not in step_content and '도메인' not in step_content:
                        email_desc = "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net)"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {email_desc}"
                        else:
                            step_content = f"- {email_desc}"
                        parts[5] = f' {step_content} '
                        new_lines[-1] = '|'.join(parts)
    
    new_section = '\n'.join(new_lines)
    return content.replace(section, new_section)

def add_password_validation_to_section(content, section_num):
    """섹션에 비밀번호 조건 설명 추가"""
    pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not match:
        return content
    
    section = match.group(1)
    
    # 이미 포함되어 있는지 확인
    if '8~20자' in section or '8-20자' in section:
        if '영문' in section and '숫자' in section and '특수문자' in section:
            return content
    
    lines = section.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # 비밀번호 입력 관련 테스트 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '8~20자' not in step_content and '8-20자' not in step_content:
                    password_desc = "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {password_desc}"
                    else:
                        step_content = f"- {password_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
    
    new_section = '\n'.join(new_lines)
    return content.replace(section, new_section)

def add_message_bytes_to_section(content, section_num):
    """섹션에 메시지 바이트 제한 설명 추가"""
    pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not match:
        return content
    
    section = match.group(1)
    
    # 이미 포함되어 있는지 확인
    if '90바이트' in section and '2000바이트' in section:
        return content
    
    lines = section.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # SMS 선택 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*SMS 선택', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '90바이트' not in step_content:
                    bytes_desc = "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
        
        # LMS 선택 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*LMS 선택', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '2000바이트' not in step_content:
                    bytes_desc = "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
        
        # 제목 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '40자' not in step_content:
                    title_desc = "제목 입력: 최대 40자까지 입력 가능"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {title_desc}"
                    else:
                        step_content = f"- {title_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
        
        # 이름/변수 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '100바이트' not in step_content:
                    limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자)"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
    
    new_section = '\n'.join(new_lines)
    return content.replace(section, new_section)

def add_template_name_limit_to_section(content, section_num):
    """섹션에 템플릿명 제한 설명 추가"""
    pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not match:
        return content
    
    section = match.group(1)
    
    # 이미 포함되어 있는지 확인
    if '50바이트' in section:
        return content
    
    lines = section.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # 템플릿명 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*템플릿명', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '50바이트' not in step_content:
                    limit_desc = "템플릿명 입력: 최대 50바이트까지 입력 가능"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    new_lines[-1] = '|'.join(parts)
    
    new_section = '\n'.join(new_lines)
    return content.replace(section, new_section)

def remove_wrong_test_id_line(content):
    """잘못된 테스트 ID 라인 제거"""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # 라인 177: TS-03-014가 섹션 5에 있는 경우 제거
        if i == 176:  # 0-based index
            if 'TS-03-014' in line and '수신번호 목록 테이블 구조 확인' in line:
                # 이 라인은 섹션 5에 있으므로 TS-05로 시작해야 함
                # 중복이므로 제거
                continue
        
        # 라인 301: TS-05-014가 섹션 6에 중복으로 있는 경우 제거
        if i == 300:  # 0-based index
            if 'TS-05-014' in line and '수신번호 목록 테이블 구조 확인' in line:
                # 이미 섹션 5에 있으므로 제거
                continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def consolidate_table_edit_cases(content, section_num):
    """테이블 직접 편집 관련 케이스 통합"""
    pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not match:
        return content
    
    section = match.group(1)
    lines = section.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 테이블 직접 편집 관련 연속 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', line):
            edit_cases = [line]
            j = i + 1
            
            # 연속된 편집 케이스 수집
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', lines[j]):
                edit_cases.append(lines[j])
                j += 1
            
            # 3개 이상이면 통합
            if len(edit_cases) >= 3:
                # 첫 번째 케이스를 기준으로 통합
                base_parts = edit_cases[0].split('|')
                if len(base_parts) >= 6:
                    # 모든 케이스의 단계별 작업 수행내용 통합
                    all_steps = []
                    for case in edit_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            if step and step not in all_steps:
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        # 테스트케이스명도 통합
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 테이블 직접 편집 (이름, 전화번호, 추가 정보 1/2/3) '
                    
                    new_lines.append('|'.join(base_parts))
                    i = j
                    continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    return content.replace(section, new_section)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 종합 개선 작업")
    print("=" * 80)
    
    # 파일 읽기
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    # 백업 생성
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 잘못된 테스트 ID 라인 제거
    print("\n[1] 잘못된 테스트 ID 라인 제거 중...")
    content = remove_wrong_test_id_line(content)
    
    # 2. 중복 테스트 ID 수정
    print("[2] 중복 테스트 ID 수정 중...")
    content = fix_duplicate_test_ids(content)
    
    # 3. 이메일 자동완성 설명 추가
    print("[3] 이메일 자동완성 설명 추가 중...")
    for section_num in [2, 3, 20]:
        content = add_email_autocomplete_to_section(content, section_num)
    
    # 4. 비밀번호 조건 설명 추가
    print("[4] 비밀번호 조건 설명 추가 중...")
    for section_num in [2, 3, 20]:
        content = add_password_validation_to_section(content, section_num)
    
    # 5. 메시지 바이트 제한 설명 추가
    print("[5] 메시지 바이트 제한 설명 추가 중...")
    for section_num in [5, 6]:
        content = add_message_bytes_to_section(content, section_num)
    
    # 6. 템플릿명 제한 설명 추가
    print("[6] 템플릿명 제한 설명 추가 중...")
    for section_num in [7, 8]:
        content = add_template_name_limit_to_section(content, section_num)
    
    # 7. 테이블 직접 편집 케이스 통합
    print("[7] 테이블 직접 편집 케이스 통합 중...")
    for section_num in [5, 6]:
        content = consolidate_table_edit_cases(content, section_num)
    
    # 변경사항 저장
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
