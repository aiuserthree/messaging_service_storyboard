#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서들을 기반으로 FO_테스트시나리오_상세.md 파일을 수정:
1. 누락된 기능 설명 추가 (글자수 제한 포함)
2. 중복 테스트 ID 제거
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

def fix_email_autocomplete(content, section_num):
    """이메일 자동완성 7개 도메인 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '7개' in section_content and 'naver.com' in section_content:
        return content
    
    # 아이디 입력 관련 테스트 케이스 찾기
    pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_email_info(match):
        line = match.group(1)
        # 단계별 작업 수행내용에 이메일 자동완성 설명 추가
        if '- 정상 입력' in line or '- 이메일 입력' in line:
            # 이미 포함되어 있지 않은 경우에만 추가
            if '7개' not in line and '도메인' not in line:
                # 단계별 작업 수행내용 부분 찾기
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if step_content and not step_content.startswith('-'):
                        step_content = f"- {step_content}"
                    # 이메일 자동완성 설명 추가
                    email_desc = "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net)"
                    if email_desc not in step_content:
                        if step_content:
                            step_content = f"{step_content}<br>- {email_desc}"
                        else:
                            step_content = f"- {email_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(pattern, add_email_info, section_content)
    content = content.replace(section_content, new_section)
    
    return content

def fix_password_validation(content, section_num):
    """비밀번호 조건 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '8~20자' in section_content or '8-20자' in section_content:
        if '영문' in section_content and '숫자' in section_content and '특수문자' in section_content:
            return content
    
    # 비밀번호 입력 관련 테스트 케이스 찾기
    pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_password_info(match):
        line = match.group(1)
        parts = line.split('|')
        if len(parts) >= 6:
            step_content = parts[5].strip()
            if '8~20자' not in step_content and '8-20자' not in step_content:
                password_desc = "비밀번호 입력 조건 확인: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)"
                if password_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {password_desc}"
                    else:
                        step_content = f"- {password_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(pattern, add_password_info, section_content)
    content = content.replace(section_content, new_section)
    
    return content

def fix_message_bytes(content, section_num):
    """메시지 바이트 제한 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '90바이트' in section_content and '2000바이트' in section_content:
        return content
    
    # SMS/LMS 선택 관련 테스트 케이스 찾기
    # SMS 선택 케이스에 바이트 제한 설명 추가
    sms_pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_sms_bytes(match):
        line = match.group(1)
        if '90바이트' not in line:
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                bytes_desc = "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트"
                if bytes_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    # LMS 선택 케이스에 바이트 제한 설명 추가
    lms_pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_lms_bytes(match):
        line = match.group(1)
        if '2000바이트' not in line:
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                bytes_desc = "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트"
                if bytes_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {bytes_desc}"
                    else:
                        step_content = f"- {bytes_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(sms_pattern, add_sms_bytes, section_content)
    new_section = re.sub(lms_pattern, add_lms_bytes, new_section)
    content = content.replace(section_content, new_section)
    
    return content

def fix_title_limit(content, section_num):
    """제목 40자 제한 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '40자' in section_content:
        return content
    
    # 제목 입력 관련 테스트 케이스 찾기
    pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_title_limit(match):
        line = match.group(1)
        if '40자' not in line:
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                title_desc = "제목 입력: 최대 40자까지 입력 가능"
                if title_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {title_desc}"
                    else:
                        step_content = f"- {title_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(pattern, add_title_limit, section_content)
    content = content.replace(section_content, new_section)
    
    return content

