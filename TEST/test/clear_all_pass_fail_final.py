#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 테이블 형식에서 PASS/FAIL과 오류내용 열 내용 비우기
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

def clear_all_pass_fail(content):
    """모든 테이블에서 PASS/FAIL과 오류내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    cleared_count = 0
    
    for line in lines:
        original_line = line
        
        # 테이블 헤더나 구분선은 그대로 유지
        if re.match(r'^\|\s*---', line) or not re.match(r'^\|', line):
            new_lines.append(line)
            continue
        
        # 테이블 헤더는 그대로 유지
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
                    if pass_fail_idx >= 0 or error_content_idx >= 0:
                        break
            
            # 기본 위치 추정
            if pass_fail_idx < 0 and len(parts) >= 6:
                # 시나리오ID 형식: 시나리오ID | 시나리오명 | 테스트케이스명 | 단계별 작업 수행내용 | 예상 결과 | PASS/FAIL | 오류내용 | ...
                for i, part in enumerate(parts):
                    if '예상 결과' in part or '예상결과' in part:
                        if i + 1 < len(parts):
                            pass_fail_idx = i + 1
                        if i + 2 < len(parts):
                            error_content_idx = i + 2
                        break
            
            # 내용 비우기
            modified = False
            if pass_fail_idx >= 0 and pass_fail_idx < len(parts):
                if parts[pass_fail_idx] and parts[pass_fail_idx] not in ['', 'PASS/FAIL']:
                    parts[pass_fail_idx] = ''
                    modified = True
                    cleared_count += 1
            
            if error_content_idx >= 0 and error_content_idx < len(parts):
                if parts[error_content_idx] and parts[error_content_idx] not in ['', '오류내용']:
                    parts[error_content_idx] = ''
                    modified = True
            
            if modified:
                line = '|' + '|'.join(parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), cleared_count

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_clear_all_pass_fail_final'
    
    print("=" * 80)
    print("모든 테이블 형식에서 PASS/FAIL, 오류내용 열 내용 비우기")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # PASS/FAIL과 오류내용 내용 비우기
    print("\n[1] 모든 테이블에서 PASS/FAIL, 오류내용 열 내용 비우기 중...")
    content, cleared_count = clear_all_pass_fail(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"  비운 행 수: {cleared_count}건")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
