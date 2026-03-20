# TokBell Biz - Enterprise Messaging Platform

## 프로젝트 개요
TokBell Biz는 글로벌 1위 Infobip 인프라를 기반으로 한 엔터프라이즈 메시징 솔루션 랜딩 페이지입니다.

## 주요 기능
- ✅ **히어로 섹션**: 중앙 정렬 + 장식적 배경 요소(원, 점, 선, 스크롤 인디케이터)
- ✅ **Key Features Grid**: 4가지 핵심 기능 소개 (4열 그리드)
- ✅ **Pricing Strategy**: 중앙 정렬, 카드 그리드 레이아웃
- ✅ **Omni-Channel**: 중앙 정렬 헤더 + Domestic/Global 2열 그리드
- ✅ **Global Infrastructure**: 중앙 정렬 헤더 + 4열 숫자 강조 + 지역 목록
- ✅ **CDP (Hyper-Personalization)**: 중앙 정렬 + 3열 스텝 카드
- ✅ **FAQ Section**: 중앙 정렬 아코디언
- ✅ **Consultation Form**: 중앙 정렬 헤더 + 중앙 배치 폼
- ✅ **반응형 디자인**: 모바일/태블릿/데스크탑 대응
- ✅ **모바일 메뉴**: 햄버거 메뉴 토글

## 디자인 원칙
- **전체 중앙 정렬 레이아웃**: 모든 섹션의 제목, 설명, 콘텐츠가 중앙 배치
- **미니멀 모노톤**: #111111 (블랙) / #999999 (그레이) / #ffffff (화이트)
- **타이포그래피 중심**: 이미지 대신 큰 텍스트와 숫자로 임팩트 전달
- **Sharp 엣지**: border-radius 0px으로 기업용 느낌

## 기술 스택
- HTML5 + Tailwind CSS (CDN)
- Font Awesome 6.4.0
- Pretendard + Inter 폰트
- Vanilla JavaScript
- RESTful Table API (상담 문의 저장)

## 파일 구조
```
index.html          - 메인 랜딩 페이지
README.md           - 프로젝트 문서
```

## 진입 URI
- `/` 또는 `/index.html` - 메인 페이지

## 데이터 모델
### consultations 테이블
| 필드 | 설명 |
|------|------|
| company_name | 회사명 |
| contact_person | 담당자명 |
| phone | 연락처 |
| email | 이메일 |
| message | 문의 내용 |
| status | 접수 상태 |

## 향후 개발 제안
- 세계 지도 배경 이미지 추가 (Global Infrastructure 섹션)
- 다크 모드 지원
- 스크롤 트리거 애니메이션 (Intersection Observer)
- 관리자용 상담 내역 조회 페이지
