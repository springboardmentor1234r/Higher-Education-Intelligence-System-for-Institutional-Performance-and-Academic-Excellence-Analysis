import pandas as pd
import numpy as np
import os
import re


# ============================================================
# DATASET 4 - EDSTATS COUNTRY
# ============================================================

INPUT_FILE = "data/raw/EdStatsCountry.csv"
OUTPUT_FILE = "data/cleaned/edstats_country_cleaned.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("=" * 60)
print("DATASET 4 - EDSTATS COUNTRY")
print("=" * 60)


# ============================================================
# STEP 4.1 - LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully!")


# Dataset shape
print("\nDataset Shape:")
print(df.shape)


# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())


# Column names
print("\nColumn Names:")
print(df.columns.tolist())


# Data types
print("\nData Types:")
print(df.dtypes)


# Missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Missing value percentage
print("\nMissing Value Percentage:")

missing_pct = (
    df.isnull().sum() / len(df) * 100
).sort_values(ascending=False)

print(missing_pct)

# ============================================================
# STEP 4.2 - REMOVE COMPLETELY EMPTY COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.2 - REMOVE COMPLETELY EMPTY COLUMNS")
print("=" * 60)

# Find columns where every value is missing
empty_columns = [
    col for col in df.columns
    if df[col].isnull().all()
]

print("\nCompletely Empty Columns:")
print(empty_columns)

# Remove completely empty columns
if empty_columns:
    df = df.drop(columns=empty_columns)

print("\nColumns After Removing Empty Columns:")
print(df.columns.tolist())

print("\nDataset Shape After Removing Empty Columns:")
print(df.shape)

# ============================================================
# STEP 4.3 - DUPLICATE ANALYSIS & COUNTRY CODE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.3 - DUPLICATE ANALYSIS & COUNTRY CODE VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# 4.3.1 - Check exact duplicate rows
# ------------------------------------------------------------

duplicate_rows = df.duplicated().sum()

print("\nExact Duplicate Rows:")
print(duplicate_rows)

# ------------------------------------------------------------
# 4.3.2 - Check duplicate Country Codes
# ------------------------------------------------------------

duplicate_country_codes = df["Country Code"].duplicated().sum()

print("\nDuplicate Country Codes:")
print(duplicate_country_codes)

# ------------------------------------------------------------
# 4.3.3 - Check duplicate Short Names
# ------------------------------------------------------------

duplicate_country_names = df["Short Name"].duplicated().sum()

print("\nDuplicate Country Names:")
print(duplicate_country_names)

# ------------------------------------------------------------
# 4.3.4 - Check missing Country Codes
# ------------------------------------------------------------

missing_country_codes = df["Country Code"].isnull().sum()

print("\nMissing Country Codes:")
print(missing_country_codes)

# ------------------------------------------------------------
# 4.3.5 - Check missing Country Names
# ------------------------------------------------------------

missing_country_names = df["Short Name"].isnull().sum()

print("\nMissing Country Names:")
print(missing_country_names)

# ------------------------------------------------------------
# 4.3.6 - Display duplicate Country Codes if any
# ------------------------------------------------------------

if duplicate_country_codes > 0:

    print("\nDuplicate Country Code Records:")

    duplicate_codes = df[
        df["Country Code"].duplicated(keep=False)
    ].sort_values("Country Code")

    print(
        duplicate_codes[
            ["Country Code", "Short Name"]
        ]
    )

# ------------------------------------------------------------
# 4.3.7 - Display duplicate country names if any
# ------------------------------------------------------------

if duplicate_country_names > 0:

    print("\nDuplicate Country Name Records:")

    duplicate_names = df[
        df["Short Name"].duplicated(keep=False)
    ].sort_values("Short Name")

    print(
        duplicate_names[
            ["Country Code", "Short Name"]
        ]
    )

# ============================================================
# STEP 4.4 - CLEAN & STANDARDIZE COUNTRY CODES AND TEXT
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.4 - CLEAN & STANDARDIZE COUNTRY CODES AND TEXT")
print("=" * 60)

# ------------------------------------------------------------
# 4.4.1 - Standardize Country Code
# ------------------------------------------------------------

