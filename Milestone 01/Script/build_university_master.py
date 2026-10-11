# ============================================================
# EduVision_DV - Build Final University Master Dataset
# ============================================================
# Combines the validated three-way university matches with
# the corresponding QS, THE, and WUR records.
#
# Output:
#   data/final/university_master_dataset.csv
#
# Raw and cleaned source files are not modified.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"
FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"


# ============================================================
# 2. Create final data directory if necessary
# ============================================================

FINAL_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 3. Load authoritative university matching table
# ============================================================

master = pd.read_csv(
    CLEANED_DATA_DIR /
    "university_master_final.csv"
)


# ============================================================
# 4. Load source datasets
# ============================================================

qs = pd.read_csv(
    CLEANED_DATA_DIR /
    "qs_2025_alias_applied.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR /
    "the_2024_standardized.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR /
    "wur_2023_standardized.csv"
)


# ============================================================
# 5. Create the same Match_Key
# ============================================================

# The authoritative master already contains Match_Key.
# Create matching keys for the three source datasets.

def create_key(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(
            r"[^a-z0-9]",
            "",
            regex=True
        )
    )


qs["Match_Key"] = create_key(
    qs["University_Name_Standard"]
)

the["Match_Key"] = create_key(
    the["University_Name_Standard"]
)

wur["Match_Key"] = create_key(
    wur["University_Name_Standard"]
)


# ============================================================
# 6. Keep only required source records
# ============================================================

qs = qs[
    qs["Match_Key"].isin(
        master["Match_Key"]
    )
].copy()

the = the[
    the["Match_Key"].isin(
        master["Match_Key"]
    )
].copy()

wur = wur[
    wur["Match_Key"].isin(
        master["Match_Key"]
    )
].copy()


# ============================================================
# 7. Remove duplicate records by Match_Key
# ============================================================

qs = qs.drop_duplicates(
    "Match_Key"
)

the = the.drop_duplicates(
    "Match_Key"
)

wur = wur.drop_duplicates(
    "Match_Key"
)


# ============================================================
# 8. Prefix source-specific columns
# ============================================================

qs_columns = [
    "Match_Key",
    "RANK_2025",
    "RANK_2024",
    "Academic_Reputation_Score",
    "Faculty_Student_Score",
    "International_Students_Score"
]

qs_available = [
    col for col in qs_columns
    if col in qs.columns
]

qs_data = qs[qs_available].copy()

qs_data = qs_data.rename(
    columns={
        col: f"QS_{col}"
        for col in qs_available
        if col != "Match_Key"
    }
)


# ============================================================
# 9. Prepare THE data
# ============================================================

the_columns = [
    "Match_Key",
    "Rank",
    "Student Population",
    "Students to Staff Ratio",
    "International Students",
    "Overall Score",
    "Teaching",
    "Research Environment",
    "Research Quality",
    "Industry Impact",
    "International Outlook"
]

the_available = [
    col for col in the_columns
    if col in the.columns
]

the_data = the[the_available].copy()

the_data = the_data.rename(
    columns={
        col: f"THE_{col.replace(' ', '_')}"
        for col in the_available
        if col != "Match_Key"
    }
)


# ============================================================
# 10. Prepare WUR data
# ============================================================

wur_columns = [
    "Match_Key",
    "No of student",
    "No of student per staff",
    "International Student",
    "Female:Male Ratio",
    "OverAll Score",
    "Teaching Score",
    "Research Score",
    "Citations Score",
    "Industry Income Score",
    "International Outlook Score"
]

wur_available = [
    col for col in wur_columns
    if col in wur.columns
]

wur_data = wur[wur_available].copy()

wur_data = wur_data.rename(
    columns={
        col: f"WUR_{col.replace(' ', '_').replace(':', '_')}"
        for col in wur_available
        if col != "Match_Key"
    }
)


# ============================================================
# 11. Merge QS data
# ============================================================

final = master.merge(
    qs_data,
    on="Match_Key",
    how="left"
)


# ============================================================
# 12. Merge THE data
# ============================================================

final = final.merge(
    the_data,
    on="Match_Key",
    how="left"
)


# ============================================================
# 13. Merge WUR data
# ============================================================

final = final.merge(
    wur_data,
    on="Match_Key",
    how="left"
)


# ============================================================
# 14. Add dataset presence flags
# ============================================================

final["Has_QS"] = (
    final["QS_RANK_2025"].notna()
)

final["Has_THE"] = (
    final["THE_Rank"].notna()
)

final["Has_WUR"] = (
    final["WUR_OverAll_Score"].notna()
)


# ============================================================
# 15. Save final master dataset
# ============================================================

output_file = (
    FINAL_DATA_DIR /
    "university_master_dataset.csv"
)

final.to_csv(
    output_file,
    index=False
)


# ============================================================
# 16. Display validation statistics
# ============================================================

print("=" * 80)
print("FINAL UNIVERSITY MASTER DATASET")
print("=" * 80)

print(f"\nTotal universities: {len(final)}")

print(
    f"QS records:  "
    f"{final['Has_QS'].sum()}"
)

print(
    f"THE records: "
    f"{final['Has_THE'].sum()}"
)

print(
    f"WUR records: "
    f"{final['Has_WUR'].sum()}"
)

print(
    "\nUniversities with all three sources: "
    f"{(
        final['Has_QS']
        & final['Has_THE']
        & final['Has_WUR']
    ).sum()}"
)


# ============================================================
# 17. Check duplicate University IDs
# ============================================================

duplicate_ids = (
    final["University_ID"]
    .duplicated()
    .sum()
)

print(
    f"\nDuplicate University_ID rows: "
    f"{duplicate_ids}"
)


# ============================================================
# 18. Display output
# ============================================================

print("\n" + "=" * 80)
print("FILE CREATED")
print("=" * 80)

print(output_file)

print("\n" + "=" * 80)
print("MASTER DATASET BUILD COMPLETED")
print("=" * 80)