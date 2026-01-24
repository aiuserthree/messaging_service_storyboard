#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단순 메뉴/페이지/탭 이동 확인 시나리오 제거
연계 기능으로 인한 페이지 이동은 유지
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
        print(f"파일 쓰기 오류: {file_path} - {e}")
        return False

def is_simple_navigation_only(line):
    """단순 메뉴/페이지/탭 이동 확인만 하는 시나리오인지 판단"""
    
    if '|' not in line or re.match(r'^\|\s*---', line):
        return False
    
    parts = line.split('|')
    if len(parts) < 6:
        return False
    
    test_case_name = parts[3].strip() if len(parts) > 3 else ''
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    combined = test_case_name + ' ' + work_content + ' ' + expected_result
    
    # 단순 이동 확인 패턴
    simple_nav_patterns = [
        r'탭.*클릭.*이동',
        r'메뉴.*클릭.*이동',
        r'드롭다운.*클릭.*이동',
        r'버튼.*클릭.*이동',
        r'링크.*클릭.*이동',
        r'이동되는지\s*확인',
        r'이동되어야함',
        r'페이지.*이동.*확인',
        r'탭.*이동.*확인',
        r'메뉴.*이동.*확인',
    ]
    
    # 연계 기능 키워드 (이것들이 있으면 유지)
    linked_function_keywords = [
        r'발송.*이동',
        r'완료.*이동',
        r'저장.*이동',
        r'등록.*이동',
        r'처리.*이동',
        r'결제.*이동',
        r'로그인.*이동',
        r'가입.*이동',
        r'연계',
        r'자동.*이동',
        r'리다이렉트',
    ]
    
    # 단순 이동 확인 패턴이 있는지 확인
    has_simple_nav = False
    for pattern in simple_nav_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            has_simple_nav = True
            break
    
    # 연계 기능 키워드가 있는지 확인
    has_linked_function = False
    for keyword in linked_function_keywords:
        if re.search(keyword, combined, re.IGNORECASE):
            has_linked_function = True
            break
    
    # 단순 이동 확인만 있고 연계 기능이 없는 경우 제거
    if has_simple_nav and not has_linked_function:
        # 예외: 기능 테스트가 함께 있는 경우는 유지
        functional_keywords = [
            r'입력',
            r'선택',
            r'제출',
            r'저장',
            r'삭제',
            r'수정',
            r'검증',
            r'유효성',
            r'오류',
            r'알림',
            r'처리',
            r'실행',
            r'전송',
            r'추가',
            r'업로드',
            r'다운로드',
            r'검색',
            r'등록',
            r'발송',
            r'결제',
        ]
        
        has_functional = False
        for keyword in functional_keywords:
            if re.search(keyword, combined, re.IGNORECASE):
                has_functional = True
                break
        
        # 기능 테스트가 없고 단순 이동만 확인하는 경우 제거
        if not has_functional:
            return True
    
    return False

def remove_navigation_from_line(line):
    """라인에서 단순 이동 확인 부분 제거"""
    
    if '|' not in line or re.match(r'^\|\s*---', line):
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    # 제거할 패턴들
    patterns_to_remove = [
        r'<br>.*?이동되는지\s*확인[^<]*',
        r'<br>.*?페이지.*?이동[^<]*',
        r'<br>.*?탭.*?이동[^<]*',
        r'이동되는지\s*확인',
        r'페이지.*?이동되어야함',
        r'탭.*?이동되어야함',
        r'메뉴.*?이동되어야함',
    ]
    
    new_work_content = work_content
    for pattern in patterns_to_remove:
        new_work_content = re.sub(pattern, '', new_work_content, flags=re.IGNORECASE)
    
    new_expected_result = expected_result
    for pattern in patterns_to_remove:
        new_expected_result = re.sub(pattern, '', new_expected_result, flags=re.IGNORECASE)
    
    # 빈 <br> 태그 제거
    new_work_content = re.sub(r'<br>\s*$', '', new_work_content)
    new_work_content = re.sub(r'^\s*<br>', '', new_work_content)
    new_work_content = re.sub(r'<br>\s*<br>', '<br>', new_work_content)
    new_work_content = re.sub(r'\s+', ' ', new_work_content).strip()
    
    # 변경사항이 있으면 업데이트
    if new_work_content != work_content or new_expected_result != expected_result:
        if len(parts) > 5:
            parts[5] = ' ' + new_work_content + ' '
        if len(parts) > 7:
            parts[7] = ' ' + new_expected_result + ' '
        return '|'.join(parts)
    
    return line

def remove_simple_navigation_scenarios(content):
    """단순 메뉴/페이지/탭 이동 확인 시나리오 제거"""
    
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    removed_ids = []
    cleaned_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 테이블 행인 경우에만 처리
        if re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            # 단순 이동 확인만 하는 시나리오인 경우 제거
            if is_simple_navigation_only(line):
                # 테스트 ID 추출
                parts = line.split('|')
                if len(parts) > 2:
                    test_id = parts[1].strip()
                    removed_ids.append(test_id)
                
                removed_count += 1
                i += 1
                continue
            
            # 단순 이동 확인 부분만 제거
            cleaned_line = remove_navigation_from_line(line)
            if cleaned_line != line:
                cleaned_count += 1
                line = cleaned_line
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines), removed_count, removed_ids, cleaned_count

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_navigation'
    
    print("=" * 80)
    print("단순 메뉴/페이지/탭 이동 확인 시나리오 제거")
    print("연계 기능으로 인한 페이지 이동은 유지")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 단순 이동 확인 시나리오 제거
    print("\n[1] 단순 이동 확인 시나리오 제거 중...")
    content, removed_count, removed_ids, cleaned_count = remove_simple_navigation_scenarios(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"\n제거된 시나리오: {removed_count}건")
            print(f"수정된 시나리오: {cleaned_count}건")
            if removed_ids:
                print(f"\n제거된 테스트 ID:")
                for test_id in removed_ids[:30]:
                    print(f"  - {test_id}")
                if len(removed_ids) > 30:
                    print(f"  ... 외 {len(removed_ids) - 30}개")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
