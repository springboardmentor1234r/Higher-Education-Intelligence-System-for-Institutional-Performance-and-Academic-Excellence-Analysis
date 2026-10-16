# =====================================================================
# EduVision_DV — Milestone 2
# Module 3 — Education KPI Engineering
# generate_education_kpis.py
#
# PURPOSE:
#   Combine the already-calculated Six KPIs dataset with the
#   Module 2 University Overview dataset.
#
# IMPORTANT:
#   - Six KPI calculations are NOT changed here.
#   - Six KPIs.xlsx is treated as the source of KPI calculations.
#   - University matching is performed using standardized university
#     names because the two files use different university_id systems.
#   - The Module 2 university_id is used as the FINAL university_id.
#
# OUTPUT:
#   university_final_dataset.xlsx
# =====================================================================

import os
import re
import unicodedata
import pandas as pd


# =====================================================================
# 1. PATHS
# =====================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODULE_03_DIR = os.path.dirname(SCRIPT_DIR)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(MODULE_03_DIR)
)

# Module 2 cleaned data
INPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "Milestone_01",
    "Module_02",
    "deliverables",
    "university_cleaned"
)

# Master Module 2 dataset
MASTER_FILE = os.path.join(
    INPUT_DIR,
    "01 University Overview.xlsx"
)

# Already-calculated Six KPI dataset
SIX_KPIS_FILE = os.path.join(
    MODULE_03_DIR,
    "Six KPIs.xlsx"
)

# Final deliverable folder
DELIVERABLES_DIR = os.path.join(
    MODULE_03_DIR,
    "deliverables"
)

# Final output
OUTPUT_FILE = os.path.join(
    DELIVERABLES_DIR,
    "university_final_dataset.xlsx"
)

os.makedirs(
    DELIVERABLES_DIR,
    exist_ok=True
)


# =====================================================================
# 2. START
# =====================================================================

print("=" * 70)
print("EDUVISION_DV - MODULE 3: FINAL UNIVERSITY DATASET")
print("=" * 70)


# =====================================================================
# 3. CHECK INPUT FILES
# =====================================================================

print("\n" + "=" * 70)
print("STEP 1 — CHECK INPUT FILES")
print("=" * 70)

if not os.path.exists(MASTER_FILE):
    raise FileNotFoundError(
        f"01 University Overview.xlsx not found:\n{MASTER_FILE}"
    )

if not os.path.exists(SIX_KPIS_FILE):
    raise FileNotFoundError(
        f"Six KPIs.xlsx not found:\n{SIX_KPIS_FILE}"
    )

print("[OK] 01 University Overview.xlsx")
print("[OK] Six KPIs.xlsx")


# =====================================================================
# 4. LOAD DATA
# =====================================================================

print("\n" + "=" * 70)
print("STEP 2 — LOAD DATA")
print("=" * 70)

df_master = pd.read_excel(
    MASTER_FILE
)

df_kpi = pd.read_excel(
    SIX_KPIS_FILE
)

print(
    f"01 University Overview : {df_master.shape}"
)

print(
    f"Six KPIs              : {df_kpi.shape}"
)


# =====================================================================
# 5. CHECK REQUIRED COLUMNS
# =====================================================================

print("\n" + "=" * 70)
print("STEP 3 — CHECK REQUIRED COLUMNS")
print("=" * 70)

required_master = [
    "university_id",
    "university_name"
]

required_kpi = [
    "university_id",
    "university_name",
    "country_id",
    "country_name",
    "region",

    # Six KPIs
    "global_ranking_score",
    "academic_reputation_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "research_productivity_index"
]

for column in required_master:

    if column not in df_master.columns:
        raise KeyError(
            f"Missing column in 01 University Overview.xlsx: {column}"
        )

print("[OK] Master required columns")


for column in required_kpi:

    if column not in df_kpi.columns:
        raise KeyError(
            f"Missing column in Six KPIs.xlsx: {column}"
        )

print("[OK] Six KPI required columns")


# =====================================================================
# 6. STANDARDIZE UNIVERSITY NAMES
# =====================================================================
#
# The two datasets use different university_id systems.
#
# Module 2:
#     massachusetts institute of technology united states
#
# Six KPIs:
#     U0463
#
# Therefore university names are used ONLY as the matching bridge.
#
# The final university_id will come from Module 2.
# =====================================================================

print("\n" + "=" * 70)
print("STEP 4 — STANDARDIZE UNIVERSITY NAMES")
print("=" * 70)


def standardize_name(value):

    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    # -------------------------------------------------------------
    # Normalize Unicode characters.
    #
    # Example:
    # Šafárik → Safarik
    # Košice  → Kosice
    # -------------------------------------------------------------

    value = unicodedata.normalize(
        "NFKD",
        value
    )

    value = "".join(
        character
        for character in value
        if not unicodedata.combining(character)
    )

    # -------------------------------------------------------------
    # Remove punctuation.
    # -------------------------------------------------------------

    value = re.sub(
        r"[^\w\s]",
        " ",
        value
    )

    # -------------------------------------------------------------
    # Normalize whitespace.
    # -------------------------------------------------------------

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


