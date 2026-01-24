#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
영어 페이지명 및 개발 용어를 한글로 변경
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

def translate_terms(content):
    """영어 용어를 한글로 변경"""
    
    # 개발 용어 → 한글
    replacements = [
        # 모달/팝업 관련
        (r'\b모달\b', '팝업창'),
        (r'\bModal\b', '팝업창'),
        (r'\b팝업\b', '팝업창'),
        (r'\bPopup\b', '팝업창'),
        (r'\bpopup\b', '팝업창'),
        (r'모달\s*오픈', '팝업창 열기'),
        (r'모달\s*닫기', '팝업창 닫기'),
        (r'모달\s*호출', '팝업창 열기'),
        (r'모달\s*열림', '팝업창 열림'),
        (r'모달\s*닫힘', '팝업창 닫힘'),
        (r'모달\s*또는', '팝업창 또는'),
        
        # 호출 관련
        (r'\b호출\b', '실행'),
        (r'\bCall\b', '실행'),
        (r'\bcall\b', '실행'),
        (r'기능\s*호출', '기능 실행'),
        (r'모달\s*호출', '팝업창 열기'),
        
        # API 관련
        (r'\bAPI\b', '서버 연동'),
        (r'\bapi\b', '서버 연동'),
        (r'API\s*조회', '서버에서 조회'),
        (r'API\s*호출', '서버 연동'),
        
        # 기술 용어
        (r'\bSubmit\s*이벤트\b', '제출 이벤트'),
        (r'\bpreventDefault\b', '기본 동작 방지'),
        (r'\blocalStorage\b', '브라우저 저장소'),
        (r'\bautocomplete\b', '자동완성'),
        (r'\bsticky\b', '고정'),
        (r'\bPrimary\s*CTA\b', '주요 행동 유도'),
        (r'\bPrimary\s*Action\b', '주요 동작'),
        (r'\bEnter\s*키\b', '엔터 키'),
        (r'\btype=password\b', '비밀번호 입력 형식'),
        
        # UI 용어
        (r'\b컨테이너\b', '영역'),
        (r'\bContainer\b', '영역'),
        (r'\b폼\b', '입력 양식'),
        (r'\bForm\b', '입력 양식'),
        (r'\b그룹\b', '입력 항목'),
        (r'\bGroup\b', '입력 항목'),
        (r'\b필드\b', '입력란'),
        (r'\bField\b', '입력란'),
        (r'\b레이블\b', '항목명'),
        (r'\bLabel\b', '항목명'),
        (r'\b체크박스\b', '선택 상자'),
        (r'\bCheckbox\b', '선택 상자'),
        (r'\b버튼\b', '버튼'),  # 버튼은 그대로
        (r'\bButton\b', '버튼'),
        (r'\b링크\b', '링크'),  # 링크는 그대로
        (r'\bLink\b', '링크'),
        (r'\b토스트\b', '알림 메시지'),
        (r'\bToast\b', '알림 메시지'),
        (r'\b아코디언\b', '접기/펼치기'),
        (r'\bAccordion\b', '접기/펼치기'),
        (r'\b드롭다운\b', '선택 목록'),
        (r'\bDropdown\b', '선택 목록'),
        (r'\b그리드\b', '목록'),
        (r'\bGrid\b', '목록'),
        (r'\b카드\b', '카드'),  # 카드는 그대로
        (r'\bCard\b', '카드'),
        (r'\b섹션\b', '영역'),
        (r'\bSection\b', '영역'),
        (r'\b영역\b', '영역'),  # 영역은 그대로
        
        # 약어
        (r'\bGNB\b', '전역 메뉴'),
        (r'\bCTA\b', '행동 유도'),
        (r'\bFAQ\b', '자주 묻는 질문'),
        
        # 기타 개발 용어
        (r'\b클릭\b', '클릭'),  # 클릭은 그대로
        (r'\bClick\b', '클릭'),
        (r'\b입력\b', '입력'),  # 입력은 그대로
        (r'\bInput\b', '입력'),
        (r'\b선택\b', '선택'),  # 선택은 그대로
        (r'\bSelect\b', '선택'),
        (r'\b테이블\b', '목록'),
        (r'\bTable\b', '목록'),
        (r'\b이벤트\b', '이벤트'),  # 이벤트는 그대로 (마케팅 이벤트)
        (r'\bEvent\b', '이벤트'),
        (r'\b이미지\b', '이미지'),  # 이미지는 그대로
        (r'\bImage\b', '이미지'),
        (r'\b아이콘\b', '아이콘'),  # 아이콘은 그대로
        (r'\bIcon\b', '아이콘'),
        (r'\b스크롤\b', '스크롤'),  # 스크롤은 그대로
        (r'\bScroll\b', '스크롤'),
        (r'\b로딩\b', '로딩'),  # 로딩은 그대로
        (r'\bLoading\b', '로딩'),
        (r'\b에러\b', '오류'),
        (r'\bError\b', '오류'),
        (r'\b성공\b', '성공'),  # 성공은 그대로
        (r'\bSuccess\b', '성공'),
        (r'\b경고\b', '경고'),  # 경고는 그대로
        (r'\bWarning\b', '경고'),
        (r'\b정보\b', '정보'),  # 정보는 그대로
        (r'\bInfo\b', '정보'),
        (r'\b확인\b', '확인'),  # 확인은 그대로
        (r'\bConfirm\b', '확인'),
        (r'\b취소\b', '취소'),  # 취소는 그대로
        (r'\bCancel\b', '취소'),
        (r'\b저장\b', '저장'),  # 저장은 그대로
        (r'\bSave\b', '저장'),
        (r'\b삭제\b', '삭제'),  # 삭제는 그대로
        (r'\bDelete\b', '삭제'),
        (r'\b수정\b', '수정'),  # 수정은 그대로
        (r'\bEdit\b', '수정'),
        (r'\b추가\b', '추가'),  # 추가는 그대로
        (r'\bAdd\b', '추가'),
        (r'\b등록\b', '등록'),  # 등록은 그대로
        (r'\bRegister\b', '등록'),
        (r'\b조회\b', '조회'),  # 조회는 그대로
        (r'\bSearch\b', '검색'),
        (r'\b검색\b', '검색'),  # 검색은 그대로
        (r'\bFind\b', '찾기'),
        (r'\b필터\b', '필터'),  # 필터는 그대로
        (r'\bFilter\b', '필터'),
        (r'\b정렬\b', '정렬'),  # 정렬은 그대로
        (r'\bSort\b', '정렬'),
        (r'\b페이징\b', '페이지 이동'),
        (r'\bPaging\b', '페이지 이동'),
        (r'\b페이지네이션\b', '페이지 이동'),
        (r'\bPagination\b', '페이지 이동'),
        (r'\b업로드\b', '업로드'),  # 업로드는 그대로
        (r'\bUpload\b', '업로드'),
        (r'\b다운로드\b', '다운로드'),  # 다운로드는 그대로
        (r'\bDownload\b', '다운로드'),
        (r'\b전송\b', '전송'),  # 전송은 그대로
        (r'\bSend\b', '발송'),
        (r'\b발송\b', '발송'),  # 발송은 그대로
        (r'\bDispatch\b', '발송'),
        (r'\b수신\b', '수신'),  # 수신은 그대로
        (r'\bReceive\b', '수신'),
        (r'\b요청\b', '요청'),  # 요청은 그대로
        (r'\bRequest\b', '요청'),
        (r'\b응답\b', '응답'),  # 응답은 그대로
        (r'\bResponse\b', '응답'),
        (r'\b처리\b', '처리'),  # 처리는 그대로
        (r'\bProcess\b', '처리'),
        (r'\b실행\b', '실행'),  # 실행은 그대로
        (r'\bExecute\b', '실행'),
        (r'\b시작\b', '시작'),  # 시작은 그대로
        (r'\bStart\b', '시작'),
        (r'\b중지\b', '중지'),  # 중지는 그대로
        (r'\bStop\b', '중지'),
        (r'\b일시정지\b', '일시정지'),  # 일시정지는 그대로
        (r'\bPause\b', '일시정지'),
        (r'\b재생\b', '재생'),  # 재생은 그대로
        (r'\bPlay\b', '재생'),
        (r'\b다음\b', '다음'),  # 다음은 그대로
        (r'\bNext\b', '다음'),
        (r'\b이전\b', '이전'),  # 이전은 그대로
        (r'\bPrevious\b', '이전'),
        (r'\b첫번째\b', '첫 번째'),
        (r'\bFirst\b', '첫 번째'),
        (r'\b마지막\b', '마지막'),  # 마지막은 그대로
        (r'\bLast\b', '마지막'),
        (r'\b전체\b', '전체'),  # 전체는 그대로
        (r'\bAll\b', '전체'),
        (r'\b선택\b', '선택'),  # 선택은 그대로
        (r'\bSelect\b', '선택'),
        (r'\b해제\b', '해제'),  # 해제는 그대로
        (r'\bDeselect\b', '해제'),
        (r'\b전체선택\b', '전체 선택'),
        (r'\bSelectAll\b', '전체 선택'),
        (r'\b전체해제\b', '전체 해제'),
        (r'\bDeselectAll\b', '전체 해제'),
        (r'\b체크\b', '선택'),
        (r'\bCheck\b', '선택'),
        (r'\b언체크\b', '선택 해제'),
        (r'\bUncheck\b', '선택 해제'),
        (r'\b활성화\b', '활성화'),  # 활성화는 그대로
        (r'\bEnable\b', '활성화'),
        (r'\b비활성화\b', '비활성화'),  # 비활성화는 그대로
        (r'\bDisable\b', '비활성화'),
        (r'\b표시\b', '표시'),  # 표시는 그대로
        (r'\bShow\b', '표시'),
        (r'\b숨김\b', '숨김'),  # 숨김은 그대로
        (r'\bHide\b', '숨김'),
        (r'\b열기\b', '열기'),  # 열기는 그대로
        (r'\bOpen\b', '열기'),
        (r'\b닫기\b', '닫기'),  # 닫기는 그대로
        (r'\bClose\b', '닫기'),
        (r'\b확장\b', '확장'),  # 확장은 그대로
        (r'\bExpand\b', '확장'),
        (r'\b축소\b', '축소'),  # 축소는 그대로
        (r'\bCollapse\b', '축소'),
        (r'\b펼치기\b', '펼치기'),  # 펼치기는 그대로
        (r'\bUnfold\b', '펼치기'),
        (r'\b접기\b', '접기'),  # 접기는 그대로
        (r'\bFold\b', '접기'),
        (r'\b새로고침\b', '새로고침'),  # 새로고침은 그대로
        (r'\bRefresh\b', '새로고침'),
        (r'\b갱신\b', '갱신'),  # 갱신은 그대로
        (r'\bUpdate\b', '갱신'),
        (r'\b동기화\b', '동기화'),  # 동기화는 그대로
        (r'\bSync\b', '동기화'),
        (r'\b연동\b', '연동'),  # 연동은 그대로
        (r'\bIntegration\b', '연동'),
        (r'\b연결\b', '연결'),  # 연결은 그대로
        (r'\bConnect\b', '연결'),
        (r'\b연결해제\b', '연결 해제'),
        (r'\bDisconnect\b', '연결 해제'),
        (r'\b인증\b', '인증'),  # 인증은 그대로
        (r'\bAuth\b', '인증'),
        (r'\b인가\b', '인가'),  # 인가는 그대로
        (r'\bAuthorization\b', '인가'),
        (r'\b권한\b', '권한'),  # 권한은 그대로
        (r'\bPermission\b', '권한'),
        (r'\b접근\b', '접근'),  # 접근은 그대로
        (r'\bAccess\b', '접근'),
        (r'\b로그인\b', '로그인'),  # 로그인은 그대로
        (r'\bLogin\b', '로그인'),
        (r'\b로그아웃\b', '로그아웃'),  # 로그아웃은 그대로
        (r'\bLogout\b', '로그아웃'),
        (r'\b회원가입\b', '회원가입'),  # 회원가입은 그대로
        (r'\bSignup\b', '회원가입'),
        (r'\b가입\b', '가입'),  # 가입은 그대로
        (r'\bJoin\b', '가입'),
        (r'\b탈퇴\b', '탈퇴'),  # 탈퇴는 그대로
        (r'\bWithdraw\b', '탈퇴'),
        (r'\b회원정보\b', '회원 정보'),
        (r'\bProfile\b', '회원 정보'),
        (r'\b설정\b', '설정'),  # 설정은 그대로
        (r'\bSetting\b', '설정'),
        (r'\b환경설정\b', '환경 설정'),
        (r'\bConfig\b', '환경 설정'),
        (r'\b옵션\b', '옵션'),  # 옵션은 그대로
        (r'\bOption\b', '옵션'),
        (r'\b기본값\b', '기본값'),  # 기본값은 그대로
        (r'\bDefault\b', '기본값'),
        (r'\b사용자\b', '사용자'),  # 사용자는 그대로
        (r'\bUser\b', '사용자'),
        (r'\b관리자\b', '관리자'),  # 관리자는 그대로
        (r'\bAdmin\b', '관리자'),
        (r'\b시스템\b', '시스템'),  # 시스템은 그대로
        (r'\bSystem\b', '시스템'),
        (r'\b서버\b', '서버'),  # 서버는 그대로
        (r'\bServer\b', '서버'),
        (r'\b클라이언트\b', '클라이언트'),  # 클라이언트는 그대로
        (r'\bClient\b', '클라이언트'),
        (r'\b데이터\b', '데이터'),  # 데이터는 그대로
        (r'\bData\b', '데이터'),
        (r'\b정보\b', '정보'),  # 정보는 그대로
        (r'\bInformation\b', '정보'),
        (r'\b내용\b', '내용'),  # 내용은 그대로
        (r'\bContent\b', '내용'),
        (r'\b제목\b', '제목'),  # 제목은 그대로
        (r'\bTitle\b', '제목'),
        (r'\b설명\b', '설명'),  # 설명은 그대로
        (r'\bDescription\b', '설명'),
        (r'\b메시지\b', '메시지'),  # 메시지는 그대로
        (r'\bMessage\b', '메시지'),
        (r'\b알림\b', '알림'),  # 알림은 그대로
        (r'\bNotification\b', '알림'),
        (r'\b공지\b', '공지'),  # 공지는 그대로
        (r'\bNotice\b', '공지'),
        (r'\b이벤트\b', '이벤트'),  # 이벤트는 그대로 (마케팅 이벤트)
        (r'\bEvent\b', '이벤트'),
        (r'\b이력\b', '이력'),  # 이력은 그대로
        (r'\bHistory\b', '이력'),
        (r'\b기록\b', '기록'),  # 기록은 그대로
        (r'\bRecord\b', '기록'),
        (r'\b로그\b', '로그'),  # 로그는 그대로
        (r'\bLog\b', '로그'),
        (r'\b상태\b', '상태'),  # 상태는 그대로
        (r'\bStatus\b', '상태'),
        (r'\b결과\b', '결과'),  # 결과는 그대로
        (r'\bResult\b', '결과'),
        (r'\b성공\b', '성공'),  # 성공은 그대로
        (r'\bSuccess\b', '성공'),
        (r'\b실패\b', '실패'),  # 실패는 그대로
        (r'\bFailure\b', '실패'),
        (r'\b완료\b', '완료'),  # 완료는 그대로
        (r'\bComplete\b', '완료'),
        (r'\b진행중\b', '진행 중'),
        (r'\bProgress\b', '진행 중'),
        (r'\b대기\b', '대기'),  # 대기는 그대로
        (r'\bWait\b', '대기'),
        (r'\b준비\b', '준비'),  # 준비는 그대로
        (r'\bReady\b', '준비'),
        (r'\b시작\b', '시작'),  # 시작은 그대로
        (r'\bStart\b', '시작'),
        (r'\b종료\b', '종료'),  # 종료는 그대로
        (r'\bEnd\b', '종료'),
        (r'\b취소\b', '취소'),  # 취소는 그대로
        (r'\bCancel\b', '취소'),
        (r'\b중단\b', '중단'),  # 중단은 그대로
        (r'\bAbort\b', '중단'),
        (r'\b재시도\b', '재시도'),  # 재시도는 그대로
        (r'\bRetry\b', '재시도'),
        (r'\b재개\b', '재개'),  # 재개는 그대로
        (r'\bResume\b', '재개'),
        (r'\b일시정지\b', '일시정지'),  # 일시정지는 그대로
        (r'\bPause\b', '일시정지'),
        (r'\b계속\b', '계속'),  # 계속은 그대로
        (r'\bContinue\b', '계속'),
        
        # 함수명/변수명 제거
        (r'\(#\w+\)', ''),  # (#phoneOnlyInputModal) 같은 것 제거
        (r'\(openAddRecipientModal\)', ''),
        (r'\(closeModal\(', ''),
        (r'\(confirmAddRecipients\(\)', ''),
        (r'\(#templateSelectModal\)', ''),
        (r'\(#testSendModal\)', ''),
        (r'\(#templateSaveModal\)', ''),
        (r'\(#excelUploadModal\)', ''),
        (r'\(#addToAddressBookModal\)', ''),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 중복 공백 정리
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'<br>\s*<br>', '<br>', content)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_translate'
    
    print("=" * 80)
    print("영어 용어를 한글로 변경")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 용어 변경
    print("\n영어 용어를 한글로 변경 중...")
    content = translate_terms(content)
    
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
