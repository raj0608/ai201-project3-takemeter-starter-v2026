"""Unit 6 improvement experiments, run with the notebook's own training code.

Two measured runs, each over the same three seeds and the same test posts as
the "before" run:

  A  10 epochs on the original labels.csv                (one change: epochs)
  B  10 epochs plus extra_examples.csv in training only  (epochs + more data)

The extra rows are added to the TRAIN split after the split is made, so the
validation and test posts are identical to the before run and nothing leaks.
Each run is scored the way section 6 scores it, plus the six clear cases from
criteria.md (criterion 5).

    python run_experiments.py
"""
import json
import re

import numpy as np
import pandas as pd
import torch

nb = json.load(open("takemeter.ipynb"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
find = lambda marker: next(c for c in cells if marker in c)

ns = {}
exec("import torch\nimport pandas as pd", ns)
exec(find("def pick_device").split("DEVICE, DEVICE_NAME = pick_device()")[0], ns)
ns["DEVICE"], ns["DEVICE_NAME"] = ns["pick_device"]()
exec(find("LABELS = ["), ns)
exec("df = pd.read_csv('labels.csv')", ns)
exec(find("def split_dataset").split("train_df, val_df, test_df")[0], ns)
exec(find("def train_model").split("trainer, tokenizer = train_model(")[0], ns)
exec(find("def evaluate").split("results = evaluate(")[0], ns)

LABELS, df = ns["LABELS"], ns["df"]
extra = pd.read_csv("extra_examples.csv")[["text", "label"]]
SEEDS = [42, 7, 2024]
EPOCHS_AFTER = 10

cases = []
for line in open("criteria.md", encoding="utf-8"):
    m = re.match(r'- `(\w+)`: "(.*)"\s*$', line)
    if m:
        cases.append((m.group(2), m.group(1)))
assert len(cases) == 6


def clear_cases(trainer, tok):
    model = trainer.model
    model.eval()
    enc = tok([t for t, _ in cases], truncation=True, padding="max_length",
              max_length=ns["MAX_LENGTH"], return_tensors="pt").to(model.device)
    with torch.no_grad():
        logits = model(**enc).logits.cpu().numpy()
    predicted = [LABELS[i] for i in np.argmax(logits, axis=-1)]
    return sum(p == g for p, (_, g) in zip(predicted, cases)), predicted


def run(name, use_extra):
    out = []
    for seed in SEEDS:
        tr, va, te = ns["split_dataset"](df, seed)
        if use_extra:
            tr = pd.concat([tr, extra], ignore_index=True)
        trainer, tok = ns["train_model"](
            tr, va, LABELS, seed, EPOCHS_AFTER, ns["LEARNING_RATE"], ns["BATCH_SIZE"],
            ns["BASE_MODEL"], quiet=True,
        )
        r = ns["evaluate"](trainer, tok, te, LABELS, seed=seed)
        r["train_size"] = int(len(tr))
        r["epochs"] = EPOCHS_AFTER
        r["loss_by_epoch"] = [
            round(h["loss"], 4) for h in trainer.state.log_history if "loss" in h
        ]
        r["clear_correct"], r["clear_predicted"] = clear_cases(trainer, tok)
        r["device"], r["device_name"] = ns["DEVICE"], ns["DEVICE_NAME"]
        r["torch_version"], r["max_length"] = torch.__version__, ns["MAX_LENGTH"]
        out.append(r)
        print(f"[{name}] seed {seed}: acc {r['accuracy']:.3f}  macroF1 {r['f1_macro']:.3f}  "
              f"F1 a/o/e {[round(v['f1'], 2) for v in r['per_label'].values()]}  "
              f"clear {r['clear_correct']}/6", flush=True)
    return out


a = run("A epochs only", use_extra=False)
json.dump(a, open("results_three_seeds_after_A_epochs.json", "w"), indent=2)
b = run("B epochs + data", use_extra=True)
json.dump(b, open("results_three_seeds_after_B_epochs_data.json", "w"), indent=2)
print("Wrote both result files.")
