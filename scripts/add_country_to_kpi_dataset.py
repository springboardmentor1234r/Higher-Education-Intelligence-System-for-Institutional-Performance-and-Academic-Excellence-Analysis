"""
Add standardized country information to the EduVision KPI dataset.

This script:
1. Loads the current final KPI dataset and preserves a copy for equivalence testing.
2. Creates a backup of the existing KPI CSV before modifying anything.
3. Loads the cleaned QS, THE, and WUR datasets.
4. Uses Match_Key to look up Country_Standard (QS primary -> THE fallback -> WUR fallback).
5. Adds Country_Standard to the KPI dataset without changing any existing column or value.
6. Rigorously validates:
   - Row count is exactly 822.
   - Zero duplicate University_IDs.
   - Zero missing Country_Standard values.
   - Complete cell-by-cell equality on all original 55 columns and all 6 KPI fields.
7. Saves the updated dataset to data/final/university_kpi_dataset.csv.
"""

from pathlib import Path
import shutil
import pandas as pd
from pandas.testing import assert_frame_equal


# ---------------------------------------------------------
# STEP 1: Define project paths
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

FINAL_FILE = ROOT / "data" / "final" / "university_kpi_dataset.csv"
QS_FILE = ROOT / "data" / "cleaned" / "qs_2025_alias_applied.csv"
THE_FILE = ROOT / "data" / "cleaned" / "the_2024_standardized.csv"
WUR_FILE = ROOT / "data" / "cleaned" / "wur_2023_standardized.csv"

BACKUP_FILE = ROOT / "data" / "final" / "university_kpi_dataset_before_country_backup.csv"


# ---------------------------------------------------------
# STEP 2: Load the final KPI dataset and preserve original
# ---------------------------------------------------------

print("=" * 80)
print("LOADING KPI DATASET")
print("=" * 80)

if not FINAL_FILE.exists():
    raise FileNotFoundError(f"Could not find: {FINAL_FILE}")

kpi_original = pd.read_csv(FINAL_FILE)
print(f"Original KPI Dataset: {kpi_original.shape[0]} rows, {kpi_original.shape[1]} columns")

if "Country_Standard" in kpi_original.columns:
    base_columns = [c for c in kpi_original.columns if c != "Country_Standard"]
    kpi_base = kpi_original[base_columns].copy()
else:
    base_columns = list(kpi_original.columns)
    kpi_base = kpi_original.copy()

print(f"Base columns count: {len(base_columns)}")


# ---------------------------------------------------------
# STEP 3: Create backup before modifying anything
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("CREATING BACKUP")
print("=" * 80)

shutil.copy2(FINAL_FILE, BACKUP_FILE)
print(f"Backup created successfully at: {BACKUP_FILE}")


# ---------------------------------------------------------
# STEP 4: Helper function for Match_Key (matching build_university_master.py)
# ---------------------------------------------------------

def create_key(series):
    """Normalized alphanumeric university matching key matching the pipeline."""
    return (
        series
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r"[^a-z0-9]", "", regex=True)
    )


# ---------------------------------------------------------
# STEP 5: Load source datasets and build country lookups
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("LOADING SOURCE DATASETS & EXTRACTING COUNTRY")
print("=" * 80)

qs = pd.read_csv(QS_FILE)
the = pd.read_csv(THE_FILE)
wur = pd.read_csv(WUR_FILE)

qs["Match_Key"] = create_key(qs["University_Name_Standard"])
the["Match_Key"] = create_key(the["University_Name_Standard"])
wur["Match_Key"] = create_key(wur["University_Name_Standard"])

def prepare_country_lookup(df, source_name):
    country_column = None
    for candidate in ["Country_Standard", "Country", "Location"]:
        if candidate in df.columns:
            country_column = candidate
            break
    if country_column is None:
        raise ValueError(f"{source_name} does not contain Country_Standard, Country, or Location.")

    lookup = df[["Match_Key", country_column]].copy()
    lookup = lookup.rename(columns={country_column: "Country_Standard"})
    lookup["Country_Standard"] = lookup["Country_Standard"].fillna("").astype(str).str.strip()
    lookup = lookup[lookup["Country_Standard"] != ""]
    lookup = lookup.drop_duplicates(subset=["Match_Key"], keep="first")
    return lookup

