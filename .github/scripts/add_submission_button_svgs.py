from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = {
'''<button class="html-runner-start" type="button" data-html-runner-start><span aria-hidden="true">▶</span> Fullscreen testen</button>''': '''<button class="html-runner-start" type="button" data-html-runner-start><svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 3H3v5"></path><path d="m3 3 6 6"></path><path d="M16 3h5v5"></path><path d="m21 3-6 6"></path><path d="M8 21H3v-5"></path><path d="m3 21 6-6"></path><path d="M16 21h5v-5"></path><path d="m21 21-6-6"></path></svg> Fullscreen testen</button>''',
'''<button class="html-runner-start html-runner-download" type="button" data-html-download><span aria-hidden="true">↓</span> HTML herunterladen</button>''': '''<button class="html-runner-start html-runner-download" type="button" data-html-download><svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3v12"></path><path d="m7 10 5 5 5-5"></path><path d="M5 21h14"></path></svg> HTML herunterladen</button>''',
'''<div class="submission-actions"><button class="check-button" type="button" data-submit-pdf>PDF erstellen</button></div>''': '''<div class="submission-actions"><button class="check-button submission-action-button" type="button" data-submit-pdf><svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path><path d="M12 11v7"></path><path d="m9 15 3 3 3-3"></path></svg> PDF erstellen</button></div>''',
'''<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.5 6.5h17v11h-17z"></path><path d="m4 7 8 6 8-6"></path></svg>\n                    Outlook öffnen''': '''<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.5 6.5h17v11h-17z"></path><path d="m4 7 8 6 8-6"></path></svg>\n                    Outlook öffnen'''
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'Missing expected markup: {old[:90]}')
    text = text.replace(old, new, 1)

css_anchor = '''    .html-runner-start:active { transform: scale(.97); }\n'''
css = '''    .action-icon {\n      width: 20px;\n      height: 20px;\n      flex: 0 0 auto;\n      fill: none;\n      stroke: currentColor;\n      stroke-width: 2;\n      stroke-linecap: round;\n      stroke-linejoin: round;\n    }\n    .submission-action-button {\n      display: inline-flex;\n      align-items: center;\n      justify-content: center;\n      gap: 8px;\n    }\n'''
if css_anchor not in text:
    raise SystemExit('CSS anchor missing')
text = text.replace(css_anchor, css_anchor + css, 1)

path.write_text(text, encoding='utf-8')
