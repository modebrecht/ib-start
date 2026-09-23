from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_css = '''    .round-nav[data-slide-home] {
      padding-bottom: 3px;
      font-size: 1.6em;
    }
'''
new_css = '''    .round-nav svg {
      width: 22px;
      height: 22px;
      display: block;
      fill: none;
      stroke: currentColor;
      stroke-width: 2.25;
      stroke-linecap: round;
      stroke-linejoin: round;
      pointer-events: none;
    }
'''
if old_css not in text:
    raise SystemExit('Expected old home icon CSS not found')
text = text.replace(old_css, new_css, 1)

old_disabled = '''    .round-nav:disabled {
      opacity: .36;
      cursor: default;
      box-shadow: none;
      transform: none;
    }
'''
new_disabled = '''    .round-nav:disabled {
      opacity: .30;
      cursor: default;
      box-shadow: none;
      transform: none;
    }
'''
if old_disabled not in text:
    raise SystemExit('Expected disabled nav CSS not found')
text = text.replace(old_disabled, new_disabled, 1)

old_markup = '''          <button class="round-nav" type="button" data-slide-home aria-label="Zu Aufgabe 1" title="Aufgabe 1">⌂</button>
          <button class="round-nav" type="button" data-slide-prev aria-label="Vorheriges Thema">&lt;</button>
          <button class="round-nav" type="button" data-slide-next aria-label="Nächstes Thema">&gt;</button>'''
new_markup = '''          <button class="round-nav" type="button" data-slide-home aria-label="Zu Aufgabe 1" title="Aufgabe 1">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 10.5 12 3l9 7.5"></path><path d="M5.5 9.5V21h13V9.5"></path></svg>
          </button>
          <button class="round-nav" type="button" data-slide-prev aria-label="Vorheriges Thema" title="Vorherige Aufgabe">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m15 18-6-6 6-6"></path></svg>
          </button>
          <button class="round-nav" type="button" data-slide-next aria-label="Nächstes Thema" title="Nächste Aufgabe">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m9 18 6-6-6-6"></path></svg>
          </button>'''
if old_markup not in text:
    raise SystemExit('Expected old navigation markup not found')
text = text.replace(old_markup, new_markup, 1)

path.write_text(text, encoding='utf-8')
