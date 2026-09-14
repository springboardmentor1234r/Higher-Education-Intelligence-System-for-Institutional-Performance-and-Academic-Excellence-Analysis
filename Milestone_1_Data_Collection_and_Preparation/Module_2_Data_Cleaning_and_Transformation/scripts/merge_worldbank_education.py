import pandas as pd
from pathlib import Path

print("=" * 70)
print("STEP 8F.6 - MERGE WORLD BANK EDUCATION INDICATORS")
print("=" * 70)

# ------------------------------------------------------------
# FILE PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

UNIVERSITY_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank.csv"
)

EDUCATION_FILE = (
    BASE_DIR / "data" / "processed" /
    "worldbank_education_2015.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank_education.csv"
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading university dataset...")

university_df = pd.read_csv(UNIVERSITY_FILE)

print("University dataset shape:", university_df.shape)

print("\nLoading World Bank education data...")

education_df = pd.read_csv(EDUCATION_FILE)

print("Education dataset shape:", education_df.shape)

# ------------------------------------------------------------
# VALIDATE EDUCATION COUNTRY CODES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATING WORLD BANK EDUCATION DATA")
print("=" * 70)

duplicate_codes = education_df["Country Code"].duplicated().sum()

print("Duplicate World Bank country codes:", duplicate_codes)

if duplicate_codes > 0:
    print("\nERROR: Duplicate country codes found.")
    print(
        education_df[
            education_df["Country Code"].duplicated(keep=False)
        ].sort_values("Country Code")
    )
    raise ValueError("Duplicate country codes detected.")

# ------------------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------------------

education_columns = [
    "Country Code",
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015",
]

missing_columns = [
    col for col in education_columns
    if col not in education_df.columns
]

if missing_columns:
    print("\nERROR: Missing required columns:")
    for col in missing_columns:
        print(" -", col)
    raise ValueError("Required World Bank education columns missing.")

# ------------------------------------------------------------
# SELECT REQUIRED COLUMNS
# ------------------------------------------------------------

education_df = education_df[education_columns].copy()

# ------------------------------------------------------------
# MERGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MERGING DATA")
print("=" * 70)

before_rows = len(university_df)

merged_df = university_df.merge(
    education_df,
    how="left",
    left_on="wb_country_code",
    right_on="Country Code",
    validate="many_to_one"
)

# Remove duplicate merge key
merged_df.drop(columns=["Country Code"], inplace=True)

after_rows = len(merged_df)

print("Rows before merge:", before_rows)
print("Rows after merge :", after_rows)

# ------------------------------------------------------------
# ROW COUNT VALIDATION
# ------------------------------------------------------------

if before_rows != after_rows:
    raise ValueError(
        "ERROR: Row count changed after merge!"
    )

print("Row count preserved: PASS")

# ------------------------------------------------------------
# EDUCATION LINKAGE
# ------------------------------------------------------------

education_indicators = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015",
]

# A country is considered education-linked if at least
# one of the six indicators is available.
merged_df["worldbank_education_2015_linked"] = (
    merged_df[education_indicators]
    .notna()
    .any(axis=1)
)

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATING MERGED DATA")
print("=" * 70)

print("Final shape:", merged_df.shape)

print(
    "Universities with at least one education indicator:",
    merged_df["worldbank_education_2015_linked"].sum()
)

print(
    "Universities without education indicators:",
    (~merged_df["worldbank_education_2015_linked"]).sum()
)

print("\nMissing values by education indicator:")

for col in education_indicators:
    available = merged_df[col].notna().sum()
    missing = merged_df[col].isna().sum()

    print(
        f"{col:<50}"
        f"Available: {available:4d} "
        f"Missing: {missing:4d}"
    )

# ------------------------------------------------------------
# CHECK UNIVERSITY IDS
# ------------------------------------------------------------

missing_ids = merged_df["university_id"].isna().sum()
duplicate_ids = merged_df["university_id"].duplicated().sum()

print("\nUniversity ID validation:")
print("Missing university IDs:", missing_ids)
print("Duplicate university IDs:", duplicate_ids)

if missing_ids != 0:
    raise ValueError("Missing university IDs detected.")

if duplicate_ids != 0:
    raise ValueError("Duplicate university IDs detected.")

# ------------------------------------------------------------
# CHECK UNLINKED COUNTRIES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EDUCATION LINKAGE BY COUNTRY")
print("=" * 70)

country_linkage = (
    merged_df
    .groupby("country_name", dropna=False)
    ["worldbank_education_2015_linked"]
    .agg(["count", "sum"])
    .reset_index()
)

country_linkage.columns = [
    "country_name",
    "universities",
    "education_linked"
]

country_linkage["linkage_rate"] = (
    country_linkage["education_linked"]
    / country_linkage["universities"]
    * 100
)

print(
    country_linkage
    .sort_values("linkage_rate")
    .head(20)
    .to_string(index=False)
)

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

merged_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("STEP 8F.6 COMPLETED")
print("=" * 70)

print("\nSaved file:")
print(OUTPUT_FILE)

print("\nFinal shape:", merged_df.shape)

print("\nFinal columns:")
for i, col in enumerate(merged_df.columns, start=1):
    print(f"{i:2d}. {col}")

print("\n" + "=" * 70)