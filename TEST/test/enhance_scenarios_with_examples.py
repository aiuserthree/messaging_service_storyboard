#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시나리오를 참고 문서 형식에 맞춰 더 구체적으로 작성
- 입력 데이터 구체적인 예시 추가
- 경우의 수 따져서 정확한 예시로 작성
- 제한사항 명확히 포함
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

def enhance_work_content(work_content, spec_item):
    """단계별 작업 수행내용을 더 구체적으로 작성"""
    
    title = spec_item['title']
    behaviors = spec_item['behaviors']
    
    # 기본 확인 항목
    enhanced_items = [f"- {title} 확인"]
    
    # 입력 필드인 경우 구체적인 예시 추가
    if '입력' in title or '입력' in spec_item['function']:
        if '이메일' in title or '이메일' in spec_item['function']:
            enhanced_items.append("  - 이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개)")
            enhanced_items.append("    (naver.com/gmail.com/icloud.com/kakao.com/daum.net/nate.com/hanmail.net)")
            enhanced_items.append("  - 정상 케이스: test@naver.com 입력 시 자동완성 목록 표시 확인")
            enhanced_items.append("  - 비정상 케이스: '@'와 '.'이 없는 경우 '올바른 이메일 주소를 입력해 주세요' 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: @앞에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: .앞과 뒤에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: 한글 텍스트가 입력된 경우 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: 입력값이 100자 이상인 경우 알림 메시지 노출 확인")
        elif '비밀번호' in title or '비밀번호' in spec_item['function']:
            enhanced_items.append("  - 비밀번호 입력(영문,숫자,특수문자 포함 8~20자 이내) 조건에 따른 알림 메시지 노출/숨김 확인")
            enhanced_items.append("  - 정상 케이스: 'Test1234!' 입력 시 조건 충족 확인")
            enhanced_items.append("  - 비정상 케이스: 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 알림 메시지 노출, 20자 이상 입력불가 확인")
        elif '전화번호' in title or '연락처' in title or '휴대폰' in title:
            enhanced_items.append("  - 전화번호 최소 9자리 이상 입력 확인")
            enhanced_items.append("  - 정상 케이스: '010-1234-5678' 입력 시 정상 처리 확인")
            enhanced_items.append("  - 정상 케이스: '01012345678' 입력 시 자동 하이픈 포맷팅 확인")
            enhanced_items.append("  - 비정상 케이스: 9자리 미만 입력 시 '전화번호는 최소 9자리 이상 입력해주세요' 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: 숫자가 아닌 문자 입력 시 자동 제거 또는 알림 메시지 노출 확인")
        elif '이름' in title and '변수' not in title:
            enhanced_items.append("  - 이름 입력 시 100바이트 제한 확인 (한글 약 50자, 영문 100자)")
            enhanced_items.append("  - 정상 케이스: '홍길동' 입력 시 정상 처리 확인")
            enhanced_items.append("  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(100바이트)를 초과했습니다' 알림 메시지 표시 확인")
        elif '변수' in title:
            enhanced_items.append("  - 변수값 입력 시 100바이트 제한 확인 (한글 약 50자, 영문 100자)")
            enhanced_items.append("  - 정상 케이스: '안녕하세요' 입력 시 정상 처리 확인")
            enhanced_items.append("  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 표시 확인")
        elif '그룹명' in title:
            enhanced_items.append("  - 주소록 그룹명 50바이트 제한 확인 (한글 약 25자, 영문 50자)")
            enhanced_items.append("  - 정상 케이스: 'VIP 고객' 입력 시 정상 처리 확인")
            enhanced_items.append("  - 비정상 케이스: 50바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(50바이트)를 초과했습니다' 알림 메시지 표시 확인")
            enhanced_items.append("  - 비정상 케이스: 미입력 시 '그룹명을 입력해주세요' 알림 메시지 노출 확인")
            enhanced_items.append("  - 비정상 케이스: 빈 문자열(공백만 입력) 시 미입력으로 처리 확인")
    
    # 선택 필드인 경우
    elif '선택' in title or '선택' in spec_item['function']:
        if '발신번호' in title:
            enhanced_items.append("  - 필수 선택 항목 확인")
            enhanced_items.append("  - 정상 케이스: 등록된 발신번호 목록에서 선택 시 정상 처리 확인")
            enhanced_items.append("  - 비정상 케이스: 발송 시 미선택 시 '발신번호를 선택해주세요' 알림 메시지 노출 확인")
    
    # 버튼/링크인 경우
    elif '버튼' in title or '링크' in title:
        enhanced_items.append("  - 클릭 시 해당 기능 실행 확인")
        if '이동' in spec_item['function'] or any('이동' in b for b in behaviors):
            for behavior in behaviors:
                if '이동' in behavior:
                    behavior = re.sub(r'\.html', '', behavior)
                    behavior = replace_html_to_pagename(behavior)
                    enhanced_items.append(f"  - 클릭 시 {behavior} 확인")
                    break
    
    # behavior에서 중요한 내용 추가
    important_behaviors = []
    for behavior in behaviors:
        if behavior.strip() and not behavior.startswith('【'):
            behavior = replace_html_to_pagename(behavior)
            behavior = re.sub(r'\([^)]*\)\s*호출', '', behavior)
            behavior = re.sub(r'\(#[^)]+\)', '', behavior)
            if behavior not in important_behaviors:
                important_behaviors.append(behavior.strip())
    
    # 중요한 behavior 추가 (이미 추가하지 않은 것만)
    for behavior in important_behaviors[:2]:
        if behavior and behavior not in ' '.join(enhanced_items):
            enhanced_items.append(f"  - {behavior}")
    
    # 제한사항 추가
    for behavior in behaviors:
        if '최소' in behavior or '최대' in behavior or '제한' in behavior or '바이트' in behavior:
            if '9자리' in behavior or '9자리 이상' in behavior:
                if '전화번호 최소 9자리 이상 입력 확인' not in ' '.join(enhanced_items):
                    enhanced_items.append("  - 전화번호 최소 9자리 이상 입력 확인")
            if '100바이트' in behavior:
                if '100바이트 제한' not in ' '.join(enhanced_items):
                    enhanced_items.append("  - 이름, 변수1~3 입력 시 100바이트 제한 확인 (한글 약 50자, 영문 100자)")
            if '50바이트' in behavior:
                if '50바이트 제한' not in ' '.join(enhanced_items):
                    enhanced_items.append("  - 주소록 그룹명 50바이트 제한 확인 (한글 약 25자, 영문 50자)")
            if '10,000건' in behavior or '10000건' in behavior:
                if '10,000건' not in ' '.join(enhanced_items):
                    enhanced_items.append("  - 최대 10,000건까지 입력 가능 확인")
            if '50,000건' in behavior or '50000건' in behavior:
                if '50,000건' not in ' '.join(enhanced_items):
                    enhanced_items.append("  - 최대 50,000건까지 업로드 가능 확인")
    
    return '<br>'.join(enhanced_items)

