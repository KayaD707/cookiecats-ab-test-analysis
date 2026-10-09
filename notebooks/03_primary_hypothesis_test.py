"""Phase 4 — the primary hypothesis test.

Per docs/PREREGISTRATION.md: tests H1 on retention_7 (the pre-registered
primary metric) using a two-proportion z-test, cross-checked against a
chi-square test (same result for a 2x2 table) and a bootstrap confidence
interval. This is the first script in the project that actually compares
gate_30 vs gate_40 outcomes -- everything before this (Phases 2 and 3) was
deliberately structured to avoid looking at this comparison early.

retention_1 and sum_gamerounds (the guardrail metrics) are NOT tested here --
that's Phase 5, kept separate on purpose so a null result here can't get
quietly rescued by switching metrics.
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(seed=42)

df = pd.read_csv("../data/raw/cookie_cats.csv")

group_30 = df.loc[df["version"] == "gate_30", "retention_7"]
group_40 = df.loc[df["version"] == "gate_40", "retention_7"]

n_30, n_40 = len(group_30), len(group_40)
x_30, x_40 = group_30.sum(), group_40.sum()
p_30, p_40 = x_30 / n_30, x_40 / n_40

print("=" * 60)
print("DESCRIPTIVE")
print("=" * 60)
print(f"gate_30: {x_30}/{n_30} retained at day 7 = {p_30:.4%}")
print(f"gate_40: {x_40}/{n_40} retained at day 7 = {p_40:.4%}")
print(f"Absolute difference (gate_40 - gate_30): {(p_40 - p_30)*100:+.3f} percentage points")
print(f"Relative difference: {(p_40 - p_30) / p_30:+.2%}")

print()
print("=" * 60)
print("PRIMARY TEST: two-proportion z-test (pre-registered)")
print("=" * 60)
count = np.array([x_40, x_30])
nobs = np.array([n_40, n_30])
z_stat, p_value = proportions_ztest(count, nobs)
print(f"z = {z_stat:.4f}")
print(f"p-value (two-sided) = {p_value:.5f}")
alpha = 0.05
if p_value < alpha:
    print(f"-> Significant at alpha={alpha}: reject H0, retention_7 differs between arms.")
else:
    print(f"-> NOT significant at alpha={alpha}: fail to reject H0.")

print()
print("=" * 60)
print("CROSS-CHECK: chi-square test of independence")
print("=" * 60)
# Pre-registration: "two-proportion z-test (or chi-square -- same result for
# a 2x2)". Confirming that here rather than just asserting it.
table = pd.crosstab(df["version"], df["retention_7"])
chi2, p_chi2, dof, expected = stats.chi2_contingency(table, correction=False)
print(table)
print(f"chi2 = {chi2:.4f}, p = {p_chi2:.5f}, dof = {dof}")
print(f"z^2 = {z_stat**2:.4f} (should equal chi2 above for a 2x2 table)")

print()
print("=" * 60)
print("BOOTSTRAP CONFIDENCE INTERVAL (cross-check, not assuming normality)")
print("=" * 60)
n_boot = 10000
arr_30 = group_30.to_numpy()
arr_40 = group_40.to_numpy()
boot_diffs = np.empty(n_boot)
for i in range(n_boot):
    sample_30 = rng.choice(arr_30, size=n_30, replace=True)
    sample_40 = rng.choice(arr_40, size=n_40, replace=True)
    boot_diffs[i] = sample_40.mean() - sample_30.mean()

ci_low, ci_high = np.percentile(boot_diffs, [2.5, 97.5])
print(f"Bootstrap resamples: {n_boot}")
print(f"Observed difference (gate_40 - gate_30): {(p_40 - p_30)*100:+.3f} pp")
print(f"95% bootstrap CI: [{ci_low*100:+.3f}pp, {ci_high*100:+.3f}pp]")
print("-> CI excludes 0" if ci_low > 0 or ci_high < 0 else "-> CI includes 0 (consistent with the z-test result)")

print()
print("=" * 60)
print("READING THIS AGAINST PHASE 3 (POWER ANALYSIS)")
print("=" * 60)
mde_pp = 0.74
observed_pp = abs((p_40 - p_30) * 100)
print(f"Pre-registered MDE at 80% power: {mde_pp}pp")
print(f"Observed absolute effect: {observed_pp:.3f}pp")
if observed_pp < mde_pp:
    print("-> Observed effect is SMALLER than this study's MDE -- a null result "
          "here is informative (true effect is likely small), not just "
          "'underpowered to see it'.")
else:
    print("-> Observed effect is at or above this study's MDE -- within the "
          "range this sample size was well-powered to detect.")
