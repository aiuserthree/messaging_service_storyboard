/**
 * 금칙어 등 차단 체계(스팸 필터링) — 발송 화면 공용
 *
 * 전송자격인증제 인증기준 5.2 대응.
 * 문자 발송을 요청받은 시점에 내용에 포함된 위험 요소를 탐지해 발송을 차단하거나 보류한다.
 *
 * ── 차단정보 ───────────────────────────────────────────────
 *   금칙어(단어) / URL·도메인 / 전화번호 3종.
 *   자체 등록분과 한국인터넷진흥원 등 외부기관에서 공유받은 정보로 구성하며,
 *   어드민 > 스팸·제재 관리 > 차단정보(금칙어) 관리에서 운영한다.
 *
 * ── 판정 ───────────────────────────────────────────────────
 *   1) 다중 조합 규칙(차단정보 2개 이상 AND)에 걸리면 규칙의 조치를 적용한다.
 *   2) 걸리지 않으면 개별 차단정보의 조치 중 가장 강한 값을 적용한다. block > hold
 *
 *   block(즉시 차단) — 발송을 중단하고 금칙어가 포함되어 차단되었음을 이용자에게 알린다.
 *   hold(보류)       — 오탐 가능성이 있는 건. 기업 고객사 승인 담당자에게 검토를 요청하고
 *                      승인되면 전송, 반려되면 차단으로 확정한다.
 *
 * ── 보류 건 승인 ───────────────────────────────────────────
 *   문자 발송의 사후승인(3.5-④)과 **동일한 이메일 OTP 인증 모듈**을 그대로 쓴다.
 *   js/alimtalk-auth.js 의 openEmailOtpAuth() — 승인 담당자 이메일 확인 → 인증번호 받기 →
 *   6자리 입력, 유효시간 3분 / 5회 초과 시 잠금 / 재전송 규칙까지 발송 승인과 같다.
 *   보류로 판정되면 별도 안내 화면 없이 이 인증 모달을 바로 띄운다.
 *   별도의 승인 대기 큐·승인 콘솔 화면은 두지 않으며, 승인 사실은 이력으로 보관한다.
 *
 *   담당자가 메시지 내용을 확인하고 승인한 것이므로 발송 사후승인도 함께 성립한 것으로 보고,
 *   이어지는 발송 단계에서 사후승인을 다시 요구하지 않는다(발신번호 소유 확인용
 *   발송 추가 인증은 발송자 본인이 하는 절차이므로 그대로 수행한다).
 *   인증번호를 입력하지 않고 닫으면 보류 상태가 유지되고 발송되지 않는다(반려).
 *
 * ── 사용법 ─────────────────────────────────────────────────
 *   screenSendContent({
 *       content: '본문',
 *       title: '제목',            // 선택
 *       caller: '02-1234-5678',   // 발신번호
 *       count: 320,               // 발송 건수
 *       msgType: '일반문자(SMS)'
 *   }, function () {
 *       // 탐지되지 않았을 때만 호출된다 — 이후 발송 인증 단계로 진행
 *   });
 *
 * 프로토타입: 탐지는 클라이언트에서 수행하고 이력은 localStorage 에 남긴다.
 * 실제 연동 시 발송 요청 API 가 서버에서 판정하고 아래 응답으로 대체한다.
 *   POST /api/send/screen             발송 요청 시점 차단정보 탐지
 *   POST /api/send/hold/{id}/request  보류 건 검토 요청 메일·인증번호 발송
 *   POST /api/send/hold/{id}/approve  인증번호 검증 후 보류 해제(승인) 기록
 *   GET  /api/send/hold/{id}          보류 건 처리 결과 조회
 */
