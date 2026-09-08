import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# EduVision_DV - Module 3
# Education KPI Engineering
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "Milestone1" / "university_cleaned.csv"
OUTPUT_FILE = BASE_DIR / "Milestone2" / "university_final_dataset.xlsx"


# ============================================================
# 1. Load cleaned dataset
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("EduVision_DV - Module 3")
print("Education KPI Engineering")
print("=" * 70)

print("\nInput dataset:")
print("Rows   :", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. Convert KPI source fields to numeric
# ============================================================

numeric_columns = [
    "ranking_score",
    "overall_score",
    "citations_per_faculty_score",
    "citations_score",
    "research_score",
    "international_research_network_score",
    "student_staff_ratio",
    "international_student_percentage",
    "academic_reputation_score",
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# 3. KPI 1 - Global Ranking Score
# ============================================================
#
# Source:
# Module 2 ranking_score
#
# The ranking_score was already calculated from normalized_rank.
#
# Unit:
# 0-100 score
#
# Missing treatment:
# Preserve missing values.
#
# ============================================================

df["global_ranking_score"] = df["ranking_score"]


# ============================================================
# 4. KPI 2 - Research Impact Score
# ============================================================
#
# QS:
# Citations_per_Faculty_Score
#
# THE / WUR:
# citations_score
#
# These are related but not identical source measures.
# Therefore the source-specific value is used without
# pretending that the definitions are identical.
#
# Priority:
# 1. Citations per Faculty Score
# 2. Citations Score
#
# Unit:
# 0-100 score
#
# ============================================================

df["research_impact_score"] = (
    df["citations_per_faculty_score"]
    .combine_first(df["citations_score"])
)


# ============================================================
# 5. KPI 3 - Faculty-to-Student Ratio
# ============================================================
#
# Source:
# student_staff_ratio
#
# This represents students per staff.
#
# We keep the original ratio rather than converting a QS
# faculty/student score into a ratio.
#
# Unit:
# students per staff
#
# ============================================================

df["faculty_to_student_ratio"] = df["student_staff_ratio"]


# ============================================================
# 6. KPI 4 - International Student Percentage
# ============================================================
#
# Source:
# international_student_percentage
#
# Only an actual percentage is used.
#
# Unit:
# percentage
#
# ============================================================

df["international_student_percentage_kpi"] = (
    df["international_student_percentage"]
)


# ============================================================
# 7. KPI 5 - Academic Reputation Score
# ============================================================
#
# Source:
# academic_reputation_score
#
# QS provides this directly.
#
# Unit:
# 0-100 score
#
# ============================================================

df["academic_reputation_kpi"] = (
    df["academic_reputation_score"]
)


# ============================================================
# 8. Min-Max normalization helper
# ============================================================

def min_max_normalize(series):
    """
    Normalize a numeric series to a 0-100 scale.

    Missing values remain missing.
    """

    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(
            np.nan,
            index=series.index
        )

    if maximum == minimum:
        return pd.Series(
            100.0,
            index=series.index
        )

    return (
        (series - minimum)
        / (maximum - minimum)
        * 100
    )


# ============================================================
# 9. KPI 6 - Research Productivity Index
# ============================================================
#
# This is a DERIVED KPI.
#
# Research-related source indicators:
#
#   research_score
#   citations_score
#   citations_per_faculty_score
#   international_research_network_score
#
# Each available component is first normalized to 0-100.
#
# The final index is the mean of the available normalized
# research indicators.
#
# This avoids assigning an artificial zero to a missing
# research indicator.
#
# Formula:
#
# RPI =
# mean(
#     normalized research indicators available
# )
#
# ============================================================

research_components = {}

if "research_score" in df.columns:
    research_components["research_score"] = (
        min_max_normalize(df["research_score"])
    )

if "citations_score" in df.columns:
    research_components["citations_score"] = (
        min_max_normalize(df["citations_score"])
    )

if "citations_per_faculty_score" in df.columns:
    research_components["citations_per_faculty_score"] = (
        min_max_normalize(
            df["citations_per_faculty_score"]
        )
    )

if "international_research_network_score" in df.columns:
    research_components["international_research_network_score"] = (
        min_max_normalize(
            df["international_research_network_score"]
        )
    )


research_component_df = pd.DataFrame(
    research_components,
    index=df.index
)

df["research_productivity_index"] = (
    research_component_df
    .mean(axis=1, skipna=True)
    .round(2)
)


# ============================================================
# 10. KPI validation
# ============================================================

kpi_columns = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage_kpi",
    "academic_reputation_kpi",
    "research_productivity_index",
]

print("\n" + "=" * 70)
print("KPI VALIDATION")
print("=" * 70)

for column in kpi_columns:

    print("\n" + column)

    print(
        "Non-null:",
        df[column].notna().sum()
    )

    print(
        "Missing:",
        df[column].isna().sum()
    )

    if df[column].notna().any():

        print(
            "Min:",
            round(df[column].min(), 2)
        )

        print(
            "Max:",
            round(df[column].max(), 2)
        )


# ============================================================
# 11. Validate score-based KPIs
# ============================================================

score_kpis = [
    "global_ranking_score",
    "research_impact_score",
    "academic_reputation_kpi",
    "research_productivity_index",
]

print("\n" + "=" * 70)
print("SCORE RANGE VALIDATION")
print("=" * 70)

for column in score_kpis:

    invalid = df[
        (df[column] < 0) |
        (df[column] > 100)
    ][column].notna().sum()

    print(
        f"{column}: invalid values = {invalid}"
    )


# ============================================================
# 12. Validate percentage KPI
# ============================================================

percentage_column = (
    "international_student_percentage_kpi"
)

invalid_percentage = df[
    (df[percentage_column] < 0) |
    (df[percentage_column] > 100)
][percentage_column].notna().sum()

print(
    "\nInternational Student Percentage "
    f"invalid values = {invalid_percentage}"
)


# ============================================================
# 13. Validate ratio KPI
# ============================================================

invalid_ratio = df[
    df["faculty_to_student_ratio"] < 0
]["faculty_to_student_ratio"].notna().sum()

print(
    "Faculty-to-Student Ratio "
    f"invalid values = {invalid_ratio}"
)


# ============================================================
# 14. KPI metadata
# ============================================================

kpi_metadata = pd.DataFrame({

    "kpi": [
        "Global Ranking Score",
        "Research Impact Score",
        "Faculty-to-Student Ratio",
        "International Student Percentage",
        "Academic Reputation Score",
        "Research Productivity Index",
    ],

    "source": [
        "ranking_score from Module 2",
        "Citations per Faculty Score / Citations Score",
        "student_staff_ratio",
        "international_student_percentage",
        "academic_reputation_score",
        "Research Score + Citation indicators + Research Network",
    ],

    "formula": [
        "Existing Module 2 ranking_score",
        "Citations_per_Faculty_Score; fallback to citations_score",
        "Direct source value",
        "Direct source percentage",
        "Direct QS academic reputation score",
        "Mean of available min-max normalized research indicators",
    ],

    "unit": [
        "Score (0-100)",
        "Score (0-100)",
        "Students per staff",
        "Percentage",
        "Score (0-100)",
        "Index (0-100)",
    ],

    "normalization": [
        "Already normalized in Module 2",
        "Source score scale",
        "None",
        "None",
        "Source score scale",
        "Min-max normalization to 0-100",
    ],

    "missing_value_treatment": [
        "Preserved as missing",
        "Use available source indicator",
        "Preserved as missing",
        "Preserved as missing",
        "Preserved as missing",
        "Mean of available components; no missing component treated as zero",
    ],

    "interpretation": [
        "Higher score indicates stronger ranking position",
        "Higher score indicates stronger citation/research impact",
        "Students represented per staff member",
        "Share of students who are international",
        "Higher score indicates stronger academic reputation",
        "Higher index indicates stronger research performance across available indicators",
    ],
})


# ============================================================
# 15. Create Tableau-friendly KPI table
# ============================================================

kpi_columns_for_tableau = [
    "university_id",
    "university_name",
    "country_id",
    "country",
    "region",
    "source",
    "ranking_year",
    "global_rank",
    "normalized_rank",

    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage_kpi",
    "academic_reputation_kpi",
    "research_productivity_index",
]

kpi_table = df[
    [
        column
        for column in kpi_columns_for_tableau
        if column in df.columns
    ]
].copy()


# ============================================================
# 16. Create dimensional university table
# ============================================================

dim_university = (
    df[
        [
            "university_id",
            "university_name",
            "country_id",
            "country",
            "region",
        ]
    ]
    .drop_duplicates("university_id")
    .reset_index(drop=True)
)


# ============================================================
# 17. Create performance table
# ============================================================

performance_columns = [
    "university_id",
    "ranking_year",
    "source",
    "global_rank",
    "normalized_rank",
    "ranking_score",
    "global_ranking_score",
    "overall_score",
    "academic_reputation_score",
    "employer_reputation_score",
    "faculty_student_score",
]

performance_columns = [
    column
    for column in performance_columns
    if column in df.columns
]

fact_performance = df[
    performance_columns
].copy()


# ============================================================
# 18. Create research table
# ============================================================

research_columns = [
    "university_id",
    "ranking_year",
    "source",
    "research_score",
    "citations_score",
    "citations_per_faculty_score",
    "international_research_network_score",
    "research_impact_score",
    "research_productivity_index",
]

research_columns = [
    column
    for column in research_columns
    if column in df.columns
]

fact_research = df[
    research_columns
].copy()


# ============================================================
# 19. Create student table
# ============================================================

student_columns = [
    "university_id",
    "ranking_year",
    "source",
    "number_of_students",
    "student_staff_ratio",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "international_student_percentage_kpi",
    "female_percentage",
]

student_columns = [
    column
    for column in student_columns
    if column in df.columns
]

fact_student = df[
    student_columns
].copy()


# ============================================================
# 20. Final validation
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET VALIDATION")
print("=" * 70)

print("\nOriginal rows:", len(df))

print(
    "KPI table rows:",
    len(kpi_table)
)

print(
    "Unique universities:",
    df["university_id"].nunique()
)

print(
    "Duplicate rows:",
    df.duplicated().sum()
)

print("\nKPI columns:")

for column in kpi_columns:
    print(
        f"✓ {column}"
    )


# ============================================================
# 21. Export Excel workbook
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    kpi_table.to_excel(
        writer,
        sheet_name="kpi_summary",
        index=False
    )

    kpi_metadata.to_excel(
        writer,
        sheet_name="kpi_metadata",
        index=False
    )

    dim_university.to_excel(
        writer,
        sheet_name="dim_university",
        index=False
    )

    fact_performance.to_excel(
        writer,
        sheet_name="fact_performance",
        index=False
    )

    fact_research.to_excel(
        writer,
        sheet_name="fact_research",
        index=False
    )

    fact_student.to_excel(
        writer,
        sheet_name="fact_student",
        index=False
    )


print("\n" + "=" * 70)
print("MODULE 3 COMPLETED")
print("=" * 70)

print(
    "\nExcel file saved to:"
)

print(OUTPUT_FILE)