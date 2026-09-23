from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Group each keyboard action into its own small framed control.
old_css = '''    .runner-shortcuts {
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
'''
new_css = '''    .runner-shortcuts {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 14px;
      flex-wrap: wrap;
    }
    .runner-shortcut {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      min-height: 42px;
      padding: 5px 9px;
      border: 1px solid color-mix(in srgb, var(--slide-text) 10%, var(--line));
      border-radius: 12px;
      background: color-mix(in srgb, var(--control-bg) 84%, transparent);
      color: var(--muted);
      box-shadow: 0 3px 10px rgba(15, 23, 42, .05);
      font-size: .88em;
      font-weight: 750;
      white-space: nowrap;
    }
    .runner-shortcut-next { gap: 6px; }
'''
assert s.count(old_css) == 1
s = s.replace(old_css, new_css)

# 2) Add school mail login hint to Outlook card.
old_outlook = '''              <div class="auftrag-card">
                <strong>2. Outlook öffnen</strong>
                <p>Öffne Outlook und erstelle eine neue Nachricht an deine Lehrperson.</p>
                <div class="submission-actions">
'''
new_outlook = '''              <div class="auftrag-card">
                <strong>2. Outlook öffnen</strong>
                <p>Öffne Outlook und erstelle eine neue Nachricht an deine Lehrperson.</p>
                <p class="school-mail-hint">Deine Schul-Mailadresse: <span class="school-mail-address">vorname.nachname@sus.gsu-so.ch</span></p>
                <div class="submission-actions">
'''
assert s.count(old_outlook) == 1
s = s.replace(old_outlook, new_outlook)

# 3) Replace emoji clip with a real SVG paperclip and insert an ODER pill.
old_title = '''              <div class="submission-files-title" id="submission-files-title"><span aria-hidden="true">📎</span><strong>Diese Dateien an die Mail anhängen</strong></div>'''
new_title = '''              <div class="submission-files-title" id="submission-files-title">
                <svg class="submission-paperclip" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m20.5 11.5-8.7 8.7a6 6 0 0 1-8.5-8.5l9.2-9.2a4.25 4.25 0 0 1 6 6l-9.2 9.2a2.5 2.5 0 1 1-3.5-3.5l8.5-8.5"></path></svg>
                <strong>Diese Dateien an die Mail anhängen</strong>
              </div>'''
assert s.count(old_title) == 1
s = s.replace(old_title, new_title)

old_between = '''              </div>
              <div class="submission-file-row">
                <span class="submission-file-variant">PowerPoint</span>'''
new_between = '''              </div>
              <div class="submission-or" aria-hidden="true"><span>ODER</span></div>
              <div class="submission-file-row">
                <span class="submission-file-variant">PowerPoint</span>'''
# Restrict to the attachment block occurrence by verifying exactly one after current markup.
assert s.count(old_between) >= 1
idx = s.find('class="submission-files"')
pos = s.find(old_between, idx)
assert pos >= 0
s = s[:pos] + s[pos:].replace(old_between, new_between, 1)

# 4) Styling for real clip, ODER divider and school email hint.
anchor = '''    .submission-file-row {
      display: grid;
'''
extra_css = '''    .submission-paperclip {
      width: 23px;
      height: 23px;
      flex: 0 0 auto;
      fill: none;
      stroke: currentColor;
      stroke-width: 1.9;
      stroke-linecap: round;
      stroke-linejoin: round;
      color: var(--slide-title);
    }
    .school-mail-hint {
      margin-top: 10px !important;
      color: var(--muted) !important;
      font-size: .92em;
    }
    .school-mail-address {
      display: inline-flex;
      align-items: center;
      margin-top: 5px;
      padding: 5px 9px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--field-bg);
      color: var(--slide-title);
      font-family: Consolas, "Courier New", monospace;
      font-weight: 800;
      overflow-wrap: anywhere;
    }
    .submission-or {
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 8px 0;
      color: var(--muted);
    }
    .submission-or::before,
    .submission-or::after {
      content: "";
      height: 1px;
      flex: 1 1 auto;
      background: color-mix(in srgb, var(--green) 18%, var(--line));
    }
    .submission-or span {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 30px;
      padding: 0 12px;
      border: 1px solid color-mix(in srgb, var(--green) 18%, var(--line));
      border-radius: 999px;
      background: var(--control-bg);
      color: var(--muted);
      font-size: .8em;
      font-weight: 900;
      letter-spacing: .06em;
      box-shadow: 0 2px 7px rgba(15, 23, 42, .05);
    }
'''
assert s.count(anchor) == 1
s = s.replace(anchor, extra_css + anchor)

assert '<span>ODER</span>' in s
assert 'submission-paperclip' in s
assert 'vorname.nachname@sus.gsu-so.ch' in s
assert 'runner-shortcut' in s and 'min-height: 42px' in s

p.write_text(s, encoding='utf-8')
