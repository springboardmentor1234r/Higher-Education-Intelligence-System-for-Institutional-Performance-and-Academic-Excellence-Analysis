import pandas as pd

# ============================================================
# STEP 2.2 - LOAD DATASET
# ============================================================

file_path = "data/raw/QS World University Rankings 2025 (Top global universities).csv"

df = pd.read_csv(file_path, encoding="latin1")

print("Dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


# ============================================================
# STEP 2.3 - INSPECT DATASET
# ============================================================

print("\nMissing Values:")
print(df.isnull().sum())

print("\nMissing Value Percentage:")
print(
    (df.isnull().mean() * 100)
    .sort_values(ascending=False)
)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Universities:")
print(df["Institution_Name"].duplicated().sum())


# ============================================================
# STEP 2.4 - STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace(".", "", regex=False)
)

print("\nStandardized Column Names:")
print(df.columns.tolist())


# ============================================================
# STEP 2.5 - CLEAN UNIVERSITY NAMES
# ============================================================

print("\nUniversity Names Before Cleaning:")
print(df["institution_name"].head(20).to_string())

# Remove leading and trailing spaces
df["institution_name"] = (
    df["institution_name"]
    .astype("string")
    .str.strip()
)

# Convert names to lowercase
df["institution_name"] = (
    df["institution_name"]
    .str.lower()
)

