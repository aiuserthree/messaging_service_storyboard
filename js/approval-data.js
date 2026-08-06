/* =====================================================================
 * 발송 사후승인 — 공용 데이터·유틸 (보안심사 3.5-④)
 *
 * 심사 항목해설
 *   · 사후승인의 기업관리자는 문자재판매사업자가 아니라 서비스를 이용하는
 *     기업 고객사의 관리자 또는 담당자를 의미한다.
 *   · 사후승인은 전자결재 · 관리자 콘솔 승인 · 이메일 승인 · 서면 결재 등
 *     승인(확인) 사실을 입증할 수 있는 방식으로 제공하면 된다.
 *
 * 톡벨은 이 중 **이메일 승인** 방식을 채택한다.
 *   API·솔루션·모듈 발송 → 기업관리자 이메일로 승인 요청 메일 발송
 *   → 메일의 승인 링크 진입 → **이메일 OTP 인증**으로 본인 확인
 *   → 승인·반려 처리 → 승인 사실을 이력으로 보관
 *
 * 사용 화면
 *   email-approval-request.html  승인 요청 메일 템플릿(증빙용 미리보기)
 *   approval-email.html          메일 링크 진입 · 이메일 OTP 승인
 *   mypage-approval.html         사후승인 관리(대기 · 이력 · 담당자 · 내부통제)
 *
 * 프로토타입: 데이터는 localStorage 기반 데모이며 실제 연동 시 API 로 대체한다.
 *   GET  /api/send-approval/pending             승인 대기 목록
 *   GET  /api/send-approval/request/{token}     메일 링크 토큰으로 승인 대상 조회
 *   POST /api/send-approval/otp/send            승인용 이메일 OTP 발송
 *   POST /api/send-approval/otp/verify          이메일 OTP 검증
 *   POST /api/send-approval/decision            승인·반려 처리(단건/일괄)
 *   POST /api/send-approval/request/resend      승인 요청 메일 재발송
 *   GET  /api/send-approval/history             승인 이력
 *   GET  /api/send-approval/history/export      승인 이력 엑셀
 *   GET/PUT /api/send-approval/control          내부통제·담당자 설정
 * ===================================================================== */

