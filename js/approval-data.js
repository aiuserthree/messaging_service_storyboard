/* =====================================================================
 * 발송 승인 (이메일 OTP) — 공용 데이터·유틸 (보안심사 3.5-④)
 *
 * 심사 항목해설
 *   · 사후승인의 기업관리자는 문자재판매사업자가 아니라 서비스를 이용하는
 *     기업 고객사의 관리자 또는 담당자를 의미한다.
 *   · 사후승인은 전자결재 · 관리자 콘솔 승인 · 이메일 승인 · 서면 결재 등
 *     승인(확인) 사실을 입증할 수 있는 방식으로 제공하면 된다.
 *
 * 톡벨은 이 중 **이메일 승인**을 채택한다.
 *   문자 발송 시 기업 고객사의 승인 담당자 이메일로 6자리 인증번호를 보내고,
 *   담당자가 이를 입력하면 그 시점에 **발송 승인이 완료**된다.
 *   별도의 승인 대기 큐·승인 콘솔 화면은 두지 않는다.
 *
 * 승인 사실은 화면이 아니라 서버 이력으로 보관한다(입증자료).
 *   승인번호 / 처리일시 / 처리자 / 본인확인 수단(이메일 OTP) /
 *   발신번호 / 발송 건수 / 접속 IP
 *
 * 사용 화면
 *   message-send-general / -ad / -election, mobile/message-send-mobile
 *     → 발송 시 openEmailOtpAuth() 로 인증, 통과하면 발송 + 이력 적재
 *   email-approval-otp.html
 *     → 담당자에게 발송되는 인증번호 메일 양식(증빙용 미리보기)
 *
 * 프로토타입: 이력은 localStorage 데모이며 실제 연동 시 API 로 대체한다.
 *   GET  /api/send-approval/approver   승인 담당자 조회
 *   POST /api/send-approval/otp/send   승인용 이메일 OTP 발송
 *   POST /api/send-approval/otp/verify OTP 검증
 *   POST /api/send-approval/record     승인 사실 기록(인증 통과 시)
 * ===================================================================== */

(function () {
    'use strict';

    /* ================= 상수 ================= */

    window.APPROVAL_OTP_MINUTES = 3;      // 이메일 OTP 유효시간
    window.APPROVAL_OTP_MAX_TRY = 5;      // OTP 입력 허용 횟수
    window.APPROVAL_OTP_DEMO = '123456';  // 프로토타입 데모 인증번호

    var HISTORY_KEY = 'sendApprovalHistory';

    /* 데모 승인 담당자 — 실제 연동 시 GET /api/send-approval/approver 로 대체.
     * 기업 고객사에 등록·확인된 주소이며 발송 화면에서 직접 입력할 수 없다. */
    window.APPROVAL_ADMIN = {
        company: '(주)아이뱅크',
        name: '김담당',
        email: 'admin@ibank.co.kr',
        ip: '211.36.142.77'
    };

    /* ================= 유틸 ================= */

    function pad2(n) { return ('0' + n).slice(-2); }

    window.apvStamp = function (date) {
        return date.getFullYear() + '-' + pad2(date.getMonth() + 1) + '-' + pad2(date.getDate()) + ' ' +
               pad2(date.getHours()) + ':' + pad2(date.getMinutes());
    };

    window.apvNow = function () { return window.apvStamp(new Date()); };

    window.apvDateOnly = function (date) {
        return date.getFullYear() + '-' + pad2(date.getMonth() + 1) + '-' + pad2(date.getDate());
    };

    window.apvComma = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); };

    window.apvMaskPhone = function (value) {
        var digits = String(value || '').replace(/\D/g, '');
        if (digits.length < 7) return value || '-';
        return digits.slice(0, 3) + '-****-' + digits.slice(-4);
    };

    /* 이메일 마스킹 — 로컬파트 앞 2자만 노출 (ad****@ibank.co.kr) */
    window.apvMaskEmail = function (value) {
        var s = String(value || '');
        var at = s.indexOf('@');
        if (at < 1) return s || '-';
        var local = s.slice(0, at);
        var head = local.slice(0, Math.min(2, local.length));
        return head + new Array(Math.max(4, local.length - head.length) + 1).join('*') + s.slice(at);
    };

    window.apvEscape = function (s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    };

    window.apvToast = function (message, type) {
        if (typeof showToast === 'function') showToast(message, type || 'info');
    };

    /* 승인 확인 번호 — 승인(확인) 사실을 입증하는 식별자.
     * 실제 연동 시 서버가 발급하며 승인 결과 메일·이력에 동일하게 표기된다. */
    window.apvApprovalNo = function (seq, at) {
        return 'APV-' + String(at).replace(/[^0-9]/g, '').slice(2, 12) + '-' + String(seq).replace(/[^0-9]/g, '');
    };

    /* ================= 승인 이력 =================
     * 화면(메뉴)은 제공하지 않고 서버 이력으로만 보관한다.
     * 아래는 프로토타입에서 기록 항목을 확인하기 위한 localStorage 데모.
     */

    window.apvLoadHistory = function () {
        try {
            var saved = JSON.parse(localStorage.getItem(HISTORY_KEY));
            if (Array.isArray(saved)) return saved;
        } catch (e) {}
        return [];
    };

    /* 이메일 OTP 인증이 통과했을 때 승인 사실을 기록한다 (3.5-④ 입증자료).
     * 실제 연동 시 POST /api/send-approval/record 로 대체한다. */
    window.apvRecordSendApproval = function (info) {
        info = info || {};
        var admin = window.APPROVAL_ADMIN;
        var at = window.apvNow();
        var seq = String(Date.now()).slice(-4);

        var rec = {
            at: at,
            approvalNo: window.apvApprovalNo(seq, at),
            decision: 'approve',
            channel: info.channel || '웹 발송',
            caller: info.caller || '-',
            msgType: info.msgType || '-',
            count: Number(info.count || 0),
            actor: admin.name + '(' + admin.email + ')',
            verify: 'email-otp',            // 본인확인 수단
            ip: admin.ip
        };

        var history = window.apvLoadHistory();
        history.unshift(rec);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
        return rec;
    };
})();
