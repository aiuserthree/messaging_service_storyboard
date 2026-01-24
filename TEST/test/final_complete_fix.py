#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전 최종 정리 스크립트:
1. 섹션 31을 표준 형식으로 변환
2. 파일 끝의 잘못된 형식 라인 제거
3. 전체 순번과 테스트 ID 최종 정리
4. 중복 항목 제거 및 간소화
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 섹션 31을 표준 형식으로 변환
def convert_section_31_to_standard():
    """섹션 31을 표준 형식으로 변환"""
    global content
    
    section31_pattern = r'(## 31\. .*?\n.*?)(?=\n---|$)'
    match = re.search(section31_pattern, content, re.DOTALL)
    
    if match:
        section_content = match.group(1)
        lines = section_content.split('\n')
        
        # 표준 형식이 아닌 경우 변환
        if '시나리오ID' in section_content and '순번' not in section_content:
            new_lines = []
            seq_num = 1
            
            for line in lines:
                if '##' in line:
                    new_lines.append(line)
                    continue
                
                if '시나리오ID' in line:
                    # 표준 헤더로 교체
                    new_lines.append('| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과(연계 모듈 점검사항 확인) | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |')
                    new_lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
                    continue
                
                if '---' in line:
                    continue
                
                if line.startswith('|') and 'TS-' in line:
                    # 데이터 라인 변환
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        test_id = parts[0] if 'TS-' in parts[0] else (parts[1] if 'TS-' in parts[1] else '')
                        test_case = parts[1] if 'TS-' not in parts[1] else (parts[2] if len(parts) > 2 else '')
                        steps = parts[2] if len(parts) > 2 and 'TS-' not in parts[2] else (parts[3] if len(parts) > 3 else '')
                        expected = parts[3] if len(parts) > 3 and 'TS-' not in parts[3] else (parts[4] if len(parts) > 4 else '')
                        
                        # 테스트 ID에서 섹션 번호 추출 및 수정
                        test_id_match = re.search(r'TS-(\d+)-(\d+)', test_id)
                        if test_id_match:
                            old_section = int(test_id_match.group(1))
                            if old_section != 31:
                                test_id = f"TS-31-{int(test_id_match.group(2)):03d}"
                        
                        if not steps.startswith('-'):
                            steps = f"- {steps}"
                        
                        new_line = f"| {seq_num} | {test_id} | {seq_num} | {test_case} | 페이지 | {steps} | 별도 테스트 아이디 없이 진행 | {expected} |  |  |  |  |  |  |  |  |  |  |"
                        new_lines.append(new_line)
                        seq_num += 1
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            new_section = '\n'.join(new_lines)
            content = content[:match.start()] + new_section + content[match.end():]

# 2. 파일 끝의 잘못된 형식 라인 제거
def remove_trailing_invalid_lines():
    """파일 끝의 잘못된 형식 라인 제거"""
    global content
    
    # 섹션 31 이후의 모든 내용 찾기
    section31_pattern = r'(## 31\. .*?\n.*?)(?=\n---|$)'
    match = re.search(section31_pattern, content, re.DOTALL)
    
    if match:
        # 섹션 31의 끝 찾기
        section31_end = match.end()
        
        # 섹션 31 이후의 모든 내용 확인
        remaining = content[section31_end:]
        
        # 표준 형식이 아닌 라인들 제거
        lines = remaining.split('\n')
        new_lines = []
        
        for line in lines:
            # 빈 줄이나 구분선만 유지
            if not line.strip() or line.strip() == '---':
                if not new_lines or new_lines[-1].strip() != line.strip():
                    new_lines.append(line)
            # 표준 형식의 테이블 라인만 유지
            elif line.startswith('|') and 'TS-' in line and '순번' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                # 순번이 있는 표준 형식만 유지
                if len(parts) >= 3 and parts[0].isdigit():
                    new_lines.append(line)
        
        content = content[:section31_end] + '\n'.join(new_lines)

# 3. 전체 순번과 테스트 ID 최종 정리
def final_fix_all_ids():
    """전체 순번과 테스트 ID 최종 정리"""
    global content
    
    # 각 섹션별로 순번과 테스트 ID 정리
    section_pattern = r'(## (\d+)\. .*?\n.*?)(?=\n## \d+\.|$)'
    sections = list(re.finditer(section_pattern, content, re.DOTALL))
    
    replacements = []
    
    for section_match in sections:
        section_content = section_match.group(1)
        section_num = int(section_match.group(2))
        
        lines = section_content.split('\n')
        new_lines = []
        seq_num = 1
        
        for line in lines:
            if not line.strip() or not line.startswith('|'):
                new_lines.append(line)
                continue
            
            if '---' in line or '순번' in line or '테스트ID' in line:
                new_lines.append(line)
                continue
            
            # 테스트 ID 추출 및 순번 수정
            parts = [p.strip() for p in line.split('|') if p.strip()]
            
            if len(parts) < 3:
                new_lines.append(line)
                continue
            
            # 테스트 ID 형식 확인 및 수정
            test_id = parts[1] if len(parts) > 1 else ''
            test_id_match = re.search(r'TS-(\d+)-(\d+)', test_id)
            
            if test_id_match:
                expected_section = int(test_id_match.group(1))
                expected_seq = int(test_id_match.group(2))
                
                # 섹션 번호가 맞지 않으면 수정
                if expected_section != section_num:
                    new_test_id = f"TS-{section_num:02d}-{seq_num:03d}"
                    parts[1] = new_test_id
                
                # 순번도 수정
                parts[0] = str(seq_num)
                
                # 순서도 수정
                if len(parts) > 2:
                    parts[2] = str(seq_num)
                
                new_line = '| ' + ' | '.join(parts) + ' |'
                new_lines.append(new_line)
                seq_num += 1
            else:
                new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        replacements.append((section_match.start(), section_match.end(), new_section))
    
    # 역순으로 교체
    for section_start, section_end, new_section in reversed(replacements):
        content = content[:section_start] + new_section + content[section_end:]

# 실행
print("섹션 31 표준 형식 변환 중...")
convert_section_31_to_standard()

print("파일 끝의 잘못된 형식 라인 제거 중...")
remove_trailing_invalid_lines()

print("전체 순번과 테스트 ID 최종 정리 중...")
final_fix_all_ids()

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("완전 최종 정리 완료!")
