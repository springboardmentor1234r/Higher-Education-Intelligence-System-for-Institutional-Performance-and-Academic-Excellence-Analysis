# ============================================================
# EduVision_DV - Cross-Dataset University Matching
# ============================================================
# This script checks university-name matches across
# QS, THE and WUR standardized datasets.
#
# It does NOT modify the datasets.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ------------------------------------------------------------
# Load standardized datasets
# ------------------------------------------------------------

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_standardized.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_standardized.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_standardized.csv"
)


# ------------------------------------------------------------
# Create sets of standardized university names
# ------------------------------------------------------------

qs_names = set(
    qs["University_Name_Standard"].dropna()
)

the_names = set(
    the["University_Name_Standard"].dropna()
)

wur_names = set(
    wur["University_Name_Standard"].dropna()
)


# ------------------------------------------------------------
# Calculate pairwise matches
# ------------------------------------------------------------

qs_the = qs_names & the_names
qs_wur = qs_names & wur_names
the_wur = the_names & wur_names


# ------------------------------------------------------------
# Calculate three-way matches
# ------------------------------------------------------------

all_three = (
    qs_names
    & the_names
    & wur_names
)


# ------------------------------------------------------------
# Calculate unique-to-each-dataset universities
# ------------------------------------------------------------

qs_only = qs_names - the_names - wur_names
the_only = the_names - qs_names - wur_names
wur_only = wur_names - qs_names - the_names


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("=" * 80)
print("CROSS-DATASET UNIVERSITY MATCHING")
print("=" * 80)

print("\nUNIQUE UNIVERSITY COUNTS")
print("-" * 80)

print(f"QS unique universities  : {len(qs_names)}")
print(f"THE unique universities : {len(the_names)}")
print(f"WUR unique universities : {len(wur_names)}")


print("\n" + "=" * 80)
print("PAIRWISE MATCHES")
print("=" * 80)

print(f"\nQS ∩ THE : {len(qs_the)}")
print(f"QS ∩ WUR : {len(qs_wur)}")
print(f"THE ∩ WUR: {len(the_wur)}")


print("\n" + "=" * 80)
print("THREE-WAY MATCH")
print("=" * 80)

print(
    f"\nQS ∩ THE ∩ WUR : {len(all_three)}"
)


print("\n" + "=" * 80)
print("DATASET-SPECIFIC UNIVERSITIES")
print("=" * 80)

print(f"\nQS only  : {len(qs_only)}")
print(f"THE only : {len(the_only)}")
print(f"WUR only : {len(wur_only)}")


# ------------------------------------------------------------
# Show sample three-way matches
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("SAMPLE THREE-WAY MATCHES")
print("=" * 80)

for name in sorted(all_three)[:30]:
    print(name)


# ------------------------------------------------------------
# Show sample QS-only universities
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("SAMPLE QS-ONLY UNIVERSITIES")
print("=" * 80)

for name in sorted(qs_only)[:30]:
    print(name)


# ------------------------------------------------------------
# Show sample THE-only universities
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("SAMPLE THE-ONLY UNIVERSITIES")
print("=" * 80)

for name in sorted(the_only)[:30]:
    print(name)


# ------------------------------------------------------------
# Show sample WUR-only universities
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("SAMPLE WUR-ONLY UNIVERSITIES")
print("=" * 80)

for name in sorted(wur_only)[:30]:
    print(name)


# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("MATCHING ANALYSIS COMPLETED")
print("=" * 80)