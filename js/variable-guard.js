/**
 * 치환 변수 화이트리스트 검증 — 발송·템플릿 화면 공용
 *
 * 메시지 본문에 쓸 수 있는 변수는 변수 삽입 버튼으로 제공하는 값으로만 한정한다.
 * 임의 변수명(#{주문번호}, #{송장번호} 등)은 수신자 표에 대응하는 컬럼이 없어
 * 발송 시 치환되지 않고 그대로 나가므로 입력 단계에서 막는다.
 *
 * ── 허용 변수 ──────────────────────────────────────────────
 *   #{이름} #{전화번호} #{변수1} ~ #{변수8}
 *   수신자 표의 컬럼과 1:1로 대응하며, 변수 항목명은 고정이라 이용자가 바꿀 수 없다.
 *
 * ── 사용법 ─────────────────────────────────────────────────
 *   초기화는 자동이다. DOMContentLoaded 시점에 #messageContent 를 찾아
 *   input 이벤트로 검증하고, 바로 아래에 경고 영역을 만들어 붙인다.
 *   다른 입력 요소를 함께 검증하려면 명시적으로 등록한다.
 *
 *       guardVariableInput(document.getElementById('emphasisText'));
 *
 *   발송·저장 직전에 확인할 때는 아래를 쓴다. 허용되지 않은 변수가 있으면
 *   false 를 반환하고 경고를 띄운다.
 *
 *       if (!assertAllowedVariables(content)) return;
 */
(function (global) {
    'use strict';

    var MAX_INDEX = 8;

    /** 허용 변수 목록 — 변수 삽입 버튼과 동일하게 유지한다 */
    function allowedVariables() {
        var list = ['이름', '전화번호'];
        for (var i = 1; i <= MAX_INDEX; i++) list.push('변수' + i);
        return list;
    }

    var ALLOWED = allowedVariables();

    /** 본문에서 허용되지 않은 #{...} 를 찾아 중복 없이 돌려준다 */
    function findInvalidVariables(content) {
        var found = String(content || '').match(/#\{[^}]*\}/g) || [];
        var invalid = [];
        found.forEach(function (token) {
            var name = token.slice(2, -1).trim();
            if (ALLOWED.indexOf(name) === -1 && invalid.indexOf(token) === -1) {
                invalid.push(token);
            }
        });
        return invalid;
    }

    function warningFor(input) {
        var id = (input.id || 'field') + 'VariableWarning';
        var box = document.getElementById(id);
        if (box) return box;

        box = document.createElement('div');
        box.id = id;
        box.className = 'variable-warning';
        box.style.cssText = 'background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px;' +
            ' padding: 12px; margin-top: 8px; display: none; font-size: 13px; line-height: 1.6;';
        input.parentNode.insertBefore(box, input.nextSibling);
        return box;
    }

    /** 입력값을 검증하고 경고를 갱신한다. 허용되지 않은 변수가 없으면 true */
    function validateInput(input) {
        if (!input) return true;
        var invalid = findInvalidVariables(input.value);
        var box = warningFor(input);

        if (invalid.length) {
            box.innerHTML = '<strong>⚠️ 사용할 수 없는 변수입니다: ' + invalid.join(', ') + '</strong>' +
                '<div style="margin-top: 6px; color: var(--text-secondary, #666);">' +
                '변수는 버튼으로 제공하는 ' + ALLOWED.map(function (v) { return '#{' + v + '}'; }).join(', ') +
                ' 만 사용할 수 있습니다.</div>';
            box.style.display = 'block';
            return false;
        }
        box.style.display = 'none';
        return true;
    }

    /** 입력 요소에 검증을 붙인다 */
    function guardVariableInput(input) {
        if (!input || input.dataset.variableGuard === 'on') return;
        input.dataset.variableGuard = 'on';
        input.addEventListener('input', function () { validateInput(input); });
        input.addEventListener('blur', function () { validateInput(input); });
        validateInput(input);
    }

    /** 발송·저장 직전 확인용. 허용되지 않은 변수가 있으면 알리고 false */
    function assertAllowedVariables(content) {
        var invalid = findInvalidVariables(content);
        if (!invalid.length) return true;

        var message = '사용할 수 없는 변수가 있습니다: ' + invalid.join(', ') + '\n\n' +
            '변수는 ' + ALLOWED.map(function (v) { return '#{' + v + '}'; }).join(', ') + ' 만 사용할 수 있습니다.';
        if (typeof showToast === 'function') {
            showToast('사용할 수 없는 변수가 있습니다: ' + invalid.join(', '), 'warning');
        } else {
            alert(message);
        }
        return false;
    }

    document.addEventListener('DOMContentLoaded', function () {
        ['messageContent', 'emphasisText', 'templateContent'].forEach(function (id) {
            guardVariableInput(document.getElementById(id));
        });
    });

    global.VARIABLE_MAX_INDEX = MAX_INDEX;
    global.ALLOWED_VARIABLES = ALLOWED;
    global.findInvalidVariables = findInvalidVariables;
    global.guardVariableInput = guardVariableInput;
    global.assertAllowedVariables = assertAllowedVariables;
})(window);
