#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 시나리오 재작성 스크립트 최종 버전
- 전화번호 중복 완전 제거
- 이메일 입력 정상 케이스 추가
- 순번/순서 중복 제거 (순서만 유지)
"""

import re
import os

def remove_duplicate_phone_completely(content):
    """전화번호 관련 중복 내용 완전 제거"""
    # 전화번호 관련 내용이 두 번 반복되는 패턴 찾기
    # 패턴: 전화번호 최소 9자리... (반복)
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

def add_email_normal_case(content):
    """이메일 입력에 정상 케이스 추가"""
    # 이메일 입력 확인 후 바로 비정상 케이스가 나오는 경우 정상 케이스 추가
    content = re.sub(
        r'(이메일 입력 확인<br>\s*)(- 비정상 케이스:)',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>\2',
        content
    )
    
    # 이메일 입력 확인 후 빈 줄이 있는 경우 정리
    content = re.sub(
        r'이메일 입력 확인<br>\s*<br>\s*<br>\s*- 비정상',
        '이메일 입력 확인<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>  - 비정상',
        content
    )
    
    # 아이디 입력 그룹/필드에도 동일하게 적용
    content = re.sub(
        r'(아이디 입력 (그룹|필드) 확인<br>\s*)(<br>\s*)(- 비정상 케이스:)',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>\3',
        content
    )
    
    # 아이디 저장에도 동일하게 적용
    content = re.sub(
        r'(아이디 저장 확인<br>\s*)(<br>\s*)(- 비정상 케이스:)',
        r'\1<br>  - 정상 케이스: \'test@example.com\' 입력 시 정상 처리 확인<br>\3',
        content
    )
    
    return content

def fix_email_expected_result(content):
    """이메일 입력 예상결과 추가"""
    # 예상결과가 비어있는 이메일 입력 항목에 추가
    content = re.sub(
        r'(\| 이메일 입력 \| 페이지 \|[^|]*\|)\s*\|',
        r'\1 이메일 유효성 검증이 정상적으로 작동되어야 함 |',
        content
    )
    
    content = re.sub(
        r'(\| 아이디 입력 (그룹|필드) \| 페이지 \|[^|]*\|)\s*\|',
        r'\1 이메일 유효성 검증이 정상적으로 작동되어야 함 |',
        content
    )
    
    content = re.sub(
        r'(\| 아이디 저장 (입력|확인) \| 페이지 \|[^|]*\|)\s*\|',
        r'\1 이메일 유효성 검증이 정상적으로 작동되어야 함 |',
        content
    )
    
    return content

def remove_duplicate_order_column_final(content):
    """순번과 순서 중복 제거 - 순서만 유지 (최종)"""
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('|') and '|' in line[1:]:
            parts = [p.strip() for p in line.split('|')]
            # 빈 문자열 제거
            parts = [p for p in parts if p]
            
            # 첫 번째와 두 번째가 모두 숫자인 경우 (순번과 순서)
            # 첫 번째 숫자(순번) 제거
            if len(parts) >= 3:
                first = parts[0] if len(parts) > 0 else ''
                second = parts[1] if len(parts) > 1 else ''
                
                # 순번과 순서가 모두 숫자인 경우 순번 제거
                if first.isdigit() and second.isdigit():
                    # 순번 제거 (첫 번째 숫자 컬럼 제거)
                    parts = parts[1:]
                    # 테이블 형식으로 재구성
                    line = '| ' + ' | '.join(parts) + ' |'
                elif first.isdigit() and not second.isdigit():
                    # 첫 번째만 숫자이고 두 번째가 숫자가 아닌 경우 (이미 순번만 있는 경우)
                    # 그대로 유지
                    pass
            
            result_lines.append(line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def remove_duplicate_expressions_final(content):
    """중복 표현 최종 제거"""
    content = re.sub(r'정상적으로\s+정상적으로', '정상적으로', content)
    content = re.sub(r'작동되어야\s+작동되어야', '작동되어야 함', content)
    
    return content

def clean_duplicate_content(content):
    """중복 내용 정리"""
    # 엑셀 업로드 중복 제거
    content = re.sub(
        r'(- 최대 50,000건까지 업로드 가능 확인<br>\s*)(- 최대 50,000건까지 업로드 가능 확인<br>\s*)',
        r'\1',
        content
    )
    
    # 템플릿명 입력 중복 제거
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
    
    print("Removing duplicate phone content completely...")
    content = remove_duplicate_phone_completely(content)
    
    print("Adding email normal case...")
    content = add_email_normal_case(content)
    
    print("Fixing email expected result...")
    content = fix_email_expected_result(content)
    
    print("Removing duplicate order column...")
    content = remove_duplicate_order_column_final(content)
    
    print("Removing duplicate expressions...")
    content = remove_duplicate_expressions_final(content)
    
    print("Cleaning duplicate content...")
    content = clean_duplicate_content(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")

if __name__ == '__main__':
    input_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 백업 생성
    backup_file = input_file + '.backup_rewrite_final'
    print(f"Creating backup: {backup_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    process_file(input_file, output_file)
    print(f"\n원본 파일이 {backup_file}로 백업되었습니다.")
    print(f"수정된 파일이 {output_file}에 저장되었습니다.")
