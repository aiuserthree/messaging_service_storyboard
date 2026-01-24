#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 화면설계 기능설명(specData)을 기반으로 테스트 시나리오 재작성 (최종)
- 구현된 기능만 포함
- 참고 문서 형식에 맞춰 구체적으로 작성
- 입력 데이터 구체적인 예시 포함 (정상/비정상 케이스)
- 제한사항 포함
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

def extract_spec_data(html_content):
    """HTML에서 specData 배열 추출 및 파싱"""
    
    spec_items = []
    
    # specData 배열 찾기
    spec_data_match = re.search(r'const\s+specData\s*=\s*\[(.*?)\];', html_content, re.DOTALL)
    if not spec_data_match:
        return spec_items
    
    spec_data_str = spec_data_match.group(1)
    
    # 각 객체 추출 (중괄호로 구분)
    brace_count = 0
    current_obj = ''
    objects = []
    
    for char in spec_data_str:
        if char == '{':
            brace_count += 1
            current_obj += char
        elif char == '}':
            brace_count -= 1
            current_obj += char
            if brace_count == 0:
                objects.append(current_obj)
                current_obj = ''
        else:
            if brace_count > 0:
                current_obj += char
    
    # 각 객체에서 title, function, behavior 추출
    for obj_str in objects:
        # title 추출
        title_match = re.search(r"title:\s*['\"]([^'\"]+)['\"]", obj_str)
        if not title_match:
            continue
        
        title = title_match.group(1)
        
        # function 추출
        function_match = re.search(r"function:\s*['\"]([^'\"]+)['\"]", obj_str)
        function = function_match.group(1) if function_match else ''
        
        # behavior 배열 추출
        behavior_match = re.search(r"behavior:\s*\[(.*?)\]", obj_str, re.DOTALL)
        behaviors = []
        if behavior_match:
            behavior_str = behavior_match.group(1)
            # 문자열 리터럴 추출
            behavior_items = re.findall(r"['\"]([^'\"]+)['\"]", behavior_str)
            behaviors.extend(behavior_items)
        
        # 번호 제거 (예: "1. 페이지 헤더" -> "페이지 헤더")
        title = re.sub(r'^\d+\.\s*', '', title)
        
        if title and function:
            spec_items.append({
                'title': title,
                'function': function,
                'behaviors': behaviors
            })
    
    return spec_items

def create_test_case_name(title, function):
    """테스트케이스명 생성 (참고 문서 형식)"""
    
    # 참고 문서 형식: "이메일 입력", "비밀번호 입력", "로그인 버튼" 등
    # 중복 제거
    if "입력 입력" in title:
        title = title.replace("입력 입력", "입력")
    if "선택 선택" in title:
        title = title.replace("선택 선택", "선택")
    
    if "확인" not in title and "입력" not in title and "선택" not in title:
        if "입력" in function:
            return f"{title} 입력"
        elif "선택" in function:
            return f"{title} 선택"
        elif "버튼" in title:
            return f"{title} 확인"
        else:
            return f"{title} 확인"
    
    return title

