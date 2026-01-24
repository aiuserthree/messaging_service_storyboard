#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 정리 스크립트:
1. 섹션 11-15 삭제 (중복, 표준 형식 아님)
2. 섹션 35-39를 섹션 11-15로 변경
3. 섹션 2의 테스트 ID를 TS-01-XXX로 수정 (랜딩 페이지는 섹션 1이어야 함)
4. 섹션 3의 테스트 ID를 TS-02-XXX로 수정
5. 섹션 4의 테스트 ID를 TS-03-XXX로 수정
6. 전체 순번과 테스트 ID 최종 정리
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 섹션 11-15 삭제
def remove_sections_11_15():
    """섹션 11-15 삭제 (중복 및 표준 형식 아님)"""
    global content
    
    # 섹션 11-15 삭제
    for section_num in range(11, 16):
        pattern = rf'\n## {section_num}\..*?(?=\n## {section_num+1}\.|$)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)

# 2. 섹션 35-39를 섹션 11-15로 변경
def move_sections_35_39_to_11_15():
    """섹션 35-39를 섹션 11-15로 변경"""
    global content
    
    section_mapping = [
        (35, 11, '카카오톡 > 알림톡 발송'),
        (36, 12, '카카오톡 > 브랜드 메시지 발송'),
        (37, 13, '카카오톡 > 카카오톡 발신 프로필'),
        (38, 14, '카카오톡 > 알림톡 템플릿'),
        (39, 15, '카카오톡 > 브랜드 메시지 템플릿'),
    ]
    
    for old_num, new_num, title in section_mapping:
        # 섹션 헤더 변경
        content = re.sub(
            rf'## {old_num}\. {re.escape(title)}',
            f'## {new_num}. {title}',
            content
        )
        
        # 테스트 ID 변경 (TS-35-XXX -> TS-11-XXX 등)
        content = re.sub(
            rf'TS-{old_num}-(\d+)',
            f'TS-{new_num}-\\1',
            content
        )

# 3. 섹션 2, 3, 4의 테스트 ID 수정
def fix_sections_234_test_ids():
    """섹션 2, 3, 4의 테스트 ID를 올바르게 수정"""
    global content
    
    # 섹션 2: TS-02-XXX -> TS-01-XXX (랜딩 페이지는 섹션 1)
    content = re.sub(r'TS-02-(\d+)', r'TS-01-\1', content)
    content = re.sub(r'## 2\. 메인 > 랜딩 페이지', '## 2. 메인 > 랜딩 페이지', content)
    
    # 섹션 3: TS-03-XXX -> TS-02-XXX (로그인은 섹션 2)
    content = re.sub(r'TS-03-(\d+)', r'TS-02-\1', content)
    
    # 섹션 4: TS-04-XXX -> TS-03-XXX (대시보드는 섹션 3)
    content = re.sub(r'TS-04-(\d+)', r'TS-03-\1', content)
    
    # 섹션 5부터는 이미 올바른 번호를 사용하고 있으므로 그대로 유지

# 4. 전체 순번과 테스트 ID 최종 정리
def final_fix_all_sequence_and_ids():
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

# 5. 섹션 12-15의 표준 형식 변환 (만약 남아있다면)
def convert_sections_12_15_to_standard():
    """섹션 12-15를 표준 형식으로 변환"""
    global content
    
    for section_num in range(12, 16):
        pattern = rf'(## {section_num}\. .*?\n.*?)(?=\n## {section_num+1}\.)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            section_content = match.group(1)
            lines = section_content.split('\n')
            
            # 표준 형식이 아닌 경우 변환
            if '시나리오ID' in section_content and '순번' not in section_content:
                new_lines = []
                header_added = False
                seq_num = 1
                
                for line in lines:
                    if '##' in line:
                        new_lines.append(line)
                        continue
                    
                    if '시나리오ID' in line:
                        # 표준 헤더로 교체
                        new_lines.append('| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과(연계 모듈 점검사항 확인) | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |')
                        new_lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
                        header_added = True
                        continue
                    
                    if '---' in line and header_added:
                        continue
                    
                    if line.startswith('|') and 'TS-' in line:
                        # 데이터 라인 변환
                        parts = [p.strip() for p in line.split('|') if p.strip()]
                        if len(parts) >= 3:
                            test_id = parts[0] if 'TS-' in parts[0] else parts[1]
                            test_case = parts[1] if 'TS-' not in parts[1] else parts[2]
                            steps = parts[2] if len(parts) > 2 else ''
                            expected = parts[3] if len(parts) > 3 else ''
                            
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

# 실행
print("섹션 11-15 삭제 중...")
remove_sections_11_15()

print("섹션 35-39를 섹션 11-15로 이동 중...")
move_sections_35_39_to_11_15()

print("섹션 2, 3, 4 테스트 ID 수정 중...")
fix_sections_234_test_ids()

print("전체 순번과 테스트 ID 최종 정리 중...")
final_fix_all_sequence_and_ids()

print("섹션 12-15 표준 형식 변환 중...")
convert_sections_12_15_to_standard()

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("최종 정리 완료!")
