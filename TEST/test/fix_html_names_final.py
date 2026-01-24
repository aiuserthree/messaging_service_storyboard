#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일명을 페이지명으로 최종 변경
"""

import re

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def fix_html_names_comprehensive(content):
    """HTML 파일명을 페이지명으로 변경 (포괄적)"""
    
    # HTML 파일명 → 페이지명 매핑
    replacements = [
        (r'일반문자\s*발송\.html', '일반문자 발송'),
        (r'광고문자\s*발송\.html', '광고문자 발송'),
        (r'일반문자\s*템플릿\.html', '일반문자 템플릿'),
        (r'광고문자\s*템플릿\.html', '광고문자 템플릿'),
        (r'선거문자\s*발송\.html', '선거문자 발송'),
        (r'선거문자\s*템플릿\.html', '선거문자 템플릿'),
        (r'예약내역\.html', '예약내역'),
        (r'발송결과\.html', '발송결과'),
        (r'주소록\s*관리-reject\.html', '수신거부관리'),
        (r'주소록\s*관리\.html', '주소록 관리'),
        (r'\.html', ''),  # 나머지 .html 제거
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_html_names'
    
    print("=" * 80)
    print("HTML 파일명을 페이지명으로 최종 변경")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # HTML 파일명 변경
    print("\nHTML 파일명을 페이지명으로 변경 중...")
    content = fix_html_names_comprehensive(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
