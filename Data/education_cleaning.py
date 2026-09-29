#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ============================================================
# EDUVISION_DV - MODULE 2: DATA CLEANING & TRANSFORMATION
# ============================================================

import pandas as pd
import numpy as np
import re
from pathlib import Path

print("=" * 70)
print("EDUVISION_DV - MODULE 2: DATA CLEANING & TRANSFORMATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

BASE_DIR = Path(
    r"C:/Users/gdivy/OneDrive/Desktop/Internship 7.0 project"
)

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_raw_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_cleaned.csv"
)

print("\nInput file:")
print(INPUT_FILE)

print("\nOutput file:")
print(OUTPUT_FILE)


# In[2]:


# ------------------------------------------------------------
# 2. Load Module 1 raw dataset
# ------------------------------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"university_raw_data.csv not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")


# In[3]:


# ------------------------------------------------------------
# 3. Initial dataset inspection
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INITIAL DATASET INSPECTION")
print("=" * 70)

print("\nColumns:")
for i, column in enumerate(df.columns, start=1):
    print(f"{i:02d}. {column}")

print("\nFirst 5 rows:")
display(df.head())

print("\nData types:")
display(df.dtypes)


# In[4]:


# -------------------------------------------------------
# 4. Check and remove duplicate records
# -------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE RECORD CHECK")
print("=" * 70)

# Count exact duplicate rows
duplicate_count = df.duplicated().sum()

print(f"Exact duplicate rows found: {duplicate_count:,}")

# Store row count before removing duplicates
rows_before = len(df)

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Store row count after removing duplicates
rows_after = len(df)

print(f"Rows before duplicate removal: {rows_before:,}")
print(f"Rows after duplicate removal : {rows_after:,}")
print(f"Duplicates removed            : {rows_before - rows_after:,}")

# Verify that no exact duplicates remain
remaining_duplicates = df.duplicated().sum()

print(f"\nExact duplicates remaining: {remaining_duplicates:,}")


# In[5]:


# -------------------------------------------------------
# 5. Standardize university names
# -------------------------------------------------------

print("\n" + "=" * 70)
print("STANDARDIZING UNIVERSITY NAMES")
print("=" * 70)


def standardize_university_name(name):
    """
    Standardizes university names by:
    - Removing extra spaces
    - Removing text inside parentheses
    - Replacing '&' with 'and'
    - Removing unnecessary punctuation
    - Normalizing whitespace
    """

    # Keep missing values as missing
    if pd.isna(name):
        return np.nan

    # Convert to string and remove leading/trailing spaces
    name = str(name).strip()

    # Remove text inside parentheses
    name = re.sub(r"\([^)]*\)", "", name)

    # Replace ampersand with "and"
    name = name.replace("&", "and")

    # Remove unnecessary punctuation
    name = re.sub(r"[^\w\s]", " ", name)

    # Remove repeated spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name


# Apply the standardization
df["University"] = df["University"].apply(
    standardize_university_name
)

print("University names standardized successfully.")

# Show sample of cleaned university names
display(
    df[["University"]]
    .drop_duplicates()
    .head(20)
)


# In[6]:


# -------------------------------------------------------
# 6. Standardize country names
# -------------------------------------------------------

print("\n" + "=" * 70)
print("STANDARDIZING COUNTRY NAMES")
print("=" * 70)


def standardize_country_name(country):
    """
    Standardizes country names by:
    - Removing leading/trailing spaces
    - Removing repeated spaces
    - Converting common country-name variations
      into a consistent form
    """

    # Keep missing values as missing
    if pd.isna(country):
        return np.nan

    # Convert to string and remove extra spaces
    country = str(country).strip()
    country = re.sub(r"\s+", " ", country)

    # Common country-name variations
    country_mapping = {
        "USA": "United States",
        "US": "United States",
        "U.S.": "United States",
        "U.S.A.": "United States",
        "UK": "United Kingdom",
        "U.K.": "United Kingdom",
        "Korea, Republic of": "South Korea",
        "South Korea": "South Korea",
        "Russia": "Russian Federation",
        "UAE": "United Arab Emirates"
    }

    # Replace only known variations
    country = country_mapping.get(country, country)

    return country


