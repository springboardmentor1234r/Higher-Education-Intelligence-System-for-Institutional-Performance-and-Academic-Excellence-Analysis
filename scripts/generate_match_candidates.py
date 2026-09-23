# ============================================================
# EduVision_DV - University Match Candidate Generation
# ============================================================
# Generates possible matches using:
#   1. University name similarity
#   2. Country agreement
#
# IMPORTANT:
# This does NOT automatically merge universities.
# It only creates candidates for validation.
# ============================================================

import pandas as pd
import re
from pathlib import Path
from difflib import SequenceMatcher


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_standardized.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_standardized.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_standardized.csv"
)


# ------------------------------------------------------------
# Keep valid university names
# ------------------------------------------------------------

qs = qs[qs["University_Name_Standard"].notna()].copy()
the = the[the["University_Name_Standard"].notna()].copy()
wur = wur[wur["University_Name_Standard"].notna()].copy()


# ------------------------------------------------------------
# Remove exact matches
# ------------------------------------------------------------

the_names = set(the["University_Name_Standard"])
wur_names = set(wur["University_Name_Standard"])


qs_unmatched = qs[
    ~qs["University_Name_Standard"].isin(the_names)
].copy()


# ------------------------------------------------------------
# Similarity function
# ------------------------------------------------------------

def similarity(name1, name2):
    return SequenceMatcher(
        None,
        str(name1),
        str(name2)
    ).ratio()


# ------------------------------------------------------------
# Generate QS → THE candidates
# ------------------------------------------------------------

candidates = []

for _, qs_row in qs_unmatched.iterrows():

    qs_name = qs_row["University_Name_Standard"]
    qs_country = qs_row["Country_Standard"]

    # Compare only universities from the same country
    country_matches = the[
        the["Country_Standard"] == qs_country
    ]

    for _, the_row in country_matches.iterrows():

        the_name = the_row["University_Name_Standard"]

        score = similarity(qs_name, the_name)

        # Keep reasonably similar candidates
        if score >= 0.65:

            candidates.append(
                {
                    "QS_Name": qs_row["University_Name_Original"],
                    "QS_Standard": qs_name,
                    "Country": qs_country,
                    "THE_Name": the_row["University_Name_Original"],
                    "THE_Standard": the_name,
                    "Similarity": round(score, 3),
                }
            )


# ------------------------------------------------------------
# Convert candidates to DataFrame
# ------------------------------------------------------------

candidate_df = pd.DataFrame(candidates)


# ------------------------------------------------------------
# Sort by similarity
# ------------------------------------------------------------

if not candidate_df.empty:

    candidate_df = candidate_df.sort_values(
        by=["Similarity", "Country"],
        ascending=[False, True]
    )


# ------------------------------------------------------------
# Save candidates
# ------------------------------------------------------------

output_file = (
    CLEANED_DATA_DIR /
    "qs_the_match_candidates.csv"
)

candidate_df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------

print("=" * 80)
print("QS → THE MATCH CANDIDATE GENERATION")
print("=" * 80)

print(
    f"\nUnmatched QS universities checked: "
    f"{len(qs_unmatched)}"
)

print(
    f"Candidate matches generated: "
    f"{len(candidate_df)}"
)

print(
    f"\nCandidate file created:\n"
    f"{output_file}"
)


print("\n" + "=" * 80)
print("TOP CANDIDATE MATCHES")
print("=" * 80)

if candidate_df.empty:

    print("No candidates found.")

else:

    print(
        candidate_df.head(30).to_string(
            index=False
        )
    )


print("\n" + "=" * 80)
print("CANDIDATE GENERATION COMPLETED")
print("=" * 80)