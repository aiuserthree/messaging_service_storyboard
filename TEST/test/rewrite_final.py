#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 파일의 화면설계 기능설명을 기반으로 테스트 시나리오 최종 재작성
- 구현된 기능만 포함
- 참고 문서 형식에 맞춰 구체적으로 작성
- 순번/순서 중복 제거
- 모바일/반응형 제거
- 입력 데이터 경우의 수 구체적으로 작성
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

def extract_spec_data_detailed(html_content):
    """HTML에서 specData 배열 상세 추출"""
    
    spec_items = []
    
    # specData 배열 찾기
    spec_data_match = re.search(r'const\s+specData\s*=\s*\[(.*?)\];', html_content, re.DOTALL)
    if not spec_data_match:
        return spec_items
    
    spec_data_str = spec_data_match.group(1)
    
    # 각 객체 추출
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
    
    # 각 객체 파싱
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
            # 문자열 리터럴 추출 (따옴표 안의 내용)
            behavior_items = re.findall(r"['\"]([^'\"]+)['\"]", behavior_str)
            behaviors.extend(behavior_items)
        
        # 번호 제거
        title = re.sub(r'^\d+\.\s*', '', title)
        
        if title and function:
            spec_items.append({
                'title': title,
                'function': function,
                'behaviors': behaviors
            })
    
    return spec_items

def create_detailed_work_content_from_spec(spec_item):
    """참고 문서 형식에 맞춰 단계별 작업 수행내용 생성"""
    
    work_items = []
    
    # 기본 확인
    work_items.append(f"- {spec_item['title']} 확인")
    
    # behavior에서 구체적인 내용 추출
    for behavior in spec_item['behaviors']:
        if behavior.strip():
            # 【】로 시작하는 것은 제목이므로 제외
            if behavior.startswith('【'):
                continue
            
            # • 로 시작하는 항목 처리
            if behavior.startswith('•'):
                behavior = behavior[1:].strip()
            
            # HTML 파일명을 페이지명으로 변경
            behavior = replace_html_to_pagename(behavior)
            # 개발 용어를 한글로 변경
            behavior = replace_tech_terms(behavior)
            # 모바일/반응형 제거
            if not re.search(r'반응형|모바일|mobile|responsive|햄버거', behavior, re.IGNORECASE):
                work_items.append(f"  - {behavior.strip()}")
    
    return '<br>'.join(work_items) if work_items else f"- {spec_item['title']} 확인"

def create_expected_result_from_spec(spec_item):
    """참고 문서 형식에 맞춰 예상 결과 생성"""
    
    expected = spec_item['function']
    
    # behavior에서 핵심 동작 추출
    key_behaviors = []
    for behavior in spec_item['behaviors']:
        if behavior.strip() and not behavior.startswith('【'):
            # 핵심 동작 추출
            if any(keyword in behavior for keyword in ['클릭 시', '입력 시', '선택 시', '이동', '표시', '확인', '노출']):
                behavior = replace_html_to_pagename(behavior)
                behavior = replace_tech_terms(behavior)
                # • 제거
                behavior = re.sub(r'^•\s*', '', behavior)
                if behavior.strip() and not re.search(r'반응형|모바일|mobile|responsive', behavior, re.IGNORECASE):
                    key_behaviors.append(behavior.strip())
                    if len(key_behaviors) >= 1:
                        break
    
    if key_behaviors:
        expected += f", {key_behaviors[0]}"
    
    return expected

