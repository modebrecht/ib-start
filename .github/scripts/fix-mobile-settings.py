from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '''      .header-tools {
        justify-content: flex-start;
      }

      .student-meta {
'''
new = '''      .header-tools {
        justify-content: flex-start;
      }

      .settings-wrap {
        position: static;
      }

      .settings-panel {
        left: 0;
        right: 0;
        width: auto;
        max-width: none;
      }

      .student-meta {
'''
if old not in text:
    raise SystemExit('Expected mobile header block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
