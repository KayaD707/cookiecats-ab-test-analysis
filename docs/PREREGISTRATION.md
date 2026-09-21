# Pre-registration

Written before the dataset is downloaded or looked at. The point of doing this
first is discipline: it's easy to fool yourself by picking whichever metric
moved after the fact ("metric shopping") or by relaxing significance
thresholds once you've seen a promising-looking number. Committing to the plan
now makes the later analysis falsifiable instead of just a narrative fitted to
the result.

## Background

Cookie Cats places a progress-blocking "gate" in front of players. The
studio ran a randomized test moving that gate from level 30 to level 40.
Players were (presumed, to be verified — see Data Quality Checks below)
randomly assigned to one of two groups:

- **Control (`gate_30`):** gate stays at level 30
- **Treatment (`gate_40`):** gate moved to level 40

## Hypotheses

**H1 (primary):** Moving the gate from level 30 to level 40 changes 7-day
retention.

- Null (H0): 7-day retention is equal between `gate_30` and `gate_40`.
- Alternative (H1): 7-day retention differs between `gate_30` and `gate_40`.
- Two-sided, not one-sided — going in, there's a real argument in both
  directions (a later gate could mean more free content before the first
  paywall-like friction point, which could help retention; or it could mean
  players quit from unblocked fatigue before ever hitting the gate that was
  quietly pacing them). A one-sided test would mean picking a direction I
  can't actually justify yet.

## Primary vs. guardrail metrics — and why

The dataset carries three usable outcome metrics:
`retention_1`, `retention_7`, `sum_gamerounds`. Picking one primary metric
*now*, before seeing results, is the actual point of this document — it's
what stops a non-significant primary result from quietly being swapped for
whichever secondary metric happened to come out significant.

| Metric | Role | Reasoning |
|---|---|---|
| `retention_7` | **Primary** | Least noisy signal of genuine sustained engagement. `retention_1` is closer to a same-session reflex (did they open the app the next day at all) and is more sensitive to day-of-week / launch-day noise. 7-day is close enough to "this game held their attention past the first curiosity visit" to be the number a real product decision should hinge on. |
| `retention_1` | Guardrail | Should be checked so a change that helps 7-day retention but craters next-day retention doesn't get waved through unexamined. |
| `sum_gamerounds` | Guardrail | Engagement/monetization proxy. Heavily right-skewed (a small number of players play a huge number of rounds), so it will need a non-parametric test or a log-transform — a plain mean/t-test would be misleading here. Flagged now so it doesn't get treated the same way as the retention metrics later. |

**Decision rule:** ship/no-ship is driven by `retention_7`. The guardrails
don't override a significant primary result on their own, but a primary
result that "wins" while a guardrail moves sharply the wrong way is reported
as a trade-off, not silently ignored.

## Minimum detectable effect (MDE) — deferred, on purpose

I don't yet know the sample size or the base retention rate, so I can't
compute a real MDE — and I'm deliberately not guessing a number now just to
have one filled in. That's Phase 3 (power analysis), done right after the
data quality checks. What I *am* committing to now: the power analysis will
be run and reported *before* the hypothesis test result is looked at, not
after — otherwise it stops being power analysis and becomes a post-hoc
rationalization of whatever came out.

## Statistical test plan

- **Primary (`retention_7`):** two-proportion z-test (or chi-square — same
  result for a 2x2), since this is a binary outcome. Cross-checked with a
  bootstrap confidence interval on the difference in proportions, so the
  conclusion doesn't rest on the normal-approximation assumption alone.
- **Guardrail (`retention_1`):** same approach as the primary metric.
- **Guardrail (`sum_gamerounds`):** not a t-test, because of the skew noted
  above — planned approach is a Mann-Whitney U test and/or a bootstrap CI on
  the difference in medians (final choice made when the actual distribution
  is visible, but "plain t-test on the raw mean" is ruled out now).
- **Multiple comparisons:** one primary test at α = 0.05. The two guardrail
  tests are exploratory context, not additional shots at "significance" —
  they will not be used to salvage a null primary result.

## Data quality checks (before any hypothesis test is trusted)

To be run in Phase 2, and the primary test result is not reported without
these passing first:

- **Sample ratio mismatch (SRM):** are the two groups actually close to
  50/50, or does the observed split deviate from the intended randomization
  in a way that suggests a bug in the assignment mechanism?
- Duplicate `userid`s, missing values, and impossible values (negative
  rounds, retention flags without a corresponding install, etc.)
- Randomization unit sanity check: confirm assignment is per-player, not
  something coarser that would make the observations non-independent.

## Decision framework

| Outcome | Interpretation |
|---|---|
| `retention_7` significant, guardrails stable or also favorable | Ship |
| `retention_7` significant, but a guardrail moves sharply against it | Trade-off — report both, no automatic ship/no-ship call |
| `retention_7` not significant | Don't ship on this evidence; note the achieved power/MDE from Phase 3 so "not significant" can be distinguished from "underpowered to detect a real effect" |

## What would change this plan

Nothing in this document should be edited once real data has been looked at.
If the data quality checks in Phase 2 reveal something that invalidates an
assumption here (e.g. randomization wasn't actually per-player), that gets
recorded as a new dated note below this line — not a silent edit above it.

---

## Amendments

**2026-09-21 — borderline Sample Ratio Mismatch found in Phase 2.** The
gate_30/gate_40 split is 49.56%/50.44% (χ² = 6.90, p = 0.0086), which flags
against this document's p < 0.01 SRM threshold but would not flag against a
stricter p < 0.001 threshold some practitioners use specifically because
large-sample SRM tests are oversensitive to small imbalances. Full
discussion in [`DATA_QUALITY.md`](DATA_QUALITY.md). Decision: proceed to
Phase 3, but this caveat must be carried into the final write-up (Phase 7)
rather than dropped once the headline result is in — the primary hypothesis
test's result should be read as "conditional on a not-fully-clean SRM check"
until/unless investigated further.
