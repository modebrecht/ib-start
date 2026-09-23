from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = {
    'Welche Informationen darf ich in einen KI-Prompt schreiben?': 'Welche Informationen darf ich einer KI geben?',
    '>KI-Prompt prüfen</button>': '>Antworten prüfen</button>',
    'Ein guter Prompt sagt der KI klar, <strong>was</strong> sie machen soll und <strong>welche Inhalte</strong> wichtig sind.': 'Ein Prompt ist deine Anweisung an die KI. Ein guter Prompt sagt klar, <strong>was du möchtest</strong> und <strong>welche Inhalte</strong> wichtig sind.',
    'Warum ist ein genauer Prompt besser?': 'Warum bekommst du mit einem genauen Prompt meist ein besseres Ergebnis?',
    '>Prompt-Check prüfen</button>': '>Antworten prüfen</button>',
    'Deinen eigenen Prompt schreiben. Beachte Aufgabe 02 und 04.': 'Schreibe einen eigenen Prompt. Nutze, was du in Aufgabe 02 und 04 gelernt hast.',
    'Die HTML-Präsentation von der KI erstellen lassen.': 'Lass die KI daraus eine HTML-Präsentation erstellen.',
    'Hilfe für deinen KI-Prompt anzeigen': 'Hilfe für deinen Prompt anzeigen',
    '• mit KI umgehen oder Medien mit KI erstellen': '• KI sinnvoll nutzen oder Medien mit KI erstellen',
    'Nutze nur Informationen, die du laut Aufgabe 02 teilen darfst.': 'Verwende nur Informationen, die du laut Aufgabe 02 mit einer KI teilen darfst.',
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'Missing expected text: {old}')
    text = text.replace(old, new, 1)

for obsolete in [
    'Welche Informationen darf ich in einen KI-Prompt schreiben?',
    'Prompt-Check prüfen',
    'Deinen eigenen Prompt schreiben. Beachte Aufgabe 02 und 04.',
    'Die HTML-Präsentation von der KI erstellen lassen.',
]:
    if obsolete in text:
        raise SystemExit(f'Obsolete wording remains: {obsolete}')

path.write_text(text, encoding='utf-8')
