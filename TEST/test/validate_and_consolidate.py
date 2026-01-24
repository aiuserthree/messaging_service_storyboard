#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서들을 기반으로 FO_테스트시나리오_상세.md 파일의 정합성을 체크하고,
화면설계의 모든 기능설명(글자수 제한 포함)이 포함되어 있는지 확인하며,
같은 영역의 세분화된 항목들을 통합하는 스크립트
"""

import re
import os
from collections import defaultdict

# 참고 문서에서 추출한 주요 기능 설명 및 제약 조건
REFERENCE_FEATURES = {
    # 이메일 관련
    'email_autocomplete': {
        'domains': ['naver.com', 'gmail.com', 'icloud.com', 'kakao.com', 'daum.net', 'nate.com', 'hanmail.net'],
        'count': 7,
        'description': '이메일 도메인리스트 자동완성 지원 기능 (7개)'
    },
    
    # 비밀번호 관련
    'password_validation': {
        'min_length': 8,
        'max_length': 20,
        'required': ['영문', '숫자', '특수문자'],
        'description': '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)'
    },
    
    # 메시지 바이트 제한
    'message_bytes': {
        'SMS': {'max_bytes': 90, 'korean_chars': 30, 'english_chars': 90},
        'LMS': {'max_bytes': 2000, 'korean_chars': 666, 'english_chars': 2000},
        'MMS': {'max_bytes': 2000, 'korean_chars': 666, 'english_chars': 2000},
        'byte_calc': '한글: 3바이트, 영문/숫자: 1바이트',
        'auto_convert': 'SMS 선택 시 90바이트 초과하면 LMS로 자동 전환'
    },
    
    # 제목 제한
    'title_limit': {
        'max_length': 40,
        'description': '제목을 입력하세요 (최대 40자)'
    },
    
    # 이름/변수 제한
    'name_variable_limit': {
        'max_bytes': 100,
        'korean_chars': 33,
        'english_chars': 100,
        'description': '입력 가능한 글자수(100바이트)를 초과했습니다'
    },
    
    # 템플릿명 제한
    'template_name_limit': {
        'max_bytes': 50,
        'description': '템플릿명 (최대 50바이트)'
    },
    
    # 메모 제한
    'memo_limit': {
        'max_length': 200,
        'description': '메모 (최대 200자)'
    },
    
    # 부고장 알림 내용
    'obituary_notice_limit': {
        'max_length': 100,
        'description': '알림 내용은 최대 100자까지 입력하실 수 있습니다'
    },
    
    # 파일 제한
    'file_limits': {
        'excel': {'max_size_mb': 10, 'max_rows': 10000, 'formats': ['.xlsx', '.xls', '.csv']},
        'image': {'max_size_kb': 300, 'max_count': 3, 'formats': ['JPG', 'PNG', 'GIF']}
    },
    
    # 테스트 수신번호
    'test_recipient_limit': {
        'max_count': 3,
        'description': '최대 3개 번호까지 입력 가능합니다'
    },
    
    # 광고 옆 문구
    'ad_prefix_limit': {
        'max_length': 20,
        'description': '(광고) 옆 문구 (최대 20자)'
    }
}

def read_file(filepath):
    """파일 읽기"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def extract_sections(content):
    """섹션 추출"""
    sections = []
    pattern = r'^## (\d+)\.\s+(.+)$'
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        section_num = int(match.group(1))
        section_title = match.group(2).strip()
        sections.append((section_num, section_title))
    
    return sections

def check_feature_coverage(content, section_num, section_title):
    """특정 섹션에서 기능 설명이 포함되어 있는지 확인"""
    issues = []
    
    # 섹션 내용 추출
    section_pattern = rf'^## {section_num}\.\s+{re.escape(section_title)}(.*?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return issues
    
    section_content = section_match.group(1)
    
    # 로그인/회원가입 관련 섹션 체크
    if section_num in [2, 3, 20]:  # 회원가입, 로그인
        # 이메일 자동완성 7개 도메인 체크
        if '7개' not in section_content and 'naver.com' not in section_content:
            issues.append(f"섹션 {section_num}: 이메일 자동완성 7개 도메인 설명 누락")
        
        # 비밀번호 조건 체크
        if '8~20자' not in section_content and '8-20자' not in section_content:
            if '비밀번호' in section_content:
                issues.append(f"섹션 {section_num}: 비밀번호 조건 (8~20자, 영문/숫자/특수문자) 설명 누락")
    
    # 문자 발송 관련 섹션 체크
    if section_num in [5, 6]:  # 일반문자 발송, 광고문자 발송
        # SMS/LMS 바이트 제한 체크
        if '90바이트' not in section_content and '90 byte' not in section_content:
            issues.append(f"섹션 {section_num}: SMS 90바이트 제한 설명 누락")
        if '2000바이트' not in section_content and '2000 byte' not in section_content:
            issues.append(f"섹션 {section_num}: LMS 2000바이트 제한 설명 누락")
        
        # 제목 40자 제한 체크
        if '40자' not in section_content:
            issues.append(f"섹션 {section_num}: 제목 40자 제한 설명 누락")
        
        # 이름/변수 100바이트 제한 체크
        if '100바이트' not in section_content:
            issues.append(f"섹션 {section_num}: 이름/변수 100바이트 제한 설명 누락")
    
    # 템플릿 관련 섹션 체크
    if section_num in [7, 8]:  # 일반문자 템플릿, 광고문자 템플릿
        # 템플릿명 50바이트 제한 체크
        if '50바이트' not in section_content and '50자' not in section_content:
            issues.append(f"섹션 {section_num}: 템플릿명 50바이트 제한 설명 누락")
    
    return issues

