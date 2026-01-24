#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 시나리오 재작성 스크립트
- 이메일 자동완성 기능 제거
- 모바일/반응형 테스트 제거
- 순번/순서 중복 제거
- 참고 문서 형식에 맞춰 테스트케이스명, 단계별 작업 수행내용, 예상결과 명확하게 작성
- 변수값 글자수 제한, 주소록 그룹명 글자수 제한, 전화번호 최소 9자리 이상 등 포함
"""

import re
import os

def remove_email_autocomplete(content):
    """이메일 자동완성 관련 내용 제거"""
    # 이메일 자동완성 기능 확인 관련 내용 제거
    patterns = [
        r'이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 \(7개\)[^|]*',
        r'\(naver\.com/gmail\.com/icloud\.com/kakao\.com/daum\.net/nate\.com/hanmail\.net\)',
        r"정상 케이스: 'test@naver\.com' 입력 시 자동완성 목록 표시 확인",
        r'이메일 자동완성 기능이 정상작동되어야 함',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    # 이메일 입력 관련 내용을 단순화
    content = re.sub(
        r'이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인[^<]*',
        '이메일 입력 확인',
        content
    )
    
    return content

def remove_mobile_responsive(content):
    """모바일/반응형 관련 내용 제거"""
    patterns = [
        r'반응형: 모바일에서[^|]*',
        r'모바일에서는[^|]*',
        r'모바일에서[^|]*',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    return content

def remove_duplicate_order(content):
    """순번과 순서 중복 제거 (순서만 유지)"""
    # 테이블 헤더에서 순번 제거
    content = re.sub(r'\|\s*순번\s*\|', '|', content)
    
    # 테이블 행에서 순번 컬럼 제거 (첫 번째 숫자 컬럼)
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('|') and '|' in line[1:]:
            parts = line.split('|')
            # 첫 번째와 두 번째가 모두 숫자인 경우 첫 번째 제거
            if len(parts) > 2:
                first = parts[1].strip()
                second = parts[2].strip()
                if first.isdigit() and second.isdigit():
                    # 순번 제거 (첫 번째 숫자 컬럼 제거)
                    parts = [parts[0]] + parts[2:]
                    line = '|'.join(parts)
            result_lines.append(line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def enhance_test_data(content):
    """테스트 데이터 구체화 및 제한사항 추가"""
    # 전화번호 최소 9자리 이상 확인 강화
    content = re.sub(
        r'전화번호.*입력.*확인',
        '전화번호 입력 확인 (최소 9자리 이상, 정상 케이스: 010-1234-5678, 비정상 케이스: 8자리 이하 시 알림 메시지 노출)',
        content
    )
    
    # 변수값 글자수 제한 추가
    content = re.sub(
        r'변수\d+.*입력',
        lambda m: m.group(0) + ' (최대 100바이트, 한글 약 50자, 영문 100자 제한)',
        content
    )
    
    # 주소록 그룹명 글자수 제한 추가
    content = re.sub(
        r'그룹.*명.*입력',
        lambda m: m.group(0) + ' (최대 50자 제한)',
        content
    )
    
    return content

def improve_test_case_format(content):
    """참고 문서 형식에 맞춰 테스트케이스명, 단계별 작업 수행내용, 예상결과 개선"""
    # 단계별 작업 수행내용을 더 구체적으로 작성
    # 예: "- 확인" -> "- [버튼명] 클릭 시 [동작] 확인"
    
    # 예상결과를 더 명확하게 작성
    # 예: "정상작동되어야 함" -> "정상적으로 작동되어야 함"
    
    content = re.sub(
        r'정상작동되어야 함',
        '정상적으로 작동되어야 함',
        content
    )
    
    content = re.sub(
        r'확인',
        lambda m: m.group(0) if '클릭' in m.string[max(0, m.start()-50):m.start()] else m.group(0),
        content
    )
    
    return content

def process_file(input_file, output_file):
    """파일 처리"""
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Removing email autocomplete features...")
    content = remove_email_autocomplete(content)
    
    print("Removing mobile/responsive test cases...")
    content = remove_mobile_responsive(content)
    
    print("Removing duplicate order column...")
    content = remove_duplicate_order(content)
    
    print("Enhancing test data specifications...")
    content = enhance_test_data(content)
    
    print("Improving test case format...")
    content = improve_test_case_format(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")

if __name__ == '__main__':
    input_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세_수정.md'
    
    process_file(input_file, output_file)
