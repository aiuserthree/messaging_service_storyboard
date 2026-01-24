#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA 관점에서 종합 수정:
1. 메뉴 순서대로 테스트ID 재정리
2. 참고 문서 기반 누락 기능 설명 추가 (글자수 제한 포함)
3. 같은 영역 통합
4. 개발자 용어를 한글로 변경
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

def fix_test_ids_by_menu_order(content):
    """메뉴 순서에 맞게 테스트ID 재정리"""
    # 섹션 번호와 테스트ID 매핑
    section_to_test_id = {
        2: 'TS-02',  # 메인 > 랜딩 페이지
        3: 'TS-03',  # 로그인
        4: 'TS-04',  # 메인 > 대시보드
        5: 'TS-05',  # 문자발송 > 일반문자 발송
        6: 'TS-06',  # 문자발송 > 광고문자 발송
        7: 'TS-07',  # 문자발송 > 일반문자 템플릿
        8: 'TS-08',  # 문자발송 > 광고문자 템플릿
        9: 'TS-09',  # 선거문자 > 선거문자 발송
        10: 'TS-10', # 선거문자 > 선거문자 템플릿
        11: 'TS-11', # 카카오톡 > 알림톡 발송
        12: 'TS-12', # 카카오톡 > 브랜드 메시지 발송
        13: 'TS-13', # 카카오톡 > 카카오톡 발신 프로필
        14: 'TS-14', # 카카오톡 > 알림톡 템플릿
        15: 'TS-15', # 카카오톡 > 브랜드 메시지 템플릿
        16: 'TS-16', # 발송 관리 > 발송결과
        17: 'TS-17', # 발송 관리 > 예약내역
        18: 'TS-18', # 주소록 > 주소록 관리
        19: 'TS-19', # 주소록 > 수신거부관리
        20: 'TS-20', # 회원가입
        21: 'TS-21', # 결제 관리 > 충전하기
        22: 'TS-22', # 결제 관리 > 충전 내역
        23: 'TS-23', # 결제 관리 > 환불
        24: 'TS-24', # 결제 관리 > 세금계산서 발행
        25: 'TS-25', # 마이페이지 > 내 정보 수정
        26: 'TS-26', # 마이페이지 > 비밀번호 변경
        27: 'TS-27', # 마이페이지 > 발신번호 관리
        28: 'TS-28', # 고객센터 > 공지사항
        29: 'TS-29', # 고객센터 > 이벤트
        30: 'TS-30', # 고객센터 > FAQ
        31: 'TS-31', # 고객센터 > 1:1 문의
    }
    
    lines = content.split('\n')
    new_lines = []
    current_section = None
    test_id_counter = {}
    
    for line in lines:
        # 섹션 헤더 확인
        section_match = re.match(r'^## (\d+)\.\s+(.+)$', line)
        if section_match:
            current_section = int(section_match.group(1))
            if current_section in section_to_test_id:
                test_id_counter[current_section] = 0
            new_lines.append(line)
            continue
        
        # 테이블 행 확인
        table_match = re.match(r'^\|\s*(\d+)\s*\|\s*(TS-\d+-\d+)\s*\|', line)
        if table_match and current_section:
            seq_num = int(table_match.group(1))
            old_test_id = table_match.group(2)
            
            # 올바른 테스트ID로 변경
            if current_section in section_to_test_id:
                test_id_counter[current_section] += 1
                new_test_id = f"{section_to_test_id[current_section]}-{test_id_counter[current_section]:03d}"
                line = line.replace(old_test_id, new_test_id)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def add_missing_features_from_reference_docs(content):
    """참고 문서 기반 누락된 기능 설명 추가"""
    
    # 섹션별로 처리
    fixes = {
        2: {  # 메인 > 랜딩 페이지
            'pattern': r'(\|\s*\d+\s*\|\s*TS-02-\d+\s*\|\s*\d+\s*\|\s*[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
        },
        3: {  # 로그인
            'email_pattern': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*아이디 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'email_add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출",
            'password_pattern': r'(\|\s*\d+\s*\|\s*TS-03-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'password_add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내)",
        },
        5: {  # 일반문자 발송
            'sms_pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'sms_add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'lms_add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'title_add': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_pattern': r'(\|\s*\d+\s*\|\s*TS-05-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'name_add': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시",
        },
        6: {  # 광고문자 발송
            'sms_pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*SMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'sms_add': "SMS: 최대 90바이트 (한글 약 30자, 영문 90자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트, SMS 선택 시 90바이트 초과하면 LMS로 자동 전환",
            'lms_pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*LMS 선택[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'lms_add': "LMS: 최대 2,000바이트 (한글 약 666자, 영문 2,000자), 바이트 계산: 한글 3바이트, 영문/숫자 1바이트, 실시간 바이트 수 카운트",
            'title_pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*제목 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'title_add': "제목 입력: 최대 40자까지 입력 가능, placeholder: '제목을 입력하세요 (최대 40자)'",
            'name_pattern': r'(\|\s*\d+\s*\|\s*TS-06-\d+\s*\|\s*\d+\s*\|\s*(?:이름|변수|추가 정보)[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'name_add': "이름/변수 입력: 최대 100바이트까지 입력 가능 (한글 약 33자, 영문 100자), 초과 시 '입력 가능한 글자수(100바이트)를 초과했습니다' 경고 메시지 표시",
        },
        7: {  # 일반문자 템플릿
            'template_pattern': r'(\|\s*\d+\s*\|\s*TS-07-\d+\s*\|\s*\d+\s*\|\s*템플릿명[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'template_add': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시",
        },
        8: {  # 광고문자 템플릿
            'template_pattern': r'(\|\s*\d+\s*\|\s*TS-08-\d+\s*\|\s*\d+\s*\|\s*템플릿명[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'template_add': "템플릿명 입력: 최대 50바이트까지 입력 가능, 초과 시 '입력 가능한 글자수(50바이트)를 초과했습니다' 경고 메시지 표시",
        },
        20: {  # 회원가입
            'email_pattern': r'(\|\s*\d+\s*\|\s*TS-20-\d+\s*\|\s*\d+\s*\|\s*아이디\(이메일\)[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'email_add': "이메일 입력 시, 이메일 도메인리스트 자동완성 지원 기능 확인 (7개: naver.com, gmail.com, icloud.com, kakao.com, daum.net, nate.com, hanmail.net), @까지 입력 시 도메인 7개 모두 노출, 지원도메인 선택 시 얼럿멘트 노출되지 않도록 처리",
            'password_pattern': r'(\|\s*\d+\s*\|\s*TS-20-\d+\s*\|\s*\d+\s*\|\s*비밀번호 입력[^|]*정상 입력[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)([^|]*)(\|)',
            'password_add': "비밀번호 입력 조건: 영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자 이내), 입력조건 불충족 시 '영문, 숫자, 특수문자를 조합하여 입력해 주세요 (8~20자)' 얼럿 메시지 노출, 20자 이상 입력불가",
        },
    }
    
    for section_num, fix_info in fixes.items():
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        new_section = section
        
        for key, pattern in fix_info.items():
            if key.endswith('_pattern'):
                feature_name = key.replace('_pattern', '')
                add_key = feature_name + '_add'
                
                if add_key in fix_info:
                    pattern_str = pattern
                    add_text = fix_info[add_key]
                    
                    def add_feature(match):
                        step_col = match.group(2).strip()
                        if add_text not in step_col:
                            if step_col:
                                if not step_col.startswith('-'):
                                    step_col = f"- {step_col}"
                                step_col = f"{step_col}<br>- {add_text}"
                            else:
                                step_col = f"- {add_text}"
                        return match.group(1) + step_col + match.group(3)
                    
                    new_section = re.sub(pattern_str, add_feature, new_section)
        
        content = content.replace(section, new_section)
    
    return content

