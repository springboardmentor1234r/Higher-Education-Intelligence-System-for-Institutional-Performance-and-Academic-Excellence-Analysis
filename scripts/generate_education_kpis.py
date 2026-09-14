import pandas as pd
import numpy as np

# ============================================================
# MODULE 3 - EDUCATION KPI ENGINEERING
# ============================================================

INPUT_FILE = "data/processed/university_integrated_worldbank_education.csv"

OUTPUT_CSV = "data/processed/university_kpi_dataset.csv"

OUTPUT_EXCEL = "university_final_dataset.xlsx"


print("=" * 70)
print("MODULE 3 - EDUCATION KPI ENGINEERING")
print("=" * 70)


# ============================================================
# STEP 1 - LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("1. LOADING FINAL ANALYTICAL DATASET")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")


# ============================================================
# STEP 2 - CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "university_id",
    "university_name",
    "country_name",
    "country_code",
    "wb_region",
    "wb_income_group",

    # KPI 1
    "qs_overall_score",

    # KPI 2
    "qs_citations_per_faculty_score",

    # KPI 3
    "the_student_staff_ratio_2024",

    # KPI 4
    "the_international_students_pct_2024",

    # KPI 5
    "qs_academic_reputation_score",

    # KPI 6
    "the_research_score_2024",
    "the_citations_score_2024",
]


missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nERROR: Missing required columns:")
    for col in missing_columns:
        print(" -", col)
    raise SystemExit(1)

print("Required columns: PASS")


# ============================================================
# STEP 3 - CREATE KPI DATASET
# ============================================================

kpi = df[required_columns].copy()


# ============================================================
# STEP 4 - KPI 1
# GLOBAL RANKING SCORE
# ============================================================

print("\n" + "=" * 70)
print("2. KPI 1 - GLOBAL RANKING SCORE")
print("=" * 70)

kpi["global_ranking_score"] = kpi["qs_overall_score"]

print("Source: qs_overall_score")
print("Available:", kpi["global_ranking_score"].notna().sum())
print("Missing:", kpi["global_ranking_score"].isna().sum())


# ============================================================
# STEP 5 - KPI 2
# RESEARCH IMPACT SCORE
# ============================================================

print("\n" + "=" * 70)
print("3. KPI 2 - RESEARCH IMPACT SCORE")
print("=" * 70)

kpi["research_impact_score"] = (
    kpi["qs_citations_per_faculty_score"]
)

print("Source: qs_citations_per_faculty_score")
print("Available:", kpi["research_impact_score"].notna().sum())
print("Missing:", kpi["research_impact_score"].isna().sum())


# ============================================================
# STEP 6 - KPI 3
# STUDENT-TO-STAFF RATIO
# ============================================================

print("\n" + "=" * 70)
print("4. KPI 3 - FACULTY-TO-STUDENT RATIO")
print("=" * 70)

kpi["student_staff_ratio"] = (
    kpi["the_student_staff_ratio_2024"]
)

print("Source: the_student_staff_ratio_2024")
print("Measurement: Students per staff member")
print("Available:", kpi["student_staff_ratio"].notna().sum())
print("Missing:", kpi["student_staff_ratio"].isna().sum())


# ============================================================
# STEP 7 - NORMALIZED KPI 3 SCORE
# ============================================================

print("\nCreating normalized Faculty-to-Student Ratio score...")

ratio = kpi["student_staff_ratio"]

# Use percentile ranks.
# Lower student/staff ratio = better score.

kpi["faculty_student_ratio_score"] = (
    (1 - ratio.rank(pct=True, method="average")) * 100
)

# Preserve missing values.
kpi.loc[ratio.isna(), "faculty_student_ratio_score"] = np.nan

print("Normalization: Inverse percentile ranking")
print("Higher score = better staff availability")


# ============================================================
# STEP 8 - KPI 4
# INTERNATIONAL STUDENT PERCENTAGE
# ============================================================

print("\n" + "=" * 70)
print("5. KPI 4 - INTERNATIONAL STUDENT PERCENTAGE")
print("=" * 70)

kpi["international_student_percentage"] = (
    kpi["the_international_students_pct_2024"]
)

print("Source: the_international_students_pct_2024")
print("Available:", kpi["international_student_percentage"].notna().sum())
print("Missing:", kpi["international_student_percentage"].isna().sum())


# ============================================================
# STEP 9 - KPI 5
# ACADEMIC REPUTATION SCORE
# ============================================================

print("\n" + "=" * 70)
print("6. KPI 5 - ACADEMIC REPUTATION SCORE")
print("=" * 70)

kpi["academic_reputation_score"] = (
    kpi["qs_academic_reputation_score"]
)

print("Source: qs_academic_reputation_score")
print("Available:", kpi["academic_reputation_score"].notna().sum())
print("Missing:", kpi["academic_reputation_score"].isna().sum())


# ============================================================
# STEP 10 - KPI 6
# RESEARCH PRODUCTIVITY INDEX
# ============================================================

print("\n" + "=" * 70)
print("7. KPI 6 - RESEARCH PRODUCTIVITY INDEX")
print("=" * 70)

# Research components

qs_citations = kpi["qs_citations_per_faculty_score"]
the_research = kpi["the_research_score_2024"]
the_citations = kpi["the_citations_score_2024"]


# Count available components

component_count = (
    qs_citations.notna().astype(int)
    + the_research.notna().astype(int)
    + the_citations.notna().astype(int)
)


# Weighted values

weighted_sum = (
    qs_citations.fillna(0) * 0.40
    + the_research.fillna(0) * 0.35
    + the_citations.fillna(0) * 0.25
)


