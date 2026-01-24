#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 specData에서 기능 설명 추출하여 시나리오 재작성
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

def extract_specdata_from_html(html_content):
    """HTML에서 specData 추출"""
    specdata_pattern = r'const\s+specData\s*=\s*\[(.*?)\];'
    match = re.search(specdata_pattern, html_content, re.DOTALL)
    
    if not match:
        return []
    
    specdata_str = match.group(1)
    
    # JavaScript 객체를 파싱 (간단한 방법)
    items = []
    
    # 각 객체 추출
    obj_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    objects = re.findall(obj_pattern, specdata_str, re.DOTALL)
    
    for obj_str in objects:
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
        
        # behavior 추출
        behavior_match = re.search(r'behavior:\s*\[(.*?)\]', obj_str, re.DOTALL)
        if behavior_match:
            behavior_str = behavior_match.group(1)
            behaviors = re.findall(r'[\'"]([^\'"]+)[\'"]', behavior_str)
            item['behavior'] = behaviors
        
        if item:
            items.append(item)
    
    return items

def create_scenario_from_specdata(spec_items, test_id_prefix, page_name):
    """specData를 기반으로 시나리오 생성"""
    scenarios = []
    seq = 1
    
    for item in spec_items:
        test_id = f"{test_id_prefix}-{seq:03d}"
        test_case_name = item.get('title', '기능 확인')
        function_desc = item.get('function', '')
        behaviors = item.get('behavior', [])
        
        # 단계별 작업 수행내용 작성
        work_content = f"- {function_desc}"
        if behaviors:
            for behavior in behaviors[:3]:  # 최대 3개만
                work_content += f"<br>- {behavior}"
        
        # 예상 결과 작성
        expected_result = function_desc
        if behaviors:
            expected_result += f", {behaviors[0] if behaviors else ''}"
        
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

def main():
    base_path = r'c:\Users\ibank\Desktop\spec'
    output_file = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    print("=" * 80)
    print("HTML 파일의 specData에서 기능 설명 추출하여 시나리오 재작성")
    print("=" * 80)
    
    all_scenarios = []
    
    # 헤더 작성
    header = """# 톡벨(Tokbell) 테스트 시나리오 상세
생성일: 2026-01-22 02:07:19
---

## 1. 전체 요약
톡벨(Tokbell) 테스트 시나리오 요약

"""
    
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
        spec_items = extract_specdata_from_html(html_content)
        
        if spec_items:
            print(f"  - {len(spec_items)}개 기능 설명 발견")
            # 시나리오 생성
            section_header = f"\n## {config['test_id']}. {config['name']}\n"
            section_header += "| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |\n"
            section_header += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            
            scenarios = create_scenario_from_specdata(spec_items, config['test_id'], config['name'])
            all_scenarios.append(section_header)
            all_scenarios.extend(scenarios)
        else:
            print(f"  - specData를 찾을 수 없습니다.")
    
    # 파일 작성
    content = header + '\n'.join(all_scenarios)
    
    backup_path = output_file + '.backup_specdata_rewrite'
    if write_file(backup_path, read_file(output_file) or ''):
        print(f"\n백업 파일 생성: {backup_path}")
    
    if write_file(output_file, content):
        print(f"\n✓ 시나리오 재작성 완료: {output_file}")
        print(f"  총 {len([s for s in all_scenarios if s.startswith('|') and 'TS-' in s])}개 시나리오 생성")
    else:
        print("\n✗ 파일 저장 실패")

if __name__ == '__main__':
    main()
