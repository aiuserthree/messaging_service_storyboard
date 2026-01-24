#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 화면설계 기능설명(specData)을 기반으로 모든 테스트 시나리오 재작성
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
        
        # 주석 제거 (//로 시작하는 라인)
        title = re.sub(r'^\d+\.\s*', '', title)  # 앞의 번호 제거
        
        if title and function:
            spec_items.append({
                'title': title,
                'function': function,
                'behaviors': behaviors
            })
    
    return spec_items

def create_scenario_row(spec_item, order, test_id_prefix, page_name):
    """시나리오 테이블 행 생성"""
    
    title = spec_item['title']
    function = spec_item['function']
    behaviors = spec_item['behaviors']
    
    # 단계별 작업 수행내용 생성
    work_content = f"- {title} 확인"
    
    # behavior에서 중요한 내용만 추출 (【】 제거, 최대 2개)
    important_behaviors = []
    for behavior in behaviors:
        if behavior.strip() and not behavior.startswith('【'):
            # HTML 파일명을 페이지명으로 변경
            behavior = re.sub(r'\.html', '', behavior)
            behavior = re.sub(r'index\.html', '메인', behavior)
            behavior = re.sub(r'login\.html', '로그인', behavior)
            behavior = re.sub(r'signup\.html', '회원가입', behavior)
            behavior = re.sub(r'message-send-general\.html', '일반문자 발송', behavior)
            behavior = re.sub(r'message-send-ad\.html', '광고문자 발송', behavior)
            behavior = re.sub(r'template-message\.html', '일반문자 템플릿', behavior)
            behavior = re.sub(r'template-message-ad\.html', '광고문자 템플릿', behavior)
            behavior = re.sub(r'message-send-election\.html', '선거문자 발송', behavior)
            behavior = re.sub(r'template-message-election\.html', '선거문자 템플릿', behavior)
            behavior = re.sub(r'kakao-send-alimtalk\.html', '알림톡 발송', behavior)
            behavior = re.sub(r'kakao-send-brandtalk\.html', '브랜드 메시지 발송', behavior)
            behavior = re.sub(r'kakao-profile-manage\.html', '카카오톡 발신 프로필 관리', behavior)
            behavior = re.sub(r'template-alimtalk\.html', '알림톡 템플릿', behavior)
            behavior = re.sub(r'template-brandtalk\.html', '브랜드 메시지 템플릿', behavior)
            behavior = re.sub(r'addressbook\.html', '주소록 관리', behavior)
            behavior = re.sub(r'addressbook-reject\.html', '수신거부관리', behavior)
            behavior = re.sub(r'send-result\.html', '발송결과', behavior)
            behavior = re.sub(r'send-reservation\.html', '예약내역', behavior)
            behavior = re.sub(r'payment-charge\.html', '충전', behavior)
            behavior = re.sub(r'payment-history\.html', '결제 내역', behavior)
            behavior = re.sub(r'payment-refund\.html', '환불', behavior)
            behavior = re.sub(r'payment-tax\.html', '세금계산서 발행', behavior)
            behavior = re.sub(r'mypage-profile\.html', '내 정보 수정', behavior)
            behavior = re.sub(r'mypage-password\.html', '비밀번호 변경', behavior)
            behavior = re.sub(r'mypage-caller-number\.html', '발신번호 관리', behavior)
            behavior = re.sub(r'support-notice\.html', '공지사항', behavior)
            behavior = re.sub(r'support-event\.html', '이벤트', behavior)
            behavior = re.sub(r'support-faq\.html', 'FAQ', behavior)
            behavior = re.sub(r'support-inquiry\.html', '1:1문의', behavior)
            behavior = re.sub(r'quote-inquiry\.html', '견적문의', behavior)
            behavior = re.sub(r'find-id\.html', '아이디찾기', behavior)
            behavior = re.sub(r'find-password\.html', '비밀번호찾기', behavior)
            behavior = re.sub(r'main\.html', '대시보드', behavior)
            
            important_behaviors.append(behavior.strip())
            if len(important_behaviors) >= 2:
                break
    
    for behavior in important_behaviors:
        work_content += f"<br>- {behavior}"
    
    # 예상 결과 생성
    expected_result = function
    if important_behaviors:
        expected_result += f", {important_behaviors[0]}"
    
    # 한글 바이트 수정 (3바이트 → 2바이트)
    work_content = re.sub(r'한글\s*3바이트', '한글 2바이트', work_content)
    work_content = re.sub(r'한글\s*1자\s*=\s*3바이트', '한글 1자 = 2바이트', work_content)
    expected_result = re.sub(r'한글\s*3바이트', '한글 2바이트', expected_result)
    
    # 바이트 초과 경고 메시지 제거
    work_content = re.sub(r'입력 가능한 글자수.*?초과했습니다', '', work_content)
    work_content = re.sub(r'초과.*?경고\s*메시지', '', work_content)
    work_content = re.sub(r'경고\s*메시지.*?표시', '', work_content)
    
    test_id = f"{test_id_prefix}-{order:03d}"
    
    # 페이지/팝업 판단
    page_type = "팝업" if "모달" in title or "팝업" in title else "페이지"
    
    return f"| {order} | {test_id} | {order} | {title} | {page_type} | {work_content} | {expected_result} | | | | | | | | |"

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

