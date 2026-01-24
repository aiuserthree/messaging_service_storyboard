#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 specData에서 기능 설명 추출하여 시나리오 재작성
- 메뉴 순서대로 정리
- 한글 바이트는 1자에 2바이트로 계산
- 화면설계 기능설명에 없는 내용은 넣지 않기
- HTML URL 제거 또는 한글 페이지명으로 변경
- 모바일 반응형 테스트 내용 제거
- 변수값 글자수 제한, 주소록 그룹명 글자수 제한, 전화번호 최소 9자리 이상 등 세부 제약사항 포함
- 입력 데이터 구체적인 경우의 수 작성
"""

import re
import os
import json

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

def count_bytes_korean(text):
    """한글 1자 = 2바이트로 계산"""
    if not text:
        return 0
    byte_count = 0
    for char in text:
        if ord(char) > 127:  # 한글 등 멀티바이트 문자
            byte_count += 2
        else:  # 영문, 숫자 등
            byte_count += 1
    return byte_count

def remove_urls_and_replace_with_korean(text, url_mapping):
    """HTML URL을 한글 페이지명으로 변경"""
    if not text:
        return text
    result = text
    for url, korean_name in url_mapping.items():
        # .html로 끝나는 URL 패턴 (다양한 형태 처리)
        url_patterns = [
            re.escape(url),  # 기본 패턴
            f"{re.escape(url.replace('.html', ''))}\\.html",  # .html 포함
            f"클릭 시 {re.escape(url)}",  # "클릭 시 xxx.html"
            f"{re.escape(url)}로 이동",  # "xxx.html로 이동"
            f"{re.escape(url)} 페이지로 이동",  # "xxx.html 페이지로 이동"
            f"상세 페이지\\({re.escape(url)}\\)",  # "상세 페이지(xxx.html)"
        ]
        for pattern in url_patterns:
            result = re.sub(pattern, korean_name, result, flags=re.IGNORECASE)
        # file:/// 형태의 URL도 처리
        file_url_pattern = f"file:///[^\\s]+{re.escape(url)}"
        result = re.sub(file_url_pattern, korean_name, result)
    return result

def remove_mobile_responsive_content(text):
    """모바일 반응형 테스트 내용 제거"""
    if not text:
        return text
    # 모바일 관련 키워드가 포함된 문장 제거
    mobile_keywords = [
        '모바일', '반응형', 'responsive', 'mobile', '햄버거 메뉴',
        '화면 크기', 'viewport', '미디어 쿼리'
    ]
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        should_remove = False
        for keyword in mobile_keywords:
            if keyword in line:
                should_remove = True
                break
        if not should_remove:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def extract_specdata_from_html(html_content):
    """HTML에서 specData 추출 - 더 정확한 파싱"""
    if not html_content:
        return []
    
    # specData 배열 찾기
    specdata_pattern = r'const\s+specData\s*=\s*\[(.*?)\];'
    match = re.search(specdata_pattern, html_content, re.DOTALL)
    
    if not match:
        return []
    
    specdata_str = match.group(1)
    items = []
    
    # 중괄호로 객체 구분 (중첩된 객체 처리)
    brace_count = 0
    current_obj = ''
    objects = []
    
    for char in specdata_str:
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
    
    # 각 객체에서 정보 추출
    for obj_str in objects:
        item = {}
        
        # selector 추출
        selector_match = re.search(r'selector:\s*[\'"]([^\'"]+)[\'"]', obj_str)
        if selector_match:
            item['selector'] = selector_match.group(1)
        
        # title 추출 (번호 제거)
        title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', obj_str)
        if title_match:
            title = title_match.group(1)
            # 번호 제거 (예: "1. 페이지 헤더" -> "페이지 헤더")
            title = re.sub(r'^\d+\.\s*', '', title)
            item['title'] = title
        
        # function 추출
        function_match = re.search(r'function:\s*[\'"]([^\'"]+)[\'"]', obj_str)
        if function_match:
            item['function'] = function_match.group(1)
        
        # behavior 추출
        behavior_match = re.search(r'behavior:\s*\[(.*?)\]', obj_str, re.DOTALL)
        if behavior_match:
            behavior_str = behavior_match.group(1)
            # 문자열 리터럴 추출
            behaviors = re.findall(r'[\'"]([^\'"]+)[\'"]', behavior_str)
            # 모바일 반응형 내용 제거 및 빈 내용 필터링
            filtered_behaviors = []
            for b in behaviors:
                # 모바일 관련 키워드 제거
                if not any(kw in b for kw in ['모바일', '반응형', 'responsive', 'mobile', '햄버거']):
                    # 빈 내용이나 의미 없는 내용 제거
                    b = b.strip()
                    if b and len(b) > 1 and b not in [',', '.', '-', '•']:
                        filtered_behaviors.append(b)
            item['behavior'] = filtered_behaviors
        
        # description 추출 (있는 경우)
        desc_match = re.search(r'description:\s*[\'"]([^\'"]+)[\'"]', obj_str)
        if desc_match:
            item['description'] = desc_match.group(1)
        
        if item.get('title') and item.get('function'):
            items.append(item)
    
    return items

def create_detailed_test_cases(spec_item, test_id_prefix, seq):
    """specData를 기반으로 상세한 테스트 케이스 생성"""
    test_cases = []
    
    title = spec_item.get('title', '기능 확인')
    function = spec_item.get('function', '')
    behaviors = spec_item.get('behavior', [])
    description = spec_item.get('description', '')
    
    # URL 매핑 (HTML 파일명 -> 한글 페이지명)
    url_mapping = {
        'index.html': '랜딩페이지',
        'quote-inquiry.html': '견적문의',
        'login.html': '로그인',
        'find-id.html': '아이디찾기',
        'find-password.html': '비밀번호찾기',
        'signup.html': '회원가입',
        'main.html': '대시보드',
        'message-send-general.html': '일반문자 발송',
        'message-send-ad.html': '광고문자 발송',
        'template-message.html': '일반문자 템플릿',
        'template-message-ad.html': '광고문자 템플릿',
        'message-send-election.html': '선거문자 발송',
        'template-message-election.html': '선거문자 템플릿',
        'kakao-send-alimtalk.html': '알림톡 발송',
        'kakao-send-brandtalk.html': '브랜드 메시지 발송',
        'kakao-profile-manage.html': '카카오톡 발신 프로필',
        'template-alimtalk.html': '알림톡 템플릿',
        'template-brandtalk.html': '브랜드 메시지 템플릿',
        'addressbook.html': '주소록 관리',
        'addressbook-reject.html': '수신거부관리',
        'send-result.html': '발송결과',
        'send-reservation.html': '예약내역',
        'payment-charge.html': '충전하기',
        'payment-history.html': '충전 내역',
        'payment-refund.html': '환불',
        'payment-tax.html': '세금계산서 발행',
        'mypage-profile.html': '내 정보 수정',
        'mypage-password.html': '비밀번호 변경',
        'mypage-caller-number.html': '발신번호 관리',
        'support-notice.html': '공지사항',
        'support-event.html': '이벤트',
        'support-faq.html': 'FAQ',
        'support-inquiry.html': '1:1문의',
    }
    
    # 단계별 작업 수행내용 작성
    work_content_parts = []
    
    # function 추가
    if function:
        work_content_parts.append(f"- {function}")
    
    # behavior 추가 (URL 제거 및 한글 페이지명으로 변경)
    for behavior in behaviors:
        behavior_cleaned = remove_urls_and_replace_with_korean(behavior, url_mapping)
        behavior_cleaned = remove_mobile_responsive_content(behavior_cleaned)
        # 빈 내용이나 쉼표만 있는 내용은 제외
        behavior_cleaned = behavior_cleaned.strip()
        if behavior_cleaned and behavior_cleaned not in [',', '.', ''] and len(behavior_cleaned) > 1:
            work_content_parts.append(f"<br>- {behavior_cleaned}")
    
    # 입력 필드에 대한 구체적인 테스트 케이스 추가 (제목이나 기능에 해당 키워드가 명확히 포함된 경우만)
    if ('이름' in title or '이름' in function) and ('입력' in title or '입력' in function):
        # 이름 입력 필드
        work_content_parts.append("<br>- 이름 입력 시 바이트 수 확인")
        work_content_parts.append("<br>- 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인")
        work_content_parts.append("<br>- 정상 케이스: '홍길동' 입력 시 '6 / 100 바이트' 표시 확인")
        work_content_parts.append("<br>- 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인")
    
    if ('그룹명' in title or '그룹명' in function) and ('입력' in title or '입력' in function):
        # 그룹명 입력 필드
        work_content_parts.append("<br>- 그룹명 입력 시 바이트 수 확인")
        work_content_parts.append("<br>- 최대 50바이트 (한글 약 25자, 영문 50자) 제한 확인")
        work_content_parts.append("<br>- 정상 케이스: '고객그룹' 입력 시 '8 / 50 바이트' 표시 확인 (한글 1자 = 2바이트)")
        work_content_parts.append("<br>- 정상 케이스: 영문 20자 입력 시 '20 / 50 바이트' 표시 확인")
        work_content_parts.append("<br>- 비정상 케이스: 50바이트 초과 입력 시 자동 잘림 및 '입력 가능한 글자수(50바이트)를 초과했습니다' 알림 메시지 노출 확인")
    
    if (('전화번호' in title or '전화번호' in function or '연락처' in title or '연락처' in function) and 
        ('입력' in title or '입력' in function)):
        # 전화번호 입력 필드
        work_content_parts.append("<br>- 전화번호 최소 9자리 이상 입력 확인")
        work_content_parts.append("<br>- 정상 케이스: '010-1234-5678' 입력 시 정상 처리 확인")
        work_content_parts.append("<br>- 정상 케이스: '01012345678' 입력 시 자동 하이픈 포맷팅 확인")
        work_content_parts.append("<br>- 비정상 케이스: 9자리 미만 입력 시 '전화번호는 최소 9자리 이상 입력해주세요' 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: 숫자가 아닌 문자 입력 시 자동 제거 또는 알림 메시지 노출 확인")
    
    if ('변수' in title or '변수' in function) and ('입력' in title or '입력' in function):
        # 변수 입력 필드
        work_content_parts.append("<br>- 변수 입력 시 바이트 수 확인")
        work_content_parts.append("<br>- 최대 100바이트 (한글 약 50자, 영문 100자) 제한 확인")
        work_content_parts.append("<br>- 정상 케이스: 한글 30자 입력 시 '60 / 100 바이트' 표시 확인")
        work_content_parts.append("<br>- 비정상 케이스: 100바이트 초과 입력 시 자동 잘림 및 알림 메시지 노출 확인")
    
    if (('이메일' in title or '이메일' in function or ('아이디' in title and '입력' in title)) and 
        ('입력' in title or '입력' in function)):
        # 이메일 입력 필드
        work_content_parts.append("<br>- 정상 케이스: 'test@example.com' 입력 시 정상 처리 확인")
        work_content_parts.append("<br>- 비정상 케이스: '@'와 '.'이 없는 경우 '올바른 이메일 주소를 입력해 주세요' 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: @앞에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: .앞과 뒤에 영문텍스트가 없는 경우 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: 한글 텍스트가 입력된 경우 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: 입력값이 100자 이상인 경우 알림 메시지 노출 확인")
    
    if ('비밀번호' in title or '비밀번호' in function) and ('입력' in title or '입력' in function or '변경' in title or '변경' in function):
        # 비밀번호 입력 필드
        work_content_parts.append("<br>- 비밀번호 입력(영문,숫자,특수문자 포함 8~20자 이내) 조건에 따른 알림 메시지 노출/숨김 확인")
        work_content_parts.append("<br>- 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 알림 메시지 노출, 20자 이상 입력불가")
        work_content_parts.append("<br>- 정상 케이스: 'Test1234!@' 입력 시 정상 처리 확인")
        work_content_parts.append("<br>- 비정상 케이스: 7자 이하 입력 시 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: 21자 이상 입력 시 입력 불가 확인")
        work_content_parts.append("<br>- 비정상 케이스: 영문만 입력 시 알림 메시지 노출 확인")
        work_content_parts.append("<br>- 비정상 케이스: 숫자만 입력 시 알림 메시지 노출 확인")
    
    work_content = ''.join(work_content_parts) if work_content_parts else "- 기능 확인"
    
    # 예상 결과 작성
    expected_result = function if function else "기능이 정상적으로 작동해야 함"
    
    # 페이지/팝업 구분
    page_type = "팝업" if "모달" in title or "팝업" in title else "페이지"
    
    test_id = f"{test_id_prefix}-{seq:03d}"
    scenario_line = f"| {seq} | {test_id} | {title} | {page_type} | {work_content} | {expected_result} | | | | | | | | |"
    
    return scenario_line

# HTML 파일명 → 한글 페이지명 및 테스트 ID 매핑 (메뉴 순서대로)
PAGE_CONFIG = [
    {'file': 'index.html', 'name': '랜딩페이지', 'test_id': 'TS-01'},
    {'file': 'quote-inquiry.html', 'name': '견적문의', 'test_id': 'TS-01-01'},
    {'file': 'login.html', 'name': '로그인', 'test_id': 'TS-02'},
    {'file': 'find-id.html', 'name': '아이디찾기', 'test_id': 'TS-02-01'},
    {'file': 'find-password.html', 'name': '비밀번호찾기', 'test_id': 'TS-02-02'},
    {'file': 'signup.html', 'name': '회원가입', 'test_id': 'TS-02-03'},
    {'file': 'main.html', 'name': '대시보드', 'test_id': 'TS-03'},
    {'file': 'message-send-general.html', 'name': '일반문자 발송', 'test_id': 'TS-04'},
    {'file': 'message-send-ad.html', 'name': '광고문자 발송', 'test_id': 'TS-05'},
    {'file': 'template-message.html', 'name': '일반문자 템플릿', 'test_id': 'TS-06'},
    {'file': 'template-message-ad.html', 'name': '광고문자 템플릿', 'test_id': 'TS-07'},
    {'file': 'message-send-election.html', 'name': '선거문자 발송', 'test_id': 'TS-08'},
    {'file': 'template-message-election.html', 'name': '선거문자 템플릿', 'test_id': 'TS-09'},
    {'file': 'kakao-send-alimtalk.html', 'name': '알림톡 발송', 'test_id': 'TS-10'},
    {'file': 'kakao-send-brandtalk.html', 'name': '브랜드 메시지 발송', 'test_id': 'TS-11'},
    {'file': 'kakao-profile-manage.html', 'name': '카카오톡 발신 프로필', 'test_id': 'TS-12'},
    {'file': 'template-alimtalk.html', 'name': '알림톡 템플릿', 'test_id': 'TS-13'},
    {'file': 'template-brandtalk.html', 'name': '브랜드 메시지 템플릿', 'test_id': 'TS-14'},
    {'file': 'addressbook.html', 'name': '주소록 관리', 'test_id': 'TS-15'},
    {'file': 'addressbook-reject.html', 'name': '수신거부관리', 'test_id': 'TS-16'},
    {'file': 'send-result.html', 'name': '발송결과', 'test_id': 'TS-17'},
    {'file': 'send-reservation.html', 'name': '예약내역', 'test_id': 'TS-18'},
    {'file': 'payment-charge.html', 'name': '충전하기', 'test_id': 'TS-19'},
    {'file': 'payment-history.html', 'name': '충전 내역', 'test_id': 'TS-20'},
    {'file': 'payment-refund.html', 'name': '환불', 'test_id': 'TS-21'},
    {'file': 'payment-tax.html', 'name': '세금계산서 발행', 'test_id': 'TS-22'},
    {'file': 'mypage-profile.html', 'name': '내 정보 수정', 'test_id': 'TS-23'},
    {'file': 'mypage-password.html', 'name': '비밀번호 변경', 'test_id': 'TS-24'},
    {'file': 'mypage-caller-number.html', 'name': '발신번호 관리', 'test_id': 'TS-25'},
    {'file': 'support-notice.html', 'name': '공지사항', 'test_id': 'TS-26'},
    {'file': 'support-event.html', 'name': '이벤트', 'test_id': 'TS-27'},
    {'file': 'support-faq.html', 'name': 'FAQ', 'test_id': 'TS-28'},
    {'file': 'support-inquiry.html', 'name': '1:1문의', 'test_id': 'TS-29'},
]

def main():
    base_path = r'c:\Users\ibank\Desktop\spec'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    print("=" * 80)
    print("HTML 파일의 specData에서 기능 설명 추출하여 시나리오 재작성")
    print("=" * 80)
    
    all_sections = []
    
    # 헤더 작성
    header = """# 톡벨(Tokbell) 테스트 시나리오 상세
