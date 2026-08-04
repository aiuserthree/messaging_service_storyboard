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
 *       onSuccess: function (result) { ... },  // result: { phone, channel }
 *       onCancel: function () { ... }
 *   });
 *
 * 프로토타입 한계: 실제 발송·대조 없이 형식 검증만 수행한다.
 * 인증번호는 6자리 숫자면 통과한다.
 */
(function () {
    'use strict';

    var TIMER_SECONDS = 180;
    var LOGO_SRC = 'img/logo/tokbell_logo_o.png';

    var state = {
        timerInterval: null,
        seconds: TIMER_SECONDS,
        channel: 'alimtalk', // 'alimtalk' | 'sms'
        phone: '',
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
            '.atk-auth-error{margin-top:8px;font-size:12px;color:#ef4444;display:none;}',
            '.atk-auth-error.show{display:block;}',
            '.atk-auth-help{margin-top:6px;font-size:12px;color:#94a3b8;}',
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
            '      <label class="atk-auth-label" for="atkAuthPhone">휴대폰 번호 <span class="required">*</span></label>',
            '      <input type="tel" inputmode="numeric" autocomplete="tel" class="atk-auth-input" id="atkAuthPhone" placeholder="숫자만 입력 (예: 01012345678)" maxlength="11">',
            '      <div class="atk-auth-error" id="atkAuthPhoneError">휴대폰 번호를 올바르게 입력해주세요.</div>',
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

    function formatPhoneDisplay(digits) {
        if (digits.length <= 3) return digits;
        if (digits.length <= 7) return digits.slice(0, 3) + '-' + digits.slice(3);
        return digits.slice(0, 3) + '-' + digits.slice(3, 7) + '-' + digits.slice(7);
    }

    function sanitizePhone(value) {
        return String(value || '').replace(/\D/g, '').slice(0, 11);
    }

    function showError(id, show) {
        var el = $(id);
        if (el) el.classList.toggle('show', !!show);
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
                resendBtn.disabled = false;
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
        state.phone = '';
        $('atkAuthStep1').style.display = '';
        $('atkAuthStep2').style.display = 'none';
        $('atkAuthPhone').value = '';
        $('atkAuthCode').value = '';
        showError('atkAuthPhoneError', false);
        showError('atkAuthCodeError', false);
        applyChannel();
    }

    function showStep2(phoneDigits) {
        state.phone = phoneDigits;
        $('atkAuthStep1').style.display = 'none';
        $('atkAuthStep2').style.display = '';
        $('atkAuthPhoneDisplay').textContent = formatPhoneDisplay(phoneDigits);
        $('atkAuthCode').value = '';
        showError('atkAuthCodeError', false);
        startTimer();
        setTimeout(function () { $('atkAuthCode').focus(); }, 50);
    }

    function handleSend() {
        var input = $('atkAuthPhone');
        var digits = sanitizePhone(input.value);
        input.value = digits;

        var valid = /^01[0-9]{8,9}$/.test(digits);
        showError('atkAuthPhoneError', !valid);
        if (!valid) return;

        showStep2(digits);
    }

    function handleVerify() {
        var input = $('atkAuthCode');
        var code = input.value.replace(/\D/g, '');
        input.value = code;
        var valid = code.length === 6;
        showError('atkAuthCodeError', !valid);
        if (!valid) return;

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

        $('atkAuthPhone').addEventListener('input', function () {
            this.value = sanitizePhone(this.value);
            showError('atkAuthPhoneError', false);
        });
        $('atkAuthPhone').addEventListener('keydown', function (e) {
            if (e.key === 'Enter') { e.preventDefault(); handleSend(); }
        });
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
            startTimer();
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

        state.onSuccess = opts.onSuccess || null;
        state.onCancel = opts.onCancel || null;

        $('alimtalkAuthModal').classList.add('is-open');
        setTimeout(function () { $('atkAuthPhone').focus(); }, 50);
    };

    window.closeAlimtalkAuth = function () { close(); };
})();
