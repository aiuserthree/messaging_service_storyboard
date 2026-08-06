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

/* ===================================================================
 * 알림톡 인증 (모바일 공용 바텀시트)
 *
 * 등록된 휴대폰 번호로 카카오톡 알림톡 인증번호를 발송하는 인증 시트.
 * 로그인 2차 인증과 발송 전 추가 인증에서 함께 사용한다.
 * 카카오톡 미사용·수신 불가 시 문자(SMS)로 대체 발송한다.
 *
 * 사용법:
 *   openAlimtalkAuth({
 *       title: '2차 인증',
 *       description: '보안을 위해 등록된 휴대폰 번호로 카카오톡 알림톡을 보내드립니다.',
 *       confirmText: '인증하기',
 *       onSuccess: (result) => { ... }   // result: { phone, channel }
 *   });
 *
 * 프로토타입 한계: 실제 발송·대조 없이 형식 검증만 수행한다.
 * =================================================================== */
const ATK_TIMER_SECONDS = 180;
const ATK_DEMO_CODE = '123456';   // 프로토타입: 이 값만 인증 성공, 그 외 6자리는 오답 처리
const ATK_MAX_ATTEMPTS = 5;       // 초과 시 잠금 → 재전송해야 재시도 가능

const atkState = {
    timerInterval: null,
    seconds: ATK_TIMER_SECONDS,
    mode: 'phone',       // 'phone'(알림톡·SMS) | 'email'(이메일 OTP)
    channel: 'alimtalk', // 'alimtalk' | 'sms' | 'email'
    phone: '',
    email: '',
    attempts: 0,
    expired: false,
    locked: false,
    onSuccess: null,
    mounted: false
};

function atkEl(id) { return document.getElementById(id); }

function atkSanitizePhone(value) {
    return String(value || '').replace(/\D/g, '').slice(0, 11);
}

/* 등록된 번호는 마스킹해 노출한다 (010-****-5678) */
function atkMaskPhone(digits) {
    if (!digits) return '-';
    if (digits.length < 7) return digits;
    return digits.slice(0, 3) + '-****-' + digits.slice(-4);
}

function atkShowError(id, show) {
    const el = atkEl(id);
    if (el) el.classList.toggle('show', !!show);
}

/* 인증번호 오류 문구를 상황별로 교체해 노출한다. */
function atkSetCodeError(message) {
    const el = atkEl('atkCodeError');
    if (!el) return;
    el.textContent = message;
    el.classList.add('show');
}

/* 시도 횟수 초과 · 유효시간 만료 → 재전송 전까지 인증 차단 */
function atkLockCode(message) {
    atkState.locked = true;
    atkSetCodeError(message);
    atkEl('atkCode').disabled = true;
    atkEl('atkVerifyBtn').disabled = true;
    clearInterval(atkState.timerInterval);
    atkState.timerInterval = null;
    atkEl('atkTimer').textContent = '00:00';  // 잠긴 인증번호는 만료 처리
    atkEl('atkResendBtn').disabled = false;
}

function atkUnlockCode() {
    atkState.locked = false;
    atkState.expired = false;
    atkEl('atkCode').disabled = false;
    atkEl('atkVerifyBtn').disabled = false;
}

