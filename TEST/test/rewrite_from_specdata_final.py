#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 specData에서 기능 설명 추출하여 시나리오 완전 재작성 (개선 버전)
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

def extract_specdata_improved(html_content):
    """HTML에서 specData 개선된 방법으로 추출"""
    # specData 배열 찾기
    specdata_pattern = r'const\s+specData\s*=\s*\[(.*?)\];'
    match = re.search(specdata_pattern, html_content, re.DOTALL)
    
    if not match:
        return []
    
    specdata_str = match.group(1)
    items = []
    
    # 각 객체를 찾기 (중첩 객체 고려)
    obj_start = 0
    depth = 0
    in_string = False
    string_char = None
    escape_next = False
    
    i = 0
    while i < len(specdata_str):
        char = specdata_str[i]
        
        if escape_next:
            escape_next = False
            i += 1
            continue
        
        if char == '\\':
            escape_next = True
            i += 1
            continue
        
        if char in ['"', "'"] and not escape_next:
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        elif not in_string:
            if char == '{':
                if depth == 0:
                    obj_start = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    # 객체 완성
                    obj_str = specdata_str[obj_start:i+1]
                    item = parse_spec_object_improved(obj_str)
                    if item:
                        items.append(item)
        
        i += 1
    
    return items

def parse_spec_object_improved(obj_str):
    """specData 객체 문자열 개선된 파싱"""
    item = {}
    
    # selector 추출
    selector_match = re.search(r'selector:\s*[\'"]([^\'"]+)[\'"]', obj_str)
    if selector_match:
        item['selector'] = selector_match.group(1)
    
    # title 추출
    title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', obj_str)
    if title_match:
        item['title'] = title_match.group(1)
    
    # function 추출
    function_match = re.search(r'function:\s*[\'"]([^\'"]+)[\'"]', obj_str)
    if function_match:
        item['function'] = function_match.group(1)
    
    # behavior 추출 (더 정확하게)
    behavior_match = re.search(r'behavior:\s*\[(.*?)\]', obj_str, re.DOTALL)
    if behavior_match:
        behavior_str = behavior_match.group(1)
        # 문자열 내의 쉼표를 제외하고 분리
        behaviors = []
        # 각 문자열 항목 추출
        behavior_items = re.findall(r'[\'"]([^\'"]+)[\'"]', behavior_str)
        behaviors.extend(behavior_items)
        item['behavior'] = behaviors
    
    return item if (item.get('title') or item.get('function')) else None

def create_scenario_from_specdata_improved(spec_items, test_id_prefix, page_name):
    """specData를 기반으로 시나리오 생성 (개선)"""
    scenarios = []
    seq = 1
    
    for item in spec_items:
        test_id = f"{test_id_prefix}-{seq:03d}"
        test_case_name = item.get('title', '기능 확인')
        function_desc = item.get('function', '')
        behaviors = item.get('behavior', [])
        
        # 단계별 작업 수행내용 작성
        work_content_parts = []
        if function_desc:
            work_content_parts.append(f"- {function_desc}")
        
        # behavior에서 기능적인 내용만 포함
        functional_behaviors = []
        skip_keywords = ['배치', '색상', '스타일', '크기', '위치', '정렬', '그림자', '효과', '표시', '노출', '레이아웃']
        
        for behavior in behaviors:
            # 레이아웃/디자인 관련이 아닌 기능적인 내용만
            if not any(keyword in behavior for keyword in skip_keywords):
                functional_behaviors.append(behavior)
            elif any(func_keyword in behavior for func_keyword in ['입력', '선택', '클릭', '실행', '검증', '저장', '삭제', '수정', '발송', '등록']):
                # 기능 키워드가 있으면 포함
                functional_behaviors.append(behavior)
        
        # 최대 3개만 포함
        for behavior in functional_behaviors[:3]:
            work_content_parts.append(f"<br>- {behavior}")
        
        work_content = ''.join(work_content_parts) if work_content_parts else "- 기능 확인"
        
        # 예상 결과 작성
        expected_result = function_desc
        if functional_behaviors:
            expected_result += f", {functional_behaviors[0]}"
        
        scenario_line = f"| {seq} | {test_id} | {seq} | {test_case_name} | 페이지 | {work_content} | {expected_result} | | | | | | | | |"
        scenarios.append(scenario_line)
        seq += 1
    
    return scenarios

