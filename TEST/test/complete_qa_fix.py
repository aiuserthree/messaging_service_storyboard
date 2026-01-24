#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA 직원 관점 최종 완성 작업:
1. 테이블 직접 편집 케이스 통합
2. 참고 문서 기반 누락 기능 설명 추가
3. HTML 파일 기반 기능 설명 확인 및 반영
4. 같은 영역 통합
5. 개발자 용어 제거 및 한글 용어로 통일
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

def consolidate_table_edit_cases_accurate(content, section_num):
    """테이블 직접 편집 관련 케이스 정확하게 통합"""
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
            case_indices = [i]
            j = i + 1
            
            # 연속된 편집 케이스 수집 (최대 5개까지)
            while j < len(lines) and len(edit_cases) < 5:
                if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', lines[j]):
                    edit_cases.append(lines[j])
                    case_indices.append(j)
                    j += 1
                else:
                    break
            
            # 3개 이상이면 통합
            if len(edit_cases) >= 3:
                base_parts = edit_cases[0].split('|')
                if len(base_parts) >= 6:
                    all_steps = []
                    step_set = set()
                    
                    for case in edit_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            # 중복 제거를 위해 정규화
                            step_normalized = re.sub(r'\s+', ' ', step)
                            if step_normalized and step_normalized not in step_set:
                                step_set.add(step_normalized)
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 테이블 직접 편집 (이름, 전화번호, 추가 정보 1/2/3) '
                        # 순번은 첫 번째 것 유지
                        new_lines.append('|'.join(base_parts))
                        i = j
                        continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_name_variable_limit_to_cases(content, section_num):
    """이름/변수 입력 케이스에 100바이트 제한 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # 이름/변수 입력 케이스 (100바이트 제한이 없는 경우)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                # 100바이트 제한이 없고, 바이트 제한 관련 내용이 없는 경우에만 추가
                if '100바이트' not in step_content and '바이트 제한' not in step_content and '글자수' not in step_content:
                    limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_title_limit_to_cases(content, section_num):
    """제목 입력 케이스에 40자 제한 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # 제목 입력 케이스 (40자 제한이 없는 경우)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '40자' not in step_content:
                    title_desc = "제목 입력: 최대 40자까지 입력 가능, 안내 문구: '제목을 입력하세요 (최대 40자)'"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {title_desc}"
                    else:
                        step_content = f"- {title_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_ad_prefix_limit_to_cases(content, section_num):
    """(광고) 옆 문구 입력 케이스에 20자 제한 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
        # (광고) 옆 문구 입력 케이스
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*\(광고\).*옆.*문구', line):
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                if '20자' not in step_content:
                    ad_desc = "(광고) 옆 문구: 최대 20자까지 입력 가능, 필수 입력 항목, 안내 문구: '업체명/서비스명', 미입력 시 '(광고) 옆에 표시될 문구를 입력해주세요' 오류 메시지 표시"
                    if step_content:
                        if not step_content.startswith('-'):
                            step_content = f"- {step_content}"
                        step_content = f"{step_content}<br>- {ad_desc}"
                    else:
                        step_content = f"- {ad_desc}"
                    parts[5] = f' {step_content} '
                    line = '|'.join(parts)
        
        new_lines.append(line)
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_template_name_limit_to_cases(content, section_num):
    """템플릿명 입력 케이스에 50바이트 제한 설명 추가"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    
    for line in lines:
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

def add_password_validation_to_cases(content, section_num):
    """비밀번호 입력 케이스에 조건 설명 추가"""
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

def consolidate_email_input_cases_accurate(content, section_num):
    """이메일 입력 관련 케이스 정확하게 통합"""
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
                    step_set = set()
                    
                    for case in email_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            step_normalized = re.sub(r'\s+', ' ', step)
                            if step_normalized and step_normalized not in step_set:
                                step_set.add(step_normalized)
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

def consolidate_inquiry_type_cases_accurate(content):
    """문의유형 선택 관련 케이스 정확하게 통합"""
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
                    step_set = set()
                    
                    for case in type_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            step_normalized = re.sub(r'\s+', ' ', step)
                            if step_normalized and step_normalized not in step_set:
                                step_set.add(step_normalized)
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

