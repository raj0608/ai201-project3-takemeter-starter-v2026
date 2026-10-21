# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments from r/nba (the NBA subreddit) by what kind of contribution they make. It reads one comment and labels it `analytical` (supported by checkable facts or reasoning), `opinion` (a firm claim with no support), or `emotional_personal` (about the writer's own feelings or life). Questions, news reposts, and jokes are left out of the dataset on purpose.

---

## Label Taxonomy

### `analytical`

**Definition:** Breaks down gameplay, roster construction, financial rules, or statistics by citing a specific, checkable fact or supporting logic.

**Example 1:**
> Here’s the biggest issue with having Jaylen Brown on the Celtics: the second apron. He’s a good and well-liked player who had a lot of success here

**Example 2:**
> Ita underrated how unusually difficult of a role Brunson had. The drop-off between him and the next best player to the run half court offense was pretty massive. It was who, KAT? Jose? And KAT can't do it too much because he had to save his stamina for Wemby I know his stats aren't impressive for a finals mvp. Im guessing he was the least efficient finals mvp in a long time ...

### `opinion`

**Definition:** Asserts a firm, subjective judgment or hot take about a player, team, or event without offering supporting evidence, data, or technical explanation.

**Example 1:**
> this list is wild no one in thier fucking mind is choosing brunson over Kawhi😂

**Example 2:**
> Lefanboys drooling over this clown - meanwhile be tried to join the knicks but they knew better than to sign a toxic flopper

### `emotional_personal`

**Definition:** Centers on the writer's own feelings, personal story, or connection to the topic, using first-person or emotional language.

**Example 1:**
> I’ve always liked Randle ever since he was so candid about his decision to quit weed. Honestly motivated me to do the same

**Example 2:**
> The Kobe circlejerking & Shai hating circlejerk have United. This is painful. I hate this sub.

### The hardest boundary

**Which two labels:** `opinion` vs. `emotional_personal`.

**The decision rule I used every time:**
Ask what the post is mainly about. If it is about the subject (a player, team, or play), it is `opinion`. If it is about the writer's own state (feelings, life, fandom), it is `emotional_personal`. Related rules:
- If a post has both a claim and a feeling, the stronger one decides.
- A hostile post, including an attack on another commenter, is `opinion` unless its main content is the writer's own feeling.
- If a post cites a specific, checkable fact, it is `analytical`, even if the tone is heated. Reasoning with no checkable fact is `opinion`.


---

## The Dataset

**Where the posts came from:** Top-level comments from r/nba, collected with `collect_posts.py` from the public Arctic Shift archive of Reddit (Reddit blocked direct scraping). It covers October 6-15, 2026. I kept comments of 80-1200 characters and dropped bots, removed comments, links, text posts, and comments that end in a question mark.

**How I labelled them:** I labelled 20 comments cold, alone and with no tools, and marked them `cold` in the note column. A model then pre-labelled 203 more comments from my definitions. I read every one of those and corrected 3; they are marked `pre-labeled` in the note column. Six comments were held out of the file on purpose for my clear-case criterion in `criteria.md`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| opinion | 139 | 62.3% |
| emotional_personal | 50 | 22.4% |
| analytical | 34 | 15.2% |
| **Total** | 223 | 100% |

**Three hard cases**

**1.**
> *The post:* I mean if a failed trade was enough destroy him like this maybe he wasn’t really built for the league
>
> *Could have been:* `opinion` or `emotional_personal`
>
> *I chose:* `opinion`, because the subject is the player ("wasn't really built for the league"), not the writer's own feelings.

**2.**
> *The post:* "Superteam" is just such a dumb term overall, but it's especially stupid with the Sixers. They made the second round of the playoffs literally last season. With Embiid being in and out. They swapped Old Paul George for Jaylen Brown and LeBron. And Maxey might be their best regular season player. The Knicks and Sixers are the only two teams in the East where failing to advance deep in the playoffs is just a clear failure.
>
> *Could have been:* `opinion` or `emotional_personal`
>
> *I chose:* `opinion`, because it argues about the Sixers ("dumb term") and the frustration is aimed at the label, not at the writer's own state. It mentions facts, but they back up a judgment and are not the main point.

**3.**
> *The post:* Grizzlies score 49 in one quarter, and somehow, hawks are an "elite defensive team"
>
> *Could have been:* `analytical` or `opinion`
>
> *I chose:* `analytical`, because it cites a specific checkable fact (49 points in one quarter) to challenge a claim. Under my rule, a checkable fact makes a post `analytical`, even if the tone is sarcastic.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on an Apple Silicon GPU (MPS) with torch 2.14.1.

