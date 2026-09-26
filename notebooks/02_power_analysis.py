"""Phase 3 — power analysis.

Per docs/PREREGISTRATION.md: this is run and reported BEFORE the primary
hypothesis test result is looked at. It uses ONLY the baseline (control
group) retention_7 rate and the actual sample sizes -- it does NOT compare
gate_30 vs gate_40 outcomes. Using a baseline rate to plan/evaluate power is
standard practice and is not "peeking" at the treatment effect; comparing
the two groups' outcomes is a separate, later action (Phase 4).
"""

import numpy as np
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

df = pd.read_csv("../data/raw/cookie_cats.csv")

alpha = 0.05
power_target = 0.80

n_30 = (df["version"] == "gate_30").sum()
n_40 = (df["version"] == "gate_40").sum()
ratio = n_40 / n_30

# Baseline rate from the CONTROL group only -- this is the one number this
# script is allowed to look at before Phase 4. It is not a comparison.
baseline_rate = df.loc[df["version"] == "gate_30", "retention_7"].mean()

print("=" * 60)
print("INPUTS")
print("=" * 60)
print(f"n (gate_30, control): {n_30}")
print(f"n (gate_40, treatment): {n_40}")
print(f"Allocation ratio (n_40 / n_30): {ratio:.4f}")
print(f"Baseline retention_7 rate (control group only): {baseline_rate:.4%}")
print(f"alpha: {alpha}, target power: {power_target}")

analysis = NormalIndPower()

print()
print("=" * 60)
print("ACHIEVED POWER FOR SEVERAL PLAUSIBLE EFFECT SIZES")
print("=" * 60)
print("(i.e. \"if the true effect were this big, how likely were we to detect it "
      "with the sample size we actually have?\")")
for delta_pp in [0.5, 1.0, 1.5, 2.0, 3.0]:
    p2 = baseline_rate + delta_pp / 100
    h = proportion_effectsize(baseline_rate, p2)
    power = analysis.power(effect_size=abs(h), nobs1=n_30, ratio=ratio, alpha=alpha)
    print(f"  +{delta_pp:>4.1f}pp absolute (retention_7: {baseline_rate:.2%} -> "
          f"{p2:.2%}): power = {power:.3f}")

print()
print("=" * 60)
print("MINIMUM DETECTABLE EFFECT (MDE) AT 80% POWER")
print("=" * 60)
print("Numerical search: smallest absolute effect this sample size can detect "
      "at 80% power, alpha=0.05, two-sided.")

# Numerical search rather than an analytic inversion: proportion_effectsize
# (Cohen's h) is a nonlinear transform of p1/p2, so solving for a target h
# and converting back to a raw probability difference isn't a clean
# closed form -- a fine-grained scan is simpler and just as accurate here.
found = None
for delta_pp in np.arange(0.05, 5.0, 0.01):
    p2 = baseline_rate + delta_pp / 100
    h = proportion_effectsize(baseline_rate, p2)
    power = analysis.power(effect_size=abs(h), nobs1=n_30, ratio=ratio, alpha=alpha)
    if power >= power_target:
        found = delta_pp
        break

if found is not None:
    print(f"MDE (absolute): +{found:.2f} percentage points "
          f"(retention_7: {baseline_rate:.2%} -> {baseline_rate + found/100:.2%})")
    print(f"MDE (relative): {found/100/baseline_rate:.2%} relative lift over baseline")
else:
    print("No effect size in the scanned range reached 80% power -- widen the range.")
