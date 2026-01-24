#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
영어 페이지명 및 개발 용어를 한글로 변경 (수정 버전)
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

def translate_terms_line_by_line(content):
    """줄 단위로 처리하여 줄바꿈 보존"""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        
        # 모달/팝업 관련
        line = re.sub(r'\b모달\b', '팝업창', line)
        line = re.sub(r'\bModal\b', '팝업창', line, flags=re.IGNORECASE)
        line = re.sub(r'모달\s*오픈', '팝업창 열기', line)
        line = re.sub(r'모달\s*닫기', '팝업창 닫기', line)
        line = re.sub(r'모달\s*호출', '팝업창 열기', line)
        line = re.sub(r'모달\s*열림', '팝업창 열림', line)
        line = re.sub(r'모달\s*닫힘', '팝업창 닫힘', line)
        line = re.sub(r'모달\s*또는', '팝업창 또는', line)
        
        # 호출 관련
        line = re.sub(r'기능\s*호출', '기능 실행', line)
        line = re.sub(r'팝업창\s*호출', '팝업창 열기', line)
        
        # API 관련
        line = re.sub(r'\bAPI\s*조회', '서버에서 조회', line)
        line = re.sub(r'\bAPI\s*호출', '서버 연동', line)
        line = re.sub(r'\bAPI\b', '서버 연동', line)
        
        # 기술 용어
        line = re.sub(r'\bSubmit\s*이벤트\b', '제출 이벤트', line)
        line = re.sub(r'\bpreventDefault\b', '기본 동작 방지', line)
        line = re.sub(r'\blocalStorage\b', '브라우저 저장소', line)
        line = re.sub(r'\bautocomplete\b', '자동완성', line)
        line = re.sub(r'\bsticky\b', '고정', line)
        line = re.sub(r'\bPrimary\s*CTA\b', '주요 행동 유도', line)
        line = re.sub(r'\bPrimary\s*Action\b', '주요 동작', line)
        line = re.sub(r'\bEnter\s*키\b', '엔터 키', line)
        line = re.sub(r'\btype=password\b', '비밀번호 입력 형식', line)
        
        # UI 용어
        line = re.sub(r'\b컨테이너\b', '영역', line)
        line = re.sub(r'\bContainer\b', '영역', line, flags=re.IGNORECASE)
        line = re.sub(r'\b폼\b', '입력 양식', line)
        line = re.sub(r'\bForm\b', '입력 양식', line, flags=re.IGNORECASE)
        line = re.sub(r'입력\s*그룹\b', '입력 항목', line)
        line = re.sub(r'입력\s*필드\b', '입력란', line)
        line = re.sub(r'\b레이블\b', '항목명', line)
        line = re.sub(r'\bLabel\b', '항목명', line, flags=re.IGNORECASE)
        line = re.sub(r'\b체크박스\b', '선택 상자', line)
        line = re.sub(r'\bCheckbox\b', '선택 상자', line, flags=re.IGNORECASE)
        line = re.sub(r'\b토스트\b', '알림 메시지', line)
        line = re.sub(r'\bToast\b', '알림 메시지', line, flags=re.IGNORECASE)
        line = re.sub(r'\b아코디언\b', '접기/펼치기', line)
        line = re.sub(r'\bAccordion\b', '접기/펼치기', line, flags=re.IGNORECASE)
        line = re.sub(r'\b드롭다운\b', '선택 목록', line)
        line = re.sub(r'\bDropdown\b', '선택 목록', line, flags=re.IGNORECASE)
        line = re.sub(r'\b그리드\b', '목록', line)
        line = re.sub(r'\bGrid\b', '목록', line, flags=re.IGNORECASE)
        line = re.sub(r'\b테이블\b', '목록', line)
        line = re.sub(r'\bTable\b', '목록', line, flags=re.IGNORECASE)
        
        # 약어
        line = re.sub(r'\bGNB\b', '전역 메뉴', line)
        line = re.sub(r'\bCTA\b', '행동 유도', line)
        line = re.sub(r'\bFAQ\b', '자주 묻는 질문', line)
        
        # 함수명/변수명 제거
        line = re.sub(r'\(#\w+\)', '', line)  # (#phoneOnlyInputModal) 같은 것 제거
        line = re.sub(r'\(openAddRecipientModal\)', '', line)
        line = re.sub(r'\(closeModal\(', '(', line)
        line = re.sub(r'\(confirmAddRecipients\(\)', '', line)
        line = re.sub(r'\(#templateSelectModal\)', '', line)
        line = re.sub(r'\(#testSendModal\)', '', line)
        line = re.sub(r'\(#templateSaveModal\)', '', line)
        line = re.sub(r'\(#excelUploadModal\)', '', line)
        line = re.sub(r'\(#addToAddressBookModal\)', '', line)
        
        # 불필요한 공백 정리 (줄 내에서만)
        line = re.sub(r'\s{2,}', ' ', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_translate_fixed'
    
    # 백업 파일에서 복원
    backup_original = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md.backup_translate'
    
    print("=" * 80)
    print("영어 용어를 한글로 변경 (수정 버전)")
    print("=" * 80)
    
    # 백업 파일에서 원본 복원
    content = read_file(backup_original)
    if not content:
        print("백업 파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 용어 변경 (줄 단위로 처리)
    print("\n영어 용어를 한글로 변경 중...")
    content = translate_terms_line_by_line(content)
    
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