# Available weights

available_weight = (
    qs_citations.notna().astype(float) * 0.40
    + the_research.notna().astype(float) * 0.35
    + the_citations.notna().astype(float) * 0.25
)


# Calculate RPI using available components

kpi["research_productivity_index"] = (
    weighted_sum / available_weight
)


# Require at least 2 components

kpi.loc[
    component_count < 2,
    "research_productivity_index"
] = np.nan


print("Components:")
print(" - QS Citations per Faculty Score       : 40%")
print(" - THE Research Score                   : 35%")
print(" - THE Citations Score                  : 25%")

print(
    "Universities with at least 2 components:",
    (component_count >= 2).sum()
)

print(
    "Universities with insufficient components:",
    (component_count < 2).sum()
)


# ============================================================
# STEP 11 - SELECT FINAL COLUMNS
# ============================================================

final_columns = [
    "university_id",
    "university_name",
    "country_name",
    "country_code",
    "wb_region",
    "wb_income_group",

    "global_ranking_score",
    "research_impact_score",

    "student_staff_ratio",
    "faculty_student_ratio_score",

    "international_student_percentage",

    "academic_reputation_score",

    "research_productivity_index",
]

kpi_final = kpi[final_columns].copy()


# ============================================================
# STEP 12 - VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. KPI VALIDATION")
print("=" * 70)


print("\nFinal KPI dataset shape:")
print(kpi_final.shape)


# Check university IDs

print(
    "\nMissing university IDs:",
    kpi_final["university_id"].isna().sum()
)

print(
    "Duplicate university IDs:",
    kpi_final["university_id"].duplicated().sum()
)


# Check score ranges

score_columns = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_student_ratio_score",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]

print("\nKPI ranges:")

for col in score_columns:

    series = kpi_final[col].dropna()

    if len(series) > 0:
        print(
            f"{col:35s} "
            f"min={series.min():.2f} "
            f"max={series.max():.2f}"
        )


# Check invalid percentage

invalid_percentage = (
    (kpi_final["international_student_percentage"] < 0)
    |
    (kpi_final["international_student_percentage"] > 100)
).sum()

print(
    "\nInvalid international student percentages:",
    invalid_percentage
)


# ============================================================
# STEP 13 - SAVE CSV
# ============================================================

print("\n" + "=" * 70)
print("9. SAVING KPI DATASET")
print("=" * 70)

kpi_final.to_csv(
    OUTPUT_CSV,
    index=False
)

print("Saved:", OUTPUT_CSV)


# ============================================================
# STEP 14 - CREATE KPI DOCUMENTATION
# ============================================================

documentation = pd.DataFrame({

    "KPI": [
        "Global Ranking Score",
        "Research Impact Score",
        "Faculty-to-Student Ratio",
        "International Student Percentage",
        "Academic Reputation Score",
        "Research Productivity Index",
    ],

    "Source": [
        "QS 2025 - qs_overall_score",
        "QS 2025 - qs_citations_per_faculty_score",
        "THE 2024 - the_student_staff_ratio_2024",
        "THE 2024 - the_international_students_pct_2024",
        "QS 2025 - qs_academic_reputation_score",
        "QS Citations + THE Research + THE Citations",
    ],

    "Formula": [
        "QS Overall Score",
        "QS Citations per Faculty Score",
        "THE Student-to-Staff Ratio",
        "THE International Students Percentage",
        "QS Academic Reputation Score",
        "0.40*QS Citations + 0.35*THE Research + 0.25*THE Citations",
    ],

    "Unit": [
        "Score",
        "Score",
        "Students per staff member",
        "Percentage",
        "Score",
        "Index",
    ],

    "Normalization": [
        "Source scale",
        "Source scale",
        "Inverse percentile ranking",
        "Native 0-100 percentage",
        "Source scale",
        "Weighted composite, approximately 0-100",
    ],

    "Missing_Value_Treatment": [
        "Keep missing as NaN",
        "Keep missing as NaN",
        "Keep missing as NaN",
        "Keep missing as NaN",
        "Keep missing as NaN",
        "At least 2 of 3 components required",
    ],

    "Interpretation": [
        "Higher score indicates stronger overall QS performance",
        "Higher score indicates stronger citation impact",
        "Lower student/staff ratio indicates better staff availability",
        "Higher percentage indicates greater international student representation",
        "Higher score indicates stronger academic reputation",
        "Higher index indicates stronger combined research performance",
    ],
})


# ============================================================
# STEP 15 - CREATE EXCEL FILE
# ============================================================

print("\n" + "=" * 70)
print("10. CREATING TABLEAU-READY EXCEL FILE")
print("=" * 70)

with pd.ExcelWriter(
    OUTPUT_EXCEL,
    engine="openpyxl"
) as writer:

    kpi_final.to_excel(
        writer,
        sheet_name="University_KPIs",
        index=False
    )

    documentation.to_excel(
        writer,
        sheet_name="KPI_Documentation",
        index=False
    )


print("Saved:", OUTPUT_EXCEL)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MODULE 3 KPI ENGINEERING COMPLETED")
print("=" * 70)

print("\nFinal dataset:")
print("Rows:", len(kpi_final))
print("Columns:", len(kpi_final.columns))

print("\nFiles created:")
print("-", OUTPUT_CSV)
print("-", OUTPUT_EXCEL)

print("\nKPI columns:")
for col in [
    "global_ranking_score",
    "research_impact_score",
    "student_staff_ratio",
    "faculty_student_ratio_score",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]:
    print("-", col)

print("\nSTATUS: SUCCESS")
print("=" * 70)