df_master["_name_match"] = (
    df_master["university_name"]
    .apply(standardize_name)
)

df_kpi["_name_match"] = (
    df_kpi["university_name"]
    .apply(standardize_name)
)


# =====================================================================
# 7. SPECIAL NAME NORMALIZATION
# =====================================================================
#
# One known difference exists in the supplied datasets:
#
# Module 2:
#   Pavol Jozef afárik University in Koice
#
# Six KPIs:
#   Pavol Jozef Šafárik University in Košice
#
# Unicode normalization alone does not resolve this because the
# Module 2 dataset contains the text "afárik" / "Koice".
#
# We therefore apply a very small explicit correction for this
# documented source discrepancy.
#
# This does NOT change KPI calculations.
# It only allows the existing KPI record to match its Module 2
# university.
# =====================================================================

df_master["_name_match"] = (
    df_master["_name_match"]
    .str.replace(
        "afarik university in ko ice",
        "safarik university in kosice",
        regex=False
    )
)


# =====================================================================
# 8. CHECK NAME DUPLICATES
# =====================================================================

master_duplicate_names = (
    df_master["_name_match"]
    .duplicated()
    .sum()
)

kpi_duplicate_names = (
    df_kpi["_name_match"]
    .duplicated()
    .sum()
)

print(
    f"Duplicate standardized names in master : "
    f"{master_duplicate_names}"
)

print(
    f"Duplicate standardized names in KPI    : "
    f"{kpi_duplicate_names}"
)


if master_duplicate_names > 0:

    raise ValueError(
        "Duplicate standardized university names "
        "found in the master dataset."
    )


if kpi_duplicate_names > 0:

    raise ValueError(
        "Duplicate standardized university names "
        "found in Six KPIs.xlsx."
    )


# =====================================================================
# 9. CHECK MATCHING
# =====================================================================

print("\n" + "=" * 70)
print("STEP 5 — MATCH UNIVERSITIES")
print("=" * 70)

master_names = set(
    df_master["_name_match"]
)

kpi_names = set(
    df_kpi["_name_match"]
)

matched_names = (
    master_names
    .intersection(kpi_names)
)

unmatched_kpi_names = (
    kpi_names
    - master_names
)

print(
    f"Six KPI universities : {len(df_kpi):,}"
)

print(
    f"Matching universities : {len(matched_names):,}"
)

print(
    f"Unmatched KPI records : {len(unmatched_kpi_names):,}"
)


if len(unmatched_kpi_names) > 0:

    print(
        "\nWARNING: Some KPI universities did not match "
        "the Module 2 master dataset."
    )

    print(
        "\nFirst unmatched KPI universities:"
    )

    unmatched_rows = df_kpi[
        df_kpi["_name_match"].isin(
            unmatched_kpi_names
        )
    ][
        [
            "university_id",
            "university_name"
        ]
    ].head(20)

    print(
        unmatched_rows.to_string(
            index=False
        )
    )


# =====================================================================
# 10. INNER JOIN USING STANDARDIZED UNIVERSITY NAME
# =====================================================================

print("\n" + "=" * 70)
print("STEP 6 — MATCH KPI DATA TO MODULE 2 UNIVERSITIES")
print("=" * 70)

final_df = df_master.merge(
    df_kpi,
    on="_name_match",
    how="inner",
    suffixes=(
        "_master",
        "_kpi"
    )
)

print(
    f"Merged dataset shape: {final_df.shape}"
)


# =====================================================================
# 11. CREATE THE FINAL UNIVERSITY ID
# =====================================================================
#
# IMPORTANT:
#
# Module 2 is the project's canonical university ID system.
#
# Therefore:
#
#     final university_id
#             =
#     Module 2 university_id
#
# The KPI-side Uxxxx ID is preserved separately for traceability.
# =====================================================================

print("\n" + "=" * 70)
print("STEP 7 — CREATE FINAL UNIVERSITY ID")
print("=" * 70)

# Preserve the Module 2 ID
final_df["university_id"] = (
    final_df["university_id_master"]
)

# Preserve the KPI ID only as a traceability field
final_df["kpi_university_id"] = (
    final_df["university_id_kpi"]
)

print(
    "[OK] Module 2 university_id used as final university_id"
)

print(
    "[OK] KPI university_id preserved as kpi_university_id"
)


# =====================================================================
# 12. CLEAN DUPLICATE COLUMNS
# =====================================================================

columns_to_drop = [

    # Temporary matching column
    "_name_match",

    # Duplicate ID columns
    "university_id_master",
    "university_id_kpi",

    # KPI-side context columns.
    #
    # The Module 2 master version is retained.
    "university_name_kpi",
    "country_id_kpi",
    "country_name_kpi",
    "region_kpi"
]

