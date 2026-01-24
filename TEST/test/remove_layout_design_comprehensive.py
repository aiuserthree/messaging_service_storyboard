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

def is_layout_design_only(line):
    """레이아웃/디자인만 확인하는 시나리오인지 판단 (기능 테스트가 아닌 경우)"""
    
    # 레이아웃/디자인 관련 키워드
    layout_keywords = [
        r'2단\s*레이아웃.*표시',
        r'2열\s*레이아웃.*표시',
        r'테이블\s*구조\s*확인',
        r'테이블\s*헤더\s*확인',
        r'카드\s*배치\s*확인',
        r'카드\s*구조\s*확인',
        r'화면에\s*표시됨\s*확인',
        r'배치.*확인',
        r'구조.*확인',
        r'레이아웃.*확인',
        r'반응형.*배치',
        r'열이\s*표시되는지\s*확인',
        r'화면\s*확인',
        r'표시\s*확인',
        r'노출\s*확인',
        r'화면에\s*표시되어야함',
        r'표시되어야함',
        r'노출되어야함',
        r'모바일\s*레이아웃',
        r'페이지네이션\s*화면\s*확인',
        r'현재\s*페이지.*표시',
        r'활성\s*상태.*표시',
        r'파란색\s*배경.*표시',
        r'3열\s*카드\s*배치',
        r'카드\s*형태로\s*배치',
        r'그리드\s*형태',
        r'화면\s*구성',
        r'화면\s*구조',
        r'화면\s*레이아웃',
        r'페이지\s*설명\s*화면\s*확인',
        r'탭\s*화면\s*확인',
        r'금액\s*화면에\s*표시됨',
        r'섹션\s*제목',
        r'카드\s*제목\s*확인',
        r'박스\s*확인',
    ]
    
    # 기능 테스트 키워드 (이것들이 있으면 유지)
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
    
    if '|' not in line:
        return False
    
    parts = line.split('|')
    if len(parts) < 6:
        return False
    
    # 테스트케이스명, 단계별 작업 수행내용, 예상 결과 확인
    test_case_name = parts[3].strip() if len(parts) > 3 else ''
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    combined = test_case_name + ' ' + work_content + ' ' + expected_result
    
    # 기능 테스트 키워드가 있으면 유지
    has_functional = False
    for keyword in functional_keywords:
        if re.search(keyword, combined, re.IGNORECASE):
            has_functional = True
            break
    
    # 레이아웃/디자인만 확인하는 경우
    has_layout_only = False
    for keyword in layout_keywords:
        if re.search(keyword, combined, re.IGNORECASE):
            has_layout_only = True
            break
    
    # 레이아웃/디자인만 있고 기능 테스트가 없는 경우 제거
    if has_layout_only and not has_functional:
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
            # 레이아웃/디자인만 확인하는 시나리오인 경우 제거
            if is_layout_design_only(line):
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
    backup_path = file_path + '.backup_layout_design'
    
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
    content, removed_count, removed_ids = remove_layout_design_scenarios(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"\n제거된 시나리오: {removed_count}건")
            if removed_ids:
                print(f"\n제거된 테스트 ID (처음 20개):")
                for test_id in removed_ids[:20]:
                    print(f"  - {test_id}")
                if len(removed_ids) > 20:
                    print(f"  ... 외 {len(removed_ids) - 20}개")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
