#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 바이트 수 80% 경고 제거 (구현 안됨, 90%만 구현됨)
2. 한글 바이트 3바이트 → 2바이트로 수정
3. 추가정보1,2,3 → 변수1,2,3으로 수정
4. 테스트 담당자, 수정방향, 우선순위 열 삭제
5. PASS/FAIL, 오류내용 열 내용 비우기
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

def remove_80_percent_warning(content):
    """바이트 수 80% 경고 관련 내용 제거 (구현 안됨)"""
    
    # 80% 경고 관련 패턴 제거
    patterns = [
        r'바이트\s*수\s*80%\s*경고',
        r'80%\s*경고\s*표시',
        r'80%\s*인\s*\d+\s*바이트',
        r'바이트\s*수\s*80%',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 80% 관련 라인 제거
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if re.search(r'80%\s*경고|80%\s*인|바이트.*80%', line, re.IGNORECASE):
            # 80% 경고만 다루는 라인인지 확인
            if re.match(r'^\|', line) and ('80%' in line or '80퍼' in line):
                # 다른 중요한 내용이 있는지 확인
                if not re.search(r'90%|발송|입력|선택|저장|삭제|수정', line, re.IGNORECASE):
                    continue  # 라인 제거
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_hangul_byte(content):
    """한글 바이트 3바이트 → 2바이트로 수정"""
    
    # 한글 바이트 계산 관련 수정
    replacements = [
        (r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트'),
        (r'한글\s*3바이트', '한글 2바이트'),
        (r'한글\s*약\s*30자', '한글 약 45자'),  # 90바이트 / 2 = 45자
        (r'한글\s*약\s*25자', '한글 약 38자'),  # 50바이트 / 2 = 25자 (아니면 38자?)
        (r'한글\s*약\s*50자', '한글 약 50자'),  # 100바이트 / 2 = 50자
        (r'한글\s*약\s*666자', '한글 약 1000자'),  # 2000바이트 / 2 = 1000자
        (r'한글\s*2자\(6바이트\)', '한글 2자(4바이트)'),
        (r'한글\s*5자\(15바이트\)', '한글 5자(10바이트)'),
        (r'\(한글\s*1자\s*=\s*3바이트\)', '(한글 1자 = 2바이트)'),
        (r'바이트\s*계산:\s*한글\s*3바이트', '바이트 계산: 한글 2바이트'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 바이트 수 예시 수정 (한글 기준)
    # "15 / 90 바이트" (한글 5자 = 15바이트) → "10 / 90 바이트" (한글 5자 = 10바이트)
    # "9 / 90 바이트" (한글 3자 = 9바이트) → "6 / 90 바이트" (한글 3자 = 6바이트)
    content = re.sub(r'(\d+)\s*/\s*90\s*바이트.*한글\s*(\d+)자\s*=\s*3바이트', 
                     lambda m: f"{int(m.group(1)) * 2 // 3} / 90 바이트 (한글 {m.group(2)}자 = 2바이트)", 
                     content)
    
    # "안녕하세요" 5자 = 15바이트 → 10바이트
    content = re.sub(r'"안녕하세요"\s*입력.*15\s*/\s*90\s*바이트', 
                     '"안녕하세요" 입력<br>- 바이트 수 표시 영역에 "10 / 90 바이트"가 표시되는지 확인', 
                     content)
    
    # "가나다" 3자 = 9바이트 → 6바이트
    content = re.sub(r'"가나다".*9바이트.*한글\s*1자\s*=\s*3바이트', 
                     '"가나다" 입력<br>- 바이트 수가 6바이트로 계산되어 표시되는지 확인 (한글 1자 = 2바이트)', 
                     content)
    
    # "홍길동" 3자 = 9바이트 → 6바이트
    content = re.sub(r'"홍길동".*9\s*/\s*40\s*바이트.*한글\s*1자\s*=\s*3바이트', 
                     '"홍길동" 입력<br>- 바이트 카운터에 "6 / 40 바이트"가 표시되는지 확인<br>- 한글 1자 = 2바이트 계산이 정확한지 확인', 
                     content)
    
    return content

def fix_variable_names(content):
    """추가정보1,2,3 → 변수1,2,3으로 수정"""
    
    replacements = [
        (r'추가\s*정보\s*1', '변수1'),
        (r'추가\s*정보\s*2', '변수2'),
        (r'추가\s*정보\s*3', '변수3'),
        (r'추가정보\s*1', '변수1'),
        (r'추가정보\s*2', '변수2'),
        (r'추가정보\s*3', '변수3'),
        (r'추가\s*정보\s*1/2/3', '변수1/2/3'),
        (r'추가정보\s*1/2/3', '변수1/2/3'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def remove_columns_and_clear_content(content):
    """테스트 담당자, 수정방향, 우선순위 열 삭제 및 PASS/FAIL, 오류내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더 라인 처리
        if re.match(r'^\|\s*순번\s*\|', line):
            # 열 순서: 순번|테스트ID|순서|테스트케이스명|페이지/팝업|단계별 작업 수행내용|테스트 데이터|예상 결과|테스트 담당자|PASS/FAIL|오류내용|수정방향|수정/오류|우선순위|수정상태|수정담당자|처리결과|최종확인|비고|
            # 삭제할 열: 테스트 담당자(9), 수정방향(12), 우선순위(14)
            # 비울 열: PASS/FAIL(10), 오류내용(11)
            
            parts = line.split('|')
            if len(parts) >= 20:
                # 헤더에서 열 제거
                new_parts = parts[:9] + parts[10:12] + parts[13:14] + parts[15:]
                line = '|'.join(new_parts)
        
        # 테이블 구분선 처리
        elif re.match(r'^\|\s*---', line):
            parts = line.split('|')
            if len(parts) >= 20:
                new_parts = parts[:9] + parts[10:12] + parts[13:14] + parts[15:]
                line = '|'.join(new_parts)
        
        # 테이블 데이터 라인 처리
        elif re.match(r'^\|', line):
            parts = line.split('|')
            if len(parts) >= 20:
                # 열 제거 및 내용 비우기
                new_parts = parts[:9]  # 순번~예상 결과까지
                new_parts.append('')  # PASS/FAIL 비우기
                new_parts.append('')  # 오류내용 비우기
                new_parts.extend(parts[13:14])  # 수정/오류
                new_parts.extend(parts[15:])  # 수정상태 이후
                line = '|'.join(new_parts)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_byte_fix'
    
    print("=" * 80)
    print("바이트 관련 수정 및 변수명 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 바이트 수 80% 경고 제거
    print("\n[1] 바이트 수 80% 경고 제거 중...")
    content = remove_80_percent_warning(content)
    
    # 2. 한글 바이트 3바이트 → 2바이트로 수정
    print("\n[2] 한글 바이트 3바이트 → 2바이트로 수정 중...")
    content = fix_hangul_byte(content)
    
    # 3. 추가정보1,2,3 → 변수1,2,3으로 수정
    print("\n[3] 추가정보1,2,3 → 변수1,2,3으로 수정 중...")
    content = fix_variable_names(content)
    
    # 4. 테이블 열 삭제 및 내용 비우기
    print("\n[4] 테이블 열 삭제 및 내용 비우기 중...")
    content = remove_columns_and_clear_content(content)
    
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
