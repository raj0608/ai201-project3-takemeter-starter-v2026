# 🏀 Project 3 — TakeMeter NLP Classifier: Skills & Technologies

> **Note:** This is a personal portfolio reflection. The graded submission is `README.md`.

---

## 🔍 What I Built

A **text classification model** that reads Reddit comments from r/nba and labels each one as one of three categories:

- `analytical` — backed by checkable facts or structured reasoning
- `opinion` — a firm claim or hot-take with no supporting evidence
- `emotional_personal` — about the writer's own feelings or personal connection

The project covered the full supervised ML lifecycle: label design, data collection, manual annotation, inter-annotator agreement, fine-tuning a pre-trained transformer, and evaluating against a zero-shot baseline — all running locally, no API key required.

---

## 🛠️ Tools & Technologies

| Category | Tool / Library | Purpose |
|---|---|---|
| **Deep Learning** | PyTorch (`torch` ≥2.2) | Training backend for the fine-tuned transformer |
| **Transformers** | Hugging Face `transformers` (≥4.44) | Pre-trained model loading, tokenisation, fine-tuning |
| **Datasets** | Hugging Face `datasets` (≥2.20) | Efficient dataset loading and train/test splitting |
| **Training** | Hugging Face `accelerate` (≥0.30) | Hardware-aware training loop (CPU / GPU / Apple Silicon) |
| **Evaluation** | scikit-learn (≥1.3) | Classification report, confusion matrix, macro F1 |
| **Data** | pandas (≥2.0) | Reading and wrangling labelled CSV data |
| **Notebook** | Jupyter (`takemeter.ipynb`) | Interactive fine-tuning and evaluation workflow |
| **Language** | Python 3.11–3.13 | Core implementation language |

---

## ⚙️ Architecture & Key Design Decisions

- **Label taxonomy** — Three mutually exclusive labels were defined with precise decision rules and worked examples, specifically designed around the hardest boundary (`opinion` vs `emotional_personal`) to produce consistent annotations.
- **Inter-annotator agreement** — `agreement.py` computes agreement metrics before training so the label quality is measured, not assumed.
- **Cold-start / pooling** — `cold_20.csv` seeds the label pool; `pool_remaining.csv` tracks what's left. `collect_posts.py` and `make_labels_csv.py` automate the data pipeline from raw Reddit threads to a structured annotation CSV.
- **Baseline-first** — `baseline.py` runs a zero-shot classifier before any fine-tuning. This gives a concrete number to beat and prevents mistaking "the task is easy" for "the model is good."
- **Local-only** — No hosted runtime, no API key, no account. PyTorch's hardware autodetection in the notebook finds and uses a GPU or Apple Silicon MPS device if available, falling back to CPU cleanly.
- **Confusion matrix as primary metric** — The notebook prints the confusion matrix as a markdown table (copy-paste ready) to surface which label pairs the model confuses most.

---

## 🧠 Skills Learned

### AI / ML Concepts
- The full supervised NLP pipeline: problem definition → label design → data collection → annotation → training → evaluation
- **Transformer fine-tuning**: starting from a pre-trained checkpoint and adapting it to a domain-specific classification task with a small dataset
- **Zero-shot baseline**: using a model without any task-specific training to establish a performance floor, then measuring how much fine-tuning improves it
- Inter-annotator agreement as a measure of label quality and task difficulty
- Reading and interpreting a confusion matrix to understand model failure modes — not just accuracy
- Macro F1 as the right metric for imbalanced multi-class classification
- The `opinion` vs `emotional_personal` boundary as a concrete example of why label definitions must be precise and example-driven

### Software Engineering
- Structuring an annotation pipeline: raw data → candidate pool → label templates → labelled CSV
- Designing a label taxonomy that is both human-annotatable and machine-learnable
- Jupyter notebook as a reproducible experimental environment (not just a scratchpad)
- Hardware-agnostic training code that runs on CPU, NVIDIA GPU, and Apple Silicon without modification
- CSV-based data management for a small-scale annotation project

### Tools & Workflow
- Hugging Face ecosystem: `transformers`, `datasets`, `accelerate` working together
- PyTorch training loop mechanics
- scikit-learn for evaluation: `classification_report`, `confusion_matrix`
- pandas for data wrangling and CSV I/O
- Jupyter notebooks for iterative ML experimentation

---

## 📂 Key Files

| File | Role |
|---|---|
| `takemeter.ipynb` | Main fine-tuning and evaluation notebook |
| `baseline.py` | Zero-shot baseline classifier |
| `agreement.py` | Inter-annotator agreement computation |
| `collect_posts.py` | Scrapes raw Reddit posts into `raw_posts.txt` |
| `make_labels_csv.py` | Converts raw posts into an annotation-ready CSV |
| `labels.csv` | Final labelled dataset |
| `candidates.csv` / `candidates_filtered.csv` | Annotation candidate pools |
| `label_definitions.txt` | Human-readable label taxonomy with examples |
| `results.json` | Evaluation results output |
| `test.py` | Sanity-check tests for the data pipeline |
