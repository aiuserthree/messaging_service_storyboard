/**
 * 알림톡 인증 (PC 공용)
 *
 * 등록된 휴대폰 번호로 카카오톡 알림톡 인증번호를 발송하는 인증 모달.
 * 로그인 2차 인증과 발송 전 추가 인증에서 함께 사용한다.
 * 카카오톡 미사용·수신 불가 시 문자(SMS)로 대체 발송한다.
 *
 * 사용법:
 *   openAlimtalkAuth({
 *       title: '2차 인증',
 *       description: '보안을 위해 등록된 휴대폰 번호로 카카오톡 알림톡을 보내드립니다.',
 *       confirmText: '인증하기',
 *       phone: '01098725784',          // 계정·발신번호에 등록·확인된 번호 (필수)
 *       callerNumber: '010-1234-5678', // 발송 인증 시 선택한 발신번호 (선택)
 *       onSuccess: function (result) { ... },  // result: { phone, channel }
 *       onCancel: function () { ... }
 *   });
 *
 * 보안심사 3.4-②·3.5-①② 대응: 사용자가 번호를 직접 입력하지 않는다.
 * 호출부가 주입한 등록·확인된 번호로만 발송하며 화면에는 마스킹해 노출한다.
 *
 * 프로토타입 한계: 실제 발송·대조 없이 인증번호 123456 만 성공 처리한다.
 */
