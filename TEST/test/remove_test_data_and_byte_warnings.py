#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 테스트 데이터 열 삭제
2. 바이트 초과 경고 메시지 관련 내용 모두 제거
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

def remove_test_data_column(content):
    """테스트 데이터 열 삭제"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더 라인
        if re.match(r'^\|', line) and '테스트 데이터' in line:
            parts = [p.strip() for p in line.split('|')]
            # 테스트 데이터 열 찾기 및 제거
            if '테스트 데이터' in parts:
                test_data_idx = None
                for i, part in enumerate(parts):
                    if '테스트 데이터' in part:
                        test_data_idx = i
                        break
                
                if test_data_idx is not None:
                    new_parts = parts[:test_data_idx] + parts[test_data_idx+1:]
                    line = '|' + '|'.join(new_parts) + '|'
        
        # 테이블 구분선
        elif re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            # 테스트 데이터 열 위치 찾기 (보통 8번째 열)
            if len(parts) >= 9:
                # 테스트 데이터 열 제거 (8번째)
                new_parts = parts[:8] + parts[9:]
                line = '|' + '|'.join(new_parts) + '|'
        
        # 테이블 데이터 라인
        elif re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            # 테스트 데이터 열 제거 (보통 8번째 열)
            if len(parts) >= 9:
                new_parts = parts[:8] + parts[9:]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def remove_byte_warning_messages(content):
    """바이트 초과 경고 메시지 관련 내용 제거"""
    
    # 바이트 초과 경고 메시지 패턴
    warning_patterns = [
        r'입력 가능한 글자수\(\d+바이트\)를 초과했습니다',
        r'메시지가 최대 바이트를 초과했습니다',
        r'제목이 \d+바이트를 초과했습니다',
        r'\d+바이트를 초과했습니다',
        r'글자수가 초과되었습니다',
        r'바이트를 초과했습니다',
    ]
    
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    
    for line in lines:
        original_line = line
        
        # 바이트 초과 경고 메시지가 포함된 라인 확인
        has_warning = False
        for pattern in warning_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                has_warning = True
                break
        
        # 바이트 초과 경고만 다루는 시나리오인 경우 제거
        if has_warning and re.match(r'^\|', line):
            # 다른 중요한 기능이 있는지 확인
            functional_keywords = [
                r'입력', r'선택', r'저장', r'삭제', r'수정', r'발송',
                r'등록', r'검색', r'표시', r'확인', r'클릭', r'버튼',
            ]
            
            has_other_function = False
            for keyword in functional_keywords:
                if re.search(keyword, line, re.IGNORECASE):
                    # 경고 메시지 부분만 제거
                    for pattern in warning_patterns:
                        line = re.sub(pattern, '', line, flags=re.IGNORECASE)
                    # 경고 메시지 확인 부분 제거
                    line = re.sub(r'<br>.*?경고\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
                    line = re.sub(r'<br>.*?오류\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
                    has_other_function = True
                    break
            
            # 경고 메시지만 다루는 시나리오인 경우 제거
            if not has_other_function:
                removed_count += 1
                continue
        
        # 경고 메시지 관련 내용 제거 (라인 내에서)
        for pattern in warning_patterns:
            line = re.sub(pattern, '', line, flags=re.IGNORECASE)
        
        # 경고 메시지 확인 부분 제거
        line = re.sub(r'<br>.*?경고\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
        line = re.sub(r'<br>.*?오류\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
        line = re.sub(r'경고\s*메시지가\s*표시되는지\s*확인', '', line, flags=re.IGNORECASE)
        line = re.sub(r'오류\s*메시지가\s*표시되는지\s*확인', '', line, flags=re.IGNORECASE)
        
        # 빈 <br> 태그 정리
        line = re.sub(r'<br>\s*<br>', '<br>', line)
        line = re.sub(r'<br>\s*$', '', line)
        line = re.sub(r'^\s*<br>', '', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), removed_count

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_warnings'
    
    print("=" * 80)
    print("테스트 데이터 열 삭제 및 바이트 초과 경고 메시지 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 테스트 데이터 열 삭제
    print("\n[1] 테스트 데이터 열 삭제 중...")
    content = remove_test_data_column(content)
    
    # 2. 바이트 초과 경고 메시지 제거
    print("\n[2] 바이트 초과 경고 메시지 제거 중...")
    content, removed_count = remove_byte_warning_messages(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"  제거된 시나리오: {removed_count}건")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
