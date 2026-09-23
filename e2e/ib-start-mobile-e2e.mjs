import { chromium } from 'playwright';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const baseUrl = process.env.E2E_BASE_URL || 'http://127.0.0.1:4173';
const outDir = process.env.E2E_ARTIFACT_DIR || 'artifacts/e2e';
await mkdir(outDir, { recursive: true });

const htmlFixture = `<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mobile E2E</title><style>*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:#111827;color:#fff;overflow:hidden}.slide{display:none;width:100vw;height:100vh;padding:8vw;background:linear-gradient(135deg,#1d4ed8,#7c3aed)}.slide.active{display:grid;place-items:center;text-align:center}.slide h1{font-size:10vw}.slide p{font-size:5vw}</style></head><body><section class="slide active"><div><h1>Mobile E2E</h1><p>Touch-Test</p></div></section><section class="slide"><div><h1>Fertig</h1><p>Responsive Präsentation</p></div></section><script>const s=[...document.querySelectorAll('.slide')];let i=0;const show=n=>{i=(n+s.length)%s.length;s.forEach((x,j)=>x.classList.toggle('active',j===i))};addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown',' '].includes(e.key))show(i+1);if(e.key==='ArrowLeft')show(i-1)});</script></body></html>`;

const profiles = [
  { name: 'phone-390x844', viewport: { width: 390, height: 844 } },
  { name: 'tablet-768x1024', viewport: { width: 768, height: 1024 } },
];

const browser = await chromium.launch({ headless: true });
const summaries = [];

