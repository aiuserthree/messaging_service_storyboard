#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 파일 종합 정리 스크립트:
1. 섹션 2, 3, 4의 데이터 수정 (단계별 작업 수행내용과 예상 결과 교정)
2. 섹션 32, 33, 34 중복 제거
3. 섹션 20, 21 순서 수정
4. 전체 중복 항목 제거 및 간소화
5. 순번과 테스트 ID 일관성 정리
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 섹션 2, 3, 4의 데이터 수정
# 원본 데이터를 기반으로 올바르게 수정
def fix_section_234_data():
    """섹션 2, 3, 4의 단계별 작업 수행내용과 예상 결과를 올바르게 수정"""
    global content
    
    # 섹션 2 수정 - 랜딩 페이지
    section2_pattern = r'(## 2\. 메인 > 랜딩 페이지\n.*?)(?=\n## 3\.)'
    section2_match = re.search(section2_pattern, content, re.DOTALL)
    
    if section2_match:
        section2_content = section2_match.group(1)
        lines = section2_content.split('\n')
        new_lines = []
        
        for line in lines:
            if not line.strip() or not line.startswith('|'):
                new_lines.append(line)
                continue
            
            if '---' in line or '순번' in line or '테스트ID' in line:
                new_lines.append(line)
                continue
            
            # 데이터 라인 파싱 및 수정
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 9:
                new_lines.append(line)
                continue
            
            seq = parts[1] if len(parts) > 1 else ''
            test_id = parts[2] if len(parts) > 2 else ''
            order = parts[3] if len(parts) > 3 else ''
            test_case = parts[4] if len(parts) > 4 else ''
            page_popup = parts[5] if len(parts) > 5 else '페이지'
            steps = parts[6] if len(parts) > 6 else ''
            test_data = parts[7] if len(parts) > 7 else '별도 테스트 아이디 없이 진행'
            expected = parts[8] if len(parts) > 8 else ''
            
            # steps와 expected가 뒤바뀌어 있는 경우 수정
            # steps는 "- "로 시작하거나 구체적인 작업 내용
            # expected는 "~되어야함", "~표시됨", "~이동됨" 등의 형식
            
            # 예상 결과 패턴: "~되어야함", "~표시됨", "~이동됨", "~확인됨" 등
            expected_patterns = ['되어야함', '표시됨', '이동됨', '확인됨', '작동됨', '완료됨', '처리됨', '생성됨', '업데이트됨']
            
            # steps가 예상 결과처럼 보이면 교환
            if steps and not steps.startswith('-'):
                if any(pattern in steps for pattern in expected_patterns):
                    steps, expected = expected, steps
                elif '접속' in steps or '클릭' in steps or '입력' in steps:
                    # steps가 실제 작업 내용인 경우
                    if expected and not any(pattern in expected for pattern in expected_patterns):
                        # expected가 작업 내용이면 교환
                        steps, expected = expected, steps
            
            # steps가 "- "로 시작하지 않으면 추가
            if steps and not steps.startswith('-') and steps.strip():
                steps = f"- {steps}"
            
            # 표준 형식으로 재구성
            new_line = f"| {seq} | {test_id} | {order} | {test_case} | {page_popup} | {steps} | {test_data} | {expected} |  |  |  |  |  |  |  |  |  |  |"
            new_lines.append(new_line)
        
        new_section2 = '\n'.join(new_lines)
        content = content[:section2_match.start()] + new_section2 + content[section2_match.end():]
    
    # 섹션 3, 4도 동일하게 처리
    for section_num, section_title in [(3, '로그인'), (4, '메인 > 대시보드')]:
        pattern = rf'(## {section_num}\. {re.escape(section_title)}\n.*?)(?=\n## {section_num+1}\.)'
        match = re.search(pattern, content, re.DOTALL)
        
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
                
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 9:
                    new_lines.append(line)
                    continue
                
                seq = parts[1] if len(parts) > 1 else ''
                test_id = parts[2] if len(parts) > 2 else ''
                order = parts[3] if len(parts) > 3 else ''
                test_case = parts[4] if len(parts) > 4 else ''
                page_popup = parts[5] if len(parts) > 5 else '페이지'
                steps = parts[6] if len(parts) > 6 else ''
                test_data = parts[7] if len(parts) > 7 else '별도 테스트 아이디 없이 진행'
                expected = parts[8] if len(parts) > 8 else ''
                
                expected_patterns = ['되어야함', '표시됨', '이동됨', '확인됨', '작동됨', '완료됨', '처리됨', '생성됨', '업데이트됨']
                
                if steps and not steps.startswith('-'):
                    if any(pattern in steps for pattern in expected_patterns):
                        steps, expected = expected, steps
                    elif '접속' in steps or '클릭' in steps or '입력' in steps:
                        if expected and not any(pattern in expected for pattern in expected_patterns):
                            steps, expected = expected, steps
                
                if steps and not steps.startswith('-') and steps.strip():
                    steps = f"- {steps}"
                
                new_line = f"| {seq} | {test_id} | {order} | {test_case} | {page_popup} | {steps} | {test_data} | {expected} |  |  |  |  |  |  |  |  |  |  |"
                new_lines.append(new_line)
            
            new_section = '\n'.join(new_lines)
            content = content[:match.start()] + new_section + content[match.end():]

