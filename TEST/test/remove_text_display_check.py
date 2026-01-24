#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
화면에 보이는 제목이나 설명 문구 확인 시나리오 제거
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

def is_text_display_check_only(line):
    """제목/설명 문구 확인만 하는 시나리오인지 판단"""
    
    if '|' not in line or re.match(r'^\|\s*---', line):
        return False
    
    parts = line.split('|')
    if len(parts) < 6:
        return False
    
    test_case_name = parts[3].strip() if len(parts) > 3 else ''
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    combined = test_case_name + ' ' + work_content + ' ' + expected_result
    
    # 제목/설명 문구 확인 패턴
    text_check_patterns = [
        r'제목.*표시',
        r'설명.*표시',
        r'안내.*표시',
        r'문구.*표시',
        r'표시되는지\s*확인',
        r'표시되어야함',
        r'화면에\s*표시',
        r'노출.*확인',
        r'표시.*확인',
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
        r'편집',
        r'생성',
        r'업데이트',
    ]
    
    # 제목/설명 문구 확인 패턴이 있는지 확인
    has_text_check = False
    for pattern in text_check_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            has_text_check = True
            break
    
    # 기능 테스트 키워드가 있는지 확인
    has_functional = False
    for keyword in functional_keywords:
        if re.search(keyword, combined, re.IGNORECASE):
            has_functional = True
            break
    
    # 제목/설명 문구 확인만 있고 기능 테스트가 없는 경우 제거
    if has_text_check and not has_functional:
        # 예외: "오류 메시지" 같은 것은 기능 테스트이므로 유지
        if '오류' in combined or '에러' in combined or '경고' in combined:
            return False
        return True
    
    return False

def clean_text_check_from_line(line):
    """라인에서 제목/설명 문구 확인 부분만 제거"""
    
    if '|' not in line or re.match(r'^\|\s*---', line):
        return line
    
    parts = line.split('|')
    if len(parts) < 6:
        return line
    
    work_content = parts[5].strip() if len(parts) > 5 else ''
    expected_result = parts[7].strip() if len(parts) > 7 else ''
    
    # 제목/설명 문구 확인 부분 제거
    patterns_to_remove = [
        r'<br>.*?제목.*?표시[^<]*',
        r'<br>.*?설명.*?표시[^<]*',
        r'<br>.*?안내.*?표시[^<]*',
        r'<br>.*?문구.*?표시[^<]*',
        r'<br>.*?표시되는지\s*확인[^<]*',
        r'<br>.*?노출.*?확인[^<]*',
        r'제목.*?표시되는지\s*확인',
        r'설명.*?표시되는지\s*확인',
        r'안내.*?표시되는지\s*확인',
        r'문구.*?표시되는지\s*확인',
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
    
    # 변경사항이 있으면 업데이트
    if new_work_content != work_content or new_expected_result != expected_result:
        if len(parts) > 5:
            parts[5] = ' ' + new_work_content + ' '
        if len(parts) > 7:
            parts[7] = ' ' + new_expected_result + ' '
        return '|'.join(parts)
    
    return line

def remove_text_display_scenarios(content):
    """제목/설명 문구 확인 시나리오 제거"""
    
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
            # 제목/설명 문구 확인만 하는 시나리오인 경우 제거
            if is_text_display_check_only(line):
                # 테스트 ID 추출
                parts = line.split('|')
                if len(parts) > 2:
                    test_id = parts[1].strip()
                    removed_ids.append(test_id)
                
                removed_count += 1
                i += 1
                continue
            
            # 제목/설명 문구 확인 부분만 제거
            cleaned_line = clean_text_check_from_line(line)
            if cleaned_line != line:
                cleaned_count += 1
                line = cleaned_line
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines), removed_count, removed_ids, cleaned_count

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_text_check'
    
    print("=" * 80)
    print("화면 제목/설명 문구 확인 시나리오 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 제목/설명 문구 확인 시나리오 제거
    print("\n[1] 제목/설명 문구 확인 시나리오 제거 중...")
    content, removed_count, removed_ids, cleaned_count = remove_text_display_scenarios(content)
    
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