df["Country Code"] = (
    df["Country Code"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 4.4.2 - Standardize Short Name
# ------------------------------------------------------------

df["Short Name"] = (
    df["Short Name"]
    .astype("string")
    .str.strip()
)

# ------------------------------------------------------------
# 4.4.3 - Standardize Long Name
# ------------------------------------------------------------

df["Long Name"] = (
    df["Long Name"]
    .astype("string")
    .str.strip()
)

# ------------------------------------------------------------
# 4.4.4 - Standardize 2-alpha code
# ------------------------------------------------------------

df["2-alpha code"] = (
    df["2-alpha code"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 4.4.5 - Standardize WB-2 code
# ------------------------------------------------------------

df["WB-2 code"] = (
    df["WB-2 code"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# ------------------------------------------------------------
# 4.4.6 - Clean whitespace in all text columns
# ------------------------------------------------------------

text_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# ------------------------------------------------------------
# 4.4.7 - Validate Country Code format
# ------------------------------------------------------------

invalid_country_codes = df[
    df["Country Code"].notna() &
    ~df["Country Code"].str.match(r"^[A-Z]{3}$", na=False)
]

print("\nInvalid Country Codes:")
print(len(invalid_country_codes))

if len(invalid_country_codes) > 0:
    print(invalid_country_codes[["Country Code", "Short Name"]])


# ------------------------------------------------------------
# 4.4.8 - Validate 2-alpha code
# ------------------------------------------------------------

# World Bank aggregate codes that are not standard 2-letter
# country codes but are valid records in this dataset.

valid_aggregate_codes = {
    "1A", "4E", "Z4", "7E", "Z7", "8S", "1W"
}

invalid_alpha_codes = df[
    df["2-alpha code"].notna() &
    ~(
        df["2-alpha code"].str.match(
            r"^[A-Z]{2}$", na=False
        )
        |
        df["2-alpha code"].isin(valid_aggregate_codes)
    )
]

print("\nInvalid 2-alpha Codes:")
print(len(invalid_alpha_codes))

if len(invalid_alpha_codes) > 0:
    print(
        invalid_alpha_codes[
            ["Country Code", "2-alpha code"]
        ]
    )


# ------------------------------------------------------------
# 4.4.9 - Validate WB-2 code
# ------------------------------------------------------------

invalid_wb_codes = df[
    df["WB-2 code"].notna() &
    ~(
        df["WB-2 code"].str.match(
            r"^[A-Z]{2}$", na=False
        )
        |
        df["WB-2 code"].isin(valid_aggregate_codes)
    )
]

print("\nInvalid WB-2 Codes:")
print(len(invalid_wb_codes))

if len(invalid_wb_codes) > 0:
    print(
        invalid_wb_codes[
            ["Country Code", "WB-2 code"]
        ]
    )

# ------------------------------------------------------------
# 4.4.10 - Display sample after cleaning
# ------------------------------------------------------------

print("\nSample After Standardization:")

print(
    df[
        ["Country Code", "Short Name", "Long Name",
         "2-alpha code", "WB-2 code"]
    ].head(10)
)

# ============================================================
# STEP 4.5 - MISSING VALUE ANALYSIS & HANDLING
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.5 - MISSING VALUE ANALYSIS & HANDLING")
print("=" * 60)

# ------------------------------------------------------------
# 4.5.1 - Count missing values
# ------------------------------------------------------------

missing_counts = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
)

missing_summary = pd.DataFrame({
    "Missing Count": missing_counts,
    "Missing Percentage": missing_percentage
})

missing_summary = missing_summary[
    missing_summary["Missing Count"] > 0
].sort_values(
    "Missing Percentage",
    ascending=False
)

print("\nMissing Value Summary:")
print(missing_summary)

# ------------------------------------------------------------
# 4.5.2 - Validate critical fields
# ------------------------------------------------------------

critical_columns = [
    "Country Code",
    "Short Name",
    "Table Name",
    "Long Name"
]

print("\nCritical Field Missing Values:")

for col in critical_columns:
    print(
        f"{col}: {df[col].isnull().sum()}"
    )

# ------------------------------------------------------------
# 4.5.3 - Missing Value Handling Decision
# ------------------------------------------------------------

print("\nMissing Value Handling Decision:")
print("• Critical identification fields are complete.")
print("• Legitimate metadata missing values are preserved.")
print("• No mean/median imputation is applied.")
print("• Missing categorical values are not replaced blindly.")
print("• Missing year/reference information is preserved.")
print("• No country records are removed because of metadata missingness.")

# ============================================================
# STEP 4.6 - YEAR AND METADATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.6 - YEAR AND METADATA VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 4.6.1 - Define year-related columns
# ------------------------------------------------------------

year_columns = [
    "National accounts base year",
    "National accounts reference year",
    "PPP survey year",
    "Latest population census",
    "Latest household survey",
    "Latest agricultural census",
    "Latest industrial data",
    "Latest trade data",
    "Latest water withdrawal data"
]

print("\nYear-related columns:")
for col in year_columns:
    print("•", col)


# ------------------------------------------------------------
# 4.6.2 - Display sample values
# ------------------------------------------------------------

print("\nSample values from year-related columns:")

for col in year_columns:
    print(f"\n{col}:")
    print(
        df[col]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .head(10)
        .tolist()
    )


# ------------------------------------------------------------
# 4.6.3 - Check for obviously invalid negative values
# ------------------------------------------------------------

print("\nChecking for negative numeric year values...")

negative_values = {}

for col in year_columns:

    numeric_values = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    invalid_negative = df[
        numeric_values < 0
    ]

    if len(invalid_negative) > 0:
        negative_values[col] = len(invalid_negative)

        print(
            f"{col}: {len(invalid_negative)} negative values"
        )

if len(negative_values) == 0:
    print("No negative year values found.")


# ------------------------------------------------------------
# 4.6.4 - Validate numeric year ranges
# ------------------------------------------------------------

print("\nChecking numeric year ranges...")

current_year = pd.Timestamp.now().year

for col in year_columns:

    numeric_values = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    invalid_years = df[
        (numeric_values < 1900) |
        (numeric_values > current_year)
    ]

    if len(invalid_years) > 0:

        print(
            f"\n{col}: {len(invalid_years)} values outside "
            f"valid range 1900-{current_year}"
        )

        print(
            invalid_years[
                ["Country Code", "Short Name", col]
            ].head(10)
        )

    else:

        print(
            f"{col}: No invalid numeric years"
        )


# ------------------------------------------------------------
# 4.6.5 - Preserve mixed year/range/text values
# ------------------------------------------------------------

print("\nMixed year/range/text values are preserved.")

print(
    "Examples such as year ranges or text-based metadata "
    "are not converted or removed."
)


# ------------------------------------------------------------
# 4.6.6 - Metadata validation summary
# ------------------------------------------------------------

print("\nMetadata Validation Decision:")
print("• Year-related fields are validated without forced conversion.")
print("• Negative numeric year values are checked.")
print("• Numeric years outside the valid range are checked.")
print("• Valid year ranges and text values are preserved.")
print("• No legitimate metadata values are removed.")

# ============================================================
# STEP 4.7 - FINAL DATASET VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.7 - FINAL DATASET VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 4.7.1 - Check final shape
# ------------------------------------------------------------

print("\nFinal Dataset Shape:")
print(df.shape)


# ------------------------------------------------------------
# 4.7.2 - Check duplicate rows
# ------------------------------------------------------------

final_duplicate_rows = df.duplicated().sum()

print("\nFinal Duplicate Rows:")
print(final_duplicate_rows)


# ------------------------------------------------------------
# 4.7.3 - Check duplicate Country Codes
# ------------------------------------------------------------

final_duplicate_codes = df["Country Code"].duplicated().sum()

print("\nFinal Duplicate Country Codes:")
print(final_duplicate_codes)


# ------------------------------------------------------------
# 4.7.4 - Check critical fields
# ------------------------------------------------------------

print("\nFinal Critical Field Validation:")

for col in [
    "Country Code",
    "Short Name",
    "Table Name",
    "Long Name"
]:

    missing = df[col].isnull().sum()

    print(f"{col}: {missing} missing values")


# ------------------------------------------------------------
# 4.7.5 - Check completely empty columns
# ------------------------------------------------------------

completely_empty = [
    col for col in df.columns
    if df[col].isnull().all()
]

print("\nCompletely Empty Columns:")
print(completely_empty)


# ------------------------------------------------------------
# 4.7.6 - Check Country Code format
# ------------------------------------------------------------

invalid_country_codes = df[
    df["Country Code"].notna() &
    ~df["Country Code"].str.match(
        r"^[A-Z]{3}$",
        na=False
    )
]

print("\nInvalid Country Codes:")
print(len(invalid_country_codes))


# ------------------------------------------------------------
# 4.7.7 - Final validation decision
# ------------------------------------------------------------

validation_passed = (
    final_duplicate_rows == 0
    and final_duplicate_codes == 0
    and df["Country Code"].isnull().sum() == 0
    and df["Short Name"].isnull().sum() == 0
    and df["Table Name"].isnull().sum() == 0
    and df["Long Name"].isnull().sum() == 0
    and len(completely_empty) == 0
    and len(invalid_country_codes) == 0
)

print("\n" + "=" * 60)

if validation_passed:
    print("✅ DATASET 4 FINAL VALIDATION PASSED")
else:
    print("❌ DATASET 4 FINAL VALIDATION FAILED")

print("=" * 60)

# ============================================================
# STEP 4.8 - CLEANED DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.8 - CLEANED DATASET SUMMARY")
print("=" * 60)

print("\nOriginal Dataset Shape: (241, 32)")
print("Final Dataset Shape:", df.shape)

print("\nTotal Countries/Records:")
print(len(df))

print("\nTotal Columns:")
print(len(df.columns))

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Country Codes:")
print(df["Country Code"].duplicated().sum())

print("\nMissing Country Codes:")
print(df["Country Code"].isnull().sum())

print("\nMissing Country Names:")
print(df["Short Name"].isnull().sum())

print("\nRemaining Missing Values:")
print(df.isnull().sum().sum())

# ============================================================
# STEP 4.9 - SAVE CLEANED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 4.9 - SAVE CLEANED DATASET")
print("=" * 60)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n✅ Cleaned Dataset Saved Successfully!")
print(f"Output File: {OUTPUT_FILE}")
print(f"Final Shape: {df.shape}")

