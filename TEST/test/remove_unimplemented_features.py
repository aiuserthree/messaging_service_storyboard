#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 페이지에 구현되지 않은 기능들을 테스트 시나리오에서 제거
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

def remove_unimplemented_features(content):
    """구현되지 않은 기능 제거"""
    
    # 1. 이메일 자동완성 관련 내용 제거 (이미 제거됨)
    # 2. 다른 구현되지 않은 기능들 확인 및 제거
    
    # 변경사항 추적
    changes = []
    
    # 이메일 자동완성 관련 내용이 남아있는지 확인
    if re.search(r'이메일.*도메인.*리스트.*자동완성|도메인.*7개.*모두.*노출|@까지.*입력.*도메인.*7개', content, re.IGNORECASE):
        # 이메일 자동완성 관련 내용 제거
        content = re.sub(
            r'<br>- 이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 \(7개: [^)]+\), @까지 입력 시 도메인 7개 모두 노출[^<]*',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<br>- 이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 \(7개: [^)]+\), @까지 입력 시 도메인 7개 모두 노출, 지원도메인 선택 시 얼럿멘트 노출되지 않도록 처리[^<]*',
            '',
            content,
            flags=re.IGNORECASE
        )
        changes.append("이메일 자동완성 관련 내용 제거")
    
    # 빈 줄 정리
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content, changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_unimplemented'
    
    print("=" * 80)
    print("구현되지 않은 기능 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 구현되지 않은 기능 제거
    print("\n[1] 구현되지 않은 기능 제거 중...")
    content, changes = remove_unimplemented_features(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            if changes:
                print("\n변경 사항:")
                for change in changes:
                    print(f"  - {change}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음 (이미 제거된 것으로 보입니다)")

if __name__ == '__main__':
    main()