columns_to_drop = [
    column
    for column in columns_to_drop
    if column in final_df.columns
]

if columns_to_drop:

    print(
        "\nRemoving duplicate/temporary columns:"
    )

    for column in columns_to_drop:
        print(
            f"  - {column}"
        )

    final_df = final_df.drop(
        columns=columns_to_drop
    )


# =====================================================================
# 13. FINAL COLUMN ORDER
# =====================================================================

print("\n" + "=" * 70)
print("STEP 8 — ORGANIZE FINAL DATASET")
print("=" * 70)

preferred_columns = [

    # -------------------------------------------------------------
    # University identity
    # -------------------------------------------------------------
    "university_id",
    "university_name",
    "kpi_university_id",

    # -------------------------------------------------------------
    # Country information
    # -------------------------------------------------------------
    "country_id",
    "country_name",
    "region",

    # -------------------------------------------------------------
    # Years
    # -------------------------------------------------------------
    "overview_year",
    "research_year",

    # -------------------------------------------------------------
    # KPI 1
    # -------------------------------------------------------------
    "global_ranking_score",
    "global_ranking_score_source",
    "overall_score_is_estimated",

    # -------------------------------------------------------------
    # KPI 5
    # -------------------------------------------------------------
    "academic_reputation_score",
    "academic_reputation_score_source",

    # -------------------------------------------------------------
    # KPI 2
    # -------------------------------------------------------------
    "research_impact_score",
    "research_impact_score_source",

    # -------------------------------------------------------------
    # KPI 3
    # -------------------------------------------------------------
    "faculty_to_student_ratio",
    "faculty_to_student_ratio_source",

    # -------------------------------------------------------------
    # KPI 4
    # -------------------------------------------------------------
    "international_student_percentage",
    "international_student_percentage_source",

    # -------------------------------------------------------------
    # KPI 6
    # -------------------------------------------------------------
    "research_productivity_index",
    "research_productivity_index_source"
]

existing_preferred = [
    column
    for column in preferred_columns
    if column in final_df.columns
]

remaining_columns = [
    column
    for column in final_df.columns
    if column not in existing_preferred
]

final_df = final_df[
    existing_preferred + remaining_columns
]

print(
    f"Final dataset columns organized: "
    f"{len(final_df.columns)}"
)


# =====================================================================
# 14. FINAL QA
# =====================================================================

print("\n" + "=" * 70)
print("STEP 9 — FINAL QA")
print("=" * 70)

duplicate_ids = (
    final_df["university_id"]
    .duplicated()
    .sum()
)

duplicate_rows = (
    final_df
    .duplicated()
    .sum()
)

missing_values = int(
    final_df
    .isna()
    .sum()
    .sum()
)

print(
    f"Final dataset rows       : "
    f"{len(final_df):,}"
)

print(
    f"Final dataset columns    : "
    f"{len(final_df.columns)}"
)

print(
    f"Duplicate university IDs : "
    f"{duplicate_ids}"
)

print(
    f"Duplicate complete rows  : "
    f"{duplicate_rows}"
)

print(
    f"Missing values           : "
    f"{missing_values}"
)


# =====================================================================
# 15. CHECK SIX KPI COLUMNS
# =====================================================================

print("\nSix KPIs:")

kpi_columns = [

    "global_ranking_score",

    "research_impact_score",

    "faculty_to_student_ratio",

    "international_student_percentage",

    "academic_reputation_score",

    "research_productivity_index"
]

for i, column in enumerate(
    kpi_columns,
    start=1
):

    missing_kpi = int(
        final_df[column]
        .isna()
        .sum()
    )

    print(
        f"{i}. {column} "
        f"| Missing: {missing_kpi}"
    )


# =====================================================================
# 16. QA VALIDATION
# =====================================================================

if duplicate_ids != 0:

    raise ValueError(
        "Duplicate university IDs found."
    )


if duplicate_rows != 0:

    raise ValueError(
        "Duplicate complete rows found."
    )


for column in kpi_columns:

    if column not in final_df.columns:

        raise ValueError(
            f"Required KPI column missing: {column}"
        )


# =====================================================================
# 17. SAVE FINAL DATASET
# =====================================================================

print("\n" + "=" * 70)
print("STEP 10 — SAVE FINAL DATASET")
print("=" * 70)

final_df.to_excel(
    OUTPUT_FILE,
    index=False
)

print(
    "\nuniversity_final_dataset.xlsx "
    "saved successfully:"
)

print(
    OUTPUT_FILE
)


# =====================================================================
# 18. COMPLETED
# =====================================================================

print("\n" + "=" * 70)
print("MODULE 3 — FINAL DATASET COMPLETED")
print("=" * 70)

print(
    f"\nUniversities: "
    f"{len(final_df):,}"
)

print(
    f"Columns: "
    f"{len(final_df.columns)}"
)

print(
    "\nCreated:"
)

print(
    "university_final_dataset.xlsx"
)

print("=" * 70)