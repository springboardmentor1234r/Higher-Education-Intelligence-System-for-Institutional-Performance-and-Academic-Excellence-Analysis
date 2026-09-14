import os
import pandas as pd


# ============================================================
# EDUVISION - FINAL DATA MODEL
# ============================================================

print("=" * 70)
print("FINAL DATA MODEL CREATION")
print("=" * 70)


# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

SOURCE_FILE = "data/processed/university_integrated_worldbank_education.csv"
KPI_FILE = "data/processed/university_kpi_dataset.csv"
OUTPUT_DIR = "data/processed/model"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. LOADING SOURCE DATA")
print("=" * 70)

df = pd.read_csv(SOURCE_FILE)
kpi = pd.read_csv(KPI_FILE)

print(f"Integrated dataset shape: {df.shape}")
print(f"KPI dataset shape: {kpi.shape}")


# ------------------------------------------------------------
# 3. REQUIRED COLUMNS
# ------------------------------------------------------------

required_source = [
    "university_id",
    "university_name",
    "country_name",
    "country_code",
    "country_name_canonical",
    "wb_country_code",
    "wb_region",
    "wb_income_group",
]

for col in required_source:
    if col not in df.columns:
        raise ValueError(f"Missing required source column: {col}")

print("Required source columns: PASS")


# ============================================================
# 4. UNIVERSITY DIMENSION
# ============================================================

print("\n" + "=" * 70)
print("2. CREATING dim_university")
print("=" * 70)

dim_university = (
    df[
        [
            "university_id",
            "university_name",
            "country_code",
            "country_name",
            "country_name_canonical",
            "wb_country_code",
            "wb_region",
            "wb_income_group",
        ]
    ]
    .drop_duplicates(subset=["university_id"])
    .copy()
)

dim_university.to_csv(
    f"{OUTPUT_DIR}/dim_university.csv",
    index=False
)

print(f"Rows: {len(dim_university)}")
print("Saved: dim_university.csv")


# ============================================================
# 5. UNIVERSITY PERFORMANCE FACT
# ============================================================

print("\n" + "=" * 70)
print("3. CREATING fact_university_performance")
print("=" * 70)

performance_frames = []


# -------------------------
# QS 2025
# -------------------------

qs = df[
    [
        "university_id",
        "qs_rank_2025",
        "qs_overall_score",
        "qs_academic_reputation_score",
        "qs_employer_reputation_score",
    ]
].copy()

qs["year"] = 2025
qs["ranking_source"] = "QS"

qs = qs.rename(
    columns={
        "qs_rank_2025": "global_rank",
        "qs_overall_score": "overall_score",
        "qs_academic_reputation_score": "academic_reputation",
        "qs_employer_reputation_score": "employer_reputation",
    }
)

performance_frames.append(
    qs[
        [
            "university_id",
            "year",
            "ranking_source",
            "global_rank",
            "overall_score",
            "academic_reputation",
            "employer_reputation",
        ]
    ]
)


# -------------------------
# THE 2024
# -------------------------

the24 = df[
    [
        "university_id",
        "the_rank_2024",
        "the_overall_score_2024",
    ]
].copy()

the24["year"] = 2024
the24["ranking_source"] = "THE"

the24 = the24.rename(
    columns={
        "the_rank_2024": "global_rank",
        "the_overall_score_2024": "overall_score",
    }
)

the24["academic_reputation"] = pd.NA
the24["employer_reputation"] = pd.NA

performance_frames.append(
    the24[
        [
            "university_id",
            "year",
            "ranking_source",
            "global_rank",
            "overall_score",
            "academic_reputation",
            "employer_reputation",
        ]
    ]
)


# -------------------------
# THE 2023
# -------------------------

the23 = df[
    [
        "university_id",
        "the_rank_2023",
        "the_overall_score_2023",
    ]
].copy()

the23["year"] = 2023
the23["ranking_source"] = "THE"

the23 = the23.rename(
    columns={
        "the_rank_2023": "global_rank",
        "the_overall_score_2023": "overall_score",
    }
)

the23["academic_reputation"] = pd.NA
the23["employer_reputation"] = pd.NA

performance_frames.append(
    the23[
        [
            "university_id",
            "year",
            "ranking_source",
            "global_rank",
            "overall_score",
            "academic_reputation",
            "employer_reputation",
        ]
    ]
)


fact_performance = pd.concat(
    performance_frames,
    ignore_index=True
)

fact_performance.to_csv(
    f"{OUTPUT_DIR}/fact_university_performance.csv",
    index=False
)

print(f"Rows: {len(fact_performance)}")
print("Saved: fact_university_performance.csv")


# ============================================================
# 6. RESEARCH FACT
# ============================================================

print("\n" + "=" * 70)
print("4. CREATING fact_research")
print("=" * 70)

research_frames = []


