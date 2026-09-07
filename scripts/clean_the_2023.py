import pandas as pd
import numpy as np
import os
import re

# ============================================================
# DATASET 3 - WORLD UNIVERSITY RANKINGS 2023
# ============================================================

INPUT_FILE = "data/raw/World University Rankings 2023.csv"
OUTPUT_FILE = "data/cleaned/the_world_university_rankings_2023_cleaned.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("=" * 60)
print("DATASET 3 - WORLD UNIVERSITY RANKINGS 2023")
print("=" * 60)

# ============================================================
# STEP 3.1 - LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully!")
print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nMissing Value Percentage:")
missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
print(missing_pct)

# ============================================================
# STEP 3.2 - DUPLICATE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.2 - DUPLICATE ANALYSIS")
print("=" * 60)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate University Names:")
name_dup_count = df["Name of University"].dropna().duplicated().sum()
print(name_dup_count)

# Remove exact duplicate rows
duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows Before Removal:")
print(duplicate_rows)

if duplicate_rows > 0:
    df = df.drop_duplicates().copy()

print("\nDuplicate Rows After Removal:")
print(df.duplicated().sum())

# ============================================================
# STEP 3.3 - RANK ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.3 - RANK ANALYSIS")
print("=" * 60)

print("\nSample Rank Values:")
print(df["University Rank"].head(20).to_string(index=False))

print("\nLast 20 Rank Values:")
print(df["University Rank"].tail(20).to_string(index=False))

print("\nUnique Rank Value Count:")
print(df["University Rank"].nunique())

print("\nRank Data Type:")
print(df["University Rank"].dtype)

# Clean rank strings such as "1", "2", "3", "Reporter", "201-250"
rank_text = df["University Rank"].astype(str).str.strip()

# Extract a numeric rank only when the value starts with a number.
# For ranges such as "201-250", the lower bound is used.
df["rank_numeric"] = pd.to_numeric(
    rank_text.str.extract(r"^(\d+(?:\.\d+)?)")[0],
    errors="coerce"
)

# Reporter / unranked rows have no numeric rank.
df["ranking_status"] = np.where(
    df["rank_numeric"].notna(),
    "Ranked",
    "Reporter"
)

print("\nRank Data Types After Cleaning:")
print(df["rank_numeric"].dtype)

print("\nNumber of Ranked Universities:")
print((df["ranking_status"] == "Ranked").sum())

print("\nNumber of Reporter Universities:")
print((df["ranking_status"] == "Reporter").sum())

print("\nRanking Status:")
print(df["ranking_status"].value_counts())

print("\nSample Cleaned Rank Data:")
print(
    df[["University Rank", "rank_numeric", "Name of University"]]
    .head(20)
    .to_string(index=False)
)

# ============================================================
# STEP 3.4 - UNIVERSITY NAME CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.4 - UNIVERSITY NAME CLEANING")
print("=" * 60)

# Convert to string, strip whitespace, and preserve missing names as NaN.
df["Name of University"] = df["Name of University"].apply(
    lambda x: x.strip() if isinstance(x, str) else x
)

print("\nMissing University Names Before:")
print(df["Name of University"].isnull().sum())

missing_names = df["Name of University"].isnull().sum()

# Remove rows where university name is missing
if missing_names > 0:
    df = df.dropna(subset=["Name of University"]).copy()

print("\nRows Removed Due to Missing University Name:")
print(missing_names)

print("\nMissing University Names After:")
print(df["Name of University"].isnull().sum())

print("\nDuplicate University Names After Cleaning:")
print(df["Name of University"].duplicated().sum())

# ============================================================
# STEP 3.5 - LOCATION CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.5 - LOCATION CLEANING")
print("=" * 60)

df["Location"] = df["Location"].apply(
    lambda x: x.strip() if isinstance(x, str) else x
)

print("\nMissing Locations Before:")
print(df["Location"].isnull().sum())

df["Location"] = df["Location"].fillna("Unknown")

print("\nMissing Locations After:")
print(df["Location"].isnull().sum())

print("\nNumber of Locations:")
print(df["Location"].nunique())

# ============================================================
# STEP 3.6 - STUDENT STATISTICS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.6 - STUDENT STATISTICS CLEANING")
print("=" * 60)