def fix_name_variable_limit(content, section_num):
    """이름/변수 100바이트 제한 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '100바이트' in section_content:
        return content
    
    # 이름/변수 관련 테스트 케이스 찾기
    pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_name_limit(match):
        line = match.group(1)
        if '100바이트' not in line:
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자)"
                if limit_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(pattern, add_name_limit, section_content)
    content = content.replace(section_content, new_section)
    
    return content

def fix_template_name_limit(content, section_num):
    """템플릿명 50바이트 제한 설명 추가"""
    section_pattern = rf'^## {section_num}\.\s+(.+?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section_content = section_match.group(0)
    
    # 이미 포함되어 있는지 확인
    if '50바이트' in section_content:
        return content
    
    # 템플릿명 관련 테스트 케이스 찾기
    pattern = r'(\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*템플릿명[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)'
    
    def add_template_limit(match):
        line = match.group(1)
        if '50바이트' not in line:
            parts = line.split('|')
            if len(parts) >= 6:
                step_content = parts[5].strip()
                limit_desc = "템플릿명 입력: 최대 50바이트까지 입력 가능"
                if limit_desc not in step_content:
                    if step_content:
                        step_content = f"{step_content}<br>- {limit_desc}"
                    else:
                        step_content = f"- {limit_desc}"
                    parts[5] = f' {step_content} '
                    return '|'.join(parts)
        return line
    
    new_section = re.sub(pattern, add_template_limit, section_content)
    content = content.replace(section_content, new_section)
    
    return content

def remove_duplicate_test_ids(content):
    """중복된 테스트 ID 제거"""
    # 중복된 테스트 ID 찾기
    test_ids = {}
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        match = re.search(r'^\|\s*\d+\s*\|\s*(TS-\d+-\d+)\s*\|', line)
        if match:
            test_id = match.group(1)
            if test_id not in test_ids:
                test_ids[test_id] = []
            test_ids[test_id].append(i)
    
    # 중복된 항목 제거 (첫 번째 항목만 유지)
    duplicates_removed = []
    for test_id, line_nums in test_ids.items():
        if len(line_nums) > 1:
            # 첫 번째 항목은 유지, 나머지는 제거
            for line_num in line_nums[1:]:
                duplicates_removed.append((test_id, line_num))
                # 해당 라인 제거 (빈 줄도 함께 제거할 수 있음)
                if line_num < len(lines):
                    lines[line_num] = None
    
    # None인 라인 제거
    new_lines = [line for line in lines if line is not None]
    
    if duplicates_removed:
        print(f"\n중복 테스트 ID 제거: {len(duplicates_removed)}건")
        for test_id, line_num in duplicates_removed[:5]:  # 최대 5개만 표시
            print(f"  - {test_id} (라인 {line_num})")
    
    return '\n'.join(new_lines)

def consolidate_similar_cases(content):
    """같은 영역의 세분화된 항목들을 통합"""
    lines = content.split('\n')
    consolidated = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 테이블 행인 경우
        if re.match(r'^\|\s*\d+\s*\|', line):
            # 연속된 유사한 테스트 케이스 그룹 찾기
            similar_group = [line]
            j = i + 1
            
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|', lines[j]):
                next_line = lines[j]
                # 같은 기능 영역인지 확인
                if is_similar_case(line, next_line):
                    similar_group.append(next_line)
                    j += 1
                else:
                    break
            
            # 유사한 케이스가 3개 이상이고 같은 기능을 테스트하는 경우 통합
            if len(similar_group) >= 3 and should_consolidate(similar_group):
                consolidated_line = merge_similar_cases(similar_group)
                consolidated.append(consolidated_line)
                i = j
            else:
                consolidated.extend(similar_group)
                i = j
        else:
            consolidated.append(line)
            i += 1
    
    return '\n'.join(consolidated)

def is_similar_case(line1, line2):
    """두 테스트 케이스가 유사한지 확인"""
    # 테스트케이스명 추출
    pattern = r'\|[^|]+\|[^|]+\|[^|]+\|\s*([^|]+)\s*\|'
    match1 = re.search(pattern, line1)
    match2 = re.search(pattern, line2)
    
    if not match1 or not match2:
        return False
    
    case1 = match1.group(1).strip()
    case2 = match2.group(1).strip()
    
    # 키워드 기반 유사도 체크
    keywords1 = set(case1.split())
    keywords2 = set(case2.split())
    
    if len(keywords1) == 0 or len(keywords2) == 0:
        return False
    
    common = len(keywords1 & keywords2)
    similarity = common / max(len(keywords1), len(keywords2))
    
    return similarity > 0.5

def should_consolidate(cases):
    """통합해야 하는지 확인"""
    # 테스트케이스명 추출
    case_names = []
    for case in cases:
        pattern = r'\|[^|]+\|[^|]+\|[^|]+\|\s*([^|]+)\s*\|'
        match = re.search(pattern, case)
        if match:
            case_names.append(match.group(1).strip())
    
    # 같은 기능의 세부 케이스인지 확인
    if len(case_names) < 2:
        return False
    
    # 공통 키워드 확인
    first_keywords = set(case_names[0].split())
    for name in case_names[1:]:
        keywords = set(name.split())
        if len(first_keywords & keywords) < 2:  # 공통 키워드가 2개 미만이면 통합하지 않음
            return False
    
    return True

def merge_similar_cases(cases):
    """유사한 테스트 케이스들을 하나로 통합"""
    # 첫 번째 케이스를 기준으로 통합
    base_case = cases[0]
    parts = base_case.split('|')
    
    if len(parts) < 6:
        return base_case
    
    # 단계별 작업 수행내용 통합
    steps = []
    for case in cases:
        case_parts = case.split('|')
        if len(case_parts) >= 6:
            step = case_parts[5].strip()
            if step and step not in steps:
                # 중복 제거하면서 추가
                steps.append(step)
    
    # 통합된 케이스 생성
    if steps:
        parts[5] = ' ' + '<br>'.join(steps) + ' '
    
    # 순번은 첫 번째 것 유지, 테스트ID는 첫 번째 것 유지
    return '|'.join(parts)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 개선 작업")
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
    
    # 1. 이메일 자동완성 설명 추가
    print("\n[1] 이메일 자동완성 설명 추가 중...")
    for section_num in [2, 3, 20]:  # 회원가입, 로그인, PC 로그인
        content = fix_email_autocomplete(content, section_num)
    
    # 2. 비밀번호 조건 설명 추가
    print("[2] 비밀번호 조건 설명 추가 중...")
    for section_num in [2, 3, 20]:
        content = fix_password_validation(content, section_num)
    
    # 3. 메시지 바이트 제한 설명 추가
    print("[3] 메시지 바이트 제한 설명 추가 중...")
    for section_num in [5, 6]:  # 일반문자 발송, 광고문자 발송
        content = fix_message_bytes(content, section_num)
        content = fix_title_limit(content, section_num)
        content = fix_name_variable_limit(content, section_num)
    
    # 4. 템플릿명 제한 설명 추가
    print("[4] 템플릿명 제한 설명 추가 중...")
    for section_num in [7, 8]:  # 일반문자 템플릿, 광고문자 템플릿
        content = fix_template_name_limit(content, section_num)
    
    # 5. 중복 테스트 ID 제거
    print("[5] 중복 테스트 ID 제거 중...")
    content = remove_duplicate_test_ids(content)
    
    # 6. 유사 케이스 통합 (선택적)
    print("[6] 유사 케이스 통합 검토 중...")
    # 주의: 통합은 신중하게 수행해야 하므로 주석 처리
    # content = consolidate_similar_cases(content)
    
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
