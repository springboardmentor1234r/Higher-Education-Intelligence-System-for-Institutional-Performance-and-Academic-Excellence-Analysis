
import os
import pandas as pd
import numpy as np

PROJECT_PATH = "/content/drive/MyDrive/EduVision_DV"
CLEANED_PATH = os.path.join(PROJECT_PATH, "02_Cleaned_Data")
PROCESSED_PATH = os.path.join(PROJECT_PATH, "03_Processed_Data")

# Load Milestone 1 data
dim_university = pd.read_csv(
    os.path.join(PROCESSED_PATH, "dim_university.csv")
)

performance = pd.read_csv(
    os.path.join(PROCESSED_PATH, "fact_university_performance.csv")
)

student = pd.read_csv(
    os.path.join(PROCESSED_PATH, "fact_student.csv")
)

qs = pd.read_csv(
    os.path.join(CLEANED_PATH, "QS_2025_Cleaned.csv")
)

the = pd.read_csv(
    os.path.join(CLEANED_PATH, "THE_2024_Cleaned.csv")
)

# Base university dataset
final_df = dim_university[
    [
        "university_id",
        "university_name",
        "country_id",
        "country_name",
        "region"
    ]
].copy()

# ------------------------------------------------------------
# KPI 1: Global Ranking Score
# Source: QS 2025 Overall Score
# ------------------------------------------------------------

performance_kpi = performance[
    [
        "university_id",
        "overall_score",
        "academic_reputation"
    ]
].copy()

performance_kpi["overall_score"] = pd.to_numeric(
    performance_kpi["overall_score"],
    errors="coerce"
)

performance_kpi["academic_reputation"] = pd.to_numeric(
    performance_kpi["academic_reputation"],
    errors="coerce"
)

performance_kpi = performance_kpi.drop_duplicates("university_id")

final_df = final_df.merge(
    performance_kpi,
    on="university_id",
    how="left"
)

final_df.rename(
    columns={
        "overall_score": "global_ranking_score",
        "academic_reputation": "academic_reputation_score"
    },
    inplace=True
)

# ------------------------------------------------------------
# Standardize names for QS and THE matching
# ------------------------------------------------------------

def standardize_name(series):
    return (
        series.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )

dim_match = dim_university[
    ["university_id", "university_name"]
].copy()

dim_match["name_std"] = standardize_name(
    dim_match["university_name"]
)

# ------------------------------------------------------------
# KPI 2: Research Impact Score
# Source: QS 2025 Citations per Faculty Score
# ------------------------------------------------------------

qs["name_std"] = standardize_name(qs["Institution_Name"])

qs_kpi2 = qs[
    [
        "name_std",
        "Citations_per_Faculty_Score"
    ]
].copy()

qs_kpi2["Citations_per_Faculty_Score"] = pd.to_numeric(
    qs_kpi2["Citations_per_Faculty_Score"],
    errors="coerce"
)

qs_kpi2 = qs_kpi2.drop_duplicates("name_std")

qs_kpi2 = dim_match.merge(
    qs_kpi2,
    on="name_std",
    how="left"
)

final_df = final_df.merge(
    qs_kpi2[
        [
            "university_id",
            "Citations_per_Faculty_Score"
        ]
    ],
    on="university_id",
    how="left"
)

final_df.rename(
    columns={
        "Citations_per_Faculty_Score":
        "research_impact_score"
    },
    inplace=True
)

# ------------------------------------------------------------
# KPI 3 + KPI 4
# Source: WUR 2023
# ------------------------------------------------------------

student_kpi = student[
    [
        "university_id",
        "students_per_staff",
        "international_student_percentage"
    ]
].copy()

student_kpi["students_per_staff"] = pd.to_numeric(
    student_kpi["students_per_staff"],
    errors="coerce"
)

student_kpi["international_student_percentage"] = pd.to_numeric(
    student_kpi["international_student_percentage"],
    errors="coerce"
)

student_kpi = student_kpi.drop_duplicates("university_id")

final_df = final_df.merge(
    student_kpi,
    on="university_id",
    how="left"
)

final_df.rename(
    columns={
        "students_per_staff":
        "faculty_to_student_ratio"
    },
    inplace=True
)

# ------------------------------------------------------------
# KPI 6: Research Productivity Index
# Source: THE 2024
#
# Formula:
# 50% Research Score
# + 30% Citations Score
# + 20% International Outlook Score
# ------------------------------------------------------------

the["name_std"] = standardize_name(the["name"])

the_kpi6 = the[
    [
        "name_std",
        "scores_research",
        "scores_citations",
        "scores_international_outlook"
    ]
].copy()

for column in [
    "scores_research",
    "scores_citations",
    "scores_international_outlook"
]:
    the_kpi6[column] = pd.to_numeric(
        the_kpi6[column],
        errors="coerce"
    )

the_kpi6 = the_kpi6.drop_duplicates("name_std")

the_kpi6 = dim_match.merge(
    the_kpi6,
    on="name_std",
    how="left"
)

the_kpi6["research_productivity_index"] = (
    0.50 * the_kpi6["scores_research"]
    + 0.30 * the_kpi6["scores_citations"]
    + 0.20 * the_kpi6["scores_international_outlook"]
)

final_df = final_df.merge(
    the_kpi6[
        [
            "university_id",
            "research_productivity_index"
        ]
    ],
    on="university_id",
    how="left"
)

# ------------------------------------------------------------
# Years
# ------------------------------------------------------------

final_df["overview_year"] = 2025
final_df["research_year"] = 2024
final_df["student_year"] = 2023

# ------------------------------------------------------------
# Round KPI values
# ------------------------------------------------------------

kpi_columns = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_to_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index"
]

for column in kpi_columns:
    final_df[column] = pd.to_numeric(
        final_df[column],
        errors="coerce"
    ).round(2)

final_df = final_df.replace(
    [np.inf, -np.inf],
    np.nan
)

# ------------------------------------------------------------
# Save final KPI dataset
# ------------------------------------------------------------

output_file = os.path.join(
    PROCESSED_PATH,
    "university_final_dataset.xlsx"
)

final_df.to_excel(
    output_file,
    index=False
)

print("Education KPI dataset generated successfully.")
print("Universities:", len(final_df))
print("KPIs:", len(kpi_columns))
print("Output:", output_file)
