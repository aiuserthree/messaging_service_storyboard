#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
바이트 계산 오류 및 예상 결과 수정
참고 문서 기반 상세 기능 설명 추가
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

def fix_byte_calculations(content):
    """바이트 계산 및 예상 결과 수정"""
    
    # "안녕하세요" (5자) = 10바이트 -> 15바이트 (5자 * 3바이트)
    content = re.sub(
        r'("안녕하세요" 입력.*?)(10 / 90 바이트)(.*?한글 1자 = 3바이트)',
        r'\g<1>15 / 90 바이트\g<3>',
        content
    )
    content = re.sub(
        r'(바이트 수 표시 영역에 ")(10 / 90 바이트)("가 표시되어야함.*?한글 1자 = 3바이트)',
        r'\g<1>15 / 90 바이트\g<3>',
        content
    )
    
    # "Hello 안녕" = 영문 5바이트 + 한글 2자(6바이트) = 11바이트
    # 예상 결과도 수정
    content = re.sub(
        r'("Hello 안녕" 입력.*?11 / 90 바이트.*?영문 5바이트 \+ 한글 2자\(6바이트\).*?바이트 수 표시 영역에 ")(9 / 90 바이트)("가 표시되어야함.*?영문 5바이트 \+ 한글 4바이트)',
        r'\g<1>11 / 90 바이트\g<2> (영문 5바이트 + 한글 2자(6바이트))',
        content
    )
    
    # "가나다" (3자) = 6바이트 -> 9바이트 (3자 * 3바이트)
    content = re.sub(
        r'("가나다" 입력.*?)(6바이트)(.*?한글 1자 = 3바이트)',
        r'\g<1>9바이트\g<3>',
        content
    )
    content = re.sub(
        r'("가나다" 입력.*?)(6 / (\d+) 바이트)(.*?한글 1자 = 3바이트)',
        r'\g<1>9 / \g<2> 바이트\g<4>',
        content
    )
    
    # "홍길동" (3자) = 6바이트 -> 9바이트
    content = re.sub(
        r'("홍길동" 입력.*?)(6 / 40 바이트)(.*?한글 1자 = 3바이트)',
        r'\g<1>9 / 40 바이트\g<3>',
        content
    )
    
    return content

def add_detailed_features_from_reference(content):
    """참고 문서에서 추출한 상세 기능 설명 추가"""
    
    # 섹션별로 처리
    sections = {
        2: {  # 회원가입
            'email': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-02-\d+\s*\|\s*\d+\s*\|\s*이메일 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출"
            },
            'password': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-02-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내), 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 얼럿 메시지 노출, 20자 이상 입력불가"
            }
        },
        3: {  # 로그인
            'email': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*아이디 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출"
            },
            'password': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)"
            }
        },
        5: {  # 일반문자 발송
            'sms': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환"
            },
            'lms': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
            },
            'title': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'"
            }
        },
        6: {  # 광고문자 발송
            'sms': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환"
            },
            'lms': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트"
            },
            'ad_prefix': {
                'pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*\(광고\).*옆.*문구[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
                'add': "(광고) 옆 문구: 최대 20자까지 입력 가능"
            }
        }
    }
    
    for section_num, features in sections.items():
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        new_section = section
        
        for feature_name, feature_info in features.items():
            pattern = feature_info['pattern']
            add_text = feature_info['add']
            
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
            
            new_section = re.sub(pattern, add_feature, new_section)
        
        content = content.replace(section, new_section)
    
    return content

def consolidate_validation_cases(content):
    """유효성 검사 케이스 통합"""
    # 같은 필드의 여러 유효성 검사 케이스를 하나로 통합
    sections_to_fix = [2, 3, 5, 6]
    
    for section_num in sections_to_fix:
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 유효성 검사 관련 연속 케이스 찾기
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*유효성.*체크', line):
                validation_cases = [line]
                j = i + 1
                
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*.*유효성.*체크', lines[j]):
                    validation_cases.append(lines[j])
                    j += 1
                
                # 3개 이상이면 통합 고려
                if len(validation_cases) >= 3:
                    # 같은 필드의 유효성 검사인지 확인
                    field_names = []
                    for case in validation_cases:
                        case_match = re.search(r'\|\s*([^|]+)\s*\|', case)
                        if case_match:
                            field_names.append(case_match.group(1).strip())
                    
                    # 같은 필드면 통합
                    if len(set(field_names)) == 1:
                        base_parts = validation_cases[0].split('|')
                        if len(base_parts) >= 6:
                            all_steps = []
                            for case in validation_cases:
                                case_parts = case.split('|')
                                if len(case_parts) >= 6:
                                    step = case_parts[5].strip()
                                    if step and step not in all_steps:
                                        all_steps.append(step)
                            
                            if all_steps:
                                base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
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
    backup_path = file_path + '.backup3'
    
    print("=" * 80)
    print("바이트 계산 및 상세 기능 설명 추가")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 바이트 계산 수정
    print("\n[1] 바이트 계산 및 예상 결과 수정 중...")
    content = fix_byte_calculations(content)
    
    # 2. 참고 문서 기반 상세 기능 설명 추가
    print("[2] 참고 문서 기반 상세 기능 설명 추가 중...")
    content = add_detailed_features_from_reference(content)
    
    # 3. 유효성 검사 케이스 통합
    print("[3] 유효성 검사 케이스 통합 중...")
    content = consolidate_validation_cases(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
