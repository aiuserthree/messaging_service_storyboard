#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 페이지에 구현되지 않은 기능들을 체계적으로 찾아서 테스트 시나리오에서 제거
"""

import re
import os

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

def check_feature_in_html(html_content, feature_keywords):
    """HTML 파일에 특정 기능이 구현되어 있는지 확인"""
    if not html_content:
        return False
    
    html_lower = html_content.lower()
    for keyword in feature_keywords:
        if keyword.lower() in html_lower:
            return True
    return False

def check_password_validation(html_content):
    """비밀번호 조건 검증 기능 확인"""
    keywords = [
        '8~20자', '8-20자', '영문.*숫자.*특수문자',
        'password.*validation', '비밀번호.*조건',
        '영문.*숫자.*특수문자.*조합'
    ]
    return check_feature_in_html(html_content, keywords)

def check_email_autocomplete(html_content):
    """이메일 자동완성 기능 확인"""
    keywords = [
        'email.*autocomplete', '도메인.*리스트',
        'naver.com.*gmail.com', '7개.*도메인',
        '@까지.*입력.*도메인'
    ]
    return check_feature_in_html(html_content, keywords)

def check_email_duplicate_check(html_content):
    """이메일 중복 확인 기능 확인"""
    keywords = [
        '중복확인', 'duplicate.*check', 'checkDuplicate',
        'checkEmail', 'checkIndividualUserId',
        'checkBusinessUserId', 'checkElectionUserId'
    ]
    return check_feature_in_html(html_content, keywords)

def remove_unimplemented_features_from_scenario(content):
    """테스트 시나리오에서 구현되지 않은 기능 제거"""
    
    # HTML 파일들 읽기
    html_files = {
        'login': read_file(r'c:\Users\ibank\Desktop\spec\login.html'),
        'signup': read_file(r'c:\Users\ibank\Desktop\spec\signup.html'),
        'support-inquiry': read_file(r'c:\Users\ibank\Desktop\spec\support-inquiry.html'),
        'mypage-profile': read_file(r'c:\Users\ibank\Desktop\spec\mypage-profile.html'),
    }
    
    changes = []
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        # 로그인 페이지 관련 (TS-02)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-02-', line):
            # 비밀번호 조건 검증 제거 (HTML에 구현되지 않음)
            if '비밀번호 입력 조건' in line or '8~20자' in line or '영문, 숫자, 특수문자' in line:
                # 비밀번호 조건 관련 내용 제거
                if not check_password_validation(html_files['login']):
                    # <br> 태그로 연결된 비밀번호 조건 설명 제거
                    line = re.sub(
                        r'<br>- 비밀번호 입력 조건: [^<]*',
                        '',
                        line
                    )
                    if line != original_line:
                        changes.append(f"로그인 페이지 비밀번호 조건 검증 제거: {line[:50]}...")
        
        # 회원가입 페이지 관련 (TS-20)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-20-', line):
            # 비밀번호 조건 검증 제거
            if '비밀번호 입력 조건' in line or '8~20자' in line:
                if not check_password_validation(html_files['signup']):
                    line = re.sub(
                        r'<br>- 비밀번호 입력 조건: [^<]*',
                        '',
                        line
                    )
                    if line != original_line:
                        changes.append(f"회원가입 페이지 비밀번호 조건 검증 제거: {line[:50]}...")
        
        # 이메일 자동완성 관련 내용 제거 (이미 대부분 제거되었지만 남은 것들 확인)
        if '이메일.*도메인.*리스트.*자동완성' in line or '7개.*도메인' in line:
            if not check_email_autocomplete(html_files.get('login', '') + html_files.get('signup', '')):
                # 해당 라인 전체 제거 또는 내용 수정
                if re.match(r'^\|\s*\d+\s*\|\s*TS-', line):
                    # 테스트 케이스가 자동완성만 테스트하는 경우 라인 제거
                    if '자동완성' in line and '정상 입력' not in line:
                        continue  # 라인 제거
                    else:
                        # 자동완성 관련 내용만 제거
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
                            changes.append(f"이메일 자동완성 관련 내용 제거: {line[:50]}...")
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines), changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_check_unimplemented'
    
    print("=" * 80)
    print("HTML 페이지에 구현되지 않은 기능 제거")
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
    content, changes = remove_unimplemented_features_from_scenario(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            if changes:
                print(f"\n변경 사항 ({len(changes)}건):")
                for i, change in enumerate(changes[:10], 1):  # 최대 10개만 표시
                    print(f"  {i}. {change}")
                if len(changes) > 10:
                    print(f"  ... 외 {len(changes) - 10}건")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
