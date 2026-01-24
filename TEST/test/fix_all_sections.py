#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 섹션 정리 스크립트:
1. 섹션 2, 3, 4를 표준 형식으로 변환
2. 중복 섹션 제거 (섹션 19와 31 중복)
3. 섹션 순서 정리
4. 순번과 테스트 ID 정리
5. 표준 형식 통일
"""

import re
import os

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 섹션 2, 3, 4를 표준 형식으로 변환
def convert_section_to_standard(section_num, section_title, old_content):
    """섹션을 표준 형식으로 변환"""
    lines = old_content.strip().split('\n')
    if not lines:
        return old_content
    
    # 헤더 라인 찾기
    header_line = None
    data_start_idx = None
    for i, line in enumerate(lines):
        if '시나리오ID' in line or '테스트ID' in line:
            header_line = i
            data_start_idx = i + 2
            break
    
    if header_line is None:
        return old_content
    
    # 표준 헤더 생성
    standard_header = '| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과(연계 모듈 점검사항 확인) | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |'
    standard_separator = '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'
    
    # 데이터 라인 파싱
    new_lines = []
    seq_num = 1
    
    for i in range(data_start_idx, len(lines)):
        line = lines[i].strip()
        if not line or not line.startswith('|'):
            continue
        
        # TS-XX-XXX 형식 찾기
        match = re.search(r'TS-(\d+)-(\d+)', line)
        if match:
            test_id = f"TS-{match.group(1)}-{match.group(2).zfill(3)}"
            order = match.group(2)
        else:
            continue
        
        # 기존 컬럼 추출
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 5:
            continue
        
        # 표준 형식으로 변환
        test_case_name = parts[2] if len(parts) > 2 else ''
        page_popup = '페이지' if '팝업' not in test_case_name else '팝업'
        steps = parts[3] if len(parts) > 3 else ''
        expected = parts[4] if len(parts) > 4 else ''
        
        # 단계별 작업 수행내용을 표준 형식으로 변환
        if steps and not steps.startswith('-'):
            steps = f"- {steps}"
        
        new_line = f"| {seq_num} | {test_id} | {order} | {test_case_name} | {page_popup} | {steps} | 별도 테스트 아이디 없이 진행 | {expected} |  |  |  |  |  |  |  |  |  |  |"
        new_lines.append(new_line)
        seq_num += 1
    
    # 섹션 재구성
    section_header = f"## {section_num}. {section_title}"
    result = section_header + '\n' + standard_header + '\n' + standard_separator + '\n'
    result += '\n'.join(new_lines)
    
    return result

# 섹션 2 변환
section2_match = re.search(r'## 2\. 랜딩 페이지\n(.*?)(?=\n## 3\.|$)', content, re.DOTALL)
if section2_match:
    section2_content = section2_match.group(1)
    new_section2 = convert_section_to_standard(2, '메인 > 랜딩 페이지', section2_content)
    content = content[:section2_match.start()] + new_section2 + content[section2_match.end():]

# 섹션 3 변환
section3_match = re.search(r'## 3\. 로그인 페이지\n(.*?)(?=\n## 4\.|$)', content, re.DOTALL)
if section3_match:
    section3_content = section3_match.group(1)
    new_section3 = convert_section_to_standard(3, '로그인', section3_content)
    content = content[:section3_match.start()] + new_section3 + content[section3_match.end():]

# 섹션 4 변환
section4_match = re.search(r'## 4\. 메인 대시보드\n(.*?)(?=\n## 5\.|$)', content, re.DOTALL)
if section4_match:
    section4_content = section4_match.group(1)
    new_section4 = convert_section_to_standard(4, '메인 > 대시보드', section4_content)
    content = content[:section4_match.start()] + new_section4 + content[section4_match.end():]

# 섹션 31 (중복) 삭제
section31_match = re.search(r'\n## 31\. 주소록 > 수신거부관리\n.*?(?=\n## 32\.|$)', content, re.DOTALL)
if section31_match:
    content = content[:section31_match.start()] + content[section31_match.end():]

# 섹션 32, 33, 34가 이미 추가되어 있는지 확인
if '## 35. 카카오톡 > 알림톡 발송' not in content:
    # 섹션 35-39 추가
    with open(r'c:\Users\ibank\Desktop\spec\TEST\test\add_sections_35_39.md', 'r', encoding='utf-8') as f:
        new_sections = f.read()
    
    # 파일 끝에 추가
    content = content.rstrip() + '\n\n' + new_sections

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("파일 정리 완료!")