function renderAlimtalkAuthSheet() {
    if (atkEl('atkSheet')) return;
    const wrap = document.createElement('div');
    wrap.innerHTML = `
        <div class="atk-backdrop" id="atkBackdrop"></div>
        <div class="atk-sheet" id="atkSheet" role="dialog" aria-modal="true" aria-labelledby="atkTitle">
            <div class="atk-grabber"></div>

            <div id="atkStep1">
                <div class="atk-title" id="atkTitle">알림톡 인증</div>
                <div class="atk-channel" id="atkChannelBox">
                    <span class="atk-badge" id="atkChannelBadge">
                        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.9 3 2.8 6.3 2.8 10.3c0 2.6 1.7 4.9 4.3 6.2-.2.7-.7 2.5-.8 2.9 0 .2.1.4.3.3.3-.1 2.6-1.7 3.6-2.4.6.1 1.2.1 1.8.1 5.1 0 9.2-3.3 9.2-7.3S17.1 3 12 3z"/></svg>
                        알림톡
                    </span>
                    <span id="atkDesc"></span>
                </div>
                <p class="atk-desc" id="atkChannelNote">카카오톡 미사용 또는 수신 불가 시<br>문자(SMS)로 자동 대체 발송됩니다.</p>
                <div class="atk-link-box">
                    <div class="atk-link-row" id="atkCallerRow">
                        <span class="atk-link-label">발신번호</span>
                        <span class="atk-link-value" id="atkCallerValue">-</span>
                    </div>
                    <div class="atk-link-row">
                        <span class="atk-link-label" id="atkTargetLabel">인증받을 번호</span>
                        <span class="atk-link-value is-strong" id="atkPhoneMasked">-</span>
                    </div>
                </div>
                <p class="form-help" id="atkLinkHelp"></p>
                <div class="atk-error" id="atkPhoneError">등록된 인증 번호가 없습니다. 마이페이지에서 인증 수단을 먼저 등록해 주세요.</div>
                <div class="atk-actions">
                    <button type="button" class="btn btn-primary btn-block" id="atkSendBtn">인증 번호 보내기</button>
                    <button type="button" class="btn btn-outline btn-block" id="atkCancelBtn">취소</button>
                </div>
                <p class="atk-help">인증 과정에 어려움이 있나요? <a href="support-inquiry-mobile.html">1:1 문의하기</a></p>
            </div>

            <div id="atkStep2" style="display:none;">
                <div class="atk-title" id="atkTitle2">알림톡 인증</div>
                <p class="atk-desc"><strong id="atkPhoneDisplay">010-0000-0000</strong>로 발송된<br><strong id="atkChannelLabel">알림톡</strong>의 인증번호 6자리를 입력해주세요.</p>
                <div class="form-group">
                    <label class="form-label required" for="atkCode">인증번호</label>
                    <div class="atk-code-row">
                        <input type="tel" inputmode="numeric" autocomplete="one-time-code" class="form-input"
                               id="atkCode" placeholder="인증번호 6자리" maxlength="6">
                        <span class="atk-timer" id="atkTimer">03:00</span>
                    </div>
                    <div class="atk-error" id="atkCodeError">인증번호 6자리를 입력해주세요.</div>
                    <div class="form-help">인증번호 유효시간 3분</div>
                </div>
                <div class="atk-resend-wrap">
                    <button type="button" class="atk-resend-btn" id="atkResendBtn" disabled>인증번호 재전송</button>
                </div>
                <div class="atk-fallback" id="atkFallback"></div>
                <div class="atk-actions">
                    <button type="button" class="btn btn-primary btn-block" id="atkVerifyBtn">인증하기</button>
                    <button type="button" class="btn btn-outline btn-block" id="atkBackBtn">취소</button>
                </div>
                <p class="atk-help">인증 과정에 어려움이 있나요? <a href="support-inquiry-mobile.html">1:1 문의하기</a></p>
            </div>
        </div>
    `;
    while (wrap.firstElementChild) document.body.appendChild(wrap.firstElementChild);
    initAlimtalkAuth();
}

function atkApplyChannel() {
    const fallback0 = atkEl('atkFallback');

    // 이메일 OTP 모드에는 문자(SMS) 대체 발송이 없다.
    if (atkState.mode === 'email') {
        atkEl('atkChannelLabel').textContent = '이메일';
        fallback0.classList.remove('used');
        fallback0.innerHTML = '';
        fallback0.style.display = 'none';
        return;
    }
    fallback0.style.display = '';

    const isSms = atkState.channel === 'sms';
    atkEl('atkChannelLabel').textContent = isSms ? '문자(SMS)' : '알림톡';
    const fallback = atkEl('atkFallback');
    fallback.classList.toggle('used', isSms);
    fallback.innerHTML = isSms
        ? '문자(SMS)로 인증번호를 다시 보냈습니다.'
        : '카카오톡으로 받지 못하셨나요? <button type="button" class="atk-link-btn" id="atkSmsBtn">문자(SMS)로 받기</button>';
    const btn = atkEl('atkSmsBtn');
    if (btn) btn.addEventListener('click', atkSmsFallback);
}

