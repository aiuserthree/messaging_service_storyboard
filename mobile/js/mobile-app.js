/**
 * Render a standard page header bar with hamburger (left) and profile icon (right).
 * @param {string} title - Page title
 * @param {string} [subtitle] - Optional subtitle
 * @param {string} [backHref] - If set, shows a back arrow; null means no back button
 * @param {boolean} [loggedIn=true] - Show profile icon (true) or login button (false)
 */
function renderPageHeader(title, subtitle, backHref, loggedIn) {
    if (loggedIn === undefined) loggedIn = true;
    const back = backHref
        ? `<a href="${backHref}" class="back-btn" aria-label="뒤로">
               <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
           </a>` : '';
    const rightBtn = loggedIn
        ? `<a href="mypage-mobile.html" class="icon-btn profile-btn" aria-label="프로필">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="22" height="22"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg>
           </a>`
        : `<a href="login-mobile.html" class="icon-btn profile-btn" aria-label="로그인">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="22" height="22"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
           </a>`;
    const sub = subtitle ? `<div class="subtitle">${subtitle}</div>` : '';
    return `<header class="page-header-bar">
        <div class="inner">
            <button class="icon-btn menu-btn" id="menuBtn" aria-label="메뉴">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" width="22" height="22"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
            </button>
            ${back}
            <div class="title-wrap">
                <div class="title">${title}</div>
                ${sub}
            </div>
            ${rightBtn}
        </div>
    </header>`;
}

function initMobileDrawer() {
    const menuBtn = document.getElementById('menuBtn');
    const drawer = document.getElementById('drawer');
    const backdrop = document.getElementById('backdrop');
    if (!menuBtn || !drawer || !backdrop) return;

    menuBtn.addEventListener('click', () => {
        drawer.classList.add('open');
        backdrop.classList.add('open');
    });
    backdrop.addEventListener('click', () => {
        drawer.classList.remove('open');
        backdrop.classList.remove('open');
    });
}

function renderTabBar(active) {
    const tabs = [
        { id: 'home', href: 'main-mobile.html', label: '홈', icon: '<path d="M3 12l9-9 9 9M5 10v10h14V10"/>' },
        { id: 'send-result', href: 'send-result-mobile.html', label: '발송내역', icon: '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>' },
        { id: 'send', href: 'message-send-mobile.html', label: '발송', fab: true, icon: '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>' },
        { id: 'addressbook', href: 'addressbook-mobile.html', label: '주소록', icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>' },
        { id: 'mypage', href: 'mypage-mobile.html', label: '마이', icon: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/>' }
    ];

    return tabs.map(tab => {
        const isActive = tab.id === active;
        if (tab.fab) {
            return `<a href="${tab.href}" class="tab-item send-fab${isActive ? ' active' : ''}">
                <span class="fab-circle"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor">${tab.icon}</svg></span>
                <span>${tab.label}</span>
            </a>`;
        }
        return `<a href="${tab.href}" class="tab-item${isActive ? ' active' : ''}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">${tab.icon}</svg>
            <span>${tab.label}</span>
        </a>`;
    }).join('');
}

function renderDrawer() {
    return `
        <div class="drawer-backdrop" id="backdrop"></div>
        <aside class="drawer" id="drawer">
            <div class="drawer-header">
                <img src="../img/logo/tokbell_logo_drawer_white.png" alt="tokbell" class="brand-logo" width="120" height="26">
                <div class="name">조준형님</div>
                <div class="email">junhyeong@tokbell.com</div>
                <span class="grade">개인회원 · 일반 등급</span>
            </div>
            <div class="drawer-menu">
                <div class="menu-section">메시지 발송</div>
                <a href="message-send-mobile.html">일반문자</a>
                <a href="message-send-mobile.html">광고문자</a>
                <a href="#">선거문자</a>
                <a href="#">알림톡</a>
                <a href="#">브랜드 메시지</a>
                <div class="menu-section">관리</div>
                <a href="addressbook-mobile.html">주소록 관리</a>
                <a href="send-result-mobile.html">발송 내역</a>
                <a href="mypage-mobile.html">발신번호 관리</a>
                <a href="template-message-mobile.html">템플릿 관리</a>
                <div class="menu-section">결제 / 마이</div>
                <a href="payment-mobile.html">충전하기</a>
                <a href="payment-history-mobile.html">결제 내역</a>
                <a href="mypage-mobile.html">내 정보</a>
                <a href="mypage-mobile.html">설정</a>
                <div class="menu-section">고객지원</div>
                <a href="support-center-mobile.html">통합 고객센터</a>
                <a href="support-notice-mobile.html">공지사항</a>
                <a href="support-faq-mobile.html">FAQ</a>
                <a href="support-event-mobile.html">이벤트</a>
                <a href="support-inquiry-mobile.html">1:1 문의</a>
                <a href="payment-refund-mobile.html">환불신청</a>
            </div>
            <div class="drawer-footer">
                <a href="index-mobile.html">로그아웃</a>
            </div>
        </aside>`;
}

function initTabPills(container) {
    if (!container) return;
    container.querySelectorAll('.tab-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            container.querySelectorAll('.tab-pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const target = pill.dataset.panel;
            if (target) {
                document.querySelectorAll('[data-tab-panel]').forEach(panel => {
                    panel.style.display = panel.dataset.tabPanel === target ? 'block' : 'none';
                });
            }
        });
    });
}

function initChipFilter(container, onChange) {
    if (!container) return;
    container.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            container.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            if (onChange) onChange(chip.dataset.value);
        });
    });
}

function renderSupportTabs(active) {
    const tabs = [
        { id: 'notice', href: 'support-notice-mobile.html', label: '공지사항' },
        { id: 'faq', href: 'support-faq-mobile.html', label: 'FAQ' },
        { id: 'inquiry', href: 'support-inquiry-mobile.html', label: '1:1 문의' },
        { id: 'event', href: 'support-event-mobile.html', label: '이벤트' }
    ];
    return tabs.map(t =>
        `<a href="${t.href}" class="support-tab${t.id === active ? ' active' : ''}">${t.label}</a>`
    ).join('');
}

function initFaqAccordion() {
    document.querySelectorAll('.faq-q').forEach(btn => {
        btn.addEventListener('click', () => btn.closest('.faq-item').classList.toggle('open'));
    });
}

function initInquiryHistory() {
    document.querySelectorAll('.inquiry-history-head').forEach(head => {
        head.addEventListener('click', () => head.closest('.inquiry-history-item').classList.toggle('open'));
    });
}

function initCategoryFilter(container, itemSelector) {
    if (!container) return;
    container.querySelectorAll('.chip, .category-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            container.querySelectorAll('.chip, .category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cat = btn.dataset.category || btn.dataset.value;
            document.querySelectorAll(itemSelector).forEach(item => {
                if (!cat || cat === 'all') item.style.display = '';
                else item.style.display = item.dataset.category === cat ? '' : 'none';
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initMobileDrawer();
});