# Apply the standardization
df["Country"] = df["Country"].apply(
    standardize_country_name
)

print("Country names standardized successfully.")

# Display unique countries
print(
    f"\nUnique countries: "
    f"{df['Country'].nunique():,}"
)

display(
    df[["Country"]]
    .drop_duplicates()
    .sort_values("Country")
    .head(50)
)


# In[7]:


# -------------------------------------------------------
# 6A. Improve country-name standardization
# -------------------------------------------------------

print("\n" + "=" * 70)
print("IMPROVING COUNTRY NAME STANDARDIZATION")
print("=" * 70)

# Additional country-name mappings
additional_country_mapping = {
    "China (Mainland)": "China",
    "Iran, Islamic Republic of": "Iran"
}

# Apply the additional mappings
df["Country"] = df["Country"].replace(
    additional_country_mapping
)

print("Additional country-name standardization completed.")

# Check the affected countries
print("\nCheck:")
display(
    df[df["Country"].isin(["China", "Iran"])][["Country"]]
    .drop_duplicates()
)


# In[8]:


# Verify unique country count after standardization

print(
    f"Unique countries after standardization: "
    f"{df['Country'].nunique():,}"
)

display(
    df[["Country"]]
    .drop_duplicates()
    .sort_values("Country")
)


# In[9]:


# -------------------------------------------------------
# 7. Clean ranking and score columns
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CLEANING RANKING AND SCORE COLUMNS")
print("=" * 70)


# -------------------------------------------------------
# 7.1 Clean QS Rank
# -------------------------------------------------------

# Convert QS rank values to numeric.
# Invalid or non-numeric values become NaN.

df["QS_Rank"] = pd.to_numeric(
    df["QS_Rank"],
    errors="coerce"
)


# -------------------------------------------------------
# 7.2 Clean QS Overall Score
# -------------------------------------------------------

# Convert QS overall score to numeric.
# Invalid values become NaN.

df["QS_Overall_Score"] = pd.to_numeric(
    df["QS_Overall_Score"],
    errors="coerce"
)


# -------------------------------------------------------
# 7.3 Clean THE International Students
# -------------------------------------------------------

# THE International Students is stored as text such as:
# "15%"
#
# Remove the % symbol and convert to numeric.