/* 재전송 — 새 인증번호가 발송되므로 이전 입력·오류·시도횟수를 모두 비운다. */
function atkHandleResend() {
    atkEl('atkCode').value = '';
    atkShowError('atkCodeError', false);
    atkStartTimer();
    atkEl('atkCode').focus();
}

function atkSmsFallback() {
    atkState.channel = 'sms';
    atkApplyChannel();
    atkEl('atkCode').value = '';
    atkShowError('atkCodeError', false);
    atkStartTimer();
    atkEl('atkCode').focus();
}

function atkStartTimer() {
    clearInterval(atkState.timerInterval);
    atkState.seconds = ATK_TIMER_SECONDS;
    atkState.attempts = 0;
    atkUnlockCode();
    const timerEl = atkEl('atkTimer');
    const resendBtn = atkEl('atkResendBtn');
    resendBtn.disabled = true;

    const tick = () => {
        const min = Math.floor(atkState.seconds / 60);
        const sec = atkState.seconds % 60;
        timerEl.textContent = ('0' + min).slice(-2) + ':' + ('0' + sec).slice(-2);
        if (atkState.seconds <= 0) {
            clearInterval(atkState.timerInterval);
            atkState.timerInterval = null;
            timerEl.textContent = '00:00';
            atkState.expired = true;
            // 유효시간 만료 → 재전송 전까지 인증 불가
            atkLockCode('인증번호 유효시간이 만료되었습니다. 인증번호를 재전송해 주세요.');
            return;
        }
        atkState.seconds--;
    };

    tick();
    atkState.timerInterval = setInterval(tick, 1000);
}

function atkReset() {
    clearInterval(atkState.timerInterval);
    atkState.timerInterval = null;
    atkState.mode = 'phone';
    atkState.channel = 'alimtalk';
    atkState.attempts = 0;
    atkRestorePhoneLabels();
    atkUnlockCode();
    atkEl('atkStep1').style.display = '';
    atkEl('atkStep2').style.display = 'none';
    atkEl('atkCode').value = '';
    atkShowError('atkPhoneError', false);
    atkShowError('atkCodeError', false);
    atkApplyChannel();
}

function atkShowStep2(target) {
    atkEl('atkStep1').style.display = 'none';
    atkEl('atkStep2').style.display = '';
    // 2단계도 동일하게 마스킹해 노출한다
    atkEl('atkPhoneDisplay').textContent = atkState.mode === 'email' ? atkMaskEmail(target) : atkMaskPhone(target);
    atkEl('atkCode').value = '';
    atkShowError('atkCodeError', false);
    atkStartTimer();
    setTimeout(() => atkEl('atkCode').focus(), 100);
}

function atkHandleSend() {
    // 사용자가 번호·이메일을 입력하지 않는다. 계정에 등록·확인된 값으로만 발송한다.
    const target = atkState.mode === 'email' ? atkState.email : atkState.phone;
    if (!target) {
        atkShowError('atkPhoneError', true);
        return;
    }
    atkShowError('atkPhoneError', false);
    atkShowStep2(target);
}

/* 등록된 이메일도 마스킹해 노출한다 (ad****@ibank.co.kr) */
function atkMaskEmail(value) {
    const s = String(value || '');
    const at = s.indexOf('@');
    if (at < 1) return s || '-';
    const local = s.slice(0, at);
    const head = local.slice(0, Math.min(2, local.length));
    return head + '*'.repeat(Math.max(4, local.length - head.length)) + s.slice(at);
}

