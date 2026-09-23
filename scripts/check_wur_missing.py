# ============================================================
# EduVision_DV - Check Universities Missing WUR Data
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"


# ============================================================
# 2. Load the final university master dataset
# ============================================================

df = pd.read_csv(
    FINAL_DATA_DIR /
    "university_master_dataset.csv"
)


# ============================================================
# 3. Find universities without WUR data
# ============================================================

missing_wur = df[
    df["Has_WUR"] == False
].copy()


# ============================================================
# 4. Display the missing universities
# ============================================================

print("=" * 80)
print("UNIVERSITIES MISSING WUR DATA")
print("=" * 80)

print(
    f"\nTotal missing WUR records: "
    f"{len(missing_wur)}"
)

print("\n")


# ============================================================
# 5. Display useful identification columns
# ============================================================

columns = [
    "University_ID",
    "University_Name",
    "Country_Standard",
    "Match_Key"
]

available_columns = [
    col for col in columns
    if col in missing_wur.columns
]

print(
    missing_wur[available_columns].to_string(
        index=False
    )
)


# ============================================================
# 6. Save the diagnostic file
# ============================================================

output_file = (
    FINAL_DATA_DIR /
    "universities_missing_wur.csv"
)

missing_wur.to_csv(
    output_file,
    index=False
)


# ============================================================
# 7. Completion message
# ============================================================

print("\n" + "=" * 80)
print("DIAGNOSTIC FILE CREATED")
print("=" * 80)

print(output_file)