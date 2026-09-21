# Cookie Cats A/B Test Analysis

**Status:** data acquired and quality-checked ([`docs/DATA_QUALITY.md`](docs/DATA_QUALITY.md)) — one real finding, a borderline sample ratio mismatch, carried forward as a documented caveat rather than silently resolved. Power analysis (Phase 3) is next.

## Business question

Cookie Cats is a mobile puzzle game. Players hit a "gate" that forces them to
wait (or pay) before continuing. The game studio ran a real A/B test moving
that gate from level 30 to level 40, and publicly released the anonymized
result data.

The question this project answers: **did moving the gate from level 30 to
level 40 actually change player retention, or does it look that way by
chance?** And separately: is a metric moving in the "right" direction always
a good reason to ship a change?

## Why this project

This is the first entry in a data science portfolio aimed at **Data
Scientist** roles specifically (as opposed to Analyst or ML Engineer roles).
A/B testing / causal inference was chosen over end-to-end predictive
modeling and time-series forecasting because it's the clearest way to
demonstrate statistical rigor — experimental design, hypothesis testing,
handling of confounders — which is the main thing that differentiates a
Data Scientist from an Analyst in interviews.

## Dataset

- **Name:** Mobile Games A/B Testing — Cookie Cats
- **Source:** Kaggle (publicly released by the studio's data scientist)
- **Why this dataset:** it's from a real, randomized experiment (not
  synthetic), in the product/growth domain, with more than one metric to
  reason about (1-day retention, 7-day retention, and rounds played) —
  enough richness to support a properly rigorous analysis instead of a
  single t-test.
- **Downloaded and quality-checked** — see [`data/README.md`](data/README.md) for how to
  reproduce, and [`docs/DATA_QUALITY.md`](docs/DATA_QUALITY.md) for the checks and findings.

## Planned methodology (roadmap)

Each phase below is intended to be its own session — depth over speed.

1. **Pre-registration** ✅ — write hypotheses, define the primary metric and
   guardrail metrics, and commit to an analysis plan *before* looking at
   results. This is the single habit that most separates a rigorous
   analysis from data dredging. See [`docs/PREREGISTRATION.md`](docs/PREREGISTRATION.md).
2. **Data acquisition + quality checks** ✅ — download the dataset, check for a
   sample ratio mismatch (was the random split actually fair?), missing
   data, duplicates, outliers. See [`docs/DATA_QUALITY.md`](docs/DATA_QUALITY.md).
3. **Power analysis** — given the actual sample size, what effect size
   could this experiment realistically detect? Sanity-check that against
   what was observed.
4. **Primary hypothesis test** — statistical significance test(s) on the
   primary metric, plus a bootstrap confidence interval as a cross-check.
5. **Guardrail / secondary metrics** — test the remaining metrics, correct
   for multiple comparisons rather than cherry-picking the metric that
   moved.
6. **Segment / heterogeneous treatment effect analysis** — does the effect
   differ by player segment, or is it uniform?
7. **Write-up** — a short recommendation memo: ship, don't ship, or need
   more data — and why, in plain language.

## Progress log

Kept as a running log, one entry per session, so the reasoning stays visible
rather than arriving as a finished repo.

**Session 1 — structure only**

1. Chose the project type (A/B testing / causal inference) and domain
   (product/growth) after discussing trade-offs against predictive modeling
   and time-series forecasting.
2. Chose the Cookie Cats dataset as a real, sufficiently rich experiment to
   analyze, with the reasoning above.
3. Created the local folder structure: `data/`, `notebooks/`, `docs/`.
4. Wrote this README as the project's plan of record.

**Session 2 — pre-registration**

1. Wrote [`docs/PREREGISTRATION.md`](docs/PREREGISTRATION.md): hypotheses,
   why `retention_7` is the primary metric (and `retention_1` /
   `sum_gamerounds` are guardrails, not alternate shots at significance),
   the statistical test plan per metric, the data-quality checks that must
   pass before any test result is trusted, and the ship / no-ship / trade-off
   decision framework. Deliberately written before the dataset is downloaded.
2. Added `requirements.txt` for the analysis phase (pandas, numpy, scipy,
   statsmodels, pingouin, matplotlib, seaborn, jupyter) — declared, not yet
   installed.

**Session 3 — data acquisition + quality checks**

1. Downloaded the dataset (90,189 rows; source and repro steps in
   [`data/README.md`](data/README.md); raw CSV gitignored, not committed).
2. Wrote [`notebooks/01_data_quality_checks.py`](notebooks/01_data_quality_checks.py):
   schema/shape, duplicate and missing-value checks, impossible-value checks,
   a sample ratio mismatch test, and a randomization-unit sanity check.
3. Found a borderline SRM (p = 0.0086) — real, not swept under the rug.
   Written up in [`docs/DATA_QUALITY.md`](docs/DATA_QUALITY.md) and logged
   as a dated amendment in `PREREGISTRATION.md`, per that document's own
   rule about not silently editing the plan after seeing data.
4. Initialized git and pushed to GitHub.

**Not done yet, on purpose:** no power analysis, no hypothesis test run.
Phase 3 (power analysis) is the next session.

## Project layout

```
data/
  README.md               how to reproduce the raw data download
  raw/                     gitignored — cookie_cats.csv lives here locally
notebooks/
  01_data_quality_checks.py
docs/
  PREREGISTRATION.md      hypotheses, metrics, test plan, decision framework
  DATA_QUALITY.md         Phase 2 checks and the SRM finding
requirements.txt          analysis dependencies
```
