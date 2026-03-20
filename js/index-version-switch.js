/**
 * index.html · index.last-commit.html 로컬 비교용 하단 바
 * main_v1.1/ 에서는 ../ 로 spec 루트 HTML로 이동 (<base> 미사용)
 */
(function () {
    var href = window.location.href || '';
    var isLastCommit = href.indexOf('index.last-commit.html') !== -1;
    var isBeforeToday = href.indexOf('index.before-today.html') !== -1;
    var isV11Standalone = /main_v1\.1[\/\\]index\.html/i.test(href);
    var isRootIndex =
        !isLastCommit &&
        !isBeforeToday &&
        !isV11Standalone &&
        /(^|[\/\\])index\.html(\?|$|#)/i.test(href) &&
        href.indexOf('index.last-commit') === -1;

    var root = isV11Standalone ? '../' : '';

    var style = document.createElement('style');
    style.textContent = [
        '#index-version-bar{',
        'position:fixed;bottom:16px;right:16px;z-index:99999;',
        'display:flex;align-items:center;gap:6px;flex-wrap:wrap;',
        'max-width:calc(100vw - 32px);',
        'padding:10px 12px;background:rgba(17,17,17,.94);color:#fff;',
        'border-radius:10px;font-size:12px;font-family:system-ui,-apple-system,sans-serif;',
        'box-shadow:0 4px 24px rgba(0,0,0,.25);',
        '}',
        '#index-version-bar .ivb-label{opacity:.75;margin-right:4px;font-size:11px;}',
        '#index-version-bar a{',
        'color:#fff;text-decoration:none;padding:7px 10px;border-radius:8px;',
        'border:1px solid rgba(255,255,255,.2);transition:background .15s;',
        'white-space:nowrap;',
        '}',
        '#index-version-bar a:hover{background:rgba(255,255,255,.12);}',
        '#index-version-bar a.ivb-active{background:#7a9e2e;border-color:#6d8a28;}',
    ].join('');
    document.head.appendChild(style);

    var bar = document.createElement('div');
    bar.id = 'index-version-bar';
    bar.setAttribute('role', 'navigation');
    bar.setAttribute('aria-label', 'index 버전 전환');

    var label = document.createElement('span');
    label.className = 'ivb-label';
    label.textContent = '랜딩 비교';

    /* 순서: A(수정버전) → B(현재 작업본) → C(이전 커밋) */
    var aV11 = document.createElement('a');
    aV11.href = root + 'main_v1.1/index.html';
    aV11.textContent = 'A';
    aV11.title = '수정 버전 · main_v1.1 랜딩';
    if (isV11Standalone) aV11.className = 'ivb-active';

    var aCurrent = document.createElement('a');
    aCurrent.href = root + 'index.html';
    aCurrent.textContent = 'B';
    aCurrent.title = '현재 작업본 · index.html';
    if (isRootIndex) aCurrent.className = 'ivb-active';

    var aPrev = document.createElement('a');
    aPrev.href = root + 'index.last-commit.html';
    aPrev.textContent = 'C';
    aPrev.title = '이전 커밋 · index.last-commit.html';
    if (isLastCommit) aPrev.className = 'ivb-active';

    bar.appendChild(label);
    bar.appendChild(aV11);
    bar.appendChild(aCurrent);
    bar.appendChild(aPrev);

    if (document.body) {
        document.body.appendChild(bar);
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            document.body.appendChild(bar);
        });
    }
})();
