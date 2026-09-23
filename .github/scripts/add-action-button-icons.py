from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

CHECK_ICON = '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"></circle><path d="m8.5 12 2.3 2.3 4.8-5"></path></svg>'
READ_ICON = '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"></path></svg>'
DOWNLOAD_ICON = '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3v12"></path><path d="m7 10 5 5 5-5"></path><path d="M5 21h14"></path></svg>'
LOCK_ICON = '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="5" y="10" width="14" height="10" rx="2"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path></svg>'
GEAR_ICON = '<svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.83 2.83-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21h-4v-.1A1.7 1.7 0 0 0 8.6 19.4a1.7 1.7 0 0 0-1.88.34l-.06.06-2.83-2.83.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3v-4h.1A1.7 1.7 0 0 0 4.6 8.6a1.7 1.7 0 0 0-.34-1.88l-.06-.06 2.83-2.83.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3h4v.1A1.7 1.7 0 0 0 15.4 4.6a1.7 1.7 0 0 0 1.88-.34l.06-.06 2.83 2.83-.06.06A1.7 1.7 0 0 0 19.4 9c.1.37.3.7.6 1 .3.27.68.4 1.1.4H21v4h-.1a1.7 1.7 0 0 0-1.5.6Z"></path></svg>'

# Settings button: replace the glyph with a real SVG.
text = text.replace(
    '<button class="settings-button" type="button" data-settings-toggle aria-label="Optionen öffnen">⚙</button>',
    f'<button class="settings-button" type="button" data-settings-toggle aria-label="Optionen öffnen">{GEAR_ICON}</button>'
)

# Settings actions.
text = text.replace(
    '<button class="download-json settings-json" type="button" data-download-json>JSON herunterladen</button>',
    f'<button class="download-json settings-json" type="button" data-download-json>{DOWNLOAD_ICON}<span class="button-label">JSON herunterladen</span></button>'
)
text = text.replace(
    '<button class="admin-unlock" type="button" data-admin-unlock>Freischalten</button>',
    f'<button class="admin-unlock" type="button" data-admin-unlock>{LOCK_ICON}<span class="button-label">Freischalten</span></button>'
)

# Read confirmation button.
text = text.replace(
    '<button class="read-button" type="button" data-read-confirm="task-1-brief" aria-pressed="false">Auftrag verstanden</button>',
    f'<button class="read-button" type="button" data-read-confirm="task-1-brief" aria-pressed="false">{READ_ICON}<span class="button-label">Auftrag verstanden</span></button>'
)

# All regular check buttons get one consistent SVG, but preserve buttons already carrying their own icon (PDF action).
def add_check_icon(match):
    attrs, inner = match.group(1), match.group(2)
    if '<svg' in inner:
        return match.group(0)
    return f'<button class="check-button"{attrs}>{CHECK_ICON}<span class="button-label">{inner.strip()}</span></button>'

text = re.sub(r'<button class="check-button"([^>]*)>(.*?)</button>', add_check_icon, text, flags=re.S)

# Dynamic button labels must update only the label, otherwise textContent would delete the SVG.
old_admin = 'if (adminUnlock) adminUnlock.textContent = adminMode ? "Abmelden" : "Freischalten";'
new_admin = '''if (adminUnlock) {
          const adminButtonLabel = adminUnlock.querySelector(".button-label");
          if (adminButtonLabel) adminButtonLabel.textContent = adminMode ? "Abmelden" : "Freischalten";
        }'''
if old_admin not in text:
    raise SystemExit('admin button label update anchor not found')
text = text.replace(old_admin, new_admin)

old_read = 'button.textContent = isRead ? "✓ Gelesen" : "Gelesen";'
new_read = '''const buttonLabel = button.querySelector(".button-label");
        if (buttonLabel) buttonLabel.textContent = isRead ? "Gelesen" : "Gelesen";'''
if old_read not in text:
    raise SystemExit('read button label update anchor not found')
text = text.replace(old_read, new_read)

# Shared visual alignment for all action buttons with icons.
style_anchor = '    .admin-unlock.is-logout {\n      background: var(--red);\n    }'
style_extra = '''    .admin-unlock.is-logout {
      background: var(--red);
    }

    .check-button,
    .read-button,
    .admin-unlock,
    .settings-json {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .settings-button .action-icon {
      width: 21px;
      height: 21px;
    }

    .check-button .action-icon,
    .read-button .action-icon,
    .admin-unlock .action-icon,
    .settings-json .action-icon {
      width: 18px;
      height: 18px;
    }'''
if style_anchor not in text:
    raise SystemExit('style anchor not found')
text = text.replace(style_anchor, style_extra, 1)

# Validation: all normal check buttons now have an SVG.
for m in re.finditer(r'<button class="check-button"[^>]*>(.*?)</button>', text, flags=re.S):
    if '<svg' not in m.group(1):
        raise SystemExit('check-button without SVG remains')

required = [
    'data-check-privacy="presentation"',
    'data-check-privacy="ai"',
    'data-check-task="task-3"',
    'data-check-task="task-5"',
    'data-check-task="task-7"',
    'data-read-confirm="task-1-brief"',
    'data-download-json',
    'data-admin-unlock',
    'data-settings-toggle',
]
for token in required:
    if token not in text:
        raise SystemExit(f'missing expected action: {token}')

path.write_text(text, encoding='utf-8')