df["THE_International_Students"] = (
    df["THE_International_Students"]
    .astype("string")
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["THE_International_Students"] = pd.to_numeric(
    df["THE_International_Students"],
    errors="coerce"
)


# -------------------------------------------------------
# 7.4 Clean THE Female-Male Ratio
# -------------------------------------------------------

# Values may look like:
# "48:52"
#
# We will keep the ratio in its original form for now.
# Later, Module 3 can derive useful numeric measures
# if required.

df["THE_Female_Male_Ratio"] = (
    df["THE_Female_Male_Ratio"]
    .astype("string")
    .str.strip()
)


# -------------------------------------------------------
# 7.5 Convert THE Year to integer
# -------------------------------------------------------

df["THE_Year"] = pd.to_numeric(
    df["THE_Year"],
    errors="coerce"
)

print("Ranking and score columns cleaned successfully.")

# Display updated data types
print("\nUpdated data types:")

display(
    df[
        [
            "QS_Rank",
            "QS_Overall_Score",
            "THE_Rank",
            "THE_Overall_Score",
            "THE_International_Students",
            "THE_Female_Male_Ratio",
            "THE_Year"
        ]
    ].dtypes
)


# In[10]:


# -------------------------------------------------------
# 8. Validate ranking and score ranges
# -------------------------------------------------------

print("\n" + "=" * 70)
print("RANKING AND SCORE RANGE VALIDATION")
print("=" * 70)


# -------------------------------------------------------
# 8.1 QS Rank
# -------------------------------------------------------

print("\nQS Rank range:")
print("Minimum:", df["QS_Rank"].min())
print("Maximum:", df["QS_Rank"].max())


# -------------------------------------------------------
# 8.2 QS Overall Score
# -------------------------------------------------------

print("\nQS Overall Score range:")
print("Minimum:", df["QS_Overall_Score"].min())
print("Maximum:", df["QS_Overall_Score"].max())


# -------------------------------------------------------
# 8.3 THE Rank
# -------------------------------------------------------

print("\nTHE Rank range:")
print("Minimum:", df["THE_Rank"].min())
print("Maximum:", df["THE_Rank"].max())


# -------------------------------------------------------
# 8.4 THE Overall Score
# -------------------------------------------------------

print("\nTHE Overall Score range:")
print("Minimum:", df["THE_Overall_Score"].min())
print("Maximum:", df["THE_Overall_Score"].max())


# -------------------------------------------------------
# 8.5 THE International Students
# -------------------------------------------------------

print("\nTHE International Students percentage range:")
print("Minimum:", df["THE_International_Students"].min())
print("Maximum:", df["THE_International_Students"].max())


# -------------------------------------------------------
# 8.6 QS score indicators
# -------------------------------------------------------

qs_score_columns = [
    "QS_Academic_Reputation",
    "QS_Employer_Reputation",
    "QS_Faculty_Student",
    "QS_Citations_Per_Faculty",
    "QS_International_Faculty",
    "QS_International_Students",
    "QS_International_Research_Network",
    "QS_Employment_Outcomes",
    "QS_Sustainability"
]

print("\nQS indicator ranges:")

for column in qs_score_columns:
    print(
        f"{column}: "
        f"{df[column].min()} → {df[column].max()}"
    )


# -------------------------------------------------------
# 8.7 THE indicator ranges
# -------------------------------------------------------

the_score_columns = [
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook"
]

print("\nTHE indicator ranges:")

for column in the_score_columns:
    print(
        f"{column}: "
        f"{df[column].min()} → {df[column].max()}"
    )


# In[11]:


# -------------------------------------------------------
# 9. Normalize QS and THE ranking positions
# -------------------------------------------------------

print("\n" + "=" * 70)
print("NORMALIZING RANKING POSITIONS")
print("=" * 70)


def normalize_rank(series):
    """
    Converts a ranking position into a 0-100 score.

    Rank 1 receives the highest score.
    A lower ranking position is considered better.

    Formula:

        (maximum_rank - rank) /
        (maximum_rank - minimum_rank) * 100
    """

    minimum_rank = series.min()
    maximum_rank = series.max()

    # Avoid division by zero
    if maximum_rank == minimum_rank:
        return pd.Series(
            100,
            index=series.index
        )

    return (
        (maximum_rank - series)
        / (maximum_rank - minimum_rank)
        * 100
    )


# -------------------------------------------------------
# QS normalized ranking score
# -------------------------------------------------------

df["QS_Normalized_Rank"] = normalize_rank(
    df["QS_Rank"]
)


# -------------------------------------------------------
# THE normalized ranking score
# -------------------------------------------------------

df["THE_Normalized_Rank"] = normalize_rank(
    df["THE_Rank"]
)


print("QS and THE ranking positions normalized to a 0-100 scale.")


# Display sample results
display(
    df[
        [
            "University",
            "QS_Rank",
            "QS_Normalized_Rank",
            "THE_Rank",
            "THE_Normalized_Rank"
        ]
    ].head(10)
)


# In[42]:


# -------------------------------------------------------
# 10. Clean percentage and ratio fields
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CLEANING PERCENTAGE AND RATIO FIELDS")
print("=" * 70)


# -------------------------------------------------------
# 10.1 Clean THE International Students
# -------------------------------------------------------

# Source values may contain values such as "15%".
# Remove the % symbol and convert to numeric.

df["THE_International_Students"] = (
    df["THE_International_Students"]
    .astype("string")
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["THE_International_Students"] = pd.to_numeric(
    df["THE_International_Students"],
    errors="coerce"
)


# -------------------------------------------------------
# 10.2 Clean THE Female-Male Ratio
# -------------------------------------------------------

# The source may contain values such as:
# "48:52"
# "39 : 61"
# "49:51:00"
#
# We keep the original ratio and extract the first
# two numeric values.

df["THE_Female_Male_Ratio"] = (
    df["THE_Female_Male_Ratio"]
    .astype("string")
    .str.strip()
)

# Extract female percentage
df["THE_Female_Percentage"] = (
    df["THE_Female_Male_Ratio"]
    .str.extract(
        r"^\s*(\d+(?:\.\d+)?)\s*:"
    )[0]
)

# Extract male percentage
df["THE_Male_Percentage"] = (
    df["THE_Female_Male_Ratio"]
    .str.extract(
        r"^\s*\d+(?:\.\d+)?\s*:\s*(\d+(?:\.\d+)?)"
    )[0]
)

# Convert to numeric
df["THE_Female_Percentage"] = pd.to_numeric(
    df["THE_Female_Percentage"],
    errors="coerce"
)

df["THE_Male_Percentage"] = pd.to_numeric(
    df["THE_Male_Percentage"],
    errors="coerce"
)

print("Female-male ratio extraction completed.")

display(
    df[
        [
            "University",
            "THE_Female_Male_Ratio",
            "THE_Female_Percentage",
            "THE_Male_Percentage"
        ]
    ].head(10)
)


# In[43]:


# -------------------------------------------------------
# 11. Review cleaned data types and missing values
# -------------------------------------------------------

print("\n" + "=" * 70)
print("POST-CLEANING DATA QUALITY CHECK")
print("=" * 70)

# Display current data types
print("\nCurrent data types:")
display(df.dtypes)

# Calculate missing values
missing_count = df.isna().sum()

missing_percentage = (
    df.isna().mean() * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage
})

print("\nMissing-value summary:")
display(
    missing_summary
    .sort_values(
        "Missing_Percentage",
        ascending=False
    )
)


# In[44]:


# -------------------------------------------------------
# 12. Create the 2025 comparison dataset
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING 2025 COMPARISON DATASET")
print("=" * 70)

# Select only THE 2025 records
the_2025 = df[
    df["THE_Year"] == 2025
].copy()

# Select QS 2025 records
qs_2025 = df[
    df["QS_Rank"].notna()
].copy()

print(f"QS 2025 records : {len(qs_2025):,}")
print(f"THE 2025 records: {len(the_2025):,}")


# In[45]:


# -------------------------------------------------------
# 12A. Create university matching keys for 2025 data
# -------------------------------------------------------

def create_matching_key(name):
    """
    Creates a consistent matching key from a university name.
    This key is used only to match QS and THE records.
    """

    if pd.isna(name):
        return ""

    name = str(name).lower().strip()

    # Remove text inside parentheses
    name = re.sub(r"\([^)]*\)", "", name)

    # Standardize ampersand
    name = name.replace("&", "and")

    # Remove punctuation
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    # Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()

    return name


qs_2025["University_Key"] = (
    qs_2025["University"]
    .apply(create_matching_key)
)

the_2025["University_Key"] = (
    the_2025["University"]
    .apply(create_matching_key)
)

print("University matching keys created.")


# In[46]:


# -------------------------------------------------------
# 12B. Merge QS and THE 2025 datasets
# -------------------------------------------------------

print("\n" + "=" * 70)
print("MERGING QS AND THE 2025 DATA")
print("=" * 70)

cleaned_2025 = pd.merge(
    qs_2025,
    the_2025,
    on="University_Key",
    how="outer",
    suffixes=("_QS", "_THE"),
    indicator=True
)

print(f"QS records       : {len(qs_2025):,}")
print(f"THE records      : {len(the_2025):,}")
print(f"Merged records   : {len(cleaned_2025):,}")

print("\nMerge status:")
print(cleaned_2025["_merge"].value_counts())


# In[47]:


# -------------------------------------------------------
# 12C. Improve university matching
# -------------------------------------------------------

import unicodedata


def create_improved_matching_key(name):
    """
    Creates a stronger matching key by:
    - Converting to lowercase
    - Removing accents/diacritics
    - Removing text inside parentheses
    - Replacing '&' with 'and'
    - Removing punctuation
    - Normalizing whitespace
    """

    if pd.isna(name):
        return ""

    name = str(name).lower().strip()

    # Remove accents / diacritics
    name = unicodedata.normalize(
        "NFKD",
        name
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "ascii"
    )

    # Remove text inside parentheses
    name = re.sub(
        r"\([^)]*\)",
        "",
        name
    )

    # Standardize ampersand
    name = name.replace(
        "&",
        "and"
    )

    # Remove punctuation
    name = re.sub(
        r"[^a-z0-9\s]",
        " ",
        name
    )

    # Normalize spaces
    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    return name


# Create improved keys
qs_2025["Improved_Key"] = (
    qs_2025["University"]
    .apply(create_improved_matching_key)
)

the_2025["Improved_Key"] = (
    the_2025["University"]
    .apply(create_improved_matching_key)
)

print("Improved university matching keys created.")


# In[48]:


# -------------------------------------------------------
# 12D. Recheck QS-THE matching
# -------------------------------------------------------

improved_merge = pd.merge(
    qs_2025,
    the_2025,
    on="Improved_Key",
    how="outer",
    suffixes=("_QS", "_THE"),
    indicator=True
)

print("\n" + "=" * 70)
print("IMPROVED MERGE VALIDATION")
print("=" * 70)

print(f"QS records       : {len(qs_2025):,}")
print(f"THE records      : {len(the_2025):,}")
print(f"Merged records   : {len(improved_merge):,}")

print("\nMerge status:")
print(improved_merge["_merge"].value_counts())

matched_improved = (
    improved_merge["_merge"] == "both"
).sum()

match_percentage = (
    matched_improved / len(qs_2025)
) * 100

print(
    f"\nQS matching percentage: "
    f"{match_percentage:.2f}%"
)


# In[49]:


# -------------------------------------------------------
# 12E. Create unique QS 2025 and THE 2025 datasets
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING UNIQUE QS AND THE 2025 DATASETS")
print("=" * 70)


# -------------------------------------------------------
# QS 2025 dataset
# -------------------------------------------------------

qs_2025_clean = df[
    df["QS_Rank"].notna()
].copy()

qs_columns_final = [
    "University",
    "Country",
    "QS_Rank",
    "QS_Overall_Score",
    "QS_Academic_Reputation",
    "QS_Employer_Reputation",
    "QS_Faculty_Student",
    "QS_Citations_Per_Faculty",
    "QS_International_Faculty",
    "QS_International_Students",
    "QS_International_Research_Network",
    "QS_Employment_Outcomes",
    "QS_Sustainability",
    "QS_Normalized_Rank"
]

qs_2025_clean = qs_2025_clean[
    qs_columns_final
].copy()


# Create a matching key
qs_2025_clean["University_Key"] = (
    qs_2025_clean["University"]
    .apply(create_improved_matching_key)
)


# Keep only one QS 2025 record per university
qs_2025_clean = (
    qs_2025_clean
    .drop_duplicates(
        subset=["University_Key"],
        keep="first"
    )
    .copy()
)


print(
    f"Unique QS 2025 records: "
    f"{len(qs_2025_clean):,}"
)


# -------------------------------------------------------
# THE 2025 dataset
# -------------------------------------------------------

the_2025_clean = df[
    df["THE_Year"] == 2025
].copy()

the_columns_final = [
    "University",
    "Country",
    "THE_Rank",
    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook",
    "THE_Number_Students",
    "THE_Student_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_Male_Ratio",
    "THE_Year",
    "THE_Normalized_Rank",
    "THE_Female_Percentage",
    "THE_Male_Percentage"
]

the_2025_clean = the_2025_clean[
    the_columns_final
].copy()


# Create a matching key
the_2025_clean["University_Key"] = (
    the_2025_clean["University"]
    .apply(create_improved_matching_key)
)


# Keep only one THE 2025 record per university
the_2025_clean = (
    the_2025_clean
    .drop_duplicates(
        subset=["University_Key"],
        keep="first"
    )
    .copy()
)


print(
    f"Unique THE 2025 records: "
    f"{len(the_2025_clean):,}"
)


# In[50]:


# -------------------------------------------------------
# 12F. Create matching keys
# -------------------------------------------------------

qs_2025_clean["University_Key"] = (
    qs_2025_clean["University"]
    .apply(create_improved_matching_key)
)

the_2025_clean["University_Key"] = (
    the_2025_clean["University"]
    .apply(create_improved_matching_key)
)

print("Matching keys created successfully.")


# In[51]:


# -------------------------------------------------------
# 12G. Merge QS and THE 2025 datasets
# -------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL QS-THE 2025 MERGE")
print("=" * 70)

university_2025 = pd.merge(
    qs_2025_clean,
    the_2025_clean,
    on="University_Key",
    how="outer",
    suffixes=("_QS", "_THE"),
    indicator=True
)

print(f"QS records       : {len(qs_2025_clean):,}")
print(f"THE records      : {len(the_2025_clean):,}")
print(f"Merged records   : {len(university_2025):,}")

print("\nMerge status:")
print(university_2025["_merge"].value_counts())


# In[52]:


# -------------------------------------------------------
# 12H. Create final university and country fields
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING FINAL UNIVERSITY AND COUNTRY FIELDS")
print("=" * 70)

# Use QS university name when available.
# Otherwise use THE university name.
university_2025["University"] = (
    university_2025["University_QS"]
    .fillna(university_2025["University_THE"])
)

# Use QS country when available.
# Otherwise use THE country.
university_2025["Country"] = (
    university_2025["Country_QS"]
    .fillna(university_2025["Country_THE"])
)

print("University and Country fields created.")

display(
    university_2025[
        [
            "University",
            "Country",
            "_merge"
        ]
    ].head(10)
)


# In[53]:


# -------------------------------------------------------
# 12I. Select final Tableau-ready columns
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING FINAL CLEANED DATASET")
print("=" * 70)

final_cleaned_columns = [
    # University information
    "University",
    "Country",

    # QS 2025 indicators
    "QS_Rank",
    "QS_Overall_Score",
    "QS_Academic_Reputation",
    "QS_Employer_Reputation",
    "QS_Faculty_Student",
    "QS_Citations_Per_Faculty",
    "QS_International_Faculty",
    "QS_International_Students",
    "QS_International_Research_Network",
    "QS_Employment_Outcomes",
    "QS_Sustainability",
    "QS_Normalized_Rank",

    # THE 2025 indicators
    "THE_Rank",
    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook",
    "THE_Number_Students",
    "THE_Student_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_Male_Ratio",
    "THE_Year",
    "THE_Normalized_Rank",
    "THE_Female_Percentage",
    "THE_Male_Percentage"
]

# Keep only the required columns
cleaned_2025 = university_2025[
    final_cleaned_columns
].copy()

print(
    f"Final cleaned dataset shape: "
    f"{cleaned_2025.shape}"
)

print("\nFinal columns:")

for i, column in enumerate(
    cleaned_2025.columns,
    start=1
):
    print(f"{i:02d}. {column}")

print("\nFirst 5 rows:")
display(cleaned_2025.head())


# In[54]:


display(
    cleaned_2025[
        [
            "University",
            "THE_Female_Male_Ratio",
            "THE_Female_Percentage",
            "THE_Male_Percentage"
        ]
    ].head(10)
)


# In[55]:


# -------------------------------------------------------
# 13. Final data-quality validation
# -------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 70)

# Check number of rows and columns
print(f"Rows    : {len(cleaned_2025):,}")
print(f"Columns : {len(cleaned_2025.columns)}")

# -------------------------------------------------------
# Check duplicate rows
# -------------------------------------------------------

duplicate_rows = cleaned_2025.duplicated().sum()

print(f"\nExact duplicate rows: {duplicate_rows:,}")


# -------------------------------------------------------
# Check duplicate universities
# -------------------------------------------------------

duplicate_universities = (
    cleaned_2025["University"]
    .duplicated()
    .sum()
)

print(
    f"Duplicate university names: "
    f"{duplicate_universities:,}"
)


# -------------------------------------------------------
# Missing-value analysis
# -------------------------------------------------------

missing_count = cleaned_2025.isna().sum()

missing_percentage = (
    cleaned_2025.isna().mean() * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage
})

