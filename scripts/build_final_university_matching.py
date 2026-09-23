# ============================================================
# EduVision_DV - Final University Matching Layer
# ============================================================
# Creates the authoritative three-way university matching table.
#
# Matching hierarchy:
#   1. Exact standardized name
#   2. Controlled validated alias
#   3. Normalized name
#   4. Review required
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
# 2. Load datasets
# ============================================================

# QS uses the validated-alias version so confirmed aliases
# participate in the final matching.
qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_alias_applied.csv"
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
# 3. Authoritative matching-key function
# ============================================================

def create_match_key(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    # Normalize Unicode characters.
    value = unicodedata.normalize("NFKD", value)

    # Convert accented characters to ASCII.
    value = value.encode("ascii", "ignore").decode("ascii")

    # Keep only letters and numbers.
    value = re.sub(r"[^a-z0-9]", "", value)

    return value


# ============================================================
# 4. Create matching keys
# ============================================================

for df in [qs, the, wur]:
    df["Match_Key"] = df["University_Name_Standard"].apply(
        create_match_key
    )


# ============================================================
# 5. Remove empty keys
# ============================================================

qs = qs[qs["Match_Key"] != ""].copy()
the = the[the["Match_Key"] != ""].copy()
wur = wur[wur["Match_Key"] != ""].copy()


# ============================================================
# 6. Build three-way matching intersection
# ============================================================

qs_keys = set(qs["Match_Key"])
the_keys = set(the["Match_Key"])
wur_keys = set(wur["Match_Key"])

three_way_keys = qs_keys & the_keys & wur_keys
three_way_keys.discard("")


# ============================================================
# 7. Build controlled alias lookup
# ============================================================

confirmed_aliases = aliases[
    aliases["Decision_Status"] == "CONFIRMED"
].copy()

alias_lookup = {}

for _, row in confirmed_aliases.iterrows():
    qs_key = create_match_key(row["QS_Name"])
    the_key = create_match_key(row["THE_Name"])
    alias_lookup[qs_key] = the_key


# ============================================================
# 8. Prepare representative records
# ============================================================

def representative(df):
    return (
        df[
            [
                "Match_Key",
                "University_Name_Original",
                "University_Name_Standard"
            ]
        ]
        .drop_duplicates("Match_Key")
    )


qs_rep = representative(qs).rename(
    columns={
        "University_Name_Original": "QS_Name",
        "University_Name_Standard": "QS_Standard"
    }
)

the_rep = representative(the).rename(
    columns={
        "University_Name_Original": "THE_Name",
        "University_Name_Standard": "THE_Standard"
    }
)

wur_rep = representative(wur).rename(
    columns={
        "University_Name_Original": "WUR_Name",
        "University_Name_Standard": "WUR_Standard"
    }
)


# ============================================================
# 9. Build final three-way table
# ============================================================

matches = pd.DataFrame({"Match_Key": sorted(three_way_keys)})

matches = matches.merge(qs_rep, on="Match_Key", how="left")
matches = matches.merge(the_rep, on="Match_Key", how="left")
matches = matches.merge(wur_rep, on="Match_Key", how="left")


# ============================================================
# 10. Classify matching method
# ============================================================

def classify(row):
    qs_standard = str(row["QS_Standard"])
    the_standard = str(row["THE_Standard"])
    wur_standard = str(row["WUR_Standard"])

    qs_key = row["Match_Key"]
    the_key = create_match_key(the_standard)
    wur_key = create_match_key(wur_standard)

    # Exact standardized-name match.
    if qs_standard == the_standard and qs_standard == wur_standard:
        return "EXACT"

    # Controlled alias match.
    if qs_key in alias_lookup and alias_lookup[qs_key] == the_key:
        return "CONTROLLED_ALIAS"

    # Normalized-name match.
    if qs_key == the_key and the_key == wur_key:
        return "NORMALIZED_NAME"

    # Anything unexpected.
    return "REVIEW_REQUIRED"


matches["Match_Method"] = matches.apply(classify, axis=1)


# ============================================================
# 11. Create authoritative University IDs
# ============================================================

matches = matches.sort_values("Match_Key").reset_index(drop=True)

matches["University_ID"] = [
    f"UNI_{i:04d}"
    for i in range(1, len(matches) + 1)
]


# ============================================================
# 12. Create preferred display name
# ============================================================

matches["University_Name"] = (
    matches["QS_Name"]
    .fillna(matches["THE_Name"])
    .fillna(matches["WUR_Name"])
)


# ============================================================
# 13. Reorder final columns
# ============================================================

matches = matches[
    [
        "University_ID",
        "University_Name",
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
# 14. Save authoritative matching table
# ============================================================

output_file = CLEANED_DATA_DIR / "university_master_final.csv"
matches.to_csv(output_file, index=False)


# ============================================================
# 15. Save method-specific audit files
# ============================================================

matches[matches["Match_Method"] == "CONTROLLED_ALIAS"].to_csv(
    CLEANED_DATA_DIR / "controlled_alias_matches.csv",
    index=False
)

matches[matches["Match_Method"] == "NORMALIZED_NAME"].to_csv(
    CLEANED_DATA_DIR / "normalized_name_matches.csv",
    index=False
)

matches[matches["Match_Method"] == "REVIEW_REQUIRED"].to_csv(
    CLEANED_DATA_DIR / "review_required_matches.csv",
    index=False
)


# ============================================================
# 16. Display final validation
# ============================================================

counts = matches["Match_Method"].value_counts()

print("=" * 80)
print("AUTHORITATIVE UNIVERSITY MATCHING")
print("=" * 80)

print(f"\nFinal three-way universities: {len(matches)}")

print("\nMatch methods:")

for method in [
    "EXACT",
    "CONTROLLED_ALIAS",
    "NORMALIZED_NAME",
    "REVIEW_REQUIRED"
]:
    print(f"{method}: {counts.get(method, 0)}")


# ============================================================
# 17. Display review-required records
# ============================================================

review = matches[matches["Match_Method"] == "REVIEW_REQUIRED"]

print("\n" + "=" * 80)
print("REVIEW REQUIRED")
print("=" * 80)

if review.empty:
    print("\nNo review-required matches.")
else:
    print(
        review[
            ["University_ID", "QS_Name", "THE_Name", "WUR_Name"]
        ].to_string(index=False)
    )


# ============================================================
# 18. Display output files
# ============================================================

print("\n" + "=" * 80)
print("FILES CREATED")
print("=" * 80)

print(output_file)
print(CLEANED_DATA_DIR / "controlled_alias_matches.csv")
print(CLEANED_DATA_DIR / "normalized_name_matches.csv")
print(CLEANED_DATA_DIR / "review_required_matches.csv")

print("\n" + "=" * 80)
print("FINAL UNIVERSITY MATCHING COMPLETED")
print("=" * 80)
