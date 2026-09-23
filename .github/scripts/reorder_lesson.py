from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

stage_start = text.index('      <div class="task-stage">')
controls_start = text.index('\n\n      <div class="slide-controls"', stage_start)
stage_blob = text[stage_start:controls_start]
section_pattern = re.compile(
    r'      <section class="section(?: is-active)?" data-task="(task-\d+)"[\s\S]*?\n      </section>'
)
sections = {m.group(1): m.group(0) for m in section_pattern.finditer(stage_blob)}
required = {"task-1", "task-2", "task-3", "task-4", "task-6", "task-7", "task-8"}
missing = required - sections.keys()
if missing:
    raise SystemExit(f"Missing expected task sections: {sorted(missing)}")

nav_start = text.index('      <nav class="task-nav" aria-label="Aufgaben">')
nav_end = text.index('      </nav>', nav_start) + len('      </nav>')
new_nav = '''      <nav class="task-nav" aria-label="Aufgaben">
        <button class="task-tile is-active" type="button" data-task-target="task-1" style="--tile-color: var(--red)"><span class="task-number">01</span><span class="task-label">Mini-Präsentation</span></button>
        <button class="task-tile" type="button" data-task-target="task-6" style="--tile-color: var(--indigo)"><span class="task-number">02</span><span class="task-label">Was darf ich teilen?</span></button>
        <button class="task-tile" type="button" data-task-target="task-5" style="--tile-color: var(--orange)"><span class="task-number">03</span><span class="task-label">KI richtig nutzen</span></button>
        <button class="task-tile" type="button" data-task-target="task-3" style="--tile-color: var(--yellow)"><span class="task-number">04</span><span class="task-label">Gute Dateinamen erkennen</span></button>
        <button class="task-tile" type="button" data-task-target="task-7" style="--tile-color: var(--violet)"><span class="task-number">05</span><span class="task-label">Tastenkombinationen</span></button>
        <button class="task-tile" type="button" data-task-target="task-2" style="--tile-color: var(--green)"><span class="task-number">06</span><span class="task-label">Meine Präsentation</span></button>
        <button class="task-tile" type="button" data-task-target="task-8" style="--tile-color: var(--cyan)"><span class="task-number">07</span><span class="task-label">Rückblick</span></button>
      </nav>'''
text = text[:nav_start] + new_nav + text[nav_end:]

task1 = '''      <section class="section is-active" data-task="task-1" style="--accent: var(--red)">
        <div class="section-number"><span>01</span><span>★</span></div>
        <div class="section-body">
          <h2 class="section-title">Mini-Präsentation</h2>
          <div class="section-content">
            <p class="auftrag-intro"><strong>Das ist dein Ziel für heute:</strong> Am Ende erstellst du eine kurze Präsentation über dich.</p>

            <div class="auftrag-grid">
              <div class="auftrag-card"><strong>1. Titel / Vorname</strong><p>Beispiel: «Kurzvorstellung – Lina»</p></div>
              <div class="auftrag-card"><strong>2. Hobbys und Interessen</strong><p>Mindestens drei Beispiele, die zu dir passen.</p></div>
              <div class="auftrag-card"><strong>3. Lieblingstier und Lieblingsessen</strong><p>Welches Tier und welches Essen magst du am liebsten?</p></div>
              <div class="auftrag-card"><strong>4. Apps oder Games</strong><p>Welche Apps oder Games nutzt du gerne?</p></div>
              <div class="auftrag-card"><strong>5. Was ich im IB lernen möchte</strong><p>Zum Beispiel KI, Word, Excel, PowerPoint, Webseiten oder kleine Apps und Games.</p></div>
            </div>

            <div class="final-box">
              <strong>🏁 Später wählst du</strong>
              <p><strong>PowerPoint oder HTML mit KI.</strong> Beide Varianten sind gleichwertig. Die nächsten Aufgaben bereiten dich darauf vor.</p>
              <div class="read-actions"><button class="read-button" type="button" data-read-confirm="task-1-brief" aria-pressed="false">Auftrag verstanden</button></div>
            </div>
          </div>
        </div>
      </section>'''