(function () {
    'use strict';

    var TIMER_SECONDS = 180;
    var LOGO_SRC = 'img/logo/tokbell_logo_o.png';
    var DEMO_CODE = '123456';   // 프로토타입: 이 값만 인증 성공, 그 외 6자리는 오답 처리
    var MAX_ATTEMPTS = 5;       // 초과 시 잠금 → 재전송해야 재시도 가능

    var state = {
        timerInterval: null,
        seconds: TIMER_SECONDS,
        mode: 'phone',       // 'phone'(알림톡·SMS) | 'email'(이메일 OTP)
        channel: 'alimtalk', // 'alimtalk' | 'sms' | 'email'
        phone: '',
        email: '',
        attempts: 0,
        expired: false,
        locked: false,
        onSuccess: null,
        onCancel: null
    };

    var mounted = false;

    /* ---------- 마크업 · 스타일 ---------- */

    function injectStyles() {
        if (document.getElementById('alimtalkAuthStyles')) return;
        var style = document.createElement('style');
        style.id = 'alimtalkAuthStyles';
        style.textContent = [
            '.atk-auth-overlay{display:none;position:fixed;inset:0;z-index:2100;background:rgba(15,23,42,0.45);align-items:center;justify-content:center;padding:24px;}',
            '.atk-auth-overlay.is-open{display:flex;}',
            '.atk-auth-box{background:#fff;border-radius:16px;max-width:420px;width:100%;padding:40px 40px 32px;box-shadow:0 8px 32px rgba(15,23,42,0.12);max-height:90vh;overflow-y:auto;}',
            '.atk-auth-brand{text-align:center;margin-bottom:24px;}',
            '.atk-auth-brand img{height:34px;width:auto;}',
            '.atk-auth-box h2{font-size:26px;font-weight:800;color:#0f172a;text-align:center;margin-bottom:8px;line-height:1.35;letter-spacing:-0.03em;}',
            '.atk-auth-subtitle{font-size:14px;color:#64748b;text-align:center;line-height:1.65;margin-bottom:20px;}',
            '.atk-auth-subtitle strong{color:#0f172a;font-weight:600;}',
            /* 알림톡 채널 안내 */
            '.atk-auth-channel{display:flex;align-items:center;gap:10px;background:#fffdf0;border:1px solid #f2e08a;border-radius:10px;padding:12px 14px;font-size:13px;font-weight:500;color:#475569;line-height:1.55;margin-bottom:20px;}',
            '.atk-auth-badge{display:inline-flex;align-items:center;gap:4px;background:#FEE500;color:#3c1e1e;border-radius:6px;padding:4px 9px;font-size:12px;font-weight:800;white-space:nowrap;flex-shrink:0;}',
            '.atk-auth-badge svg{width:13px;height:13px;}',
            /* 폼 */
            '.atk-auth-label{display:block;margin-bottom:8px;font-weight:600;font-size:14px;color:#334155;}',
            '.atk-auth-label .required{color:#ef4444;}',
            '.atk-auth-input{width:100%;padding:13px 16px;font-size:14px;border:1px solid #dde3ea;border-radius:8px;background:#fff;color:#1e293b;transition:border-color .2s,box-shadow .2s;font-family:inherit;}',
            '.atk-auth-input:focus{outline:none;border-color:#5cb82e;box-shadow:0 0 0 3px rgba(92,184,46,0.12);}',
            '.atk-auth-input::placeholder{color:#94a3b8;}',
            '.atk-auth-input:disabled{background:#f1f5f9;color:#94a3b8;cursor:not-allowed;}',
            '.atk-auth-error{margin-top:8px;font-size:12px;color:#ef4444;display:none;}',
            '.atk-auth-error.show{display:block;}',
            '.atk-auth-help{margin-top:6px;font-size:12px;color:#94a3b8;line-height:1.6;}',
            /* 발신번호 ↔ 인증번호 연계 정보 */
            '.atk-auth-link-box{border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;padding:14px 16px;}',
            '.atk-auth-link-row{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;padding:4px 0;}',
            '.atk-auth-link-label{color:#64748b;font-weight:500;flex-shrink:0;}',
            '.atk-auth-link-value{color:#334155;font-weight:600;text-align:right;word-break:break-all;}',
            '.atk-auth-link-value.is-strong{color:#0f172a;font-weight:800;font-size:15px;letter-spacing:0.01em;}',
            /* 유선번호 ARS 인증 */
            '.atk-auth-ars-badge{display:inline-flex;align-items:center;gap:5px;background:#e0f2fe;color:#0369a1;border-radius:6px;padding:4px 9px;font-size:12px;font-weight:800;white-space:nowrap;flex-shrink:0;}',
            '.atk-auth-mail-badge{display:inline-flex;align-items:center;gap:5px;background:#eef2ff;color:#4338ca;border-radius:6px;padding:4px 9px;font-size:12px;font-weight:800;white-space:nowrap;flex-shrink:0;}',
            '.atk-auth-channel.is-email{background:#f5f7ff;border-color:#c7d2fe;}',
            '.atk-auth-mail-badge svg{width:13px;height:13px;}',
            '.atk-auth-ars-guide{background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:14px 16px;margin-top:16px;font-size:13px;line-height:1.7;color:#0c4a6e;}',
            '.atk-auth-ars-number{display:block;text-align:center;font-size:24px;font-weight:800;color:#0f172a;letter-spacing:0.02em;margin:10px 0 4px;}',
            '.atk-auth-ars-status{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:16px;padding:12px;border:1px dashed #cbd5e1;border-radius:8px;font-size:13px;font-weight:600;color:#64748b;}',
            '.atk-auth-ars-status .dot{width:8px;height:8px;border-radius:50%;background:#38bdf8;animation:atkPulse 1.2s ease-in-out infinite;}',
            '@keyframes atkPulse{0%,100%{opacity:1}50%{opacity:0.3}}',
            /* 인증번호 + 타이머 */
            '.atk-auth-code-row{display:flex;align-items:center;gap:10px;}',
            '.atk-auth-code-row .atk-auth-input{flex:1;}',
            '.atk-auth-timer{font-size:14px;font-weight:700;color:#ef4444;white-space:nowrap;min-width:46px;text-align:right;}',
            /* 재전송 · SMS 대체 */
            '.atk-auth-resend-wrap{text-align:right;margin-top:12px;}',
            '.atk-auth-resend-btn{background:none;border:none;padding:2px 0;font-size:13px;font-weight:600;color:#5cb82e;text-decoration:underline;cursor:pointer;font-family:inherit;}',
            '.atk-auth-resend-btn:disabled{color:#94a3b8;text-decoration:none;cursor:default;}',
            '.atk-auth-fallback{margin-top:14px;padding-top:14px;border-top:1px dashed #e2e8f0;font-size:13px;color:#94a3b8;text-align:center;}',
            '.atk-auth-fallback.used{color:#10b981;}',
            '.atk-auth-link-btn{background:none;border:none;padding:2px 0;font-size:13px;font-weight:700;color:#5cb82e;text-decoration:underline;cursor:pointer;font-family:inherit;}',
            /* 버튼 */
            '.atk-auth-actions{display:flex;flex-direction:column;gap:10px;margin-top:24px;}',
            '.atk-auth-btn{flex:1;padding:14px 16px;border-radius:8px;font-size:15px;font-weight:700;border:none;cursor:pointer;font-family:inherit;transition:background .2s,color .2s;}',
            '.atk-auth-btn-primary{background:#5cb82e;color:#fff;}',
            '.atk-auth-btn-primary:hover:not(:disabled){background:#4a9a24;}',
            '.atk-auth-btn-primary:disabled{background:#cbd5e1;cursor:not-allowed;}',
            '.atk-auth-btn-cancel{background:#fff;color:#475569;border:1px solid #dde3ea;}',
            '.atk-auth-btn-cancel:hover{background:#f8fafc;}',
            '.atk-auth-footnote{margin-top:18px;text-align:center;font-size:12px;color:#94a3b8;}',
            '.atk-auth-footnote a{color:#5cb82e;font-weight:600;text-decoration:none;}'
        ].join('\n');
        document.head.appendChild(style);
    }

    function injectMarkup() {
        if (document.getElementById('alimtalkAuthModal')) return;
        var wrap = document.createElement('div');
        wrap.innerHTML = [
            '<div class="atk-auth-overlay" id="alimtalkAuthModal" role="dialog" aria-modal="true" aria-labelledby="atkAuthTitle">',
            '  <div class="atk-auth-box">',
            '    <div class="atk-auth-brand"><img src="' + LOGO_SRC + '" alt="tokbell" width="140" height="34"></div>',
            /* 1단계 */
            '    <div id="atkAuthStep1">',
            '      <h2 id="atkAuthTitle">알림톡 인증</h2>',
            '      <p class="atk-auth-subtitle" id="atkAuthDesc"></p>',
            '      <div class="atk-auth-channel" id="atkAuthChannelBox">',
            '        <span class="atk-auth-badge">',
            '          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.9 3 2.8 6.3 2.8 10.3c0 2.6 1.7 4.9 4.3 6.2-.2.7-.7 2.5-.8 2.9 0 .2.1.4.3.3.3-.1 2.6-1.7 3.6-2.4.6.1 1.2.1 1.8.1 5.1 0 9.2-3.3 9.2-7.3S17.1 3 12 3z"/></svg>',
            '          알림톡',
            '        </span>',
            '        <span>카카오톡 미사용 또는 수신 불가 시 문자(SMS)로 자동 대체 발송됩니다.</span>',
            '      </div>',
            /* 연계 정보 — 사용자가 번호를 직접 입력하지 않고, 등록·확인된 번호로만 인증한다 */
            '      <div class="atk-auth-link-box">',
            '        <div class="atk-auth-link-row" id="atkAuthCallerRow">',
            '          <span class="atk-auth-link-label">발신번호</span>',
            '          <span class="atk-auth-link-value" id="atkAuthCallerValue">-</span>',
            '        </div>',
            '        <div class="atk-auth-link-row">',
            '          <span class="atk-auth-link-label" id="atkAuthTargetLabel">인증받을 번호</span>',
            '          <span class="atk-auth-link-value is-strong" id="atkAuthPhoneMasked">-</span>',
            '        </div>',
            '      </div>',
            '      <p class="atk-auth-help" id="atkAuthLinkHelp"></p>',
            '      <div class="atk-auth-error" id="atkAuthPhoneError">등록된 인증 번호가 없습니다. 마이페이지에서 인증 수단을 먼저 등록해 주세요.</div>',
            '      <div class="atk-auth-actions">',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-primary" id="atkAuthSendBtn">인증 번호 보내기</button>',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-cancel" id="atkAuthCancelBtn">취소</button>',
            '      </div>',
            '      <p class="atk-auth-footnote">인증 과정에 어려움이 있나요? <a href="support-inquiry.html">1:1 문의하기</a></p>',
            '    </div>',
            /* 2단계 */
            '    <div id="atkAuthStep2" style="display:none;">',
            '      <h2 id="atkAuthTitle2">알림톡 인증</h2>',
            '      <p class="atk-auth-subtitle"><strong id="atkAuthPhoneDisplay">010-0000-0000</strong>로 발송된<br><strong id="atkAuthChannelLabel">알림톡</strong>의 인증번호 6자리를 입력해주세요.</p>',
            '      <label class="atk-auth-label" for="atkAuthCode">인증번호 <span class="required">*</span></label>',
            '      <div class="atk-auth-code-row">',
            '        <input type="tel" inputmode="numeric" autocomplete="one-time-code" class="atk-auth-input" id="atkAuthCode" placeholder="인증번호 6자리" maxlength="6">',
            '        <span class="atk-auth-timer" id="atkAuthTimer">03:00</span>',
            '      </div>',
            '      <div class="atk-auth-error" id="atkAuthCodeError">인증번호 6자리를 입력해주세요.</div>',
            '      <p class="atk-auth-help">인증번호 유효시간 3분</p>',
            '      <div class="atk-auth-resend-wrap">',
            '        <button type="button" class="atk-auth-resend-btn" id="atkAuthResendBtn" disabled>인증번호 재전송</button>',
            '      </div>',
            '      <div class="atk-auth-fallback" id="atkAuthFallback"></div>',
            '      <div class="atk-auth-actions">',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-primary" id="atkAuthVerifyBtn">인증하기</button>',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-cancel" id="atkAuthBackBtn">취소</button>',
            '      </div>',
            '      <p class="atk-auth-footnote">인증 과정에 어려움이 있나요? <a href="support-inquiry.html">1:1 문의하기</a></p>',
            '    </div>',
            /* 유선·대표번호 ARS 인증 단계 */
            '    <div id="atkAuthStepArs" style="display:none;">',
            '      <h2 id="atkAuthArsTitle">발송 추가 인증</h2>',
            '      <p class="atk-auth-subtitle">유선·대표번호는 ARS 음성 인증으로<br>발신번호 소유를 확인합니다.</p>',
            '      <div class="atk-auth-channel">',
            '        <span class="atk-auth-ars-badge">ARS</span>',
            '        <span>알림톡·문자는 휴대폰 전용이라 유선번호는 ARS 로 인증합니다.</span>',
            '      </div>',
            '      <div class="atk-auth-link-box">',
            '        <div class="atk-auth-link-row">',
            '          <span class="atk-auth-link-label">발신번호</span>',
            '          <span class="atk-auth-link-value" id="atkAuthArsCaller">-</span>',
            '        </div>',
            '      </div>',
            '      <div class="atk-auth-ars-guide">',
            '        아래 <strong>인증 전화번호</strong>로 <strong id="atkAuthArsFrom">발신번호</strong> 에서 전화를 걸어주세요.',
            '        <span class="atk-auth-ars-number" id="atkAuthArsNumber">1600-0000</span>',
            '        시스템이 인입 번호와 등록된 발신번호의 일치 여부를 확인해 자동으로 인증 처리합니다.',
            '      </div>',
            '      <div class="atk-auth-ars-status" id="atkAuthArsStatus">',
            '        <span class="dot"></span><span>수신 대기 중</span>',
            '        <span class="atk-auth-timer" id="atkAuthArsTimer">05:00</span>',
            '      </div>',
            '      <div class="atk-auth-error" id="atkAuthArsError">아직 인증 전화가 확인되지 않았습니다. 통화 후 다시 시도해주세요.</div>',
            '      <div class="atk-auth-actions">',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-primary" id="atkAuthArsVerifyBtn">인증 확인</button>',
            '        <button type="button" class="atk-auth-btn atk-auth-btn-cancel" id="atkAuthArsCancelBtn">취소</button>',
            '      </div>',
            '      <p class="atk-auth-footnote">인증 과정에 어려움이 있나요? <a href="support-inquiry.html">1:1 문의하기</a></p>',
            '    </div>',
            '  </div>',
            '</div>'
        ].join('\n');
        document.body.appendChild(wrap.firstElementChild);
    }

    /* ---------- 유틸 ---------- */

    function $(id) { return document.getElementById(id); }

    function sanitizePhone(value) {
        return String(value || '').replace(/\D/g, '').slice(0, 11);
    }

    /* 등록된 번호는 마스킹해 노출한다 (010-****-5678) */
    function maskPhone(digits) {
        if (!digits) return '-';
        if (digits.length < 7) return digits;
        var head = digits.slice(0, 3);
        var tail = digits.slice(-4);
        return head + '-****-' + tail;
    }

    /* 등록된 이메일도 마스킹해 노출한다 (ad****@ibank.co.kr) */
    function maskEmail(value) {
        var s = String(value || '');
        var at = s.indexOf('@');
        if (at < 1) return s || '-';
        var local = s.slice(0, at);
        var head = local.slice(0, Math.min(2, local.length));
        var stars = Math.max(4, local.length - head.length);
        return head + new Array(stars + 1).join('*') + s.slice(at);
    }

    /* 이메일 OTP 모드로 바뀐 라벨·안내를 기본(알림톡) 상태로 되돌린다.
     * 한 페이지에서 알림톡 인증과 이메일 OTP 를 함께 쓰는 경우가 있어 필요하다. */
    var PHONE_CHANNEL_HTML = '' +
        '<span class="atk-auth-badge">' +
          '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.9 3 2.8 6.3 2.8 10.3c0 2.6 1.7 4.9 4.3 6.2-.2.7-.7 2.5-.8 2.9 0 .2.1.4.3.3.3-.1 2.6-1.7 3.6-2.4.6.1 1.2.1 1.8.1 5.1 0 9.2-3.3 9.2-7.3S17.1 3 12 3z"/></svg>' +
          '알림톡' +
        '</span>' +
        '<span>카카오톡 미사용 또는 수신 불가 시 문자(SMS)로 자동 대체 발송됩니다.</span>';

    function restorePhoneLabels() {
        var box = $('atkAuthChannelBox');
        if (box) {
            box.classList.remove('is-email');
            box.innerHTML = PHONE_CHANNEL_HTML;
        }
        var label = $('atkAuthTargetLabel');
        if (label) label.textContent = '인증받을 번호';
        var err = $('atkAuthPhoneError');
        if (err) err.textContent = '등록된 인증 번호가 없습니다. 마이페이지에서 인증 수단을 먼저 등록해 주세요.';
        var sendBtn = $('atkAuthSendBtn');
        if (sendBtn) sendBtn.textContent = '인증 번호 보내기';
    }

    function showError(id, show) {
        var el = $(id);
        if (el) el.classList.toggle('show', !!show);
    }

    /* 인증번호 오류 문구를 상황별로 교체해 노출한다. */
    function setCodeError(message) {
        var el = $('atkAuthCodeError');
        if (!el) return;
        el.textContent = message;
        el.classList.add('show');
    }

    /* 시도 횟수 초과 · 유효시간 만료 → 재전송 전까지 인증 차단 */
    function lockCode(message) {
        state.locked = true;
        setCodeError(message);
        $('atkAuthCode').disabled = true;
        $('atkAuthVerifyBtn').disabled = true;
        clearInterval(state.timerInterval);
        state.timerInterval = null;
        $('atkAuthTimer').textContent = '00:00';  // 잠긴 인증번호는 만료 처리
        $('atkAuthResendBtn').disabled = false;
    }

    function unlockCode() {
        state.locked = false;
        state.expired = false;
        $('atkAuthCode').disabled = false;
        $('atkAuthVerifyBtn').disabled = false;
    }

    /* ---------- 흐름 ---------- */

    function applyChannel() {
        var fallback = $('atkAuthFallback');

        // 이메일 OTP 모드에는 문자(SMS) 대체 발송이 없다.
        if (state.mode === 'email') {
            $('atkAuthChannelLabel').textContent = '이메일';
            fallback.classList.remove('used');
            fallback.innerHTML = '';
            fallback.style.display = 'none';
            return;
        }

        fallback.style.display = '';
        var isSms = state.channel === 'sms';
        $('atkAuthChannelLabel').textContent = isSms ? '문자(SMS)' : '알림톡';
        fallback.classList.toggle('used', isSms);
        fallback.innerHTML = isSms
            ? '문자(SMS)로 인증번호를 다시 보냈습니다.'
            : '카카오톡으로 받지 못하셨나요? <button type="button" class="atk-auth-link-btn" id="atkAuthSmsBtn">문자(SMS)로 받기</button>';
        var btn = $('atkAuthSmsBtn');
        if (btn) btn.addEventListener('click', handleSmsFallback);
    }

    /* 재전송 — 새 인증번호가 발송되므로 이전 입력·오류·시도횟수를 모두 비운다. */
    function handleResend() {
        $('atkAuthCode').value = '';
        showError('atkAuthCodeError', false);
        startTimer();
        $('atkAuthCode').focus();
    }

    function handleSmsFallback() {
        state.channel = 'sms';
        applyChannel();
        $('atkAuthCode').value = '';
        showError('atkAuthCodeError', false);
        startTimer();
        $('atkAuthCode').focus();
    }

    function startTimer() {
        clearInterval(state.timerInterval);
        state.seconds = TIMER_SECONDS;
        state.attempts = 0;
        unlockCode();
        var timerEl = $('atkAuthTimer');
        var resendBtn = $('atkAuthResendBtn');
        resendBtn.disabled = true;

        function tick() {
            var min = Math.floor(state.seconds / 60);
            var sec = state.seconds % 60;
            timerEl.textContent = ('0' + min).slice(-2) + ':' + ('0' + sec).slice(-2);
            if (state.seconds <= 0) {
                clearInterval(state.timerInterval);
                state.timerInterval = null;
                timerEl.textContent = '00:00';
                state.expired = true;
                // 유효시간 만료 → 재전송 전까지 인증 불가
                lockCode('인증번호 유효시간이 만료되었습니다. 인증번호를 재전송해 주세요.');
                return;
            }
            state.seconds--;
        }

        tick();
        state.timerInterval = setInterval(tick, 1000);
    }

    function reset() {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
        state.mode = 'phone';
        state.channel = 'alimtalk';
        state.attempts = 0;
        restorePhoneLabels();
        unlockCode();
        clearInterval(arsTimerInterval);
        arsTimerInterval = null;
        $('atkAuthStep1').style.display = '';
        $('atkAuthStep2').style.display = 'none';
        if ($('atkAuthStepArs')) $('atkAuthStepArs').style.display = 'none';
        $('atkAuthCode').value = '';
        showError('atkAuthPhoneError', false);
        showError('atkAuthCodeError', false);
        applyChannel();
    }

    function showStep2(target) {
        $('atkAuthStep1').style.display = 'none';
        $('atkAuthStep2').style.display = '';
        // 2단계도 동일하게 마스킹해 노출한다
        $('atkAuthPhoneDisplay').textContent = state.mode === 'email' ? maskEmail(target) : maskPhone(target);
        $('atkAuthCode').value = '';
        showError('atkAuthCodeError', false);
        startTimer();
        setTimeout(function () { $('atkAuthCode').focus(); }, 50);
    }

    function handleSend() {
        // 사용자가 번호·이메일을 입력하지 않는다. 계정에 등록·확인된 값으로만 발송한다.
        var target = state.mode === 'email' ? state.email : state.phone;
        if (!target) {
            showError('atkAuthPhoneError', true);
            return;
        }
        showError('atkAuthPhoneError', false);
        showStep2(target);
    }

    function handleVerify() {
        if (state.locked) return;

        var input = $('atkAuthCode');
        var code = input.value.replace(/\D/g, '');
        input.value = code;

        // 미입력 · 자릿수 부족
        if (code.length !== 6) {
            setCodeError('인증번호 6자리를 입력해주세요.');
            return;
        }

        // 유효시간 만료
        if (state.expired) {
            lockCode('인증번호 유효시간이 만료되었습니다. 인증번호를 재전송해 주세요.');
            return;
        }

        // 인증번호 불일치
        if (code !== DEMO_CODE) {
            state.attempts++;
            if (state.attempts >= MAX_ATTEMPTS) {
                lockCode('인증 시도 횟수(' + MAX_ATTEMPTS + '회)를 초과했습니다. 인증번호를 재전송해 주세요.');
            } else {
                setCodeError('인증번호가 일치하지 않습니다. (' + state.attempts + '/' + MAX_ATTEMPTS + '회)');
                input.focus();
                input.select();
            }
            return;
        }

        var result = { phone: state.phone, email: state.email, channel: state.channel, mode: state.mode };
        var cb = state.onSuccess;
        close(true);
        if (typeof cb === 'function') cb(result);
    }

    function close(skipCancel) {
        var el = $('alimtalkAuthModal');
        if (el) el.classList.remove('is-open');
        var cb = state.onCancel;
        reset();
        if (!skipCancel && typeof cb === 'function') cb();
        state.onSuccess = null;
        state.onCancel = null;
    }

    function bind() {
        if (mounted) return;
        mounted = true;

        $('atkAuthCode').addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '').slice(0, 6);
            showError('atkAuthCodeError', false);
        });
        $('atkAuthCode').addEventListener('keydown', function (e) {
            if (e.key === 'Enter') { e.preventDefault(); handleVerify(); }
        });

        $('atkAuthArsVerifyBtn').addEventListener('click', handleArsVerify);
        $('atkAuthArsCancelBtn').addEventListener('click', function () { close(); });
        $('atkAuthSendBtn').addEventListener('click', handleSend);
        $('atkAuthVerifyBtn').addEventListener('click', handleVerify);
        $('atkAuthCancelBtn').addEventListener('click', function () { close(); });
        $('atkAuthBackBtn').addEventListener('click', function () { close(); });
        $('atkAuthResendBtn').addEventListener('click', function () {
            if (this.disabled) return;
            handleResend();
        });

        $('alimtalkAuthModal').addEventListener('click', function (e) {
            if (e.target === this) close();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && $('alimtalkAuthModal').classList.contains('is-open')) close();
        });
    }

    function mount() {
        injectStyles();
        injectMarkup();
        bind();
    }

    /* ---------- 공개 API ---------- */

    window.openAlimtalkAuth = function (options) {
        var opts = options || {};
        mount();
        reset();

        var title = opts.title || '알림톡 인증';
        $('atkAuthTitle').textContent = title;
        $('atkAuthTitle2').textContent = title;
        $('atkAuthDesc').innerHTML = opts.description
            || '보안을 위해 등록된 휴대폰 번호로<br>카카오톡 알림톡을 보내드립니다.';
        $('atkAuthVerifyBtn').textContent = opts.confirmText || '인증하기';

        /* 인증 대상은 호출부가 주입한 '등록·확인된 번호'로 고정한다.
         * 발송 인증에서는 선택한 발신번호를 함께 노출해 연계성을 명시한다. */
        state.phone = sanitizePhone(opts.phone || '');
        $('atkAuthPhoneMasked').textContent = state.phone ? maskPhone(state.phone) : '미등록';

        var callerRow = $('atkAuthCallerRow');
        if (opts.callerNumber) {
            callerRow.style.display = '';
            $('atkAuthCallerValue').textContent = opts.callerNumber;
            $('atkAuthLinkHelp').innerHTML = '발신번호 등록 시 본인확인한 번호입니다.<br>번호 변경은 마이페이지 &gt; 발신번호 관리에서 가능합니다.';
        } else {
            callerRow.style.display = 'none';
            $('atkAuthLinkHelp').innerHTML = '회원가입 시 본인확인한 번호입니다.<br>번호 변경은 마이페이지 &gt; 2차 인증 설정에서 가능합니다.';
        }

        // 등록된 번호가 없으면 발송 불가 — 등록 안내만 노출
        $('atkAuthSendBtn').disabled = !state.phone;
        showError('atkAuthPhoneError', !state.phone);

        state.onSuccess = opts.onSuccess || null;
        state.onCancel = opts.onCancel || null;

        $('alimtalkAuthModal').classList.add('is-open');
        setTimeout(function () { $('atkAuthSendBtn').focus(); }, 50);
    };

    /* ---------- 유선·대표번호 ARS 인증 (보안심사 3.5-③) ----------
     * 항목해설이 예시한 인바운드 방식: 인증받으려는 유선번호에서 사업자가 지정한
     * 번호로 전화를 걸면, 시스템이 인입 발신번호와 등록 요청 발신번호의 일치
     * 여부를 확인해 인증 처리한다.
     * 프로토타입: 실제 수신 확인 없이 "인증 확인" 클릭 시 성공 처리한다.
     */
    var ARS_TIMER_SECONDS = 300;   // 인증 전화 수신 대기 5분
    var arsTimerInterval = null;
    var arsSeconds = ARS_TIMER_SECONDS;

    function startArsTimer() {
        clearInterval(arsTimerInterval);
        arsSeconds = ARS_TIMER_SECONDS;
        var el = $('atkAuthArsTimer');

        function tick() {
            var m = Math.floor(arsSeconds / 60), sec = arsSeconds % 60;
            el.textContent = ('0' + m).slice(-2) + ':' + ('0' + sec).slice(-2);
            if (arsSeconds <= 0) {
                clearInterval(arsTimerInterval);
                arsTimerInterval = null;
                el.textContent = '00:00';
                showError('atkAuthArsError', true);
                $('atkAuthArsError').textContent = '인증 대기시간이 만료되었습니다. 취소 후 다시 시도해주세요.';
                $('atkAuthArsVerifyBtn').disabled = true;
                return;
            }
            arsSeconds--;
        }
        tick();
        arsTimerInterval = setInterval(tick, 1000);
    }

    function handleArsVerify() {
        var cb = state.onSuccess;
        var result = { callerNumber: state.phone, channel: 'ars' };
        clearInterval(arsTimerInterval);
        arsTimerInterval = null;
        close(true);
        if (typeof cb === 'function') cb(result);
    }

    /* ---------------------------------------------------------------
     * 이메일 OTP 인증 (보안심사 3.5-④ 기업관리자 사후승인)
     *
     * 심사 항목해설상 사후승인은 전자결재·관리자 콘솔 승인·이메일 승인·
     * 서면 결재 등 "승인(확인) 사실을 입증할 수 있는 방식"이면 된다.
     * 톡벨은 이 중 **이메일 승인**을 채택해, 기업 고객사의 관리자·담당자
     * 이메일로 6자리 인증번호를 보내고 이를 입력해야 발송되도록 한다.
     *
     * 인증 대상 이메일은 사용자가 직접 입력하지 않고, 계정에 등록·확인된
     * 승인 담당자 이메일로 고정된다(3.4-② 연계 기준과 동일).
     *
     * 실제 연동 시 대체할 API
     *   POST /api/send-approval/otp/send    승인용 이메일 OTP 발송
     *   POST /api/send-approval/otp/verify  OTP 검증
     * --------------------------------------------------------------- */
    window.openEmailOtpAuth = function (options) {
        var opts = options || {};
        mount();
        reset();

        state.mode = 'email';
        state.channel = 'email';
        state.email = String(opts.email || '').trim();
        state.phone = '';

        var title = opts.title || '발송 승인 인증';
        $('atkAuthTitle').textContent = title;
        $('atkAuthTitle2').textContent = title;
        $('atkAuthDesc').innerHTML = opts.description
            || '발송 승인을 위해 등록된 담당자 이메일로<br>인증번호를 보내드립니다.';
        $('atkAuthVerifyBtn').textContent = opts.confirmText || '인증하고 발송하기';

        // 채널 안내를 이메일로 교체
        $('atkAuthChannelBox').classList.add('is-email');
        $('atkAuthChannelBox').innerHTML =
            '<span class="atk-auth-mail-badge">' +
              '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 4.8-8-4.8V6l8 4.8L20 6z"/></svg>' +
              '이메일' +
            '</span>' +
            '<span>' + (opts.channelNote || '기업 고객사 승인 담당자 이메일로 6자리 인증번호가 발송됩니다.') + '</span>';

        // 연계 정보 — 발신번호와 승인 담당자 이메일을 함께 노출한다
        var callerRow = $('atkAuthCallerRow');
        if (opts.callerNumber) {
            callerRow.style.display = '';
            $('atkAuthCallerValue').textContent = opts.callerNumber;
        } else {
            callerRow.style.display = 'none';
        }

        $('atkAuthTargetLabel').textContent = '승인 담당자';
        $('atkAuthPhoneMasked').textContent = state.email ? maskEmail(state.email) : '미등록';
        $('atkAuthLinkHelp').innerHTML = opts.linkHelp
            || '기업 고객사에 등록·확인된 승인 담당자 이메일입니다.<br>변경은 마이페이지 &gt; 발송 사후승인에서 가능합니다.';

        $('atkAuthPhoneError').textContent = '등록된 승인 담당자 이메일이 없습니다. 마이페이지에서 먼저 등록해 주세요.';
        $('atkAuthSendBtn').disabled = !state.email;
        showError('atkAuthPhoneError', !state.email);
        $('atkAuthSendBtn').textContent = '인증번호 받기';

        state.onSuccess = typeof opts.onSuccess === 'function' ? opts.onSuccess : null;
        state.onCancel = typeof opts.onCancel === 'function' ? opts.onCancel : null;

        applyChannel();
        $('alimtalkAuthModal').classList.add('is-open');
    };

    /* 유선·대표번호 여부 판정 — 01X 가 아니면 유선으로 본다. */
    window.isLandlineNumber = function (value) {
        var digits = String(value || '').replace(/\D/g, '');
        return digits.length > 0 && !/^01[0-9]{8,9}$/.test(digits);
    };

    window.openArsAuth = function (options) {
        var opts = options || {};
        mount();
        reset();

        var caller = opts.callerNumber || '-';
        $('atkAuthArsTitle').textContent = opts.title || '발송 추가 인증';
        $('atkAuthArsCaller').textContent = caller;
        $('atkAuthArsFrom').textContent = caller;
        $('atkAuthArsNumber').textContent = opts.arsNumber || '1600-0000';
        $('atkAuthArsVerifyBtn').disabled = false;
        showError('atkAuthArsError', false);
        $('atkAuthArsError').textContent = '아직 인증 전화가 확인되지 않았습니다. 통화 후 다시 시도해주세요.';

        state.phone = caller;
        state.onSuccess = opts.onSuccess || null;
        state.onCancel = opts.onCancel || null;

        $('atkAuthStep1').style.display = 'none';
        $('atkAuthStep2').style.display = 'none';
        $('atkAuthStepArs').style.display = '';

        $('alimtalkAuthModal').classList.add('is-open');
        startArsTimer();
        setTimeout(function () { $('atkAuthArsVerifyBtn').focus(); }, 50);
    };

    /* ===================================================================
     * 발송 추가 인증 세션 (보안심사 3.5-⑤ 재인증 기준)
     *
     * 심사 항목해설상 매 발송 건마다 인증을 반복할 필요는 없으며,
     * 동일 세션에서 일정 시간 인증 상태를 유지하되 위험 조건에서는
     * 재인증하도록 운영할 수 있다. 아래 기준으로 판정한다.
     *
     *   1) 최초 발송            → 인증 필요
     *   2) 인증 후 30분 경과    → 인증 필요 (유효시간 만료)
     *   3) 발신번호 변경        → 인증 필요
     *   4) 대량발송 임계 초과   → 인증 필요
     *   5) 접속환경 변경        → 인증 필요
     *
     * 프로토타입: sessionStorage 기반이며 접속환경은 User-Agent 지문으로 대체한다.
     * 실제 연동 시 서버 세션과 접속 IP 기준으로 판정한다.
     * =================================================================== */

    var SEND_AUTH_VALID_MINUTES = 30;   // 인증 유지 시간
    var BULK_SEND_THRESHOLD = 1000;     // 대량발송 재인증 임계 건수 (사업자 자체 기준)

    var SESSION_KEYS = { at: 'sendAuthAt', caller: 'sendAuthCaller', env: 'sendAuthEnv' };

    function envFingerprint() {
        return String(navigator.userAgent || '').slice(0, 120);
    }

    /* 재인증 필요 여부와 사유를 반환한다. */
    window.getSendAuthState = function (ctx) {
        ctx = ctx || {};
        var count = Number(ctx.recipientCount || 0);
        var caller = String(ctx.callerNumber || '');

        if (count >= BULK_SEND_THRESHOLD) {
            return { required: true, code: 'bulk',
                     reason: '대량발송(' + BULK_SEND_THRESHOLD.toLocaleString() + '건 이상)은 매번 인증이 필요합니다.' };
        }

        var at = Number(sessionStorage.getItem(SESSION_KEYS.at) || 0);
        if (!at) {
            return { required: true, code: 'none', reason: '' };
        }

        var elapsedMin = (Date.now() - at) / 60000;
        if (elapsedMin >= SEND_AUTH_VALID_MINUTES) {
            return { required: true, code: 'expired',
                     reason: '인증 유효시간(' + SEND_AUTH_VALID_MINUTES + '분)이 지나 다시 인증이 필요합니다.' };
        }
        if (sessionStorage.getItem(SESSION_KEYS.caller) !== caller) {
            return { required: true, code: 'caller-changed',
                     reason: '발신번호가 변경되어 다시 인증이 필요합니다.' };
        }
        if (sessionStorage.getItem(SESSION_KEYS.env) !== envFingerprint()) {
            return { required: true, code: 'env-changed',
                     reason: '접속환경이 변경되어 다시 인증이 필요합니다.' };
        }

        return { required: false, code: 'valid', remainMin: Math.max(1, Math.ceil(SEND_AUTH_VALID_MINUTES - elapsedMin)) };
    };

    /* 인증 성공 시 세션에 상태를 기록한다. */
    window.markSendAuthenticated = function (ctx) {
        ctx = ctx || {};
        sessionStorage.setItem(SESSION_KEYS.at, String(Date.now()));
        sessionStorage.setItem(SESSION_KEYS.caller, String(ctx.callerNumber || ''));
        sessionStorage.setItem(SESSION_KEYS.env, envFingerprint());
    };

    window.SEND_AUTH_VALID_MINUTES = SEND_AUTH_VALID_MINUTES;
    window.BULK_SEND_THRESHOLD = BULK_SEND_THRESHOLD;

    window.closeAlimtalkAuth = function () { close(); };
    window.mountAlimtalkAuth = mount;

    /* 화면설계 오버레이는 첫 토글 시점에 마커를 한 번만 만든다.
     * 그 전에 모달이 DOM 에 없으면 인증 항목 마커가 누락되므로 미리 올려둔다. */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', mount);
    } else {
        mount();
    }
})();
