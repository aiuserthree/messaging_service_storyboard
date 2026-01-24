#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
바이트 초과 경고 메시지 관련 시나리오 모두 제거
테스트 데이터 열 삭제
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

def remove_byte_warning_lines(content):
    """바이트 초과 경고 관련 라인 제거"""
    
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    removed_ids = []
    
    for line in lines:
        original_line = line
        
        # 바이트 초과 경고 관련 키워드
        warning_keywords = [
            '바이트 제한',
            '바이트 초과',
            '초과 입력 시도',
            '초과.*경고',
            '바이트를 초과',
            '초과했습니다',
            '초과된 부분',
        ]
        
        # 바이트 초과 경고만 다루는 시나리오인지 확인
        is_warning_only = False
        if re.match(r'^\|', line) and 'TS-' in line:
            has_warning = False
            for keyword in warning_keywords:
                if re.search(keyword, line, re.IGNORECASE):
                    has_warning = True
                    break
            
            if has_warning:
                # 다른 중요한 기능이 있는지 확인 (LMS 자동 전환은 유지)
                if 'LMS 자동 전환' in line or '자동 전환' in line:
                    # 경고 메시지 부분만 제거하고 유지
                    line = re.sub(r'경고\s*메시지.*?표시', '', line, flags=re.IGNORECASE)
                    line = re.sub(r'오류\s*메시지.*?표시', '', line, flags=re.IGNORECASE)
                    line = re.sub(r'초과.*?경고', '', line, flags=re.IGNORECASE)
                else:
                    # 경고 메시지만 다루는 시나리오 제거
                    is_warning_only = True
                    parts = line.split('|')
                    if len(parts) > 2:
                        test_id = parts[1].strip()
                        if test_id:
                            removed_ids.append(test_id)
                    removed_count += 1
        
        if not is_warning_only:
            # 경고 메시지 관련 내용 제거 (라인 내에서)
            line = re.sub(r'경고\s*메시지.*?표시[^<]*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'오류\s*메시지.*?표시[^<]*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'초과된\s*부분.*?확인[^<]*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'초과.*?경고\s*메시지', '', line, flags=re.IGNORECASE)
            line = re.sub(r'입력 가능한 글자수.*?초과했습니다', '', line, flags=re.IGNORECASE)
            line = re.sub(r'메시지가 최대 바이트를 초과했습니다', '', line, flags=re.IGNORECASE)
            line = re.sub(r'제목이.*?바이트를 초과했습니다', '', line, flags=re.IGNORECASE)
            
            # 빈 <br> 태그 정리
            line = re.sub(r'<br>\s*<br>', '<br>', line)
            line = re.sub(r'<br>\s*$', '', line)
            line = re.sub(r'^\s*<br>', '', line)
            
            new_lines.append(line)
    
    return '\n'.join(new_lines), removed_count, removed_ids

def remove_test_data_column_final(content):
    """테스트 데이터 열 삭제 (최종)"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더에서 테스트 데이터 열 찾기 및 제거
        if '테스트 데이터' in line and re.match(r'^\|', line):
            # 테스트 데이터 열 제거
            line = re.sub(r'\|\s*테스트\s*데이터\s*\|', '|', line)
        
        # 테이블 데이터 라인에서 테스트 데이터 열 제거 (보통 8번째 열)
        elif re.match(r'^\|', line):
            parts = [p.strip() for p in line.split('|')]
            # 테스트 데이터 열이 있는 경우 제거 (보통 8번째, 인덱스 7)
            if len(parts) >= 9:
                # 테스트 데이터 열 제거
                new_parts = parts[:8] + parts[9:]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final_remove'
    
    print("=" * 80)
    print("바이트 초과 경고 메시지 제거 및 테스트 데이터 열 삭제")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 바이트 초과 경고 메시지 제거
    print("\n[1] 바이트 초과 경고 메시지 제거 중...")
    content, removed_count, removed_ids = remove_byte_warning_lines(content)
    
    # 2. 테스트 데이터 열 삭제
    print("\n[2] 테스트 데이터 열 삭제 중...")
    content = remove_test_data_column_final(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"  제거된 시나리오: {removed_count}건")
            if removed_ids:
                print(f"\n제거된 테스트 ID (일부):")
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