# HTML 파일명 → 한글 페이지명 및 테스트 ID 매핑
PAGE_CONFIG = {
    'index.html': {'name': '랜딩페이지', 'test_id': 'TS-01'},
    'quote-inquiry.html': {'name': '견적문의', 'test_id': 'TS-01-01'},
    'login.html': {'name': '로그인', 'test_id': 'TS-02'},
    'find-id.html': {'name': '아이디찾기', 'test_id': 'TS-02-01'},
    'find-password.html': {'name': '비밀번호찾기', 'test_id': 'TS-02-02'},
    'signup.html': {'name': '회원가입', 'test_id': 'TS-02-03'},
    'main.html': {'name': '대시보드', 'test_id': 'TS-03'},
    'message-send-general.html': {'name': '일반문자 발송', 'test_id': 'TS-04'},
    'message-send-ad.html': {'name': '광고문자 발송', 'test_id': 'TS-05'},
    'template-message.html': {'name': '일반문자 템플릿', 'test_id': 'TS-06'},
    'template-message-ad.html': {'name': '광고문자 템플릿', 'test_id': 'TS-07'},
    'message-send-election.html': {'name': '선거문자 발송', 'test_id': 'TS-08'},
    'template-message-election.html': {'name': '선거문자 템플릿', 'test_id': 'TS-09'},
    'kakao-send-alimtalk.html': {'name': '알림톡 발송', 'test_id': 'TS-10'},
    'kakao-send-brandtalk.html': {'name': '브랜드 메시지 발송', 'test_id': 'TS-11'},
    'kakao-profile-manage.html': {'name': '카카오톡 발신 프로필', 'test_id': 'TS-12'},
    'template-alimtalk.html': {'name': '알림톡 템플릿', 'test_id': 'TS-13'},
    'template-brandtalk.html': {'name': '브랜드 메시지 템플릿', 'test_id': 'TS-14'},
    'addressbook.html': {'name': '주소록 관리', 'test_id': 'TS-15'},
    'addressbook-reject.html': {'name': '수신거부관리', 'test_id': 'TS-16'},
    'send-result.html': {'name': '발송결과', 'test_id': 'TS-17'},
    'send-reservation.html': {'name': '예약내역', 'test_id': 'TS-18'},
    'payment-charge.html': {'name': '충전하기', 'test_id': 'TS-19'},
    'payment-history.html': {'name': '충전 내역', 'test_id': 'TS-20'},
    'payment-refund.html': {'name': '환불', 'test_id': 'TS-21'},
    'payment-tax.html': {'name': '세금계산서 발행', 'test_id': 'TS-22'},
    'mypage-profile.html': {'name': '내 정보 수정', 'test_id': 'TS-23'},
    'mypage-password.html': {'name': '비밀번호 변경', 'test_id': 'TS-24'},
    'mypage-caller-number.html': {'name': '발신번호 관리', 'test_id': 'TS-25'},
    'support-notice.html': {'name': '공지사항', 'test_id': 'TS-26'},
    'support-event.html': {'name': '이벤트', 'test_id': 'TS-27'},
    'support-faq.html': {'name': 'FAQ', 'test_id': 'TS-28'},
    'support-inquiry.html': {'name': '1:1문의', 'test_id': 'TS-29'},
}

