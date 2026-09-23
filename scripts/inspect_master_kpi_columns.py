# ============================================================
# EduVision_DV - Inspect Master Dataset KPI Fields
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"


# ============================================================
# 2. Load the final master dataset
# ============================================================

df = pd.read_csv(
    FINAL_DATA_DIR /
    "university_master_dataset.csv"
)


# ============================================================
# 3. Display dataset dimensions
# ============================================================

print("=" * 80)
print("MASTER DATASET OVERVIEW")
print("=" * 80)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ============================================================
# 4. Display all columns
# ============================================================

print("\n" + "=" * 80)
print("AVAILABLE COLUMNS")
print("=" * 80)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:02d}. {column}")


# ============================================================
# 5. Display missing-value summary
# ============================================================

print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)

missing = df.isna().sum()

missing = missing[
    missing > 0
].sort_values(
    ascending=False
)

print(missing.to_string())


# ============================================================
# 6. Display data types
# ============================================================

print("\n" + "=" * 80)
print("DATA TYPES")
print("=" * 80)

print(
    df.dtypes.to_string()
)


# ============================================================
# 7. Display sample records
# ============================================================

print("\n" + "=" * 80)
print("SAMPLE RECORDS")
print("=" * 80)

print(
    df.head(5).to_string()
)