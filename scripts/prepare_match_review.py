# ============================================================
# EduVision_DV - Prepare University Match Review
# ============================================================
# Extracts high-confidence QS -> THE candidates for manual
# validation before they are accepted as the same university.
#
# No university records are modified.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ------------------------------------------------------------
# Load best candidates
# ------------------------------------------------------------

input_file = (
    CLEANED_DATA_DIR /
    "qs_the_best_matches.csv"
)

df = pd.read_csv(input_file)


# ------------------------------------------------------------
# Select HIGH candidates
# ------------------------------------------------------------

review = df[
    df["Confidence"] == "HIGH"
].copy()


# ------------------------------------------------------------
# Add review column
# ------------------------------------------------------------

review["Match_Decision"] = ""


# ------------------------------------------------------------
# Reorder columns
# ------------------------------------------------------------

review = review[
    [
        "QS_Name",
        "QS_Standard",
        "THE_Name",
        "THE_Standard",
        "Country",
        "Similarity",
        "Confidence",
        "Match_Decision",
    ]
]


# ------------------------------------------------------------
# Save review file
# ------------------------------------------------------------

output_file = (
    CLEANED_DATA_DIR /
    "university_match_review.csv"
)

review.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# Print candidates
# ------------------------------------------------------------

print("=" * 80)
print("UNIVERSITY MATCH REVIEW")
print("=" * 80)

print(
    f"\nCandidates requiring review: "
    f"{len(review)}"
)

print("\n" + "=" * 80)
print("HIGH-CONFIDENCE CANDIDATES")
print("=" * 80)

print(
    review.to_string(index=False)
)

print("\n" + "=" * 80)
print("REVIEW FILE CREATED")
print("=" * 80)

print(output_file)

print("\n" + "=" * 80)
print("NEXT STEP")
print("=" * 80)

print(
    "\nReview Match_Decision before accepting "
    "any candidate as the same university."
)