# Normalize multiple spaces
df["institution_name"] = (
    df["institution_name"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print("\nUniversity Names After Cleaning:")
print(df["institution_name"].head(20).to_string())

# Check missing university names
print("\nMissing University Names:")
print(df["institution_name"].isna().sum())

# Check duplicate university names after cleaning
print("\nDuplicate Universities After Cleaning:")
print(df["institution_name"].duplicated().sum())

# ============================================================
# STEP 2.6 - INSPECT COUNTRY NAMES
# ============================================================

print("\nUnique Country Values:")
print(df["location"].unique())

print("\nNumber of Unique Countries:")
print(df["location"].nunique())

print("\nCountry Value Counts:")
print(df["location"].value_counts().head(30))

# ============================================================
# STEP 2.6 - CREATE STANDARDIZED COUNTRY CODE
# ============================================================

country_mapping = {
    "United States": "US",
    "United Kingdom": "GB",
    "Switzerland": "CH",
    "Singapore": "SG",
    "Australia": "AU",
    "China (Mainland)": "CN",
    "Hong Kong SAR": "HK",
    "France": "FR",
    "Canada": "CA",
    "Germany": "DE",
    "Japan": "JP",
    "Russia": "RU",
    "India": "IN",
    "South Korea": "KR",
    "Italy": "IT",
    "Brazil": "BR",
    "Spain": "ES",
    "Mexico": "MX",
    "Malaysia": "MY",
    "Taiwan": "TW",
    "Indonesia": "ID",
    "Argentina": "AR",
    "Chile": "CL",
    "Turkey": "TR",
    "Colombia": "CO",
    "Poland": "PL",
    "Kazakhstan": "KZ",
    "Saudi Arabia": "SA",
    "Czech Republic": "CZ",
    "Egypt": "EG",
    "Bangladesh": "BD",
    "Pakistan": "PK",
    "Netherlands": "NL",

    "Armenia": "AM",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahrain": "BH",
    "Belarus": "BY",
    "Belgium": "BE",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Denmark": "DK",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Finland": "FI",
    "Georgia": "GE",
    "Ghana": "GH",
    "Greece": "GR",
    "Guatemala": "GT",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "Iran, Islamic Republic of": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Jordan": "JO",
    "Kenya": "KE",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Macau SAR": "MO",
    "Malta": "MT",
    "Morocco": "MA",
    "New Zealand": "NZ",
    "Nigeria": "NG",
    "Northern Cyprus": "XC",
    "Norway": "NO",
    "Oman": "OM",
    "Palestinian Territory, Occupied": "PS",
    "Panama": "PA",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Qatar": "QA",
    "Romania": "RO",
    "Serbia": "RS",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "South Africa": "ZA",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Sweden": "SE",
    "Syrian Arab Republic": "SY",
    "Thailand": "TH",
    "Tunisia": "TN",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Venezuela": "VE",
    "Vietnam": "VN"
}
df["country_code"] = df["location"].map(country_mapping)

print("\nCountry Code Sample:")
print(
    df[["location", "country_code"]]
    .drop_duplicates()
    .sort_values("location")
    .to_string(index=False)
)

print("\nNumber of Unique QS Countries:")
print(df["location"].nunique())

print("\nNumber of Unique Country Codes:")
print(df["country_code"].nunique())

print("\nCountries Without Mapping:")
unmapped = (
    df.loc[df["country_code"].isna(), "location"]
    .drop_duplicates()
    .sort_values()
)

if len(unmapped) == 0:
    print("None - all countries are mapped successfully!")
else:
    print(unmapped.to_string(index=False))

# ============================================================
# STEP 2.7 - MISSING VALUE ANALYSIS
# ============================================================

print("\nMissing Value Analysis:")

missing_summary = pd.DataFrame({
    "missing_count": df.isnull().sum(),
    "missing_percentage": (df.isnull().mean() * 100).round(2)
})

missing_summary = (
    missing_summary[missing_summary["missing_count"] > 0]
    .sort_values("missing_percentage", ascending=False)
)

print(missing_summary)

# ============================================================
# STEP 2.7 - HANDLE MISSING VALUES
# ============================================================

# Categorical field:
# Missing status means the status is unavailable.
df["status"] = df["status"].fillna("Unknown")

# Numeric and ranking fields:
# Keep missing values as NaN.
# Do NOT replace them with 0.

print("\nMissing Values After Handling:")

missing_after = pd.DataFrame({
    "missing_count": df.isnull().sum(),
    "missing_percentage": (df.isnull().mean() * 100).round(2)
})

missing_after = (
    missing_after[missing_after["missing_count"] > 0]
    .sort_values("missing_percentage", ascending=False)
)

print(missing_after)

print("\nMissing Status Values:")
print(df["status"].isnull().sum())

print("\nStatus Value Counts:")
print(df["status"].value_counts(dropna=False))

# ============================================================
# STEP 2.8 - CONVERT DATA TYPES
# ============================================================

print("\nData Type Conversion:")

# ------------------------------------------------------------
# 1. Rank columns
# ------------------------------------------------------------

rank_columns = [
    "rank_2025",
    "rank_2024",
    "academic_reputation_rank",
    "employer_reputation_rank",
    "faculty_student_rank",
    "citations_per_faculty_rank",
    "international_faculty_rank",
    "international_students_rank",
    "international_research_network_rank",
    "employment_outcomes_rank",
    "sustainability_rank"
]

for column in rank_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.replace("=", "", regex=False)
        .str.strip()
    )

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 2. Score columns
# ------------------------------------------------------------

score_columns = [
    "academic_reputation_score",
    "employer_reputation_score",
    "faculty_student_score",
    "citations_per_faculty_score",
    "international_faculty_score",
    "international_students_score",
    "international_research_network_score",
    "employment_outcomes_score",
    "sustainability_score",
    "overall_score"
]

for column in score_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 3. Display new data types
# ------------------------------------------------------------

print("\nData Types After Conversion:")

print(df.dtypes)

# ============================================================
# STEP 2.9 - FINAL DUPLICATE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.9 - DUPLICATE VALIDATION")
print("=" * 60)

# 1. Check complete duplicate rows
duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows After Cleaning:")
print(duplicate_rows)


# 2. Check duplicate university names
duplicate_universities = df["institution_name"].duplicated().sum()

print("\nDuplicate University Names After Cleaning:")
print(duplicate_universities)


# 3. Display duplicate university names if any exist
if duplicate_universities > 0:

    print("\nDuplicate University Names:")

    duplicates = df[
        df["institution_name"].duplicated(keep=False)
    ].sort_values("institution_name")

    print(
        duplicates[
            ["institution_name", "location", "rank_2025"]
        ].to_string(index=False)
    )

else:

    print("\nNo duplicate university names found.")

# ============================================================
# STEP 2.10 - CREATE UNIVERSITY MASTER ID
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.10 - UNIVERSITY MASTER ID")
print("=" * 60)

# Create a unique ID for every university
df["university_id"] = [
    f"U{i:04d}" for i in range(1, len(df) + 1)
]

print("\nUniversity ID Created Successfully!")

print("\nSample University Master Data:")

print(
    df[
        [
            "university_id",
            "institution_name",
            "country_code"
        ]
    ].head(20).to_string(index=False)
)

# Check whether IDs are unique
print("\nTotal University IDs:")
print(df["university_id"].nunique())

print("\nTotal Dataset Rows:")
print(len(df))

# Validate uniqueness
if df["university_id"].nunique() == len(df):
    print("\nUniversity ID Validation: PASSED")
else:
    print("\nUniversity ID Validation: FAILED")

# ============================================================
# STEP 2.11 - CREATE COUNTRY MASTER TABLE
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.11 - COUNTRY MASTER ID")
print("=" * 60)

# Create unique country master table
country_master = (
    df[["country_code", "location"]]
    .drop_duplicates()
    .sort_values("country_code")
    .reset_index(drop=True)
)

# Create Country Master ID
country_master["country_id"] = [
    f"C{i:03d}" for i in range(1, len(country_master) + 1)
]

# Rename country name column
country_master = country_master.rename(
    columns={
        "location": "country_name"
    }
)

# Reorder columns
country_master = country_master[
    [
        "country_id",
        "country_code",
        "country_name"
    ]
]

print("\nCountry Master Created Successfully!")

print("\nCountry Master Sample:")
print(country_master.head(20).to_string(index=False))

print("\nTotal Countries:")
print(len(country_master))

print("\nUnique Country Codes:")
print(country_master["country_code"].nunique())

# Validate
if (
    country_master["country_id"].nunique()
    == len(country_master)
    and
    country_master["country_code"].nunique()
    == len(country_master)
):
    print("\nCountry Master Validation: PASSED")
else:
    print("\nCountry Master Validation: FAILED")

# ============================================================
# STEP 2.12 - VALIDATE UNIVERSITY → COUNTRY RELATIONSHIP
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.12 - UNIVERSITY → COUNTRY VALIDATION")
print("=" * 60)

# Check universities with missing country codes
missing_country_codes = df["country_code"].isna().sum()

print("\nUniversities with Missing Country Code:")
print(missing_country_codes)


# Check whether every country code exists in Country Master
valid_country_codes = set(country_master["country_code"])

invalid_country_codes = df[
    ~df["country_code"].isin(valid_country_codes)
]

print("\nUniversities with Invalid Country Code:")
print(len(invalid_country_codes))


# Display invalid records if any
if len(invalid_country_codes) > 0:

    print("\nInvalid Country Code Records:")

    print(
        invalid_country_codes[
            [
                "university_id",
                "institution_name",
                "location",
                "country_code"
            ]
        ].to_string(index=False)
    )

else:

    print("\nAll universities have valid country codes.")


# Final validation
if missing_country_codes == 0 and len(invalid_country_codes) == 0:
    print("\nUniversity → Country Validation: PASSED")
else:
    print("\nUniversity → Country Validation: FAILED")

# ============================================================
# STEP 2.13 - FINAL QS 2025 VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.13 - FINAL QS 2025 VALIDATION")
print("=" * 60)

required_columns = [
    "university_id",
    "institution_name",
    "country_code",
    "rank_2025",
    "rank_2024",
    "location",
    "region",
    "size",
    "focus",
    "res",
    "status",
    "academic_reputation_score",
    "academic_reputation_rank",
    "employer_reputation_score",
    "employer_reputation_rank",
    "faculty_student_score",
    "faculty_student_rank",
    "citations_per_faculty_score",
    "citations_per_faculty_rank",
    "international_faculty_score",
    "international_faculty_rank",
    "international_students_score",
    "international_students_rank",
    "international_research_network_score",
    "international_research_network_rank",
    "employment_outcomes_score",
    "employment_outcomes_rank",
    "sustainability_score",
    "sustainability_rank",
    "overall_score"
]

# Check required columns
missing_required_columns = [
    col for col in required_columns
    if col not in df.columns
]

# Validation values
duplicate_rows = df.duplicated().sum()

duplicate_universities = df["institution_name"].duplicated().sum()

duplicate_ids = df["university_id"].duplicated().sum()

missing_university_ids = df["university_id"].isna().sum()

missing_university_names = df["institution_name"].isna().sum()

missing_country_codes = df["country_code"].isna().sum()

number_of_countries = df["country_code"].nunique()

# Print validation results
print("\nDataset Shape:")
print(df.shape)

print("\nMissing Required Columns:")
print(missing_required_columns)

print("\nDuplicate Rows:")
print(duplicate_rows)

print("\nDuplicate University Names:")
print(duplicate_universities)

print("\nDuplicate University IDs:")
print(duplicate_ids)

print("\nMissing University IDs:")
print(missing_university_ids)

print("\nMissing University Names:")
print(missing_university_names)

print("\nMissing Country Codes:")
print(missing_country_codes)

print("\nNumber of Countries:")
print(number_of_countries)

# ============================================================
# STEP 2.14 - SAVE CLEANED QS 2025 DATASET
# ============================================================

output_path = "data/cleaned/qs_world_university_rankings_2025_cleaned.csv"

df.to_csv(output_path, index=False)

print("\n============================================================")
print("QS 2025 CLEANED DATASET SAVED")
print("============================================================")
print(f"Output file: {output_path}")
print(f"Final shape: {df.shape}")
print("File saved successfully!")

# ============================================================
# FINAL VALIDATION CONDITION
# ============================================================

validation_passed = (
    len(missing_required_columns) == 0
    and duplicate_rows == 0
    and duplicate_universities == 0
    and duplicate_ids == 0
    and missing_university_ids == 0
    and missing_university_names == 0
    and missing_country_codes == 0
    and number_of_countries == 106
)

if validation_passed:

    print("\n" + "=" * 60)
    print("FINAL QS 2025 VALIDATION: PASSED")
    print("=" * 60)

else:

    print("\n" + "=" * 60)
    print("FINAL QS 2025 VALIDATION: FAILED")
    print("=" * 60)

    print("\nValidation Details:")

    if len(missing_required_columns) > 0:
        print("❌ Missing required columns:",
              missing_required_columns)

    if duplicate_rows > 0:
        print("❌ Duplicate rows:", duplicate_rows)

    if duplicate_universities > 0:
        print("❌ Duplicate university names:",
              duplicate_universities)

    if duplicate_ids > 0:
        print("❌ Duplicate university IDs:",
              duplicate_ids)

    if missing_university_ids > 0:
        print("❌ Missing university IDs:",
              missing_university_ids)

    if missing_university_names > 0:
        print("❌ Missing university names:",
              missing_university_names)

    if missing_country_codes > 0:
        print("❌ Missing country codes:",
              missing_country_codes)

    if number_of_countries != 106:
        print("❌ Unexpected number of countries:",
              number_of_countries)