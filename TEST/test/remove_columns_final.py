#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 담당자, 수정방향, 우선순위 열 삭제
PASS/FAIL, 오류내용 열 내용 비우기 (모든 테이블 형식)
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

def process_table_columns(content):
    """테이블 열 삭제 및 내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        original_line = line
        
        # 테이블 헤더 라인 처리
        if '|' in line and ('테스트 담당자' in line or '수정방향' in line or '우선순위' in line or 'PASS/FAIL' in line or '오류내용' in line):
            parts = [p.strip() for p in line.split('|')]
            
            # 삭제할 열 인덱스 찾기
            indices_to_remove = []
            pass_fail_idx = -1
            error_content_idx = -1
            
            for i, part in enumerate(parts):
                if part in ['테스트 담당자', '수정방향', '우선순위']:
                    indices_to_remove.append(i)
                elif part == 'PASS/FAIL':
                    pass_fail_idx = i
                elif part == '오류내용':
                    error_content_idx = i
            
            # 헤더에서 열 제거
            new_parts = []
            for i, part in enumerate(parts):
                if i == 0:  # 첫 번째 빈 열
                    new_parts.append('')
                elif i in indices_to_remove:
                    continue  # 삭제할 열
                else:
                    new_parts.append(part)
            
            new_line = '|' + '|'.join(new_parts) + '|'
            new_lines.append(new_line)
            continue
        
        # 데이터 행 처리
        if re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) < 5:
                new_lines.append(line)
                continue
            
            # 이전 헤더에서 인덱스 찾기
            test_manager_idx = -1
            pass_fail_idx = -1
            error_content_idx = -1
            fix_direction_idx = -1
            priority_idx = -1
            
            # 이전 헤더 라인 찾기
            for prev_line in reversed(new_lines):
                if '|' in prev_line and ('테스트 담당자' in prev_line or 'PASS/FAIL' in prev_line or '수정방향' in prev_line):
                    prev_parts = [p.strip() for p in prev_line.split('|')]
                    for i, part in enumerate(prev_parts):
                        if part == '테스트 담당자':
                            test_manager_idx = i
                        elif part == 'PASS/FAIL':
                            pass_fail_idx = i
                        elif part == '오류내용':
                            error_content_idx = i
                        elif part == '수정방향':
                            fix_direction_idx = i
                        elif part == '우선순위':
                            priority_idx = i
                    break
            
            # 기본 인덱스 (일반적인 테이블 구조)
            if test_manager_idx < 0 and len(parts) >= 14:
                # 순번(0) | 테스트ID(1) | ... | 예상 결과(7) | 테스트 담당자(8) | PASS/FAIL(9) | 오류내용(10) | 수정방향(11) | ... | 우선순위(13) | ...
                test_manager_idx = 8
                pass_fail_idx = 9
                error_content_idx = 10
                fix_direction_idx = 11
                priority_idx = 13
            
            # 열 처리
            if (test_manager_idx >= 0 or pass_fail_idx >= 0 or error_content_idx >= 0 or 
                fix_direction_idx >= 0 or priority_idx >= 0):
                new_parts = []
                for i, part in enumerate(parts):
                    if i == 0:  # 첫 번째 빈 열
                        new_parts.append('')
                    elif i == test_manager_idx or i == fix_direction_idx or i == priority_idx:
                        continue  # 삭제할 열
                    elif i == pass_fail_idx or i == error_content_idx:
                        new_parts.append('')  # 내용 비우기
                    else:
                        new_parts.append(part)
                
                new_line = '|' + '|'.join(new_parts) + '|'
                new_lines.append(new_line)
            else:
                # PASS/FAIL이나 오류내용이 있는 행 찾기 (다른 형식)
                # 시나리오ID 형식의 테이블
                if 'PASS' in line or 'FAIL' in line:
                    # PASS/FAIL과 오류내용 열 찾기
                    parts = [p.strip() for p in line.split('|')]
                    
                    # 이전 헤더에서 PASS/FAIL과 오류내용 위치 찾기
                    for prev_line in reversed(new_lines):
                        if '|' in prev_line and 'PASS/FAIL' in prev_line:
                            prev_parts = [p.strip() for p in prev_line.split('|')]
                            for i, part in enumerate(prev_parts):
                                if part == 'PASS/FAIL':
                                    pass_fail_idx = i
                                elif part == '오류내용':
                                    error_content_idx = i
                            break
                    
                    if pass_fail_idx >= 0 or error_content_idx >= 0:
                        new_parts = []
                        for i, part in enumerate(parts):
                            if i == 0:
                                new_parts.append('')
                            elif i == pass_fail_idx or i == error_content_idx:
                                new_parts.append('')  # 내용 비우기
                            else:
                                new_parts.append(part)
                        new_line = '|' + '|'.join(new_parts) + '|'
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_columns_final'
    
    print("=" * 80)
    print("테스트 담당자, 수정방향, 우선순위 열 삭제")
    print("PASS/FAIL, 오류내용 열 내용 비우기 (모든 테이블 형식)")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 테이블 열 처리
    print("\n[1] 테이블 열 삭제 및 내용 비우기 중...")
    content = process_table_columns(content)
    
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
