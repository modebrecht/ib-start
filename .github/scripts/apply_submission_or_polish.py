from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_css = '''    .submission-paperclip {
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
'''
new_css = '''    .submission-clip {
      width: 22px;
      height: 22px;
      stroke: currentColor;
      stroke-width: 1.9;
      fill: none;
      color: var(--slide-title);
      flex: 0 0 auto;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
'''
assert old_css in s
s = s.replace(old_css, new_css, 1)

old_or_css = '''    .submission-or {
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
new_or_css = '''    .submission-or-pill {
      display: flex;
      align-items: center;
      justify-content: center;
      width: fit-content;
      min-height: 34px;
      padding: 0 16px;
      margin: 8px auto;
      border-radius: 999px;
      border: 1px solid color-mix(in srgb, var(--slide-text) 8%, var(--line));
      background: color-mix(in srgb, var(--control-bg) 88%, transparent);
      color: var(--muted);
      font-size: .8em;
      font-weight: 900;
      letter-spacing: .04em;
      box-shadow: 0 2px 7px rgba(15, 23, 42, .05);
    }
'''
assert old_or_css in s
s = s.replace(old_or_css, new_or_css, 1)

old_svg = '''<svg class="submission-paperclip" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m20.5 11.5-8.7 8.7a6 6 0 0 1-8.5-8.5l9.2-9.2a4.25 4.25 0 0 1 6 6l-9.2 9.2a2.5 2.5 0 1 1-3.5-3.5l8.5-8.5"></path></svg>'''
new_svg = '''<svg class="submission-clip" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8.5 12.5 14.8 6.2a3.5 3.5 0 1 1 5 5L10.9 20a5 5 0 1 1-7.1-7.1l9-9"></path></svg>'''
assert old_svg in s
s = s.replace(old_svg, new_svg, 1)

old_or = '''<div class="submission-or" aria-hidden="true"><span>ODER</span></div>'''
new_or = '''<div class="submission-or-pill" aria-hidden="true">ODER</div>'''
assert old_or in s
s = s.replace(old_or, new_or, 1)

assert 'submission-paperclip' not in s
assert 'class="submission-or"' not in s
assert s.count('class="submission-clip"') == 1
assert s.count('class="submission-or-pill"') == 1
assert 'vorname.nachname@sus.gsu-so.ch' in s

p.write_text(s, encoding='utf-8')
