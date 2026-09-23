import { chromium } from 'playwright';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const baseUrl = process.env.E2E_BASE_URL || 'http://127.0.0.1:4173';
const outDir = process.env.E2E_ARTIFACT_DIR || 'artifacts/e2e';
await mkdir(outDir, { recursive: true });

const htmlFixture = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>E2E Mini-Präsentation</title>
<style>
  *{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:#111827;color:white;overflow:hidden}
  .slide{display:none;width:100vw;height:100vh;padding:8vw;background:linear-gradient(135deg,#1d4ed8,#7c3aed)}
  .slide.active{display:grid;place-items:center;text-align:center}.slide h1{font-size:8vw;margin:0}.slide p{font-size:3vw;max-width:900px}
</style>
</head>
<body>
<section class="slide active"><div><h1>E2E Test</h1><p>HTML-Präsentation für den automatischen IB-Startcheck.</p></div></section>
<section class="slide"><div><h1>Hobbys</h1><p>Programmieren · Games · Musik</p></div></section>
<section class="slide"><div><h1>Fertig</h1><p>Die Tastatur-Navigation funktioniert.</p></div></section>
<script>
  const slides=[...document.querySelectorAll('.slide')]; let i=0;
  const show=n=>{i=(n+slides.length)%slides.length;slides.forEach((s,j)=>s.classList.toggle('active',j===i));};
  addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown',' '].includes(e.key))show(i+1);if(e.key==='ArrowLeft')show(i-1);});
</script>
</body>
</html>`;

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  acceptDownloads: true,
  viewport: { width: 1440, height: 1000 },
});

await context.addInitScript(() => {
  try {
    localStorage.setItem('ib-startcheck:index2:v2', JSON.stringify({
      studentName: 'E2E Test',
      studentFirstName: 'E2E Test',
      studentClass: '7B',
      theme: 'white',
      fontScale: 100,
      readConfirmations: {},
      solvedTasks: {},
      matches: [],
    }));
  } catch {}
  window.__E2E_PRINT_CALLED__ = false;
  window.print = () => { window.__E2E_PRINT_CALLED__ = true; };
});

const page = await context.newPage();
const failures = [];
page.on('pageerror', error => failures.push(`pageerror: ${error.message}`));
page.on('console', message => {
  if (message.type() === 'error') failures.push(`console: ${message.text()}`);
});

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const openTask = async taskId => {
  await page.locator(`[data-task-target="${taskId}"]`).click();
  await page.locator(`[data-task="${taskId}"]`).waitFor({ state: 'visible' });
};

const checkAll = async locator => {
  const count = await locator.count();
  for (let i = 0; i < count; i += 1) await locator.nth(i).check();
};

const expectDone = async taskId => {
  await page.waitForFunction(id => document.querySelector(`[data-task-target="${id}"]`)?.classList.contains('is-done'), taskId);
};

try {
  await page.goto(`${baseUrl}/index.html`, { waitUntil: 'networkidle' });
  await page.locator('h1').waitFor({ state: 'visible' });
  assert((await page.locator('[data-student-name]').textContent())?.includes('E2E Test'), 'Student name was not restored');

  // 01 Mini-Präsentation
  await openTask('task-1');
  await page.locator('[data-read-confirm="task-1-brief"]').click();
  await expectDone('task-1');

  // 02 Datenschutz: only the permitted values are selected.
  await openTask('task-6');
  for (const group of ['presentation', 'ai']) {
    const section = page.locator(`[data-privacy-group="${group}"]`);
    await checkAll(section.locator('input[data-privacy-answer][value="good"]'));
    await section.locator(`[data-check-privacy="${group}"]`).click();
  }
  await expectDone('task-6');

  // 03 Dateinamen
  await openTask('task-3');
  const filenameAnswers = {
    presentation: 'bad',
    lena: 'good',
    asdf: 'bad',
    noah: 'good',
    final: 'bad',
  };
  for (const [row, answer] of Object.entries(filenameAnswers)) {
    await page.locator(`[data-filename-row="${row}"] input[value="${answer}"]`).check();
  }
  await page.locator('input[name="good-filename"]').fill('e2e_test_informatik.html');
  await page.locator('[data-check-task="task-3"]').click();
  await expectDone('task-3');

  // 04 KI richtig nutzen
  await openTask('task-5');
  await checkAll(page.locator('[data-prompt-answer][value="good"]'));
  await page.locator('textarea[name="prompt-reason"]').fill('Ein genauer Prompt beschreibt Ziel und Inhalte klar, deshalb kann die KI passender antworten.');
  await page.locator('[data-check-task="task-5"]').click();
  await expectDone('task-5');

  // 05 Tastenkombinationen
  await openTask('task-7');
  const shortcutPairs = [
    ['ctrl-s', 'save'],
    ['ctrl-c', 'copy'],
    ['ctrl-v', 'paste'],
    ['ctrl-z', 'undo'],
    ['alt-tab', 'switch'],
    ['f5', 'present'],
    ['f11', 'fullscreen'],
  ];
  for (const [left, right] of shortcutPairs) {
    await page.locator(`[data-side="left"][data-id="${left}"]`).click();
    await page.locator(`[data-side="right"][data-id="${right}"]`).click();
  }
  await page.locator('[data-check-task="task-7"]').click();
  await expectDone('task-7');

  // 06 Präsentation: HTML variant selected.
  await openTask('task-2');
  await page.locator('input[name="created"][value="html"]').check();
  await expectDone('task-2');

  // 07 Rückblick
  await openTask('task-8');
  await page.locator('textarea[name="learned"]').fill('Ich habe Dateien, Datenschutz, Prompts und Tastenkombinationen geübt.');
  await page.locator('textarea[name="easy"]').fill('Das Speichern und die Dateinamen waren einfach.');
  await page.locator('textarea[name="difficult"]').fill('Die Datenschutz-Unterschiede musste ich genau lesen.');
  await page.locator('textarea[name="future"]').fill('Ich möchte eine kleine Webseite und ein Game programmieren.');
  await expectDone('task-8');

  // 08 Abgabe: use the real HTML preview, fullscreen flow and download.
  await openTask('task-9');
  await page.locator('[data-html-runner-input]').fill(htmlFixture);
  await page.locator('[data-html-runner-start]').click();
  const stage = page.locator('[data-presentation-stage]');
  await stage.waitFor({ state: 'visible' });
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('ArrowLeft');
  await page.keyboard.press('Escape');
  if (await stage.isVisible()) await page.locator('[data-presentation-back]').click();
  await stage.waitFor({ state: 'hidden' });

  const htmlPath = path.join(outDir, 'IB-Startcheck-E2E-Praesentation.html');
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.locator('[data-html-download]').click(),
  ]);
  await download.saveAs(htmlPath);
  const downloadedHtml = await readFile(htmlPath, 'utf8');
  assert(downloadedHtml.includes('E2E Mini-Präsentation'), 'Downloaded HTML does not contain the E2E presentation');

  const outlookHref = await page.locator('.outlook-link').getAttribute('href');
  assert(outlookHref === 'https://outlook.cloud.microsoft/', 'Outlook link is incorrect');
  assert((await page.locator('.school-mail-address').textContent())?.trim() === 'vorname.nachname@sus.gsu-so.ch', 'School mail hint is incorrect');

  await page.locator('input[name="mail-submission"]').check();
  await expectDone('task-9');

  // All eight visible tasks must be complete.
  const doneCount = await page.locator('.task-tile.is-done').count();
  assert(doneCount === 8, `Expected 8 completed tasks, got ${doneCount}`);

  // Exercise the app's own PDF unlock logic. window.print is intercepted in CI.
  await page.locator('[data-submit-pdf]').click();
  await page.waitForFunction(() => window.__E2E_PRINT_CALLED__ === true);
  assert(await page.locator('[data-pdf-lock-modal]').evaluate(el => el.hidden), 'PDF lock modal opened although all required tasks were complete');

  await page.screenshot({ path: path.join(outDir, 'IB-Startcheck-E2E-complete.png'), fullPage: true });

  // Produce the final printable artifact with Chromium's PDF engine using the app's print CSS.
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: path.join(outDir, 'IB-Startcheck-E2E.pdf'),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
  });
  await page.emulateMedia({ media: 'screen' });

  const state = await page.evaluate(() => JSON.parse(localStorage.getItem('ib-startcheck:index2:v2') || '{}'));
  await writeFile(path.join(outDir, 'e2e-state.json'), JSON.stringify(state, null, 2));
  await writeFile(path.join(outDir, 'e2e-summary.txt'), [
    'IB-Startcheck E2E: PASS',
    `URL: ${baseUrl}/index.html`,
    `Completed task tiles: ${doneCount}/8`,
    `HTML download: ${download.suggestedFilename()}`,
    'PDF unlock: passed',
    'HTML preview/fullscreen: passed',
    'Outlook URL + school mail hint: passed',
  ].join('\n') + '\n');

  if (failures.length) {
    await writeFile(path.join(outDir, 'browser-console.txt'), failures.join('\n') + '\n');
    throw new Error(`Browser reported ${failures.length} console/page error(s). See browser-console.txt`);
  }

  console.log('IB-Startcheck E2E passed: all tasks completed, HTML downloaded, PDF generated.');
} catch (error) {
  try {
    await page.screenshot({ path: path.join(outDir, 'E2E-FAILURE.png'), fullPage: true });
    await writeFile(path.join(outDir, 'E2E-FAILURE.txt'), `${error.stack || error}\n${failures.join('\n')}\n`);
  } catch {}
  throw error;
} finally {
  await browser.close();
}