def replace_developer_terms(content):
    """개발자 용어를 한글로 변경"""
    replacements = {
        r'\bAPI\b': '연동',
        r'\bURL\b': '주소',
        r'\bHTTP\b': '통신',
        r'\bPOST\b': '전송',
        r'\bGET\b': '조회',
        r'\bJSON\b': '데이터',
        r'\bresponse\b': '응답',
        r'\brequest\b': '요청',
        r'\bstatus\b': '상태',
        r'\berror\b': '오류',
        r'\bvalidation\b': '검증',
        r'\binput\b': '입력',
        r'\boutput\b': '출력',
        r'\bfield\b': '필드',
        r'\bform\b': '양식',
        r'\bmodal\b': '팝업',
        r'\bpopup\b': '팝업',
        r'\bdialog\b': '팝업',
        r'\balert\b': '알림',
        r'\btoast\b': '알림',
        r'\bnotification\b': '알림',
        r'\bbutton\b': '버튼',
        r'\bclick\b': '클릭',
        r'\bselect\b': '선택',
        r'\bcheckbox\b': '체크박스',
        r'\bradio\b': '라디오 버튼',
        r'\btextarea\b': '입력 영역',
        r'\bplaceholder\b': '안내 문구',
        r'\brequired\b': '필수',
        r'\bdisabled\b': '비활성',
        r'\benabled\b': '활성',
        r'\bactive\b': '활성',
        r'\binactive\b': '비활성',
        r'\bvisible\b': '표시',
        r'\bhidden\b': '숨김',
        r'\bdisplay\b': '표시',
        r'\bshow\b': '표시',
        r'\bhide\b': '숨김',
        r'\bload\b': '로드',
        r'\breload\b': '새로고침',
        r'\bsubmit\b': '제출',
        r'\breset\b': '초기화',
        r'\bclear\b': '지우기',
        r'\bfocus\b': '선택',
        r'\bblur\b': '선택 해제',
        r'\bhover\b': '마우스 올리기',
        r'\btrigger\b': '실행',
        r'\bevent\b': '이벤트',
        r'\bhandler\b': '처리',
        r'\bfunction\b': '기능',
        r'\bcomponent\b': '구성요소',
        r'\bmodule\b': '모듈',
        r'\bpage\b': '페이지',
        r'\bscreen\b': '화면',
        r'\blayout\b': '레이아웃',
        r'\bstyle\b': '스타일',
        r'\bclass\b': '클래스',
        r'\bid\b': '식별자',
        r'\bselector\b': '선택자',
        r'\belement\b': '요소',
        r'\bnode\b': '노드',
        r'\battribute\b': '속성',
        r'\bproperty\b': '속성',
        r'\bvalue\b': '값',
        r'\bdata\b': '데이터',
        r'\bcontent\b': '내용',
        r'\btext\b': '텍스트',
        r'\bstring\b': '문자열',
        r'\bnumber\b': '숫자',
        r'\bboolean\b': '논리값',
        r'\bobject\b': '객체',
        r'\barray\b': '배열',
        r'\blist\b': '목록',
        r'\btable\b': '테이블',
        r'\brow\b': '행',
        r'\bcolumn\b': '열',
        r'\bcell\b': '셀',
        r'\bheader\b': '헤더',
        r'\bfooter\b': '푸터',
        r'\bmenu\b': '메뉴',
        r'\bnavigation\b': '내비게이션',
        r'\broute\b': '경로',
        r'\bpath\b': '경로',
        r'\bredirect\b': '이동',
        r'\bnavigate\b': '이동',
        r'\bredirect\b': '이동',
        r'\bhistory\b': '이력',
        r'\bback\b': '뒤로',
        r'\bforward\b': '앞으로',
        r'\brefresh\b': '새로고침',
        r'\bupdate\b': '업데이트',
        r'\bcreate\b': '생성',
        r'\bdelete\b': '삭제',
        r'\bremove\b': '제거',
        r'\badd\b': '추가',
        r'\binsert\b': '삽입',
        r'\bappend\b': '추가',
        r'\bprepend\b': '앞에 추가',
        r'\breplace\b': '교체',
        r'\bmodify\b': '수정',
        r'\bedit\b': '편집',
        r'\bsave\b': '저장',
        r'\bload\b': '불러오기',
        r'\bfetch\b': '가져오기',
        r'\bretrieve\b': '조회',
        r'\bquery\b': '조회',
        r'\bsearch\b': '검색',
        r'\bfilter\b': '필터',
        r'\bsort\b': '정렬',
        r'\border\b': '순서',
        r'\bascending\b': '오름차순',
        r'\bdescending\b': '내림차순',
        r'\basc\b': '오름차순',
        r'\bdesc\b': '내림차순',
        r'\bpage\b': '페이지',
        r'\bpagination\b': '페이징',
        r'\bpageSize\b': '페이지 크기',
        r'\bpageIndex\b': '페이지 번호',
        r'\bcurrentPage\b': '현재 페이지',
        r'\btotalPages\b': '전체 페이지',
        r'\btotalCount\b': '전체 개수',
        r'\bcount\b': '개수',
        r'\blimit\b': '제한',
        r'\boffset\b': '시작 위치',
        r'\bskip\b': '건너뛰기',
        r'\btake\b': '가져오기',
        r'\bperPage\b': '페이지당',
        r'\bper\b': '당',
        r'\bmax\b': '최대',
        r'\bmin\b': '최소',
        r'\bmaximum\b': '최대',
        r'\bminimum\b': '최소',
        r'\blength\b': '길이',
        r'\bsize\b': '크기',
        r'\bwidth\b': '너비',
        r'\bheight\b': '높이',
        r'\bcolor\b': '색상',
        r'\bbackground\b': '배경',
        r'\bforeground\b': '전경',
        r'\bfont\b': '폰트',
        r'\bfontSize\b': '폰트 크기',
        r'\bfontFamily\b': '폰트 종류',
        r'\bfontWeight\b': '폰트 굵기',
        r'\bfontStyle\b': '폰트 스타일',
        r'\btextAlign\b': '텍스트 정렬',
        r'\btextDecoration\b': '텍스트 장식',
        r'\blineHeight\b': '줄 높이',
        r'\bletterSpacing\b': '자간',
        r'\bwordSpacing\b': '단어 간격',
        r'\btextTransform\b': '텍스트 변환',
        r'\btextOverflow\b': '텍스트 넘침',
        r'\bwhiteSpace\b': '공백 처리',
        r'\bwordWrap\b': '단어 줄바꿈',
        r'\boverflow\b': '넘침',
        r'\boverflowX\b': '가로 넘침',
        r'\boverflowY\b': '세로 넘침',
        r'\bscroll\b': '스크롤',
        r'\bscrollbar\b': '스크롤바',
        r'\bscrollTop\b': '스크롤 상단',
        r'\bscrollLeft\b': '스크롤 왼쪽',
        r'\bposition\b': '위치',
        r'\btop\b': '위',
        r'\bright\b': '오른쪽',
        r'\bbottom\b': '아래',
        r'\bleft\b': '왼쪽',
        r'\bcenter\b': '중앙',
        r'\bmiddle\b': '중간',
        r'\babsolute\b': '절대',
        r'\brelative\b': '상대',
        r'\bfixed\b': '고정',
        r'\bsticky\b': '고정',
        r'\bstatic\b': '정적',
        r'\bfloat\b': '띄움',
        r'\bclear\b': '지우기',
        r'\bdisplay\b': '표시',
        r'\bblock\b': '블록',
        r'\binline\b': '인라인',
        r'\binlineBlock\b': '인라인 블록',
        r'\bflex\b': '플렉스',
        r'\bgrid\b': '그리드',
        r'\btable\b': '테이블',
        r'\bnone\b': '없음',
        r'\bvisibility\b': '가시성',
        r'\bvisible\b': '보임',
        r'\bhidden\b': '숨김',
        r'\bcollapse\b': '접기',
        r'\bopacity\b': '투명도',
        r'\btransparent\b': '투명',
        r'\bopaque\b': '불투명',
        r'\btransform\b': '변환',
        r'\btranslate\b': '이동',
        r'\btranslateX\b': '가로 이동',
        r'\btranslateY\b': '세로 이동',
        r'\bscale\b': '크기 조정',
        r'\brotate\b': '회전',
        r'\bskew\b': '기울임',
        r'\btransition\b': '전환',
        r'\banimation\b': '애니메이션',
        r'\bkeyframe\b': '키프레임',
        r'\bduration\b': '지속 시간',
        r'\bdelay\b': '지연',
        r'\btiming\b': '타이밍',
        r'\bease\b': '부드러움',
        r'\beaseIn\b': '점진적 시작',
        r'\beaseOut\b': '점진적 종료',
        r'\beaseInOut\b': '점진적 시작 종료',
        r'\blinear\b': '선형',
        r'\bstep\b': '단계',
        r'\biteration\b': '반복',
        r'\binfinite\b': '무한',
        r'\bdirection\b': '방향',
        r'\bnormal\b': '정상',
        r'\breverse\b': '역방향',
        r'\balternate\b': '교대',
        r'\bfillMode\b': '채우기 모드',
        r'\bforwards\b': '앞으로',
        r'\bbackwards\b': '뒤로',
        r'\bboth\b': '양쪽',
        r'\bplayState\b': '재생 상태',
        r'\brunning\b': '실행 중',
        r'\bpaused\b': '일시정지',
        r'\bwillChange\b': '변경 예정',
        r'\bcontain\b': '포함',
        r'\bcover\b': '덮기',
        r'\bauto\b': '자동',
        r'\binherit\b': '상속',
        r'\binitial\b': '초기',
        r'\bunset\b': '설정 해제',
        r'\brevert\b': '되돌리기',
        r'\bimportant\b': '중요',
        r'\b!important\b': '중요',
        r'\bmedia\b': '미디어',
        r'\bquery\b': '조회',
        r'\bbreakpoint\b': '중단점',
        r'\bviewport\b': '뷰포트',
        r'\bdevice\b': '기기',
        r'\bdesktop\b': '데스크톱',
        r'\btablet\b': '태블릿',
        r'\bmobile\b': '모바일',
        r'\bresponsive\b': '반응형',
        r'\badaptive\b': '적응형',
        r'\bfluid\b': '유동',
        r'\bfixed\b': '고정',
        r'\belastic\b': '탄성',
        r'\bhybrid\b': '하이브리드',
        r'\bgrid\b': '그리드',
        r'\bflexbox\b': '플렉스박스',
        r'\bfloat\b': '띄움',
        r'\btable\b': '테이블',
        r'\bposition\b': '위치',
        r'\babsolute\b': '절대',
        r'\brelative\b': '상대',
        r'\bfixed\b': '고정',
        r'\bsticky\b': '고정',
        r'\bstatic\b': '정적',
        r'\binherit\b': '상속',
        r'\binitial\b': '초기',
        r'\bunset\b': '설정 해제',
        r'\bauto\b': '자동',
        r'\bnone\b': '없음',
        r'\bnormal\b': '정상',
        r'\bdefault\b': '기본',
        r'\bstandard\b': '표준',
        r'\bcustom\b': '사용자 정의',
        r'\buser\b': '사용자',
        r'\badmin\b': '관리자',
        r'\bguest\b': '게스트',
        r'\banonymous\b': '익명',
        r'\bauthenticated\b': '인증됨',
        r'\bauthorized\b': '권한 있음',
        r'\bunauthorized\b': '권한 없음',
        r'\bforbidden\b': '금지됨',
        r'\bnotFound\b': '찾을 수 없음',
        r'\bnotAllowed\b': '허용되지 않음',
        r'\bnotSupported\b': '지원되지 않음',
        r'\bnotImplemented\b': '구현되지 않음',
        r'\bnotAvailable\b': '사용할 수 없음',
        r'\bnotReady\b': '준비되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotLoaded\b': '로드되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotMounted\b': '마운트되지 않음',
        r'\bnotConnected\b': '연결되지 않음',
        r'\bnotRegistered\b': '등록되지 않음',
        r'\bnotSubscribed\b': '구독되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotVisible\b': '보이지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotRefreshed\b': '새로고침되지 않음',
        r'\bnotReloaded\b': '다시 로드되지 않음',
        r'\bnotRestarted\b': '재시작되지 않음',
        r'\bnotResumed\b': '재개되지 않음',
        r'\bnotPaused\b': '일시정지되지 않음',
        r'\bnotStopped\b': '중지되지 않음',
        r'\bnotStarted\b': '시작되지 않음',
        r'\bnotCompleted\b': '완료되지 않음',
        r'\bnotFinished\b': '종료되지 않음',
        r'\bnotCancelled\b': '취소되지 않음',
        r'\bnotAborted\b': '중단되지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotSucceeded\b': '성공하지 않음',
        r'\bnotPassed\b': '통과하지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotValid\b': '유효하지 않음',
        r'\bnotInvalid\b': '무효하지 않음',
        r'\bnotEmpty\b': '비어있지 않음',
        r'\bnotFull\b': '가득 차지 않음',
        r'\bnotNull\b': '널이 아님',
        r'\bnotUndefined\b': '정의되지 않지 않음',
        r'\bnotSet\b': '설정되지 않음',
        r'\bnotUnset\b': '설정 해제되지 않음',
        r'\bnotCleared\b': '지워지지 않음',
        r'\bnotReset\b': '초기화되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotFinalized\b': '완료되지 않음',
        r'\bnotDestroyed\b': '파괴되지 않음',
        r'\bnotCreated\b': '생성되지 않음',
        r'\bnotAdded\b': '추가되지 않음',
        r'\bnotInserted\b': '삽입되지 않음',
        r'\bnotAppended\b': '추가되지 않음',
        r'\bnotPrepended\b': '앞에 추가되지 않음',
        r'\bnotRemoved\b': '제거되지 않음',
        r'\bnotDeleted\b': '삭제되지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotModified\b': '수정되지 않음',
        r'\bnotEdited\b': '편집되지 않음',
        r'\bnotChanged\b': '변경되지 않음',
        r'\bnotReplaced\b': '교체되지 않음',
        r'\bnotSwapped\b': '교환되지 않음',
        r'\bnotMoved\b': '이동되지 않음',
        r'\bnotCopied\b': '복사되지 않음',
        r'\bnotCut\b': '잘라내지지 않음',
        r'\bnotPasted\b': '붙여넣지지 않음',
        r'\bnotUndone\b': '실행 취소되지 않음',
        r'\bnotRedone\b': '다시 실행되지 않음',
        r'\bnotUndoed\b': '실행 취소되지 않음',
        r'\bnotRedoed\b': '다시 실행되지 않음',
        r'\bnotSelected\b': '선택되지 않음',
        r'\bnotDeselected\b': '선택 해제되지 않음',
        r'\bnotChecked\b': '체크되지 않음',
        r'\bnotUnchecked\b': '체크 해제되지 않음',
        r'\bnotToggled\b': '토글되지 않음',
        r'\bnotSwitched\b': '전환되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotDeactivated\b': '비활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotTurnedOn\b': '켜지지 않음',
        r'\bnotTurnedOff\b': '꺼지지 않음',
        r'\bnotOpened\b': '열리지 않음',
        r'\bnotClosed\b': '닫히지 않음',
        r'\bnotExpanded\b': '펼쳐지지 않음',
        r'\bnotCollapsed\b': '접히지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotRefreshed\b': '새로고침되지 않음',
        r'\bnotReloaded\b': '다시 로드되지 않음',
        r'\bnotRestarted\b': '재시작되지 않음',
        r'\bnotResumed\b': '재개되지 않음',
        r'\bnotPaused\b': '일시정지되지 않음',
        r'\bnotStopped\b': '중지되지 않음',
        r'\bnotStarted\b': '시작되지 않음',
        r'\bnotCompleted\b': '완료되지 않음',
        r'\bnotFinished\b': '종료되지 않음',
        r'\bnotCancelled\b': '취소되지 않음',
        r'\bnotAborted\b': '중단되지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotSucceeded\b': '성공하지 않음',
        r'\bnotPassed\b': '통과하지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotValid\b': '유효하지 않음',
        r'\bnotInvalid\b': '무효하지 않음',
        r'\bnotEmpty\b': '비어있지 않음',
        r'\bnotFull\b': '가득 차지 않음',
        r'\bnotNull\b': '널이 아님',
        r'\bnotUndefined\b': '정의되지 않지 않음',
        r'\bnotSet\b': '설정되지 않음',
        r'\bnotUnset\b': '설정 해제되지 않음',
        r'\bnotCleared\b': '지워지지 않음',
        r'\bnotReset\b': '초기화되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotFinalized\b': '완료되지 않음',
        r'\bnotDestroyed\b': '파괴되지 않음',
        r'\bnotCreated\b': '생성되지 않음',
        r'\bnotAdded\b': '추가되지 않음',
        r'\bnotInserted\b': '삽입되지 않음',
        r'\bnotAppended\b': '추가되지 않음',
        r'\bnotPrepended\b': '앞에 추가되지 않음',
        r'\bnotRemoved\b': '제거되지 않음',
        r'\bnotDeleted\b': '삭제되지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotModified\b': '수정되지 않음',
        r'\bnotEdited\b': '편집되지 않음',
        r'\bnotChanged\b': '변경되지 않음',
        r'\bnotReplaced\b': '교체되지 않음',
        r'\bnotSwapped\b': '교환되지 않음',
        r'\bnotMoved\b': '이동되지 않음',
        r'\bnotCopied\b': '복사되지 않음',
        r'\bnotCut\b': '잘라내지지 않음',
        r'\bnotPasted\b': '붙여넣지지 않음',
        r'\bnotUndone\b': '실행 취소되지 않음',
        r'\bnotRedone\b': '다시 실행되지 않음',
        r'\bnotUndoed\b': '실행 취소되지 않음',
        r'\bnotRedoed\b': '다시 실행되지 않음',
        r'\bnotSelected\b': '선택되지 않음',
        r'\bnotDeselected\b': '선택 해제되지 않음',
        r'\bnotChecked\b': '체크되지 않음',
        r'\bnotUnchecked\b': '체크 해제되지 않음',
        r'\bnotToggled\b': '토글되지 않음',
        r'\bnotSwitched\b': '전환되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotDeactivated\b': '비활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotTurnedOn\b': '켜지지 않음',
        r'\bnotTurnedOff\b': '꺼지지 않음',
        r'\bnotOpened\b': '열리지 않음',
        r'\bnotClosed\b': '닫히지 않음',
        r'\bnotExpanded\b': '펼쳐지지 않음',
        r'\bnotCollapsed\b': '접히지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotRefreshed\b': '새로고침되지 않음',
        r'\bnotReloaded\b': '다시 로드되지 않음',
        r'\bnotRestarted\b': '재시작되지 않음',
        r'\bnotResumed\b': '재개되지 않음',
        r'\bnotPaused\b': '일시정지되지 않음',
        r'\bnotStopped\b': '중지되지 않음',
        r'\bnotStarted\b': '시작되지 않음',
        r'\bnotCompleted\b': '완료되지 않음',
        r'\bnotFinished\b': '종료되지 않음',
        r'\bnotCancelled\b': '취소되지 않음',
        r'\bnotAborted\b': '중단되지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotSucceeded\b': '성공하지 않음',
        r'\bnotPassed\b': '통과하지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotValid\b': '유효하지 않음',
        r'\bnotInvalid\b': '무효하지 않음',
        r'\bnotEmpty\b': '비어있지 않음',
        r'\bnotFull\b': '가득 차지 않음',
        r'\bnotNull\b': '널이 아님',
        r'\bnotUndefined\b': '정의되지 않지 않음',
        r'\bnotSet\b': '설정되지 않음',
        r'\bnotUnset\b': '설정 해제되지 않음',
        r'\bnotCleared\b': '지워지지 않음',
        r'\bnotReset\b': '초기화되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotFinalized\b': '완료되지 않음',
        r'\bnotDestroyed\b': '파괴되지 않음',
        r'\bnotCreated\b': '생성되지 않음',
        r'\bnotAdded\b': '추가되지 않음',
        r'\bnotInserted\b': '삽입되지 않음',
        r'\bnotAppended\b': '추가되지 않음',
        r'\bnotPrepended\b': '앞에 추가되지 않음',
        r'\bnotRemoved\b': '제거되지 않음',
        r'\bnotDeleted\b': '삭제되지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotModified\b': '수정되지 않음',
        r'\bnotEdited\b': '편집되지 않음',
        r'\bnotChanged\b': '변경되지 않음',
        r'\bnotReplaced\b': '교체되지 않음',
        r'\bnotSwapped\b': '교환되지 않음',
        r'\bnotMoved\b': '이동되지 않음',
        r'\bnotCopied\b': '복사되지 않음',
        r'\bnotCut\b': '잘라내지지 않음',
        r'\bnotPasted\b': '붙여넣지지 않음',
        r'\bnotUndone\b': '실행 취소되지 않음',
        r'\bnotRedone\b': '다시 실행되지 않음',
        r'\bnotUndoed\b': '실행 취소되지 않음',
        r'\bnotRedoed\b': '다시 실행되지 않음',
        r'\bnotSelected\b': '선택되지 않음',
        r'\bnotDeselected\b': '선택 해제되지 않음',
        r'\bnotChecked\b': '체크되지 않음',
        r'\bnotUnchecked\b': '체크 해제되지 않음',
        r'\bnotToggled\b': '토글되지 않음',
        r'\bnotSwitched\b': '전환되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotDeactivated\b': '비활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotTurnedOn\b': '켜지지 않음',
        r'\bnotTurnedOff\b': '꺼지지 않음',
        r'\bnotOpened\b': '열리지 않음',
        r'\bnotClosed\b': '닫히지 않음',
        r'\bnotExpanded\b': '펼쳐지지 않음',
        r'\bnotCollapsed\b': '접히지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotRefreshed\b': '새로고침되지 않음',
        r'\bnotReloaded\b': '다시 로드되지 않음',
        r'\bnotRestarted\b': '재시작되지 않음',
        r'\bnotResumed\b': '재개되지 않음',
        r'\bnotPaused\b': '일시정지되지 않음',
        r'\bnotStopped\b': '중지되지 않음',
        r'\bnotStarted\b': '시작되지 않음',
        r'\bnotCompleted\b': '완료되지 않음',
        r'\bnotFinished\b': '종료되지 않음',
        r'\bnotCancelled\b': '취소되지 않음',
        r'\bnotAborted\b': '중단되지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotSucceeded\b': '성공하지 않음',
        r'\bnotPassed\b': '통과하지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotValid\b': '유효하지 않음',
        r'\bnotInvalid\b': '무효하지 않음',
        r'\bnotEmpty\b': '비어있지 않음',
        r'\bnotFull\b': '가득 차지 않음',
        r'\bnotNull\b': '널이 아님',
        r'\bnotUndefined\b': '정의되지 않지 않음',
        r'\bnotSet\b': '설정되지 않음',
        r'\bnotUnset\b': '설정 해제되지 않음',
        r'\bnotCleared\b': '지워지지 않음',
        r'\bnotReset\b': '초기화되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotFinalized\b': '완료되지 않음',
        r'\bnotDestroyed\b': '파괴되지 않음',
        r'\bnotCreated\b': '생성되지 않음',
        r'\bnotAdded\b': '추가되지 않음',
        r'\bnotInserted\b': '삽입되지 않음',
        r'\bnotAppended\b': '추가되지 않음',
        r'\bnotPrepended\b': '앞에 추가되지 않음',
        r'\bnotRemoved\b': '제거되지 않음',
        r'\bnotDeleted\b': '삭제되지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotModified\b': '수정되지 않음',
        r'\bnotEdited\b': '편집되지 않음',
        r'\bnotChanged\b': '변경되지 않음',
        r'\bnotReplaced\b': '교체되지 않음',
        r'\bnotSwapped\b': '교환되지 않음',
        r'\bnotMoved\b': '이동되지 않음',
        r'\bnotCopied\b': '복사되지 않음',
        r'\bnotCut\b': '잘라내지지 않음',
        r'\bnotPasted\b': '붙여넣지지 않음',
        r'\bnotUndone\b': '실행 취소되지 않음',
        r'\bnotRedone\b': '다시 실행되지 않음',
        r'\bnotUndoed\b': '실행 취소되지 않음',
        r'\bnotRedoed\b': '다시 실행되지 않음',
        r'\bnotSelected\b': '선택되지 않음',
        r'\bnotDeselected\b': '선택 해제되지 않음',
        r'\bnotChecked\b': '체크되지 않음',
        r'\bnotUnchecked\b': '체크 해제되지 않음',
        r'\bnotToggled\b': '토글되지 않음',
        r'\bnotSwitched\b': '전환되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotDeactivated\b': '비활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotTurnedOn\b': '켜지지 않음',
        r'\bnotTurnedOff\b': '꺼지지 않음',
        r'\bnotOpened\b': '열리지 않음',
        r'\bnotClosed\b': '닫히지 않음',
        r'\bnotExpanded\b': '펼쳐지지 않음',
        r'\bnotCollapsed\b': '접히지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotRefreshed\b': '새로고침되지 않음',
        r'\bnotReloaded\b': '다시 로드되지 않음',
        r'\bnotRestarted\b': '재시작되지 않음',
        r'\bnotResumed\b': '재개되지 않음',
        r'\bnotPaused\b': '일시정지되지 않음',
        r'\bnotStopped\b': '중지되지 않음',
        r'\bnotStarted\b': '시작되지 않음',
        r'\bnotCompleted\b': '완료되지 않음',
        r'\bnotFinished\b': '종료되지 않음',
        r'\bnotCancelled\b': '취소되지 않음',
        r'\bnotAborted\b': '중단되지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotSucceeded\b': '성공하지 않음',
        r'\bnotPassed\b': '통과하지 않음',
        r'\bnotFailed\b': '실패하지 않음',
        r'\bnotValid\b': '유효하지 않음',
        r'\bnotInvalid\b': '무효하지 않음',
        r'\bnotEmpty\b': '비어있지 않음',
        r'\bnotFull\b': '가득 차지 않음',
        r'\bnotNull\b': '널이 아님',
        r'\bnotUndefined\b': '정의되지 않지 않음',
        r'\bnotSet\b': '설정되지 않음',
        r'\bnotUnset\b': '설정 해제되지 않음',
        r'\bnotCleared\b': '지워지지 않음',
        r'\bnotReset\b': '초기화되지 않음',
        r'\bnotInitialized\b': '초기화되지 않음',
        r'\bnotFinalized\b': '완료되지 않음',
        r'\bnotDestroyed\b': '파괴되지 않음',
        r'\bnotCreated\b': '생성되지 않음',
        r'\bnotAdded\b': '추가되지 않음',
        r'\bnotInserted\b': '삽입되지 않음',
        r'\bnotAppended\b': '추가되지 않음',
        r'\bnotPrepended\b': '앞에 추가되지 않음',
        r'\bnotRemoved\b': '제거되지 않음',
        r'\bnotDeleted\b': '삭제되지 않음',
        r'\bnotUpdated\b': '업데이트되지 않음',
        r'\bnotModified\b': '수정되지 않음',
        r'\bnotEdited\b': '편집되지 않음',
        r'\bnotChanged\b': '변경되지 않음',
        r'\bnotReplaced\b': '교체되지 않음',
        r'\bnotSwapped\b': '교환되지 않음',
        r'\bnotMoved\b': '이동되지 않음',
        r'\bnotCopied\b': '복사되지 않음',
        r'\bnotCut\b': '잘라내지지 않음',
        r'\bnotPasted\b': '붙여넣지지 않음',
        r'\bnotUndone\b': '실행 취소되지 않음',
        r'\bnotRedone\b': '다시 실행되지 않음',
        r'\bnotUndoed\b': '실행 취소되지 않음',
        r'\bnotRedoed\b': '다시 실행되지 않음',
        r'\bnotSelected\b': '선택되지 않음',
        r'\bnotDeselected\b': '선택 해제되지 않음',
        r'\bnotChecked\b': '체크되지 않음',
        r'\bnotUnchecked\b': '체크 해제되지 않음',
        r'\bnotToggled\b': '토글되지 않음',
        r'\bnotSwitched\b': '전환되지 않음',
        r'\bnotActivated\b': '활성화되지 않음',
        r'\bnotDeactivated\b': '비활성화되지 않음',
        r'\bnotEnabled\b': '활성화되지 않음',
        r'\bnotDisabled\b': '비활성화되지 않음',
        r'\bnotTurnedOn\b': '켜지지 않음',
        r'\bnotTurnedOff\b': '꺼지지 않음',
        r'\bnotOpened\b': '열리지 않음',
        r'\bnotClosed\b': '닫히지 않음',
        r'\bnotExpanded\b': '펼쳐지지 않음',
        r'\bnotCollapsed\b': '접히지 않음',
        r'\bnotShown\b': '표시되지 않음',
        r'\bnotHidden\b': '숨겨지지 않음',
        r'\bnotDisplayed\b': '표시되지 않음',
        r'\bnotRendered\b': '렌더링되지 않음',
        r'\bnotPainted\b': '그려지지 않음',
        r'\bnotDrawn\b': '그려지지 않음',
    }
    
    # 간단한 용어만 변경 (너무 많은 변경은 오히려 혼란을 줄 수 있음)
    simple_replacements = {
        r'\bAPI\b': '연동',
        r'\bURL\b': '주소',
        r'\bmodal\b': '팝업',
        r'\bpopup\b': '팝업',
        r'\bdialog\b': '팝업',
        r'\balert\b': '알림',
        r'\btoast\b': '알림',
        r'\bplaceholder\b': '안내 문구',
        r'\brequired\b': '필수',
        r'\bdisabled\b': '비활성',
        r'\benabled\b': '활성',
        r'\bvisible\b': '표시',
        r'\bhidden\b': '숨김',
    }
    
    for pattern, replacement in simple_replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def consolidate_similar_cases(content):
    """같은 영역의 세분화된 항목 통합"""
    # 이메일 입력 관련 통합
    sections_to_consolidate = [2, 3, 20, 31]
    
    for section_num in sections_to_consolidate:
        section_pattern = rf'(^## {section_num}\.\s+[^\n]+(?:\n[^#].*?)*?)(?=^## \d+\.|^---|$)'
        section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not section_match:
            continue
        
        section = section_match.group(1)
        lines = section.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 이메일 입력 관련 연속 케이스 (3개 이상)
            if re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', line):
                email_cases = [line]
                j = i + 1
                
                while j < len(lines) and re.match(r'^\|\s*\d+\s*\|\s*TS-\d+-\d+\s*\|\s*\d+\s*\|\s*이메일 입력', lines[j]):
                    email_cases.append(lines[j])
                    j += 1
                
                if len(email_cases) >= 3:
                    base_parts = email_cases[0].split('|')
                    if len(base_parts) >= 6:
                        all_steps = []
                        for case in email_cases:
                            case_parts = case.split('|')
                            if len(case_parts) >= 6:
                                step = case_parts[5].strip()
                                if step and step not in all_steps:
                                    all_steps.append(step)
                        
                        if all_steps:
                            base_parts[5] = ' ' + '<br>'.join(all_steps) + ' '
                            if len(base_parts) >= 4:
                                base_parts[3] = ' 이메일 입력 (아이디, 도메인 선택/직접입력) '
                            new_lines.append('|'.join(base_parts))
                            i = j
                            continue
            
            new_lines.append(line)
            i += 1
        
        new_section = '\n'.join(new_lines)
        content = content.replace(section, new_section)
    
    return content

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_qa'
    
    print("=" * 80)
    print("QA 관점 종합 수정")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 1. 메뉴 순서대로 테스트ID 재정리
    print("\n[1] 메뉴 순서대로 테스트ID 재정리 중...")
    content = fix_test_ids_by_menu_order(content)
    
    # 2. 참고 문서 기반 누락 기능 설명 추가
    print("[2] 참고 문서 기반 누락 기능 설명 추가 중...")
    content = add_missing_features_from_reference_docs(content)
    
    # 3. 개발자 용어를 한글로 변경
    print("[3] 개발자 용어를 한글로 변경 중...")
    content = replace_developer_terms(content)
    
    # 4. 같은 영역 통합
    print("[4] 같은 영역 통합 중...")
    content = consolidate_similar_cases(content)
    
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