# QS 2025
research_qs = df[
    [
        "university_id",
        "qs_citations_per_faculty_score",
    ]
].copy()

research_qs["year"] = 2025
research_qs["ranking_source"] = "QS"
research_qs["research_score"] = pd.NA
research_qs["citation_score"] = pd.NA
research_qs["research_impact"] = research_qs[
    "qs_citations_per_faculty_score"
]
research_qs["research_productivity"] = pd.NA

research_qs = research_qs[
    [
        "university_id",
        "year",
        "ranking_source",
        "research_score",
        "citation_score",
        "research_impact",
        "research_productivity",
    ]
]

research_frames.append(research_qs)


# THE 2024
research_the24 = df[
    [
        "university_id",
        "the_research_score_2024",
        "the_citations_score_2024",
    ]
].copy()

research_the24["year"] = 2024
research_the24["ranking_source"] = "THE"
research_the24["research_score"] = research_the24[
    "the_research_score_2024"
]
research_the24["citation_score"] = research_the24[
    "the_citations_score_2024"
]
research_the24["research_impact"] = pd.NA
research_the24["research_productivity"] = pd.NA

research_the24 = research_the24[
    [
        "university_id",
        "year",
        "ranking_source",
        "research_score",
        "citation_score",
        "research_impact",
        "research_productivity",
    ]
]

research_frames.append(research_the24)


# THE 2023
research_the23 = df[
    [
        "university_id",
        "the_research_score_2023",
        "the_citations_score_2023",
    ]
].copy()

research_the23["year"] = 2023
research_the23["ranking_source"] = "THE"
research_the23["research_score"] = research_the23[
    "the_research_score_2023"
]
research_the23["citation_score"] = research_the23[
    "the_citations_score_2023"
]
research_the23["research_impact"] = pd.NA
research_the23["research_productivity"] = pd.NA

research_the23 = research_the23[
    [
        "university_id",
        "year",
        "ranking_source",
        "research_score",
        "citation_score",
        "research_impact",
        "research_productivity",
    ]
]

research_frames.append(research_the23)


fact_research = pd.concat(
    research_frames,
    ignore_index=True
)

fact_research.to_csv(
    f"{OUTPUT_DIR}/fact_research.csv",
    index=False
)

print(f"Rows: {len(fact_research)}")
print("Saved: fact_research.csv")


# ============================================================
# 7. STUDENT FACT
# ============================================================

print("\n" + "=" * 70)
print("5. CREATING fact_student")
print("=" * 70)

student_frames = []


# THE 2024
student24 = df[
    [
        "university_id",
        "the_student_staff_ratio_2024",
        "the_international_students_pct_2024",
    ]
].copy()

student24["year"] = 2024
student24["ranking_source"] = "THE"

student24["total_students"] = pd.NA
student24["students_per_staff"] = student24[
    "the_student_staff_ratio_2024"
]
student24["international_students"] = pd.NA
student24["international_student_percentage"] = student24[
    "the_international_students_pct_2024"
]

student24 = student24[
    [
        "university_id",
        "year",
        "ranking_source",
        "total_students",
        "students_per_staff",
        "international_students",
        "international_student_percentage",
    ]
]

student_frames.append(student24)


# THE 2023
student23 = df[
    [
        "university_id",
        "the_student_staff_ratio_2023",
        "the_international_students_pct_2023",
    ]
].copy()

student23["year"] = 2023
student23["ranking_source"] = "THE"

student23["total_students"] = pd.NA
student23["students_per_staff"] = student23[
    "the_student_staff_ratio_2023"
]
student23["international_students"] = pd.NA
student23["international_student_percentage"] = student23[
    "the_international_students_pct_2023"
]

student23 = student23[
    [
        "university_id",
        "year",
        "ranking_source",
        "total_students",
        "students_per_staff",
        "international_students",
        "international_student_percentage",
    ]
]

student_frames.append(student23)


fact_student = pd.concat(
    student_frames,
    ignore_index=True
)

fact_student.to_csv(
    f"{OUTPUT_DIR}/fact_student.csv",
    index=False
)

print(f"Rows: {len(fact_student)}")
print("Saved: fact_student.csv")

print("Note: total_students and international_students are unavailable")
print("in the validated integrated dataset and are intentionally blank.")


# ============================================================
# 8. UNIVERSITY KPI FACT
# ============================================================

print("\n" + "=" * 70)
print("6. CREATING fact_university_kpi")
print("=" * 70)

kpi_required = [
    "university_id",
    "global_ranking_score",
    "research_impact_score",
    "student_staff_ratio",
    "faculty_student_ratio_score",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index",
]

for col in kpi_required:
    if col not in kpi.columns:
        raise ValueError(f"Missing KPI column: {col}")


fact_kpi = kpi[kpi_required].copy()

fact_kpi["year"] = 2024

