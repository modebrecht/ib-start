from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

nav_pattern = re.compile(r'      <nav class="task-nav" aria-label="Aufgaben">.*?      </nav>', re.S)
new_nav = """      <nav class="task-nav" aria-label="Aufgaben">
        <button class="task-tile is-active" type="button" data-task-target="task-1" style="--tile-color: var(--red)"><span class="task-number">01</span><span class="task-label">Mini-Präsentation</span></button>
        <button class="task-tile" type="button" data-task-target="task-6" style="--tile-color: var(--orange)"><span class="task-number">02</span><span class="task-label">Was darf ich teilen?</span></button>
        <button class="task-tile" type="button" data-task-target="task-3" style="--tile-color: var(--yellow)"><span class="task-number">03</span><span class="task-label">Gute Dateinamen erkennen</span></button>
        <button class="task-tile" type="button" data-task-target="task-5" style="--tile-color: var(--green)"><span class="task-number">04</span><span class="task-label">KI richtig nutzen</span></button>
        <button class="task-tile" type="button" data-task-target="task-7" style="--tile-color: var(--cyan)"><span class="task-number">05</span><span class="task-label">Tastenkombinationen</span></button>
        <button class="task-tile" type="button" data-task-target="task-2" style="--tile-color: var(--blue)"><span class="task-number">06</span><span class="task-label">Meine Präsentation</span></button>
        <button class="task-tile" type="button" data-task-target="task-8" style="--tile-color: var(--violet)"><span class="task-number">07</span><span class="task-label">Rückblick</span></button>
      </nav>"""
text, nav_count = nav_pattern.subn(new_nav, text, count=1)
if nav_count != 1:
    raise SystemExit(f"Expected one task nav, found {nav_count}")

stage_start = text.index('      <div class="task-stage">')
controls_start = text.index('\n      <div class="slide-controls"', stage_start)
stage_blob = text[stage_start:controls_start]
section_pattern = re.compile(r'      <section class="section(?: is-active)?" data-task="(task-\d+)" style="--accent: var\(--[a-z]+\)">.*?      </section>', re.S)
sections = {m.group(1): m.group(0) for m in section_pattern.finditer(stage_blob)}
order = ["task-1", "task-6", "task-3", "task-5", "task-7", "task-2", "task-8"]
missing = [task for task in order if task not in sections]
if missing:
    raise SystemExit(f"Missing task sections: {missing}")

meta = {
    "task-1": ("01", "red"),
    "task-6": ("02", "orange"),
    "task-3": ("03", "yellow"),
    "task-5": ("04", "green"),
    "task-7": ("05", "cyan"),
    "task-2": ("06", "blue"),
    "task-8": ("07", "violet"),
}
rebuilt = []
for task_id in order:
    block = sections[task_id]
    number, colour = meta[task_id]
    block = re.sub(
        r'(data-task="' + re.escape(task_id) + r'" style="--accent: var\(--)[a-z]+(\)")',
        r'\g<1>' + colour + r'\g<2>',
        block,
        count=1
    )
    block = re.sub(
        r'(<div class="section-number"><span>)\d{2}(</span>)',
        r'\g<1>' + number + r'\g<2>',
        block,
        count=1
    )
    rebuilt.append(block)
new_stage = '      <div class="task-stage">\n' + '\n\n'.join(rebuilt) + '\n      </div>\n'
text = text[:stage_start] + new_stage + text[controls_start:]

presentation_options = """
                <label class="choice"><input type="checkbox" name="privacy-presentation-hobby" value="good" data-privacy-answer> Hobby</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-game" value="good" data-privacy-answer> Lieblingsgame</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-first-name" value="good" data-privacy-answer> Vorname</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-last-name" value="good" data-privacy-answer> Nachname</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-birthday" value="good" data-privacy-answer> Geburtsdatum</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-address" value="bad" data-privacy-answer> Adresse</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-phone" value="bad" data-privacy-answer> Telefonnummer</label>
                <label class="choice"><input type="checkbox" name="privacy-presentation-password" value="bad" data-privacy-answer> Passwort</label>"""
ai_options = """
                <label class="choice"><input type="checkbox" name="privacy-ai-hobby" value="good" data-privacy-answer> Hobby</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-game" value="good" data-privacy-answer> Lieblingsgame</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-first-name" value="good" data-privacy-answer> Vorname</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-last-name" value="bad" data-privacy-answer> Nachname</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-birthday" value="bad" data-privacy-answer> Geburtsdatum</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-address" value="bad" data-privacy-answer> Adresse</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-phone" value="bad" data-privacy-answer> Telefonnummer</label>
                <label class="choice"><input type="checkbox" name="privacy-ai-password" value="bad" data-privacy-answer> Passwort</label>"""

def replace_privacy_group(source, group, options):
    pattern = re.compile(
        r'(<div class="privacy-task" data-privacy-group="' + group + r'">.*?<div class="privacy-options" data-randomize-options>).*?(</div>\s*<div class="check-actions">)',
        re.S
    )
    result, count = pattern.subn(r'\1' + options + '\n              ' + r'\2', source, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace privacy group {group}")
    return result

text = replace_privacy_group(text, "presentation", presentation_options)
text = replace_privacy_group(text, "ai", ai_options)

text = text.replace(
    'Deinen Dateinamen aus Aufgabe 04 verwenden und speichern.',
    'Deinen Dateinamen aus Aufgabe 03 verwenden und speichern.'
)
text = text.replace(
    'Deinen eigenen Prompt schreiben. Beachte Aufgabe 02 und 03.',
    'Deinen eigenen Prompt schreiben. Beachte Aufgabe 02 und 04.'
)
text = text.replace(
    'Gespeichert: Aufgabe 04 ist richtig gelöst.',
    'Gespeichert: Aufgabe 03 ist richtig gelöst.'
)

anchor = '    .html-runner-status { color: var(--muted); font-weight: 750; }\n'
override = """    .html-runner-status { color: var(--muted); font-weight: 750; }
    .html-runner {
      border-color: color-mix(in srgb, var(--accent, var(--blue)) 30%, var(--line));
      background: color-mix(in srgb, var(--accent, var(--blue)) 6%, var(--panel-bg));
    }
    .html-runner-start { background: var(--accent, var(--blue)); }
"""
if anchor not in text:
    raise SystemExit("HTML runner CSS anchor missing")
text = text.replace(anchor, override, 1)

if text.count('data-privacy-answer') != 16:
    raise SystemExit(f"Expected 16 privacy options, got {text.count('data-privacy-answer')}")
if 'Aufgabe 04 verwenden und speichern' in text or 'Beachte Aufgabe 02 und 03.' in text:
    raise SystemExit("Old task references remain")

path.write_text(text, encoding="utf-8")