task5 = '''      <section class="section" data-task="task-5" style="--accent: var(--orange)">
        <div class="section-number"><span>03</span><span>✦</span></div>
        <div class="section-body">
          <h2 class="section-title">KI richtig nutzen</h2>
          <div class="section-content">
            <p class="auftrag-intro">Ein guter Prompt sagt der KI klar, <strong>was</strong> sie machen soll und <strong>welche Inhalte</strong> wichtig sind.</p>
            <span class="label">Welche Prompts sind gut? Es können mehrere Antworten richtig sein.</span>
            <div class="prompt-list">
              <label class="choice"><input type="checkbox" name="prompt-quality-generic" value="bad" data-prompt-answer> Mach eine Präsentation.</label>
              <label class="choice"><input type="checkbox" name="prompt-quality-detailed" value="good" data-prompt-answer> Erstelle eine Präsentation mit 5 Folien über mich. Verwende meinen Vornamen, 3 Hobbys, mein Lieblingstier und mein Lieblingsessen.</label>
              <label class="choice"><input type="checkbox" name="prompt-quality-vague" value="bad" data-prompt-answer> Mach etwas Schönes.</label>
              <label class="choice"><input type="checkbox" name="prompt-quality-hobby" value="good" data-prompt-answer> Erstelle eine Präsentation über mein Hobby Tennis mit Titel, 3 Fakten, Bildidee und Abschlussfolie.</label>
            </div>
            <label>Warum ist ein genauer Prompt besser?<textarea name="prompt-reason"></textarea></label>
            <div class="check-actions">
              <button class="check-button" type="button" data-check-task="task-5">Prompt-Check prüfen</button>
              <span class="check-status" data-check-status="task-5" aria-live="polite"></span>
            </div>
          </div>
        </div>
      </section>'''

task2 = '''      <section class="section" data-task="task-2" style="--accent: var(--green)">
        <div class="section-number"><span>06</span><span>▣</span></div>
        <div class="section-body">
          <h2 class="section-title">Meine Präsentation</h2>
          <div class="section-content">
            <p class="auftrag-intro"><strong>Jetzt setzt du alles zusammen.</strong> Erstelle deine Mini-Präsentation aus Aufgabe 01.</p>

            <span class="label">Wähle deine Variante:</span>
            <div class="check-grid">
              <label class="choice"><input type="checkbox" name="created" value="powerpoint"> PowerPoint-Präsentation</label>
              <label class="choice"><input type="checkbox" name="created" value="html"> HTML-Präsentation mit KI</label>
            </div>

            <div class="auftrag-grid">
              <div class="auftrag-card">
                <strong>PowerPoint – so gehst du vor</strong>
                <ol class="auftrag-list">
                  <li>PowerPoint öffnen und die Inhalte aus Aufgabe 01 verwenden.</li>
                  <li>Deinen Dateinamen aus Aufgabe 04 verwenden und speichern.</li>
                  <li>Die Präsentation mit <strong>F5</strong> testen.</li>
                  <li>Datei abgeben oder per Outlook senden.</li>
                </ol>
              </div>
              <div class="auftrag-card">
                <strong>HTML mit KI – so gehst du vor</strong>
                <ol class="auftrag-list">
                  <li>Deinen eigenen Prompt schreiben. Beachte Aufgabe 02 und 03.</li>
                  <li>Die HTML-Präsentation von der KI erstellen lassen.</li>
                  <li>Den HTML-Code unten einfügen und im Vollbild testen.</li>
                  <li>Datei sinnvoll benennen, speichern und abgeben.</li>
                </ol>
              </div>
            </div>

            <details class="prompt-box">
              <summary class="prompt-head"><span class="prompt-summary-label">Hilfe für deinen KI-Prompt anzeigen</span></summary>
              <pre class="prompt-code"><code>Schreibe deinen Prompt selbst.

Diese Informationen müssen in deiner Präsentation vorkommen:
• Titel / dein Vorname
• Mindestens 3 Hobbys oder Interessen
• Dein Lieblingstier und dein Lieblingsessen
• Apps oder Games, die du gerne nutzt
• Was du im Informatikunterricht lernen möchtest

Beispiele für das, was du lernen möchtest:
• mit KI umgehen oder Medien mit KI erstellen
• Word, Excel und PowerPoint nutzen
• Webseiten machen
• kleine Apps oder Games programmieren

Nutze nur Informationen, die du laut Aufgabe 02 teilen darfst.
Du entscheidest selbst, wie die Präsentation aussehen soll.
Passt das Ergebnis nicht? Verbessere deinen Prompt und probiere erneut.</code></pre>
            </details>

            <div class="html-runner">
              <div class="html-runner-head"><strong>HTML-Präsentation testen</strong><span>Esc zurück · ← vorherige · → / ↓ / Leertaste nächste</span></div>
              <p class="auftrag-intro">Eine Präsentation muss auch auf einem grossen Bildschirm oder Beamer gut aussehen und funktionieren. Teste sie deshalb im Vollbild.</p>
              <label>HTML-Code hier einfügen<textarea data-html-runner-input data-no-store data-ignore-completion spellcheck="false" placeholder="&lt;!doctype html&gt; ..."></textarea></label>
              <div class="html-runner-actions"><button class="html-runner-start" type="button" data-html-runner-start>▶ Fullscreen starten</button><span class="html-runner-status" data-html-runner-status aria-live="polite"></span></div>
            </div>

            <span class="label" style="display:block; margin-top:24px;">Zum Schluss:</span>
            <div class="check-grid"><label class="choice"><input type="checkbox" name="created" value="submitted"> Ich habe meine Präsentation gespeichert und abgegeben.</label></div>
          </div>
        </div>
      </section>'''

