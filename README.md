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

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
I predicted that my trained model would do well on `opinion`, the label it saw most (97 of 155 training comments), but that it would struggle with `emotional_personal` because it may treat emotional comments as opinions. So the contest comes down to `emotional_personal`: if the baseline labels those comments more accurately, the baseline wins overall. If the baseline is still worse than my trained model on `emotional_personal`, the trained model wins.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

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

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



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