print("\nMissing-value summary:")

display(
    missing_summary[
        missing_summary["Missing_Count"] > 0
    ].sort_values(
        "Missing_Percentage",
        ascending=False
    )
)


# -------------------------------------------------------
# Overall missing percentage
# -------------------------------------------------------

total_cells = (
    cleaned_2025.shape[0] *
    cleaned_2025.shape[1]
)

total_missing = cleaned_2025.isna().sum().sum()

overall_missing_percentage = (
    total_missing / total_cells * 100
)

print(
    f"\nOverall missing percentage: "
    f"{overall_missing_percentage:.2f}%"
)


# -------------------------------------------------------
# Final validation result
# -------------------------------------------------------

if (
    duplicate_rows == 0
    and duplicate_universities == 0
    and overall_missing_percentage < 2
):

    print("\nPASS: Dataset meets the Module 2 quality checks.")

else:

    print("\nWARNING: One or more quality checks need attention.")


# In[56]:


# -------------------------------------------------------
# 14. Create matched QS-THE 2025 dataset
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING MATCHED QS-THE 2025 DATASET")
print("=" * 70)

# Keep only universities that appear in BOTH QS and THE
matched_2025 = university_2025[
    university_2025["_merge"] == "both"
].copy()

print(f"Matched universities: {len(matched_2025):,}")

