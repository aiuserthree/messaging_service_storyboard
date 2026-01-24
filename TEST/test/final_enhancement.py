#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
참고 문서와 화면설계를 기반으로 FO_테스트시나리오_상세.md 최종 보완:
1. 섹션 31 (1:1 문의) 상세 내용 보완
2. 참고 문서 기반 누락 기능 설명 추가
3. 같은 영역의 세분화된 항목 통합
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

def enhance_section31(content):
    """섹션 31 (1:1 문의) 상세 내용 보완"""
    section_pattern = r'(^## 31\.\s+고객센터 > 1:1 문의(?:\n[^#].*?)*?)(?=^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    
    # 현재 섹션의 간소화된 내용을 참고 문서 기반으로 상세하게 보완
    new_section_lines = [
        "## 31. 고객센터 > 1:1 문의",
        "| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과(연계 모듈 점검사항 확인) | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        "| 1 | TS-31-001 | 1 | 페이지 로드 | 페이지 | - 1:1 문의 페이지 접속<br>- 페이지 제목 '고객센터'와 설명이 표시되는지 확인<br>- 문의하기/문의내역 탭이 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | 1:1 문의 페이지가 정상적으로 표시되고, 페이지 제목 '고객센터'와 설명이 표시되어야함 |",
        "| 2 | TS-31-002 | 2 | 로그인 상태 확인 | 페이지 | - 로그인 상태에서 1:1 문의 페이지 접속<br>- 로그인 사용자 아이디가 자동으로 표시되는지 확인 | 로그인 상태 | 로그인 사용자 아이디가 자동으로 표시되어야함 |",
        "| 3 | TS-31-003 | 3 | 비로그인 접근 | 페이지 | - 비로그인 상태에서 1:1 문의 페이지 접속<br>- 로그인 페이지로 자동 이동되는지 확인 | 비로그인 상태 | 로그인 페이지로 자동 이동되어야함 |",
        "| 4 | TS-31-004 | 4 | 탭 메뉴 - 문의하기 탭 | 페이지 | - '문의하기' 탭 클릭<br>- 문의 작성 폼이 표시되는지 확인<br>- 탭이 활성화 상태로 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | 문의 작성 폼이 표시되고, 탭이 활성화 상태로 표시되어야함 |",
        "| 5 | TS-31-005 | 5 | 탭 메뉴 - 문의내역 탭 | 페이지 | - '문의내역' 탭 클릭<br>- 문의 내역 테이블이 표시되는지 확인<br>- 탭이 활성화 상태로 표시되는지 확인 | 로그인 상태 | 문의 내역 테이블이 표시되고, 탭이 활성화 상태로 표시되어야함 |",
        "| 6 | TS-31-006 | 6 | 아이디 필드 | 페이지 | - 아이디 필드 확인<br>- 로그인 사용자 아이디가 자동으로 표시되는지 확인<br>- 아이디 필드 클릭/입력 시도 시 수정 불가능한지 확인 | 로그인 상태 | 로그인 사용자 아이디가 자동으로 표시되고, 수정 불가능해야함 (읽기전용) |",
        "| 7 | TS-31-007 | 7 | 이메일 입력 - 아이디 부분 | 페이지 | - 이메일 아이디(@ 앞부분) 입력<br>- 입력한 내용이 정상적으로 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | 입력한 내용이 정상적으로 표시되어야함 |",
        "| 8 | TS-31-008 | 8 | 이메일 입력 - 도메인 선택 | 페이지 | - 이메일 도메인 선택 드롭다운 확인<br>- 네이버, Gmail, 다음, 직접입력 옵션이 표시되는지 확인<br>- 각 옵션 선택 시 도메인이 자동 입력되는지 확인 | 별도 테스트 아이디 없이 진행 | 네이버, Gmail, 다음, 직접입력 옵션이 표시되고, 각 옵션 선택 시 도메인이 자동 입력되어야함 |",
        "| 9 | TS-31-009 | 9 | 이메일 입력 - 직접입력 | 페이지 | - '직접입력' 선택<br>- 도메인 입력 필드가 활성화되는지 확인<br>- 도메인 직접 입력 가능한지 확인 | 별도 테스트 아이디 없이 진행 | 도메인 입력 필드가 활성화되고, 도메인 직접 입력이 가능해야함 |",
        "| 10 | TS-31-010 | 10 | 이메일 유효성 검사 | 페이지 | - 이메일 형식이 올바르지 않은 경우<br>- '올바른 이메일 형식이 아닙니다' 오류 메시지가 표시되는지 확인 | 잘못된 이메일 형식 | '올바른 이메일 형식이 아닙니다' 오류 메시지가 표시되어야함 |",
        "| 11 | TS-31-011 | 11 | 문의유형 선택 | 페이지 | - 문의유형 선택 드롭다운 확인<br>- 관리자 등록 공통코드명이 노출조건에 따라 선택가능한 문의 유형 항목으로 노출되는지 확인 (가격문의/서비스문의/기술문의/기타 등)<br>- 문의유형 선택 시 선택된 값이 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | 관리자 등록 공통코드명이 노출조건에 따라 선택가능한 문의 유형 항목으로 노출되고, 선택 시 선택된 값이 표시되어야함 |",
        "| 12 | TS-31-012 | 12 | 제목 입력 | 페이지 | - 제목 입력 필드 확인<br>- placeholder '제목을 입력해주세요'가 표시되는지 확인<br>- 제목 입력 시 입력한 내용이 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | placeholder '제목을 입력해주세요'가 표시되고, 제목 입력 시 입력한 내용이 표시되어야함 |",
        "| 13 | TS-31-013 | 13 | 문의내용 입력 | 페이지 | - 문의내용 입력 필드 확인<br>- placeholder '문의 내용을 입력해주세요'가 표시되는지 확인<br>- 문의내용 입력 시 입력한 내용이 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | placeholder '문의 내용을 입력해주세요'가 표시되고, 문의내용 입력 시 입력한 내용이 표시되어야함 |",
        "| 14 | TS-31-014 | 14 | 첨부파일 - 파일 선택 | 페이지 | - '찾아보기' 버튼 클릭<br>- 파일 선택 다이얼로그가 열리는지 확인<br>- 파일 선택 시 파일명이 표시되는지 확인 | 별도 테스트 아이디 없이 진행 | 파일 선택 다이얼로그가 열리고, 파일 선택 시 파일명이 표시되어야함 |",
        "| 15 | TS-31-015 | 15 | 첨부파일 - 파일 형식 제한 | 페이지 | - 지원하지 않는 파일 형식 선택<br>- '지원하지 않는 파일 형식입니다' 오류 메시지가 표시되는지 확인<br>- 업로드되지 않는지 확인 | 지원하지 않는 파일 형식 | '지원하지 않는 파일 형식입니다' 오류 메시지가 표시되고 업로드되지 않아야함 |",
        "| 16 | TS-31-016 | 16 | 첨부파일 - 파일 용량 제한 | 페이지 | - 5MB를 초과하는 파일 선택<br>- '파일 크기가 5MB를 초과합니다' 오류 메시지가 표시되는지 확인<br>- 업로드되지 않는지 확인 | 5MB를 초과하는 파일 | '파일 크기가 5MB를 초과합니다' 오류 메시지가 표시되고 업로드되지 않아야함 |",
        "| 17 | TS-31-017 | 17 | 개인정보 동의 | 페이지 | - 개인정보 수집 및 이용 동의 체크박스 확인<br>- 체크박스 선택/해제 기능 확인<br>- 체크박스 미체크 상태 확인 | 별도 테스트 아이디 없이 진행 | 체크박스 선택/해제 기능이 정상적으로 작동되어야함 |",
        "| 18 | TS-31-018 | 18 | 등록하기 버튼 - 비활성화 상태 | 페이지 | - 상담유형/문의제목/문의내용 중 하나라도 공백이나 선택값 없는 경우<br>- [등록하기] 버튼이 비활성화 상태로 표시되는지 확인 | 필수 항목 미입력 상태 | [등록하기] 버튼이 비활성화 상태로 표시되어야함 |",
        "| 19 | TS-31-019 | 19 | 등록하기 버튼 - 활성화 상태 | 페이지 | - 상담유형, 문의제목, 문의내용 모두 입력 및 선택된 경우<br>- [등록하기] 버튼이 활성화 상태로 표시되는지 확인 | 모든 필수 항목 입력 완료 | [등록하기] 버튼이 활성화 상태로 표시되어야함 |",
        "| 20 | TS-31-020 | 20 | 등록하기 - 필수 항목 미입력 | 페이지 | - 필수 항목을 입력하지 않은 상태에서 [등록하기] 버튼 클릭<br>- 각 필수 항목별 오류 메시지가 표시되는지 확인<br>- 이메일 미입력: '이메일을 입력해주세요.'<br>- 문의유형 미선택: '문의유형을 선택해주세요.'<br>- 제목 미입력: '제목을 입력해주세요.'<br>- 내용 미입력: '문의내용을 입력해주세요.'<br>- 동의 미체크: '개인정보 수집 및 이용에 동의해주세요.' | 필수 항목 미입력 상태 | 각 필수 항목별 오류 메시지가 표시되어야함 |",
        "| 21 | TS-31-021 | 21 | 등록하기 - 등록 성공 | 페이지 | - 모든 필수 항목 입력 후 [등록하기] 버튼 클릭<br>- 등록완료 안내 팝업이 노출되는지 확인<br>- '문의가 등록되었습니다. 빠른 시일 내 답변드리겠습니다.' 메시지가 표시되는지 확인<br>- 문의글 접수 완료 시 알림톡 전송되는지 확인<br>- 문의글 등록 후, 마이페이지 > 1:1문의내역에 등록한 문의글 노출되는지 확인 | 모든 필수 항목 입력 완료 | 등록완료 안내 팝업이 노출되고, 알림톡이 전송되며, 문의내역에 등록한 문의글이 노출되어야함 |",
        "| 22 | TS-31-022 | 22 | 다시쓰기 버튼 | 페이지 | - [다시쓰기] 버튼 클릭<br>- 모든 입력 내용이 초기화되는지 확인<br>- 기본값으로 복원되는지 확인 | 별도 테스트 아이디 없이 진행 | 모든 입력 내용이 초기화되고 기본값으로 복원되어야함 |",
        "| 23 | TS-31-023 | 23 | 문의내역 - 테이블 구조 | 페이지 | - 문의내역 탭에서 테이블 확인<br>- 번호, 문의유형, 제목, 답변여부, 등록일 열이 표시되는지 확인 | 로그인 상태 | 번호, 문의유형, 제목, 답변여부, 등록일 열이 표시되어야함 |",
        "| 24 | TS-31-024 | 24 | 문의내역 - 빈 상태 | 페이지 | - 문의 내역이 없는 경우<br>- 빈 상태 안내 메시지가 표시되는지 확인 | 문의 내역이 없는 계정 | 빈 상태 안내 메시지가 표시되어야함 |",
        "| 25 | TS-31-025 | 25 | 문의내역 - 행 클릭 | 페이지 | - 문의 내역 테이블의 행 클릭<br>- 문의 상세 내용이 표시되는지 확인 | 문의 내역이 있는 계정 | 문의 상세 내용이 표시되어야함 |"
    ]
    
    new_section = '\n'.join(new_section_lines) + '\n'
    content = content.replace(section, new_section)
    
    return content

