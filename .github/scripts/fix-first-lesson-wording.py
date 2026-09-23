from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = {
    "Was ich im IB lernen möchte": "Was ich im Informatikunterricht lernen möchte",
    "im IB-Unterricht": "im Informatikunterricht",
    "im IB Unterricht": "im Informatikunterricht",
    "im IB lernen": "im Informatikunterricht lernen",
}

for old, new in replacements.items():
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