def create_work_content_detailed(spec_item, page_name):
    """단계별 작업 수행내용 생성 (참고 문서 형식 - 구체적)"""
    
    title = spec_item['title']
    function = spec_item['function']
    behaviors = spec_item['behaviors']
    
    work_items = []
    
    # 기본 확인 항목 (중복 제거)
    base_text = title
    if "입력 입력" in base_text:
        base_text = base_text.replace("입력 입력", "입력")
    if "선택 선택" in base_text:
        base_text = base_text.replace("선택 선택", "선택")
    
    if "입력" in title or "입력" in function:
        work_items.append(f"- {base_text} 확인")
    elif "선택" in title or "선택" in function:
        work_items.append(f"- {base_text} 확인")
    else:
        work_items.append(f"- {base_text} 확인")
    
    # 입력 필드인 경우 구체적인 예시 추가
    if "입력" in title or "입력" in function:
        # 이메일 입력
        if "이메일" in title or "이메일" in function or "아이디" in title:
            work_items.append("  - 이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개)")
            work_items.append("    (naver.com/gmail.com/icloud.com/kakao.com/daum.net/nate.com/hanmail.net)")
            work_items.append("  - 정상 케이스: 'test@naver.com' 입력 시 자동완성 목록 표시 확인")
            work_items.append("  - 비정상 케이스: '@'와 '.'이 없는 경우 '올바른 이메일 주소를 입력해 주세요' 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: @앞에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: .앞과 뒤에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: 한글 텍스트가 입력된 경우 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: 입력값이 100자 이상인 경우 알림 메시지 노출 확인")
        
        # 비밀번호 입력
        elif "비밀번호" in title or "비밀번호" in function:
            work_items.append("  - 비밀번호 입력(영문,숫자,특수문자 포함 8~20자 이내) 조건에 따른 알림 메시지 노출/숨김 확인")
            work_items.append("  - 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 알림 메시지 노출, 20자 이상 입력불가")
            work_items.append("  - 정상 케이스: 'Test1234!@' 입력 시 정상 처리 확인")
            work_items.append("  - 비정상 케이스: 7자 이하 입력 시 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: 21자 이상 입력 시 입력 불가 확인")
            work_items.append("  - 비정상 케이스: 영문만 입력 시 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: 숫자만 입력 시 알림 메시지 노출 확인")
        
        # 전화번호 입력
        elif "전화번호" in title or "연락처" in title or "휴대폰" in title:
            work_items.append("  - 전화번호 최소 9자리 이상 입력 확인")
            work_items.append("  - 정상 케이스: '010-1234-5678' 입력 시 정상 처리 확인")
            work_items.append("  - 정상 케이스: '01012345678' 입력 시 자동 하이픈 포맷팅 확인")
            work_items.append("  - 비정상 케이스: 9자리 미만 입력 시 '전화번호는 최소 9자리 이상 입력해주세요' 알림 메시지 노출 확인")
            work_items.append("  - 비정상 케이스: 숫자가 아닌 문자 입력 시 자동 제거 또는 알림 메시지 노출 확인")
        
        # 메시지 내용 입력
        elif "메시지" in title and ("내용" in title or "본문" in title):
            work_items.append("  - 메시지 내용 입력 시 바이트 수 실시간 표시 확인")
            work_items.append("  - SMS 선택 시: 최대 90바이트 (한글 약 45자, 영문 90자) 제한 확인")
            work_items.append("  - LMS 선택 시: 최대 2,000바이트 (한글 약 1,000자, 영문 2,000자) 제한 확인")
            work_items.append("  - 정상 케이스: 한글 40자 입력 시 '80 / 90 바이트' 표시 확인 (한글 1자 = 2바이트)")
            work_items.append("  - 정상 케이스: 영문 80자 입력 시 '80 / 90 바이트' 표시 확인")
            work_items.append("  - 비정상 케이스: SMS 선택 시 90바이트 초과 입력 시 LMS로 자동 전환 확인")
        
        # 제목 입력
        elif "제목" in title:
            work_items.append("  - 제목 입력 시 바이트 수 실시간 표시 확인")
            work_items.append("  - 최대 40바이트 (한글 20자, 영문 40자) 제한 확인")
            work_items.append("  - 정상 케이스: 한글 15자 입력 시 '30 / 40 바이트' 표시 확인")
            work_items.append("  - 비정상 케이스: 40바이트 초과 입력 시 '제목은 40바이트(한글 20자)를 초과할 수 없습니다' 알림 메시지 노출 확인")
        
        # 이름 입력
        elif "이름" in title and "그룹" not in title:
            work_items.append("  - 이름 입력 시 바이트 수 확인")
            work_items.append("  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인")
            work_items.append("  - 정상 케이스: '홍길동' 입력 시 '6 / 100 바이트' 표시 확인")
            work_items.append("  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인")
        
        # 변수 입력
        elif "변수" in title:
            work_items.append("  - 변수 입력 시 바이트 수 확인")
            work_items.append("  - 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인")
            work_items.append("  - 정상 케이스: 한글 30자 입력 시 '60 / 100 바이트' 표시 확인")
            work_items.append("  - 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인")
        
        # 그룹명 입력
        elif "그룹" in title and ("명" in title or "이름" in title):
            work_items.append("  - 그룹명 입력 시 바이트 수 확인")
            work_items.append("  - 최대 50바이트 (한글 약 25자, 영문 50자) 제한 확인")
            work_items.append("  - 정상 케이스: '고객그룹' 입력 시 '8 / 50 바이트' 표시 확인")
            work_items.append("  - 비정상 케이스: 50바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인")
        
        # 기타 입력 필드
        else:
            for behavior in behaviors[:2]:
                if behavior.strip() and not behavior.startswith('【'):
                    behavior = replace_html_to_pagename(behavior)
                    behavior = re.sub(r'\([^)]*\)\s*호출', '', behavior)
                    behavior = re.sub(r'\(#[^)]+\)', '', behavior)
                    if behavior.strip():
                        work_items.append(f"  - {behavior.strip()}")
    
    # 선택 필드인 경우
    elif "선택" in title or "선택" in function:
        for behavior in behaviors[:2]:
            if behavior.strip() and not behavior.startswith('【'):
                behavior = replace_html_to_pagename(behavior)
                behavior = re.sub(r'\([^)]*\)\s*호출', '', behavior)
                behavior = re.sub(r'\(#[^)]+\)', '', behavior)
                if behavior.strip():
                    work_items.append(f"  - {behavior.strip()}")
    
    # 버튼/링크인 경우
    elif "버튼" in title or "링크" in title or "메뉴" in title:
        for behavior in behaviors[:2]:
            if behavior.strip() and not behavior.startswith('【'):
                behavior = replace_html_to_pagename(behavior)
                behavior = re.sub(r'\([^)]*\)\s*호출', '', behavior)
                behavior = re.sub(r'\(#[^)]+\)', '', behavior)
                if behavior.strip():
                    work_items.append(f"  - {behavior.strip()}")
    
    # 기타
    else:
        for behavior in behaviors[:2]:
            if behavior.strip() and not behavior.startswith('【'):
                behavior = replace_html_to_pagename(behavior)
                behavior = re.sub(r'\([^)]*\)\s*호출', '', behavior)
                behavior = re.sub(r'\(#[^)]+\)', '', behavior)
                if behavior.strip():
                    work_items.append(f"  - {behavior.strip()}")
    
    # 제한사항 추가 (behavior에서 추출)
    for behavior in behaviors:
        if '10,000건' in behavior or '10000건' in behavior:
            work_items.append("  - 최대 10,000건까지 입력 가능 확인")
        if '50,000건' in behavior or '50000건' in behavior:
            work_items.append("  - 최대 50,000건까지 업로드 가능 확인")
    
    return '<br>'.join(work_items)