print("\nMerge status:")
print(
    university_2025["_merge"].value_counts()
)

display(
    matched_2025[
        ["University", "Country"]
    ].head(10)
)


# In[57]:


# Check the missing values in the matched dataset

print("\nMissing values in matched dataset:")

matched_missing = (
    matched_2025
    .isna()
    .sum()
    .sort_values(ascending=False)
)

display(
    matched_missing[
        matched_missing > 0
    ]
)


# In[58]:


# -------------------------------------------------------
# 14. Final missing-value check for matched dataset
# -------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL MISSING-VALUE CHECK")
print("=" * 70)

total_cells = (
    matched_2025.shape[0] *
    matched_2025.shape[1]
)

total_missing = (
    matched_2025.isna().sum().sum()
)

missing_percentage = (
    total_missing /
    total_cells *
    100
)

print(f"Rows    : {matched_2025.shape[0]:,}")
print(f"Columns : {matched_2025.shape[1]:,}")
print(f"Missing cells : {total_missing:,}")
print(
    f"Overall missing percentage: "
    f"{missing_percentage:.2f}%"
)

if missing_percentage < 2:
    print("PASS: Overall missing percentage is below 2%.")
else:
    print("WARNING: Overall missing percentage is 2% or higher.")


# In[59]:


# -------------------------------------------------------
# 15. Create final Tableau-ready cleaned dataset
# -------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING FINAL TABLEAU-READY DATASET")
print("=" * 70)