# 2. 섹션 32, 33, 34 중복 제거
def remove_duplicate_sections():
    """섹션 32, 33, 34 중복 제거"""
    global content
    
    # 섹션 32, 33, 34 제거
    for section_num in [32, 33, 34]:
        pattern = rf'\n## {section_num}\..*?(?=\n## {section_num+1}\.|$)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)

# 3. 섹션 20, 21 순서 수정
def fix_section_order():
    """섹션 20, 21 순서 수정"""
    global content
    
    # 섹션 20과 21 찾기
    section20_pattern = r'(## 20\. 결제 관리 > 충전하기\n.*?)(?=\n## 21\.)'
    section21_pattern = r'(## 21\. 회원가입\n.*?)(?=\n## 21\. 결제 관리 > 충전 내역|$)'
    section21_2_pattern = r'(## 21\. 결제 관리 > 충전 내역\n.*?)(?=\n## 22\.)'
    
    section20_match = re.search(section20_pattern, content, re.DOTALL)
    section21_match = re.search(section21_pattern, content, re.DOTALL)
    section21_2_match = re.search(section21_2_pattern, content, re.DOTALL)
    
    if section20_match and section21_match and section21_2_match:
        # 섹션 21 (회원가입)을 섹션 20 앞으로 이동
        section21_content = section21_match.group(1)
        section20_content = section20_match.group(1)
        section21_2_content = section21_2_match.group(1)
        
        # 섹션 21을 섹션 19로 변경하고, 섹션 20을 섹션 21로 변경
        section21_content = re.sub(r'## 21\.', '## 20.', section21_content)
        section20_content = re.sub(r'## 20\.', '## 21.', section20_content)
        section21_2_content = re.sub(r'## 21\.', '## 22.', section21_2_content)
        
        # 순서 재배치
        before_section20 = content[:section20_match.start()]
        after_section21_2 = content[section21_2_match.end():]
        
        content = before_section20 + section21_content + '\n' + section20_content + '\n' + section21_2_content + after_section21_2

# 4. 순번과 테스트 ID 일관성 정리
def fix_sequence_and_ids():
    """순번과 테스트 ID 일관성 정리"""
    global content
    
    # 각 섹션별로 순번과 테스트 ID 정리
    sections = re.findall(r'(## \d+\. .*?\n.*?)(?=\n## \d+\.|$)', content, re.DOTALL)
    
    new_content_parts = []
    current_pos = 0
    
    for section in sections:
        section_match = re.search(re.escape(section), content[current_pos:], re.DOTALL)
        if not section_match:
            continue
        
        section_start = current_pos + section_match.start()
        section_end = current_pos + section_match.end()
        
        # 섹션 번호 추출
        section_num_match = re.search(r'## (\d+)\.', section)
        if not section_num_match:
            new_content_parts.append((section_start, section_end, section))
            current_pos = section_end
            continue
        
        section_num = int(section_num_match.group(1))
        lines = section.split('\n')
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
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 3:
                new_lines.append(line)
                continue
            
            # 테스트 ID 형식 확인 및 수정
            test_id = parts[2] if len(parts) > 2 else ''
            test_id_match = re.search(r'TS-(\d+)-(\d+)', test_id)
            
            if test_id_match:
                expected_section = int(test_id_match.group(1))
                expected_seq = int(test_id_match.group(2))
                
                # 섹션 번호가 맞지 않으면 수정
                if expected_section != section_num:
                    new_test_id = f"TS-{section_num:02d}-{seq_num:03d}"
                    parts[2] = new_test_id
                
                # 순번도 수정
                if len(parts) > 1:
                    parts[1] = str(seq_num)
                
                # 순서도 수정
                if len(parts) > 3:
                    parts[3] = str(seq_num)
                
                new_line = '|'.join([''] + parts + [''])
                new_lines.append(new_line)
                seq_num += 1
            else:
                new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        new_content_parts.append((section_start, section_end, new_section))
        current_pos = section_end
    
    # 역순으로 교체 (뒤에서부터 교체하여 인덱스 오류 방지)
    for section_start, section_end, new_section in reversed(new_content_parts):
        content = content[:section_start] + new_section + content[section_end:]

# 실행
print("섹션 2, 3, 4 데이터 수정 중...")
fix_section_234_data()

print("중복 섹션 제거 중...")
remove_duplicate_sections()

print("섹션 순서 수정 중...")
fix_section_order()

print("순번과 테스트 ID 정리 중...")
fix_sequence_and_ids()

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("전체 정리 완료!")
