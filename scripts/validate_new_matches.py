# ============================================================
# EduVision_DV - Validate Newly Created University Matches
# ============================================================
# Identifies universities that became present in all three
# datasets after Match_Key normalization.
#
# These are compared against the previous exact-name matching
# result so we can manually validate the newly linked records.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ============================================================
# 2. Load ID-enabled datasets
# ============================================================

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_with_ids.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_with_ids.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_with_ids.csv"
)


# ============================================================
# 3. Create University_ID sets
# ============================================================

qs_ids = set(qs["University_ID"].dropna())
the_ids = set(the["University_ID"].dropna())
wur_ids = set(wur["University_ID"].dropna())


# ============================================================
# 4. Find current three-way matches
# ============================================================

current_three_way = (
    qs_ids
    & the_ids
    & wur_ids
)


# ============================================================
# 5. Recreate the previous exact-name matching
# ============================================================

qs_standard = set(
    qs["University_Name_Standard_Before_Alias"]
    .dropna()
    .astype(str)
)

the_standard = set(
    the["University_Name_Standard"]
    .dropna()
    .astype(str)
)

wur_standard = set(
    wur["University_Name_Standard"]
    .dropna()
    .astype(str)
)


# ============================================================
# 6. Identify exact three-way matches
# ============================================================

exact_three_way_names = (
    qs_standard
    & the_standard
    & wur_standard
)


# ============================================================
# 7. Build a lookup from University_ID to names
# ============================================================

qs_lookup = (
    qs[
        [
            "University_ID",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Original":
                "QS_Original",
            "University_Name_Standard":
                "QS_Standard"
        }
    )
)

the_lookup = (
    the[
        [
            "University_ID",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Original":
                "THE_Original",
            "University_Name_Standard":
                "THE_Standard"
        }
    )
)

wur_lookup = (
    wur[
        [
            "University_ID",
            "University_Name_Original",
            "University_Name_Standard"
        ]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Original":
                "WUR_Original",
            "University_Name_Standard":
                "WUR_Standard"
        }
    )
)


# ============================================================
# 8. Combine names for current three-way matches
# ============================================================

three_way = pd.DataFrame(
    {"University_ID": sorted(current_three_way)}
)

three_way = three_way.merge(
    qs_lookup,
    on="University_ID",
    how="left"
)

three_way = three_way.merge(
    the_lookup,
    on="University_ID",
    how="left"
)

three_way = three_way.merge(
    wur_lookup,
    on="University_ID",
    how="left"
)


# ============================================================
# 9. Identify genuinely new matches
# ============================================================
# A match is considered "new" when the three datasets do not
# share the exact same standardized name.

three_way["Previously_Exact_Match"] = (
    three_way["QS_Standard"]
    == three_way["THE_Standard"]
) & (
    three_way["QS_Standard"]
    == three_way["WUR_Standard"]
)

new_matches = three_way[
    ~three_way["Previously_Exact_Match"]
].copy()


# ============================================================
# 10. Save review file
# ============================================================

review_file = (
    CLEANED_DATA_DIR /
    "new_three_way_matches_review.csv"
)

new_matches.to_csv(
    review_file,
    index=False
)


# ============================================================
# 11. Display results
# ============================================================

print("=" * 80)
print("NEW THREE-WAY MATCH VALIDATION")
print("=" * 80)

print(f"\nCurrent three-way matches: {len(current_three_way)}")
print(
    f"Potential newly linked matches: "
    f"{len(new_matches)}"
)

print("\n" + "=" * 80)
print("NEW MATCHES")
print("=" * 80)

if len(new_matches) > 0:
    print(
        new_matches[
            [
                "University_ID",
                "QS_Original",
                "THE_Original",
                "WUR_Original"
            ]
        ].to_string(index=False)
    )
else:
    print("\nNo new matches found.")


# ============================================================
# 12. Output file
# ============================================================

print("\n" + "=" * 80)
print("REVIEW FILE CREATED")
print("=" * 80)

print(review_file)

print("\n" + "=" * 80)
print("VALIDATION PREPARATION COMPLETED")
print("=" * 80)