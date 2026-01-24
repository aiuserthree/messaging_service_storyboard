#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 수정: 중복 제거, 바이트 계산 오류 수정, 누락 기능 설명 추가
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

def remove_duplicate_section31(content):
    """섹션 31의 중복된 기존 내용 제거"""
    # 섹션 31의 두 번째 테이블 헤더부터 끝까지 제거
    pattern = r'(^## 31\.\s+고객센터 > 1:1 문의.*?\n\| 25 \| TS-31-025.*?\n)(\n\|\s*순번.*?)(?=^---|$)'
    
    def replace_func(match):
        # 첫 번째 부분(새로운 상세 내용)만 유지
        return match.group(1) + '\n'
    
    content = re.sub(pattern, replace_func, content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def fix_byte_calculation_errors(content):
    """바이트 계산 오류 및 예상 결과 수정"""
    
    # 라인 230: "11 / 90 바이트9 / 90 바이트" -> "11 / 90 바이트"
    content = re.sub(
        r'("11 / 90 바이트"9 / 90 바이트)',
        '"11 / 90 바이트"',
        content
    )
    content = re.sub(
        r'바이트 수 표시 영역에 "11 / 90 바이트9 / 90 바이트',
        '바이트 수 표시 영역에 "11 / 90 바이트',
        content
    )
    
    # "가나다" (3자) = 9바이트로 수정 (예상 결과도)
    content = re.sub(
        r'바이트 수가 (6바이트)로 계산되어 표시되어야함.*?한글 1자 = 3바이트',
        r'바이트 수가 9바이트로 계산되어 표시되어야함 (한글 1자 = 3바이트)',
        content
    )
    content = re.sub(
        r'바이트 카운터에 "(6 / \d+ 바이트)"가 표시되어야함.*?한글 1자 = 3바이트',
        r'바이트 카운터에 "9 / \1"가 표시되어야함 (한글 1자 = 3바이트)',
        content
    )
    
    # "홍길동" (3자) = 9바이트로 수정
    content = re.sub(
        r'바이트 카운터에 "(6 / 40 바이트)"가 표시되어야함.*?한글 1자 = 3바이트',
        r'바이트 카운터에 "9 / 40 바이트"가 표시되어야함 (한글 1자 = 3바이트)',
        content
    )
    
    # 혼합 계산 수정: "홍길동ABC" = 한글 3자(9바이트) + 영문 3자(3바이트) = 12바이트
    content = re.sub(
        r'바이트 카운터에 "(9 / 40 바이트)"가 표시되어야함.*?한글 3자\(6바이트\) \+ 영문 3자\(3바이트\)',
        r'바이트 카운터에 "12 / 40 바이트"가 표시되어야함 (한글 3자(9바이트) + 영문 3자(3바이트))',
        content
    )
    
    # 중복된 바이트 표시 제거
    content = re.sub(
        r'(\d+ / \d+ 바이트)\1',
        r'\1',
        content
    )
    content = re.sub(
        r'바이트 바이트',
        '바이트',
        content
    )
    
    return content

def add_missing_features_comprehensive(content):
    """참고 문서 기반 누락된 기능 설명 종합 추가"""
    
    # 섹션별로 처리
    fixes = {
        2: {  # 회원가입
            'email_line': r'(\|\s*\d+\s*\|\s*TS-02-\d+\s*\|\s*\d+\s*\|\s*이메일 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'email_add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출, 지원도메인 선택 시 얼럿멘트 노출되지 않도록 처리",
            'password_line': r'(\|\s*\d+\s*\|\s*TS-02-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'password_add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내), 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 얼럿 메시지 노출, 20자 이상 입력불가"
        },
        3: {  # 로그인
            'email_line': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*아이디 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'email_add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출",
            'password_line': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'password_add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
        },
        5: {  # 일반문자 발송
            'sms_line': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'sms_add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_line': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'lms_add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_line': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'title_add': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_line': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'name_add': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시"
        },
        6: {  # 광고문자 발송
            'sms_line': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'sms_add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_line': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'lms_add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_line': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'title_add': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_line': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'name_add': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시",
            'ad_prefix_line': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*\(광고\).*옆.*문구[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'ad_prefix_add': "(광고) 옆 문구: 최대 20자까지 입력 가능"
        },
        7: {  # 일반문자 템플릿
            'template_line': r'(\|\s*\d+\s*\|\s*TS-07-\d+\s*\|\s*\d+\s*\|\s*템플릿명[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'template_add': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
        },
        8: {  # 광고문자 템플릿
            'template_line': r'(\|\s*\d+\s*\|\s*TS-08-\d+\s*\|\s*\d+\s*\|\s*템플릿명[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'template_add': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시"
        },
        20: {  # PC 로그인
            'email_line': r'(\|\s*\d+\s*\|\s*TS-20-\d+\s*\|\s*\d+\s*\|\s*아이디 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'email_add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출"
        }
    }
    
    for section_num, fix_info in fixes.items():
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        new_section = section
        
        for key, pattern in fix_info.items():
            if key.endswith('_line'):
                feature_name = key.replace('_line', '')
                add_key = feature_name + '_add'
                
                if add_key in fix_info:
                    pattern_str = pattern
                    add_text = fix_info[add_key]
                    
                    def add_feature(match):
                        step_col = match.group(2).strip()
                        if add_text not in step_col:
                            if step_col:
                                if not step_col.startswith('-'):
                                    step_col = f"- {step_col}"
                                step_col = f"{step_col}<br>- {add_text}"
                            else:
                                step_col = f"- {add_text}"
                        return match.group(1) + step_col + match.group(3)
                    
                    new_section = re.sub(pattern_str, add_feature, new_section)
        
        content = content.replace(section, new_section)
    
    return content

def consolidate_similar_cases_final(content):
    """같은 영역의 세분화된 항목 통합"""
    
    # 이메일 입력 관련 통합 (섹션 2, 3, 20, 31)
    for section_num in [2, 3, 20, 31]:
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 이메일 입력 관련 연속 케이스 (3개 이상)
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', line):
                email_cases = [line]
                j = i + 1
                
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', lines[j]):
                    email_cases.append(lines[j])
                    j += 1
                
                if len(email_cases) >= 3:
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
                            if len(base_parts) >= 4:
                                base_parts[3] = ' 이메일 입력 (아이디, 도메인 선택/직접입력) '
                            new_lines.append('|'.join(base_parts))
                            i = j
                            continue
            
            # 문의유형 선택 관련 통합 (섹션 31)
            if section_num == 31 and re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', line):
                type_cases = [line]
                j = i + 1
                
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-31-\d+\s*\|\s*\d+\s*\|\s*문의유형', lines[j]):
                    type_cases.append(lines[j])
                    j += 1
                
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

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup5'
    
    print("=" * 80)
    print("FO_테스트시나리오_상세.md 최종 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 섹션 31 중복 제거
    print("\n[1] 섹션 31 중복 제거 중...")
    content = remove_duplicate_section31(content)
    
    # 2. 바이트 계산 오류 수정
    print("[2] 바이트 계산 오류 수정 중...")
    content = fix_byte_calculation_errors(content)
    
    # 3. 누락된 기능 설명 종합 추가
    print("[3] 누락된 기능 설명 종합 추가 중...")
    content = add_missing_features_comprehensive(content)
    
    # 4. 같은 영역의 세분화된 항목 통합
    print("[4] 같은 영역의 세분화된 항목 통합 중...")
    content = consolidate_similar_cases_final(content)
    
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