# Keep only universities available in BOTH QS and THE
final_cleaned = university_2025[
    university_2025["_merge"] == "both"
].copy()


# -------------------------------------------------------
# Select useful analytical columns
# -------------------------------------------------------

final_columns = [
    # University information
    "University",
    "Country",

    # QS 2025 indicators
    "QS_Rank",
    "QS_Overall_Score",
    "QS_Academic_Reputation",
    "QS_Employer_Reputation",
    "QS_Faculty_Student",
    "QS_Citations_Per_Faculty",
    "QS_International_Faculty",
    "QS_International_Students",
    "QS_International_Research_Network",
    "QS_Employment_Outcomes",
    "QS_Sustainability",
    "QS_Normalized_Rank",

    # THE 2025 indicators
    "THE_Rank",
    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook",
    "THE_Number_Students",
    "THE_Student_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_Male_Ratio",
    "THE_Year",
    "THE_Normalized_Rank",
    "THE_Female_Percentage",
    "THE_Male_Percentage"
]


# Create the final dataset
final_cleaned = final_cleaned[
    final_columns
].copy()


# -------------------------------------------------------
# Clean THE Year
# -------------------------------------------------------

final_cleaned["THE_Year"] = (
    pd.to_numeric(
        final_cleaned["THE_Year"],
        errors="coerce"
    ).astype("Int64")
)


