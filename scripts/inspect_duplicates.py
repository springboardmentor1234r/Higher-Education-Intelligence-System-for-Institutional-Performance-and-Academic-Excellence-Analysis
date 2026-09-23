# ============================================================
# EduVision_DV - WUR Valid Record Profiling
# ============================================================
# This script profiles only identifiable university records.
# It does NOT modify the raw dataset.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Locate the raw WUR dataset
# ============================================================

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Define the WUR dataset path
WUR_FILE = RAW_DATA_DIR / "wur_2023_raw.csv"


# ============================================================
# 2. Load the raw WUR dataset
# ============================================================

df = pd.read_csv(WUR_FILE)


# ============================================================
# 3. Keep only identifiable university records
# ============================================================

# A valid university record must have a university name
valid_df = df[df["Name of University"].notna()].copy()


# ============================================================
# 4. Display basic statistics
# ============================================================

print("=" * 80)
print("WUR VALID UNIVERSITY RECORD PROFILE")
print("=" * 80)

print(f"\nRaw records: {len(df)}")
print(f"Identifiable university records: {len(valid_df)}")


# ============================================================
# 5. Display column information
# ============================================================

print("\n" + "=" * 80)
print("COLUMN DATA TYPES")
print("=" * 80)

print(valid_df.dtypes.to_string())


# ============================================================
# 6. Display missing values
# ============================================================

print("\n" + "=" * 80)
print("MISSING VALUES IN VALID UNIVERSITY RECORDS")
print("=" * 80)

missing = valid_df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("No missing values.")
else:
    print(missing.to_string())


# ============================================================
# 7. Display sample records
# ============================================================

print("\n" + "=" * 80)
print("SAMPLE VALID UNIVERSITY RECORDS")
print("=" * 80)

print(
    valid_df[
        [
            "University Rank",
            "Name of University",
            "Location",
            "No of student",
            "No of student per staff",
            "International Student",
            "Female:Male Ratio",
            "OverAll Score",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 8. Display unique value samples for important fields
# ============================================================

profile_columns = [
    "No of student",
    "No of student per staff",
    "International Student",
    "Female:Male Ratio",
    "OverAll Score",
]


print("\n" + "=" * 80)
print("VALUE FORMAT INSPECTION")
print("=" * 80)

for column in profile_columns:

    print(f"\n--- {column} ---")

    # Display up to 10 unique non-null values
    values = (
        valid_df[column]
        .dropna()
        .astype(str)
        .unique()
    )

    for value in values[:10]:
        print(f"  {value}")


# ============================================================
# 9. Check duplicate university names
# ============================================================

duplicate_names = valid_df[
    valid_df.duplicated(
        subset=["Name of University"],
        keep=False
    )
]

print("\n" + "=" * 80)
print("DUPLICATE UNIVERSITY NAMES")
print("=" * 80)

print(f"Duplicate-name records: {len(duplicate_names)}")


# ============================================================
# 10. Final summary
# ============================================================

print("\n" + "=" * 80)
print("WUR PROFILING COMPLETED")
print("=" * 80)