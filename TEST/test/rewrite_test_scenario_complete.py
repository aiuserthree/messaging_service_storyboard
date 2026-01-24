#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 시나리오 재작성 스크립트 완전 버전
- 전화번호 중복 완전 제거
- 연락처 입력에서 이메일 내용 제거
- 이메일 입력 형식 정리
"""

import re
import os

def remove_phone_duplicates_complete(content):
    """전화번호 중복 완전 제거"""
    # 전화번호 관련 내용이 여러 번 반복되는 패턴 찾기
    # 최대 3번까지 반복 제거
    for i in range(3):
        pattern = r'(- 전화번호 최소 9자리 이상 입력 확인<br>\s*- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)(- 전화번호 최소 9자리 이상 입력 확인<br>\s*- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)'
        content = re.sub(pattern, r'\1', content, flags=re.MULTILINE)
    
    # 수신번호 카운트 확인에 잘못 들어간 전화번호 내용 제거
    content = re.sub(
        r'(수신번호 카운트 확인[^<]*<br>\s*- 정상 케이스: 5개 행 중[^<]*<br>\s*)(- 전화번호 최소 9자리 이상[^|]*)',
        r'\1',
        content
    )
    
    # 추가하기 버튼 확인에 잘못 들어간 전화번호 내용 제거
    content = re.sub(
        r'(추가하기 버튼 확인[^<]*<br>\s*- 비정상 케이스: 전화번호가 입력된 행이 없는 경우[^<]*<br>\s*)(- 전화번호 최소 9자리 이상[^|]*)',
        r'\1',
        content
    )
    
    return content

def fix_contact_input_email_removal(content):
    """연락처 입력에서 이메일 관련 내용 제거"""
    # 연락처 입력에 이메일 관련 내용이 잘못 들어간 경우 제거
    content = re.sub(
        r'(연락처 입력 확인<br>\s*- 전화번호 최소 9자리 이상 입력 확인<br>\s*- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)(- 비정상 케이스: \'@\'와[^<]*<br>\s*- 비정상 케이스: @앞에[^<]*<br>\s*- 비정상 케이스: \.앞과[^<]*<br>\s*- 비정상 케이스: 한글 텍스트가[^<]*<br>\s*- 비정상 케이스: 입력값이 100자 이상인 경우[^<]*<br>\s*)(\| 이메일 유효성 검증이)',
        r'\1\3',
        content
    )
    
    # 연락처 입력의 예상결과 수정
    content = re.sub(
        r'(\| 연락처 입력 \| 페이지 \|[^|]*\|)\s*이메일 유효성 검증이 정상적으로 작동되어야 함',
        r'\1 전화번호 형식 검증 및 자동 포맷팅이 정상적으로 작동되어야 함',
        content
    )
    
    return content

def fix_email_input_format(content):
    """이메일 입력 형식 정리"""
    # 이메일 입력 확인 후 빈 줄과 이상한 형식 정리
    content = re.sub(
        r'이메일 입력 확인<br>\s*<br>\s*<br>\s*- 비정상',
        '이메일 입력 확인<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>  - 비정상',
        content
    )
    
    # 아이디 입력 그룹/필드 형식 정리
    content = re.sub(
        r'(아이디 입력 (그룹|필드) 확인<br>\s*)<br>\s*<br>\s*- 정상 케이스: \\\'test@example\.com\\\' 입력 시 정상 처리 확인<br><br>\s*\'@\'와',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>  - 비정상 케이스: \'@\'와',
        content
    )
    
    # 아이디 저장 형식 정리
    content = re.sub(
        r'(아이디 저장 확인<br>\s*)<br>\s*<br>\s*- 정상 케이스: \\\'test@example\.com\\\' 입력 시 정상 처리 확인<br>- 비정상 케이스: \'@\'와',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>  - 비정상 케이스: \'@\'와',
        content
    )
    
    # 이메일 입력에 정상 케이스가 없는 경우 추가
    content = re.sub(
        r'(이메일 입력 확인<br>\s*)(- 비정상 케이스:)',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>\2',
        content
    )
    
    return content

def remove_duplicate_phone_in_modal(content):
    """모달 내 전화번호 중복 제거"""
    # 전화번호만 입력 모달에 중복된 전화번호 내용 제거
    content = re.sub(
        r'(전화번호만 입력 모달 확인<br>\s*- 전화번호 최소 9자리 이상 입력 확인<br>\s*- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)(- 최대 10,000건까지 입력 가능 확인<br>\s*)(- 전화번호 최소 9자리 이상 입력 확인<br>\s*- 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>\s*- 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>\s*- 비정상 케이스: 9자리 미만 입력 시[^<]*<br>\s*- 비정상 케이스: 숫자가 아닌 문자 입력 시[^<]*<br>\s*)',
        r'\1\2',
        content
    )
    
    return content

def process_file(input_file, output_file):
    """파일 처리"""
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Removing phone duplicates completely...")
    content = remove_phone_duplicates_complete(content)
    
    print("Fixing contact input email removal...")
    content = fix_contact_input_email_removal(content)
    
    print("Fixing email input format...")
    content = fix_email_input_format(content)
    
    print("Removing duplicate phone in modal...")
    content = remove_duplicate_phone_in_modal(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")

if __name__ == '__main__':
    input_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 백업 생성
    backup_file = input_file + '.backup_rewrite_complete'
    print(f"Creating backup: {backup_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    process_file(input_file, output_file)
    print(f"\n원본 파일이 {backup_file}로 백업되었습니다.")
    print(f"수정된 파일이 {output_file}에 저장되었습니다.")
