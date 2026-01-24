#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 페이지에 구현되지 않은 기능들을 모두 찾아서 테스트 시나리오에서 제거
체계적으로 각 페이지별로 확인
"""

import re
import os

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def check_feature_in_html(html_content, keywords):
    """HTML에 특정 기능이 있는지 확인"""
    if not html_content:
        return False
    html_lower = html_content.lower()
    for keyword in keywords:
        if keyword.lower() in html_lower:
            return True
    return False

def remove_unimplemented_features(content):
    """구현되지 않은 기능 제거"""
    
    # HTML 파일들 읽기
    html_files = {
        'login': read_file(r'c:\Users\ibank\Desktop\spec\login.html'),
        'signup': read_file(r'c:\Users\ibank\Desktop\spec\signup.html'),
        'index': read_file(r'c:\Users\ibank\Desktop\spec\index.html'),
        'support-inquiry': read_file(r'c:\Users\ibank\Desktop\spec\support-inquiry.html'),
        'mypage-profile': read_file(r'c:\Users\ibank\Desktop\spec\mypage-profile.html'),
    }
    
    changes = []
    lines = content.split('\n')
    new_lines = []
    removed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        # 테이블 행인 경우에만 처리
        if not re.match(r'^\|', line):
            new_lines.append(line)
            i += 1
            continue
        
        # 1. 로그인 페이지 (TS-02) - 비밀번호 조건 검증 제거
        if re.match(r'^\|\s*\d+\s*\|\s*TS-02-013', line):
            if '비밀번호 입력 조건' in line or '8~20자' in line or '영문, 숫자, 특수문자.*조합' in line:
                line = re.sub(
                    r'<br>- 비밀번호 입력 조건: [^<]*',
                    '',
                    line
                )
                if line != original_line:
                    changes.append("TS-02-013: 로그인 페이지 비밀번호 조건 검증 제거")
        
        # 2. 로그인 실패 케이스 제거 (검증 없이 바로 로그인 처리)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-02-0(23|24|25)', line):
            # HTML 확인: "아이디, 비밀번호 검증 없이 바로 로그인"
            if '검증 없이 바로 로그인' in html_files.get('login', ''):
                removed_lines.append(f"제거: {line[:80]}...")
                i += 1
                continue
        
        # 3. 이메일 자동완성 관련 내용 제거
        if '이메일.*도메인.*리스트.*자동완성' in line or '7개.*도메인.*모두.*노출' in line or '@까지.*입력.*도메인.*7개' in line:
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
        
        # 4. 빈 줄 정리
        if line.strip() == '' and new_lines and new_lines[-1].strip() == '':
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    if removed_lines:
        changes.append(f"로그인 실패 케이스 {len(removed_lines)}건 제거 (실제 검증 없음)")
        for removed in removed_lines[:3]:  # 처음 3개만 표시
            changes.append(f"  - {removed}")
    
    return '\n'.join(new_lines), changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final_remove'
    
    print("=" * 80)
    print("HTML 페이지에 구현되지 않은 기능 모두 제거 (최종)")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 구현되지 않은 기능 제거
    print("\n[1] HTML 파일 확인 및 구현되지 않은 기능 제거 중...")
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
