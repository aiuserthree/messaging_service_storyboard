#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 담당자, 수정방향, 우선순위 열 삭제
PASS/FAIL, 오류내용 열 비우기
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

def process_table_line(line):
    """테이블 행 처리"""
    
    if not line.strip().startswith('|'):
        return line
    
    # 구분선 처리
    if re.match(r'^\|\s*---', line):
        # 구분선도 열 개수에 맞춰 조정
        parts = line.split('|')
        parts = [p.strip() for p in parts]
        if parts and parts[0] == '':
            parts = parts[1:]
        if parts and parts[-1] == '':
            parts = parts[:-1]
        
        if len(parts) >= 19:
            # 삭제할 열: 테스트 담당자(8), 수정방향(11), 우선순위(13)
            new_parts = []
            for i in range(len(parts)):
                if i == 8 or i == 11 or i == 13:  # 삭제할 열
                    continue
                else:
                    new_parts.append('---')
            return '| ' + ' | '.join(new_parts) + ' |'
        return line
    
    # 열 분리
    parts = line.split('|')
    
    # 빈 부분 제거 (앞뒤)
    parts = [p.strip() for p in parts]
    
    # 첫 번째와 마지막이 빈 문자열이므로 제거
    if parts and parts[0] == '':
        parts = parts[1:]
    if parts and parts[-1] == '':
        parts = parts[:-1]
    
    # 열 개수 확인 (최소 19개 필요)
    if len(parts) < 19:
        # 열 개수가 부족하면 그대로 반환
        return line
    
    # 디버깅: 실제 열 개수 확인
    # print(f"열 개수: {len(parts)}, 첫 5개: {parts[:5]}")
    
    # 열 인덱스 (0부터 시작)
    # 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과 | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고
    # 0     1         2      3                4             5                      6             7           8             9          10         11         12         13         14         15         16         17         18
    
    # 삭제할 열: 테스트 담당자(8), 수정방향(11), 우선순위(13)
    # 비울 열: PASS/FAIL(9), 오류내용(10)
    
    new_parts = []
    for i, part in enumerate(parts):
        if i == 8:  # 테스트 담당자 - 삭제
            continue
        elif i == 9:  # PASS/FAIL - 비우기
            new_parts.append('')
        elif i == 10:  # 오류내용 - 비우기
            new_parts.append('')
        elif i == 11:  # 수정방향 - 삭제
            continue
        elif i == 13:  # 우선순위 - 삭제
            continue
        else:
            new_parts.append(part)
    
    # 마크다운 테이블 형식으로 재구성
    result = '| ' + ' | '.join(new_parts) + ' |'
    return result

def process_content(content):
    """전체 내용 처리"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = process_table_line(line)
        new_lines.append(new_line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_columns'
    
    print("=" * 80)
    print("테스트 담당자, 수정방향, 우선순위 열 삭제")
    print("PASS/FAIL, 오류내용 열 비우기")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 내용 처리
    print("\n[1] 테이블 열 처리 중...")
    content = process_content(content)
    
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
