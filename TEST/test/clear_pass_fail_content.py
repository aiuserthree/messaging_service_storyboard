#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS/FAIL 열의 내용을 모두 비우기
오류내용 열의 내용도 모두 비우기
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

def clear_pass_fail_and_error_content(content):
    """PASS/FAIL과 오류내용 열의 내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        original_line = line
        
        # 테이블 헤더나 구분선은 그대로 유지
        if re.match(r'^\|\s*---', line) or not re.match(r'^\|', line):
            new_lines.append(line)
            continue
        
        # 테이블 헤더에서 열 위치 찾기
        if 'PASS/FAIL' in line or '오류내용' in line:
            new_lines.append(line)
            continue
        
        # 데이터 행 처리
        if re.match(r'^\|', line):
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) < 3:
                new_lines.append(line)
                continue
            
            # 이전 헤더에서 PASS/FAIL과 오류내용 위치 찾기
            pass_fail_idx = -1
            error_content_idx = -1
            
            for prev_line in reversed(new_lines):
                if '|' in prev_line and ('PASS/FAIL' in prev_line or '오류내용' in prev_line):
                    prev_parts = [p.strip() for p in prev_line.split('|')]
                    for i, part in enumerate(prev_parts):
                        if part == 'PASS/FAIL':
                            pass_fail_idx = i
                        elif part == '오류내용':
                            error_content_idx = i
                    break
            
            # 기본 위치 추정 (일반적인 테이블 구조)
            # 순번 | 테스트ID | ... | 예상 결과 | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | ...
            if pass_fail_idx < 0 and len(parts) >= 10:
                # 일반적으로 PASS/FAIL은 예상 결과 다음
                # 예상 결과를 찾아서 그 다음이 PASS/FAIL일 가능성
                for i, part in enumerate(parts):
                    if '예상 결과' in part or '예상결과' in part:
                        if i + 2 < len(parts):
                            pass_fail_idx = i + 2  # 테스트 담당자 다음
                        if i + 3 < len(parts):
                            error_content_idx = i + 3
                        break
            
            # PASS나 FAIL이 포함된 경우 해당 열 찾기
            if pass_fail_idx < 0:
                for i, part in enumerate(parts):
                    if part in ['PASS', 'FAIL'] or part.startswith('PASS') or part.startswith('FAIL'):
                        pass_fail_idx = i
                        # 오류내용은 보통 PASS/FAIL 다음
                        if i + 1 < len(parts):
                            error_content_idx = i + 1
                        break
            
            # 내용 비우기
            if pass_fail_idx >= 0 and pass_fail_idx < len(parts):
                parts[pass_fail_idx] = ''
            
            if error_content_idx >= 0 and error_content_idx < len(parts):
                parts[error_content_idx] = ''
            
            new_line = '|' + '|'.join(parts) + '|'
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_clear_pass_fail'
    
    print("=" * 80)
    print("PASS/FAIL, 오류내용 열 내용 비우기")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # PASS/FAIL과 오류내용 내용 비우기
    print("\n[1] PASS/FAIL, 오류내용 열 내용 비우기 중...")
    content = clear_pass_fail_and_error_content(content)
    
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
