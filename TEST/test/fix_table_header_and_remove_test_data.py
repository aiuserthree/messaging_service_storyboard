#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테이블 헤더 정리 및 남은 테스트 데이터 열 제거
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

def fix_table_headers(content):
    """테이블 헤더 정리"""
    
    # 잘못된 헤더 형식 수정
    content = re.sub(
        r'\|\|\|\|\|\|순번\|테스트ID\|순서\|테스트케이스명\|단계별 작업 수행내용\|\|\|수정상태\|처리결과\|최종확인\|비고\|\|\|\|\|',
        '| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |',
        content
    )
    
    # 잘못된 구분선 형식 수정
    content = re.sub(
        r'\|\|\|\|-\|-\|-\|-\|-\|-\|-\|-\|\|\|',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
        content
    )
    
    return content

def remove_remaining_test_data(content):
    """남은 테스트 데이터 열 제거"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테스트 데이터가 포함된 라인 찾기
        if '테스트 데이터' in line or re.search(r'중복된 전화번호가 있는 테스트 데이터|수신거부 번호가 포함된 테스트 데이터', line):
            # 테스트 데이터 열 제거
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8:
                # 테스트 데이터 열 찾기 및 제거
                new_parts = []
                for i, part in enumerate(parts):
                    if '테스트 데이터' in part or part in ['중복된 전화번호가 있는 테스트 데이터', '수신거부 번호가 포함된 테스트 데이터']:
                        continue  # 이 열 제거
                    new_parts.append(part)
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_table_fix'
    
    print("=" * 80)
    print("테이블 헤더 정리 및 테스트 데이터 열 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 테이블 헤더 정리
    print("\n[1] 테이블 헤더 정리 중...")
    content = fix_table_headers(content)
    
    # 2. 남은 테스트 데이터 열 제거
    print("\n[2] 남은 테스트 데이터 열 제거 중...")
    content = remove_remaining_test_data(content)
    
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
