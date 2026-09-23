from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_head = '''              <div class="html-runner-head"><strong>HTML-Präsentation vorbereiten</strong><span>Esc zurück · ← vorherige · → / ↓ / Leertaste nächste</span></div>'''
new_head = '''              <div class="html-runner-head">
                <strong>HTML-Präsentation vorbereiten</strong>
                <div class="runner-shortcuts" aria-label="Tasten für die Präsentation">
                  <span class="runner-shortcut"><kbd>Esc</kbd><span>zurück</span></span>
                  <span class="runner-shortcut"><kbd>←</kbd><span>vorherige</span></span>
                  <span class="runner-shortcut runner-shortcut-next"><kbd>→</kbd><kbd>↓</kbd><kbd>Leertaste</kbd><span>nächste</span></span>
                </div>
              </div>'''
assert s.count(old_head) == 1, s.count(old_head)
s = s.replace(old_head, new_head)

old_actions = '''              <div class="html-runner-actions">
                <button class="html-runner-start" type="button" data-html-runner-start>▶ Fullscreen testen</button>
                <button class="html-runner-start html-runner-download" type="button" data-html-download>↓ HTML herunterladen</button>
                <span class="html-runner-status" data-html-runner-status aria-live="polite"></span>
              </div>'''
new_actions = '''              <div class="html-runner-actions">
                <button class="html-runner-start" type="button" data-html-runner-start><span aria-hidden="true">▶</span> Fullscreen testen</button>
                <button class="html-runner-start html-runner-download" type="button" data-html-download><span aria-hidden="true">↓</span> HTML herunterladen</button>
              </div>
              <div class="html-runner-status" data-html-runner-status aria-live="polite"></div>'''
assert s.count(old_actions) == 1, s.count(old_actions)
s = s.replace(old_actions, new_actions)

old_files = '''            <div class="final-box">
              <strong>📎 Diese Dateien an die Mail anhängen</strong>
              <p><strong>HTML-Variante:</strong> PDF + HTML-Datei<br><strong>PowerPoint-Variante:</strong> PDF + PowerPoint-Datei (.pptx)</p>
            </div>'''
new_files = '''            <div class="submission-files" aria-labelledby="submission-files-title">
              <div class="submission-files-title" id="submission-files-title"><span aria-hidden="true">📎</span><strong>Diese Dateien an die Mail anhängen</strong></div>
              <div class="submission-file-row">
                <span class="submission-file-variant">HTML</span>
                <div class="submission-file-chips" aria-label="PDF und HTML-Datei">
                  <span class="submission-file-chip">PDF</span><span class="submission-file-plus" aria-hidden="true">+</span><span class="submission-file-chip">HTML-Datei</span>
                </div>
              </div>
              <div class="submission-file-row">
                <span class="submission-file-variant">PowerPoint</span>
                <div class="submission-file-chips" aria-label="PDF und PowerPoint-Datei">
                  <span class="submission-file-chip">PDF</span><span class="submission-file-plus" aria-hidden="true">+</span><span class="submission-file-chip">PowerPoint-Datei (.pptx)</span>
                </div>
              </div>
            </div>'''
assert s.count(old_files) == 1, s.count(old_files)
s = s.replace(old_files, new_files)

old_status = '''      const runnerStatus = (text, error = false) => {
        if (!htmlRunnerStatus) return;
        htmlRunnerStatus.textContent = text;
        htmlRunnerStatus.style.color = error ? "var(--red)" : "";
      };'''
new_status = '''      const runnerStatus = (text, error = false) => {
        if (!htmlRunnerStatus) return;
        htmlRunnerStatus.textContent = text;
        htmlRunnerStatus.classList.toggle("is-error", Boolean(text) && error);
        htmlRunnerStatus.classList.toggle("is-success", Boolean(text) && !error);
      };'''
assert s.count(old_status) == 1, s.count(old_status)
s = s.replace(old_status, new_status)