task6 = sections["task-6"].replace('<div class="section-number"><span>05</span>', '<div class="section-number"><span>02</span>', 1)
task3 = sections["task-3"].replace('<div class="section-number"><span>03</span>', '<div class="section-number"><span>04</span>', 1)
task3 = task3.replace('Mein guter Dateiname', 'Dein Dateiname', 1)
task7 = sections["task-7"].replace('<div class="section-number"><span>06</span>', '<div class="section-number"><span>05</span>', 1)
task8 = sections["task-8"]

new_stage = '      <div class="task-stage">\n' + '\n\n'.join([task1, task6, task5, task3, task7, task2, task8]) + '\n      </div>'
stage_start = text.index('      <div class="task-stage">')
controls_start = text.index('\n\n      <div class="slide-controls"', stage_start)
text = text[:stage_start] + new_stage + text[controls_start:]

text, count = re.subn(
    r'''      const goodFilenameInput = document\.querySelector\('input\[name="good-filename"\]'\);\n      const filenameCheckInput = document\.querySelector\('input\[name="filename-check"\]'\);\n      const syncGoodFilename = \(\) => \{[\s\S]*?      goodFilenameInput\?\.addEventListener\("input", syncGoodFilename\);\n''',
    '''      const goodFilenameInput = document.querySelector('input[name="good-filename"]');\n''',
    text,
    count=1
)
if count != 1:
    raise SystemExit(f"Expected to remove filename sync once, got {count}")

old_needs = '      const taskNeedsSolved = (taskId) => taskId === "task-1" || taskId === "task-3" || taskId === "task-4" || taskId === "task-6" || taskId === "task-7";'
new_needs = '      const taskNeedsSolved = (taskId) => taskId === "task-3" || taskId === "task-5" || taskId === "task-6" || taskId === "task-7";'
if old_needs not in text:
    raise SystemExit("taskNeedsSolved marker not found")
text = text.replace(old_needs, new_needs, 1)
text = text.replace('\n      syncGoodFilename();\n', '\n', 1)

text = text.replace('setCheckStatus("task-3", "Gespeichert: Aufgabe 03 ist richtig gelöst.", "success");', 'setCheckStatus("task-3", "Gespeichert: Aufgabe 04 ist richtig gelöst.", "success");')
text = text.replace('setCheckStatus("task-7", "Gespeichert: Aufgabe 06 ist richtig gelöst.", "success");', 'setCheckStatus("task-7", "Gespeichert: Aufgabe 05 ist richtig gelöst.", "success");')
text, count = re.subn(r'''\n      if \(saved\.solvedTasks\?\.\["task-4"\]\) \{\n        setCheckStatus\("task-4", "Gespeichert: Aufgabe 04 ist richtig gelöst\.", "success"\);\n      \}\n''', '\n', text, count=1)
if count != 1:
    raise SystemExit(f"Expected one task-4 saved status block, got {count}")

