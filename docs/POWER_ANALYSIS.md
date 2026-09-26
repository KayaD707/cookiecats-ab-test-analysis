# Power Analysis — Phase 3

Run via [`notebooks/02_power_analysis.py`](../notebooks/02_power_analysis.py), using
**only the control group's (`gate_30`) baseline `retention_7` rate** and the actual
sample sizes from Phase 2. This does not compare `gate_30` vs `gate_40` outcomes —
that's Phase 4. Using a baseline rate to plan/evaluate power is standard practice, not
a look at the treatment effect the pre-registration committed to not peeking at yet.

## Inputs

| | Value |
|---|---|
| n (`gate_30`, control) | 44,700 |
| n (`gate_40`, treatment) | 45,489 |
| Baseline `retention_7` rate (control only) | 19.02% |
| α | 0.05 (two-sided) |
| Target power | 80% |

## Achieved power at plausible effect sizes

| Absolute lift | New rate | Power |
|---|---|---|
| +0.5pp | 19.52% | 47.8% |
| +1.0pp | 20.02% | 96.6% |
| +1.5pp | 20.52% | ~100% |
| +2.0pp | 21.02% | ~100% |
| +3.0pp | 22.02% | ~100% |

## Minimum detectable effect (MDE)

**At 80% power: +0.74 percentage points absolute** (19.02% → 19.76%), a **3.89%
relative lift**. Found by numerical search rather than an analytic inversion — Cohen's
h (the effect-size measure two-proportion power calculations use) is a nonlinear
transform of the two rates, so scanning candidate effect sizes is simpler and just as
accurate as solving for it algebraically.

## What this means before looking at the actual result

- This sample size (90,189 players) is well-powered for anything but a genuinely small
  effect. A swing of even 1 percentage point in `retention_7` would have been detected
  96.6% of the time.
- If the eventual result (Phase 4) comes back **not significant**, that's meaningful:
  it means any true effect is almost certainly smaller than ~0.74pp, not that the study
  was too weak to have found a real, practically important effect. That distinction —
  "no effect" vs. "underpowered to see it" — is exactly what committing to this
  analysis *before* the test result exists to protect.
- If the result **is significant**, the MDE gives an immediate sanity check: an
  observed effect much larger than 0.74pp would be a big, easily-detected swing;
  something close to 0.74pp is a result sitting near this study's practical limit of
  resolution, worth treating with more caution before calling it a clear win.

## Caveat carried over from Phase 2

The borderline sample ratio mismatch documented in
[`DATA_QUALITY.md`](DATA_QUALITY.md) doesn't change this power analysis materially —
the actual, unequal sample sizes (44,700 vs 45,489) are already what's used above,
not an assumed clean 50/50 split. It remains a separate caveat to carry into the
Phase 4 write-up, not something this step resolves.
