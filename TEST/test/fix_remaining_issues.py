#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
남은 문제 수정:
1. 한글 바이트 3바이트 → 2바이트로 수정
2. HTML 파일명을 페이지명으로 변경 (index → 메인, login → 로그인 등)
3. 바이트 초과 경고 관련 내용 제거
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

def fix_hangul_byte_final(content):
    """한글 바이트 3바이트 → 2바이트로 최종 수정"""
    
    replacements = [
        (r'한글:\s*3바이트', '한글: 2바이트'),
        (r'한글\s*3바이트', '한글 2바이트'),
        (r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트'),
        (r'\(한글:\s*3바이트\)', '(한글: 2바이트)'),
        (r'•\s*한글:\s*3바이트', '• 한글: 2바이트'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def fix_html_filenames_to_pagenames(content):
    """HTML 파일명을 페이지명으로 변경"""
    
    replacements = [
        (r'\bindex\b', '메인'),
        (r'\blogin\b', '로그인'),
        (r'\bsignup\b', '회원가입'),
        (r'\bquote-inquiry\b', '견적문의'),
        (r'\bfind-id\b', '아이디찾기'),
        (r'\bfind-password\b', '비밀번호찾기'),
        (r'\bmain\b', '대시보드'),
        (r'\bmessage-send-general\b', '일반문자 발송'),
        (r'\bmessage-send-ad\b', '광고문자 발송'),
        (r'\btemplate-message\b', '일반문자 템플릿'),
        (r'\btemplate-message-ad\b', '광고문자 템플릿'),
        (r'\bmessage-send-election\b', '선거문자 발송'),
        (r'\btemplate-message-election\b', '선거문자 템플릿'),
        (r'\bkakao-send-alimtalk\b', '알림톡 발송'),
        (r'\bkakao-send-brandtalk\b', '브랜드 메시지 발송'),
        (r'\bkakao-profile-manage\b', '카카오톡 발신 프로필 관리'),
        (r'\btemplate-alimtalk\b', '알림톡 템플릿'),
        (r'\btemplate-brandtalk\b', '브랜드 메시지 템플릿'),
        (r'\baddressbook\b', '주소록 관리'),
        (r'\baddressbook-reject\b', '수신거부관리'),
        (r'\bsend-result\b', '발송결과'),
        (r'\bsend-reservation\b', '예약내역'),
        (r'\bpayment-charge\b', '충전'),
        (r'\bpayment-history\b', '결제 내역'),
        (r'\bpayment-refund\b', '환불'),
        (r'\bpayment-tax\b', '세금계산서 발행'),
        (r'\bmypage-profile\b', '내 정보 수정'),
        (r'\bmypage-password\b', '비밀번호 변경'),
        (r'\bmypage-caller-number\b', '발신번호 관리'),
        (r'\bsupport-notice\b', '공지사항'),
        (r'\bsupport-event\b', '이벤트'),
        (r'\bsupport-faq\b', 'FAQ'),
        (r'\bsupport-inquiry\b', '1:1문의'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def remove_byte_warning_final(content):
    """바이트 초과 경고 관련 내용 최종 제거"""
    
    # 경고 관련 패턴 제거
    patterns = [
        r'90%\s*초과\s*시\s*경고',
        r'100%\s*초과\s*시',
        r'초과\s*시\s*색상\s*변경\s*경고',
        r'초과\s*시\s*경고',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 빈 <br> 태그 정리
    content = re.sub(r'<br>\s*<br>', '<br>', content)
    content = re.sub(r'<br>\s*$', '', content, flags=re.MULTILINE)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_fix_remaining'
    
    print("=" * 80)
    print("남은 문제 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 한글 바이트 수정
    print("\n[1] 한글 바이트 3바이트 → 2바이트로 수정 중...")
    content = fix_hangul_byte_final(content)
    
    # 2. HTML 파일명을 페이지명으로 변경
    print("\n[2] HTML 파일명을 페이지명으로 변경 중...")
    content = fix_html_filenames_to_pagenames(content)
    
    # 3. 바이트 초과 경고 제거
    print("\n[3] 바이트 초과 경고 관련 내용 제거 중...")
    content = remove_byte_warning_final(content)
    
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