def replace_html_to_pagename(text):
    """HTML 파일명을 페이지명으로 변경"""
    
    replacements = [
        (r'index\.html', '메인'),
        (r'login\.html', '로그인'),
        (r'signup\.html', '회원가입'),
        (r'quote-inquiry\.html', '견적문의'),
        (r'find-id\.html', '아이디찾기'),
        (r'find-password\.html', '비밀번호찾기'),
        (r'main\.html', '대시보드'),
        (r'message-send-general\.html', '일반문자 발송'),
        (r'message-send-ad\.html', '광고문자 발송'),
        (r'template-message\.html', '일반문자 템플릿'),
        (r'template-message-ad\.html', '광고문자 템플릿'),
        (r'message-send-election\.html', '선거문자 발송'),
        (r'template-message-election\.html', '선거문자 템플릿'),
        (r'kakao-send-alimtalk\.html', '알림톡 발송'),
        (r'kakao-send-brandtalk\.html', '브랜드 메시지 발송'),
        (r'kakao-profile-manage\.html', '카카오톡 발신 프로필 관리'),
        (r'template-alimtalk\.html', '알림톡 템플릿'),
        (r'template-brandtalk\.html', '브랜드 메시지 템플릿'),
        (r'addressbook\.html', '주소록 관리'),
        (r'addressbook-reject\.html', '수신거부관리'),
        (r'send-result\.html', '발송결과'),
        (r'send-reservation\.html', '예약내역'),
        (r'payment-charge\.html', '충전'),
        (r'payment-history\.html', '결제 내역'),
        (r'payment-refund\.html', '환불'),
        (r'payment-tax\.html', '세금계산서 발행'),
        (r'mypage-profile\.html', '내 정보 수정'),
        (r'mypage-password\.html', '비밀번호 변경'),
        (r'mypage-caller-number\.html', '발신번호 관리'),
        (r'support-notice\.html', '공지사항'),
        (r'support-event\.html', '이벤트'),
        (r'support-faq\.html', 'FAQ'),
        (r'support-inquiry\.html', '1:1문의'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def enhance_expected_result(expected_result, spec_item):
    """예상 결과를 더 구체적으로 작성"""
    
    function = spec_item['function']
    behaviors = spec_item['behaviors']
    
    # function을 기본으로 사용
    enhanced = function
    
    # behavior에서 중요한 결과 추가
    for behavior in behaviors[:2]:
        if behavior.strip() and not behavior.startswith('【'):
            if '이동' in behavior or '표시' in behavior or '노출' in behavior:
                behavior = replace_html_to_pagename(behavior)
                if behavior not in enhanced:
                    enhanced += f", {behavior.strip()}"
                break
    
    return enhanced

def enhance_scenarios(content):
    """시나리오를 참고 문서 형식에 맞춰 더 구체적으로 작성"""
    
    # 이 함수는 향후 HTML 파일의 specData를 다시 읽어서 더 구체적으로 작성할 때 사용
    # 현재는 기본적인 개선만 수행
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip() or not re.match(r'^\|', line):
            new_lines.append(line)
            continue
        
        # 테이블 헤더는 그대로
        if '순번' in line and '테스트ID' in line:
            # 순서 열 제거 확인
            if '순서' in line:
                line = line.replace('| 순서 |', '')
            new_lines.append(line)
            continue
        
        if '---' in line:
            # 순서 열 제거 확인
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 15:  # 순서 열이 있는 경우
                # 순서 열 제거 (3번째 열)
                new_parts = parts[:2] + parts[3:]
                line = '|' + '|'.join(new_parts) + '|'
            new_lines.append(line)
            continue
        
        # 테이블 데이터 행 처리
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 6 and 'TS-' in line:
            # 순서 열 제거 (3번째 열)
            if len(parts) > 15:
                new_parts = parts[:2] + parts[3:]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_enhance'
    
    print("=" * 80)
    print("시나리오를 참고 문서 형식에 맞춰 더 구체적으로 작성")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 순서 열 제거 및 기본 개선
    print("\n순서 열 제거 및 기본 개선 중...")
    content = enhance_scenarios(content)
    
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
