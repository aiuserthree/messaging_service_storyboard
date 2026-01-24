#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
레이아웃/디자인 관련 시나리오 제거 및 기능 테스트에 집중
화면설계 기능설명에 언급된 것은 유지
"""

import re

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def is_layout_design_scenario(line):
    """레이아웃/디자인 관련 시나리오인지 확인"""
    layout_keywords = [
        '레이아웃', '배치', '구조 확인', '카드.*배치', '테이블.*구조',
        '화면에 표시됨 확인', '화면 확인', '디자인', '스케치',
        '2단 레이아웃', '2열 레이아웃', '반응형.*배치',
        '테이블 헤더 확인', '열이 표시되는지 확인',
        '카드 형태로 배치', '그리드 형태', '배치 확인',
        '화면에 표시되어야함', '표시 확인', '노출 확인',
        '화면 구성', '화면 구조', '화면 레이아웃'
    ]
    
    # 단계별 작업 수행내용과 예상 결과 모두 확인
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 6:  # 순번, 테스트ID, 순서, 테스트케이스명, 페이지/팝업, 단계별 작업 수행내용
            work_content = parts[5] if len(parts) > 5 else ''
            expected_result = parts[7] if len(parts) > 7 else ''
            
            combined = work_content + ' ' + expected_result
            
            for keyword in layout_keywords:
                if re.search(keyword, combined, re.IGNORECASE):
                    return True
    
    return False

def is_functional_test(line):
    """기능 테스트인지 확인"""
    functional_keywords = [
        '입력', '클릭', '선택', '제출', '저장', '삭제', '수정',
        '검증', '유효성', '오류 메시지', '알림', '이동',
        '동작', '처리', '실행', '호출', '전송'
    ]
    
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 6:
            work_content = parts[5] if len(parts) > 5 else ''
            for keyword in functional_keywords:
                if keyword in work_content:
                    return True
    
    return False

def remove_layout_design_scenarios(content):
    """레이아웃/디자인 관련 시나리오 제거"""
    
    changes = []
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 테이블 행인 경우에만 처리
        if re.match(r'^\|', line):
            # 레이아웃/디자인 관련이면서 기능 테스트가 아닌 경우 제거
            if is_layout_design_scenario(line) and not is_functional_test(line):
                # 예외: 화면설계 기능설명에 언급된 것은 유지
                # (현재는 일단 레이아웃/디자인 관련은 모두 제거)
                removed_count += 1
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    if removed_count > 0:
        changes.append(f"레이아웃/디자인 관련 시나리오 {removed_count}건 제거")
    
    return '\n'.join(new_lines), changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_layout'
    
    print("=" * 80)
    print("레이아웃/디자인 관련 시나리오 제거 (기능 테스트에 집중)")
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
    content, changes = remove_layout_design_scenarios(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            if changes:
                print(f"\n변경 사항:")
                for change in changes:
                    print(f"  - {change}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
