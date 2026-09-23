from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '<p class="subtitle">Präsentieren · Speichern · KI nutzen</p>'
new = '<p class="subtitle">Einstieg in die Informatische Bildung</p>'
if old not in text:
    raise SystemExit('Expected old subtitle not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
