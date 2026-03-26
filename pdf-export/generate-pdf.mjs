import puppeteer from 'puppeteer';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const htmlPath = join(__dirname, 'message-send-system.html');
const pdfPath = join(__dirname, 'message-send-system.pdf');
const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
try {
  const page = await browser.newPage();
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 120000 });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '18mm', right: '16mm', bottom: '18mm', left: '16mm' },
  });
  console.log('Wrote:', pdfPath);
} finally {
  await browser.close();
}