# -------------------------------------------------------
# Clean the female-male ratio display
# -------------------------------------------------------

final_cleaned["THE_Female_Male_Ratio"] = (
    final_cleaned["THE_Female_Male_Ratio"]
    .astype("string")
    .str.replace(
        r":00$",
        "",
        regex=True
    )
)


# -------------------------------------------------------
# Final duplicate check
# -------------------------------------------------------

duplicate_rows = final_cleaned.duplicated().sum()

duplicate_universities = (
    final_cleaned["University"]
    .duplicated()
    .sum()
)


print(f"Final rows: {len(final_cleaned):,}")
print(f"Final columns: {len(final_cleaned.columns)}")

print(
    f"Exact duplicate rows: "
    f"{duplicate_rows:,}"
)

print(
    f"Duplicate universities: "
    f"{duplicate_universities:,}"
)

print("\nFinal dataset preview:")
display(final_cleaned.head())


# In[60]:


# -------------------------------------------------------
# 16. Final missing-value validation
# -------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL MODULE 2 VALIDATION")
print("=" * 70)


# Count missing values
final_missing_count = (
    final_cleaned.isna().sum()
)

final_missing_percentage = (
    final_cleaned.isna().mean() * 100
).round(2)


# Create missing-value report
final_missing_summary = pd.DataFrame({
    "Missing_Count": final_missing_count,
    "Missing_Percentage": final_missing_percentage
})


