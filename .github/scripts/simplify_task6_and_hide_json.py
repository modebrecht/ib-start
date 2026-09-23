from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Put JSON export in settings.
settings_anchor = '''                <div class="settings-group">
                  <span class="settings-title">Admin Mode</span>
'''
settings_export = '''                <div class="settings-group settings-export">
                  <span class="settings-title">Export</span>
                  <button class="download-json settings-json" type="button" data-download-json>JSON herunterladen</button>
                  <span class="admin-status" data-json-status aria-live="polite"></span>
                </div>
                <div class="settings-group">
                  <span class="settings-title">Admin Mode</span>
'''
assert s.count(settings_anchor) == 1
s = s.replace(settings_anchor, settings_export)

# 2) Prompt help is always visible; remove the useless final checkbox.
old_task6 = '''            <details class="prompt-box">
              <summary class="prompt-head"><span class="prompt-summary-label">Hilfe für deinen Prompt anzeigen</span></summary>
              <pre class="prompt-code"><code>Schreibe deinen Prompt selbst.

Diese Informationen müssen in deiner Präsentation vorkommen:
• Titel / dein Vorname
• Mindestens 3 Hobbys oder Interessen
• Dein Lieblingstier und dein Lieblingsessen
• Apps oder Games, die du gerne nutzt
• Was du im Informatikunterricht lernen möchtest

Beispiele für das, was du lernen möchtest:
• KI sinnvoll nutzen oder Medien mit KI erstellen
• Word, Excel und PowerPoint nutzen
• Webseiten machen
• kleine Apps oder Games programmieren

Verwende nur Informationen, die du laut Aufgabe 02 mit einer KI teilen darfst.
Du entscheidest selbst, wie die Präsentation aussehen soll.
Passt das Ergebnis nicht? Verbessere deinen Prompt und probiere erneut.</code></pre>
            </details>

            <span class="label" style="display:block; margin-top:24px;">Wenn du fertig bist:</span>
            <div class="check-grid">
              <label class="choice"><input type="checkbox" name="created" value="finished"> Meine Präsentation ist fertig und gespeichert.</label>
            </div>
'''
new_task6 = '''            <div class="prompt-box prompt-box-static">
              <div class="prompt-head"><span>Hilfe für deinen Prompt</span></div>
              <pre class="prompt-code"><code>Schreibe deinen Prompt selbst.

Diese Informationen müssen in deiner Präsentation vorkommen:
• Titel / dein Vorname
• Mindestens 3 Hobbys oder Interessen
• Dein Lieblingstier und dein Lieblingsessen
• Apps oder Games, die du gerne nutzt
• Was du im Informatikunterricht lernen möchtest

Beispiele für das, was du lernen möchtest:
• KI sinnvoll nutzen oder Medien mit KI erstellen
• Word, Excel und PowerPoint nutzen
• Webseiten machen
• kleine Apps oder Games programmieren

Verwende nur Informationen, die du laut Aufgabe 02 mit einer KI teilen darfst.
Du entscheidest selbst, wie die Präsentation aussehen soll.
Passt das Ergebnis nicht? Verbessere deinen Prompt und probiere erneut.</code></pre>
            </div>
'''
assert s.count(old_task6) == 1
s = s.replace(old_task6, new_task6)

# 3) Remove the public JSON action from the bottom navigation.
old_final_actions = '''        <div class="final-actions" data-final-actions>
          <button class="download-json" type="button" data-download-json>JSON herunterladen</button>
        </div>
'''
assert s.count(old_final_actions) == 1
s = s.replace(old_final_actions, '')

# 4) Static prompt box styling instead of collapsible details styling.
old_prompt_css = '''    .prompt-box summary {
      list-style: none;
      cursor: pointer;
    }

    .prompt-box summary::-webkit-details-marker {
      display: none;
    }

'''
assert s.count(old_prompt_css) == 1
s = s.replace(old_prompt_css, '')

old_open_css = '''    .prompt-box[open] .prompt-head {
      border-bottom: 1px solid var(--line);
    }

    .prompt-summary-label::before {
      content: "▸";
      display: inline-block;
      margin-right: 8px;
      transition: transform .16s ease;
    }

    .prompt-box[open] .prompt-summary-label::before {
      transform: rotate(90deg);
    }

'''
assert s.count(old_open_css) == 1
s = s.replace(old_open_css, '''    .prompt-box-static .prompt-head {
      border-bottom: 1px solid var(--line);
    }

''')

# 5) Make JSON export fit the settings panel and keep generic button CSS away from it.
css_anchor = '''    .admin-status.is-error {
      color: var(--red);
    }

'''
css_add = '''    .admin-status.is-error {
      color: var(--red);
    }

    .settings-json {
      width: 100%;
      min-height: 42px;
      border-radius: 10px;
      padding: 0 14px;
      box-shadow: none;
    }

'''
assert s.count(css_anchor) == 1
s = s.replace(css_anchor, css_add)

old_generic = '''button:not(.match-item):not(.task-tile):not(.round-nav):not(.print-final):not(.copy-prompt):not(.check-button):not(.read-button):not(.settings-button):not(.admin-unlock):not(.html-runner-start):not(.presentation-back):not(.pdf-lock-close):not(.pdf-lock-dismiss)'''
new_generic = '''button:not(.match-item):not(.task-tile):not(.round-nav):not(.print-final):not(.download-json):not(.copy-prompt):not(.check-button):not(.read-button):not(.settings-button):not(.admin-unlock):not(.html-runner-start):not(.presentation-back):not(.pdf-lock-close):not(.pdf-lock-dismiss)'''
assert s.count(old_generic) == 1
s = s.replace(old_generic, new_generic)

# 6) Keep JSON feedback inside settings instead of at the bottom of the page.
old_const = '''      const downloadJsonButton = document.querySelector("[data-download-json]");
      const finalActions = document.querySelector("[data-final-actions]");
      const printStatus = document.querySelector("[data-print-status]");
'''
new_const = '''      const downloadJsonButton = document.querySelector("[data-download-json]");
      const jsonStatus = document.querySelector("[data-json-status]");
      const finalActions = document.querySelector("[data-final-actions]");
      const printStatus = document.querySelector("[data-print-status]");
'''
assert s.count(old_const) == 1
s = s.replace(old_const, new_const)

old_json_status = '''        setPrintStatus("JSON-Datensicherung wurde heruntergeladen.", "admin");
'''
new_json_status = '''        if (jsonStatus) jsonStatus.textContent = "JSON heruntergeladen.";
'''
assert s.count(old_json_status) == 1
s = s.replace(old_json_status, new_json_status)

# Sanity checks.
assert 'Hilfe für deinen Prompt anzeigen' not in s
assert 'Meine Präsentation ist fertig und gespeichert.' not in s
assert s.count('data-download-json') == 2  # HTML + JS selector
assert s.count('class="download-json settings-json"') == 1
assert s.count('data-json-status') == 2  # HTML + JS selector
assert 'data-final-actions' in s  # JS selector remains harmless; markup is removed.

p.write_text(s, encoding='utf-8')
