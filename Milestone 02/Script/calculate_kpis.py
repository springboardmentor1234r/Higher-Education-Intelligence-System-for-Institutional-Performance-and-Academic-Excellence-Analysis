# ============================================================
# EduVision_DV - KPI Calculation
# ============================================================
# Creates the final KPI dataset from the university master
# dataset.
#
# The original master dataset is NOT modified.
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"


# ============================================================
# 2. Load the master dataset
# ============================================================

df = pd.read_csv(
    FINAL_DATA_DIR /
    "university_master_dataset.csv"
)


# ============================================================
# 3. Convert QS ranking to numeric
# ============================================================
# QS contains both individual ranks and ranking bands such as
# 661-670. For a band, use its midpoint.

def parse_qs_rank(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if "-" in value:
        parts = value.split("-")

        try:
            lower = float(parts[0])
            upper = float(parts[1])
            return (lower + upper) / 2
        except ValueError:
            return np.nan

    try:
        return float(value)
    except ValueError:
        return np.nan


df["QS_Rank_Numeric"] = (
    df["QS_RANK_2025"]
    .apply(parse_qs_rank)
)


# ============================================================
# 4. Calculate Global Ranking Score
# ============================================================
# Lower QS rank means stronger ranking.
#
# Formula:
#   100 * (max_rank - university_rank)
#   / (max_rank - minimum_rank)
#
# The result is scaled between 0 and 100.

min_rank = df["QS_Rank_Numeric"].min()
max_rank = df["QS_Rank_Numeric"].max()

df["Global_Ranking_Score"] = (
    100
    * (max_rank - df["QS_Rank_Numeric"])
    / (max_rank - min_rank)
)


# ============================================================
# 5. Calculate Research Impact Score
# ============================================================
# Research Quality comes from THE.
# Citation impact comes from WUR.
#
# Average only available components.

research_impact_columns = [
    "THE_Research_Quality",
    "WUR_Citations_Score"
]

df["Research_Impact_Score"] = (
    df[research_impact_columns]
    .mean(axis=1, skipna=True)
)


# ============================================================
# 6. Calculate Faculty-to-Student Ratio
# ============================================================
# Prefer THE because its field is directly named
# Students-to-Staff Ratio.
# Use WUR as fallback where THE is unavailable.

df["Faculty_to_Student_Ratio"] = (
    df["THE_Students_to_Staff_Ratio"]
    .fillna(
        df["WUR_No_of_student_per_staff"]
    )
)


# ============================================================
# 7. Convert international student percentages
# ============================================================

def parse_percentage(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    value = value.replace("%", "")

    try:
        return float(value)
    except ValueError:
        return np.nan


df["THE_International_Students_Numeric"] = (
    df["THE_International_Students"]
    .apply(parse_percentage)
)

df["WUR_International_Student_Numeric"] = (
    df["WUR_International_Student"]
    .apply(parse_percentage)
)


# ============================================================
# 8. Calculate International Student Percentage
# ============================================================
# Prefer THE and use WUR as fallback.

df["International_Student_Percentage"] = (
    df["THE_International_Students_Numeric"]
    .fillna(
        df["WUR_International_Student_Numeric"]
    )
)


# ============================================================
# 9. Calculate Academic Reputation Score
# ============================================================
# Directly sourced from QS.

df["Academic_Reputation_Score"] = (
    df["QS_Academic_Reputation_Score"]
)


# ============================================================
# 10. Calculate Research Productivity Index
# ============================================================
# Uses:
#   THE Research Environment
#   WUR Research Score
#
# Average only available values.

research_productivity_columns = [
    "THE_Research_Environment",
    "WUR_Research_Score"
]

df["Research_Productivity_Index"] = (
    df[research_productivity_columns]
    .mean(axis=1, skipna=True)
)


# ============================================================
# 11. Create KPI availability flags
# ============================================================

kpi_columns = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

for column in kpi_columns:

    df[f"{column}_Available"] = (
        df[column].notna()
    )


# ============================================================
# 12. Calculate overall KPI completeness
# ============================================================

df["KPI_Available_Count"] = (
    df[kpi_columns]
    .notna()
    .sum(axis=1)
)

df["KPI_Completeness_Percentage"] = (
    df["KPI_Available_Count"]
    / len(kpi_columns)
    * 100
)


# ============================================================
# 13. Round KPI values
# ============================================================

df["Global_Ranking_Score"] = (
    df["Global_Ranking_Score"]
    .round(2)
)

df["Research_Impact_Score"] = (
    df["Research_Impact_Score"]
    .round(2)
)

df["Faculty_to_Student_Ratio"] = (
    df["Faculty_to_Student_Ratio"]
    .round(2)
)

df["International_Student_Percentage"] = (
    df["International_Student_Percentage"]
    .round(2)
)

df["Academic_Reputation_Score"] = (
    df["Academic_Reputation_Score"]
    .round(2)
)

df["Research_Productivity_Index"] = (
    df["Research_Productivity_Index"]
    .round(2)
)


# ============================================================
# 14. Save KPI dataset
# ============================================================

output_file = (
    FINAL_DATA_DIR /
    "university_kpi_dataset.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 15. Print KPI validation
# ============================================================

print("=" * 80)
print("KPI DATASET CREATED")
print("=" * 80)

print(f"\nUniversities: {len(df)}")

print("\nKPI availability:")

for column in kpi_columns:

    available = df[column].notna().sum()

    percentage = (
        available
        / len(df)
        * 100
    )

    print(
        f"{column}: "
        f"{available}/{len(df)} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# 16. Display KPI summary statistics
# ============================================================

print("\n" + "=" * 80)
print("KPI SUMMARY")
print("=" * 80)

print(
    df[kpi_columns]
    .describe()
    .round(2)
    .to_string()
)


# ============================================================
# 17. Display sample KPI records
# ============================================================

print("\n" + "=" * 80)
print("SAMPLE KPI RECORDS")
print("=" * 80)

display_columns = [
    "University_ID",
    "University_Name",
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

print(
    df[display_columns]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 18. Completion message
# ============================================================

print("\n" + "=" * 80)
print("OUTPUT")
print("=" * 80)

print(output_file)

print("\nKPI CALCULATION COMPLETED")
print("=" * 80)