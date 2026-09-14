import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - ASSIGN UNIVERSITY MASTER IDs
# ============================================================

BASE_DIR = Path("data/processed")

MASTER_FILE = BASE_DIR / "university_master.csv"
QS_FILE = BASE_DIR / "qs_2025_common.csv"
THE24_FILE = BASE_DIR / "the_2024_common.csv"
THE23_FILE = BASE_DIR / "the_2023_common.csv"


# ============================================================
# STEP 1 - LOAD DATA
# ============================================================

print("=" * 70)
print("STEP 1 - LOADING MASTER AND RANKING DATA")
print("=" * 70)

master = pd.read_csv(MASTER_FILE)
qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE24_FILE)
the23 = pd.read_csv(THE23_FILE)

print(f"Master universities: {len(master):,}")
print(f"QS 2025 universities: {len(qs):,}")
print(f"THE 2024 universities: {len(the24):,}")
print(f"THE 2023 universities: {len(the23):,}")


# ============================================================
# STEP 2 - CREATE MASTER LOOKUP
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 - CREATING UNIVERSITY ID LOOKUP")
print("=" * 70)

master_lookup = master[
    [
        "university_id",
        "university_name_clean"
    ]
].copy()

print(f"Master lookup records: {len(master_lookup):,}")


# ============================================================
# STEP 3 - ASSIGN IDs TO QS 2025
# ============================================================

print("\n" + "=" * 70)
print("STEP 3 - ASSIGNING IDs TO QS 2025")
print("=" * 70)

qs = qs.merge(
    master_lookup,
    on="university_name_clean",
    how="left"
)

print(
    "QS records with university_id:",
    qs["university_id"].notna().sum()
)

print(
    "QS records without university_id:",
    qs["university_id"].isna().sum()
)


# ============================================================
# STEP 4 - ASSIGN IDs TO THE 2024
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 - ASSIGNING IDs TO THE 2024")
print("=" * 70)

the24 = the24.merge(
    master_lookup,
    on="university_name_clean",
    how="left"
)

print(
    "THE 2024 records with university_id:",
    the24["university_id"].notna().sum()
)

print(
    "THE 2024 records without university_id:",
    the24["university_id"].isna().sum()
)


# ============================================================
# STEP 5 - ASSIGN IDs TO THE 2023
# ============================================================

print("\n" + "=" * 70)
print("STEP 5 - ASSIGNING IDs TO THE 2023")
print("=" * 70)

the23 = the23.merge(
    master_lookup,
    on="university_name_clean",
    how="left"
)

print(
    "THE 2023 records with university_id:",
    the23["university_id"].notna().sum()
)

print(
    "THE 2023 records without university_id:",
    the23["university_id"].isna().sum()
)


# ============================================================
# STEP 6 - VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 - ID ASSIGNMENT VALIDATION")
print("=" * 70)

datasets = {
    "QS 2025": qs,
    "THE 2024": the24,
    "THE 2023": the23
}

for name, df in datasets.items():

    missing_ids = df["university_id"].isna().sum()
    duplicate_ids = df["university_id"].duplicated().sum()

    print(f"\n{name}")
    print(f"  Total records: {len(df):,}")
    print(f"  Missing university IDs: {missing_ids:,}")
    print(f"  Duplicate university IDs: {duplicate_ids:,}")


# ============================================================
# STEP 7 - SAVE DATASETS
# ============================================================

print("\n" + "=" * 70)
print("STEP 7 - SAVING ID-ASSIGNED DATASETS")
print("=" * 70)

qs_output = BASE_DIR / "qs_2025_with_id.csv"
the24_output = BASE_DIR / "the_2024_with_id.csv"
the23_output = BASE_DIR / "the_2023_with_id.csv"

qs.to_csv(qs_output, index=False)
the24.to_csv(the24_output, index=False)
the23.to_csv(the23_output, index=False)

print(f"Saved: {qs_output}")
print(f"Saved: {the24_output}")
print(f"Saved: {the23_output}")


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("STEP 7 COMPLETED")
print("=" * 70)

print("University IDs assigned using exact standardized names.")
print("No fuzzy matching was used.")