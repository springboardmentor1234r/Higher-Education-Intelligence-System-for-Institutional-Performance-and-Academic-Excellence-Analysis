# ============================================================
# EduVision_DV - Final University Match Classification
# ============================================================
# Classifies three-way university matches using the ORIGINAL
# standardized datasets and the manually validated aliases.
#
# Match methods:
#   EXACT
#   CONTROLLED_ALIAS
#   NORMALIZED_NAME
#   REVIEW_REQUIRED
#
# This preserves the audit trail for the matching process.
# ============================================================

import pandas as pd
from pathlib import Path
import re
import unicodedata


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ============================================================
# 2. Load ORIGINAL standardized datasets
# ============================================================

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_standardized.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_standardized.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_standardized.csv"
)

aliases = pd.read_csv(
    CLEANED_DATA_DIR / "university_alias_mapping.csv"
)


# ============================================================
# 3. Create the same matching key used for University_ID
# ============================================================

def create_key(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()

    # Normalize Unicode characters.
    value = unicodedata.normalize("NFKD", value)

    # Remove non-ASCII remnants.
    value = value.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    # Keep only letters and numbers.
    value = re.sub(
        r"[^a-z0-9]",
        "",
        value
    )

    return value


# ============================================================
# 4. Add matching keys to original standardized datasets
# ============================================================

qs["Match_Key"] = (
    qs["University_Name_Standard"]
    .apply(create_key)
)

the["Match_Key"] = (
    the["University_Name_Standard"]
    .apply(create_key)
)

wur["Match_Key"] = (
    wur["University_Name_Standard"]
    .apply(create_key)
)


# ============================================================
# 5. Create three-way normalized matches
# ============================================================

qs_keys = set(
    qs["Match_Key"].dropna()
)

the_keys = set(
    the["Match_Key"].dropna()
)

wur_keys = set(
    wur["Match_Key"].dropna()
)

three_way_keys = (
    qs_keys
    & the_keys
    & wur_keys
)

three_way_keys.discard("")


# ============================================================
# 6. Prepare one record per matching key
# ============================================================

qs_info = (
    qs[
        [
            "Match_Key",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("Match_Key")
    .rename(
        columns={
            "University_Name_Original":
                "QS_Name",
            "University_Name_Standard":
                "QS_Standard"
        }
    )
)

the_info = (
    the[
        [
            "Match_Key",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("Match_Key")
    .rename(
        columns={
            "University_Name_Original":
                "THE_Name",
            "University_Name_Standard":
                "THE_Standard"
        }
    )
)

wur_info = (
    wur[
        [
            "Match_Key",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("Match_Key")
    .rename(
        columns={
            "University_Name_Original":
                "WUR_Name",
            "University_Name_Standard":
                "WUR_Standard"
        }
    )
)


# ============================================================
# 7. Combine the three datasets
# ============================================================

matches = pd.DataFrame(
    {
        "Match_Key": sorted(three_way_keys)
    }
)

matches = matches.merge(
    qs_info,
    on="Match_Key",
    how="left"
)

matches = matches.merge(
    the_info,
    on="Match_Key",
    how="left"
)

matches = matches.merge(
    wur_info,
    on="Match_Key",
    how="left"
)


# ============================================================
# 8. Build validated alias keys
# ============================================================

confirmed_aliases = aliases[
    aliases["Decision_Status"] == "CONFIRMED"
].copy()

confirmed_alias_keys = set()

for _, row in confirmed_aliases.iterrows():

    qs_key = create_key(
        row["QS_Name"]
    )

    the_key = create_key(
        row["THE_Name"]
    )

    confirmed_alias_keys.add(
        (qs_key, the_key)
    )


# ============================================================
# 9. Classify matching method
# ============================================================

def classify_match(row):

    qs_standard = str(
        row["QS_Standard"]
    )

    the_standard = str(
        row["THE_Standard"]
    )

    wur_standard = str(
        row["WUR_Standard"]
    )

    qs_key = create_key(
        qs_standard
    )

    the_key = create_key(
        the_standard
    )

    wur_key = create_key(
        wur_standard
    )

    # --------------------------------------------------------
    # EXACT
    # --------------------------------------------------------
    # Original standardized names are identical.

    if (
        qs_standard == the_standard
        and
        qs_standard == wur_standard
    ):
        return "EXACT"

    # --------------------------------------------------------
    # CONTROLLED_ALIAS
    # --------------------------------------------------------
    # The QS → THE relationship was explicitly validated.

    if (
        qs_key,
        the_key
    ) in confirmed_alias_keys:
        return "CONTROLLED_ALIAS"

    # --------------------------------------------------------
    # NORMALIZED_NAME
    # --------------------------------------------------------
    # Names become identical only after normalization.

    if (
        qs_key == the_key
        and
        the_key == wur_key
    ):
        return "NORMALIZED_NAME"

    # --------------------------------------------------------
    # REVIEW_REQUIRED
    # --------------------------------------------------------

    return "REVIEW_REQUIRED"


matches["Match_Method"] = matches.apply(
    classify_match,
    axis=1
)


# ============================================================
# 10. Assign final University IDs
# ============================================================

matches = matches.sort_values(
    "Match_Key"
).reset_index(drop=True)

matches["University_ID"] = [
    f"UNI_{i:04d}"
    for i in range(
        1,
        len(matches) + 1
    )
]


# ============================================================
# 11. Reorder columns
# ============================================================

matches = matches[
    [
        "University_ID",
        "Match_Key",
        "Match_Method",
        "QS_Name",
        "THE_Name",
        "WUR_Name",
        "QS_Standard",
        "THE_Standard",
        "WUR_Standard"
    ]
]


# ============================================================
# 12. Save final validation table
# ============================================================

output_file = (
    CLEANED_DATA_DIR /
    "university_match_validation.csv"
)

matches.to_csv(
    output_file,
    index=False
)


# ============================================================
# 13. Display classification summary
# ============================================================

counts = (
    matches["Match_Method"]
    .value_counts()
)

print("=" * 80)
print("FINAL UNIVERSITY MATCH CLASSIFICATION")
print("=" * 80)

print(
    f"\nTotal three-way matches: "
    f"{len(matches)}"
)

print("\nMatch methods:")

for method in [
    "EXACT",
    "CONTROLLED_ALIAS",
    "NORMALIZED_NAME",
    "REVIEW_REQUIRED"
]:

    print(
        f"{method}: "
        f"{counts.get(method, 0)}"
    )


# ============================================================
# 14. Display review-required records
# ============================================================

review = matches[
    matches["Match_Method"]
    == "REVIEW_REQUIRED"
]

print("\n" + "=" * 80)
print("REVIEW REQUIRED")
print("=" * 80)

if review.empty:

    print("\nNo review-required matches.")

else:

    print(
        review[
            [
                "University_ID",
                "QS_Name",
                "THE_Name",
                "WUR_Name"
            ]
        ].to_string(index=False)
    )


# ============================================================
# 15. Display output
# ============================================================

print("\n" + "=" * 80)
print("FILE CREATED")
print("=" * 80)

print(output_file)

print("\n" + "=" * 80)
print("FINAL MATCH CLASSIFICATION COMPLETED")
print("=" * 80)