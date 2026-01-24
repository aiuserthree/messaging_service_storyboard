#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
메뉴 순서에 맞춰 섹션 번호 및 테스트ID 재정리
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

# 메뉴 순서 매핑 (현재 섹션 번호 -> 새로운 섹션 번호)
MENU_ORDER_MAP = {
    2: 1,   # 랜딩페이지 (TS-01)
    3: 2,   # 로그인 (TS-02)
    4: 3,   # 대시보드 (TS-03)
    5: 4,   # 일반문자 발송 (TS-04)
    6: 5,   # 광고문자 발송 (TS-05)
    7: 6,   # 일반문자 템플릿 (TS-06)
    8: 7,   # 광고문자 템플릿 (TS-07)
    9: 8,   # 선거문자 발송 (TS-08)
    10: 9,  # 선거문자 템플릿 (TS-09)
    11: 10, # 알림톡 발송 (TS-10)
    12: 11, # 브랜드 메시지 발송 (TS-11)
    13: 12, # 카카오톡 발신 프로필 (TS-12)
    14: 13, # 알림톡 템플릿 (TS-13)
    15: 14, # 브랜드 메시지 템플릿 (TS-14)
    18: 15, # 주소록 관리 (TS-15)
    19: 16, # 수신거부관리 (TS-16)
    16: 17, # 발송결과 (TS-17)
    17: 18, # 예약내역 (TS-18)
    21: 19, # 충전하기 (TS-19)
    22: 20, # 충전 내역 (TS-20)
    23: 21, # 환불 (TS-21)
    24: 22, # 세금계산서 발행 (TS-22)
    25: 23, # 내 정보 수정 (TS-23)
    26: 24, # 비밀번호 변경 (TS-24)
    27: 25, # 발신번호 관리 (TS-25)
    28: 26, # 공지사항 (TS-26)
    29: 27, # 이벤트 (TS-27)
    30: 28, # FAQ (TS-28)
    31: 29, # 1:1문의 (TS-29)
    20: None  # 회원가입은 별도 처리 필요
}

# 섹션 제목 매핑
SECTION_TITLES = {
    1: "랜딩페이지",
    2: "로그인",
    3: "대시보드",
    4: "일반문자 발송",
    5: "광고문자 발송",
    6: "일반문자 템플릿",
    7: "광고문자 템플릿",
    8: "선거문자 발송",
    9: "선거문자 템플릿",
    10: "알림톡 발송",
    11: "브랜드 메시지 발송",
    12: "카카오톡 발신 프로필",
    13: "알림톡 템플릿",
    14: "브랜드 메시지 템플릿",
    15: "주소록 관리",
    16: "수신거부관리",
    17: "발송결과",
    18: "예약내역",
    19: "충전하기",
    20: "충전 내역",
    21: "환불",
    22: "세금계산서 발행",
    23: "내 정보 수정",
    24: "비밀번호 변경",
    25: "발신번호 관리",
    26: "공지사항",
    27: "이벤트",
    28: "FAQ",
    29: "1:1문의"
}

def reorganize_sections(content):
    """섹션 번호와 테스트ID를 메뉴 순서에 맞춰 재정리"""
    lines = content.split('\n')
    new_lines = []
    current_section = None
    new_section_num = None
    
    for line in lines:
        # 섹션 헤더 찾기
        section_match = re.match(r'^## (\d+)\.\s+(.+)$', line)
        if section_match:
            old_section_num = int(section_match.group(1))
            section_title = section_match.group(2).strip()
            
            # 메뉴 순서 매핑 확인
            if old_section_num in MENU_ORDER_MAP:
                new_section_num = MENU_ORDER_MAP[old_section_num]
                if new_section_num:
                    new_title = SECTION_TITLES.get(new_section_num, section_title)
                    line = f"## {new_section_num}. {new_title}"
                    current_section = new_section_num
                else:
                    # 회원가입은 나중에 처리
                    continue
            else:
                current_section = None
                new_section_num = None
        
        # 테스트ID 변경
        if current_section and new_section_num:
            test_id_match = re.match(r'^(\|\s*\d+\s*\|)\s*(TS-\d+-\d+)\s*(\|)', line)
            if test_id_match:
                old_test_id = test_id_match.group(2)
                # TS-XX-YYY 형식에서 XX를 새로운 섹션 번호로 변경
                parts = old_test_id.split('-')
                if len(parts) == 3:
                    new_test_id = f"TS-{new_section_num:02d}-{parts[2]}"
                    line = test_id_match.group(1) + f' {new_test_id} ' + test_id_match.group(3)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_reorganize'
    
    print("=" * 80)
    print("메뉴 순서에 맞춰 섹션 및 테스트ID 재정리")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    print("\n[1] 섹션 번호 및 테스트ID 재정리 중...")
    content = reorganize_sections(content)
    
    if write_file(file_path, content):
        print(f"\n✓ 파일 수정 완료: {file_path}")
    else:
        print("\n✗ 파일 저장 실패")

if __name__ == '__main__':
    main()
