#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 시나리오 재작성 스크립트 v3
- 중복 내용 제거
- 빈 내용 정리
- 이메일 입력 예상결과 추가
- 중복 표현 정리
"""

import re
import os

def remove_duplicate_phone_content(content):
    """전화번호 관련 중복 내용 제거"""
    # 전화번호 관련 내용이 중복되어 있는 경우 제거
    pattern = r'(- 전화번호 최소 9자리 이상 입력 확인<br>\s*)(- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*)(- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*)(- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*)(- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)\1\2\3\4\5'
    content = re.sub(pattern, r'\1\2\3\4\5', content, flags=re.MULTILINE)
    
    return content

def remove_duplicate_expressions(content):
    """중복 표현 제거"""
    # "정상적으로 정상적으로" 같은 중복 제거
    content = re.sub(r'정상적으로\s+정상적으로', '정상적으로', content)
    content = re.sub(r'작동되어야\s+작동되어야', '작동되어야 함', content)
    
    return content

def fix_email_input_expected_result(content):
    """이메일 입력 예상결과 추가"""
    # 이메일 입력 관련 예상결과가 비어있는 경우 추가
    content = re.sub(
        r'(\| 이메일 입력 \| 페이지 \|[^|]*\|)\s*\|',
        r'\1 이메일 유효성 검증이 정상적으로 작동되어야 함 |',
        content
    )
    
    # 이메일 입력 확인 후 빈 줄이 있는 경우 정리
    content = re.sub(
        r'이메일 입력 확인<br>\s*<br>\s*- 비정상',
        '이메일 입력 확인<br>  - 비정상',
        content
    )
    
    # 이메일 입력에 정상 케이스 추가
    content = re.sub(
        r'(이메일 입력 확인<br>)\s*<br>\s*(- 비정상 케이스: \'@\'와)',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>\2',
        content
    )
    
    return content

def clean_empty_lines(content):
    """빈 줄 정리"""
    # 연속된 <br> 태그 정리
    content = re.sub(r'<br>\s*<br>\s*<br>+', '<br><br>', content)
    content = re.sub(r'<br>\s*<br>\s*<br>', '<br><br>', content)
    
    # 빈 내용 정리
    content = re.sub(r'\|\s*\|\s*\|', '| | |', content)
    
    return content

def fix_duplicate_phone_in_wrong_places(content):
    """잘못된 위치의 전화번호 중복 제거"""
    # 수신번호 카운트 확인에 전화번호 내용이 잘못 들어간 경우 제거
    content = re.sub(
        r'(수신번호 카운트 확인[^<]*<br>\s*- 정상 케이스: 5개 행 중[^<]*<br>\s*)(- 전화번호 최소 9자리 이상[^|]*)',
        r'\1',
        content
    )
    
    # 추가하기 버튼 확인에 전화번호 내용이 잘못 들어간 경우 제거
    content = re.sub(
        r'(추가하기 버튼 확인[^<]*<br>\s*- 비정상 케이스: 전화번호가 입력된 행이 없는 경우[^<]*<br>\s*)(- 전화번호 최소 9자리 이상[^|]*)',
        r'\1',
        content
    )
    
    return content

def fix_template_name_duplicate(content):
    """템플릿명 입력 중복 제거"""
    content = re.sub(
        r'(- 최대 100바이트 \(한글 약 50자, 영문 100자\) 제한 확인<br>\s*- 정상 케이스: \'홍길동\' 입력 시 \'6 / 100 바이트\' 표시 확인 \(한글 1자 = 2바이트\)<br>\s*- 정상 케이스: 영문 50자 입력 시 \'50 / 100 바이트\' 표시 확인<br>\s*- 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 \'입력 가능한 글자수\(100바이트\)를 초과했습니다\' 알림 메시지 노출 확인<br>\s*)(- 최대 100바이트[^<]*<br>\s*- 정상 케이스: \'홍길동\' 입력 시 \'6 / 100 바이트\' 표시 확인<br>\s*- 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인<br>\s*)',
        r'\1',
        content
    )
    
    return content

def process_file(input_file, output_file):
    """파일 처리"""
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Removing duplicate phone content...")
    content = remove_duplicate_phone_content(content)
    
    print("Removing duplicate expressions...")
    content = remove_duplicate_expressions(content)
    
    print("Fixing email input expected result...")
    content = fix_email_input_expected_result(content)
    
    print("Fixing duplicate phone in wrong places...")
    content = fix_duplicate_phone_in_wrong_places(content)
    
    print("Fixing template name duplicate...")
    content = fix_template_name_duplicate(content)
    
    print("Cleaning empty lines...")
    content = clean_empty_lines(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")

if __name__ == '__main__':
    input_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 백업 생성
    backup_file = input_file + '.backup_rewrite_v3'
    print(f"Creating backup: {backup_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    process_file(input_file, output_file)
    print(f"\n원본 파일이 {backup_file}로 백업되었습니다.")
    print(f"수정된 파일이 {output_file}에 저장되었습니다.")