def fix_hangul_byte_in_content(content):
    """내용에서 한글 바이트 2바이트로 수정"""
    
    replacements = [
        (r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트'),
        (r'\(한글\s*1자\s*=\s*3바이트\)', '(한글 1자 = 2바이트)'),
        (r'한글\s*3바이트', '한글 2바이트'),
        (r'한글\s*약\s*30자', '한글 약 45자'),
        (r'한글\s*약\s*25자', '한글 약 25자'),
        (r'한글\s*약\s*50자', '한글 약 50자'),
        (r'한글\s*약\s*666자', '한글 약 1000자'),
        (r'한글\s*2자\(6바이트\)', '한글 2자(4바이트)'),
        (r'한글\s*3자\(9바이트\)', '한글 3자(6바이트)'),
        (r'한글\s*5자\(15바이트\)', '한글 5자(10바이트)'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def replace_html_with_pagename_in_content(content):
    """내용에서 HTML 파일명을 한글 페이지명으로 변경"""
    
    replacements = {
        r'index\.html': '랜딩페이지',
        r'quote-inquiry\.html': '견적문의',
        r'login\.html': '로그인',
        r'find-id\.html': '아이디찾기',
        r'find-password\.html': '비밀번호찾기',
        r'signup\.html': '회원가입',
        r'main\.html': '대시보드',
        r'message-send-general\.html': '일반문자 발송',
        r'message-send-ad\.html': '광고문자 발송',
        r'template-message\.html': '일반문자 템플릿',
        r'template-message-ad\.html': '광고문자 템플릿',
        r'message-send-election\.html': '선거문자 발송',
        r'template-message-election\.html': '선거문자 템플릿',
        r'kakao-send-alimtalk\.html': '알림톡 발송',
        r'kakao-send-brandtalk\.html': '브랜드 메시지 발송',
        r'kakao-profile-manage\.html': '카카오톡 발신 프로필',
        r'template-alimtalk\.html': '알림톡 템플릿',
        r'template-brandtalk\.html': '브랜드 메시지 템플릿',
        r'addressbook\.html': '주소록 관리',
        r'addressbook-reject\.html': '수신거부관리',
        r'send-result\.html': '발송결과',
        r'send-reservation\.html': '예약내역',
        r'payment-charge\.html': '충전하기',
        r'payment-history\.html': '충전 내역',
        r'payment-refund\.html': '환불',
        r'payment-tax\.html': '세금계산서 발행',
        r'mypage-profile\.html': '내 정보 수정',
        r'mypage-password\.html': '비밀번호 변경',
        r'mypage-caller-number\.html': '발신번호 관리',
        r'support-notice\.html': '공지사항',
        r'support-event\.html': '이벤트',
        r'support-faq\.html': 'FAQ',
        r'support-inquiry\.html': '1:1문의',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def main():
    base_path = r'c:\Users\ibank\Desktop\spec'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    print("=" * 80)
    print("HTML 파일의 specData에서 기능 설명 추출하여 시나리오 완전 재작성 (개선)")
    print("=" * 80)
    
    all_sections = []
    
    # 헤더 작성
    header = """# 톡벨(Tokbell) 테스트 시나리오 상세
생성일: 2026-01-22 02:07:19
---

## 1. 전체 요약
톡벨(Tokbell) 테스트 시나리오 요약

"""
    
    all_sections.append(header)
    
    # 각 HTML 파일 처리
    for html_file, config in PAGE_CONFIG.items():
        html_path = os.path.join(base_path, html_file)
        if not os.path.exists(html_path):
            print(f"  ⚠ {html_file} 파일을 찾을 수 없습니다.")
            continue
        
        print(f"\n[{config['test_id']}] {config['name']} ({html_file}) 처리 중...")
        html_content = read_file(html_path)
        
        if not html_content:
            continue
        
        # specData 추출
        spec_items = extract_specdata_improved(html_content)
        
        if spec_items:
            print(f"  - {len(spec_items)}개 기능 설명 발견")
            # 시나리오 생성
            section_header = f"\n## {config['test_id']}. {config['name']}\n"
            section_header += "| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |\n"
            section_header += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            
            scenarios = create_scenario_from_specdata_improved(spec_items, config['test_id'], config['name'])
            all_sections.append(section_header)
            all_sections.extend(scenarios)
        else:
            print(f"  - specData를 찾을 수 없습니다.")
    
    # 파일 작성
    content = '\n'.join(all_sections)
    
    # 한글 바이트 2바이트로 수정
    print("\n한글 바이트 2바이트로 수정 중...")
    content = fix_hangul_byte_in_content(content)
    
    # HTML 파일명을 한글 페이지명으로 변경
    print("\nHTML 파일명을 한글 페이지명으로 변경 중...")
    content = replace_html_with_pagename_in_content(content)
    
    backup_path = output_file + '.backup_final_rewrite'
    original_content = read_file(output_file)
    if original_content and write_file(backup_path, original_content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    if write_file(output_file, content):
        print(f"\n✓ 시나리오 재작성 완료: {output_file}")
        total_scenarios = len([s for s in all_sections if s.startswith('|') and 'TS-' in s])
        print(f"  총 {total_scenarios}개 시나리오 생성")
    else:
        print("\n✗ 파일 저장 실패")

if __name__ == '__main__':
    main()