def create_test_data_from_spec(spec_item):
    """입력 데이터 경우의 수 구체적으로 작성"""
    
    title = spec_item['title']
    behaviors = spec_item['behaviors']
    
    # 입력 필드인 경우 구체적인 예시
    if any(keyword in title for keyword in ['입력', '선택', '등록', '추가']):
        if '이메일' in title or '아이디' in title:
            return 'test@example.com'
        elif '비밀번호' in title:
            return 'Test1234!@'
        elif '전화번호' in title or '연락처' in title or '휴대폰' in title:
            return '010-1234-5678'
        elif '이름' in title or '담당자' in title:
            return '홍길동'
        elif '회사명' in title:
            return '테스트회사'
        elif '메시지' in title or '내용' in title:
            return '테스트 메시지 내용입니다'
        elif '발신번호' in title:
            return '010-1234-5678'
        elif '수신번호' in title:
            return '010-9876-5432'
        elif '그룹명' in title:
            return '테스트 그룹'
        elif '템플릿명' in title:
            return '테스트 템플릿'
        elif '금액' in title or '포인트' in title:
            return '10000'
        elif '발송량' in title:
            return '1000'
    
    # 선택 항목인 경우
    if '선택' in title:
        return '별도 테스트 아이디 없이 진행'
    
    # 기본값
    return '별도 테스트 아이디 없이 진행'

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
        (r'support-faq\.html', '자주 묻는 질문'),
        (r'support-inquiry\.html', '1:1문의'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def replace_tech_terms(text):
    """개발 용어를 한글로 변경"""
    
    replacements = [
        (r'\b모달\b', '팝업창'),
        (r'\bModal\b', '팝업창'),
        (r'모달\s*오픈', '팝업창 열기'),
        (r'모달\s*닫기', '팝업창 닫기'),
        (r'모달\s*호출', '팝업창 열기'),
        (r'모달\s*열림', '팝업창 열림'),
        (r'모달\s*닫힘', '팝업창 닫힘'),
        (r'기능\s*호출', '기능 실행'),
        (r'\bAPI\b', '서버 연동'),
        (r'\bGNB\b', '전역 메뉴'),
        (r'\bCTA\b', '행동 유도'),
        (r'\bFAQ\b', '자주 묻는 질문'),
        (r'\b컨테이너\b', '영역'),
        (r'\b폼\b', '입력 양식'),
        (r'\b그룹\b', '입력 항목'),
        (r'\b필드\b', '입력란'),
        (r'\b레이블\b', '항목명'),
        (r'\b체크박스\b', '선택 상자'),
        (r'\b토스트\b', '알림 메시지'),
        (r'\b아코디언\b', '접기/펼치기'),
        (r'\b드롭다운\b', '선택 목록'),
        (r'\b그리드\b', '목록'),
        (r'\b테이블\b', '목록'),
        (r'\bSubmit\s*이벤트\b', '제출 이벤트'),
        (r'\bpreventDefault\b', '기본 동작 방지'),
        (r'\blocalStorage\b', '브라우저 저장소'),
        (r'\bautocomplete\b', '자동완성'),
        (r'\bsticky\b', '고정'),
        (r'\bPrimary\s*CTA\b', '주요 행동 유도'),
        (r'\bPrimary\s*Action\b', '주요 동작'),
        (r'\bEnter\s*키\b', '엔터 키'),
        (r'\btype=password\b', '비밀번호 입력 형식'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def create_scenario_row_final(spec_item, order, test_id_prefix):
    """시나리오 테이블 행 생성 (최종)"""
    
    title = spec_item['title']
    
    # 단계별 작업 수행내용
    work_content = create_detailed_work_content_from_spec(spec_item)
    
    # 예상 결과
    expected_result = create_expected_result_from_spec(spec_item)
    
    # 테스트 데이터
    test_data = create_test_data_from_spec(spec_item)
    
    test_id = f"{test_id_prefix}-{order:03d}"
    
    # 페이지/팝업 판단
    page_type = "팝업" if "팝업창" in title or "모달" in title else "페이지"
    
    return f"| {order} | {test_id} | {title} | {page_type} | {work_content} | {test_data} | {expected_result} | | | | | | | | |"

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
        'TS-28': ('support-faq.html', '자주 묻는 질문'),
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
        
        spec_items = extract_spec_data_detailed(html_content)
        
        if spec_items:
            all_sections[test_id_prefix] = {
                'page_name': page_name,
                'scenarios': spec_items
            }
            print(f"    ✓ {len(spec_items)}개 기능 추출")
        else:
            print(f"    ✗ 기능설명을 찾을 수 없습니다.")
    
    return all_sections

def rewrite_markdown_complete(all_sections, original_content):
    """마크다운 파일 완전 재작성"""
    
    lines = original_content.split('\n')
    new_lines = []
    i = 0
    
    # 헤더 부분 유지
    while i < len(lines) and not re.match(r'^##\s*\d+\.', lines[i]):
        new_lines.append(lines[i])
        i += 1
    
    # 섹션별 처리
    while i < len(lines):
        line = lines[i]
        
        # 섹션 헤더 찾기
        section_match = re.match(r'^##\s*(\d+)\.\s*(.+)$', line)
        if section_match:
            section_num = section_match.group(1)
            section_name = section_match.group(2).strip()
            
            new_lines.append(line)
            i += 1
            
            # 해당 섹션의 테스트 ID 찾기
            test_id_prefix = None
            for prefix, data in all_sections.items():
                if data['page_name'] == section_name or section_name in data['page_name']:
                    test_id_prefix = prefix
                    break
            
            # 테이블 헤더 추가
            new_lines.append('| 순번 | 테스트ID | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과(연계 모듈 점검사항 확인) | | | 수정/오류 | 수정상태 | 수정담당자 | 처리결과 | 최종확인 | 비고 |')
            new_lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
            
            # 기존 테이블 행 건너뛰기
            while i < len(lines) and re.match(r'^\|', lines[i]):
                i += 1
            
            # 새로운 시나리오 추가
            if test_id_prefix and test_id_prefix in all_sections:
                scenarios = all_sections[test_id_prefix]['scenarios']
                for order, spec_item in enumerate(scenarios, 1):
                    scenario_row = create_scenario_row_final(spec_item, order, test_id_prefix)
                    new_lines.append(scenario_row)
            
            continue
        
        # 기존 테이블 행은 건너뛰기
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
    print("HTML 화면설계 기준으로 테스트 시나리오 최종 재작성")
    print("=" * 80)
    
    # 백업
    content = read_file(test_file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    # 모든 HTML 파일 처리
    print("\n[1] HTML 파일에서 화면설계 기능설명 추출 중...")
    all_sections = process_all_html_files()
    
    total_scenarios = sum(len(s['scenarios']) for s in all_sections.values())
    print(f"\n총 {total_scenarios}개 기능 추출됨")
    
    # 마크다운 파일 재작성
    print("\n[2] 테스트 시나리오 재작성 중...")
    new_content = rewrite_markdown_complete(all_sections, content)
    
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
