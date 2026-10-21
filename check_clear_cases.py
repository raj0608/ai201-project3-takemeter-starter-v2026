"""Criterion 5: score the six hand-picked clear cases from criteria.md.

The notebook never saves a model, so this retrains it per seed using the
notebook's own code (same labels, settings and seeds) and predicts the six
comments, which are kept out of labels.csv. Writes clear_cases_results.json.

    python check_clear_cases.py
"""
import json
import re
import sys

import numpy as np
import pandas as pd

nb = json.load(open("takemeter.ipynb"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def find(marker):
    return next(c for c in cells if marker in c)


ns = {}
exec(find("LABELS = ["), ns)                                    # label map and settings
exec("import pandas as pd\ndf = pd.read_csv('labels.csv')", ns)
exec(find("def split_dataset").split("train_df, val_df, test_df")[0], ns)
exec(find("def train_model").split("trainer, tokenizer = train_model(")[0], ns)

# the six comments and their intended labels, straight from criteria.md
cases = []
for line in open("criteria.md", encoding="utf-8"):
    m = re.match(r'- `(\w+)`: "(.*)"\s*$', line)
    if m:
        cases.append((m.group(2), m.group(1)))
assert len(cases) == 6, f"expected 6 clear cases, found {len(cases)}"

LABELS = ns["LABELS"]
results = []
for seed in [42, 7, 2024]:
    tr, va, te = ns["split_dataset"](ns["df"], seed)
    trainer, tok = ns["train_model"](
        tr, va, LABELS, seed, ns["EPOCHS"], ns["LEARNING_RATE"], ns["BATCH_SIZE"],
        ns["BASE_MODEL"], quiet=True,
    )
    model = trainer.model
    model.eval()
    enc = tok([t for t, _ in cases], truncation=True, padding="max_length",
              max_length=ns["MAX_LENGTH"], return_tensors="pt").to(model.device)
    import torch
    with torch.no_grad():
        logits = model(**enc).logits.cpu().numpy()
    predicted = [LABELS[i] for i in np.argmax(logits, axis=-1)]
    correct = sum(p == g for p, (_, g) in zip(predicted, cases))
    print(f"seed {seed}: {correct}/6 correct  predicted={predicted}", flush=True)
    results.append({"seed": seed, "correct": correct,
                    "cases": [{"gold": g, "predicted": p} for p, (_, g) in zip(predicted, cases)]})

json.dump(results, open("clear_cases_results.json", "w"), indent=2)
print("Wrote clear_cases_results.json")