print("Columns with missing values:")

display(
    final_missing_summary[
        final_missing_summary["Missing_Count"] > 0
    ].sort_values(
        "Missing_Percentage",
        ascending=False
    )
)


# Calculate overall missing percentage
total_cells = (
    final_cleaned.shape[0] *
    final_cleaned.shape[1]
)

total_missing = (
    final_cleaned.isna().sum().sum()
)

overall_missing_percentage = (
    total_missing / total_cells * 100
)


print(
    f"\nOverall missing percentage: "
    f"{overall_missing_percentage:.2f}%"
)


# Final quality checks
print(f"\nRows: {len(final_cleaned):,}")
print(f"Columns: {len(final_cleaned.columns)}")
print(
    f"Exact duplicates: "
    f"{final_cleaned.duplicated().sum():,}"
)
print(
    f"Duplicate universities: "
    f"{final_cleaned['University'].duplicated().sum():,}"
)


if overall_missing_percentage < 2:
    print("\nPASS: Missing values are below the 2% target.")
else:
    print("\nWARNING: Missing values exceed the 2% target.")


# In[61]:


# -------------------------------------------------------
# 17. Save university_cleaned.csv
# -------------------------------------------------------

print("\n" + "=" * 70)
print("SAVING MODULE 2 OUTPUT")
print("=" * 70)

# Make sure the processed folder exists
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save the final cleaned dataset
final_cleaned.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("university_cleaned.csv created successfully.")

print("\nSaved to:")
print(OUTPUT_FILE)

print(f"\nRows: {len(final_cleaned):,}")
print(f"Columns: {len(final_cleaned.columns)}")


# In[ ]:




