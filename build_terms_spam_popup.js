var fs = require('fs');
var path = require('path');

function escapeForTemplateLiteral(s) {
    return s.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$\{/g, '\\${');
}

function mdToHtml(md) {
    var lines = md.split(/\r?\n/);
    var out = [];
    var inList = false;
    var listItems = [];
    function flushList() {
        if (!inList) return;
        inList = false;
        out.push('<ul style="padding-left: 32px; margin-bottom: 16px;">');
        listItems.forEach(function(li) {
            out.push('<li style="margin-bottom: 6px;">' + li + '</li>');
        });
        listItems = [];
        out.push('</ul>');
    }
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        var t = line.trim();
        if (!t) {
            flushList();
            continue;
        }
        if (/^제\d+장\s/.test(t)) {
            flushList();
            var marginTop = (i === 0) ? '0' : '28px';
            out.push('<h4 style="margin-top: ' + marginTop + '; margin-bottom: 12px; color: var(--primary-color);">' + t + '</h4>');
            continue;
        }
        if (/^제\d+조\s*\(/.test(t) || /^제\d+조의\d+/.test(t)) {
            flushList();
            out.push('<p style="margin-bottom: 12px;"><strong>' + t + '</strong></p>');
            continue;
        }
        if (/^[①②③④⑤⑥⑦⑧⑨⑩]\s/.test(t) || /^[가나다]\)\s/.test(t)) {
            flushList();
            out.push('<p style="margin-bottom: 8px; padding-left: 16px;">' + t + '</p>');
            continue;
        }
        if (/^\d+\.\s/.test(t)) {
            if (!inList) flushList();
            inList = true;
            listItems.push(t.replace(/^\d+\.\s*/, ''));
            continue;
        }
        if (/^[oO]\s/.test(t) || /^[oO]\t/.test(t)) {
            flushList();
            out.push('<p style="margin-bottom: 6px; padding-left: 32px;">' + t.replace(/^[oO]\s*/, '').replace(/^[oO]\t*/, '') + '</p>');
            continue;
        }
        if (t === '부칙') {
            flushList();
            out.push('<p style="margin-bottom: 8px; padding-left: 16px;">부칙</p>');
            continue;
        }
        flushList();
        out.push('<p style="margin-bottom: 8px; padding-left: 16px;">' + t + '</p>');
    }
    flushList();
    return out.join('\n            ');
}

function wrapWithVersionSelector(innerHtml, selectId, currentId, previousId, switchFn) {
    var html = [
        '<div style="line-height: 1.8; color: var(--text-primary);">',
        '    <div class="policy-version-selector" style="margin-bottom: 20px; padding: 12px 16px; background: var(--bg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px;">',
        '        <label for="' + selectId + '" style="font-weight: 600;">시행일 선택: </label>',
        '        <select id="' + selectId + '" onchange="' + switchFn + '(this.value)" style="padding: 6px 12px; margin-left: 8px; border-radius: 6px; border: 1px solid var(--border-color, #e2e8f0);">',
        '            <option value="current">현재 (2026년 XX월 XX일)</option>',
        '        </select>',
        '    </div>',
        '    <div id="' + currentId + '">',
        innerHtml,
        '    </div>',
        '    <div id="' + previousId + '" style="display: none;"></div>',
        '</div>'
    ].join('\n            ');
    return escapeForTemplateLiteral(html);
}

var termsMd = fs.readFileSync(path.join(__dirname, 'docs/사용자이용약관_v0.4.md'), 'utf8');
var spamMd = fs.readFileSync(path.join(__dirname, 'docs/스팸방지정책_v0.4.md'), 'utf8');

var termsHtml = mdToHtml(termsMd);
var spamHtml = mdToHtml(spamMd);

var termsBlock = "        'terms': `\n            " + wrapWithVersionSelector(termsHtml, 'termsVersionSelect', 'termsContentCurrent', 'termsContentPrevious', 'switchTermsVersion') + "\n        `,";
var spamBlock = "        'spam': `\n            " + wrapWithVersionSelector(spamHtml, 'spamVersionSelect', 'spamContentCurrent', 'spamContentPrevious', 'switchSpamVersion') + "\n        `,";

var footerPath = path.join(__dirname, 'js/footer.js');
var footer = fs.readFileSync(footerPath, 'utf8');

var privacyMarker = "        `,\n        'privacy': `";
var refundMarker = "        `,\n        'refund': `";

var termsStart = footer.indexOf("        'terms': `");
var termsEnd = footer.indexOf(privacyMarker);
if (termsStart === -1 || termsEnd === -1) {
    console.error('terms block not found');
    process.exit(1);
}
var spamStart = footer.indexOf("        'spam': `");
var spamEnd = footer.indexOf(refundMarker);
if (spamStart === -1 || spamEnd === -1) {
    console.error('spam block not found');
    process.exit(1);
}

// Replace spam first (later in file), then terms
footer = footer.slice(0, spamStart) + spamBlock + "\n        'refund': `" + footer.slice(spamEnd + refundMarker.length);
footer = footer.slice(0, termsStart) + termsBlock + "\n        'privacy': `" + footer.slice(termsEnd + privacyMarker.length);

fs.writeFileSync(footerPath, footer);
console.log('Replaced terms and spam blocks in js/footer.js');
