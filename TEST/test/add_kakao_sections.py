#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카카오톡 발송 섹션 추가 스크립트
"""

import re

file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
add_sections_file = r'c:\Users\ibank\Desktop\spec\TEST\test\add_sections_35_39.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(add_sections_file, 'r', encoding='utf-8') as f:
    kakao_sections = f.read()

# 섹션 10 다음에 카카오톡 발송 섹션 추가
section10_pattern = r'(## 10\. .*?\n.*?)(?=\n## 16\.)'
match = re.search(section10_pattern, content, re.DOTALL)

if match:
    # 카카오톡 섹션을 섹션 11-15로 변경
    kakao_content = kakao_sections
    
    # 섹션 번호 변경
    kakao_content = re.sub(r'## 35\.', '## 11.', kakao_content)
    kakao_content = re.sub(r'## 36\.', '## 12.', kakao_content)
    kakao_content = re.sub(r'## 37\.', '## 13.', kakao_content)
    kakao_content = re.sub(r'## 38\.', '## 14.', kakao_content)
    kakao_content = re.sub(r'## 39\.', '## 15.', kakao_content)
    
    # 테스트 ID 변경
    kakao_content = re.sub(r'TS-35-', 'TS-11-', kakao_content)
    kakao_content = re.sub(r'TS-36-', 'TS-12-', kakao_content)
    kakao_content = re.sub(r'TS-37-', 'TS-13-', kakao_content)
    kakao_content = re.sub(r'TS-38-', 'TS-14-', kakao_content)
    kakao_content = re.sub(r'TS-39-', 'TS-15-', kakao_content)
    
    # 섹션 10 다음에 삽입
    content = content[:match.end()] + '\n\n' + kakao_content + '\n\n' + content[match.end():]
    
    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("카카오톡 발송 섹션 추가 완료!")
