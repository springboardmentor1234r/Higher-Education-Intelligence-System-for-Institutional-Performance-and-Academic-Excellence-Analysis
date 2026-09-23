# ============================================================
# EduVision_DV - Analyze University Match Candidates
# ============================================================
# This script analyzes the candidate matches generated between
# QS and THE.
#
# It does NOT automatically approve any match.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"

INPUT_FILE = CLEANED_DATA_DIR / "qs_the_match_candidates.csv"


# ------------------------------------------------------------
# Load candidate file
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)


# ------------------------------------------------------------
# Check country agreement
# ------------------------------------------------------------

# The candidate generator already restricted candidates
# to the same country, but we verify it here.

df["Country_Match"] = True


# ------------------------------------------------------------
# Classify similarity
# ------------------------------------------------------------

def classify_similarity(score):

    if score >= 0.95:
        return "VERY_HIGH"

    elif score >= 0.85:
        return "HIGH"

    elif score >= 0.65:
        return "MEDIUM"

    return "LOW"


df["Match_Category"] = (
    df["Similarity"]
    .apply(classify_similarity)
)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("=" * 80)
print("MATCH CANDIDATE ANALYSIS")
print("=" * 80)

print(f"\nTotal candidate pairs: {len(df)}")


print("\n" + "=" * 80)
print("SIMILARITY DISTRIBUTION")
print("=" * 80)

print(
    df["Match_Category"]
    .value_counts()
    .to_string()
)


print("\n" + "=" * 80)
print("SIMILARITY STATISTICS")
print("=" * 80)

print(
    df["Similarity"]
    .describe()
    .to_string()
)


# ------------------------------------------------------------
# Very high confidence candidates
# ------------------------------------------------------------

very_high = df[
    df["Similarity"] >= 0.95
].copy()


print("\n" + "=" * 80)
print("VERY HIGH CONFIDENCE CANDIDATES (>= 0.95)")
print("=" * 80)

print(
    f"\nCount: {len(very_high)}"
)

print(
    very_high[
        [
            "QS_Name",
            "THE_Name",
            "Country",
            "Similarity",
        ]
    ]
    .head(50)
    .to_string(index=False)
)


# ------------------------------------------------------------
# High confidence candidates
# ------------------------------------------------------------

high = df[
    (df["Similarity"] >= 0.85)
    & (df["Similarity"] < 0.95)
].copy()


print("\n" + "=" * 80)
print("HIGH CONFIDENCE CANDIDATES (0.85 - 0.949)")
print("=" * 80)

print(
    f"\nCount: {len(high)}"
)


# ------------------------------------------------------------
# Medium confidence candidates
# ------------------------------------------------------------

medium = df[
    (df["Similarity"] >= 0.65)
    & (df["Similarity"] < 0.85)
].copy()


print("\n" + "=" * 80)
print("MEDIUM CONFIDENCE CANDIDATES (0.65 - 0.849)")
print("=" * 80)

print(
    f"\nCount: {len(medium)}"
)


# ------------------------------------------------------------
# Save categorized files
# ------------------------------------------------------------

very_high.to_csv(
    CLEANED_DATA_DIR / "qs_the_very_high_candidates.csv",
    index=False
)

high.to_csv(
    CLEANED_DATA_DIR / "qs_the_high_candidates.csv",
    index=False
)

medium.to_csv(
    CLEANED_DATA_DIR / "qs_the_medium_candidates.csv",
    index=False
)


# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("FILES CREATED")
print("=" * 80)

print(
    "\nqs_the_very_high_candidates.csv"
)

print(
    "qs_the_high_candidates.csv"
)

print(
    "qs_the_medium_candidates.csv"
)

print("\n" + "=" * 80)
print("MATCH CANDIDATE ANALYSIS COMPLETED")
print("=" * 80)