# No of student may contain commas or other non-numeric text.
df["No of student"] = (
    df["No of student"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace(r"[^\d.]", "", regex=True)
)

df["No of student"] = pd.to_numeric(
    df["No of student"], errors="coerce"
)

df["No of student per staff"] = pd.to_numeric(
    df["No of student per staff"], errors="coerce"
)

print("\nStudent Statistics Data Types:")
print(
    df[
        ["No of student", "No of student per staff"]
    ].dtypes
)

# International Student percentage
df["International Student"] = (
    df["International Student"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["International Student"] = pd.to_numeric(
    df["International Student"], errors="coerce"
)

# ============================================================
# STEP 3.7 - FEMALE-MALE RATIO CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.7 - FEMALE-MALE RATIO CLEANING")
print("=" * 60)

def extract_female_percentage(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # Accept formats such as:
    # 49:51
    # 49 : 51
    # 49%
    match = re.search(r"(\d+(?:\.\d+)?)\s*[:/]", value)

    if match:
        return float(match.group(1))

    # If there is only a numeric value, use it as female percentage.
    match = re.fullmatch(r"\d+(?:\.\d+)?", value)

    if match:
        return float(value)

    return np.nan

df["female_percentage"] = df["Female:Male Ratio"].apply(
    extract_female_percentage
)

print("\nFemale Percentage Sample:")
print(
    df[
        ["Female:Male Ratio", "female_percentage"]
    ].head(20).to_string(index=False)
)

print("\nMissing Female Percentage:")
print(df["female_percentage"].isnull().sum())

# ============================================================
# STEP 3.8 - SCORE DATA TYPE CONVERSION
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.8 - SCORE DATA TYPE CONVERSION")
print("=" * 60)

score_columns = [
    "OverAll Score",
    "Teaching Score",
    "Research Score",
    "Citations Score",
    "Industry Income Score",
    "International Outlook Score"
]


for col in score_columns:

    def convert_score(value):

        # Handle missing values first
        if pd.isna(value):
            return np.nan

        # Convert value to string
        value = str(value).strip()

        # Remove percentage symbol
        value = value.replace("%", "")

        # Handle missing-value symbols
        if value in ["", "-", "—", "nan", "NaN", "N/A"]:
            return np.nan

        # Handle score ranges such as 51.2–54.3 or 51.2-54.3
        range_match = re.match(
            r"^\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*$",
            value
        )

        if range_match:
            lower = float(range_match.group(1))
            upper = float(range_match.group(2))

            # Use midpoint of the range
            return (lower + upper) / 2

        # Handle normal numeric score
        try:
            return float(value)

        except ValueError:
            return np.nan

    df[col] = df[col].apply(convert_score)


print("\nScore Data Types After Conversion:")
print(df[score_columns].dtypes)

print("\nMissing Score Values After Conversion:")
print(df[score_columns].isnull().sum())

# ============================================================
# STEP 3.9 - SCORE STATUS
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.9 - SCORE STATUS")
print("=" * 60)

df["score_status"] = np.where(
    df["OverAll Score"].notna(),
    "Available",
    "Not Available"
)

print("\nUniversities With Valid Overall Score:")
print((df["score_status"] == "Available").sum())

print("\nUniversities Without Overall Score:")
print((df["score_status"] == "Not Available").sum())

print("\nScore Status:")
print(df["score_status"].value_counts())

# ============================================================
# STEP 3.10 - HANDLE MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.10 - HANDLE MISSING VALUES")
print("=" * 60)

# Numeric student statistics:
# Use median only for the student-related fields where the dataset
# has missing values. This avoids inventing ranking scores.
numeric_impute_columns = [
    "No of student",
    "No of student per staff",
    "International Student",
    "female_percentage"
]

for col in numeric_impute_columns:
    before = df[col].isnull().sum()

    if before > 0:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)

        print(f"\n{col}")
        print("Missing Before:", before)
        print("Median Used:", median_value)
        print("Missing After:", df[col].isnull().sum())

# Female:Male Ratio is kept as the original categorical/string field.
# Fill missing original ratios with a ratio based on the imputed
# female percentage.
def make_ratio(female_pct):
    female_pct = float(female_pct)
    male_pct = 100 - female_pct
    return f"{female_pct:g} : {male_pct:g}"

df["Female:Male Ratio"] = df["Female:Male Ratio"].apply(
    lambda x: x.strip() if isinstance(x, str) else x
)

df["Female:Male Ratio"] = df["Female:Male Ratio"].fillna(
    df["female_percentage"].apply(make_ratio)
)

print("\nMissing Female:Male Ratio After:")
print(df["Female:Male Ratio"].isnull().sum())

# ============================================================
# STEP 3.11 - SCORE RANGE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.11 - SCORE RANGE VALIDATION")
print("=" * 60)

for col in score_columns:
    invalid = ((df[col] < 0) | (df[col] > 100)).sum()
    print(f"{col} invalid values: {invalid}")

invalid_intl = (
    (df["International Student"] < 0)
    | (df["International Student"] > 100)
).sum()

invalid_female = (
    (df["female_percentage"] < 0)
    | (df["female_percentage"] > 100)
).sum()

print("\nInvalid International Student Percentage:")
print(invalid_intl)

print("\nInvalid Female Percentage:")
print(invalid_female)

print("\nInvalid Student Count:")
print((df["No of student"] < 0).sum())

# ============================================================
# STEP 3.12 - FINAL DATA QUALITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 3.12 - FINAL DATA QUALITY VALIDATION")
print("=" * 60)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Rows After Removal:")
print(df.duplicated().sum())

print("\nMissing University Names:")
print(df["Name of University"].isnull().sum())

print("\nMissing Locations:")
print(df["Location"].isnull().sum())

print("\nRanking Status:")
print(df["ranking_status"].value_counts())

print("\nScore Status:")
print(df["score_status"].value_counts())

print("\nFinal Missing Values:")
final_missing = df.isnull().sum()
print(final_missing[final_missing > 0])

# Expected missing values:
# - rank_numeric: reporter universities
# - score columns: universities without scores
expected_rank_missing = (df["ranking_status"] == "Reporter").sum()
expected_score_missing = (df["score_status"] == "Not Available").sum()

actual_rank_missing = df["rank_numeric"].isnull().sum()
actual_score_missing = df["OverAll Score"].isnull().sum()

print("\nExpected Missing rank_numeric:")
print(expected_rank_missing)

print("\nActual Missing rank_numeric:")
print(actual_rank_missing)

print("\nExpected Missing Score Values:")
print(expected_score_missing)

print("\nActual Missing Overall Score:")
print(actual_score_missing)

# Check consistency
rank_check = actual_rank_missing == expected_rank_missing
score_check = actual_score_missing == expected_score_missing

# Score columns should all have the same missing-score count.
all_score_missing_same = all(
    df[col].isnull().sum() == expected_score_missing
    for col in score_columns
)

# No invalid values
score_range_check = all(
    (((df[col] >= 0) & (df[col] <= 100)) | df[col].isna()).all()
    for col in score_columns
)

intl_check = (
    df["International Student"].between(0, 100).all()
)

female_check = (
    df["female_percentage"].between(0, 100).all()
)

student_check = (
    (df["No of student"] >= 0).all()
)

unexpected_missing = df[
    [
        "Name of University",
        "Location",
        "No of student",
        "No of student per staff",
        "International Student",
        "Female:Male Ratio",
        "female_percentage"
    ]
].isnull().sum().sum()

print("\nUnexpected Missing Values:")
print(unexpected_missing)

if (
    rank_check
    and score_check
    and all_score_missing_same
    and score_range_check
    and intl_check
    and female_check
    and student_check
    and unexpected_missing == 0
):
    print("\n" + "=" * 60)
    print("✅ DATASET 3 CLEANING PASSED")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("⚠️ DATASET 3 CLEANING NEEDS REVIEW")
    print("=" * 60)

# ============================================================
# STEP 3.13 - FINAL DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATASET 3 SUMMARY")
print("=" * 60)

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nNumber of Ranked Universities:")
print((df["ranking_status"] == "Ranked").sum())

print("\nNumber of Reporter Universities:")
print((df["ranking_status"] == "Reporter").sum())

print("\nUniversities With Available Scores:")
print((df["score_status"] == "Available").sum())

print("\nUniversities Without Scores:")
print((df["score_status"] == "Not Available").sum())

print("\nFinal Dataset Columns:")
print(df.columns.tolist())

# ============================================================
# STEP 3.14 - SAVE CLEANED DATASET
# ============================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("STEP 3.14 - SAVE CLEANED DATASET")
print("=" * 60)

print("\nCleaned Dataset Saved Successfully!")
print(OUTPUT_FILE)

print("\nFinal Dataset Shape:")
print(df.shape)

print("\n" + "=" * 60)
print("FINAL WORLD UNIVERSITY RANKINGS 2023 CLEANING COMPLETED")
print("=" * 60)