qs_country = prepare_country_lookup(qs, "QS")
the_country = prepare_country_lookup(the, "THE")
wur_country = prepare_country_lookup(wur, "WUR")

print(f"QS country records: {len(qs_country)}")
print(f"THE country records: {len(the_country)}")
print(f"WUR country records: {len(wur_country)}")


# ---------------------------------------------------------
# STEP 6: Merge Country_Standard with strict priority
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("MERGING COUNTRY INFORMATION (QS -> THE -> WUR)")
print("=" * 80)

kpi = kpi_base.copy()
kpi["Match_Key"] = kpi["Match_Key"].fillna("").astype(str)

kpi = kpi.merge(
    qs_country.rename(columns={"Country_Standard": "Country_QS"}),
    on="Match_Key",
    how="left",
)

kpi = kpi.merge(
    the_country.rename(columns={"Country_Standard": "Country_THE"}),
    on="Match_Key",
    how="left",
)

kpi = kpi.merge(
    wur_country.rename(columns={"Country_Standard": "Country_WUR"}),
    on="Match_Key",
    how="left",
)

# Source priority: QS -> THE -> WUR
kpi["Country_Standard"] = (
    kpi["Country_QS"]
    .replace("", pd.NA)
    .fillna(kpi["Country_THE"].replace("", pd.NA))
    .fillna(kpi["Country_WUR"].replace("", pd.NA))
)

# Drop helper merge columns
kpi = kpi.drop(columns=["Country_QS", "Country_THE", "Country_WUR"])


# ---------------------------------------------------------
# STEP 7: Comprehensive Validation Checks
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("DATASET INTEGRITY & EQUIVALENCE VALIDATION")
print("=" * 80)

# Check 1: Row count
assert len(kpi) == 822, f"Expected 822 rows, got {len(kpi)}"
print(f"[PASS] Row count: {len(kpi)} == 822")

# Check 2: Duplicate University_IDs
dup_ids = kpi["University_ID"].duplicated().sum()
assert dup_ids == 0, f"Found {dup_ids} duplicate University_IDs"
print(f"[PASS] Duplicate University_IDs: {dup_ids}")

# Check 3: Missing countries
missing_countries = kpi["Country_Standard"].isna().sum()
if missing_countries > 0:
    print(f"\n[FAIL] Found {missing_countries} universities missing country:")
    print(kpi[kpi["Country_Standard"].isna()][["University_ID", "University_Name", "Match_Key"]].to_string())
    raise ValueError("Country coverage is incomplete. Aborting.")
else:
    print(f"[PASS] Missing Country_Standard count: {missing_countries}")

# Check 4: Unique countries
unique_countries = kpi["Country_Standard"].nunique()
print(f"[PASS] Unique countries count: {unique_countries}")

# Check 5: Cell-by-cell equivalence on original 55 columns
print("\nVerifying cell-by-cell equivalence for all original 55 columns...")
assert_frame_equal(kpi_base[base_columns], kpi[base_columns], check_dtype=True)
print("[PASS] All original 55 columns are cell-by-cell and dtype identical!")

# Check 6: Check all 6 KPI columns explicitly
kpis = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

for kpi_col in kpis:
    assert (kpi_base[kpi_col].fillna(-999) == kpi[kpi_col].fillna(-999)).all(), f"Mismatch in KPI {kpi_col}"
    print(f"[PASS] KPI '{kpi_col}' verified 100% identical.")


# ---------------------------------------------------------
# STEP 8: Save validated dataset
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("SAVING FINAL DATASET")
print("=" * 80)

kpi.to_csv(FINAL_FILE, index=False)
print(f"Updated KPI dataset successfully written to: {FINAL_FILE}")
print(f"Final shape: {kpi.shape} (822 universities, {len(kpi.columns)} columns)")
print(f"Added column: Country_Standard")
