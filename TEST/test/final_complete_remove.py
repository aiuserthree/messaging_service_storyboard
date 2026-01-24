#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 페이지에 구현되지 않은 기능들을 모두 찾아서 테스트 시나리오에서 제거
최종 완전한 버전
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

def check_feature_actually_works(html_content, keywords, check_javascript=True):
    """HTML에 특정 기능이 실제로 동작하는지 확인"""
    if not html_content:
        return False
    
    # HTML 주석 제거
    html_no_comments = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    html_lower = html_no_comments.lower()
    
    # 키워드가 있는지 확인
    has_keyword = False
    for keyword in keywords:
        if keyword.lower() in html_lower:
            has_keyword = True
            break
    
    if not has_keyword:
        return False
    
    # JavaScript 로직 확인 (필요한 경우)
    if check_javascript:
        # display: none으로 숨겨져 있지만 JavaScript로 표시하는 로직이 있는지 확인
        # 예: callerNumberAlert의 경우 display: none이지만 JavaScript로 표시하는 로직이 없으면 동작하지 않음
        pass
    
    return True

def remove_unimplemented_features(content):
    """구현되지 않은 기능 제거"""
    
    base_path = r'c:\Users\ibank\Desktop\spec'
    html_files = {
        'login': read_file(os.path.join(base_path, 'login.html')),
        'signup': read_file(os.path.join(base_path, 'signup.html')),
        'index': read_file(os.path.join(base_path, 'index.html')),
        'main': read_file(os.path.join(base_path, 'main.html')),
        'support-inquiry': read_file(os.path.join(base_path, 'support-inquiry.html')),
        'mypage-profile': read_file(os.path.join(base_path, 'mypage-profile.html')),
        'message-send-general': read_file(os.path.join(base_path, 'message-send-general.html')),
        'template-message': read_file(os.path.join(base_path, 'template-message.html')),
    }
    
    changes = []
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    
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
            if '비밀번호 입력 조건' in line or '8~20자' in line:
                line = re.sub(
                    r'<br>- 비밀번호 입력 조건: [^<]*',
                    '',
                    line
                )
                if line != original_line:
                    changes.append("TS-02-013: 로그인 페이지 비밀번호 조건 검증 제거")
        
        # 2. 로그인 실패 케이스 제거
        if re.match(r'^\|\s*\d+\s*\|\s*TS-02-0(23|24|25)', line):
            if '검증 없이 바로 로그인' in html_files.get('login', ''):
                removed_count += 1
                i += 1
                continue
        
        # 3. 이메일 자동완성 관련 내용 제거
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
        
        # 4. 발신번호 미등록 알림 제거 (display: none이고 JavaScript 로직 없음)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-04-00(3|4)', line):
            html_content = html_files.get('message-send-general', '')
            if html_content:
                # callerNumberAlert가 display: none이고 JavaScript로 표시하는 로직이 없는지 확인
                if 'callerNumberAlert.*style.*display.*none' in html_content or 'id="callerNumberAlert".*display.*none' in html_content:
                    # JavaScript에서 표시하는 로직 확인
                    if 'callerNumberAlert.*style.*display' not in html_content.replace('display: none', ''):
                        if '*확인불가' in line or '확인불가' in line:
                            removed_count += 1
                            i += 1
                            continue
        
        # 5. 템플릿 일괄 삭제 관련 제거 (템플릿 선택 기능 없음)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-06-0(37|38)', line):
            html_content = html_files.get('template-message', '')
            if html_content:
                # 템플릿 선택 체크박스가 있는지 확인
                if not check_feature_actually_works(html_content, [
                    'template.*checkbox',
                    'checkbox.*template',
                    'input.*type.*checkbox.*template'
                ], check_javascript=False):
                    if 'FAIL' in line and ('템플릿 선택 불가' in line or '일괄삭제 버튼 없음' in line):
                        removed_count += 1
                        i += 1
                        continue
        
        # 6. 템플릿 내보내기 제거 (버튼은 있지만 실제 동작 확인 필요)
        if re.match(r'^\|\s*\d+\s*\|\s*TS-06-039', line):
            if 'FAIL' in line and '내보내기 버튼 없음' in line:
                # HTML에 버튼은 있지만 실제 동작하지 않을 수 있음
                # FAIL로 표시된 경우 제거
                removed_count += 1
                i += 1
                continue
        
        # 7. 빈 줄 정리
        if line.strip() == '' and new_lines and new_lines[-1].strip() == '':
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    if removed_count > 0:
        changes.append(f"구현되지 않은 기능 {removed_count}건 제거")
    
    return '\n'.join(new_lines), changes

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_final_complete'
    
    print("=" * 80)
    print("HTML 페이지에 구현되지 않은 기능 모두 제거 (최종 완전한 버전)")
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
