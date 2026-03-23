# tokbell — 비즈니스 메시징 플랫폼 랜딩페이지

## 프로젝트 개요
톡벨(tokbell)의 B2B 비즈니스 메시징 서비스 랜딩페이지입니다.
U.STRA CLOUD 스타일의 기업용 SaaS 디자인 시스템을 적용했습니다.

## 완료된 기능

### 페이지 섹션 (5개)
1. **Hero** — 핵심 메시지 + 4개 가치 카드
2. **Pricing** — 문자(SMS/LMS/MMS) + 카카오톡(알림톡/브랜드 메시지) 요금 카드
3. **Features Detail** — 주요 기능 3블록 교차 레이아웃
4. **FAQ** — 자주 묻는 질문 + 1:1 문의
5. **CTA Banner** — 견적 문의 유도

### 디자인 시스템
- **Primary**: #5CB85C (톡벨 로고 계열 그린)
- **Gradient**: #4a9d4e → #6bcf6b
- **Typography**: Noto Sans KR (300~900)
- **카드 라운드**: 20px / 12px
- **교차 배경**: white → #F7FAFC → dark(#1A202C~#2D3748)
- **그림자**: 0 4px 30px rgba(0,0,0,0.06)

### 인터랙션
- 스크롤 fade-in-up (200ms stagger)
- 공통 GNB( `header.js` ) 스크롤 시 `scrolled` 클래스
- 가격 숫자 count-up 애니메이션
- FAQ 아코디언 (한 번에 하나만 오픈)
- 랜딩 비교 바: **D** = 본 페이지 (`js/index-version-switch.js`)
- prefers-reduced-motion 접근성 지원

### 사이트 연동
- 상위 `spec`과 동일한 **GNB·푸터** (`header.js` / `footer.js`, `common.css`)
- 랜딩 본문은 `.landing-v12`로 스타일 스코프 (`css/style.css`)

## 파일 구조
```
index.html          — 메인 랜딩페이지
css/style.css       — 전체 스타일시트
js/main.js          — 인터랙션 스크립트
README.md           — 프로젝트 문서
```

## 진입 URI
- `/index.html` — 메인 페이지
- `#pricing` — 요금 섹션
- `#features` — 주요 기능 섹션
- `#faq` — FAQ 섹션

## 기술 스택
- 순수 HTML5 / CSS3 / Vanilla JS
- Google Fonts (Noto Sans KR)
- CSS Custom Properties
- IntersectionObserver API
- 외부 이미지 없음 (CSS 그라디언트/도형만 사용)
- 이모지 아이콘 사용 (외부 아이콘 라이브러리 없음)

## 미구현 기능
- 백엔드 연동 (로그인/회원가입)
- 실제 결제 시스템
- 발송 통계 대시보드
- 관리자 패널

## 다음 단계
1. CMS 또는 API 연동으로 공지사항 동적 로딩
2. 실제 회원가입/로그인 플로우
3. 가격 계산기 인터랙티브 도구
4. SEO 메타태그 및 OG 태그 추가
5. 퍼포먼스 최적화 (이미지 lazy load 등)
