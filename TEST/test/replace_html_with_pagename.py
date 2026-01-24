#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 주소를 페이지명으로 변경
템플릿 개수 예시 제거
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

# HTML 파일명 → 페이지명 매핑
HTML_TO_PAGENAME = {
    'template-alimtalk.html': '알림톡 템플릿',
    'template-brandtalk.html': '브랜드 메시지 템플릿',
    'kakao-profile-manage.html': '카카오톡 발신 프로필 관리',
    'template-alimtalk-register.html': '알림톡 템플릿 등록',
    'template-brandtalk-register.html': '브랜드 메시지 템플릿 등록',
    'template-brandtalk-edit.html': '브랜드 메시지 템플릿 수정',
    'kakao-send-brandtalk.html': '브랜드 메시지 발송',
    'payment-charge.html': '충전',
    'payment-history.html': '결제 내역',
    'mypage-profile.html': '내 정보 수정',
    'support-notice-detail.html': '공지사항 상세',
    'support-event-detail.html': '이벤트 상세',
    'index.html': '메인',
    'main.html': '대시보드',
    'login.html': '로그인',
    'signup.html': '회원가입',
    'message-send-general.html': '일반문자 발송',
    'message-send-ad.html': '광고문자 발송',
    'send-result.html': '발송결과',
    'send-reservation.html': '예약내역',
    'mypage-password.html': '비밀번호 변경',
    'mypage-caller-number.html': '발신번호 관리',
    'payment-refund.html': '환불',
    'payment-tax.html': '세금계산서 발행',
    'kakao-send-alimtalk.html': '알림톡 발송',
}

def replace_html_with_pagename(content):
    """HTML 주소를 페이지명으로 변경"""
    
    # HTML 파일명 패턴 찾기 및 교체 (순서 중요: 구체적인 패턴부터)
    for html_file, page_name in HTML_TO_PAGENAME.items():
        # 다양한 패턴 처리 (구체적인 패턴부터 처리)
        patterns = [
            # "template-alimtalk.html?id=xxx 접속"
            (rf'{re.escape(html_file)}\?[^\s<>]*\s*접속', f'{page_name} 페이지 접속'),
            # "template-alimtalk.html?edit=템플릿ID 페이지로 이동"
            (rf'{re.escape(html_file)}\?[^\s<>]*\s*페이지로\s*이동', f'{page_name} 페이지로 이동'),
            # "template-alimtalk.html 페이지로 이동"
            (rf'{re.escape(html_file)}\s*페이지로\s*이동', f'{page_name} 페이지로 이동'),
            # "template-alimtalk.html로 이동"
            (rf'{re.escape(html_file)}\s*로\s*이동', f'{page_name} 페이지로 이동'),
            # "template-alimtalk.html 접속"
            (rf'{re.escape(html_file)}\s*접속', f'{page_name} 페이지 접속'),
            # "template-alimtalk.html 페이지"
            (rf'{re.escape(html_file)}\s*페이지', f'{page_name} 페이지'),
            # "template-alimtalk.html" (단독, 단어 경계 사용)
            (rf'\b{re.escape(html_file)}\b', page_name),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def remove_template_count_examples(content):
    """템플릿 개수 예시 제거 (예: "24개")"""
    
    # 패턴: (예: "24개") 또는 (예: "12개") 등
    patterns = [
        r'\(예\s*:\s*"[0-9]+개"\)',
        r'\(예\s*:\s*[0-9]+개\)',
        r'예\s*:\s*"[0-9]+개"',
        r'예\s*:\s*[0-9]+개',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 빈 괄호 제거
    content = re.sub(r'\(\s*\)', '', content)
    
    # 연속된 공백 정리 (줄바꿈은 유지)
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # 각 줄 내에서만 연속된 공백 정리
        cleaned_line = re.sub(r'[ \t]+', ' ', line)
        cleaned_lines.append(cleaned_line)
    content = '\n'.join(cleaned_lines)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_html_replace'
    
    print("=" * 80)
    print("HTML 주소를 페이지명으로 변경")
    print("템플릿 개수 예시 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # HTML 주소를 페이지명으로 변경
    print("\n[1] HTML 주소를 페이지명으로 변경 중...")
    content = replace_html_with_pagename(content)
    
    # 템플릿 개수 예시 제거
    print("\n[2] 템플릿 개수 예시 제거 중...")
    content = remove_template_count_examples(content)
    
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
