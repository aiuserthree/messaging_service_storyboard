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
        channel: 'alimtalk', // 'alimtalk' | 'sms'
        phone: '',
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
            '      <div class="atk-auth-channel">',
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
            '          <span class="atk-auth-link-label">인증받을 번호</span>',
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
        var isSms = state.channel === 'sms';
        $('atkAuthChannelLabel').textContent = isSms ? '문자(SMS)' : '알림톡';
        var fallback = $('atkAuthFallback');
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
        state.channel = 'alimtalk';
        state.attempts = 0;
        unlockCode();
        $('atkAuthStep1').style.display = '';
        $('atkAuthStep2').style.display = 'none';
        $('atkAuthCode').value = '';
        showError('atkAuthPhoneError', false);
        showError('atkAuthCodeError', false);
        applyChannel();
    }

    function showStep2(phoneDigits) {
        state.phone = phoneDigits;
        $('atkAuthStep1').style.display = 'none';
        $('atkAuthStep2').style.display = '';
        $('atkAuthPhoneDisplay').textContent = maskPhone(phoneDigits);   // 2단계도 동일하게 마스킹
        $('atkAuthCode').value = '';
        showError('atkAuthCodeError', false);
        startTimer();
        setTimeout(function () { $('atkAuthCode').focus(); }, 50);
    }

    function handleSend() {
        // 사용자가 번호를 입력하지 않는다. 계정·발신번호에 등록·확인된 번호로만 발송한다.
        if (!state.phone) {
            showError('atkAuthPhoneError', true);
            return;
        }
        showError('atkAuthPhoneError', false);
        showStep2(state.phone);
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

        var result = { phone: state.phone, channel: state.channel };
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
