#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서들을 기반으로 FO_테스트시나리오_상세.md 파일을 최종 수정:
1. 바이트 계산 오류 수정 (한글 2바이트 -> 3바이트)
2. 누락된 기능 설명 추가 (참고 문서 기반)
3. 중복 제거 및 통합
"""

import re

def read_file(filepath):
    """파일 읽기"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def write_file(filepath, content):
    """파일 쓰기"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def fix_byte_calculation(content):
    """바이트 계산 오류 수정 (한글 2바이트 -> 3바이트)"""
    # 한글 1자 = 2바이트 -> 3바이트로 수정
    content = re.sub(
        r'한글 1자\s*=\s*2바이트',
        '한글 1자 = 3바이트',
        content
    )
    
    # "안녕하세요" (5자) = 10바이트 -> 15바이트로 수정
    content = re.sub(
        r'"안녕하세요" 입력.*?10 / 90 바이트.*?한글 1자\s*=\s*2바이트',
        lambda m: m.group(0).replace('10 / 90 바이트', '15 / 90 바이트').replace('한글 1자 = 2바이트', '한글 1자 = 3바이트'),
        content
    )
    
    # "가나다" (3자) = 6바이트 -> 9바이트로 수정
    content = re.sub(
        r'"가나다" 입력.*?6바이트.*?한글 1자\s*=\s*2바이트',
        lambda m: m.group(0).replace('6바이트', '9바이트').replace('한글 1자 = 2바이트', '한글 1자 = 3바이트'),
        content
    )
    
    # "홍길동" (3자) = 6바이트 -> 9바이트로 수정
    content = re.sub(
        r'"홍길동" 입력.*?6 / 40 바이트.*?한글 1자\s*=\s*2바이트',
        lambda m: m.group(0).replace('6 / 40 바이트', '9 / 40 바이트').replace('한글 1자 = 2바이트', '한글 1자 = 3바이트'),
        content
    )
    
    # "Hello 안녕" 계산 수정: 영문 5바이트 + 한글 2자 = 5 + 6 = 11바이트 (현재 9바이트로 잘못 표시)
    content = re.sub(
        r'"Hello 안녕" 입력.*?9 / 90 바이트.*?영문 5바이트 \+ 한글 4바이트',
        lambda m: m.group(0).replace('9 / 90 바이트', '11 / 90 바이트').replace('영문 5바이트 + 한글 4바이트', '영문 5바이트 + 한글 2자(6바이트)'),
        content
    )
    
    return content

def add_email_autocomplete_detailed(content):
    """이메일 자동완성 상세 설명 추가"""
    # 섹션 2, 3, 20에서 아이디 입력 케이스 찾기
    sections_to_fix = [2, 3, 20]
    
    for section_num in sections_to_fix:
        pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            continue
        
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # 아이디 입력 - 정상 입력 케이스 찾기
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '7개' not in step_content and '도메인' not in step_content:
                        email_desc = "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net)"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {email_desc}"
                        else:
                            step_content = f"- {email_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def add_password_validation_detailed(content):
    """비밀번호 조건 상세 설명 추가"""
    sections_to_fix = [2, 3, 20]
    
    for section_num in sections_to_fix:
        pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            continue
        
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # 비밀번호 입력 - 정상 입력 케이스 찾기
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '8~20자' not in step_content and '8-20자' not in step_content:
                        password_desc = "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {password_desc}"
                        else:
                            step_content = f"- {password_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def add_message_bytes_detailed(content):
    """메시지 바이트 제한 상세 설명 추가"""
    sections_to_fix = [5, 6]
    
    for section_num in sections_to_fix:
        pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            continue
        
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # SMS 선택 케이스
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*SMS 선택', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '90바이트' not in step_content or '한글 약 30자' not in step_content:
                        bytes_desc = "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {bytes_desc}"
                        else:
                            step_content = f"- {bytes_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # LMS 선택 케이스
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*LMS 선택', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '2000바이트' not in step_content or '한글 약 666자' not in step_content:
                        bytes_desc = "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {bytes_desc}"
                        else:
                            step_content = f"- {bytes_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 제목 입력 케이스
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*제목 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '40자' not in step_content:
                        title_desc = "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {title_desc}"
                        else:
                            step_content = f"- {title_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 이름/변수 입력 케이스 (100바이트 제한)
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '100바이트' not in step_content:
                        limit_desc = "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {limit_desc}"
                        else:
                            step_content = f"- {limit_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def add_template_name_limit_detailed(content):
    """템플릿명 제한 상세 설명 추가"""
    sections_to_fix = [7, 8]
    
    for section_num in sections_to_fix:
        pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            continue
        
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # 템플릿명 입력 케이스
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*템플릿명', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '50바이트' not in step_content:
                        limit_desc = "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {limit_desc}"
                        else:
                            step_content = f"- {limit_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def remove_duplicate_lines(content):
    """중복된 라인 제거"""
    lines = content.split('\n')
    new_lines = []
    seen_test_ids = set()
    
    for i, line in enumerate(lines):
        # 테이블 행인 경우
        match = re.match(r'^\|\s*\d+\s*\|\s*(TS-\d+-\d+)\s*\|', line)
        if match:
            test_id = match.group(1)
            
            # 섹션 번호 추출
            section_match = re.search(r'^## (\d+)\.', '\n'.join(new_lines[-10:]), re.MULTILINE)
            if section_match:
                current_section = int(section_match.group(1))
                test_section = int(test_id.split('-')[1])
                
                # 섹션 번호가 일치하지 않으면 제거
                if test_section != current_section:
                    continue
                
                # 중복 체크 (섹션별로)
                key = f"{current_section}_{test_id}"
                if key in seen_test_ids:
                    continue
                seen_test_ids.add(key)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def consolidate_table_edit_cases(content):
    """테이블 직접 편집 케이스 통합"""
    sections_to_fix = [5, 6]
    
    for section_num in sections_to_fix:
        pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            continue
        
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 테이블 직접 편집 관련 연속 케이스 찾기
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', line):
                edit_cases = [line]
                j = i + 1
                
                # 연속된 편집 케이스 수집
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*테이블 직접 편집', lines[j]):
                    edit_cases.append(lines[j])
                    j += 1
                
                # 3개 이상이면 통합
                if len(edit_cases) >= 3:
                    # 첫 번째 케이스를 기준으로 통합
                    base_parts = edit_cases[0].split('|')
                    if len(base_parts) >= 6:
                        # 모든 케이스의 단계별 작업 수행내용 통합
                        all_steps = []
                        for case in edit_cases:
                            case_parts = case.split('|')
                            if len(case_parts) >= 6:
                                step = case_parts[5].strip()
                                if step and step not in all_steps:
                                    all_steps.append(step)
                        
                        if all_steps:
                            base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                            # 테스트케이스명도 통합
                            if len(base_parts) >= 4:
                                base_parts[3] = ' 테이블 직접 편집 (이름, 전화번호, 추가 정보 1/2/3) '
                            # 순번은 첫 번째 것 유지
                            new_lines.append('|'.join(base_parts))
                            i = j
                            continue
            
            new_lines.append(line)
            i += 1
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def add_obituary_notice_limit(content):
    """부고장 알림 내용 100자 제한 추가 (참고 문서 09.md 기반)"""
    # 섹션 31 (고객센터 > 1:1 문의) 또는 부고장 관련 섹션 찾기
    pattern = r'(^## \d+\.\s+[^\n]*부고[^\n]*(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        section = match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # 알림 내용 입력 관련 케이스
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*알림.*내용', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if '100자' not in step_content:
                        limit_desc = "알림 내용 입력: 최대 100자까지 입력 가능, 초과 시 '알림 내용은 최대 100자까지 입력하실 수 있습니다' 얼럿 메시지 표시"
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {limit_desc}"
                        else:
                            step_content = f"- {limit_desc}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup2'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 최종 종합 개선 작업")
    print("=" * 80)
    
    # 파일 읽기
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    # 백업 생성
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 바이트 계산 오류 수정
    print("\n[1] 바이트 계산 오류 수정 중... (한글 2바이트 -> 3바이트)")
    content = fix_byte_calculation(content)
    
    # 2. 이메일 자동완성 상세 설명 추가
    print("[2] 이메일 자동완성 상세 설명 추가 중...")
    content = add_email_autocomplete_detailed(content)
    
    # 3. 비밀번호 조건 상세 설명 추가
    print("[3] 비밀번호 조건 상세 설명 추가 중...")
    content = add_password_validation_detailed(content)
    
    # 4. 메시지 바이트 제한 상세 설명 추가
    print("[4] 메시지 바이트 제한 상세 설명 추가 중...")
    content = add_message_bytes_detailed(content)
    
    # 5. 템플릿명 제한 상세 설명 추가
    print("[5] 템플릿명 제한 상세 설명 추가 중...")
    content = add_template_name_limit_detailed(content)
    
    # 6. 부고장 알림 내용 제한 추가
    print("[6] 부고장 알림 내용 제한 추가 중...")
    content = add_obituary_notice_limit(content)
    
    # 7. 중복 라인 제거
    print("[7] 중복 라인 제거 중...")
    content = remove_duplicate_lines(content)
    
    # 8. 테이블 직접 편집 케이스 통합
    print("[8] 테이블 직접 편집 케이스 통합 중...")
    content = consolidate_table_edit_cases(content)
    
    # 변경사항 저장
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