(function () {
    'use strict';

    /* ================= 상수 ================= */

    window.APPROVAL_OVERDUE_HOURS = 24;   // 사후승인 지연 기준
    window.APPROVAL_NOTIFY_HOURS = 4;     // 미확인 알림 기준
    window.APPROVAL_AUDIT_COUNT = 3;      // 반복 미확인 점검 기준(재알림 횟수)
    window.APPROVAL_OTP_MINUTES = 3;      // 이메일 OTP 유효시간
    window.APPROVAL_OTP_MAX_TRY = 5;      // OTP 입력 허용 횟수
    window.APPROVAL_OTP_DEMO = '123456';  // 프로토타입 데모 인증번호

    var PENDING_KEY = 'sendApprovalPending';
    var HISTORY_KEY = 'sendApprovalHistory';
    var CONTROL_KEY = 'sendApprovalControl';

    /* 데모 기업관리자 — 실제 연동 시 GET /api/send-approval/control 의 승인 담당자 정보로 대체 */
    window.APPROVAL_ADMIN = {
        company: '(주)아이뱅크',
        name: '김담당',
        email: 'admin@ibank.co.kr',
        role: '발송 승인·반려',
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

    /* 'YYYY-MM-DD HH:mm' → Date (Safari 호환을 위해 직접 파싱) */
    window.apvParse = function (s) {
        var m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/.exec(s || '');
        if (!m) return new Date(NaN);
        return new Date(+m[1], +m[2] - 1, +m[3], +m[4], +m[5]);
    };

    window.apvHoursSince = function (stamp) {
        return (Date.now() - window.apvParse(stamp).getTime()) / 3600000;
    };

    window.apvElapsed = function (stamp) {
        var h = window.apvHoursSince(stamp);
        if (h < 1) return Math.max(0, Math.floor(h * 60)) + '분';
        if (h < 48) return Math.floor(h) + '시간';
        return Math.floor(h / 24) + '일';
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

    window.apvIsOverdue = function (item) {
        return window.apvHoursSince(item.sentAt) >= window.APPROVAL_OVERDUE_HOURS;
    };

    /* 승인 확인 번호 — 승인(확인) 사실을 입증하는 식별자.
     * 실제 연동 시 서버가 발급하며, 승인 결과 메일·이력에 동일하게 표기된다. */
    window.apvApprovalNo = function (targetId, at) {
        return 'APV-' + String(at).replace(/[^0-9]/g, '').slice(2, 12) + '-' + String(targetId).replace(/[^0-9]/g, '');
    };

    /* ================= 데모 데이터 =================
     * hoursAgo 로 정의해 조회 시점 기준 경과시간이 자연스럽게 계산되도록 한다.
     * 실제 연동 시 GET /api/send-approval/pending 응답의 sentAt 을 그대로 사용.
     */

    var DEMO_PENDING = [
        { id: 'AP-0001', hoursAgo: 31.5, channel: 'API', caller: '02-1234-5678', msgType: '알림톡',
          template: '주문 배송 안내', pattern: 'TPL-DELIV-01', count: 1240, risk: 'high',
          riskReason: '대량 발송(1,000건 초과)', restricted: true, patternApproval: false,
          mailSent: 3, sample: '01012345678',
          content: '[아이뱅크] 고객님이 주문하신 상품이 오늘 출발했습니다.\n· 운송장번호: 1234-5678-9012\n· 배송조회는 아래 버튼을 눌러주세요.' },

        { id: 'AP-0002', hoursAgo: 27.2, channel: '솔루션', caller: '1600-0000', msgType: '광고문자(LMS)',
          template: '8월 정기 프로모션', pattern: 'TPL-PROMO-08', count: 8600, risk: 'high',
          riskReason: '광고성 대량 발송', restricted: true, patternApproval: false,
          mailSent: 2, sample: '01098761234',
          content: '(광고)[아이뱅크] 8월 정기 프로모션 안내\n최대 30% 할인 쿠폰이 발급되었습니다.\n무료거부 080-123-4567' },

        { id: 'AP-0003', hoursAgo: 25.1, channel: 'API', caller: '02-1234-5678', msgType: '알림톡',
          template: '결제 완료 안내', pattern: 'TPL-PAY-01', count: 412, risk: 'normal',
          riskReason: '', restricted: false, patternApproval: true,
          mailSent: 2, sample: '01055557777',
          content: '[아이뱅크] 결제가 정상 처리되었습니다.\n· 결제금액: 32,000원\n· 결제수단: 신용카드' },

        { id: 'AP-0004', hoursAgo: 9.8, channel: 'API', caller: '02-1234-5678', msgType: '일반문자(SMS)',
          template: '본인확인 인증번호', pattern: 'TPL-AUTH-01', count: 3182, risk: 'normal',
          riskReason: '', restricted: false, patternApproval: true,
          mailSent: 1, sample: '01033334444',
          content: '[아이뱅크] 인증번호 [123456] 을 입력해주세요.' },

        { id: 'AP-0005', hoursAgo: 6.4, channel: '모듈', caller: '1600-0000', msgType: '알림톡',
          template: '결제 완료 안내', pattern: 'TPL-PAY-01', count: 197, risk: 'normal',
          riskReason: '', restricted: false, patternApproval: true,
          mailSent: 1, sample: '01077778888',
          content: '[아이뱅크] 결제가 정상 처리되었습니다.\n· 결제금액: 15,900원\n· 결제수단: 계좌이체' },

        { id: 'AP-0006', hoursAgo: 5.1, channel: '솔루션', caller: '010-1234-5678', msgType: '일반문자(SMS)',
          template: '예약 확정 안내', pattern: 'TPL-RSV-01', count: 86, risk: 'normal',
          riskReason: '', restricted: false, patternApproval: false,
          mailSent: 1, sample: '01022221111',
          content: '[아이뱅크] 8월 12일 14:00 상담 예약이 확정되었습니다.' },

        { id: 'AP-0007', hoursAgo: 2.3, channel: 'API', caller: '02-1234-5678', msgType: '일반문자(SMS)',
          template: '본인확인 인증번호', pattern: 'TPL-AUTH-01', count: 1547, risk: 'normal',
          riskReason: '', restricted: false, patternApproval: true,
          mailSent: 1, sample: '01099998888',
          content: '[아이뱅크] 인증번호 [123456] 을 입력해주세요.' },

        { id: 'AP-0008', hoursAgo: 0.7, channel: 'API', caller: '1600-0000', msgType: '광고문자(MMS)',
          template: '신규 서비스 오픈 안내', pattern: 'TPL-PROMO-09', count: 2400, risk: 'high',
          riskReason: '광고성 대량 발송', restricted: false, patternApproval: false,
          mailSent: 1, sample: '01044445555',
          content: '(광고)[아이뱅크] 신규 서비스가 오픈했습니다.\n지금 가입하면 첫 달 무료!\n무료거부 080-123-4567' }
    ];

    var DEMO_HISTORY_SEED = [
        { hoursAgo: 3,   decision: 'approve', target: 'AP-0101', channel: 'API',    template: '결제 완료 안내',    pattern: 'TPL-PAY-01',   count: 508,  method: 'bulk',   reason: '정형 안내 메시지 패턴 일괄 승인' },
        { hoursAgo: 5,   decision: 'approve', target: 'AP-0102', channel: 'API',    template: '본인확인 인증번호', pattern: 'TPL-AUTH-01',  count: 2914, method: 'bulk',   reason: '인증번호 발송 패턴 일괄 승인' },
        { hoursAgo: 21,  decision: 'reject',  target: 'AP-0103', channel: '솔루션', template: '7월 프로모션',      pattern: 'TPL-PROMO-07', count: 9120, method: 'single', reason: '수신동의 확보 근거 미제출 — 재확인 후 재발송 요청' },
        { hoursAgo: 27,  decision: 'approve', target: 'AP-0104', channel: '모듈',   template: '주문 배송 안내',    pattern: 'TPL-DELIV-01', count: 743,  method: 'single', reason: '발송 내용·건수 확인 완료' },
        { hoursAgo: 49,  decision: 'approve', target: 'AP-0105', channel: 'API',    template: '예약 확정 안내',    pattern: 'TPL-RSV-01',   count: 122,  method: 'single', reason: '' },
        { hoursAgo: 74,  decision: 'reject',  target: 'AP-0106', channel: 'API',    template: '이벤트 당첨 안내',  pattern: 'TPL-EVT-02',   count: 4300, method: 'single', reason: '사전 협의되지 않은 발신번호 사용' },
        { hoursAgo: 122, decision: 'approve', target: 'AP-0107', channel: '솔루션', template: '결제 완료 안내',    pattern: 'TPL-PAY-01',   count: 331,  method: 'bulk',   reason: '정형 안내 메시지 패턴 일괄 승인' }
    ];

    function demoPending() {
        return DEMO_PENDING.map(function (p) {
            var item = {};
            Object.keys(p).forEach(function (k) { item[k] = p[k]; });
            item.sentAt = window.apvStamp(new Date(Date.now() - p.hoursAgo * 3600000));
            delete item.hoursAgo;
            return item;
        });
    }

    function demoHistory() {
        var admin = window.APPROVAL_ADMIN;
        return DEMO_HISTORY_SEED.map(function (s) {
            var at = window.apvStamp(new Date(Date.now() - s.hoursAgo * 3600000));
            return {
                at: at, decision: s.decision, target: s.target, channel: s.channel,
                template: s.template, pattern: s.pattern, count: s.count, method: s.method,
                actor: admin.name + '(' + admin.email + ')', reason: s.reason, ip: admin.ip,
                verify: 'email-otp',                       // 본인확인 수단
                approvalNo: window.apvApprovalNo(s.target, at)
            };
        });
    }

    /* ================= 저장소 ================= */

    window.apvLoadPending = function () {
        try {
            var saved = JSON.parse(localStorage.getItem(PENDING_KEY));
            if (Array.isArray(saved)) return saved;
        } catch (e) {}
        var fresh = demoPending();
        localStorage.setItem(PENDING_KEY, JSON.stringify(fresh));
        return fresh;
    };

    window.apvSavePending = function (list) { localStorage.setItem(PENDING_KEY, JSON.stringify(list)); };

    window.apvLoadHistory = function () {
        try {
            var saved = JSON.parse(localStorage.getItem(HISTORY_KEY));
            if (Array.isArray(saved)) return saved;
        } catch (e) {}
        var fresh = demoHistory();
        localStorage.setItem(HISTORY_KEY, JSON.stringify(fresh));
        return fresh;
    };

    window.apvSaveHistory = function (list) { localStorage.setItem(HISTORY_KEY, JSON.stringify(list)); };

    window.apvLoadControl = function () {
        try {
            var saved = JSON.parse(localStorage.getItem(CONTROL_KEY));
            if (saved && typeof saved === 'object') return saved;
        } catch (e) {}
        return { notify: true, renotify: true, audit: true, restrict: true };
    };

    window.apvSaveControl = function (c) { localStorage.setItem(CONTROL_KEY, JSON.stringify(c)); };

    /* ================= 승인 인증 세션 =================
     * 이메일 OTP 로 담당자 본인 확인을 마치면 30분간 유효하다.
     * 발송 화면의 재인증 세션(getSendAuthState)은 발신번호 소유 확인이 목적이라
     * 발신번호가 바뀌면 재인증하지만, 승인 세션은 "담당자 본인 확인"이 목적이므로
     * 발신번호와 무관하게 30분간 유지한다.
     *
     * 프로토타입: sessionStorage 기반. 실제 연동 시 서버 세션으로 대체한다.
     */
    var APPROVAL_AUTH_KEY = 'approvalOtpAuthAt';

    window.APPROVAL_AUTH_VALID_MINUTES = 30;

    window.apvMarkApprovalAuth = function () {
        sessionStorage.setItem(APPROVAL_AUTH_KEY, String(Date.now()));
    };

    window.apvApprovalAuthState = function () {
        var at = Number(sessionStorage.getItem(APPROVAL_AUTH_KEY) || 0);
        if (!at) return { required: true, reason: '' };

        var elapsedMin = (Date.now() - at) / 60000;
        if (elapsedMin >= window.APPROVAL_AUTH_VALID_MINUTES) {
            return {
                required: true,
                reason: '인증 유효시간(' + window.APPROVAL_AUTH_VALID_MINUTES + '분)이 지나 다시 인증이 필요합니다.'
            };
        }
        return {
            required: false,
            remainMin: Math.max(1, Math.ceil(window.APPROVAL_AUTH_VALID_MINUTES - elapsedMin))
        };
    };

    /* ================= 승인 처리 =================
     * 이메일 OTP 로 본인 확인을 마친 뒤에만 호출한다.
     * 실제 연동 시 POST /api/send-approval/decision 으로 대체.
     */
    window.apvApplyDecision = function (targetIds, decision, reason, verify) {
        var pending = window.apvLoadPending();
        var targets = pending.filter(function (p) { return targetIds.indexOf(p.id) >= 0; });
        if (!targets.length) return [];

        var admin = window.APPROVAL_ADMIN;
        var history = window.apvLoadHistory();
        var method = targets.length > 1 ? 'bulk' : 'single';
        var at = window.apvNow();
        var records = [];

        targets.forEach(function (p) {
            var rec = {
                at: at, decision: decision, target: p.id, channel: p.channel,
                template: p.template, pattern: p.pattern, count: p.count, method: method,
                actor: admin.name + '(' + admin.email + ')', reason: reason, ip: admin.ip,
                verify: verify || 'email-otp',
                approvalNo: window.apvApprovalNo(p.id, at)
            };
            records.push(rec);
            history.unshift(rec);
        });

        window.apvSavePending(pending.filter(function (p) { return targetIds.indexOf(p.id) < 0; }));
        window.apvSaveHistory(history);
        return records;
    };

    /* 발송 화면에서 이메일 OTP 인증이 통과했을 때 승인 사실을 이력에 남긴다.
     * 대기 큐를 거치지 않고 발송 시점에 바로 승인된 건이므로 method='send-time'.
     * 실제 연동 시 POST /api/send-approval/decision 응답으로 대체한다. */
    window.apvRecordSendApproval = function (info) {
        info = info || {};
        var admin = window.APPROVAL_ADMIN;
        var at = window.apvNow();
        var seq = String(Date.now()).slice(-4);
        var target = 'SD-' + window.apvDateOnly(new Date()).replace(/-/g, '').slice(2) + '-' + seq;

        var rec = {
            at: at,
            decision: 'approve',
            target: target,
            channel: info.channel || '웹 발송',
            template: info.template || '직접 작성',
            pattern: info.pattern || '-',
            count: Number(info.count || 0),
            method: 'send-time',
            actor: admin.name + '(' + admin.email + ')',
            reason: '발송 시 이메일 OTP 인증으로 승인',
            ip: admin.ip,
            verify: 'email-otp',
            caller: info.caller || '-',
            approvalNo: window.apvApprovalNo(seq, at)
        };

        var history = window.apvLoadHistory();
        history.unshift(rec);
        window.apvSaveHistory(history);
        return rec;
    };
})();
