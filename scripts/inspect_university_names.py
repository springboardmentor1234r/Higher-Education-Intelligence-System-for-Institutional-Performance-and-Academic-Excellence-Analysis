# ============================================================
# EduVision_DV - University Name Inspection
# ============================================================
# This script compares university names across QS, THE and WUR.
# It does NOT modify any raw dataset.
# ============================================================

import pandas as pd
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# File paths
QS_FILE = RAW_DATA_DIR / "qs_2025_raw.csv"
THE_FILE = RAW_DATA_DIR / "the_2024_raw.csv"
WUR_FILE = RAW_DATA_DIR / "wur_2023_raw.csv"

# Load datasets
qs = pd.read_csv(QS_FILE)
the = pd.read_csv(THE_FILE)
wur = pd.read_csv(WUR_FILE)

# ------------------------------------------------------------
# Identify university-name columns
# ------------------------------------------------------------

print("=" * 80)
print("UNIVERSITY NAME COLUMN INSPECTION")
print("=" * 80)

print("\nQS columns:")
print(qs.columns.tolist())

print("\nTHE columns:")
print(the.columns.tolist())

print("\nWUR columns:")
print(wur.columns.tolist())

# ------------------------------------------------------------
# Display basic university-name information
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("UNIVERSITY NAME COUNTS")
print("=" * 80)

print(f"\nQS university records: {len(qs)}")
print(f"THE university records: {len(the)}")
print(f"WUR university records: {len(wur)}")

# ------------------------------------------------------------
# Display first 20 university names
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("FIRST 20 QS UNIVERSITY NAMES")
print("=" * 80)

print(
    qs["Institution_Name"]
    .dropna()
    .head(20)
    .to_string(index=False)
)

print("\n" + "=" * 80)
print("FIRST 20 THE UNIVERSITY NAMES")
print("=" * 80)

print(
    the["Name"]
    .dropna()
    .head(20)
    .to_string(index=False)
)

print("\n" + "=" * 80)
print("FIRST 20 WUR UNIVERSITY NAMES")
print("=" * 80)

print(
    wur["Name of University"]
    .dropna()
    .head(20)
    .to_string(index=False)
)

# ------------------------------------------------------------
# Unique university name counts
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("UNIQUE UNIVERSITY NAME COUNTS")
print("=" * 80)

print(
    f"\nQS unique names: "
    f"{qs['Institution_Name'].dropna().nunique()}"
)

print(
    f"THE unique names: "
    f"{the['Name'].dropna().nunique()}"
)

print(
    f"WUR unique names: "
    f"{wur['Name of University'].dropna().nunique()}"
)

# ------------------------------------------------------------
# Missing university names
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("MISSING UNIVERSITY NAMES")
print("=" * 80)

print(
    f"\nQS missing names: "
    f"{qs['Institution_Name'].isna().sum()}"
)

print(
    f"THE missing names: "
    f"{the['Name'].isna().sum()}"
)

print(
    f"WUR missing names: "
    f"{wur['Name of University'].isna().sum()}"
)

# ------------------------------------------------------------
# Country column inspection
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("COUNTRY COLUMN SAMPLES")
print("=" * 80)

print("\nQS country/location values:")
print(
    qs["Location"]
    .dropna()
    .unique()[:20]
)

print("\nTHE country values:")
print(
    the["Country"]
    .dropna()
    .unique()[:20]
)

print("\nWUR location values:")
print(
    wur["Location"]
    .dropna()
    .unique()[:20]
)

# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("UNIVERSITY NAME INSPECTION COMPLETED")
print("=" * 80)