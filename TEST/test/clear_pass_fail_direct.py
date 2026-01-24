#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS/FAIL 열의 내용을 직접 찾아서 비우기
오류내용 열의 내용도 비우기
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

def clear_pass_fail_direct(content):
    """PASS/FAIL과 오류내용을 직접 찾아서 비우기"""
    
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
        
        # 데이터 행에서 PASS/FAIL과 오류내용 비우기
        if re.match(r'^\|', line):
            # PASS나 FAIL이 포함된 경우
            if re.search(r'\|\s*(PASS|FAIL)\s*\|', line):
                # PASS 또는 FAIL을 빈 문자열로 교체
                line = re.sub(r'\|\s*(PASS|FAIL)\s*\|', '| |', line)
                cleared_count += 1
            
            # 오류내용이 있는 경우 (FAIL 다음에 오는 내용)
            # 일반적으로 | PASS | 오류내용 | 형식
            # 또는 | FAIL | 오류내용 | 형식
            # 오류내용 열을 찾아서 비우기
            parts = [p.strip() for p in line.split('|')]
            
            # 이전 헤더에서 오류내용 위치 찾기
            error_content_idx = -1
            for prev_line in reversed(new_lines):
                if '|' in prev_line and '오류내용' in prev_line:
                    prev_parts = [p.strip() for p in prev_line.split('|')]
                    for i, part in enumerate(prev_parts):
                        if part == '오류내용':
                            error_content_idx = i
                            break
                    if error_content_idx >= 0:
                        break
            
            # 오류내용이 있는 열 비우기 (FAIL 다음 열 또는 특정 위치)
            if error_content_idx >= 0 and error_content_idx < len(parts):
                # 오류내용이 비어있지 않은 경우만 비우기
                if parts[error_content_idx] and parts[error_content_idx] not in ['PASS', 'FAIL', '']:
                    parts[error_content_idx] = ''
                    line = '|' + '|'.join(parts) + '|'
            
            # PASS/FAIL 다음에 오는 내용도 비우기 (일반적인 패턴)
            # | ... | PASS | 오류내용 | ... |
            # 또는 | ... | FAIL | 오류내용 | ... |
            for i, part in enumerate(parts):
                if part in ['PASS', 'FAIL']:
                    # 다음 열이 오류내용일 가능성
                    if i + 1 < len(parts) and parts[i + 1] and parts[i + 1] not in ['PASS', 'FAIL']:
                        # 오류내용으로 보이는 경우 비우기
                        if len(parts[i + 1]) > 0 and '오류' not in parts[i + 1] and '수정' not in parts[i + 1]:
                            # 오류내용이 아닌 경우는 건너뛰기
                            pass
                        else:
                            parts[i + 1] = ''
                    parts[i] = ''  # PASS/FAIL도 비우기
                    line = '|' + '|'.join(parts) + '|'
                    break
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), cleared_count

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_clear_pass_fail_direct'
    
    print("=" * 80)
    print("PASS/FAIL, 오류내용 열 내용 직접 비우기")
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
    content, cleared_count = clear_pass_fail_direct(content)
    
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
