from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

repls = {
'''      --lesson-bg: rgba(255, 255, 255, .86);\n      --lesson-strong: #1d4ed8;\n      --lesson-sub: #334155;''':
'''      --lesson-bg: rgba(255, 255, 255, .70);\n      --lesson-strong: #1d4ed8;\n      --lesson-sub: #334155;''',
'''      --lesson-bg: rgba(15, 23, 42, .30);\n      --lesson-strong: #ffffff;\n      --lesson-sub: rgba(255, 255, 255, .80);''':
'''      --lesson-bg: rgba(15, 23, 42, .52);\n      --lesson-strong: #ffffff;\n      --lesson-sub: rgba(255, 255, 255, .86);''',
'''    .student-meta {\n      min-width: 180px;\n      text-align: left;\n      padding: 14px 16px;\n      border: 1px solid rgba(255, 255, 255, .34);\n      border-radius: 18px;\n      background: var(--lesson-bg);\n      box-shadow: 0 14px 34px rgba(15, 23, 42, .16);\n    }''':
'''    .student-meta {\n      min-width: 190px;\n      text-align: left;\n      padding: 16px 20px;\n      border: 1px solid rgba(255, 255, 255, .38);\n      border-radius: 22px;\n      background: var(--lesson-bg);\n      box-shadow: 0 12px 30px rgba(15, 23, 42, .13);\n      backdrop-filter: blur(12px) saturate(1.08);\n      -webkit-backdrop-filter: blur(12px) saturate(1.08);\n    }''',
'''    .student-meta strong {\n      display: block;\n      color: var(--lesson-strong);\n      font-size: 1.12em;\n    }''':
'''    .student-meta strong {\n      display: block;\n      margin-bottom: 4px;\n      color: var(--lesson-strong);\n      font-size: 1.14em;\n      line-height: 1.2;\n    }''',
'''    .student-meta span {\n      display: block;\n      color: var(--lesson-sub);\n      font-size: 1em;\n    }''':
'''    .student-meta span {\n      display: block;\n      color: var(--lesson-sub);\n      font-size: .98em;\n      line-height: 1.38;\n    }\n\n    .student-meta span + span {\n      margin-top: 2px;\n      font-size: .93em;\n    }''',
'''    .settings-button {\n      width: 44px;\n      height: 44px;\n      display: grid;\n      place-items: center;\n      border: 1px solid rgba(255, 255, 255, .34);\n      border-radius: 50%;\n      background: var(--lesson-bg);\n      color: var(--lesson-strong);\n      font: inherit;\n      font-size: 1.2em;\n      font-weight: 900;\n      cursor: pointer;\n      box-shadow: 0 14px 34px rgba(15, 23, 42, .16);\n      transition: transform .16s ease, box-shadow .16s ease;\n      touch-action: manipulation;\n      -webkit-tap-highlight-color: transparent;\n    }''':
'''    .settings-button {\n      width: 48px;\n      height: 48px;\n      display: grid;\n      place-items: center;\n      border: 1px solid rgba(255, 255, 255, .38);\n      border-radius: 50%;\n      background: var(--lesson-bg);\n      color: var(--lesson-strong);\n      font: inherit;\n      font-size: 1.16em;\n      font-weight: 900;\n      cursor: pointer;\n      box-shadow: 0 10px 26px rgba(15, 23, 42, .12);\n      backdrop-filter: blur(12px) saturate(1.08);\n      -webkit-backdrop-filter: blur(12px) saturate(1.08);\n      transition: transform .16s ease, box-shadow .16s ease, background .16s ease;\n      touch-action: manipulation;\n      -webkit-tap-highlight-color: transparent;\n    }''',
'''    .settings-button:hover,\n    .settings-button:focus-visible {\n      transform: translateY(-1px);\n      outline: 3px solid rgba(255, 255, 255, .66);\n      outline-offset: 3px;\n    }''':
'''    .settings-button:hover,\n    .settings-button:focus-visible {\n      transform: translateY(-1px);\n      background: rgba(255, 255, 255, .82);\n      box-shadow: 0 14px 30px rgba(15, 23, 42, .16);\n      outline: 3px solid rgba(255, 255, 255, .56);\n      outline-offset: 3px;\n    }\n\n    body[data-theme="dark"] .settings-button:hover,\n    body[data-theme="dark"] .settings-button:focus-visible {\n      background: rgba(30, 41, 59, .78);\n    }'''
}

for old, new in repls.items():
    if old not in s:
        raise SystemExit(f'Expected block not found:\n{old[:120]}')
    s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