def replace_developer_terms_korean(content):
    """개발자 용어를 한글 용어로 변경 (더 정확하게)"""
    # 테이블 행 내에서만 변경 (섹션 헤더나 다른 부분은 제외)
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # 테이블 행인 경우에만 용어 변경
        if re.match(r'^\|', line):
            # API -> 연동
            line = re.sub(r'\bAPI\b', '연동', line, flags=re.IGNORECASE)
            # URL -> 주소
            line = re.sub(r'\bURL\b', '주소', line, flags=re.IGNORECASE)
            # modal -> 팝업
            line = re.sub(r'\bmodal\b', '팝업', line, flags=re.IGNORECASE)
            # alert -> 알림
            line = re.sub(r'\balert\b', '알림', line, flags=re.IGNORECASE)
            # toast -> 알림
            line = re.sub(r'\btoast\b', '알림', line, flags=re.IGNORECASE)
            # validation -> 검증
            line = re.sub(r'\bvalidation\b', '검증', line, flags=re.IGNORECASE)
            # input -> 입력
            line = re.sub(r'\binput\b', '입력', line, flags=re.IGNORECASE)
            # textarea -> 입력
            line = re.sub(r'\btextarea\b', '입력', line, flags=re.IGNORECASE)
            # select -> 선택
            line = re.sub(r'\bselect\b', '선택', line, flags=re.IGNORECASE)
            # button -> 버튼
            line = re.sub(r'\bbutton\b', '버튼', line, flags=re.IGNORECASE)
            # checkbox -> 체크박스
            line = re.sub(r'\bcheckbox\b', '체크박스', line, flags=re.IGNORECASE)
            # radio -> 선택
            line = re.sub(r'\bradio\b', '선택', line, flags=re.IGNORECASE)
            # dropdown -> 드롭다운
            line = re.sub(r'\bdropdown\b', '드롭다운', line, flags=re.IGNORECASE)
            # hover -> 마우스 올리기
            line = re.sub(r'\bhover\b', '마우스 올리기', line, flags=re.IGNORECASE)
            # click -> 클릭
            line = re.sub(r'\bclick\b', '클릭', line, flags=re.IGNORECASE)
            # focus -> 선택
            line = re.sub(r'\bfocus\b', '선택', line, flags=re.IGNORECASE)
            # disabled -> 비활성화
            line = re.sub(r'\bdisabled\b', '비활성화', line, flags=re.IGNORECASE)
            # enabled -> 활성화
            line = re.sub(r'\benabled\b', '활성화', line, flags=re.IGNORECASE)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_complete_qa'
    
    print("=" * 80)
    print("QA 직원 관점 최종 완성 작업")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 테이블 직접 편집 케이스 통합
    print("\n[1] 테이블 직접 편집 케이스 통합 중...")
    for section_num in [4, 5, 8]:
        content = consolidate_table_edit_cases_accurate(content, section_num)
    
    # 2. 이름/변수 100바이트 제한 설명 추가
    print("[2] 이름/변수 100바이트 제한 설명 추가 중...")
    for section_num in [4, 5, 8]:
        content = add_name_variable_limit_to_cases(content, section_num)
    
    # 3. 제목 40자 제한 설명 추가
    print("[3] 제목 40자 제한 설명 추가 중...")
    for section_num in [4, 5, 8]:
        content = add_title_limit_to_cases(content, section_num)
    
    # 4. (광고) 옆 문구 20자 제한 설명 추가
    print("[4] (광고) 옆 문구 20자 제한 설명 추가 중...")
    for section_num in [5, 7]:
        content = add_ad_prefix_limit_to_cases(content, section_num)
    
    # 5. 템플릿명 50바이트 제한 설명 추가
    print("[5] 템플릿명 50바이트 제한 설명 추가 중...")
    for section_num in [6, 7]:
        content = add_template_name_limit_to_cases(content, section_num)
    
    # 6. 비밀번호 조건 설명 추가
    print("[6] 비밀번호 조건 설명 추가 중...")
    for section_num in [2]:
        content = add_password_validation_to_cases(content, section_num)
    
    # 7. 이메일 입력 케이스 통합
    print("[7] 이메일 입력 케이스 통합 중...")
    for section_num in [2, 29]:
        content = consolidate_email_input_cases_accurate(content, section_num)
    
    # 8. 문의유형 선택 케이스 통합
    print("[8] 문의유형 선택 케이스 통합 중...")
    content = consolidate_inquiry_type_cases_accurate(content)
    
    # 9. 개발자 용어 제거 및 한글 용어로 통일
    print("[9] 개발자 용어 제거 및 한글 용어로 통일 중...")
    content = replace_developer_terms_korean(content)
    
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
