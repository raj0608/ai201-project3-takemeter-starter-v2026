# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

**Criterion:** Overall accuracy on the held-out test set is at least 0.70 (about 21 of 30 posts), on all three seeds.

**Why this target:** Random guessing on 3 labels gets about 0.33. I want TakeMeter right on roughly 7 of 10 comments before I'd trust it. The test split is only about 30 posts, so one mistake moves accuracy by 3.3 points and this target is deliberately ambitious.

## 2. Per-label performance (smallest label)

**Criterion:** F1 for `analytical` on the test set is at least 0.60, on all three seeds.

**Why this target:** `analytical` is my smallest label, so it has the fewest training examples and the fewest test posts (about 5). I still want the model to find these comments and not ignore them.

## 3. Balance of predictions

**Criterion:** No single label makes up more than 60% of the model's predictions on the test set.

**Why this target:** If one label is above 60% of predictions, the model has mostly learned to guess one class and is failing on the other two.

## 4. Precision on `emotional_personal`

**Criterion:** Precision for `emotional_personal` on the test set is at least 0.60, on all three seeds.

**Why this target:** The hardest boundary in my taxonomy is `opinion` vs. `emotional_personal`. High precision shows the model does not label every heated opinion as `emotional_personal`.

## 5. Clear-case check

**Criterion:** The model labels all 6 of these hand-picked, clear-cut comments correctly (6 of 6), on all three seeds. They are kept out of `labels.csv`, so the model never trains on them.

**Why this target:** If it misses a clear case, there is a basic problem. Two comments per label, chosen before any training:

- `opinion`: "Better players have been cut quicker than he has. He is in the nba strictly bc he is lebrons son. If you disagree, you are blind"
- `opinion`: "Bro is actually shredded with a six pack and a v from his pecks to his ween. He just looks frumpy because of all the jerseys."
- `analytical`: "Brewers won over 100 games but are low in salary, so it's essentially like the Hornets (#27th in payroll) maintaining their end of year form from last year and winning 62-65 games and being the #1 seed."
- `analytical`: "Dude the Brewers were the #1 seed in the regular season lol It's not unexpected at all. Baseball is also a much higher variance sport than basketball. On paper, this was probably a 55/45 series or something with the Dodgers being favored. During the season, they had the 3rd best offense, top 5 starting pitching, and a top 5 bullpen. They are a VERY good team."
- `emotional_personal`: "Man why the announcers have to emphasize "the thirty THREE year old" like he's an old man. It's hurting myself esteem."
- `emotional_personal`: "I was so angry. We all knew the Heat weren't going to win this, so my hating ass was like "just lie the fuck down already.""
