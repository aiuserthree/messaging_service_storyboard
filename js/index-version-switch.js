/**
 * index.html · index.last-commit.html 로컬 비교용 하단 바
 */
(function () {
    var href = window.location.href || '';
    var isLastCommit = href.indexOf('index.last-commit.html') !== -1;
    var isBeforeToday = href.indexOf('index.before-today.html') !== -1;
    var isCurrent = !isLastCommit && !isBeforeToday;

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

    var aCurrent = document.createElement('a');
    aCurrent.href = 'index.html';
    aCurrent.textContent = '현재 작업본';
    aCurrent.title = '지금 워킹 디렉터리';
    if (isCurrent) aCurrent.className = 'ivb-active';

    var aPrev = document.createElement('a');
    aPrev.href = 'index.last-commit.html';
    aPrev.textContent = '이전 커밋';
    aPrev.title = '마지막 git 커밋(HEAD) 스냅샷';
    if (isLastCommit) aPrev.className = 'ivb-active';

    bar.appendChild(label);
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
