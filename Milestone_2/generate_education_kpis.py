"""
EduVision_DV - KPI Generation
Generates the clean Six KPI dataset from university_final_dataset1.csv.
"""

import pandas as pd
import numpy as np

INPUT_FILE = "data/cleaned/university_final_dataset1.csv"
OUTPUT_FILE = "data/cleaned/Six_KPI_Cleaned.csv"

# Read source data. latin1 safely handles the source CSV encoding.
df = pd.read_csv(INPUT_FILE, encoding="latin1")

# Convert KPI source columns to numeric.
numeric_cols = [
    "overall_score",
    "academic_reputation",
    "research_score_source",
    "citation_score_source",
    "faculty_to_student_ratio",
    "international_student_percentage",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Keep university/country identifiers and useful context columns.
kpi = df[
    [
        "university_id",
        "university_name",
        "country_id",
        "country_name",
        "region",
        "overview_year",
        "research_year",
    ]
].copy()

# KPI 1: Global Ranking Score
kpi["global_ranking_score"] = df["overall_score"]

# KPI 2: Research Impact Score
kpi["research_impact_score"] = df["citation_score_source"]

# KPI 3: Faculty-to-Student Ratio
# Source is students per staff, so convert to staff per 100 students.
students_per_staff = df["faculty_to_student_ratio"]
kpi["faculty_to_student_ratio"] = np.where(
    students_per_staff > 0,
    100 / students_per_staff,
    np.nan,
)

# KPI 4: International Student Percentage
kpi["international_student_percentage"] = (
    df["international_student_percentage"]
)

# KPI 5: Academic Reputation Score
kpi["academic_reputation_score"] = df["academic_reputation"]

# KPI 6: Research Productivity Index
# RPI = 0.5 * Research Score + 0.5 * Citation Score
research = df["research_score_source"]
citation = df["citation_score_source"]

kpi["research_productivity_index"] = np.where(
    research.notna() & citation.notna(),
    0.5 * research + 0.5 * citation,
    np.nan,
)

# Round KPI values to two decimal places.
kpi[
    [
        "global_ranking_score",
        "research_impact_score",
        "faculty_to_student_ratio",
        "international_student_percentage",
        "academic_reputation_score",
        "research_productivity_index",
    ]
] = kpi[
    [
        "global_ranking_score",
        "research_impact_score",
        "faculty_to_student_ratio",
        "international_student_percentage",
        "academic_reputation_score",
        "research_productivity_index",
    ]
].round(2)

# Missing values remain missing; they are not replaced with zero.
kpi.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"Created: {OUTPUT_FILE}")
print(f"Rows: {len(kpi)}")