def create_expected_result_detailed(spec_item):
    """예상 결과 생성 (참고 문서 형식 - 명확하고 구체적)"""
    
    function = spec_item['function']
    behaviors = spec_item['behaviors']
    
    # function을 기본으로 사용
    expected = function
    
    # 입력 필드인 경우 구체적인 결과 추가
    if "입력" in spec_item['title'] or "입력" in function:
        if "이메일" in spec_item['title'] or "아이디" in spec_item['title']:
            expected = "이메일 자동완성 기능이 정상작동되어야 함"
        elif "비밀번호" in spec_item['title']:
            expected = "비밀번호 입력 시 비밀번호 입력 조건 알림이 정상적으로 표시되어야 함"
        elif "전화번호" in spec_item['title'] or "연락처" in spec_item['title']:
            expected = "전화번호 형식 검증 및 자동 포맷팅이 정상작동되어야 함"
        elif "메시지" in spec_item['title'] and ("내용" in spec_item['title'] or "본문" in spec_item['title']):
            expected = "입력된 메시지 바이트 수 실시간 표시, 한글 1자 = 2바이트 계산이 정확해야 함"
        elif "제목" in spec_item['title']:
            expected = "제목 바이트 수 실시간 표시 및 40바이트 제한이 정상작동되어야 함"
        elif "이름" in spec_item['title'] and "그룹" not in spec_item['title']:
            expected = "이름 입력 시 100바이트 제한이 정상작동되어야 함"
        elif "변수" in spec_item['title']:
            expected = "변수 입력 시 100바이트 제한이 정상작동되어야 함"
        elif "그룹" in spec_item['title'] and ("명" in spec_item['title'] or "이름" in spec_item['title']):
            expected = "그룹명 입력 시 50바이트 제한이 정상작동되어야 함"
    
    # 선택 필드인 경우
    elif "선택" in spec_item['title'] or "선택" in function:
        if "발신번호" in spec_item['title']:
            expected = "등록된 발신번호 목록이 정상적으로 표시되어야 함"
        else:
            expected = function
    
    # 버튼/링크인 경우
    elif "버튼" in spec_item['title'] or "링크" in spec_item['title']:
        for behavior in behaviors[:1]:
            if '이동' in behavior or '열림' in behavior:
                behavior = replace_html_to_pagename(behavior)
                expected = f"{function}, {behavior.strip()}"
                break
    
    return expected

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