**Anything I changed from the defaults, and why:** Nothing. I used every default.

**Split sizes:** train 155, validation 34, test 34 (70/15/15, stratified).

| Label | Train | Val | Test |
|---|---|---|---|
| analytical | 24 | 5 | 5 |
| opinion | 97 | 21 | 21 |
| emotional_personal | 34 | 8 | 8 |

`analytical` has only 5 examples in the test split, so any score for it will move a lot between seeds.

---

## How I Used AI

**Moment 1: stress-testing my labels**

- *What I asked for:* eight invented posts that sit on the boundaries of my three label definitions, so I could classify them cold.
- *What came back:* eight short posts. I labelled them and was unsure about three (a post that mixes a claim and a feeling, a post attacking another commenter, and a post with thin support).
- *What I changed:* each of the three uncertain posts became a written rule. If a post has both a claim and a feeling, the stronger one decides. An attack on another commenter is `opinion`. A checkable fact makes a post `analytical`.

**Moment 2: checking my cold-labelled file**

- *What I asked for:* a format check of my 20 cold labels, without any comment on my choices.
- *What came back:* capitalised labels, hard-case notes typed in the label column, and two near-duplicate comments that I had labelled differently.
- *What I changed:* I fixed the spelling and moved the notes. I dropped one of the duplicates so it could not leak between the training and test splits, and I labelled its replacement cold.

**Pre-labelling disclosure:** A model pre-labelled 203 of my 223 rows (every row except the 20 cold ones) from my written definitions. I read each one and changed 3, all to `opinion`. The same model helped write `collect_posts.py`. The label definitions, decision rules, and acceptance criteria are mine.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

Both models were scored on the same 34 held-out posts in `test_split.csv` (5 `analytical`, 21 `opinion`, 8 `emotional_personal`). The baseline is `facebook/bart-large-mnli`, zero-shot, with no training. I ran it twice: once with my three README definitions as the prompt, and once with bare label names only (`baseline_bare_names_results.json`). The trained model is `distilbert-base-uncased` from `results.json` (seed 42, MPS).

| Measure | Baseline (my definitions) | Baseline (bare names) | Trained |
|---|---|---|---|
| Overall accuracy | 0.353 | 0.676 | 0.618 |
| Macro F1 | 0.247 | 0.571 | 0.255 |
| F1 — `analytical` | 0.000 | 0.250 | 0.000 |
| F1 — `emotional_personal` | 0.421 | 0.727 | 0.000 |
| F1 — `opinion` | 0.320 | 0.737 | 0.764 |

**What I predicted before I looked:**
I predicted that my trained model would do well on `opinion`, the label it saw most (97 of 155 training comments), but that it would struggle with `emotional_personal` because it may treat emotional comments as opinions. So the contest comes down to `emotional_personal`: if the baseline labels those comments more accurately, the baseline wins overall. If the baseline is still worse than my trained model on `emotional_personal`, the trained model wins.

**What the gap actually means:**
My prediction was half right. The trained model is strong on `opinion` (F1 0.764), but it never predicted `analytical` or `emotional_personal` at all: its confusion matrix puts all 34 test posts in the `opinion` column. Its 0.618 accuracy is just the `opinion` share of the test split (21 of 34). By my own rule, the baseline wins, because it scored `emotional_personal` F1 0.421 (0.727 with bare names) against 0.000 for the trained model.

Two surprises. First, with my definitions as the prompt the baseline was worse than the trained model on accuracy (0.353 vs 0.618), but with bare label names it did far better (0.676), so my written definitions made the baseline worse by 0.323 accuracy. Second, the trained model is no better than a model that always says `opinion`. Fine-tuning on 155 posts with 97 of them `opinion` taught it the majority label and nothing else. The baseline needed no training and still beat it on both smaller labels.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**Device:** Apple Silicon GPU (MPS), torch 2.14.1, max length 128. All runs are the same system as the earlier unit: 3 epochs, learning rate 2e-5, batch size 16. Only the seed changed (42, 7, 2024).

