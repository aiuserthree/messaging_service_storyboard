#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
레이아웃/디자인 관련 시나리오 제거 (최종)
- 레이아웃/디자인만 확인하는 시나리오 제거
- 기능 테스트와 함께 있는 경우, 레이아웃 확인 부분만 제거하거나 전체 제거 판단
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

def should_remove_line(line):
    """레이아웃/디자인만 확인하는 시나리오인지 판단"""
    
    if '|' not in line or re.match(r'^\|\s*---', line):
        return False
    
    parts = line.split('|')
    if len(parts) < 6:
        return False
    
    test_case_name = parts[3].strip() if len(parts) > 3 else ''
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    combined = test_case_name + ' ' + work_content + ' ' + expected_result
    
    # 명확한 레이아웃/디자인만 확인하는 패턴
    layout_only_patterns = [
        r'테이블\s*구조\s*확인',
        r'테이블\s*헤더\s*확인',
        r'카드\s*배치\s*확인',
        r'카드\s*구조\s*확인',
        r'2단\s*레이아웃\s*확인',
        r'2열\s*레이아웃\s*확인',
        r'페이지네이션.*화면\s*확인',
        r'현재\s*페이지.*표시',
        r'활성\s*상태.*표시',
        r'파란색\s*배경.*표시',
    ]
    
    # 기능 테스트 키워드
    functional_keywords = [
        r'입력',
        r'클릭',
        r'선택',
        r'제출',
        r'저장',
        r'삭제',
        r'수정',
        r'검증',
        r'유효성',
        r'오류\s*메시지',
        r'알림',
        r'이동',
        r'동작',
        r'처리',
        r'실행',
        r'호출',
        r'전송',
        r'추가',
        r'업로드',
        r'다운로드',
        r'검색',
        r'필터',
        r'정렬',
        r'변경',
        r'등록',
        r'발송',
        r'결제',
        r'환불',
        r'충전',
    ]
    
    # 레이아웃/디자인만 확인하는 패턴이 있는지 확인
    has_layout_only = False
    for pattern in layout_only_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            has_layout_only = True
            break
    
    # 기능 테스트 키워드가 있는지 확인
    has_functional = False
    for keyword in functional_keywords:
        if re.search(keyword, combined, re.IGNORECASE):
            has_functional = True
            break
    
    # 레이아웃/디자인만 확인하고 기능 테스트가 없는 경우 제거
    if has_layout_only and not has_functional:
        return True
    
    # "페이지 로드 확인" 중 레이아웃만 확인하는 경우
    if '페이지 로드 확인' in test_case_name or '페이지 로드' in test_case_name:
        if '2단 레이아웃' in combined or '레이아웃' in combined:
            # 레이아웃 확인 부분만 있는 경우 제거
            if '접근' in work_content and '표시되는지 확인' in work_content:
                if not any(kw in work_content for kw in ['클릭', '입력', '선택', '이동', '처리']):
                    return True
    
    return False

def remove_layout_design_scenarios(content):
    """레이아웃/디자인 관련 시나리오 제거"""
    
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    removed_ids = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 테이블 행인 경우에만 처리
        if re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            if should_remove_line(line):
                # 테스트 ID 추출
                parts = line.split('|')
                if len(parts) > 2:
                    test_id = parts[1].strip()
                    removed_ids.append(test_id)
                
                removed_count += 1
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines), removed_count, removed_ids

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final'
    
    print("=" * 80)
    print("레이아웃/디자인 관련 시나리오 제거 (최종)")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 레이아웃/디자인 관련 시나리오 제거
    print("\n[1] 레이아웃/디자인 관련 시나리오 제거 중...")
    content, removed_count, removed_ids = remove_layout_design_scenarios(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"\n제거된 시나리오: {removed_count}건")
            if removed_ids:
                print(f"\n제거된 테스트 ID:")
                for test_id in removed_ids:
                    print(f"  - {test_id}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
