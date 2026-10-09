# Primary Hypothesis Test — Phase 4

Run via [`notebooks/03_primary_hypothesis_test.py`](../notebooks/03_primary_hypothesis_test.py).
This is the first point in the project where `gate_30` and `gate_40` outcomes are actually
compared — everything in Phases 1–3 was deliberately structured to avoid looking at this
early.

## Result

| | `gate_30` (control) | `gate_40` (treatment) |
|---|---|---|
| n | 44,700 | 45,489 |
| Retained at day 7 | 8,502 | 8,279 |
| `retention_7` rate | 19.02% | 18.20% |

**Absolute difference: −0.82 percentage points. Relative difference: −4.31%.** Moving the
gate from level 30 to level 40 is associated with *lower* 7-day retention, not higher.

- **Two-proportion z-test (pre-registered primary test):** z = −3.16, **p = 0.00155**
- **Chi-square cross-check:** χ² = 10.01, p = 0.00155, confirming z² = χ² exactly, as
  expected for a 2×2 table
- **Bootstrap 95% CI** (10,000 resamples, not assuming normality): **[−1.34pp, −0.33pp]** —
  excludes zero, agreeing with the z-test

At α = 0.05, this is **statistically significant**. Per the pre-registered decision
framework, a significant primary result normally means "ship" — except this result points
the *opposite* direction from what "shipping the gate_40 change" would require, so the
real conclusion is: **don't move the gate to level 40** — the evidence says the later gate
hurts retention, not helps it. H1 is supported, just not in the direction a product team
hoping to ship this change would have wanted.

## Reading this against the power analysis (Phase 3)

The pre-registered minimum detectable effect at 80% power was 0.74pp. The observed effect
(0.82pp) is **above** that threshold — this result sits within the range the study was
well-powered to detect, not a borderline detection riding on statistical noise. Compare
this to the Phase 2 SRM finding, which *was* a genuinely borderline call; this result is
not in the same category of ambiguity.

## The SRM caveat, still carried forward

Per the pre-registration's own amendment rule: the Phase 2 finding (a borderline sample
ratio mismatch, p = 0.0086 against the committed p < 0.01 threshold) is not resolved by
this result being clean. It's a separate, open question — could a mechanism that caused a
slight imbalance in group *sizes* also have introduced a confound that affects the
*outcome*? Nothing found in Phase 2 points to that, but nothing has actively ruled it out
either. This gets carried into the Phase 7 write-up as a caveat on an otherwise clean
result, not quietly dropped because the headline number came out significant.

## What's not tested here, on purpose

`retention_1` and `sum_gamerounds` — the two pre-registered guardrail metrics — are not
touched in this script. Testing them is Phase 5, kept deliberately separate so this
primary result can't later be quietly supplemented or rescued by a guardrail metric if it
had come out differently. It didn't need rescuing here, but the discipline applies
regardless of how the primary result landed.