**Raw numbers, three seeds (34 test posts each):**

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.618 | 0.618 | 0.618 | 0.000 |
| Macro F1 | 0.255 | 0.255 | 0.255 | 0.000 |
| F1 `analytical` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 `opinion` | 0.764 | 0.764 | 0.764 | 0.000 |
| F1 `emotional_personal` | 0.000 | 0.000 | 0.000 | 0.000 |

A spread of 0.000 does not mean the result is trustworthy. All three seeds gave the identical result because every seed made the same collapse: the model predicted `opinion` for every test post.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.618 | 0.618 | 0.618 | MISSED |
| 2. F1 `analytical` | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |
| 3. Biggest label's share of predictions | ≤ 60% | 100% (`opinion`) | 100% (`opinion`) | 100% (`opinion`) | MISSED |
| 4. Precision `emotional_personal` | ≥ 0.60 | 0.000 (no predictions) | 0.000 (no predictions) | 0.000 (no predictions) | MISSED |
| 5. Clear cases correct | 6 of 6 | 2 of 6 | 2 of 6 | 2 of 6 | MISSED |

Criterion 5 was scored by `check_clear_cases.py`, which retrains with the notebook's own code and seeds and predicts the six held-out comments (`clear_cases_results.json`). Its training losses match the notebook's runs.

### Confusion matrix

Seed 42. Seeds 7 and 2024 produced the identical matrix. Rows are the true label, columns are the model's guess.

| true \ predicted | analytical | opinion | emotional_personal |
|---|---|---|---|
| **analytical** | 0 | 5 | 0 |
| **opinion** | 0 | 21 | 0 |
| **emotional_personal** | 0 | 8 | 0 |

**My biggest off-diagonal number, and what it means:**
The biggest is 8 real `emotional_personal` posts called `opinion`, and 0 went the other way. The 5 `analytical` posts were also all called `opinion`. So the model did not learn a boundary between `opinion` and either of the other two labels. It only learned to say `opinion`, the majority label.

---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

All five criteria were MISSED on all three seeds. A target counts as met only if it holds on every seed, and none held on any seed.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.70 | MISSED | 0.618 on every seed, below 0.70. |
| 2 | F1 `analytical` | ≥ 0.60 | MISSED | F1 was 0.000 on every seed. |
| 3 | No label above 60% of predictions | ≤ 60% | MISSED | `opinion` was 100% of predictions (34 of 34) on every seed. |
| 4 | Precision `emotional_personal` | ≥ 0.60 | MISSED | The model never predicted `emotional_personal`, so precision is undefined and scored 0.000. A criterion cannot be met by making no predictions. |
| 5 | Six clear cases correct | 6 of 6 | MISSED | 2 of 6 on every seed. |

**Diagnoses**

**The one cause behind all five: the model collapsed to the majority label.** All 34 test posts were called `opinion` on all three seeds, and the confusion matrix shows it (columns `analytical` and `emotional_personal` are all zero). Accuracy of 0.618 is exactly the share of `opinion` in the test split (21 of 34), so a model that always says `opinion` scores the same. The loss was still falling at epoch 3 (1.00, 0.90, 0.87) while accuracy stayed flat, so the model was still undertrained, not finished. The spread of 0.000 across seeds is the same collapse repeating, not stability.

- **Criterion 1 (accuracy):** the cause is the collapse above. The score is the floor for always guessing `opinion`, so the model learned nothing beyond the label frequencies. I know this from the matrix and from the accuracy matching 21/34.
- **Criterion 2 (`analytical` F1):** the cause is too few examples, plus the collapse. `analytical` has 34 labelled comments, only 24 in training, and 5 in the test split, and all 5 were called `opinion`. The zero-shot baseline with bare label names also scored only 0.250 F1 on `analytical`, so this is a hard label for any model, not just mine.
- **Criterion 3 (balance):** the cause is the collapse, which is a model problem and not a data-balance problem: my data is 62% `opinion`, but the model's predictions are 100% `opinion`, so it amplified the imbalance.
- **Criterion 4 (`emotional_personal` precision):** the cause is the collapse. The model never predicted this label, so all 8 real `emotional_personal` test posts were called `opinion`. The reverse never happened (0 real `opinion` called `emotional_personal`). This is my hardest boundary, so a labelling problem is possible. *Agreement-report evidence for this boundary goes here once I have the staff labels.*
- **Criterion 5 (clear cases):** the model got only the two `opinion` cases right and missed the two `analytical` and two `emotional_personal` ones on every seed. These six were picked as obvious, so a labelling inconsistency in my training data cannot fully explain the misses. This points at the model, which has not learned the smaller labels at all.

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**
I made two changes, kept separable so each one could be measured: (1) training for **10 epochs instead of 3**, and (2) adding **68 more real r/nba comments** (34 `analytical`, 34 `emotional_personal`) to the **training split only**. The extra comments are in `extra_examples.csv`, collected with `collect_posts.py` from older days and from r/nbadiscussion, pre-labelled by a model, and each one reviewed and corrected by me. The validation and test posts are the same 34 posts as the "before" run for every seed, so the two logs are scored on identical test posts, and no new row can leak into the test split. Training size went from 155 to 223. Everything else (labels, taxonomy, criteria, learning rate, batch size, max length, seeds) is unchanged. The project asks for one change; I used two on purpose and measured them in sequence, so the effect of each is visible below.

