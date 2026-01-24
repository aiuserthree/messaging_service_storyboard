#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 페이지에 구현되지 않은 기능들을 모두 찾아서 테스트 시나리오에서 제거
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
    
    changes = []
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        original_line = line
        
        # 1. 로그인 페이지 (TS-02) - 비밀번호 조건 검증 제거 (HTML에 없음)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-02-013', line):
            # 비밀번호 입력 조건 관련 내용 제거
            if '비밀번호 입력 조건' in line or '8~20자' in line:
                line = re.sub(
                    r'<br>- 비밀번호 입력 조건: [^<]*',
                    '',
                    line
                )
                if line != original_line:
                    changes.append("TS-02-013: 로그인 페이지 비밀번호 조건 검증 제거")
        
        # 2. 이메일 자동완성 관련 내용 제거 (이미 대부분 제거되었지만 남은 것들)
        if '이메일.*도메인.*리스트.*자동완성' in line or '7개.*도메인.*모두.*노출' in line:
            line = re.sub(
                r'<br>- 이메일 입력 시, 이메일 도메인리스트 자동완성[^<]*',
                '',
                line
            )
            line = re.sub(
                r'<br>- 이메일 도메인리스트 자동완성[^<]*',
                '',
                line
            )
            if line != original_line:
                changes.append("이메일 자동완성 관련 내용 제거")
        
        # 3. 빈 줄 정리
        if line.strip() == '' and new_lines and new_lines[-1].strip() == '':
            continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_all_unimplemented'
    
    print("=" * 80)
    print("HTML 페이지에 구현되지 않은 기능 모두 제거")
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
                print(f"\n변경 사항 ({len(changes)}건):")
                for i, change in enumerate(changes, 1):
                    print(f"  {i}. {change}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
