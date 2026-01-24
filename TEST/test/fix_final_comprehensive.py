#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 종합 수정:
1. 테이블 열 삭제 및 PASS/FAIL, 오류내용 비우기 (모든 테이블 형식)
2. 한글 바이트 3바이트 → 2바이트로 수정 (남은 부분)
3. 추가정보 → 변수로 수정 (남은 부분)
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

def fix_all_tables(content):
    """모든 테이블 형식에서 PASS/FAIL, 오류내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 시나리오ID 형식 테이블 처리
        if re.match(r'^\|\s*시나리오ID\s*\|', line):
            # 원래: 시나리오ID|시나리오명|테스트케이스명|단계별 작업 수행내용|예상 결과|PASS/FAIL|오류내용|수정담당자|처리결과|
            # 수정: 시나리오ID|시나리오명|테스트케이스명|단계별 작업 수행내용|예상 결과|||수정담당자|처리결과|
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 9:
                new_parts = [
                    parts[0],  # |
                    parts[1],  # 시나리오ID
                    parts[2],  # 시나리오명
                    parts[3],  # 테스트케이스명
                    parts[4],  # 단계별 작업 수행내용
                    parts[5],  # 예상 결과
                    '',        # PASS/FAIL (비움)
                    '',        # 오류내용 (비움)
                    parts[7],  # 수정담당자
                    parts[8],  # 처리결과
                ]
                line = '|' + '|'.join(new_parts) + '|'
        
        # 시나리오ID 형식 구분선
        elif re.match(r'^\|\s*---.*시나리오ID', line) or (re.match(r'^\|\s*---', line) and len([p for p in line.split('|') if p.strip()]) >= 9):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 9:
                new_parts = [''] * 10
                new_parts[0] = '|'
                new_parts[1:6] = ['---'] * 5
                new_parts[6:8] = [''] * 2  # PASS/FAIL, 오류내용
                new_parts[8:10] = ['---'] * 2
                line = '|'.join(new_parts) + '|'
        
        # 시나리오ID 형식 데이터 라인
        elif re.match(r'^\|', line) and 'TS-' in line and len([p for p in line.split('|') if p.strip()]) >= 9:
            parts = [p.strip() for p in line.split('|')]
            # 시나리오ID 형식인지 확인 (TS-로 시작하는 ID가 첫 번째 데이터 열에 있음)
            if len(parts) >= 9 and re.match(r'TS-', parts[1] if len(parts) > 1 else ''):
                new_parts = [
                    parts[0],  # |
                    parts[1],  # 시나리오ID
                    parts[2] if len(parts) > 2 else '',  # 시나리오명
                    parts[3] if len(parts) > 3 else '',  # 테스트케이스명
                    parts[4] if len(parts) > 4 else '',  # 단계별 작업 수행내용
                    parts[5] if len(parts) > 5 else '',  # 예상 결과
                    '',        # PASS/FAIL (비움)
                    '',        # 오류내용 (비움)
                    parts[7] if len(parts) > 7 else '',  # 수정담당자
                    parts[8] if len(parts) > 8 else '',  # 처리결과
                ]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_remaining_hangul_byte(content):
    """남은 한글 바이트 수정"""
    
    # 구체적인 수치 수정
    replacements = [
        (r'9\s*/\s*40\s*바이트.*한글\s*3자\(6바이트\)\s*\+\s*영문\s*3자\(3바이트\)', 
         '9 / 40 바이트 (한글 3자(6바이트) + 영문 3자(3바이트))'),
        (r'"안녕하세요".*10\s*/\s*90\s*바이트.*표시되어야함\s*\(한글\s*1자\s*=\s*2바이트\)', 
         '"안녕하세요" 입력<br>- 바이트 수 표시 영역에 "10 / 90 바이트"가 표시되는지 확인<br>- 한글 1자 = 2바이트 계산이 정확한지 확인'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def fix_remaining_variable_names(content):
    """남은 추가정보 → 변수 수정"""
    
    # "추가 정보 바이트 제한" 같은 제목도 수정
    content = re.sub(r'추가\s*정보\s*바이트\s*제한', '변수 바이트 제한', content, flags=re.IGNORECASE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final'
    
    print("=" * 80)
    print("최종 종합 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 모든 테이블 형식 수정
    print("\n[1] 모든 테이블 형식에서 PASS/FAIL, 오류내용 비우기 중...")
    content = fix_all_tables(content)
    
    # 2. 남은 한글 바이트 수정
    print("\n[2] 남은 한글 바이트 수정 중...")
    content = fix_remaining_hangul_byte(content)
    
    # 3. 남은 변수명 수정
    print("\n[3] 남은 변수명 수정 중...")
    content = fix_remaining_variable_names(content)
    
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