생성일: 2026-01-23
---

"""
    
    # 각 페이지 처리 (메뉴 순서대로)
    for config in PAGE_CONFIG:
        html_file = config['file']
        page_name = config['name']
        test_id_prefix = config['test_id']
        
        html_path = os.path.join(base_path, html_file)
        if not os.path.exists(html_path):
            print(f"  ⚠ {html_file} 파일을 찾을 수 없습니다.")
            continue
        
        print(f"\n[{test_id_prefix}] {page_name} ({html_file}) 처리 중...")
        html_content = read_file(html_path)
        
        if not html_content:
            continue
        
        # specData 추출
        spec_items = extract_specdata_from_html(html_content)
        
        if spec_items:
            print(f"  - {len(spec_items)}개 기능 설명 발견")
            
            # 섹션 헤더 작성 (TS-01 -> 1, TS-01-01 -> 1.1 형식)
            section_num = test_id_prefix.replace('TS-', '').replace('-', '.')
            # 숫자만 추출하여 섹션 번호 생성
            parts = section_num.split('.')
            if len(parts) == 1:
                section_num_formatted = f"{int(parts[0]):d}"
            else:
                section_num_formatted = f"{int(parts[0]):d}.{'.'.join(parts[1:])}"
            section_header = f"\n## {section_num_formatted}. {page_name}\n"
            section_header += "| 순번 | 테스트ID | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |\n"
            section_header += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            
            all_sections.append(section_header)
            
            # 각 spec 항목에 대해 시나리오 생성
            for idx, spec_item in enumerate(spec_items, 1):
                scenario = create_detailed_test_cases(spec_item, test_id_prefix, idx)
                all_sections.append(scenario)
        else:
            print(f"  - specData를 찾을 수 없습니다.")
    
    # 파일 작성
    content = header + '\n'.join(all_sections)
    
    # 백업 생성
    backup_path = output_file + '.backup_final_complete'
    existing_content = read_file(output_file)
    if existing_content:
        if write_file(backup_path, existing_content):
            print(f"\n백업 파일 생성: {backup_path}")
    
    if write_file(output_file, content):
        print(f"\n✅ 시나리오 재작성 완료: {output_file}")
        print(f"   총 {len(all_sections)}개 섹션 생성")
    else:
        print(f"\n❌ 파일 쓰기 실패: {output_file}")

if __name__ == '__main__':
    main()
