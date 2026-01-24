#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시나리오 상세화 및 수정
- 메시지 내용 입력 등 구체적인 시나리오 추가
- 한글 바이트 2바이트 기준으로 수정
- 중복 표현 제거
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

def enhance_message_content_scenarios(content):
    """메시지 내용 입력 시나리오 구체화"""
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 메시지 내용 관련 시나리오 찾기
        if '메시지 내용' in line and 'TS-04-020' in line:
            # 다음 몇 줄 읽기
            work_content_start = i
            while i < len(lines) and '|' in lines[i]:
                current_line = lines[i]
                
                # 단계별 작업 수행내용이 간단한 경우 구체화
                if '메시지 내용 확인' in current_line and '<br>' in current_line:
                    # 기존 내용을 구체적인 내용으로 교체
                    parts = current_line.split('|')
                    if len(parts) >= 6:
                        # 단계별 작업 수행내용 부분 (인덱스 5)
                        new_work = (
                            "- 메시지 내용 입력 확인<br>"
                            "  - 메시지 내용 입력 시 바이트 수 실시간 표시 확인<br>"
                            "  - SMS 선택 시: 최대 90바이트 (한글 약 45자, 영문 90자) 제한 확인<br>"
                            "  - LMS 선택 시: 최대 2,000바이트 (한글 약 1,000자, 영문 2,000자) 제한 확인<br>"
                            "  - 정상 케이스: 한글 40자 입력 시 '80 / 90 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                            "  - 정상 케이스: 영문 80자 입력 시 '80 / 90 바이트' 표시 확인<br>"
                            "  - 비정상 케이스: SMS 선택 시 90바이트 초과 입력 시 LMS로 자동 전환 확인<br>"
                            "  - 필수 입력 항목<br>"
                            "  - 미입력 시 '메시지 내용을 입력해주세요' 알림 메시지 노출 확인"
                        )
                        parts[5] = new_work
                        current_line = '|'.join(parts)
                
                new_lines.append(current_line)
                i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def fix_hangul_byte_references(content):
    """한글 바이트 2바이트 기준으로 수정"""
    
    # 한글 바이트 계산 관련 수정
    replacements = [
        (r'한글\s*약\s*30자', '한글 약 45자'),  # 90바이트 / 2 = 45자
        (r'한글\s*약\s*666자', '한글 약 1,000자'),  # 2000바이트 / 2 = 1000자
        (r'한글\s*약\s*33자', '한글 약 50자'),  # 100바이트 / 2 = 50자
        (r'한글\s*3바이트', '한글 2바이트'),
        (r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트'),
        (r'\(한글\s*1자\s*=\s*3바이트\)', '(한글 1자 = 2바이트)'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def remove_duplicate_expressions(content):
    """중복 표현 제거"""
    
    # "입력 입력 확인" -> "입력 확인"
    content = re.sub(r'입력\s*입력\s*확인', '입력 확인', content)
    content = re.sub(r'선택\s*선택\s*확인', '선택 확인', content)
    
    return content

def enhance_work_content(content):
    """단계별 작업 수행내용 구체화"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # 메시지 내용 입력 시나리오 구체화
        if '메시지 내용 확인' in line and 'TS-04-020' in line:
            # 기존 라인을 찾아서 교체
            parts = line.split('|')
            if len(parts) >= 6:
                # 단계별 작업 수행내용이 간단한 경우 구체화
                if '• 필수 입력 항목' in parts[5] or len(parts[5].strip()) < 50:
                    parts[5] = (
                        "- 메시지 내용 입력 확인<br>"
                        "  - 메시지 내용 입력 시 바이트 수 실시간 표시 확인<br>"
                        "  - SMS 선택 시: 최대 90바이트 (한글 약 45자, 영문 90자) 제한 확인<br>"
                        "  - LMS 선택 시: 최대 2,000바이트 (한글 약 1,000자, 영문 2,000자) 제한 확인<br>"
                        "  - 정상 케이스: 한글 40자 입력 시 '80 / 90 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                        "  - 정상 케이스: 영문 80자 입력 시 '80 / 90 바이트' 표시 확인<br>"
                        "  - 비정상 케이스: SMS 선택 시 90바이트 초과 입력 시 LMS로 자동 전환 확인<br>"
                        "  - 필수 입력 항목<br>"
                        "  - 미입력 시 '메시지 내용을 입력해주세요' 알림 메시지 노출 확인"
                    )
                    line = '|'.join(parts)
        
        # 제목 입력 시나리오 구체화
        elif '제목' in line and '입력' in line and 'TS-04' in line:
            parts = line.split('|')
            if len(parts) >= 6 and ('• 최대' in parts[5] or len(parts[5].strip()) < 50):
                parts[5] = (
                    "- 메시지 제목 입력 확인<br>"
                    "  - 제목 입력 시 바이트 수 실시간 표시 확인<br>"
                    "  - 최대 40바이트 (한글 20자, 영문 40자) 제한 확인<br>"
                    "  - 정상 케이스: 한글 15자 입력 시 '30 / 40 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                    "  - 정상 케이스: 영문 30자 입력 시 '30 / 40 바이트' 표시 확인<br>"
                    "  - 비정상 케이스: 40바이트 초과 입력 시 '제목은 40바이트(한글 20자)를 초과할 수 없습니다' 알림 메시지 노출 확인<br>"
                    "  - 선택 입력 항목"
                )
                line = '|'.join(parts)
        
        # 이름 입력 시나리오 구체화
        elif '이름' in line and '입력' in line and ('TS-04' in line or 'TS-05' in line or 'TS-08' in line):
            parts = line.split('|')
            if len(parts) >= 6 and ('100바이트' in parts[5] or len(parts[5].strip()) < 50):
                parts[5] = (
                    "- 이름 입력 확인<br>"
                    "  - 이름 입력 시 바이트 수 확인<br>"
                    "  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인<br>"
                    "  - 정상 케이스: '홍길동' 입력 시 '6 / 100 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                    "  - 정상 케이스: 영문 50자 입력 시 '50 / 100 바이트' 표시 확인<br>"
                    "  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(100바이트)를 초과했습니다' 알림 메시지 노출 확인<br>"
                    "  - 선택 입력 항목"
                )
                line = '|'.join(parts)
        
        # 변수 입력 시나리오 구체화
        elif '변수' in line and '입력' in line and ('TS-04' in line or 'TS-05' in line or 'TS-08' in line):
            parts = line.split('|')
            if len(parts) >= 6 and ('100바이트' in parts[5] or len(parts[5].strip()) < 50):
                parts[5] = (
                    "- 변수 입력 확인<br>"
                    "  - 변수 입력 시 바이트 수 확인<br>"
                    "  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인<br>"
                    "  - 정상 케이스: 한글 30자 입력 시 '60 / 100 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                    "  - 정상 케이스: 영문 60자 입력 시 '60 / 100 바이트' 표시 확인<br>"
                    "  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(100바이트)를 초과했습니다' 알림 메시지 노출 확인<br>"
                    "  - 선택 입력 항목"
                )
                line = '|'.join(parts)
        
        # 그룹명 입력 시나리오 구체화
        elif '그룹' in line and ('명' in line or '이름' in line) and '입력' in line:
            parts = line.split('|')
            if len(parts) >= 6 and ('50바이트' in parts[5] or len(parts[5].strip()) < 50):
                parts[5] = (
                    "- 그룹명 입력 확인<br>"
                    "  - 그룹명 입력 시 바이트 수 확인<br>"
                    "  - 최대 50바이트 (한글 약 25자, 영문 50자) 제한 확인<br>"
                    "  - 정상 케이스: '고객그룹' 입력 시 '8 / 50 바이트' 표시 확인 (한글 1자 = 2바이트)<br>"
                    "  - 정상 케이스: 영문 20자 입력 시 '20 / 50 바이트' 표시 확인<br>"
                    "  - 비정상 케이스: 50바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(50바이트)를 초과했습니다' 알림 메시지 노출 확인<br>"
                    "  - 필수 입력 항목 (새 그룹 생성 시)"
                )
                line = '|'.join(parts)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_fix_detailed'
    
    print("=" * 80)
    print("시나리오 상세화 및 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 중복 표현 제거
    print("\n[1] 중복 표현 제거 중...")
    content = remove_duplicate_expressions(content)
    
    # 2. 한글 바이트 2바이트 기준으로 수정
    print("\n[2] 한글 바이트 2바이트 기준으로 수정 중...")
    content = fix_hangul_byte_references(content)
    
    # 3. 시나리오 구체화
    print("\n[3] 시나리오 구체화 중...")
    content = enhance_work_content(content)
    
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