fact_kpi = fact_kpi[
    [
        "university_id",
        "year",
        "global_ranking_score",
        "research_impact_score",
        "student_staff_ratio",
        "faculty_student_ratio_score",
        "international_student_percentage",
        "academic_reputation_score",
        "research_productivity_index",
    ]
]

fact_kpi.to_csv(
    f"{OUTPUT_DIR}/fact_university_kpi.csv",
    index=False
)

print(f"Rows: {len(fact_kpi)}")
print("Saved: fact_university_kpi.csv")


# ============================================================
# 9. COUNTRY EDUCATION FACT
# ============================================================

print("\n" + "=" * 70)
print("7. CREATING fact_country_education")
print("=" * 70)

country_source = df[
    [
        "wb_country_code",
        "wb_tertiary_enrollment_ratio_2015",
        "wb_tertiary_graduation_ratio_2015",
        "wb_female_tertiary_students_pct_2015",
        "wb_tertiary_pupil_teacher_ratio_2015",
        "wb_youth_literacy_15_24_pct_2015",
        "wb_tertiary_graduates_2015",
    ]
].drop_duplicates(
    subset=["wb_country_code"]
)

country_source = country_source[
    country_source["wb_country_code"].notna()
].copy()


indicator_mapping = {
    "wb_tertiary_enrollment_ratio_2015":
        "tertiary_enrollment_ratio",

    "wb_tertiary_graduation_ratio_2015":
        "tertiary_graduation_ratio",

    "wb_female_tertiary_students_pct_2015":
        "female_tertiary_students_pct",

    "wb_tertiary_pupil_teacher_ratio_2015":
        "tertiary_pupil_teacher_ratio",

    "wb_youth_literacy_15_24_pct_2015":
        "youth_literacy_15_24_pct",

    "wb_tertiary_graduates_2015":
        "tertiary_graduates",
}


country_frames = []

for source_col, indicator_name in indicator_mapping.items():

    temp = country_source[
        [
            "wb_country_code",
            source_col
        ]
    ].copy()

    temp["year"] = 2015
    temp["indicator"] = indicator_name

    temp = temp.rename(
        columns={
            "wb_country_code": "country_code",
            source_col: "value"
        }
    )

    country_frames.append(
        temp[
            [
                "country_code",
                "year",
                "indicator",
                "value"
            ]
        ]
    )


fact_country_education = pd.concat(
    country_frames,
    ignore_index=True
)

fact_country_education.to_csv(
    f"{OUTPUT_DIR}/fact_country_education.csv",
    index=False
)

print(f"Rows: {len(fact_country_education)}")
print("Saved: fact_country_education.csv")


# ============================================================
# 10. VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. DATA MODEL VALIDATION")
print("=" * 70)


print("\nUniversity dimension:")
print(f"Rows: {len(dim_university)}")
print(
    "Duplicate university IDs:",
    dim_university["university_id"].duplicated().sum()
)
print(
    "Missing university IDs:",
    dim_university["university_id"].isna().sum()
)


print("\nPerformance fact:")
print(f"Rows: {len(fact_performance)}")
print("Years:", sorted(fact_performance["year"].unique()))
print(
    "Sources:",
    fact_performance["ranking_source"].unique().tolist()
)


print("\nResearch fact:")
print(f"Rows: {len(fact_research)}")
print("Years:", sorted(fact_research["year"].unique()))


print("\nStudent fact:")
print(f"Rows: {len(fact_student)}")
print("Years:", sorted(fact_student["year"].unique()))


print("\nKPI fact:")
print(f"Rows: {len(fact_kpi)}")
print(
    "Missing university IDs:",
    fact_kpi["university_id"].isna().sum()
)
print(
    "Duplicate university IDs:",
    fact_kpi["university_id"].duplicated().sum()
)


print("\nCountry education fact:")
print(f"Rows: {len(fact_country_education)}")
print(
    "Unique countries:",
    fact_country_education["country_code"].nunique()
)
print(
    "Indicators:",
    fact_country_education["indicator"].nunique()
)


# ------------------------------------------------------------
# Referential integrity
# ------------------------------------------------------------

university_ids = set(
    dim_university["university_id"].dropna()
)

for table_name, table in [
    ("performance", fact_performance),
    ("research", fact_research),
    ("student", fact_student),
    ("kpi", fact_kpi),
]:

    invalid_ids = set(
        table["university_id"].dropna()
    ) - university_ids

    print(
        f"Invalid university IDs in {table_name}:",
        len(invalid_ids)
    )


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATA MODEL CREATED")
print("=" * 70)

print("\nFiles created:")
print("- dim_university.csv")
print("- fact_university_performance.csv")
print("- fact_research.csv")
print("- fact_student.csv")
print("- fact_university_kpi.csv")
print("- fact_country_education.csv")

print("\nSTATUS: SUCCESS")
print("=" * 70)