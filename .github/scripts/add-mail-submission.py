from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_nav = '''        <button class="task-tile" type="button" data-task-target="task-8" style="--tile-color: var(--violet)"><span class="task-number">07</span><span class="task-label">Rückblick</span></button>'''
new_nav = '''        <button class="task-tile" type="button" data-task-target="task-8" style="--tile-color: var(--indigo)"><span class="task-number">07</span><span class="task-label">Rückblick</span></button>
        <button class="task-tile" type="button" data-task-target="task-9" style="--tile-color: var(--violet)"><span class="task-number">08</span><span class="task-label">Abgabe per Mail</span></button>'''
assert old_nav in text
text = text.replace(old_nav, new_nav, 1)

text = text.replace('''                  <li>Datei abgeben oder per Outlook senden.</li>''', '''                  <li>Datei speichern. Die Abgabe machst du in Aufgabe 08.</li>''', 1)
text = text.replace('''                  <li>Den HTML-Code unten einfügen und im Vollbild testen.</li>
                  <li>Datei sinnvoll benennen, speichern und abgeben.</li>''', '''                  <li>Präsentation prüfen und verbessern.</li>
                  <li>In Aufgabe 08 den HTML-Code testen, herunterladen und abgeben.</li>''', 1)

start = text.index('            <div class="html-runner">', text.index('data-task="task-2"'))
end_marker = '''          </div>
        </div>
      </section>

      <section class="section" data-task="task-8"'''
end = text.index(end_marker, start)
replacement = '''            <span class="label" style="display:block; margin-top:24px;">Wenn du fertig bist:</span>
            <div class="check-grid">
              <label class="choice"><input type="checkbox" name="created" value="finished"> Meine Präsentation ist fertig und gespeichert.</label>
            </div>
'''
text = text[:start] + replacement + text[end:]

text = text.replace('''      <section class="section" data-task="task-8" style="--accent: var(--violet)">''', '''      <section class="section" data-task="task-8" style="--accent: var(--indigo)">''', 1)

submission = '''

      <section class="section" data-task="task-9" style="--accent: var(--violet)">
        <div class="section-number"><span>08</span><span>✉</span></div>
        <div class="section-body">
          <h2 class="section-title">Abgabe per Mail</h2>
          <div class="section-content">
            <p class="auftrag-intro"><strong>Zum Schluss gibst du deine Arbeit per Mail ab.</strong> Bereite zuerst deine Dateien vor und öffne danach Outlook.</p>

            <div class="html-runner">
              <div class="html-runner-head"><strong>HTML-Präsentation vorbereiten</strong><span>Esc zurück · ← vorherige · → / ↓ / Leertaste nächste</span></div>
              <p class="auftrag-intro">Wenn du die HTML-Variante gewählt hast: Füge den Code hier ein, teste die Präsentation im Vollbild und lade danach die HTML-Datei herunter.</p>
              <label>HTML-Code hier einfügen<textarea data-html-runner-input data-no-store data-ignore-completion spellcheck="false" placeholder="&lt;!doctype html&gt; ..."></textarea></label>
              <div class="html-runner-actions">
                <button class="html-runner-start" type="button" data-html-runner-start>▶ Fullscreen testen</button>
                <button class="html-runner-start html-runner-download" type="button" data-html-download>↓ HTML herunterladen</button>
                <span class="html-runner-status" data-html-runner-status aria-live="polite"></span>
              </div>
            </div>

            <div class="auftrag-grid submission-grid">
              <div class="auftrag-card">
                <strong>1. PDF erstellen</strong>
                <p>Erstelle jetzt die PDF-Abgabe mit deinen Antworten aus diesem Startcheck.</p>
                <div class="submission-actions"><button class="check-button" type="button" data-submit-pdf>PDF erstellen</button></div>
              </div>
              <div class="auftrag-card">
                <strong>2. Outlook öffnen</strong>
                <p>Öffne Outlook und erstelle eine neue Nachricht an deine Lehrperson.</p>
                <div class="submission-actions">
                  <a class="outlook-link" href="https://outlook.cloud.microsoft/" target="_blank" rel="noopener noreferrer">
                    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.5 6.5h17v11h-17z"></path><path d="m4 7 8 6 8-6"></path></svg>
                    Outlook öffnen
                  </a>
                </div>
              </div>
            </div>

            <div class="final-box">
              <strong>📎 Diese Dateien an die Mail anhängen</strong>
              <p><strong>HTML-Variante:</strong> PDF + HTML-Datei<br><strong>PowerPoint-Variante:</strong> PDF + PowerPoint-Datei (.pptx)</p>
            </div>

            <div class="check-grid">
              <label class="choice"><input type="checkbox" name="mail-submission" value="sent"> Ich habe die richtigen Dateien angehängt und die Mail gesendet.</label>
            </div>
          </div>
        </div>
      </section>'''

