#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
섹션 2, 3, 4 데이터 수정 스크립트
단계별 작업 수행내용과 예상 결과를 올바르게 배치
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 섹션 2 수정
def fix_section_data(section_num, section_title):
    """섹션 데이터 수정"""
    pattern = rf'## {section_num}\. {re.escape(section_title)}\n(.*?)(?=\n## |$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return content
    
    section_content = match.group(1)
    lines = section_content.split('\n')
    
    new_lines = []
    for line in lines:
        if not line.strip() or not line.startswith('|'):
            new_lines.append(line)
            continue
        
        # 테이블 헤더나 구분선은 그대로
        if '---' in line or '순번' in line or '테스트ID' in line:
            new_lines.append(line)
            continue
        
        # 데이터 라인 파싱
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8:
            new_lines.append(line)
            continue
        
        # 현재: 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과
        # 문제: 단계별 작업 수행내용과 예상 결과가 뒤바뀜
        # 원본 데이터를 찾아서 올바르게 배치
        
        # 원본 파일에서 해당 섹션의 원본 데이터를 찾아야 함
        # 일단 현재 구조를 유지하되, 순서만 수정
        
        seq = parts[1] if len(parts) > 1 else ''
        test_id = parts[2] if len(parts) > 2 else ''
        order = parts[3] if len(parts) > 3 else ''
        test_case = parts[4] if len(parts) > 4 else ''
        page_popup = parts[5] if len(parts) > 5 else '페이지'
        steps = parts[6] if len(parts) > 6 else ''
        test_data = parts[7] if len(parts) > 7 else '별도 테스트 아이디 없이 진행'
        expected = parts[8] if len(parts) > 8 else ''
        
        # steps와 expected가 뒤바뀌어 있음
        # steps는 보통 "- "로 시작하거나 긴 설명
        # expected는 "~되어야함", "~표시됨" 등의 형식
        
        # 간단한 휴리스틱: steps가 예상 결과처럼 보이면 교환
        if steps and not steps.startswith('-') and ('표시' in steps or '이동' in steps or '확인' in steps):
            # 교환
            steps, expected = expected, steps
        
        # 표준 형식으로 재구성
        new_line = f"| {seq} | {test_id} | {order} | {test_case} | {page_popup} | {steps} | {test_data} | {expected} |  |  |  |  |  |  |  |  |  |  |"
        new_lines.append(new_line)
    
    new_section = f"## {section_num}. {section_title}\n" + '\n'.join(new_lines)
    return content[:match.start()] + new_section + content[match.end():]

# 섹션 2, 3, 4 수정
content = fix_section_data(2, '메인 > 랜딩 페이지')
content = fix_section_data(3, '로그인')
content = fix_section_data(4, '메인 > 대시보드')

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("섹션 2, 3, 4 데이터 수정 완료!")
