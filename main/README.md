# 톡벨 (TokBell) — AI 기반 비즈니스 메시징 플랫폼

## 프로젝트 개요
톡벨 비즈니스 메시징 플랫폼의 메인 웹사이트입니다.  
**Enhans.ai** 디자인 스타일을 참고하여 "화이트 & 클린" 미니멀 엔터프라이즈 컨셉으로 제작되었습니다.

## 디자인 컨셉
- **테마**: White & Clean 미니멀리즘
- **컬러 팔레트**: `#FFFFFF` (배경), `#F5F5F7` (섹션 구분), `#111111` (텍스트), `#6B7B8D` (포인트)
- **타이포그래피**: Inter (Google Fonts)
- **모서리**: 직각에 가까운 날카로운 모서리 (border-radius: 2px)
- **여백**: 화면의 50% 이상 흰색 여백 활용
- **이미지 톤**: 채도 낮은 Cool Tone 실사 이미지

## 완성된 기능

### 메인 페이지 (index.html)
1. **상단 알림바** — 회색 배경 공지사항 (파트너십 선정 소식)
2. **네비게이션** — 좌측 로고 / 중앙 메뉴 / 우측 Contact 아웃라인 버튼 + Sticky 헤더
3. **히어로 섹션** — 텍스트 중심 대형 헤드라인 + 풀와이드 대시보드 이미지
4. **Trust Strip** — 글로벌 기업 로고 (SAMSUNG, amazon, P&G 등)
5. **기능 소개 섹션** — 비대칭 그리드 (텍스트 5:이미지 6) 3개 Feature Row
   - AI 기반 타겟팅 전송
   - 대량 메시지 자동화
   - 실시간 성과 분석 (라이브 차트 카드)
6. **솔루션 섹션** — 텍스트 + 메시징 UI 목업 카드
7. **요금 섹션** — 4개 요금 카드 (SMS/LMS/MMS/알림톡) + 2개 특징 카드
8. **CTA 섹션** — 다크 배경 전환 유도 영역
9. **푸터** — 서비스/솔루션/회사/지원 4컬럼 링크

### 인터랙션
- Intersection Observer 기반 스크롤 애니메이션 (fade-in + slide-up)
- 요금 숫자 카운터 애니메이션
- 분석 차트 바 애니메이션
- 모바일 햄버거 메뉴 토글
- Smooth 앵커 스크롤

## 파일 구조
```
index.html                 → 메인 페이지
css/
  └── style.css            → 전체 스타일시트
js/
  └── main.js              → 인터랙션 및 애니메이션
images/
  ├── hero-dashboard.jpg   → 히어로 대시보드 이미지
  ├── feature-collaboration.jpg → 기능1 이미지
  └── feature-mobile.jpg   → 기능2 이미지
```

## 접속 경로
| 페이지 | 경로 |
|--------|------|
| 메인 | `index.html` |

## 반응형 지원
- **Desktop**: 1280px+
- **Tablet**: 768px ~ 1024px
- **Mobile**: 480px ~ 768px
- **Small Mobile**: ~480px

## 사용 기술
- HTML5 / CSS3 / Vanilla JavaScript
- Google Fonts (Inter)
- Intersection Observer API
- CSS Backdrop Filter

## 미구현 / 향후 개발 추천
- [ ] 서브 페이지 (signup.html, quote-inquiry.html 등)
- [ ] 실제 로고 이미지 교체 (텍스트 → SVG 로고)
- [ ] 다크모드 토글
- [ ] 다국어 지원 (KO/EN)
- [ ] 문의 폼 기능 (Contact 섹션)
- [ ] 블로그/뉴스룸 페이지
- [ ] SEO 메타태그 및 OG 이미지 최적화