def remove_mobile_responsive(content):
    """모바일/반응형 관련 내용 제거"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # 모바일/반응형 관련 키워드가 포함된 라인 제거
        if re.search(r'모바일|반응형|mobile|responsive|햄버거|햄버거 메뉴', line, re.IGNORECASE):
            continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def process_all_html_files():
    """모든 HTML 파일 처리"""
    
    base_path = r'c:\Users\ibank\Desktop\spec'
    
    html_files = {
        'TS-01': ('index.html', '랜딩페이지'),
        'TS-01-01': ('quote-inquiry.html', '견적문의'),
        'TS-02': ('login.html', '로그인'),
        'TS-02-01': ('find-id.html', '아이디찾기'),
        'TS-02-02': ('find-password.html', '비밀번호찾기'),
        'TS-02-03': ('signup.html', '회원가입'),
        'TS-03': ('main.html', '대시보드'),
        'TS-04': ('message-send-general.html', '일반문자 발송'),
        'TS-05': ('message-send-ad.html', '광고문자 발송'),
        'TS-06': ('template-message.html', '일반문자 템플릿'),
        'TS-07': ('template-message-ad.html', '광고문자 템플릿'),
        'TS-08': ('message-send-election.html', '선거문자 발송'),
        'TS-09': ('template-message-election.html', '선거문자 템플릿'),
        'TS-10': ('kakao-send-alimtalk.html', '알림톡 발송'),
        'TS-11': ('kakao-send-brandtalk.html', '브랜드 메시지 발송'),
        'TS-12': ('kakao-profile-manage.html', '카카오톡 발신 프로필'),
        'TS-13': ('template-alimtalk.html', '알림톡 템플릿'),
        'TS-14': ('template-brandtalk.html', '브랜드 메시지 템플릿'),
        'TS-15': ('addressbook.html', '주소록 관리'),
        'TS-16': ('addressbook-reject.html', '수신거부관리'),
        'TS-17': ('send-result.html', '발송결과'),
        'TS-18': ('send-reservation.html', '예약내역'),
        'TS-19': ('payment-charge.html', '충전하기'),
        'TS-20': ('payment-history.html', '충전 내역'),
        'TS-21': ('payment-refund.html', '환불'),
        'TS-22': ('payment-tax.html', '세금계산서 발행'),
        'TS-23': ('mypage-profile.html', '내 정보 수정'),
        'TS-24': ('mypage-password.html', '비밀번호 변경'),
        'TS-25': ('mypage-caller-number.html', '발신번호 관리'),
        'TS-26': ('support-notice.html', '공지사항'),
        'TS-27': ('support-event.html', '이벤트'),
        'TS-28': ('support-faq.html', 'FAQ'),
        'TS-29': ('support-inquiry.html', '1:1문의'),
    }
    
    all_sections = {}
    
    for test_id_prefix, (html_file, page_name) in html_files.items():
        html_path = os.path.join(base_path, html_file)
        print(f"  - {page_name} ({html_file}) 처리 중...")
        
        html_content = read_file(html_path)
        if not html_content:
            print(f"    ✗ 파일을 읽을 수 없습니다.")
            continue
        
        spec_items = extract_spec_data(html_content)
        
        if spec_items:
            all_sections[test_id_prefix] = {
                'page_name': page_name,
                'scenarios': spec_items
            }
            print(f"    ✓ {len(spec_items)}개 기능 추출")
        else:
            print(f"    ✗ 기능설명을 찾을 수 없습니다.")
    
    return all_sections

def create_scenario_row(spec_item, order, test_id_prefix, page_name):
    """시나리오 테이블 행 생성"""
    
    test_case_name = create_test_case_name(spec_item['title'], spec_item['function'])
    work_content = create_work_content_detailed(spec_item, page_name)
    expected_result = create_expected_result_detailed(spec_item)
    
    test_id = f"{test_id_prefix}-{order:03d}"
    
    # 페이지/팝업 판단
    page_type = "팝업" if "팝업" in spec_item['title'] or "모달" in spec_item['title'] else "페이지"
    
    return f"| {order} | {test_id} | {test_case_name} | {page_type} | {work_content} | {expected_result} | | | | | | | | |"

def rewrite_markdown_file(all_sections):
    """마크다운 파일 재작성"""
    
    test_file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 기존 파일 읽기
    content = read_file(test_file_path)
    if not content:
        return None
    
    # 모바일/반응형 제거
    content = remove_mobile_responsive(content)
    
    # 섹션별로 재작성
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 섹션 헤더 찾기 (## 번호. 페이지명 형식)
        section_match = re.match(r'^##\s*(\d+)(?:-(\d+))?\.\s*(.+)$', line)
        if section_match:
            section_num = section_match.group(1)
            sub_num = section_match.group(2)
            section_name = section_match.group(3).strip()
            
            # 해당 섹션의 테스트 ID 찾기
            test_id_prefix = None
            if sub_num:
                test_id_prefix = f"TS-{section_num}-{sub_num}"
            else:
                test_id_prefix = f"TS-{int(section_num):02d}"
            
            # 페이지명 매칭
            for prefix, data in all_sections.items():
                if data['page_name'] == section_name or section_name in data['page_name']:
                    test_id_prefix = prefix
                    break
            
            new_lines.append(line)
            i += 1
            
            # 테이블 헤더 추가 (순서 열 제거)
            if i < len(lines) and not re.match(r'^\|', lines[i]):
                new_lines.append('| 순번 | 테스트ID | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |')
                new_lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
            
            # 기존 테이블 행 건너뛰기
            while i < len(lines) and re.match(r'^\|', lines[i]):
                i += 1
            
            # 새로운 시나리오 추가
            if test_id_prefix and test_id_prefix in all_sections:
                scenarios = all_sections[test_id_prefix]['scenarios']
                for order, spec_item in enumerate(scenarios, 1):
                    scenario_row = create_scenario_row(
                        spec_item, order, test_id_prefix, all_sections[test_id_prefix]['page_name']
                    )
                    new_lines.append(scenario_row)
            
            continue
        
        # 기존 테이블 행은 건너뛰기 (섹션 내에서)
        if re.match(r'^\|', line) and '순번' not in line and '---' not in line:
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def main():
    test_file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = test_file_path + '.backup_final'
    
    print("=" * 80)
    print("HTML 화면설계 기준으로 테스트 시나리오 재작성 (최종)")
    print("=" * 80)
    
    # 백업
    content = read_file(test_file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    # 모든 HTML 파일에서 기능설명 추출
    print("\n[1] HTML 파일에서 화면설계 기능설명 추출 중...")
    all_sections = process_all_html_files()
    
    total_scenarios = sum(len(s['scenarios']) for s in all_sections.values())
    print(f"\n총 {total_scenarios}개 기능 추출됨")
    
    # 마크다운 파일 재작성
    print("\n[2] 테스트 시나리오 재작성 중...")
    new_content = rewrite_markdown_file(all_sections)
    
    if new_content and new_content != content:
        if write_file(test_file_path, new_content):
            print(f"\n✓ 파일 수정 완료: {test_file_path}")
            print(f"  백업 파일: {backup_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음 또는 재작성 실패")

if __name__ == '__main__':
    main()
