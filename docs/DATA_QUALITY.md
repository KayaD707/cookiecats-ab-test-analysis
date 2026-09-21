# Data Quality Checks — Phase 2

Run via [`notebooks/01_data_quality_checks.py`](../notebooks/01_data_quality_checks.py),
against the checklist committed to in [`PREREGISTRATION.md`](PREREGISTRATION.md). Nothing
in this document touches `retention_1`, `retention_7`, or `sum_gamerounds` as an *outcome*
— that's deliberately out of scope until Phase 3 (power analysis) and Phase 4 (primary
test).

## Dataset

90,189 rows, one per player: `userid`, `version` (`gate_30` / `gate_40`), `sum_gamerounds`,
`retention_1`, `retention_7`. No missing values, no duplicate `userid`s, no negative round
counts. `userid` count equals row count, so the randomization unit is confirmed to be the
individual player, not something coarser.

## The one real finding: a borderline Sample Ratio Mismatch

| | gate_30 | gate_40 |
|---|---|---|
| Count | 44,700 | 45,489 |
| Share | 49.56% | 50.44% |

A chi-square goodness-of-fit test against an expected 50/50 split gives **χ² = 6.90, p =
0.0086**. Against the threshold this project committed to in the pre-registration (p <
0.01, per standard SRM-testing practice — stricter than the usual 0.05 specifically
because trusting a broken randomization is a worse mistake than a false alarm), this
**technically flags as an SRM**.

**But this needs a second read, not a reflexive stop.** At n = 90,189, a chi-square test is
extremely sensitive — a 0.88-percentage-point gap between groups is enough to cross p =
0.01 even though it's a small effect in absolute terms. This is a well-known property of
SRM testing at scale: some practitioners (notably Kohavi's experimentation team) use an
even stricter threshold (p < 0.001) *specifically* to avoid flagging deviations this small.
By that stricter standard, this result would **not** flag (p = 0.0086 > 0.001).

**What this means concretely:** the split is close enough to 50/50 that it's very unlikely
to meaningfully bias a well-powered analysis, but it isn't the clean, unambiguous pass the
pre-registration hoped for either. This dataset is a public one with no access to the
original assignment logs, so the usual next step for a real SRM investigation — checking
whether the mechanism generating the imbalance is itself correlated with the outcome
(e.g., a bug that dropped certain devices/regions differently per arm) — isn't fully
available here. That's a real limitation of working with a public dataset rather than a
live experiment, and it's being written down rather than quietly worked around.

## Decision for now

Proceed to Phase 3 (power analysis), but carry this forward explicitly rather than treat
Phase 2 as a clean pass. The eventual write-up (Phase 7) needs to state this caveat
alongside the headline result, not bury it. See the dated amendment in
[`PREREGISTRATION.md`](PREREGISTRATION.md) — the pre-registration's own rules require this
to be logged there, not silently absorbed.

## Other findings, for completeness

- 4.43% of players (3,994) installed and played zero rounds. Real, not a data error —
  worth keeping in mind for Phase 6 (segment analysis): a "never engaged" segment may
  behave differently from the rest of the population.
- One extreme outlier: a single player with 49,854 rounds (the next-highest is 2,961).
  Not removed here — that's a modeling decision for later phases, not a data-quality fix,
  and removing it now would mean making an outcome-related judgment call before the
  analysis plan says to.