def consolidate_email_input_cases(content, section_num):
    """이메일 입력 관련 세분화된 케이스 통합"""
    section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 이메일 입력 관련 연속 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', line):
            email_cases = [line]
            j = i + 1
            
            # 연속된 이메일 입력 케이스 수집
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', lines[j]):
                email_cases.append(lines[j])
                j += 1
            
            # 3개 이상이면 통합
            if len(email_cases) >= 3:
                # 첫 번째 케이스를 기준으로 통합
                base_parts = email_cases[0].split('|')
                if len(base_parts) >= 6:
                    all_steps = []
                    for case in email_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            if step and step not in all_steps:
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        # 테스트케이스명도 통합
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 이메일 입력 (아이디, 도메인 선택/직접입력) '
                        new_lines.append('|'.join(base_parts))
                        i = j
                        continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def consolidate_inquiry_type_cases(content):
    """문의유형 선택 관련 세분화된 케이스 통합"""
    section_pattern = r'(^## 31\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^---|$)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not section_match:
        return content
    
    section = section_match.group(1)
    lines = section.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 문의유형 선택 관련 연속 케이스 찾기
        if re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', line):
            type_cases = [line]
            j = i + 1
            
            while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', lines[j]):
                type_cases.append(lines[j])
                j += 1
            
            # 3개 이상이면 통합
            if len(type_cases) >= 3:
                base_parts = type_cases[0].split('|')
                if len(base_parts) >= 6:
                    all_steps = []
                    for case in type_cases:
                        case_parts = case.split('|')
                        if len(case_parts) >= 6:
                            step = case_parts[5].strip()
                            if step and step not in all_steps:
                                all_steps.append(step)
                    
                    if all_steps:
                        base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                        if len(base_parts) >= 4:
                            base_parts[3] = ' 문의유형 선택 (가격문의/서비스문의/기술문의/기타) '
                        new_lines.append('|'.join(base_parts))
                        i = j
                        continue
        
        new_lines.append(line)
        i += 1
    
    new_section = '\n'.join(new_lines)
    content = content.replace(section, new_section)
    
    return content

