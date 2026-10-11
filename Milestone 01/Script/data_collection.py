# ============================================================
# EduVision_DV - Raw Dataset Inspection
# ============================================================
# This script loads all raw datasets and generates a basic
# structural and data-quality report.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define the project directories
# ============================================================

# Get the main project directory from this script's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the folder containing the original datasets
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# 2. Define the raw datasets
# ============================================================

datasets = {
    "QS 2025": RAW_DATA_DIR / "qs_2025_raw.csv",
    "THE 2024": RAW_DATA_DIR / "the_2024_raw.csv",
    "World Bank Education": RAW_DATA_DIR / "world_bank_education_raw.csv",
    "WUR 2023": RAW_DATA_DIR / "wur_2023_raw.csv",
}


# ============================================================
# 3. Inspect each dataset
# ============================================================

for dataset_name, file_path in datasets.items():

    print("\n" + "=" * 80)
    print(f"DATASET: {dataset_name}")
    print("=" * 80)

    # Check whether the expected file exists
    if not file_path.exists():
        print(f"ERROR: File not found -> {file_path}")
        continue

    # Load the CSV dataset
    df = pd.read_csv(file_path)

    # --------------------------------------------------------
    # Display basic dataset information
    # --------------------------------------------------------

    print(f"\nFile: {file_path.name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # --------------------------------------------------------
    # Display column names
    # --------------------------------------------------------

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    # --------------------------------------------------------
    # Display data types
    # --------------------------------------------------------

    print("\nData Types:")
    print(df.dtypes.to_string())

    # --------------------------------------------------------
    # Check missing values
    # --------------------------------------------------------

    print("\nMissing Values:")

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("  No missing values found.")
    else:
        print(missing.to_string())

    # --------------------------------------------------------
    # Check duplicate rows
    # --------------------------------------------------------

    duplicate_count = df.duplicated().sum()

    print(f"\nDuplicate Rows: {duplicate_count}")

    # --------------------------------------------------------
    # Display first three records
    # --------------------------------------------------------

    print("\nFirst 3 Records:")
    print(df.head(3).to_string())

print("\n" + "=" * 80)
print("RAW DATASET INSPECTION COMPLETED")
print("=" * 80)