const runProfile = async profile => {
  const context = await browser.newContext({
    acceptDownloads: true,
    viewport: profile.viewport,
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 1,
  });

  await context.addInitScript(() => {
    try {
      localStorage.setItem('ib-startcheck:index2:v2', JSON.stringify({
        studentName: 'Mobile Test',
        studentFirstName: 'Mobile Test',
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
  const browserErrors = [];
  page.on('pageerror', error => browserErrors.push(`pageerror: ${error.message}`));
  page.on('console', message => {
    if (message.type() === 'error') browserErrors.push(`console: ${message.text()}`);
  });

  const assert = (condition, message) => {
    if (!condition) throw new Error(`[${profile.name}] ${message}`);
  };

  const tap = async locator => {
    await locator.scrollIntoViewIfNeeded();
    await locator.tap();
  };

  const assertMobileLayout = async label => {
    const result = await page.evaluate(() => {
      const viewportWidth = window.innerWidth;
      const scrollWidth = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth);
      const visible = el => {
        const style = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
      };
      const clippedActions = [...document.querySelectorAll('button, a.outlook-link')]
        .filter(visible)
        .filter(el => el.scrollWidth > el.clientWidth + 3)
        .slice(0, 8)
        .map(el => (el.textContent || el.getAttribute('aria-label') || el.className).trim().replace(/\s+/g, ' '));
      return { viewportWidth, scrollWidth, clippedActions };
    });
    assert(result.scrollWidth <= result.viewportWidth + 2, `${label}: horizontal overflow ${result.scrollWidth}px > ${result.viewportWidth}px`);
    assert(result.clippedActions.length === 0, `${label}: clipped action controls: ${result.clippedActions.join(' | ')}`);
  };

  const openTask = async taskId => {
    await tap(page.locator(`[data-task-target="${taskId}"]`));
    await page.locator(`[data-task="${taskId}"]`).waitFor({ state: 'visible' });
    await assertMobileLayout(`task ${taskId}`);
  };

  const expectDone = async taskId => {
    await page.waitForFunction(id => document.querySelector(`[data-task-target="${id}"]`)?.classList.contains('is-done'), taskId);
  };

  const checkAll = async locator => {
    for (let i = 0, count = await locator.count(); i < count; i += 1) await locator.nth(i).check();
  };

  try {
    await page.goto(`${baseUrl}/index.html`, { waitUntil: 'networkidle' });
    await page.locator('h1').waitFor({ state: 'visible' });
    await assertMobileLayout('home');

    const navBoxes = await page.locator('.task-tile').evaluateAll(els => els.map(el => el.getBoundingClientRect().width));
    assert(navBoxes.every(width => width >= 120), `task tiles are too narrow: ${navBoxes.map(x => Math.round(x)).join(', ')}`);

    await tap(page.locator('.settings-button'));
    await page.locator('.settings-panel').waitFor({ state: 'visible' });
    const settingsRect = await page.locator('.settings-panel').boundingBox();
    assert(settingsRect && settingsRect.x >= -1 && settingsRect.x + settingsRect.width <= profile.viewport.width + 1, 'settings panel escapes viewport');
    await tap(page.locator('.settings-button'));

    await openTask('task-1');
    await tap(page.locator('[data-read-confirm="task-1-brief"]'));
    await expectDone('task-1');

    await openTask('task-6');
    for (const group of ['presentation', 'ai']) {
      const section = page.locator(`[data-privacy-group="${group}"]`);
      await checkAll(section.locator('input[data-privacy-answer][value="good"]'));
      await tap(section.locator(`[data-check-privacy="${group}"]`));
    }
    await expectDone('task-6');

    await openTask('task-3');
    for (const [row, answer] of Object.entries({ presentation: 'bad', lena: 'good', asdf: 'bad', noah: 'good', final: 'bad' })) {
      await page.locator(`[data-filename-row="${row}"] input[value="${answer}"]`).check();
    }
    await page.locator('input[name="good-filename"]').fill(`mobile_${profile.name}.html`);
    await tap(page.locator('[data-check-task="task-3"]'));
    await expectDone('task-3');

    await openTask('task-5');
    await checkAll(page.locator('[data-prompt-answer][value="good"]'));
    await page.locator('textarea[name="prompt-reason"]').fill('Ein genauer Prompt beschreibt Ziel und Inhalte klar.');
    await tap(page.locator('[data-check-task="task-5"]'));
    await expectDone('task-5');

    await openTask('task-7');
    for (const [left, right] of [['ctrl-s','save'],['ctrl-c','copy'],['ctrl-v','paste'],['ctrl-z','undo'],['alt-tab','switch'],['f5','present'],['f11','fullscreen']]) {
      await tap(page.locator(`[data-side="left"][data-id="${left}"]`));
      await tap(page.locator(`[data-side="right"][data-id="${right}"]`));
    }
    await tap(page.locator('[data-check-task="task-7"]'));
    await expectDone('task-7');

    await openTask('task-2');
    await page.locator('input[name="created"][value="html"]').check();
    await expectDone('task-2');

    await openTask('task-8');
    await page.locator('textarea[name="learned"]').fill('Ich habe den Startcheck mobil bearbeitet.');
    await page.locator('textarea[name="easy"]').fill('Tippen und Auswählen.');
    await page.locator('textarea[name="difficult"]').fill('Die Verbindungsaufgabe.');
    await page.locator('textarea[name="future"]').fill('Webseiten und Games programmieren.');
    await expectDone('task-8');

    await openTask('task-9');
    await page.locator('[data-html-runner-input]').fill(htmlFixture);
    await tap(page.locator('[data-html-runner-start]'));
    const stage = page.locator('[data-presentation-stage]');
    await stage.waitFor({ state: 'visible' });
    const back = page.locator('[data-presentation-back]');
    await back.waitFor({ state: 'visible' });
    const backBox = await back.boundingBox();
    assert(backBox && backBox.width >= 44 && backBox.height >= 44, 'presentation back control is too small for touch');
    await tap(back);
    await stage.waitFor({ state: 'hidden' });

    const htmlPath = path.join(outDir, `IB-Startcheck-Mobile-${profile.name}.html`);
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      tap(page.locator('[data-html-download]')),
    ]);
    await download.saveAs(htmlPath);
    const downloadedHtml = await readFile(htmlPath, 'utf8');
    assert(downloadedHtml.includes('Mobile E2E'), 'downloaded HTML is wrong');

    const mailCopy = (await page.locator('.outlook-link').locator('xpath=ancestor::div[contains(@class,"auftrag-card")]').textContent()) || '';
    assert(mailCopy.includes('vorname.nachname@sus.gsu-so.ch'), 'school mail hint missing');
    assert(!mailCopy.includes('Deine Schul-Mailadresse:'), 'obsolete school mail label is still visible');

    await page.locator('input[name="mail-submission"]').check();
    await expectDone('task-9');
    assert(await page.locator('.task-tile.is-done').count() === 8, 'not all eight tasks completed');
    await assertMobileLayout('completed lesson');

    await tap(page.locator('[data-submit-pdf]'));
    await page.waitForFunction(() => window.__E2E_PRINT_CALLED__ === true);
    assert(await page.locator('[data-pdf-lock-modal]').evaluate(el => el.hidden), 'PDF remained locked');

    const submissionButtons = page.locator('[data-task="task-9"] .submission-action-button, [data-task="task-9"] .outlook-link, [data-task="task-9"] .html-runner-start');
    for (let i = 0, count = await submissionButtons.count(); i < count; i += 1) {
      if (!(await submissionButtons.nth(i).isVisible())) continue;
      const box = await submissionButtons.nth(i).boundingBox();
      assert(box && box.height >= 40, `submission action ${i + 1} is too short for touch`);
    }

    await page.screenshot({ path: path.join(outDir, `IB-Startcheck-Mobile-${profile.name}.png`), fullPage: true });
    assert(browserErrors.length === 0, `browser errors: ${browserErrors.join(' | ')}`);
    summaries.push(`${profile.name}: PASS — 8/8 tasks, touch/fullscreen/download/PDF unlock, no horizontal overflow`);
  } catch (error) {
    await page.screenshot({ path: path.join(outDir, `MOBILE-FAILURE-${profile.name}.png`), fullPage: true }).catch(() => {});
    await writeFile(path.join(outDir, `MOBILE-FAILURE-${profile.name}.txt`), `${error.stack || error}\n${browserErrors.join('\n')}\n`).catch(() => {});
    throw error;
  } finally {
    await context.close();
  }
};

try {
  for (const profile of profiles) await runProfile(profile);
  await writeFile(path.join(outDir, 'mobile-e2e-summary.txt'), ['IB-Startcheck Mobile E2E: PASS', ...summaries].join('\n') + '\n');
  console.log(summaries.join('\n'));
} finally {
  await browser.close();
}