def add_missing_features_from_reference(content):
    """참고 문서에서 누락된 기능 설명 추가"""
    
    # 섹션 2 (회원가입) - 이메일 자동완성 상세 설명
    sections_to_fix = {
        2: {  # 회원가입
            'email': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출, 지원도메인 선택 시 얼럿멘트 노출되지 않도록 처리",
            'password': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내), 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 얼럿 메시지 노출, 20자 이상 입력불가"
        },
        3: {  # 로그인
            'email': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출",
            'password': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
        }
    }
    
    for section_num, features in sections_to_fix.items():
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        
        for line in lines:
            # 이메일 입력 - 정상 입력 케이스
            if 'email' in features and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*아이디 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if features['email'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {features['email']}"
                        else:
                            step_content = f"- {features['email']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            # 비밀번호 입력 - 정상 입력 케이스
            if 'password' in features and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력.*정상 입력', line):
                parts = line.split('|')
                if len(parts) >= 6:
                    step_content = parts[5].strip()
                    if features['password'] not in step_content:
                        if step_content:
                            if not step_content.startswith('-'):
                                step_content = f"- {step_content}"
                            step_content = f"{step_content}<br>- {features['password']}"
                        else:
                            step_content = f"- {features['password']}"
                        parts[5] = f' {step_content} '
                        line = '|'.join(parts)
            
            new_lines.append(line)
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup4'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 최종 보완 작업")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 섹션 31 상세 내용 보완
    print("\n[1] 섹션 31 (1:1 문의) 상세 내용 보완 중...")
    content = enhance_section31(content)
    
    # 2. 참고 문서 기반 누락 기능 설명 추가
    print("[2] 참고 문서 기반 누락 기능 설명 추가 중...")
    content = add_missing_features_from_reference(content)
    
    # 3. 이메일 입력 케이스 통합
    print("[3] 이메일 입력 케이스 통합 중...")
    for section_num in [2, 3, 20, 31]:
        content = consolidate_email_input_cases(content, section_num)
    
    # 4. 문의유형 선택 케이스 통합
    print("[4] 문의유형 선택 케이스 통합 중...")
    content = consolidate_inquiry_type_cases(content)
    
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
