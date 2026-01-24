#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 시나리오 재작성 스크립트 v2
- 이메일 자동완성 기능 제거
- 모바일/반응형 테스트 제거
- 순번/순서 중복 제거 (순서만 유지)
- 참고 문서 형식에 맞춰 테스트케이스명, 단계별 작업 수행내용, 예상결과 명확하게 작성
- 변수값 글자수 제한, 주소록 그룹명 글자수 제한, 전화번호 최소 9자리 이상 등 포함
"""

import re
import os

def remove_email_autocomplete_detailed(content):
    """이메일 자동완성 관련 내용 상세 제거"""
    # 이메일 자동완성 기능 확인 관련 내용 제거
    patterns_to_remove = [
        r'이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 \(7개\)',
        r'\(naver\.com/gmail\.com/icloud\.com/kakao\.com/daum\.net/nate\.com/hanmail\.net\)',
        r"정상 케이스: 'test@naver\.com' 입력 시 자동완성 목록 표시 확인",
        r'이메일 자동완성 기능이 정상작동되어야 함',
        r'이메일 자동완성 기능이 정상적으로 작동되어야 함',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    # 이메일 입력 관련 내용을 단순화하되 유효성 검사는 유지
    content = re.sub(
        r'이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인[^<]*<br>',
        '',
        content
    )
    
    # 이메일 유효성 검사는 유지하되 자동완성 관련 내용만 제거
    content = re.sub(
        r'<br>\s*\(naver\.com[^<]*\)<br>',
        '<br>',
        content
    )
    
    # 빈 줄 정리
    content = re.sub(r'<br>\s*<br>\s*<br>+', '<br><br>', content)
    content = re.sub(r'<br>\s*-\s*<br>', '<br>', content)
    
    return content

def remove_mobile_responsive_detailed(content):
    """모바일/반응형 관련 내용 상세 제거"""
    patterns = [
        r'<br>\s*- 반응형: 모바일에서[^<]*',
        r'<br>\s*- 모바일에서는[^<]*',
        r'<br>\s*- 모바일에서[^<]*',
        r'반응형: 모바일에서[^|]*',
        r'모바일에서는[^|]*',
        r'모바일에서[^|]*',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    return content

def remove_duplicate_order_column(content):
    """순번과 순서 중복 제거 - 순서만 유지"""
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
                    line = '| ' + ' | '.join(parts) + ' |'
            
            result_lines.append(line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def enhance_test_data_specifications(content):
    """테스트 데이터 구체화 및 제한사항 추가"""
    # 전화번호 최소 9자리 이상 확인 강화
    content = re.sub(
        r'전화번호.*입력.*확인(?!.*최소 9자리)',
        lambda m: m.group(0) + '<br>  - 전화번호 최소 9자리 이상 입력 확인<br>  - 정상 케이스: \'010-1234-5678\' 입력 시 정상 처리 확인<br>  - 정상 케이스: \'01012345678\' 입력 시 자동 하이픈 포맷팅 확인<br>  - 비정상 케이스: 9자리 미만 입력 시 \'전화번호는 최소 9자리 이상 입력해주세요\' 알림 메시지 노출 확인<br>  - 비정상 케이스: 숫자가 아닌 문자 입력 시 자동 제거 또는 알림 메시지 노출 확인',
        content
    )
    
    # 변수값 글자수 제한 추가
    content = re.sub(
        r'(변수\d+.*입력.*확인)(?!.*100바이트)',
        lambda m: m.group(0) + '<br>  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인<br>  - 정상 케이스: 한글 30자 입력 시 \'60 / 100 바이트\' 표시 확인<br>  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인',
        content
    )
    
    # 주소록 그룹명 글자수 제한 추가
    content = re.sub(
        r'(그룹.*명.*입력.*확인)(?!.*50자)',
        lambda m: m.group(0) + '<br>  - 최대 50자 제한 확인<br>  - 정상 케이스: \'테스트그룹\' 입력 시 정상 처리 확인<br>  - 비정상 케이스: 50자 초과 입력 시 \'그룹명은 50자를 초과할 수 없습니다\' 알림 메시지 노출 확인',
        content
    )
    
    # 이름 입력 시 바이트 제한 추가
    content = re.sub(
        r'(이름.*입력.*확인)(?!.*100바이트)',
        lambda m: m.group(0) + '<br>  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인<br>  - 정상 케이스: \'홍길동\' 입력 시 \'6 / 100 바이트\' 표시 확인<br>  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인',
        content
    )
    
    return content

def improve_test_case_format(content):
    """참고 문서 형식에 맞춰 테스트케이스명, 단계별 작업 수행내용, 예상결과 개선"""
    # 단계별 작업 수행내용을 더 구체적으로 작성
    # "- 확인" -> "- [구체적인 동작] 확인"
    
    # 예상결과를 더 명확하게 작성
    content = re.sub(
        r'정상작동되어야 함',
        '정상적으로 작동되어야 함',
        content
    )
    
    content = re.sub(
        r'작동되어야 함',
        '정상적으로 작동되어야 함',
        content
    )
    
    # 이메일 입력 관련 예상결과 수정
    content = re.sub(
        r'이메일.*정상적으로 작동되어야 함',
        '이메일 유효성 검증이 정상적으로 작동되어야 함',
        content
    )
    
    return content

def clean_empty_content(content):
    """빈 내용 정리"""
    # 빈 예상결과 정리
    content = re.sub(r'\|\s*\|\s*\|', '| | |', content)
    
    # 연속된 빈 줄 정리
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    return content

def process_file(input_file, output_file):
    """파일 처리"""
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Removing email autocomplete features...")
    content = remove_email_autocomplete_detailed(content)
    
    print("Removing mobile/responsive test cases...")
    content = remove_mobile_responsive_detailed(content)
    
    print("Removing duplicate order column...")
    content = remove_duplicate_order_column(content)
    
    print("Enhancing test data specifications...")
    content = enhance_test_data_specifications(content)
    
    print("Improving test case format...")
    content = improve_test_case_format(content)
    
    print("Cleaning empty content...")
    content = clean_empty_content(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")

if __name__ == '__main__':
    input_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 백업 생성
    backup_file = input_file + '.backup_rewrite_v2'
    print(f"Creating backup: {backup_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    process_file(input_file, output_file)
    print(f"\n원본 파일이 {backup_file}로 백업되었습니다.")
    print(f"수정된 파일이 {output_file}에 저장되었습니다.")
