const fs = require('fs');
const path = require('path');

const mdPath = path.join(__dirname, '톡벨(TalkBell) 서비스 이용약관_20260204.md');
const outPath = path.join(__dirname, 'terms-modal-body.html');

const md = fs.readFileSync(mdPath, 'utf8');
const lines = md.split(/\r?\n/);

const s = (str) => String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const styleP = 'style="margin-bottom: 8px; padding-left: 16px;"';
const styleP2 = 'style="margin-bottom: 12px; padding-left: 16px;"';
const styleLi = 'style="margin-bottom: 6px;"';
const styleUl = 'style="padding-left: 32px; margin-bottom: 16px;"';
const styleH4 = 'style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);"';
const styleH4First = 'style="margin-top: 0; margin-bottom: 12px; color: var(--primary-color);"';

let html = '';
let inUl = false;
let firstH4 = true;

function closeUl() {
  if (inUl) {
    html += '</ul>\n';
    inUl = false;
  }
}

for (let i = 0; i < lines.length; i++) {
  const raw = lines[i];
  const line = raw.trim();
  if (!line) {
    closeUl();
    html += '\n';
    continue;
  }
  if (/^제\d+장/.test(line)) {
    closeUl();
    const style = firstH4 ? styleH4First : styleH4;
    firstH4 = false;
    html += `<h4 ${style}>${s(line)}</h4>\n`;
  } else if (/^제[\d]+조/.test(line) || /^제\d+조의\d+/.test(line)) {
    closeUl();
    html += `<p style="margin-bottom: 12px;"><strong>${s(line)}</strong></p>\n`;
  } else if (/^[①②③④⑤⑥⑦⑧⑨⑩]\s*/.test(line)) {
    closeUl();
    html += `<p ${styleP}>${s(line)}</p>\n`;
  } else if (/^\d+\.\s+/.test(line) || /^\d+\.\t/.test(line)) {
    const text = line.replace(/^\d+\.\s*/, '').replace(/^\d+\.\t/, '');
    if (!inUl) {
      html += `<ul ${styleUl}>\n`;
      inUl = true;
    }
    html += `<li ${styleLi}>${s(text)}</li>\n`;
  } else if (/^[가나다라마바사]\)\s*/.test(line) && inUl) {
    html += `<li ${styleLi}>${s(line)}</li>\n`;
  } else if (/^[oO]\s+/.test(line) && inUl) {
    html += `<li ${styleLi}>${s(line.replace(/^[oO]\s+/, ''))}</li>\n`;
  } else {
    closeUl();
    html += `<p ${styleP}>${s(line)}</p>\n`;
  }
}
closeUl();

fs.writeFileSync(outPath, html, 'utf8');
console.log('Wrote', outPath);
