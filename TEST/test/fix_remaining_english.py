#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
남은 영어 용어 및 함수명 제거/변경
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

def fix_remaining_terms(content):
    """남은 영어 용어 및 함수명 처리"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 남은 모달 관련
        line = re.sub(r'모달에서', '팝업창에서', line)
        line = re.sub(r'모달\s*또는', '팝업창 또는', line)
        
        # 함수명 제거
        line = re.sub(r'closeModal\([^)]*\)', '팝업창 닫기', line)
        line = re.sub(r'confirmAddRecipients\(\)', '확인', line)
        line = re.sub(r'openAddRecipientModal', '수신번호 추가 팝업창 열기', line)
        
        # FAQ → 자주 묻는 질문
        line = re.sub(r'\bFAQ\b', '자주 묻는 질문', line)
        
        # 레이블 → 항목명
        line = re.sub(r'\b레이블\b', '항목명', line)
        
        # 중복 표현 정리
        line = re.sub(r'팝업창\s*팝업', '팝업창', line)
        line = re.sub(r'팝업창\s*열기\s*팝업창', '팝업창', line)
        
        # 불필요한 함수 호출 표현 제거
        line = re.sub(r'•\s*closeModal\(', '• ', line)
        line = re.sub(r'•\s*confirmAddRecipients\(\)', '• ', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_fix_remaining'
    
    print("=" * 80)
    print("남은 영어 용어 및 함수명 처리")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 용어 변경
    print("\n남은 영어 용어 및 함수명 처리 중...")
    content = fix_remaining_terms(content)
    
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