def rewrite_markdown_file(all_sections):
    """마크다운 파일 재작성"""
    
    test_file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    
    # 기존 파일 읽기
    content = read_file(test_file_path)
    if not content:
        return None
    
    # 섹션별로 재작성
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 섹션 헤더 찾기 (## 번호. 페이지명 형식)
        section_match = re.match(r'^##\s*(\d+)\.\s*(.+)$', line)
        if section_match:
            section_num = section_match.group(1)
            section_name = section_match.group(2).strip()
            
            # 해당 섹션의 테스트 ID 찾기
            test_id_prefix = None
            for prefix, data in all_sections.items():
                if data['page_name'] == section_name or section_name in data['page_name']:
                    test_id_prefix = prefix
                    break
            
            new_lines.append(line)
            i += 1
            
            # 테이블 헤더 추가
            if i < len(lines) and not re.match(r'^\|', lines[i]):
                new_lines.append('| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |')
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
    backup_path = test_file_path + '.backup_rewrite_all'
    
    print("=" * 80)
    print("HTML 화면설계 기준으로 모든 테스트 시나리오 재작성")
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
    content = fix_table_structure(content)
    
    # 모든 HTML 파일에서 기능설명 추출
    print("\n[2] HTML 파일에서 화면설계 기능설명 추출 중...")
    all_sections = process_all_html_files()
    
    total_scenarios = sum(len(s['scenarios']) for s in all_sections.values())
    print(f"\n총 {total_scenarios}개 기능 추출됨")
    
    # 마크다운 파일 재작성
    print("\n[3] 테스트 시나리오 재작성 중...")
    new_content = rewrite_markdown_file(all_sections)
    
    if new_content and new_content != content:
        if write_file(test_file_path, new_content):
            print(f"\n✓ 파일 수정 완료: {test_file_path}")
            print(f"  백업 파일: {backup_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음 또는 재작성 실패")

def fix_table_structure(content):
    """테이블 헤더 정리 및 테스트 데이터 열 제거"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 테이블 헤더 정리
        if re.match(r'^\|+.*순번.*테스트ID', line):
            line = '| 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |'
        
        # 테이블 구분선 정리
        elif re.match(r'^\|+.*---', line):
            line = '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'
        
        # 테이블 데이터 라인에서 테스트 데이터 열 제거
        elif re.match(r'^\|', line) and 'TS-' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 9:
                # 테스트 데이터 열 제거 (보통 8번째 열)
                new_parts = parts[:8] + parts[9:]
                line = '|' + '|'.join(new_parts) + '|'
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

if __name__ == '__main__':
    main()