/* 이메일 OTP 모드로 바뀐 라벨·안내를 기본(알림톡) 상태로 되돌린다. */
function atkRestorePhoneLabels() {
    const cbox0 = atkEl('atkChannelBox');
    if (cbox0) cbox0.classList.remove('is-email');
    const badge = atkEl('atkChannelBadge');
    if (badge) {
        badge.className = 'atk-badge';
        badge.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.9 3 2.8 6.3 2.8 10.3c0 2.6 1.7 4.9 4.3 6.2-.2.7-.7 2.5-.8 2.9 0 .2.1.4.3.3.3-.1 2.6-1.7 3.6-2.4.6.1 1.2.1 1.8.1 5.1 0 9.2-3.3 9.2-7.3S17.1 3 12 3z"/></svg> 알림톡';
    }
    const note = atkEl('atkChannelNote');
    if (note) note.innerHTML = '카카오톡 미사용 또는 수신 불가 시<br>문자(SMS)로 자동 대체 발송됩니다.';
    const label = atkEl('atkTargetLabel');
    if (label) label.textContent = '인증받을 번호';
    const err = atkEl('atkPhoneError');
    if (err) err.textContent = '등록된 인증 번호가 없습니다. 마이페이지에서 인증 수단을 먼저 등록해 주세요.';
    const sendBtn = atkEl('atkSendBtn');
    if (sendBtn) sendBtn.textContent = '인증 번호 보내기';
}

function atkHandleVerify() {
    if (atkState.locked) return;

    const input = atkEl('atkCode');
    const code = input.value.replace(/\D/g, '');
    input.value = code;

    // 미입력 · 자릿수 부족
    if (code.length !== 6) {
        atkSetCodeError('인증번호 6자리를 입력해주세요.');
        return;
    }

    // 유효시간 만료
    if (atkState.expired) {
        atkLockCode('인증번호 유효시간이 만료되었습니다. 인증번호를 재전송해 주세요.');
        return;
    }

    // 인증번호 불일치
    if (code !== ATK_DEMO_CODE) {
        atkState.attempts++;
        if (atkState.attempts >= ATK_MAX_ATTEMPTS) {
            atkLockCode(`인증 시도 횟수(${ATK_MAX_ATTEMPTS}회)를 초과했습니다. 인증번호를 재전송해 주세요.`);
        } else {
            atkSetCodeError(`인증번호가 일치하지 않습니다. (${atkState.attempts}/${ATK_MAX_ATTEMPTS}회)`);
            input.focus();
            input.select();
        }
        return;
    }

    const result = { phone: atkState.phone, channel: atkState.channel };
    const cb = atkState.onSuccess;
    closeAlimtalkAuth();
    if (typeof cb === 'function') cb(result);
}

function closeAlimtalkAuth() {
    atkEl('atkBackdrop').classList.remove('open');
    atkEl('atkSheet').classList.remove('open');
    atkReset();
    atkState.onSuccess = null;
}

function initAlimtalkAuth() {
    if (atkState.mounted) return;
    atkState.mounted = true;

    atkEl('atkCode').addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, '').slice(0, 6);
        atkShowError('atkCodeError', false);
    });
    atkEl('atkCode').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') { e.preventDefault(); atkHandleVerify(); }
    });

    atkEl('atkSendBtn').addEventListener('click', atkHandleSend);
    atkEl('atkVerifyBtn').addEventListener('click', atkHandleVerify);
    atkEl('atkCancelBtn').addEventListener('click', closeAlimtalkAuth);
    atkEl('atkBackBtn').addEventListener('click', closeAlimtalkAuth);
    atkEl('atkBackdrop').addEventListener('click', closeAlimtalkAuth);
    atkEl('atkResendBtn').addEventListener('click', function () {
        if (this.disabled) return;
        atkHandleResend();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && atkEl('atkSheet').classList.contains('open')) closeAlimtalkAuth();
    });
}

