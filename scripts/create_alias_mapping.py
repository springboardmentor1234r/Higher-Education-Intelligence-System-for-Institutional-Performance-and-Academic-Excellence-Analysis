# ============================================================
# EduVision_DV - Controlled University Alias Mapping
# ============================================================
# Creates a manually validated alias mapping for university
# names that represent the same institution across datasets.
#
# IMPORTANT:
# Only explicitly validated mappings are included.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ------------------------------------------------------------
# Load review file
# ------------------------------------------------------------

review_file = (
    CLEANED_DATA_DIR /
    "university_match_review.csv"
)

review = pd.read_csv(review_file)


# ------------------------------------------------------------
# Explicit validation decisions
# ------------------------------------------------------------
# TRUE  = same university
# FALSE = different universities
#
# These decisions are based on the actual names shown in the
# review output, not on similarity score alone.
# ------------------------------------------------------------

decisions = {

    "Binghamton University SUNY":
        "SUNY Binghamton University",

    "University of North Carolina, Chapel Hill":
        "University of North Carolina at Chapel Hill",

    "Czech University of Life Sciences in Prague":
        "Czech University of Life Sciences Prague (CZU)",

    "King Fahd University of Petroleum & Minerals":
        "King Fahd University of Petroleum and Minerals",

    "The National University of Science and Technology MISIS":
        "National University of Science and Technology (MISiS)",

    "Imam Mohammad Ibn Saud Islamic University – IMSIU":
        "Imam Mohammad Ibn Saud Islamic University",

    "University Ulm":
        "Ulm University",

    "Thapar Institute of Engineering & Technology":
        "Thapar Institute of Engineering and Technology",

    "University of Rome \"Tor Vergata\"":
        "University of Rome II – Tor Vergata",

    "Jordan University of Science & Technology":
        "Jordan University of Science and Technology",

    "University of Texas El Paso":
        "University of Texas at El Paso",

    "National University of Sciences And Technology (NUST) Islamabad":
        "National University of Sciences and Technology",

    "Essex, University of":
        "University of Essex",

    # IMPORTANT:
    # Do NOT map Nanjing University of Science and Technology
    # to Nanjing University of Information Science and Technology.
    "Nanjing University of Science and Technology":
        None,

    "Johannes Kepler University Linz":
        "Johannes Kepler University of Linz",

    "University of Illinois at Chicago (UIC)":
        "University of Illinois Chicago",

    "Universidad Industrial de Santander - UIS":
        "Universidad Industrial de Santander (UIS)",

    "University of Naples Parthenope":
        "Parthenope University of Naples",

    "University of Texas Dallas":
        "University of Texas at Dallas",

    "KIT, Karlsruhe Institute of Technology":
        "Karlsruhe Institute of Technology",

    "University of New Brunswick":
        "University of New Brunswick UNB",
}


# ------------------------------------------------------------
# Apply decisions
# ------------------------------------------------------------

# ============================================================
# Apply validated alias decisions
# ============================================================
review["Match_Decision"] = review["QS_Name"].map(decisions)

# ============================================================
# Explicitly confirm Texas El Paso alias
# ============================================================
# Use a normalized text check so hidden whitespace or encoding
# differences do not prevent the confirmed alias from applying.

review.loc[
    review["QS_Name"].astype(str).str.strip().str.contains(
        "University of Texas El Paso",
        case=False,
        regex=False
    ),
    "Match_Decision"
] = "University of Texas at El Paso"

# ============================================================
# Set final decision status
# ============================================================
review["Decision_Status"] = review["Match_Decision"].apply(
    lambda x: "CONFIRMED" if pd.notna(x) else "REJECTED"
)

# ------------------------------------------------------------
# Convert decision into status
# ------------------------------------------------------------

review["Decision_Status"] = review[
    "Match_Decision"
].apply(
    lambda x: (
        "CONFIRMED"
        if pd.notna(x)
        else "REJECTED"
    )
)


# ------------------------------------------------------------
# Save alias mapping
# ------------------------------------------------------------

output_file = (
    CLEANED_DATA_DIR /
    "university_alias_mapping.csv"
)

review.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("=" * 80)
print("CONTROLLED UNIVERSITY ALIAS MAPPING")
print("=" * 80)

print(
    f"\nTotal reviewed candidates: {len(review)}"
)

print(
    "\nConfirmed matches:",
    (review["Decision_Status"] == "CONFIRMED").sum()
)

print(
    "Rejected matches:",
    (review["Decision_Status"] == "REJECTED").sum()
)


print("\n" + "=" * 80)
print("CONFIRMED ALIASES")
print("=" * 80)

confirmed = review[
    review["Decision_Status"] == "CONFIRMED"
]

print(
    confirmed[
        [
            "QS_Name",
            "THE_Name",
            "Country",
            "Similarity",
        ]
    ].to_string(index=False)
)


print("\n" + "=" * 80)
print("REJECTED / NOT AUTO-MATCHED")
print("=" * 80)

rejected = review[
    review["Decision_Status"] == "REJECTED"
]

print(
    rejected[
        [
            "QS_Name",
            "THE_Name",
            "Country",
            "Similarity",
        ]
    ].to_string(index=False)
)


print("\n" + "=" * 80)
print("FILE CREATED")
print("=" * 80)

print(output_file)

print("\n" + "=" * 80)
print("ALIAS MAPPING COMPLETED")
print("=" * 80)