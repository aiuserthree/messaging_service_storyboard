#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 화면설계 기능설명을 기반으로 테스트 시나리오 재작성
"""

import re
import os
from pathlib import Path

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

def extract_spec_data_from_html(html_content):
    """HTML에서 화면설계 기능설명 추출"""
    
    spec_items = []
    
    # specData 배열에서 기능설명 추출
    spec_data_match = re.search(r'const\s+specData\s*=\s*\[(.*?)\];', html_content, re.DOTALL)
    if spec_data_match:
        spec_data_str = spec_data_match.group(1)
        
        # 각 spec 항목 추출
        # { selector: '...', title: '...', function: '...', behavior: [...] }
        pattern = r'\{\s*selector:\s*[\'"]([^\'"]+)[\'"],\s*title:\s*[\'"]([^\'"]+)[\'"],\s*function:\s*[\'"]([^\'"]+)[\'"],\s*behavior:\s*\[(.*?)\]\s*\}'
        
        matches = re.finditer(pattern, spec_data_str, re.DOTALL)
        for match in matches:
            selector = match.group(1)
            title = match.group(2)
            function = match.group(3)
            behavior_str = match.group(4)
            
            # behavior 배열에서 항목 추출
            behaviors = []
            behavior_items = re.findall(r'[\'"]([^\'"]+)[\'"]', behavior_str)
            behaviors.extend(behavior_items)
            
            spec_items.append({
                'selector': selector,
                'title': title,
                'function': function,
                'behaviors': behaviors
            })
    
    return spec_items

def create_test_scenario_from_spec(spec_item, test_id_prefix, order):
    """화면설계 기능설명으로부터 테스트 시나리오 생성"""
    
    title = spec_item['title']
    function = spec_item['function']
    behaviors = spec_item['behaviors']
    
    # 단계별 작업 수행내용 생성
    work_content = f"- {title} 확인"
    if behaviors:
        for behavior in behaviors[:3]:  # 최대 3개만
            if behavior.strip() and not behavior.startswith('【'):
                work_content += f"<br>- {behavior.strip()}"
    
    # 예상 결과 생성
    expected_result = function
    if behaviors:
        key_behaviors = [b for b in behaviors if not b.startswith('【')][:2]
        if key_behaviors:
            expected_result += f", {', '.join(key_behaviors[:2])}"
    
    return {
        'order': order,
        'test_case_name': title,
        'work_content': work_content,
        'expected_result': expected_result
    }

def process_html_file(html_path, test_id_prefix, page_name):
    """HTML 파일 처리하여 시나리오 생성"""
    
    html_content = read_file(html_path)
    if not html_content:
        return []
    
    spec_items = extract_spec_data_from_html(html_content)
    
    scenarios = []
    order = 1
    
    for spec_item in spec_items:
        scenario = create_test_scenario_from_spec(spec_item, test_id_prefix, order)
        scenario['test_id'] = f"{test_id_prefix}-{order:03d}"
        scenarios.append(scenario)
        order += 1
    
    return scenarios

def fix_table_header_and_remove_test_data(content):
    """테이블 헤더 정리 및 테스트 데이터 열 제거"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더 정리
        if re.match(r'^\|+.*순번.*테스트ID', line):
            # 정규화된 헤더로 변경
            line = '| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |'
        
        # 테이블 구분선 정리
        elif re.match(r'^\|+.*---', line):
            line = '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'
        
        # 테이블 데이터 라인에서 테스트 데이터 열 제거
        elif re.match(r'^\|', line) and 'TS-' in line:
            parts = [p.strip() for p in line.split('|')]
            # 테스트 데이터 열이 있는 경우 제거 (보통 8번째 열)
            if len(parts) >= 9:
                # 테스트 데이터 열 제거
                new_parts = parts[:8] + parts[9:]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    # HTML 파일 경로 매핑
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
    
    base_path = r'c:\Users\ibank\Desktop\spec'
    test_file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = test_file_path + '.backup_rewrite'
    
    print("=" * 80)
    print("HTML 화면설계 기준으로 테스트 시나리오 재작성")
    print("=" * 80)
    
    # 백업
    content = read_file(test_file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    # 테이블 헤더 정리 및 테스트 데이터 열 제거
    print("\n[1] 테이블 헤더 정리 및 테스트 데이터 열 제거 중...")
    content = fix_table_header_and_remove_test_data(content)
    
    # 각 HTML 파일 처리
    print("\n[2] HTML 파일에서 화면설계 기능설명 추출 중...")
    all_scenarios = {}
    
    for test_id_prefix, (html_file, page_name) in html_files.items():
        html_path = os.path.join(base_path, html_file)
        print(f"  - {page_name} ({html_file}) 처리 중...")
        
        scenarios = process_html_file(html_path, test_id_prefix, page_name)
        if scenarios:
            all_scenarios[test_id_prefix] = {
                'page_name': page_name,
                'scenarios': scenarios
            }
            print(f"    → {len(scenarios)}개 시나리오 추출")
    
    print(f"\n총 {sum(len(s['scenarios']) for s in all_scenarios.values())}개 시나리오 추출됨")
    
    # 시나리오를 파일에 적용하는 것은 다음 단계에서...

if __name__ == '__main__':
    main()