anchor = '''    body.presentation-open { overflow: hidden; }'''
css = r'''    /* Submission polish: clear keyboard affordances, button hierarchy and attachment summary. */
    .html-runner-head {
      align-items: flex-start;
      gap: 14px 18px;
      margin-bottom: 14px;
    }
    .runner-shortcuts {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 8px 12px;
      flex-wrap: wrap;
    }
    .runner-shortcut {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--muted);
      font-size: .88em;
      font-weight: 750;
      white-space: nowrap;
    }
    .runner-shortcut-next { gap: 5px; }
    .runner-shortcut kbd {
      min-width: 32px;
      min-height: 30px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 9px;
      border: 1px solid color-mix(in srgb, var(--slide-text) 18%, var(--line));
      border-bottom-width: 3px;
      border-radius: 8px;
      background: var(--control-bg);
      color: var(--control-color);
      box-shadow: 0 2px 6px rgba(15, 23, 42, .08);
      font: inherit;
      font-size: .95em;
      font-weight: 900;
      line-height: 1;
    }
    .html-runner-actions { margin-top: 14px; }
    .html-runner-start {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: filter .16s ease, transform .16s ease, box-shadow .16s ease;
    }
    .html-runner-start:hover,
    .html-runner-start:focus-visible {
      filter: brightness(1.05);
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent, var(--blue)) 16%, transparent);
      outline: 0;
    }
    .html-runner-start:active { transform: scale(.97); }
    .html-runner-start.html-runner-download {
      background: var(--control-bg);
      color: var(--accent, var(--violet));
      border: 1px solid color-mix(in srgb, var(--accent, var(--violet)) 34%, var(--line));
      box-shadow: none;
    }
    .html-runner-status {
      display: none;
      width: fit-content;
      max-width: 100%;
      margin-top: 12px;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: .92em;
      font-weight: 800;
    }
    .html-runner-status:not(:empty) {
      display: inline-flex;
      align-items: center;
    }
    .html-runner-status.is-success {
      color: color-mix(in srgb, var(--green) 82%, var(--slide-text));
      background: color-mix(in srgb, var(--green) 10%, var(--panel-bg));
      border: 1px solid color-mix(in srgb, var(--green) 25%, var(--line));
    }
    .html-runner-status.is-error {
      color: var(--red);
      background: color-mix(in srgb, var(--red) 8%, var(--panel-bg));
      border: 1px solid color-mix(in srgb, var(--red) 24%, var(--line));
    }
    .submission-files {
      margin: 18px 0;
      padding: 16px;
      border: 1px solid color-mix(in srgb, var(--green) 28%, var(--line));
      border-radius: 18px;
      background: color-mix(in srgb, var(--green) 5%, var(--panel-bg));
      box-shadow: 0 10px 24px rgba(15, 23, 42, .05);
    }
    .submission-files-title {
      display: flex;
      align-items: center;
      gap: 9px;
      margin-bottom: 12px;
      color: var(--slide-title);
      font-size: 1.02em;
    }
    .submission-file-row {
      display: grid;
      grid-template-columns: minmax(120px, .42fr) minmax(0, 1fr);
      align-items: center;
      gap: 12px;
      padding: 12px 13px;
      border: 1px solid color-mix(in srgb, var(--green) 12%, var(--line));
      border-radius: 13px;
      background: color-mix(in srgb, var(--control-bg) 88%, transparent);
    }
    .submission-file-row + .submission-file-row { margin-top: 9px; }
    .submission-file-variant {
      color: var(--slide-title);
      font-weight: 850;
    }
    .submission-file-chips {
      display: flex;
      align-items: center;
      gap: 7px;
      flex-wrap: wrap;
    }
    .submission-file-chip {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 4px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--control-bg);
      color: var(--control-color);
      font-size: .92em;
      font-weight: 800;
      box-shadow: 0 2px 7px rgba(15, 23, 42, .06);
    }
    .submission-file-plus {
      color: var(--muted);
      font-weight: 900;
    }
    @media (max-width: 760px) {
      .runner-shortcuts { justify-content: flex-start; }
      .submission-file-row { grid-template-columns: 1fr; gap: 7px; }
    }

'''
assert s.count(anchor) == 1
s = s.replace(anchor, css + anchor)

assert s.count('class="runner-shortcuts"') == 1
assert s.count('class="submission-files"') == 1
assert s.count('data-html-runner-status') == 1
assert 'html-runner-head span { color:' in s  # harmless legacy rule, overridden by more specific runner styles

p.write_text(s, encoding='utf-8')