prompt_start = text.index('      const promptInputs = [...document.querySelectorAll("[data-prompt-answer]")];')
filename_start = text.index('      const filenameAnswers = {', prompt_start)
new_prompt_logic = '''      const promptInputs = [...document.querySelectorAll("[data-prompt-answer]")];
      const isPromptTaskSolved = () => promptInputs.length > 0 && promptInputs.every((input) => input.value === "good" ? input.checked : !input.checked);

      const legacyPromptSolved = saved.solvedTasks?.["task-1"] === true || saved.solvedTasks?.["task-5"] === true;
      if (legacyPromptSolved && saved.solvedTasks?.["task-5"] !== true) {
        const next = readSaved();
        next.solvedTasks = { ...(next.solvedTasks || {}), "task-5": true };
        writeSaved(next);
        saved.solvedTasks = next.solvedTasks;
      }

      if (saved.solvedTasks?.["task-5"]) {
        if (isPromptTaskSolved()) setCheckStatus("task-5", "Gespeichert: Prompt-Check richtig gelöst.", "success");
        else {
          const next = readSaved();
          next.solvedTasks = { ...(next.solvedTasks || {}), "task-5": false };
          writeSaved(next);
        }
      }

      promptInputs.forEach((input) => input.addEventListener("change", () => {
        saveSolvedTask("task-5", false);
        setCheckStatus("task-5", "");
      }));

      document.querySelector('[data-check-task="task-5"]')?.addEventListener("click", () => {
        let correctChecked = 0;
        let correctTotal = 0;
        let wrongRemoved = 0;
        promptInputs.forEach((input) => {
          if (input.value === "good") {
            correctTotal += 1;
            if (input.checked) correctChecked += 1;
            return;
          }
          if (!input.checked) return;
          input.checked = false;
          syncChoiceState(input);
          const next = readSaved();
          next[input.dataset.storeKey] = false;
          writeSaved(next);
          wrongRemoved += 1;
        });
        const solved = wrongRemoved === 0 && correctChecked === correctTotal && isPromptTaskSolved();
        saveSolvedTask("task-5", solved);
        if (solved) setCheckStatus("task-5", "Richtig gelöst und gespeichert.", "success");
        else if (wrongRemoved > 0) setCheckStatus("task-5", "Nicht passende Haken entfernt. Prüfe deine Auswahl nochmal.", "error");
        else setCheckStatus("task-5", "Noch nicht alle guten Prompts ausgewählt.", "error");
      });

'''
text = text[:prompt_start] + new_prompt_logic + text[filename_start:]

text, count = re.subn(r'''\n      const task4Fields = \[[\s\S]*?\n      const privacyInputs =''', '\n      const privacyInputs =', text, count=1)
if count != 1:
    raise SystemExit(f"Expected one task4Fields block, got {count}")

expected_order = ['data-task-target="task-1"', 'data-task-target="task-6"', 'data-task-target="task-5"', 'data-task-target="task-3"', 'data-task-target="task-7"', 'data-task-target="task-2"', 'data-task-target="task-8"']
nav_slice = text[text.index('<nav class="task-nav"'):text.index('</nav>', text.index('<nav class="task-nav"'))]
positions = [nav_slice.index(item) for item in expected_order]
if positions != sorted(positions):
    raise SystemExit("Task navigation order is wrong")

for forbidden in ['data-task="task-4"', 'data-task-target="task-4"', 'data-check-task="task-4"', 'task4Fields', 'filename-check', 'fullscreen-check']:
    if forbidden in text:
        raise SystemExit(f"Obsolete task-4 marker still present: {forbidden}")

if text.count('data-task="task-5"') != 1:
    raise SystemExit("Expected exactly one KI task")
if text.count('data-task="task-2"') != 1:
    raise SystemExit("Expected exactly one final presentation task")
if 'Hilfe für deinen KI-Prompt anzeigen' not in text:
    raise SystemExit("Prompt help was not moved to final presentation")
if 'Dein Dateiname' not in text:
    raise SystemExit("Own filename field label missing")

path.write_text(text, encoding="utf-8")