/* ===================================================================
 * 발송 추가 인증 세션 (보안심사 3.5-⑤ 재인증 기준) — PC 와 동일 기준
 *   최초 / 30분 경과 / 발신번호 변경 / 대량발송 / 접속환경 변경 시 재인증
 * =================================================================== */
const SEND_AUTH_VALID_MINUTES = 30;
const BULK_SEND_THRESHOLD = 1000;
const ATK_SESSION_KEYS = { at: 'sendAuthAt', caller: 'sendAuthCaller', env: 'sendAuthEnv' };

function atkEnvFingerprint() {
    return String(navigator.userAgent || '').slice(0, 120);
}

function getSendAuthState(ctx = {}) {
    const count = Number(ctx.recipientCount || 0);
    const caller = String(ctx.callerNumber || '');

    if (count >= BULK_SEND_THRESHOLD) {
        return { required: true, code: 'bulk',
                 reason: `대량발송(${BULK_SEND_THRESHOLD.toLocaleString()}건 이상)은 매번 인증이 필요합니다.` };
    }
    const at = Number(sessionStorage.getItem(ATK_SESSION_KEYS.at) || 0);
    if (!at) return { required: true, code: 'none', reason: '' };

    const elapsedMin = (Date.now() - at) / 60000;
    if (elapsedMin >= SEND_AUTH_VALID_MINUTES) {
        return { required: true, code: 'expired',
                 reason: `인증 유효시간(${SEND_AUTH_VALID_MINUTES}분)이 지나 다시 인증이 필요합니다.` };
    }
    if (sessionStorage.getItem(ATK_SESSION_KEYS.caller) !== caller) {
        return { required: true, code: 'caller-changed', reason: '발신번호가 변경되어 다시 인증이 필요합니다.' };
    }
    if (sessionStorage.getItem(ATK_SESSION_KEYS.env) !== atkEnvFingerprint()) {
        return { required: true, code: 'env-changed', reason: '접속환경이 변경되어 다시 인증이 필요합니다.' };
    }
    return { required: false, code: 'valid', remainMin: Math.max(1, Math.ceil(SEND_AUTH_VALID_MINUTES - elapsedMin)) };
}

window.SEND_AUTH_VALID_MINUTES = SEND_AUTH_VALID_MINUTES;
window.BULK_SEND_THRESHOLD = BULK_SEND_THRESHOLD;

function markSendAuthenticated(ctx = {}) {
    sessionStorage.setItem(ATK_SESSION_KEYS.at, String(Date.now()));
    sessionStorage.setItem(ATK_SESSION_KEYS.caller, String(ctx.callerNumber || ''));
    sessionStorage.setItem(ATK_SESSION_KEYS.env, atkEnvFingerprint());
}

function openAlimtalkAuth(options = {}) {
    renderAlimtalkAuthSheet();
    atkReset();

    const title = options.title || '알림톡 인증';
    atkEl('atkTitle').textContent = title;
    atkEl('atkTitle2').textContent = title;
    atkEl('atkDesc').innerHTML = options.description
        || '보안을 위해 등록된 휴대폰 번호로 카카오톡 알림톡을 보내드립니다.';
    atkEl('atkVerifyBtn').textContent = options.confirmText || '인증하기';

    /* 인증 대상은 호출부가 주입한 '등록·확인된 번호'로 고정 (보안심사 3.4-②·3.5-①②) */
    atkState.phone = atkSanitizePhone(options.phone || '');
    atkEl('atkPhoneMasked').textContent = atkState.phone ? atkMaskPhone(atkState.phone) : '미등록';

    const callerRow = atkEl('atkCallerRow');
    if (options.callerNumber) {
        callerRow.style.display = '';
        atkEl('atkCallerValue').textContent = options.callerNumber;
        atkEl('atkLinkHelp').innerHTML = '발신번호 등록 시 본인확인한 번호입니다.<br>번호 변경은 마이페이지 &gt; 발신번호 관리에서 가능합니다.';
    } else {
        callerRow.style.display = 'none';
        atkEl('atkLinkHelp').innerHTML = '회원가입 시 본인확인한 번호입니다.<br>번호 변경은 마이페이지 &gt; 2차 인증 설정에서 가능합니다.';
    }
    atkEl('atkSendBtn').disabled = !atkState.phone;
    atkShowError('atkPhoneError', !atkState.phone);

    atkState.onSuccess = options.onSuccess || null;

    atkEl('atkBackdrop').classList.add('open');
    atkEl('atkSheet').classList.add('open');
}

