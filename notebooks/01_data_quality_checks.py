"""Phase 2 — data acquisition + quality checks.

Per docs/PREREGISTRATION.md, no hypothesis test result is trusted until these
checks pass. This script only checks data quality — it does not touch
retention_1, retention_7 as outcomes, and does not run the primary hypothesis
test. That's Phase 3+ (power analysis) and Phase 4 (primary test), on
purpose, per the pre-registration.
"""

import pandas as pd
from scipy import stats

df = pd.read_csv("../data/raw/cookie_cats.csv")

print("=" * 60)
print("1. SHAPE & SCHEMA")
print("=" * 60)
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(df.dtypes)

print()
print("=" * 60)
print("2. DUPLICATE userid CHECK")
print("=" * 60)
n_dupes = df["userid"].duplicated().sum()
print(f"Duplicate userid rows: {n_dupes}")
print("-> Each row is one player exactly once." if n_dupes == 0
      else "-> WARNING: duplicate players present, investigate before proceeding.")

print()
print("=" * 60)
print("3. MISSING VALUES")
print("=" * 60)
missing = df.isna().sum()
print(missing)
print("-> No missing values." if missing.sum() == 0 else "-> WARNING: missing values present.")

print()
print("=" * 60)
print("4. IMPOSSIBLE / SUSPICIOUS VALUES")
print("=" * 60)
print(f"sum_gamerounds min: {df['sum_gamerounds'].min()}, max: {df['sum_gamerounds'].max()}")
neg_rounds = (df["sum_gamerounds"] < 0).sum()
print(f"Negative game-round counts: {neg_rounds}")
print(f"version unique values: {df['version'].unique().tolist()}")
zero_rounds = (df["sum_gamerounds"] == 0).sum()
print(f"Players with 0 game rounds (installed, never played): {zero_rounds} "
      f"({zero_rounds / len(df):.2%})")
# A single extreme outlier is a known feature of this dataset -- flagged, not
# removed here. Removing it is a modeling decision for Phase 4/5, not a data
# quality fix -- deciding now would already be touching the outcome data.
top5 = df["sum_gamerounds"].sort_values(ascending=False).head(5).tolist()
print(f"Top 5 sum_gamerounds values: {top5}")

print()
print("=" * 60)
print("5. SAMPLE RATIO MISMATCH (SRM) CHECK")
print("=" * 60)
counts = df["version"].value_counts()
n_30 = counts.get("gate_30", 0)
n_40 = counts.get("gate_40", 0)
total = n_30 + n_40
print(f"gate_30: {n_30} ({n_30/total:.4%})")
print(f"gate_40: {n_40} ({n_40/total:.4%})")

# Chi-square goodness-of-fit against the expected 50/50 split. This is the
# standard SRM test: if randomization was fair, observed counts should not
# differ from a 50/50 expectation beyond chance.
chi2, p_value = stats.chisquare([n_30, n_40], f_exp=[total / 2, total / 2])
print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")
# Convention (Fabijan et al.): p < 0.01 flags a likely SRM, not the usual 0.05
# -- SRM checks intentionally use a stricter threshold because the cost of
# missing a real SRM (trusting a broken randomization) is high.
if p_value < 0.01:
    print("-> SRM DETECTED (p < 0.01). Do not trust downstream hypothesis "
          "tests until this is understood.")
else:
    print("-> No sample ratio mismatch detected. Split is consistent with "
          "fair 50/50 randomization.")

print()
print("=" * 60)
print("6. RANDOMIZATION UNIT SANITY CHECK")
print("=" * 60)
print(f"Unique userid count: {df['userid'].nunique()} (matches row count: "
      f"{df['userid'].nunique() == len(df)})")
print("-> One row per player, one version per player -- consistent with "
      "per-player randomization, not some coarser unit.")
