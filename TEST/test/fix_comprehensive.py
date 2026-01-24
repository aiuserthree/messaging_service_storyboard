#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종합 수정:
1. 테이블 열 삭제 (테스트 담당자, 수정방향, 우선순위)
2. PASS/FAIL, 오류내용 열 비우기
3. 한글 바이트 3바이트 → 2바이트로 수정 (더 정확하게)
4. 추가정보 → 변수로 수정 (더 정확하게)
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

def fix_table_structure(content):
    """테이블 구조 수정: 열 삭제 및 내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더 라인
        if re.match(r'^\|\s*순번\s*\|', line):
            # 원래: 순번|테스트ID|순서|테스트케이스명|페이지/팝업|단계별 작업 수행내용|테스트 데이터|예상 결과|테스트 담당자|PASS/FAIL|오류내용|수정방향|수정/오류|우선순위|수정상태|수정담당자|처리결과|최종확인|비고|
            # 수정: 순번|테스트ID|순서|테스트케이스명|페이지/팝업|단계별 작업 수행내용|테스트 데이터|예상 결과|||수정/오류|수정상태|수정담당자|처리결과|최종확인|비고|
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 20:
                new_parts = [
                    parts[0],  # |
                    parts[1],  # 순번
                    parts[2],  # 테스트ID
                    parts[3],  # 순서
                    parts[4],  # 테스트케이스명
                    parts[5],  # 페이지/팝업
                    parts[6],  # 단계별 작업 수행내용
                    parts[7],  # 테스트 데이터
                    parts[8],  # 예상 결과
                    '',        # PASS/FAIL (비움)
                    '',        # 오류내용 (비움)
                    parts[12], # 수정/오류
                    parts[14], # 수정상태
                    parts[15], # 수정담당자
                    parts[16], # 처리결과
                    parts[17], # 최종확인
                    parts[18], # 비고
                ]
                line = '|' + '|'.join(new_parts) + '|'
        
        # 테이블 구분선
        elif re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 20:
                new_parts = [''] * 17
                new_parts[0] = '|'
                new_parts[1:9] = ['---'] * 8
                new_parts[9:11] = [''] * 2  # PASS/FAIL, 오류내용
                new_parts[11:17] = ['---'] * 6
                line = '|'.join(new_parts) + '|'
        
        # 테이블 데이터 라인
        elif re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 20:
                new_parts = [
                    parts[0],  # |
                    parts[1],  # 순번
                    parts[2],  # 테스트ID
                    parts[3],  # 순서
                    parts[4],  # 테스트케이스명
                    parts[5],  # 페이지/팝업
                    parts[6],  # 단계별 작업 수행내용
                    parts[7],  # 테스트 데이터
                    parts[8],  # 예상 결과
                    '',        # PASS/FAIL (비움)
                    '',        # 오류내용 (비움)
                    parts[12], # 수정/오류
                    parts[14], # 수정상태
                    parts[15], # 수정담당자
                    parts[16], # 처리결과
                    parts[17], # 최종확인
                    parts[18], # 비고
                ]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_hangul_byte_comprehensive(content):
    """한글 바이트 3바이트 → 2바이트로 수정 (더 정확하게)"""
    
    # 한글 바이트 계산 관련 수정
    replacements = [
        (r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트'),
        (r'한글\s*3바이트', '한글 2바이트'),
        (r'\(한글\s*1자\s*=\s*3바이트\)', '(한글 1자 = 2바이트)'),
        (r'한글\s*1자\s*=\s*3바이트\s*계산', '한글 1자 = 2바이트 계산'),
        (r'바이트\s*계산:\s*한글\s*3바이트', '바이트 계산: 한글 2바이트'),
        (r'한글\s*약\s*30자', '한글 약 45자'),  # 90/2 = 45
        (r'한글\s*약\s*25자', '한글 약 25자'),  # 50/2 = 25
        (r'한글\s*약\s*50자', '한글 약 50자'),  # 100/2 = 50
        (r'한글\s*약\s*666자', '한글 약 1000자'),  # 2000/2 = 1000
        (r'한글\s*2자\(6바이트\)', '한글 2자(4바이트)'),
        (r'한글\s*3자\(9바이트\)', '한글 3자(6바이트)'),
        (r'한글\s*5자\(15바이트\)', '한글 5자(10바이트)'),
        (r'한글\s*3자\s*6바이트', '한글 3자(6바이트)'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 구체적인 바이트 수 예시 수정
    # "안녕하세요" 5자 = 15바이트 → 10바이트
    content = re.sub(r'"안녕하세요".*15\s*/\s*90\s*바이트', 
                     '"안녕하세요" 입력<br>- 바이트 수 표시 영역에 "10 / 90 바이트"가 표시되는지 확인', 
                     content)
    
    # "가나다" 3자 = 9바이트 → 6바이트
    content = re.sub(r'"가나다".*9바이트.*한글\s*1자', 
                     '"가나다" 입력<br>- 바이트 수가 6바이트로 계산되어 표시되는지 확인 (한글 1자 = 2바이트)', 
                     content)
    
    # "홍길동" 3자 = 9바이트 → 6바이트
    content = re.sub(r'"홍길동".*9\s*/\s*40\s*바이트.*한글\s*1자\s*=\s*3바이트', 
                     '"홍길동" 입력<br>- 바이트 카운터에 "6 / 40 바이트"가 표시되는지 확인<br>- 한글 1자 = 2바이트 계산이 정확한지 확인', 
                     content)
    
    # "9 / 6 / 40 바이트" 같은 잘못된 형식 수정
    content = re.sub(r'9\s*/\s*6\s*/\s*40\s*바이트', '6 / 40 바이트', content)
    
    return content

def fix_variable_names_comprehensive(content):
    """추가정보 → 변수로 수정 (더 정확하게)"""
    
    replacements = [
        (r'추가\s*정보\s*1', '변수1'),
        (r'추가\s*정보\s*2', '변수2'),
        (r'추가\s*정보\s*3', '변수3'),
        (r'추가정보\s*1', '변수1'),
        (r'추가정보\s*2', '변수2'),
        (r'추가정보\s*3', '변수3'),
        (r'추가\s*정보\s*1/2/3', '변수1/2/3'),
        (r'추가정보\s*1/2/3', '변수1/2/3'),
        (r'추가\s*정보\s*값', '변수 값'),
        (r'추가\s*정보\s*삽입', '변수 삽입'),
        (r'추가\s*정보\s*입력', '변수 입력'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_comprehensive'
    
    print("=" * 80)
    print("종합 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 테이블 구조 수정
    print("\n[1] 테이블 구조 수정 중...")
    content = fix_table_structure(content)
    
    # 2. 한글 바이트 수정
    print("\n[2] 한글 바이트 3바이트 → 2바이트로 수정 중...")
    content = fix_hangul_byte_comprehensive(content)
    
    # 3. 변수명 수정
    print("\n[3] 추가정보 → 변수로 수정 중...")
    content = fix_variable_names_comprehensive(content)
    
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
