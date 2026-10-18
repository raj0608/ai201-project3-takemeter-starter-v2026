"""Turn raw_posts.txt into labels.csv (text,label,note) with correct quoting.

Blocks are separated by a line of ====. A block may start with ">> label | note".
Blocks with no label are written with an empty label so you can fill them in
later; the notebook's check will flag any left blank.
"""
import csv
import sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_posts.txt")
DST = Path(sys.argv[2] if len(sys.argv) > 2 else "labels.csv")

rows = []
for block in SRC.read_text(encoding="utf-8").split("\n===="):
    lines = [l for l in block.splitlines() if not l.startswith("###")]
    label = note = ""
    if lines and lines[0].lstrip().startswith(">>"):
        label, _, note = lines.pop(0).lstrip()[2:].partition("|")
        label, note = label.strip(), note.strip()
    text = " ".join(" ".join(lines).split())  # one line per post
    if text:
        rows.append((text, label, note))

with DST.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text", "label", "note"])
    w.writerows(rows)

print(f"Wrote {len(rows)} posts to {DST}")
