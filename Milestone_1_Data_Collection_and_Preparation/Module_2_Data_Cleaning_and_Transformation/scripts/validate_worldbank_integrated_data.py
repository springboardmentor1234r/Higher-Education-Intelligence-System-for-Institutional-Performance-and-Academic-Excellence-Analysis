import pandas as pd
from pathlib import Path

print("=" * 70)
print("STEP 8F.4 - FINAL WORLD BANK INTEGRATED DATA VALIDATION")
print("=" * 70)

INPUT_FILE = Path("data/processed/university_integrated_worldbank.csv")

if not INPUT_FILE.exists():
    print(f"\nERROR: File not found: {INPUT_FILE}")
    raise SystemExit(1)

df = pd.read_csv(INPUT_FILE)

print(f"\nDataset shape: {df.shape}")

# ================================================================
# 1. BASIC VALIDATION
# ================================================================

print("\n" + "=" * 70)
print("1. BASIC VALIDATION")
print("=" * 70)

print(f"Rows                    : {len(df):,}")
print(f"Columns                 : {len(df.columns):,}")
print(f"Missing university IDs  : {df['university_id'].isna().sum():,}")
print(f"Duplicate university IDs: {df['university_id'].duplicated().sum():,}")
print(f"Missing university names: {df['university_name'].isna().sum():,}")

# ================================================================
# 2. REQUIRED COLUMNS
# ================================================================

print("\n" + "=" * 70)
print("2. REQUIRED WORLD BANK COLUMNS")
print("=" * 70)

required_wb_columns = [
    "worldbank_match_key",
    "wb_country_code",
    "wb_country_name",
    "wb_long_name",
    "wb_2alpha_code",
    "wb_region",
    "wb_income_group",
    "worldbank_linked"
]

missing_columns = [
    col for col in required_wb_columns
    if col not in df.columns
]

if missing_columns:
    print("Missing columns:")
    for col in missing_columns:
        print(f"  ❌ {col}")
else:
    print("All World Bank columns present: ✅")

# ================================================================
# 3. WORLD BANK LINKAGE
# ================================================================

print("\n" + "=" * 70)
print("3. WORLD BANK LINKAGE")
print("=" * 70)

linked = df["worldbank_linked"].fillna(False)

# Handle boolean/string values safely
linked = linked.astype(str).str.lower().isin(
    ["true", "1", "yes"]
)

linked_count = linked.sum()
unlinked_count = len(df) - linked_count

linkage_rate = (
    linked_count / len(df) * 100
    if len(df) > 0 else 0
)

print(f"Linked universities   : {linked_count:,}")
print(f"Unlinked universities : {unlinked_count:,}")
print(f"Linkage rate          : {linkage_rate:.2f}%")

# ================================================================
# 4. UNLINKED COUNTRIES
# ================================================================

print("\n" + "=" * 70)
print("4. UNLINKED UNIVERSITY COUNTRIES")
print("=" * 70)

unlinked_df = df.loc[~linked].copy()

if len(unlinked_df) == 0:
    print("All universities linked to World Bank: ✅")
else:
    print(
        unlinked_df[
            ["country_name_canonical", "worldbank_match_key"]
        ]
        .drop_duplicates()
        .to_string(index=False)
    )

# ================================================================
# 5. DUPLICATE CHECK
# ================================================================

print("\n" + "=" * 70)
print("5. DUPLICATE CHECK")
print("=" * 70)

duplicate_ids = df[df["university_id"].duplicated(keep=False)]

print(f"Duplicate university IDs: {len(duplicate_ids):,}")

if len(duplicate_ids) == 0:
    print("Duplicate check: ✅ PASSED")
else:
    print("Duplicate check: ❌ FAILED")

# ================================================================
# 6. WORLD BANK MISSING VALUES
# ================================================================

print("\n" + "=" * 70)
print("6. WORLD BANK MISSING VALUE SUMMARY")
print("=" * 70)

for col in required_wb_columns:
    if col in df.columns:
        missing = df[col].isna().sum()
        percentage = missing / len(df) * 100

        print(
            f"{col:<25} "
            f"{missing:>6,} missing "
            f"({percentage:>6.2f}%)"
        )

# ================================================================
# 7. WORLD BANK COUNTRY DISTRIBUTION
# ================================================================

print("\n" + "=" * 70)
print("7. WORLD BANK REGION DISTRIBUTION")
print("=" * 70)

if "wb_region" in df.columns:
    print(
        df["wb_region"]
        .value_counts(dropna=False)
        .to_string()
    )

# ================================================================
# 8. WORLD BANK INCOME GROUP
# ================================================================

print("\n" + "=" * 70)
print("8. WORLD BANK INCOME GROUP DISTRIBUTION")
print("=" * 70)

if "wb_income_group" in df.columns:
    print(
        df["wb_income_group"]
        .value_counts(dropna=False)
        .to_string()
    )

# ================================================================
# 9. DATASET PRESENCE
# ================================================================

print("\n" + "=" * 70)
print("9. RANKING DATASET PRESENCE")
print("=" * 70)

for col in ["qs_present", "the24_present", "the23_present"]:
    if col in df.columns:
        count = df[col].fillna(False).astype(bool).sum()
        print(f"{col:<20}: {count:,}")

# ================================================================
# 10. FINAL VALIDATION
# ================================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

checks = {
    "Correct row count": len(df) == 3530,
    "University IDs present": df["university_id"].notna().all(),
    "No duplicate university IDs": df["university_id"].duplicated().sum() == 0,
    "World Bank columns present": len(missing_columns) == 0,
    "World Bank linkage >= 95%": linkage_rate >= 95
}

all_passed = True

for check, result in checks.items():
    status = "PASS" if result else "FAIL"

    print(f"{check:<35}: {status}")

    if not result:
        all_passed = False

print("\n" + "=" * 70)

if all_passed:
    print("STEP 8F.4 PASSED ✅")
    print("Final World Bank integrated dataset is structurally valid.")
else:
    print("STEP 8F.4 FAILED ❌")
    print("Review the failed checks above.")

print("=" * 70)