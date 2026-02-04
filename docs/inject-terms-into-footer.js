const fs = require('fs');
const path = require('path');

const footerPath = path.join(__dirname, '..', 'js', 'footer.js');
const termsPath = path.join(__dirname, 'terms-modal-body.html');

let footer = fs.readFileSync(footerPath, 'utf8');
const termsBody = fs.readFileSync(termsPath, 'utf8').trim();

// Escape for JS template literal: ` -> \`, \ -> \\, ${ -> \${
const escaped = termsBody
  .replace(/\\/g, '\\\\')
  .replace(/`/g, '\\`')
  .replace(/\$\{/g, '\\${');

// Indent each line with 12 spaces to match footer style
const indented = escaped.split('\n').map(line => '            ' + line).join('\n');

const startTag = "        'terms': `\n            <div style=\"line-height: 1.8; color: var(--text-primary);\">\n";
const endTag = "\n            </div>\n        `,\n        'privacy'";

const startIdx = footer.indexOf(startTag);
if (startIdx === -1) {
  console.error('Start marker not found');
  process.exit(1);
}
const afterStart = startIdx + startTag.length;
const endIdx = footer.indexOf(endTag, afterStart);
if (endIdx === -1) {
  console.error('End marker not found');
  process.exit(1);
}

const newBlock = startTag + indented + endTag;
footer = footer.slice(0, startIdx) + newBlock + footer.slice(endIdx + endTag.length);

fs.writeFileSync(footerPath, footer, 'utf8');
console.log('Updated js/footer.js with new terms content.');
