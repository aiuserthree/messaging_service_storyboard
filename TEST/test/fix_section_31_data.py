#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
섹션 31 데이터 수정 스크립트
단계별 작업 수행내용과 예상 결과를 올바르게 수정
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 섹션 31 수정
section31_pattern = r'(## 31\. .*?\n.*?)(?=\n---|$)'
match = re.search(section31_pattern, content, re.DOTALL)

if match:
    section_content = match.group(1)
    lines = section_content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip() or not line.startswith('|'):
            new_lines.append(line)
            continue
        
        if '---' in line or '순번' in line or '테스트ID' in line:
            new_lines.append(line)
            continue
        
        # 데이터 라인 파싱 및 수정
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) < 8:
            new_lines.append(line)
            continue
        
        seq = parts[0] if parts[0].isdigit() else ''
        test_id = parts[1] if len(parts) > 1 else ''
        order = parts[2] if len(parts) > 2 else ''
        test_case = parts[3] if len(parts) > 3 else ''
        page_popup = parts[4] if len(parts) > 4 else '페이지'
        steps = parts[5] if len(parts) > 5 else ''
        test_data = parts[6] if len(parts) > 6 else '별도 테스트 아이디 없이 진행'
        expected = parts[7] if len(parts) > 7 else ''
        
        # steps와 expected가 뒤바뀌어 있는 경우 수정
        # steps는 "- "로 시작하거나 구체적인 작업 내용
        # expected는 "~되어야함", "~표시됨", "~이동됨" 등의 형식
        
        expected_patterns = ['되어야함', '표시됨', '이동됨', '확인됨', '작동됨', '완료됨', '처리됨', '생성됨', '업데이트됨', '열려야함', '닫혀야함']
        
        # steps가 예상 결과처럼 보이면 교환
        if steps and not steps.startswith('-'):
            if any(pattern in steps for pattern in expected_patterns):
                steps, expected = expected, steps
            elif '접속' in steps or '클릭' in steps or '입력' in steps or '확인' in steps:
                # steps가 실제 작업 내용인 경우
                if expected and not any(pattern in expected for pattern in expected_patterns):
                    # expected가 작업 내용이면 교환
                    steps, expected = expected, steps
        
        # steps가 "- "로 시작하지 않으면 추가
        if steps and not steps.startswith('-') and steps.strip():
            steps = f"- {steps}"
        
        # 예상 결과가 비어있거나 잘못된 경우 기본값 생성
        if not expected or len(expected) < 5:
            if '접속' in test_case or '로드' in test_case:
                expected = '페이지가 정상적으로 표시되어야함'
            elif '클릭' in test_case:
                expected = '해당 기능이 정상적으로 작동되어야함'
            elif '입력' in test_case:
                expected = '입력한 내용이 정상적으로 표시되어야함'
            elif '확인' in test_case:
                expected = '해당 항목이 정상적으로 표시되어야함'
            else:
                expected = '정상적으로 작동되어야함'
        
        # 표준 형식으로 재구성
        new_line = f"| {seq} | {test_id} | {order} | {test_case} | {page_popup} | {steps} | {test_data} | {expected} |  |  |  |  |  |  |  |  |  |  |"
        new_lines.append(new_line)
    
    new_section = '\n'.join(new_lines)
    content = content[:match.start()] + new_section + content[match.end():]
    
    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("섹션 31 데이터 수정 완료!")