marker = '''      </section>
      </div>

      <div class="slide-controls" aria-label="Navigation">'''
pos = text.rfind(marker)
assert pos != -1
text = text[:pos+len('      </section>')] + submission + text[pos+len('      </section>'):]

# The PDF action now lives in task 08; keep only JSON in the bottom utility area.
text = text.replace('''          <button class="print-final" type="button" data-print-final>Drucken / PDF</button>
          <button class="download-json" type="button" data-download-json>JSON herunterladen</button>''', '''          <button class="download-json" type="button" data-download-json>JSON herunterladen</button>''', 1)

css_marker = '''    .html-runner-status { color: var(--muted); font-weight: 750; }
'''
css_add = '''    .html-runner-status { color: var(--muted); font-weight: 750; }
    .html-runner-download {
      background: var(--control-bg);
      color: var(--control-color);
      border: 1px solid var(--line);
    }
    .submission-actions {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-top: 14px;
    }
    .outlook-link {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      min-height: 44px;
      padding: 10px 15px;
      border-radius: 999px;
      background: var(--accent, var(--violet));
      color: #fff;
      text-decoration: none;
      font-weight: 850;
      box-shadow: 0 10px 24px rgba(15, 23, 42, .12);
      transition: filter .16s ease, transform .16s ease, box-shadow .16s ease;
    }
    .outlook-link svg {
      width: 20px;
      height: 20px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .outlook-link:hover,
    .outlook-link:focus-visible {
      filter: brightness(1.06);
      box-shadow: 0 10px 24px rgba(15, 23, 42, .12), 0 0 0 3px color-mix(in srgb, var(--accent, var(--violet)) 18%, transparent);
      outline: 0;
    }
    .outlook-link:active { transform: scale(.97); }
'''
assert css_marker in text
text = text.replace(css_marker, css_add, 1)

# Query download control.
query_marker = '''      const htmlRunnerStart = document.querySelector("[data-html-runner-start]");
      const htmlRunnerStatus = document.querySelector("[data-html-runner-status]");'''
query_repl = '''      const htmlRunnerStart = document.querySelector("[data-html-runner-start]");
      const htmlRunnerDownload = document.querySelector("[data-html-download]");
      const htmlRunnerStatus = document.querySelector("[data-html-runner-status]");'''
assert query_marker in text
text = text.replace(query_marker, query_repl, 1)

# Add raw HTML download. It intentionally downloads the pupil's own HTML, without the preview bridge.
listener_marker = '''      htmlRunnerStart?.addEventListener("click", startPresentation);
      presentationBack?.addEventListener("click", () => closePresentation());'''
listener_repl = '''      htmlRunnerStart?.addEventListener("click", startPresentation);
      htmlRunnerDownload?.addEventListener("click", () => {
        if (!htmlRunnerInput) return;
        const html = cleanPastedHtml(htmlRunnerInput.value);
        if (!html) {
          runnerStatus("Bitte zuerst den HTML-Code einfügen.", true);
          htmlRunnerInput.focus();
          return;
        }
        const rawName = (goodFilenameInput?.value || `${studentName || "praesentation"}_praesentation`).trim();
        const baseName = rawName.replace(/\\.(pptx|html?)$/i, "").replace(/[^a-z0-9äöüéèà_-]+/gi, "-").replace(/^-+|-+$/g, "") || "praesentation";
        const blob = new Blob([html], { type: "text/html;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${baseName}.html`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(url), 0);
        runnerStatus("HTML-Datei wurde heruntergeladen.");
      });
      presentationBack?.addEventListener("click", () => closePresentation());'''
assert listener_marker in text
text = text.replace(listener_marker, listener_repl, 1)

# Printing must be possible before the mail task itself is marked as sent.
missing_marker = '''        return taskTiles.filter((tile) => !tile.classList.contains("is-done"));'''
missing_repl = '''        return taskTiles.filter((tile) => tile.dataset.taskTarget !== "task-9" && !tile.classList.contains("is-done"));'''
assert missing_marker in text
text = text.replace(missing_marker, missing_repl, 1)

print_listener = '''      printButton?.addEventListener("click", handlePrint);'''
print_repl = '''      printButton?.addEventListener("click", handlePrint);
      document.querySelector("[data-submit-pdf]")?.addEventListener("click", handlePrint);'''
assert print_listener in text
text = text.replace(print_listener, print_repl, 1)

# Sanity checks
assert 'data-task-target="task-9"' in text
assert 'data-task="task-9"' in text
assert 'https://outlook.cloud.microsoft/' in text
assert 'data-html-download' in text
assert text.count('data-html-runner-input') >= 2

path.write_text(text, encoding='utf-8')
