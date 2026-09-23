# ============================================================
# EduVision_DV - Recalculate University Matching
# ============================================================
# Recalculates exact university-name overlap after applying
# the manually validated aliases.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ============================================================
# 2. Load alias-applied datasets
# ============================================================

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_alias_applied.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_alias_applied.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_alias_applied.csv"
)


# ============================================================
# 3. Create unique university-name sets
# ============================================================

qs_names = set(
    qs["University_Name_Standard"]
    .dropna()
    .astype(str)
)

the_names = set(
    the["University_Name_Standard"]
    .dropna()
    .astype(str)
)

wur_names = set(
    wur["University_Name_Standard"]
    .dropna()
    .astype(str)
)


# ============================================================
# 4. Calculate pairwise intersections
# ============================================================

qs_the = qs_names & the_names
qs_wur = qs_names & wur_names
the_wur = the_names & wur_names

all_three = qs_names & the_names & wur_names


# ============================================================
# 5. Calculate dataset-only universities
# ============================================================

qs_only = qs_names - the_names - wur_names
the_only = the_names - qs_names - wur_names
wur_only = wur_names - qs_names - the_names


# ============================================================
# 6. Display matching statistics
# ============================================================

print("=" * 80)
print("UNIVERSITY MATCHING AFTER CONTROLLED ALIAS APPLICATION")
print("=" * 80)

print("\nUnique universities:")
print(f"QS:  {len(qs_names)}")
print(f"THE: {len(the_names)}")
print(f"WUR: {len(wur_names)}")

print("\nPairwise overlaps:")
print(f"QS ∩ THE:  {len(qs_the)}")
print(f"QS ∩ WUR:  {len(qs_wur)}")
print(f"THE ∩ WUR: {len(the_wur)}")

print("\nAll three datasets:")
print(f"QS ∩ THE ∩ WUR: {len(all_three)}")

print("\nDataset-only universities:")
print(f"QS only:  {len(qs_only)}")
print(f"THE only: {len(the_only)}")
print(f"WUR only: {len(wur_only)}")


# ============================================================
# 7. Save the three-way matched university list
# ============================================================

matched_file = (
    CLEANED_DATA_DIR /
    "universities_matched_all_three.csv"
)

matched_df = pd.DataFrame(
    sorted(all_three),
    columns=["University_Name_Standard"]
)

matched_df.to_csv(
    matched_file,
    index=False
)


# ============================================================
# 8. Save dataset-only lists for later investigation
# ============================================================

pd.DataFrame(
    sorted(qs_only),
    columns=["University_Name_Standard"]
).to_csv(
    CLEANED_DATA_DIR / "qs_only_universities.csv",
    index=False
)

pd.DataFrame(
    sorted(the_only),
    columns=["University_Name_Standard"]
).to_csv(
    CLEANED_DATA_DIR / "the_only_universities.csv",
    index=False
)

pd.DataFrame(
    sorted(wur_only),
    columns=["University_Name_Standard"]
).to_csv(
    CLEANED_DATA_DIR / "wur_only_universities.csv",
    index=False
)


# ============================================================
# 9. Completion message
# ============================================================

print("\n" + "=" * 80)
print("MATCHING FILES CREATED")
print("=" * 80)

print(matched_file)

print("\n" + "=" * 80)
print("MATCHING RECALCULATION COMPLETED")
print("=" * 80)