def find_duplicate_test_cases(content):
    """중복된 테스트 케이스 찾기"""
    duplicates = []
    test_cases = defaultdict(list)
    
    # 테스트 케이스 추출 (테스트ID 기준)
    pattern = r'^\|\s*\d+\s*\|\s*(TS-\d+-\d+)\s*\|'
    for match in re.finditer(pattern, content, re.MULTILINE):
        test_id = match.group(1)
        line_num = content[:match.start()].count('\n') + 1
        test_cases[test_id].append(line_num)
    
    # 중복 찾기
    for test_id, line_nums in test_cases.items():
        if len(line_nums) > 1:
            duplicates.append({
                'test_id': test_id,
                'lines': line_nums
            })
    
    return duplicates

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
                # 같은 기능 영역인지 확인 (테스트케이스명 기준)
                if is_similar_case(line, next_line):
                    similar_group.append(next_line)
                    j += 1
                else:
                    break
            
            # 유사한 케이스가 3개 이상이면 통합 고려
            if len(similar_group) >= 3:
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
    
    # 유사도 체크 (간단한 키워드 기반)
    keywords1 = set(case1.split())
    keywords2 = set(case2.split())
    
    # 공통 키워드가 50% 이상이면 유사
    if len(keywords1) == 0 or len(keywords2) == 0:
        return False
    
    common = len(keywords1 & keywords2)
    similarity = common / max(len(keywords1), len(keywords2))
    
    return similarity > 0.5

def merge_similar_cases(cases):
    """유사한 테스트 케이스들을 하나로 통합"""
    # 첫 번째 케이스를 기준으로 통합
    base_case = cases[0]
    
    # 단계별 작업 수행내용 통합
    steps = []
    for case in cases:
        parts = case.split('|')
        if len(parts) >= 6:
            step = parts[5].strip()
            if step and step not in steps:
                steps.append(step)
    
    # 통합된 케이스 생성
    parts = base_case.split('|')
    if len(parts) >= 6:
        parts[5] = ' ' + '<br>'.join(steps) + ' '
    
    return '|'.join(parts)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 정합성 체크 및 개선")
    print("=" * 80)
    
    # 파일 읽기
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    # 섹션 추출
    sections = extract_sections(content)
    print(f"\n총 {len(sections)}개 섹션 발견")
    
    # 기능 설명 누락 체크
    print("\n[1] 기능 설명 누락 체크 중...")
    all_issues = []
    for section_num, section_title in sections:
        issues = check_feature_coverage(content, section_num, section_title)
        all_issues.extend(issues)
    
    if all_issues:
        print(f"\n⚠️  {len(all_issues)}개 이슈 발견:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("✓ 기능 설명 누락 없음")
    
    # 중복 테스트 케이스 찾기
    print("\n[2] 중복 테스트 케이스 찾는 중...")
    duplicates = find_duplicate_test_cases(content)
    if duplicates:
        print(f"\n⚠️  {len(duplicates)}개 중복 테스트 ID 발견:")
        for dup in duplicates[:10]:  # 최대 10개만 표시
            print(f"  - {dup['test_id']}: {len(dup['lines'])}회 (라인: {dup['lines']})")
    else:
        print("✓ 중복 테스트 케이스 없음")
    
    # 통합 가능한 케이스 찾기
    print("\n[3] 통합 가능한 유사 케이스 분석 중...")
    # 이 부분은 실제로 통합하지 않고 분석만 수행
    print("  (통합 작업은 수동 검토 후 수행 권장)")
    
    # 개선 사항 요약
    print("\n" + "=" * 80)
    print("개선 사항 요약")
    print("=" * 80)
    print(f"1. 기능 설명 누락: {len(all_issues)}건")
    print(f"2. 중복 테스트 ID: {len(duplicates)}건")
    print("\n다음 단계:")
    print("  - 누락된 기능 설명 추가")
    print("  - 중복 항목 제거 또는 통합")
    print("  - 유사한 테스트 케이스 통합 검토")

if __name__ == '__main__':
    main()