/* ===================================================================
 * 이메일 OTP 인증 (모바일 · 보안심사 3.5-④ 기업관리자 사후승인)
 *
 * 심사 항목해설상 사후승인은 전자결재·관리자 콘솔 승인·이메일 승인·
 * 서면 결재 등 "승인(확인) 사실을 입증할 수 있는 방식"이면 된다.
 * 톡벨은 이메일 승인을 채택해 기업 고객사 승인 담당자 이메일로 6자리
 * 인증번호를 보내고, 이를 입력해야 발송되도록 한다.
 *
 * 인증 대상 이메일은 사용자가 직접 입력하지 않고 등록·확인된 값으로 고정.
 * 실제 연동 시 POST /api/send-approval/otp/send · /verify 로 대체한다.
 * =================================================================== */
function openEmailOtpAuth(options = {}) {
    renderAlimtalkAuthSheet();
    atkReset();

    atkState.mode = 'email';
    atkState.channel = 'email';
    atkState.email = String(options.email || '').trim();
    atkState.phone = '';

    const title = options.title || '발송 승인 인증';
    atkEl('atkTitle').textContent = title;
    atkEl('atkTitle2').textContent = title;
    atkEl('atkDesc').innerHTML = options.description
        || '발송 승인을 위해 등록된 담당자 이메일로 인증번호를 보내드립니다.';
    atkEl('atkVerifyBtn').textContent = options.confirmText || '인증하고 발송하기';

    const cbox = atkEl('atkChannelBox');
    if (cbox) cbox.classList.add('is-email');
    const badge = atkEl('atkChannelBadge');
    if (badge) {
        badge.className = 'atk-badge atk-badge-mail';
        badge.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 4.8-8-4.8V6l8 4.8L20 6z"/></svg> 이메일';
    }
    const note = atkEl('atkChannelNote');
    if (note) note.innerHTML = options.channelNote || '기업 고객사 승인 담당자 이메일로<br>6자리 인증번호가 발송됩니다.';

    const callerRow = atkEl('atkCallerRow');
    if (options.callerNumber) {
        callerRow.style.display = '';
        atkEl('atkCallerValue').textContent = options.callerNumber;
    } else {
        callerRow.style.display = 'none';
    }

    atkEl('atkTargetLabel').textContent = '승인 담당자';
    atkEl('atkPhoneMasked').textContent = atkState.email ? atkMaskEmail(atkState.email) : '미등록';
    atkEl('atkLinkHelp').innerHTML = options.linkHelp
        || '기업 고객사에 등록·확인된 승인 담당자 이메일입니다.<br>변경은 마이페이지 &gt; 2차 인증 설정에서 가능합니다.';

    atkEl('atkPhoneError').textContent = '등록된 승인 담당자 이메일이 없습니다. 마이페이지에서 먼저 등록해 주세요.';
    atkEl('atkSendBtn').disabled = !atkState.email;
    atkEl('atkSendBtn').textContent = '인증번호 받기';
    atkShowError('atkPhoneError', !atkState.email);

    atkState.onSuccess = options.onSuccess || null;

    atkApplyChannel();
    atkEl('atkBackdrop').classList.add('open');
    atkEl('atkSheet').classList.add('open');
}


document.addEventListener('DOMContentLoaded', () => {
    initMobileDrawer();
});
