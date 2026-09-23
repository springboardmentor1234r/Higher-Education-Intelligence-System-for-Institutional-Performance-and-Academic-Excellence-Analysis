# ============================================================
# EduVision_DV - University Standardization
# ============================================================
# Creates standardized university and country fields.
# Raw datasets are NOT modified.
# ============================================================

import pandas as pd
import re
import unicodedata
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"

CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------

qs = pd.read_csv(RAW_DATA_DIR / "qs_2025_raw.csv")
the = pd.read_csv(RAW_DATA_DIR / "the_2024_raw.csv")
wur = pd.read_csv(RAW_DATA_DIR / "wur_2023_raw.csv")


# ------------------------------------------------------------
# Standardize university names
# ------------------------------------------------------------

def standardize_university_name(name):
    """
    Creates a normalized university name for matching.

    Original university name is preserved separately.
    """

    if pd.isna(name):
        return None

    name = str(name).strip()

    # Remove text inside parentheses
    name = re.sub(r"\([^)]*\)", "", name)

    # Remove common leading article
    name = re.sub(r"^the\s+", "", name, flags=re.IGNORECASE)

    # Convert accented characters to their closest ASCII form
    import unicodedata

    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # Replace punctuation with spaces
    name = re.sub(r"[^A-Za-z0-9\s]", " ", name)

    # Normalize multiple spaces
    name = re.sub(r"\s+", " ", name)

    # Convert to lowercase
    name = name.lower().strip()

    return name


# ------------------------------------------------------------
# Standardize country names
# ------------------------------------------------------------

country_mapping = {
    "China (Mainland)": "China",
    "Russian Federation": "Russia",
}


def standardize_country(country):
    """
    Standardizes known country-name variations.
    """

    if pd.isna(country):
        return None

    country = str(country).strip()

    return country_mapping.get(country, country)


# ------------------------------------------------------------
# QS standardization
# ------------------------------------------------------------

qs_clean = qs.copy()

qs_clean["University_Name_Original"] = qs_clean["Institution_Name"]

qs_clean["University_Name_Standard"] = (
    qs_clean["Institution_Name"]
    .apply(standardize_university_name)
)

qs_clean["Country_Standard"] = (
    qs_clean["Location"]
    .apply(standardize_country)
)


# ------------------------------------------------------------
# THE standardization
# ------------------------------------------------------------

the_clean = the.copy()

the_clean["University_Name_Original"] = the_clean["Name"]

the_clean["University_Name_Standard"] = (
    the_clean["Name"]
    .apply(standardize_university_name)
)

the_clean["Country_Standard"] = (
    the_clean["Country"]
    .apply(standardize_country)
)


# ------------------------------------------------------------
# WUR standardization
# ------------------------------------------------------------

wur_clean = wur.copy()

wur_clean["University_Name_Original"] = (
    wur_clean["Name of University"]
)

wur_clean["University_Name_Standard"] = (
    wur_clean["Name of University"]
    .apply(standardize_university_name)
)

wur_clean["Country_Standard"] = (
    wur_clean["Location"]
    .apply(standardize_country)
)


# ------------------------------------------------------------
# Remove records without identifiable university names
# ------------------------------------------------------------

wur_clean = wur_clean[
    wur_clean["University_Name_Standard"].notna()
].copy()


# ------------------------------------------------------------
# Save standardized datasets
# ------------------------------------------------------------

qs_output = CLEANED_DATA_DIR / "qs_2025_standardized.csv"
the_output = CLEANED_DATA_DIR / "the_2024_standardized.csv"
wur_output = CLEANED_DATA_DIR / "wur_2023_standardized.csv"

qs_clean.to_csv(qs_output, index=False)
the_clean.to_csv(the_output, index=False)
wur_clean.to_csv(wur_output, index=False)


# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

print("=" * 80)
print("UNIVERSITY STANDARDIZATION COMPLETED")
print("=" * 80)

print("\nQS records:", len(qs_clean))
print("THE records:", len(the_clean))
print("WUR identifiable records:", len(wur_clean))

print("\nFiles created:")

print(qs_output)
print(the_output)
print(wur_output)

print("\n" + "=" * 80)
print("STANDARDIZATION EXAMPLES")
print("=" * 80)

print("\nQS examples:")
print(
    qs_clean[
        [
            "University_Name_Original",
            "University_Name_Standard",
            "Country_Standard",
        ]
    ].head(10).to_string(index=False)
)

print("\nTHE examples:")
print(
    the_clean[
        [
            "University_Name_Original",
            "University_Name_Standard",
            "Country_Standard",
        ]
    ].head(10).to_string(index=False)
)

print("\nWUR examples:")
print(
    wur_clean[
        [
            "University_Name_Original",
            "University_Name_Standard",
            "Country_Standard",
        ]
    ].head(10).to_string(index=False)
)

print("\n" + "=" * 80)
print("RAW DATASETS WERE NOT MODIFIED")
print("=" * 80)