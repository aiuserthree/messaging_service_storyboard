# 톡벨 (TOKBELL) — AI 기반 비즈니스 메시징 플랫폼

## 프로젝트 개요
톡벨 비즈니스 메시징 플랫폼의 메인 랜딩 페이지입니다.  
**모아샷(MOASHOT)** 디자인 스타일을 참고하여 B2B SaaS 랜딩 페이지로 제작되었습니다.

## 디자인 시스템
| 항목 | 값 |
|------|-----|
| **Primary** | `#5CB85C` (그린) |
| **Secondary** | `#333333` |
| **Accent** | `#FF6B35` (오렌지, 뱃지용) |
| **배경 교차** | `#FFFFFF` → `#F5F5F5` → `#FFFFFF` → `#1E1E2E` → `#FFFFFF` → `#2D2D2D` |
| **폰트** | Noto Sans KR (Google Fonts) |
| **제목** | 700-800 weight, 32-42px, letter-spacing: -0.5px |
| **본문** | 400 weight, 15-16px, line-height: 1.7, color: #666 |
| **카드** | border-radius: 16px, box-shadow: 0 4px 20px rgba(0,0,0,0.08) |
| **버튼** | border-radius: 50px (pill), font-weight: 700 |
| **Max Width** | 1200px centered |
| **섹션 패딩** | 80-100px vertical |

## 완성된 기능 / 섹션

### 1. Sticky Header
- 투명 배경 → 스크롤 시 흰색 + 그림자
- 좌측 그린 로고 `TOKBELL` / 중앙 네비게이션 / 우측 그린 `회원가입` 버튼
- 모바일: 햄버거 메뉴 (3 line → X 애니메이션 + 풀스크린 오버레이)
- 스크롤 시 현재 섹션 활성 네비 하이라이트

### 2. Hero Section
- 2컬럼 (55% 텍스트 / 45% 폰 목업)
- 오렌지 뱃지 "최저 8.3원부터"
- 대형 헤드라인 + 서브텍스트
- 2x2 서비스 미니카드 (일반문자, RCS, 팩스, 알림톡)
- 그린 CTA 버튼 (pulse 애니메이션)
- CSS로 그린 스마트폰 목업 (채팅 UI + float 애니메이션)

### 3. Benefits Section (#F5F5F5)
- 4개 원형 아이콘 + 카운트업 애니메이션
- 10% 할인, 스타벅스 쿠폰, 3,000원, +2개월

### 4. Trust & Features Section
- 신뢰 헤드라인 + 신규 사업 서브카피 + 3개 pill 버튼 (호버 효과)
- 무한 마키 로고 바 (8개 공공기관 로고, CSS @keyframes)
- 마스크 그라디언트로 좌우 페이드아웃

### 5. App Showcase (다크 #1E1E2E)
- 중앙 텍스트 + Google Play / App Store 뱃지
- 4개 스마트폰 팬 배치 (rotate -12° ~ +12°, perspective)
- 각 폰: 전송결과, 메시지작성, 주소록, 충전하기 UI
- 그린 glow 배경 효과

### 6. Pricing Section
- 4컬럼 요금 카드 (SMS 8.3원 / LMS 26.5원 / MMS 59원 / 알림톡 6.2원)
- 인기 카드 리본 뱃지 + 그린 보더
- 카운트업 애니메이션 (소수점 지원)
- 다이내믹 프라이싱 / 스마트 볼륨 관리 부가 카드

### 7. Events Section (#F5F5F5)
- 3개 이벤트 카드 (그라디언트 이미지 + 텍스트)
- 호버 시 상승 + 그림자 확대
- "더 많은 실속가를 보러가기" 아웃라인 버튼

### 8. Footer (#2D2D2D)
- 고객센터 전화번호 크게 표시
- 회사 정보 + 약관 링크

## 애니메이션 & 인터랙션
| 효과 | 설명 |
|------|------|
| Scroll Fade-in-up | 모든 섹션 자식 요소, opacity 0→1, translateY 30→0, 150ms stagger |
| Hero Phone Float | translateY 0 ↔ -12px, 3s ease-in-out infinite |
| CTA Pulse | scale 1→1.04→1, 4s cycle |
| Benefits Counter | 0→목표값, 1.5s, easeOutCubic |
| Pricing Counter | 0→소수점 목표, 1.2s, easeOutCubic |
| Logo Marquee | CSS @keyframes 무한 수평 스크롤, 40s linear |
| Header Transition | 스크롤 80px 이후 흰색 배경 + 그림자 |
| Phone Fan Hover | rotate→0, translateY -12px, scale 1.04 |
| Card Hover | translateY -4~8px + shadow 확대 |
| Nav Underline | ::after width 0→100% on hover |
| Reduced Motion | `prefers-reduced-motion` 미디어 쿼리로 모든 애니메이션 비활성화 |

## 파일 구조
```
index.html          → 메인 랜딩 페이지
css/
  └── style.css     → 전체 스타일 (CSS Custom Properties 기반)
js/
  └── main.js       → 모든 인터랙션 (Vanilla JS)
```

## 접속 경로
| 페이지 | 경로 |
|--------|------|
| 메인 랜딩 | `index.html` |

## 반응형 지원
- **Desktop**: 1200px+
- **Tablet**: 768px ~ 1024px (2x2 그리드, 햄버거 메뉴)
- **Mobile**: 480px ~ 768px (1컬럼, 축소 폰팬)
- **Small Mobile**: ~480px

## 기술 스택
- HTML5 시맨틱 태그 (header, nav, main, section, footer)
- CSS3 Custom Properties + CSS Grid + Flexbox
- Vanilla JavaScript (no frameworks)
- Google Fonts (Noto Sans KR)
- Intersection Observer API (스크롤 애니메이션)
- CSS @keyframes (마키, float, pulse)
- `prefers-reduced-motion` 접근성 지원

## 미구현 / 향후 개발 추천
- [ ] 서브 페이지 (회원가입, 견적문의 등)
- [ ] 공공기관 로고 실제 이미지로 교체
- [ ] 백엔드 문의 폼 연동
- [ ] 다크모드 토글
- [ ] SEO 메타태그 및 OG 이미지 최적화
- [ ] GA4 또는 GTM 이벤트 트래킹
