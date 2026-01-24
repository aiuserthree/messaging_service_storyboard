#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 완전 정리 스크립트:
1. 파일 끝의 섹션 11-15 중복 제거
2. 섹션 16-31을 섹션 11-26으로 변경
3. 전체 순번과 테스트 ID 일관성 최종 정리
4. 중복 항목 제거 및 간소화
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 파일 끝의 섹션 11-15 중복 제거
def remove_duplicate_sections_at_end():
    """파일 끝의 섹션 11-15 중복 제거"""
    global content
    
    # 섹션 11부터 파일 끝까지 찾기
    section11_pattern = r'\n## 11\. 카카오톡 > 알림톡 발송.*$'
    match = re.search(section11_pattern, content, re.DOTALL)
    
    if match:
        # 섹션 11부터 파일 끝까지 삭제
        content = content[:match.start()]

# 2. 섹션 16-31을 섹션 11-26으로 변경
def renumber_sections_16_31():
    """섹션 16-31을 섹션 11-26으로 변경"""
    global content
    
    section_mapping = [
        (16, 11, '발송 관리 > 발송결과'),
        (17, 12, '발송 관리 > 예약내역'),
        (18, 13, '주소록 > 주소록 관리'),
        (19, 14, '주소록 > 수신거부관리'),
        (20, 15, '회원가입'),
        (21, 16, '결제 관리 > 충전하기'),
        (22, 17, '결제 관리 > 충전 내역'),
        (23, 18, '결제 관리 > 환불'),
        (24, 19, '결제 관리 > 세금계산서 발행'),
        (25, 20, '마이페이지 > 내 정보 수정'),
        (26, 21, '마이페이지 > 비밀번호 변경'),
        (27, 22, '마이페이지 > 발신번호 관리'),
        (28, 23, '고객센터 > 공지사항'),
        (29, 24, '고객센터 > 이벤트'),
        (30, 25, '고객센터 > FAQ'),
        (31, 26, '고객센터 > 1:1 문의'),
    ]
    
    # 역순으로 변경 (뒤에서부터 변경하여 인덱스 오류 방지)
    for old_num, new_num, title in reversed(section_mapping):
        # 섹션 헤더 변경
        content = re.sub(
            rf'## {old_num}\. {re.escape(title)}',
            f'## {new_num}. {title}',
            content
        )
        
        # 테스트 ID 변경
        content = re.sub(
            rf'TS-{old_num}-(\d+)',
            f'TS-{new_num}-\\1',
            content
        )

# 3. 전체 순번과 테스트 ID 일관성 최종 정리
def final_fix_all_ids():
    """전체 순번과 테스트 ID 일관성 최종 정리"""
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
print("파일 끝의 섹션 11-15 중복 제거 중...")
remove_duplicate_sections_at_end()

print("섹션 16-31을 섹션 11-26으로 변경 중...")
renumber_sections_16_31()

print("전체 순번과 테스트 ID 최종 정리 중...")
final_fix_all_ids()

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("최종 정리 완료!")
