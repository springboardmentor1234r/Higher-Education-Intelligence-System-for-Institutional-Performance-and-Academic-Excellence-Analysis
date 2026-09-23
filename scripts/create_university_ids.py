# ============================================================
# EduVision_DV - Create University IDs
# ============================================================
# Creates a stable University_ID for universities appearing
# across QS, THE, and WUR datasets.
#
# Exact standardized names are used first.
# Manually validated aliases are then linked using the
# controlled alias mapping.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ============================================================
# 2. Load the alias-applied datasets
# ============================================================

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_alias_applied.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_alias_applied.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_alias_applied.csv"
)

aliases = pd.read_csv(
    CLEANED_DATA_DIR / "university_alias_mapping.csv"
)


# ============================================================
# 3. Create normalized matching keys
# ============================================================
# These keys are used only for matching.
# They are NOT displayed as the final university name.

def create_key(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r"[^a-z0-9]+", "", regex=True)
    )


qs["Match_Key"] = create_key(
    qs["University_Name_Standard"]
)

the["Match_Key"] = create_key(
    the["University_Name_Standard"]
)

wur["Match_Key"] = create_key(
    wur["University_Name_Standard"]
)


# ============================================================
# 4. Build the set of all university matching keys
# ============================================================

all_keys = sorted(
    set(qs["Match_Key"])
    | set(the["Match_Key"])
    | set(wur["Match_Key"])
)

# Remove empty keys
all_keys = [
    key for key in all_keys
    if key
]


# ============================================================
# 5. Create stable University IDs
# ============================================================

university_id_map = {
    key: f"UNI_{index:04d}"
    for index, key in enumerate(all_keys, start=1)
}


# ============================================================
# 6. Apply University IDs
# ============================================================

qs["University_ID"] = qs["Match_Key"].map(
    university_id_map
)

the["University_ID"] = the["Match_Key"].map(
    university_id_map
)

wur["University_ID"] = wur["Match_Key"].map(
    university_id_map
)


# ============================================================
# 7. Create the university master key table
# ============================================================

master_keys = pd.DataFrame(
    {
        "University_ID": [
            university_id_map[key]
            for key in all_keys
        ],
        "Match_Key": all_keys
    }
)


# ============================================================
# 8. Add representative university names
# ============================================================

qs_names = (
    qs[
        ["University_ID", "University_Name_Standard"]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Standard":
            "QS_University_Name"
        }
    )
)

the_names = (
    the[
        ["University_ID", "University_Name_Standard"]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Standard":
            "THE_University_Name"
        }
    )
)

wur_names = (
    wur[
        ["University_ID", "University_Name_Standard"]
    ]
    .drop_duplicates("University_ID")
    .rename(
        columns={
            "University_Name_Standard":
            "WUR_University_Name"
        }
    )
)


# ============================================================
# 9. Combine university names
# ============================================================

university_master = master_keys.merge(
    qs_names,
    on="University_ID",
    how="left"
)

university_master = university_master.merge(
    the_names,
    on="University_ID",
    how="left"
)

university_master = university_master.merge(
    wur_names,
    on="University_ID",
    how="left"
)


# ============================================================
# 10. Create a preferred display name
# ============================================================

university_master["University_Name"] = (
    university_master["QS_University_Name"]
    .fillna(
        university_master["THE_University_Name"]
    )
    .fillna(
        university_master["WUR_University_Name"]
    )
)


# ============================================================
# 11. Add dataset presence indicators
# ============================================================

university_master["Has_QS"] = (
    university_master["QS_University_Name"]
    .notna()
)

university_master["Has_THE"] = (
    university_master["THE_University_Name"]
    .notna()
)

university_master["Has_WUR"] = (
    university_master["WUR_University_Name"]
    .notna()
)


# ============================================================
# 12. Save University Master table
# ============================================================

master_file = (
    CLEANED_DATA_DIR /
    "university_master.csv"
)

university_master.to_csv(
    master_file,
    index=False
)


# ============================================================
# 13. Save datasets with University_ID
# ============================================================

qs.to_csv(
    CLEANED_DATA_DIR /
    "qs_2025_with_ids.csv",
    index=False
)

the.to_csv(
    CLEANED_DATA_DIR /
    "the_2024_with_ids.csv",
    index=False
)

wur.to_csv(
    CLEANED_DATA_DIR /
    "wur_2023_with_ids.csv",
    index=False
)


# ============================================================
# 14. Calculate coverage
# ============================================================

total_universities = len(university_master)

all_three_count = (
    university_master[
        university_master["Has_QS"]
        & university_master["Has_THE"]
        & university_master["Has_WUR"]
    ]
    .shape[0]
)


# ============================================================
# 15. Display results
# ============================================================

print("=" * 80)
print("UNIVERSITY ID GENERATION")
print("=" * 80)

print(f"\nTotal unique University IDs: {total_universities}")

print(f"Universities in QS:  {qs['University_ID'].nunique()}")
print(f"Universities in THE: {the['University_ID'].nunique()}")
print(f"Universities in WUR: {wur['University_ID'].nunique()}")

print(
    f"\nUniversities present in all three datasets: "
    f"{all_three_count}"
)

print("\n" + "=" * 80)
print("FILES CREATED")
print("=" * 80)

print(master_file)
print(
    CLEANED_DATA_DIR /
    "qs_2025_with_ids.csv"
)
print(
    CLEANED_DATA_DIR /
    "the_2024_with_ids.csv"
)
print(
    CLEANED_DATA_DIR /
    "wur_2023_with_ids.csv"
)

print("\n" + "=" * 80)
print("UNIVERSITY ID GENERATION COMPLETED")
print("=" * 80)