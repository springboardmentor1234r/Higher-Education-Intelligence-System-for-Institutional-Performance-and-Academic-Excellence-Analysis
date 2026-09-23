# ============================================================
# EduVision_DV - Best University Match Selection
# ============================================================
# Selects the strongest QS -> THE candidate for each QS
# university that currently has no exact name match.
#
# This does NOT approve the matches.
# It only reduces the candidate list for review.
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
# Load standardized datasets
# ------------------------------------------------------------

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_standardized.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_standardized.csv"
)


# ------------------------------------------------------------
# Keep valid names
# ------------------------------------------------------------

qs = qs[
    qs["University_Name_Standard"].notna()
].copy()

the = the[
    the["University_Name_Standard"].notna()
].copy()


# ------------------------------------------------------------
# Remove exact QS-THE matches
# ------------------------------------------------------------

the_names = set(
    the["University_Name_Standard"]
)

qs_unmatched = qs[
    ~qs["University_Name_Standard"].isin(the_names)
].copy()


# ------------------------------------------------------------
# Token-based similarity
# ------------------------------------------------------------

def token_similarity(name1, name2):

    tokens1 = set(
        re.findall(
            r"[a-z0-9]+",
            str(name1).lower()
        )
    )

    tokens2 = set(
        re.findall(
            r"[a-z0-9]+",
            str(name2).lower()
        )
    )

    if not tokens1 or not tokens2:
        return 0

    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)

    jaccard = intersection / union

    sequence = SequenceMatcher(
        None,
        str(name1),
        str(name2)
    ).ratio()

    # Combine both measurements
    return (
        0.6 * jaccard
        + 0.4 * sequence
    )


# ------------------------------------------------------------
# Generate best match for each QS university
# ------------------------------------------------------------

best_matches = []


for _, qs_row in qs_unmatched.iterrows():

    qs_name = qs_row[
        "University_Name_Standard"
    ]

    qs_country = qs_row[
        "Country_Standard"
    ]

    # Only compare universities from same country
    country_candidates = the[
        the["Country_Standard"] == qs_country
    ]

    best_score = 0
    best_row = None

    for _, the_row in country_candidates.iterrows():

        the_name = the_row[
            "University_Name_Standard"
        ]

        score = token_similarity(
            qs_name,
            the_name
        )

        if score > best_score:

            best_score = score
            best_row = the_row

    if best_row is not None:

        best_matches.append(
            {
                "QS_Name":
                    qs_row["University_Name_Original"],

                "QS_Standard":
                    qs_name,

                "Country":
                    qs_country,

                "THE_Name":
                    best_row[
                        "University_Name_Original"
                    ],

                "THE_Standard":
                    best_row[
                        "University_Name_Standard"
                    ],

                "Similarity":
                    round(best_score, 3),
            }
        )


# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

result = pd.DataFrame(best_matches)


# ------------------------------------------------------------
# Classify candidate confidence
# ------------------------------------------------------------

def classify(score):

    if score >= 0.85:
        return "HIGH"

    elif score >= 0.70:
        return "MEDIUM"

    else:
        return "LOW"


result["Confidence"] = (
    result["Similarity"]
    .apply(classify)
)


# ------------------------------------------------------------
# Sort strongest matches first
# ------------------------------------------------------------

result = result.sort_values(
    by="Similarity",
    ascending=False
)


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_file = (
    CLEANED_DATA_DIR /
    "qs_the_best_matches.csv"
)

result.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("=" * 80)
print("BEST QS → THE MATCH ANALYSIS")
print("=" * 80)

print(
    f"\nUnmatched QS universities: "
    f"{len(qs_unmatched)}"
)

print(
    f"Best candidates generated: "
    f"{len(result)}"
)


print("\n" + "=" * 80)
print("CONFIDENCE DISTRIBUTION")
print("=" * 80)

print(
    result["Confidence"]
    .value_counts()
    .to_string()
)


print("\n" + "=" * 80)
print("TOP 50 BEST CANDIDATES")
print("=" * 80)

print(
    result[
        [
            "QS_Name",
            "THE_Name",
            "Country",
            "Similarity",
            "Confidence",
        ]
    ]
    .head(50)
    .to_string(index=False)
)


print("\n" + "=" * 80)
print("FILE CREATED")
print("=" * 80)

print(output_file)


print("\n" + "=" * 80)
print("BEST MATCH ANALYSIS COMPLETED")
print("=" * 80)