- **Run A (epochs only):** `results_three_seeds_after_A_epochs.json`, 10 epochs on the original data.
- **Run B (epochs + data):** `results_three_seeds_after_B_epochs_data.json`, the same file as `results_three_seeds_after.json`. I treat B as my final "after" system.

Both runs were produced by `run_experiments.py`, which reuses the notebook's own training and evaluation code.

**Which diagnosis pointed at it:**
The model collapsed to the majority label (`opinion` for all 34 test posts on every seed), and the training loss was still falling at epoch 3 (1.00, 0.90, 0.87) while accuracy stayed flat, so it was undertrained. That pointed at more epochs. The second diagnosis was too few examples: `analytical` had only 24 training posts and scored F1 0.000, so I added examples for the two thin labels.

### Run Log — After

This is run B (10 epochs plus the extra training data), same device (Apple Silicon GPU, MPS) and same three seeds.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.706 | 0.676 | 0.853 | MISSED (seed 7) |
| 2. F1 `analytical` | ≥ 0.60 | 0.444 | 0.400 | 0.571 | MISSED |
| 3. Biggest label's share of predictions | ≤ 60% | 62% (`opinion`) | 59% (`opinion`) | 71% (`opinion`) | MISSED (seeds 42, 2024) |
| 4. Precision `emotional_personal` | ≥ 0.60 | 0.667 | 0.667 | 0.875 | MET |
| 5. Clear cases correct | 6 of 6 | 5 of 6 | 5 of 6 | 5 of 6 | MISSED |

**Side by side (before, A, B):**

| Measure | Before (3 epochs) | A: 10 epochs | B: 10 epochs + data |
|---|---|---|---|
| Accuracy, seeds 42 / 7 / 2024 | 0.618 / 0.618 / 0.618 | 0.676 / 0.676 / 0.588 | 0.706 / 0.676 / 0.853 |
| F1 `analytical` | 0.000 / 0.000 / 0.000 | 0.000 / 0.250 / 0.000 | 0.444 / 0.400 / 0.571 |
| F1 `emotional_personal` | 0.000 / 0.000 / 0.000 | 0.571 / 0.615 / 0.000 | 0.706 / 0.706 / 0.875 |
| `opinion` share of predictions | 100% / 100% / 100% | 82% / 76% / 97% | 62% / 59% / 71% |
| Clear cases correct | 2 / 2 / 2 | 4 / 5 / 4 | 5 / 5 / 5 |

**Did it help, and how do I know:**
Yes, it helped, and the two changes did different jobs. More epochs alone (A) broke the collapse on two of three seeds: `emotional_personal` F1 went from 0.000 to 0.57 and 0.62, accuracy rose to 0.676, and clear cases went from 2 to 4 or 5. But it was unstable: on seed 2024 the model still predicted `opinion` for 97% of posts and `emotional_personal` precision was 0.000, so criterion 4 was still missed. Adding the extra data on top (B) fixed that: every seed now predicts all three labels, `analytical` F1 rose from 0.000 to 0.40-0.57, `emotional_personal` F1 is 0.71-0.88, and criterion 4 is now MET on all three seeds. Mean accuracy rose from 0.618 to 0.745.

Two cautions. First, the test split is only 34 posts, with 5 `analytical`, so a single post moves `analytical` F1 a lot, and accuracy swung 0.676 to 0.853 across seeds in run B (a 0.177 spread). I trust the direction of the change (the collapse is gone) more than any single number. Second, I chose the extra `analytical` comments partly by looking for numbers and stats, so the model may have learned "has a number" as a shortcut for `analytical`, which could make the improvement look better than it is on posts without numbers.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
