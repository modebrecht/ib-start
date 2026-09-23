from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_css = '''    .school-mail-address {
      display: inline-flex;
      align-items: center;
      margin-top: 5px;
      padding: 5px 9px;
'''
new_css = '''    .school-mail-address {
      display: inline-flex;
      align-items: center;
      margin: 0 0 0 6px;
      vertical-align: middle;
      padding: 5px 9px;
'''

old_markup = '''                <p>Öffne Outlook und erstelle eine neue Nachricht an deine Lehrperson.</p>
                <p class="school-mail-hint">Deine Schul-Mailadresse: <span class="school-mail-address">vorname.nachname@sus.gsu-so.ch</span></p>
'''
new_markup = '''                <p>Öffne Outlook und erstelle eine neue Nachricht an deine Lehrperson. <span class="school-mail-address">vorname.nachname@sus.gsu-so.ch</span></p>
'''

for old, new, label in [
    (old_css, new_css, 'school mail chip CSS'),
    (old_markup, new_markup, 'Outlook instruction markup'),
]:
    if old not in text:
        raise SystemExit(f'Missing expected block: {label}')
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