(function () {
    'use strict';

    /* ================= 차단정보 ================= */

    /* 어드민 차단정보 관리와 동일한 목록. 실제로는 서버가 보유한다. */
    var BLOCK_ITEMS = [
        { type: 'word',  value: '도박',         action: 'block', note: '불법 사행성' },
        { type: 'word',  value: '카지노',       action: 'block', note: '불법 사행성' },
        { type: 'word',  value: '토토',         action: 'block', note: '불법 사행성' },
        { type: 'word',  value: '불법대출',     action: 'block', note: '미등록 대부업' },
        { type: 'word',  value: '신용조회없이', action: 'block', note: '미등록 대부업' },
        { type: 'word',  value: '몸캠',         action: 'block', note: '불법 성인물' },
        { type: 'word',  value: '작업대출',     action: 'block', note: '금융사기' },
        { type: 'word',  value: '무료',         action: 'hold',  note: '광고 상용구' },
        { type: 'word',  value: '당첨',         action: 'hold',  note: '광고 상용구' },
        { type: 'word',  value: '수익보장',     action: 'hold',  note: '투자 유인 문구' },
        { type: 'word',  value: '원금보장',     action: 'hold',  note: '투자 유인 문구' },
        { type: 'word',  value: '지금바로클릭', action: 'hold',  note: '피싱 유도 문구' },
        { type: 'url',   value: 'bit.ly',       action: 'hold',  note: '단축 URL' },
        { type: 'url',   value: 'me2.do',       action: 'hold',  note: '단축 URL' },
        { type: 'url',   value: 'free-money.top',  action: 'block', note: '피싱 신고 도메인' },
        { type: 'url',   value: 'win-lotto.xyz',   action: 'block', note: '불법 사행성 도메인' },
        { type: 'url',   value: 'cash-loan.click', action: 'block', note: '불법 대부 도메인' },
        { type: 'phone', value: '070-1234-5678', action: 'block', note: '스팸 신고 다발 번호' },
        { type: 'phone', value: '070-9999-0000', action: 'block', note: '보이스피싱 신고 번호' }
    ];

    /* 다중 조합 규칙 — any:true 는 해당 유형의 차단정보가 하나라도 탐지된 경우를 뜻한다.
     * 단독으로는 보류 수준인 항목도 조합으로 탐지되면 즉시 차단으로 상향한다. */
    var RULES = [
        { id: 'R01', name: '도박 유인 조합', action: 'block',
          conditions: [{ type: 'word', value: '당첨' }, { type: 'url', any: true }] },
        { id: 'R02', name: '불법 대부 조합', action: 'block',
          conditions: [{ type: 'word', value: '무료' }, { type: 'word', value: '수익보장' }, { type: 'phone', any: true }] },
        { id: 'R03', name: '피싱 유도 조합', action: 'block',
          conditions: [{ type: 'word', value: '지금바로클릭' }, { type: 'url', any: true }] },
        { id: 'R04', name: '투자 리딩 조합', action: 'hold',
          conditions: [{ type: 'word', value: '원금보장' }, { type: 'word', value: '수익보장' }] }
    ];

    var TYPE_LABEL = { word: '금칙어', url: 'URL·도메인', phone: '전화번호' };

    var HISTORY_KEY = 'spamDetectionHistory';

    /* ================= 탐지 ================= */

    function escapeHtml(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    /* 전화번호는 하이픈·공백 표기가 달라도 같은 번호로 본다 */
    function digitsOnly(s) { return String(s || '').replace(/\D/g, ''); }

    function detect(text) {
        var lower = String(text || '').toLowerCase();
        var digits = digitsOnly(text);
        var matched = [];

        BLOCK_ITEMS.forEach(function (item) {
            var hit = item.type === 'phone'
                ? digits.indexOf(digitsOnly(item.value)) !== -1
                : lower.indexOf(item.value.toLowerCase()) !== -1;
            if (hit) matched.push({ type: item.type, value: item.value, action: item.action, note: item.note });
        });

        return matched;
    }

    function ruleSatisfied(rule, matched) {
        return rule.conditions.every(function (c) {
            return matched.some(function (m) {
                if (m.type !== c.type) return false;
                return c.any ? true : m.value === c.value;
            });
        });
    }

    /* 탐지 결과 → 조치 판정 */
    function judge(matched) {
        if (!matched.length) return { action: 'pass', matched: matched, rule: null };

        var hitRule = null;
        RULES.some(function (r) {
            if (ruleSatisfied(r, matched)) { hitRule = r; return true; }
            return false;
        });

        if (hitRule) return { action: hitRule.action, matched: matched, rule: hitRule };

        var hasBlock = matched.some(function (m) { return m.action === 'block'; });
        return { action: hasBlock ? 'block' : 'hold', matched: matched, rule: null };
    }

    /* ================= 이력 ================= */

    function pad2(n) { return ('0' + n).slice(-2); }

    function nowStamp() {
        var d = new Date();
        return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()) + ' ' +
               pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds());
    }

    var idSeq = 0;

    function detectionId() {
        var d = new Date();
        idSeq += 1;
        return 'D-' + d.getFullYear() + pad2(d.getMonth() + 1) + pad2(d.getDate()) +
               '-' + String(Date.now()).slice(-4) + pad2(idSeq % 100);
    }

    /* 탐지·조치 결과를 이력으로 남긴다 — 어드민 탐지·차단 결과 로그와 같은 항목.
     * 실제 연동 시 서버가 적재하며 사후 점검·소명 대응 근거자료가 된다. */
    /* 같은 내용·발신번호로 다시 발송을 시도하면 새 건을 만들지 않고
     * 아직 승인 대기 중인 기존 보류 건을 이어서 처리한다. */
    function findPendingRecord(ctx) {
        var list = window.spfLoadHistory();
        for (var i = 0; i < list.length; i++) {
            if (list[i].holdStatus === 'pending' &&
                list[i].content === (ctx.content || '') &&
                list[i].caller === (ctx.caller || '-')) {
                return list[i];
            }
        }
        return null;
    }

    function record(verdict, ctx) {
        var rec = {
            id: detectionId(),
            at: nowStamp(),
            msgType: ctx.msgType || '-',
            caller: ctx.caller || '-',
            count: Number(ctx.count || 0),
            content: ctx.content || '',
            matched: verdict.matched.map(function (m) { return { type: m.type, value: m.value }; }),
            rule: verdict.rule ? (verdict.rule.id + ' ' + verdict.rule.name) : '-',
            action: verdict.action,
            holdStatus: verdict.action === 'hold' ? 'pending' : null
        };
        try {
            var list = JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
            list.unshift(rec);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(list));
        } catch (e) {}
        return rec;
    }

    window.spfLoadHistory = function () {
        try {
            var saved = JSON.parse(localStorage.getItem(HISTORY_KEY));
            if (Array.isArray(saved)) return saved;
        } catch (e) {}
        return [];
    };

    /* 이메일 OTP 인증이 통과했을 때 보류 해제(승인) 사실을 이력에 반영한다.
     * 승인번호·처리자·본인확인 수단·접속 IP 를 함께 남겨 승인 사실을 입증한다.
     * 실제 연동 시 POST /api/send/hold/{id}/approve 로 대체한다. */
    function recordHoldApproval(detectionId) {
        var admin = (typeof APPROVAL_ADMIN !== 'undefined') ? APPROVAL_ADMIN : {};
        var at = nowStamp();
        var approvalNo = (typeof apvApprovalNo === 'function')
            ? apvApprovalNo(String(Date.now()).slice(-4), at)
            : 'APV-' + String(Date.now()).slice(-10);

        var decision = {
            holdStatus: 'approved',
            approvalNo: approvalNo,
            approver: (admin.name || '승인 담당자') + '(' + (admin.email || '-') + ')',
            decidedAt: at,
            verify: 'email-otp',
            decisionReason: '승인 담당자가 메시지 내용을 확인하고 승인 — 오탐',
            decidedIp: admin.ip || '-'
        };

        try {
            var list = window.spfLoadHistory();
            for (var i = 0; i < list.length; i++) {
                if (list[i].id === detectionId) {
                    Object.keys(decision).forEach(function (k) { list[i][k] = decision[k]; });
                    break;
                }
            }
            localStorage.setItem(HISTORY_KEY, JSON.stringify(list));
        } catch (e) {}

        return decision;
    }

    /* ================= 화면 ================= */

    function injectStyles() {
        if (document.getElementById('spamFilterStyles')) return;
        var style = document.createElement('style');
        style.id = 'spamFilterStyles';
        style.textContent = [
            '.spf-overlay{display:none;position:fixed;inset:0;z-index:2200;background:rgba(15,23,42,0.45);align-items:center;justify-content:center;padding:24px;}',
            '.spf-overlay.is-open{display:flex;}',
            '.spf-box{background:#fff;border-radius:16px;max-width:520px;width:100%;padding:36px 36px 28px;box-shadow:0 8px 32px rgba(15,23,42,0.12);max-height:90vh;overflow-y:auto;}',
            /* 헤더 */
            '.spf-icon{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;}',
            '.spf-icon svg{width:28px;height:28px;}',
            '.spf-icon.block{background:#fee2e2;color:#dc2626;}',
            '.spf-icon.hold{background:#fef3c7;color:#b45309;}',
            '.spf-box h2{font-size:22px;font-weight:800;color:#0f172a;text-align:center;margin-bottom:10px;line-height:1.4;letter-spacing:-0.02em;}',
            '.spf-subtitle{font-size:14px;color:#64748b;text-align:center;line-height:1.7;margin-bottom:22px;}',
            '.spf-subtitle strong{color:#0f172a;font-weight:700;}',
            /* 탐지 결과 */
            '.spf-label{font-size:13px;font-weight:700;color:#334155;margin-bottom:8px;}',
            '.spf-detected{border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;padding:14px 16px;margin-bottom:16px;}',
            '.spf-chip{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:6px;font-size:13px;font-weight:700;margin:3px 4px 3px 0;}',
            '.spf-chip .t{font-size:11px;font-weight:600;opacity:0.75;}',
            '.spf-chip.word{background:#fef3c7;color:#92400e;}',
            '.spf-chip.url{background:#dbeafe;color:#1e40af;}',
            '.spf-chip.phone{background:#e2e8f0;color:#475569;}',
            '.spf-rule{margin-top:10px;padding-top:10px;border-top:1px dashed #e2e8f0;font-size:12px;color:#64748b;line-height:1.6;}',
            '.spf-rule strong{color:#334155;font-weight:700;}',
            /* 메시지 원문 */
            '.spf-content{border:1px solid #e2e8f0;border-radius:10px;padding:13px 15px;font-size:13px;line-height:1.85;color:#334155;background:#fff;word-break:break-all;max-height:130px;overflow-y:auto;margin-bottom:16px;}',
            '.spf-mark{padding:1px 3px;border-radius:3px;font-weight:800;background:#fef3c7;color:#92400e;}',
            '.spf-mark.url{background:#dbeafe;color:#1e40af;}',
            '.spf-mark.phone{background:#e2e8f0;color:#334155;}',
            /* 안내 */
            '.spf-notice{border-radius:10px;padding:14px 16px;font-size:13px;line-height:1.75;margin-bottom:4px;}',
            '.spf-notice.block{background:#fef2f2;border:1px solid #fecaca;color:#991b1b;}',
            '.spf-notice.hold{background:#fffbeb;border:1px solid #fde68a;color:#92400e;}',
            '.spf-notice strong{font-weight:800;}',
            '.spf-meta{margin-top:14px;font-size:12px;color:#94a3b8;text-align:center;line-height:1.7;}',
            /* 버튼 */
            '.spf-actions{display:flex;gap:10px;margin-top:22px;}',
            '.spf-btn{flex:1;padding:14px 16px;border-radius:8px;font-size:15px;font-weight:700;border:none;cursor:pointer;font-family:inherit;transition:background .2s,color .2s;}',
            '.spf-btn-primary{background:#5cb82e;color:#fff;}',
            '.spf-btn-primary:hover{background:#4a9a24;}',
            '.spf-btn-cancel{background:#fff;color:#475569;border:1px solid #dde3ea;}',
            '.spf-btn-cancel:hover{background:#f8fafc;}',
            '.spf-footnote{margin-top:16px;text-align:center;font-size:12px;color:#94a3b8;}',
            '.spf-footnote a{color:#5cb82e;font-weight:600;text-decoration:none;}'
        ].join('\n');
        document.head.appendChild(style);
    }

    var ICON_BLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/></svg>';
    var ICON_HOLD  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5l3 2"/></svg>';

    var mounted = false;

    /* 현재 안내 중인 탐지 건 — 보류 승인 시 어느 건을 해제할지 판단하는 데 쓴다 */
    var pending = null;   // { verdict, ctx, rec, onPass }

    function mount() {
        if (mounted) return;
        injectStyles();

        var wrap = document.createElement('div');
        wrap.innerHTML = [
            '<div class="spf-overlay" id="spamFilterModal" role="dialog" aria-modal="true" aria-labelledby="spfTitle">',
            '  <div class="spf-box">',
            '    <div class="spf-icon block" id="spfIcon"></div>',
            '    <h2 id="spfTitle">발송이 차단되었습니다</h2>',
            '    <p class="spf-subtitle" id="spfSubtitle"></p>',
            '    <div class="spf-label">탐지된 차단정보</div>',
            '    <div class="spf-detected">',
            '      <div id="spfChips"></div>',
            '      <div class="spf-rule" id="spfRule" style="display:none;"></div>',
            '    </div>',
            '    <div class="spf-label">메시지 내용</div>',
            '    <div class="spf-content" id="spfContent"></div>',
            '    <div class="spf-notice block" id="spfNotice"></div>',
            '    <div class="spf-meta" id="spfMeta"></div>',
            '    <div class="spf-actions">',
            '      <button type="button" class="spf-btn spf-btn-cancel" id="spfCloseBtn">내용 수정하기</button>',
            '      <button type="button" class="spf-btn spf-btn-primary" id="spfActionBtn">문의하기</button>',
            '    </div>',
            '    <p class="spf-footnote" id="spfFootnote"></p>',
            '  </div>',
            '</div>'
        ].join('');
        document.body.appendChild(wrap.firstChild);

        document.getElementById('spfCloseBtn').addEventListener('click', close);
        document.getElementById('spfActionBtn').addEventListener('click', function () {
            window.location.href = 'support-inquiry.html';
        });
        document.getElementById('spamFilterModal').addEventListener('click', function (e) {
            if (e.target === this) close();
        });

        mounted = true;
    }

    function close() {
        var el = document.getElementById('spamFilterModal');
        if (el) el.classList.remove('is-open');
    }

    /* ================= 보류 건 승인 (이메일 OTP) =================
     * 문자 발송의 사후승인(3.5-④)과 **동일한 인증 모듈**을 그대로 사용한다.
     *   js/alimtalk-auth.js 의 openEmailOtpAuth()
     *   → 승인 담당자 이메일 확인 → 인증번호 받기 → 6자리 입력
     *   → 유효시간 3분 / 5회 초과 시 잠금 / 재전송 규칙 모두 동일
     * 보류로 판정되면 안내 팝업 없이 이 인증 모달을 바로 띄운다.
     * 통과하면 보류가 해제되어 발송되고, 취소하면 보류가 유지되어 발송되지 않는다.
     * 실제 연동 시 POST /api/send/hold/{id}/request, /approve 로 대체한다. */
    function requestHoldApproval() {
        if (!pending) return;
        if (typeof openEmailOtpAuth !== 'function') {
            if (typeof showToast === 'function') showToast('승인 인증 모듈을 불러오지 못했습니다.', 'error');
            return;
        }

        var verdict = pending.verdict;
        var ctx = pending.ctx;
        var rec = pending.rec;
        var onPass = pending.onPass;
        var email = (typeof APPROVAL_ADMIN !== 'undefined' && APPROVAL_ADMIN.email)
            ? APPROVAL_ADMIN.email : '';

        var ruleNote = verdict.rule
            ? '<br>적용 규칙 ' + verdict.rule.id + ' ' + verdict.rule.name
            : '';

        openEmailOtpAuth({
            title: '발송 보류 검토 승인',
            description: '차단정보가 탐지되어 <strong>발송이 보류</strong>되었습니다.<br>' +
                         '승인 담당자 이메일로 검토 요청과 인증번호를 보내드립니다.',
            confirmText: '승인하고 발송하기',
            channelNote: '탐지 내역과 메시지 원문이 담긴 검토 요청 메일과 함께 6자리 인증번호가 발송됩니다.',
            linkHelp: '탐지된 차단정보 ' + chipsHtml(verdict.matched) + ruleNote +
                      '<br>담당자가 내용을 확인하고 승인해야 발송되며, 승인하지 않으면 발송되지 않습니다.',
            email: email,
            callerNumber: ctx.caller || '-',
            onSuccess: function () {
                var decision = recordHoldApproval(rec.id);

                // 담당자가 내용을 확인하고 승인했으므로 발송 사후승인도 함께 성립한 것으로 본다.
                // 이후 발송 단계에서 사후승인을 다시 요구하지 않는다.
                if (typeof apvMarkApprovalAuth === 'function') apvMarkApprovalAuth();
                if (typeof apvRecordSendApproval === 'function') {
                    apvRecordSendApproval({
                        channel: '웹 발송 (보류 검토 승인)',
                        caller: ctx.caller || '-',
                        msgType: ctx.msgType || '-',
                        count: ctx.count || 0
                    });
                }

                pending = null;
                if (typeof showToast === 'function') {
                    showToast('보류가 해제되었습니다. (승인번호 ' + decision.approvalNo + ')', 'success');
                }
                if (typeof onPass === 'function') onPass();
            },
            onCancel: function () {
                // 승인하지 않으면 보류 상태가 유지되고 발송되지 않는다
                if (typeof showToast === 'function') {
                    showToast('승인되지 않아 발송이 보류 상태로 유지됩니다.', 'warning');
                }
            }
        });
    }

    function chipsHtml(matched) {
        return matched.map(function (m) {
            return '<span class="spf-chip ' + m.type + '">' +
                   '<span class="t">' + TYPE_LABEL[m.type] + '</span>' + escapeHtml(m.value) + '</span>';
        }).join('');
    }

    function highlight(content, matched) {
        var html = escapeHtml(content);
        matched.forEach(function (m) {
            if (m.type === 'phone') return;   // 표기가 달라질 수 있어 번호는 강조하지 않는다
            var safe = escapeHtml(m.value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            html = html.replace(new RegExp(safe, 'gi'), function (hit) {
                return '<mark class="spf-mark ' + m.type + '">' + hit + '</mark>';
            });
        });
        return html;
    }

    /* 즉시 차단 안내 — 보류는 이 화면 없이 바로 승인 인증 모달로 넘어간다 */
    function render(verdict, ctx, rec) {
        mount();

        document.getElementById('spfIcon').className = 'spf-icon block';
        document.getElementById('spfIcon').innerHTML = ICON_BLOCK;
        document.getElementById('spfTitle').textContent = '금칙어가 포함되어 발송이 차단되었습니다';
        document.getElementById('spfSubtitle').innerHTML =
            '메시지 내용에서 <strong>차단 대상 정보</strong>가 확인되어<br>발송이 중단되었습니다.';

        document.getElementById('spfChips').innerHTML = chipsHtml(verdict.matched);

        var ruleEl = document.getElementById('spfRule');
        if (verdict.rule) {
            ruleEl.style.display = '';
            ruleEl.innerHTML = '<strong>적용 규칙</strong> ' + verdict.rule.id + ' ' + verdict.rule.name +
                ' — 차단정보 ' + verdict.rule.conditions.length + '개가 함께 확인되어 조치가 상향되었습니다.';
        } else {
            ruleEl.style.display = 'none';
        }

        document.getElementById('spfContent').innerHTML = highlight(ctx.content || '', verdict.matched);

        var notice = document.getElementById('spfNotice');
        notice.className = 'spf-notice block';
        notice.innerHTML =
            '<strong>발송이 취소되었습니다.</strong> 해당 표현을 수정한 뒤 다시 시도해 주세요.<br>' +
            '정상적인 문구인데 차단되었다면 1:1 문의로 소명해 주시면 검토 후 처리해 드립니다.';

        document.getElementById('spfMeta').innerHTML =
            '탐지번호 ' + rec.id + ' · ' + rec.at + ' · ' + (ctx.msgType || '-') +
            ' · 발송 예정 ' + Number(ctx.count || 0).toLocaleString('ko-KR') + '건';

        document.getElementById('spfFootnote').innerHTML =
            '차단 기준이 궁금하신가요? <a href="support-faq.html">FAQ 보기</a>';

        document.getElementById('spfCloseBtn').textContent = '내용 수정하기';
        document.getElementById('spfActionBtn').textContent = '문의하기';

        document.getElementById('spamFilterModal').classList.add('is-open');
    }

    /* ================= 공개 API ================= */

    /* 발송 요청 시점 차단정보 검사.
     * 탐지되지 않았을 때만 onPass 를 호출하고, 차단·보류면 안내 화면을 띄운다. */
    window.screenSendContent = function (ctx, onPass) {
        ctx = ctx || {};
        var text = [ctx.title || '', ctx.content || ''].join(' ');
        var verdict = judge(detect(text));

        if (verdict.action === 'pass') {
            pending = null;
            if (typeof onPass === 'function') onPass();
            return verdict;
        }

        // 보류는 같은 건을 다시 시도한 것이면 기존 승인 대기 건을 이어서 처리한다
        var rec = (verdict.action === 'hold' && findPendingRecord(ctx)) || record(verdict, ctx);

        // 보류는 승인 후 발송을 이어가야 하므로 onPass 를 들고 있는다
        pending = { verdict: verdict, ctx: ctx, rec: rec, onPass: onPass };

        if (verdict.action === 'hold') {
            // 문자 발송의 사후승인과 동일한 이메일 OTP 인증으로 바로 진입한다
            requestHoldApproval();
        } else {
            render(verdict, ctx, rec);
        }
        return verdict;
    };

    /* 판정만 필요할 때 (미리보기·검증용) */
    window.screenSendContentDryRun = function (text) {
        return judge(detect(text));
    };

    window.closeSpamFilterModal = close;
    window.mountSpamFilter = mount;
    window.SPF_BLOCK_ITEMS = BLOCK_ITEMS;
    window.SPF_RULES = RULES;

    /* 화면설계 오버레이는 첫 토글 시점에 마커를 한 번만 만든다.
     * 그 전에 모달이 DOM 에 없으면 차단 안내 항목 마커가 누락되므로 미리 올려둔다. */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', mount);
    } else {
        mount();
    }
})();
