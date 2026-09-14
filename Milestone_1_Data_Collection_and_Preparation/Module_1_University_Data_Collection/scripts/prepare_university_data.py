import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - UNIVERSITY DATA COMMON STRUCTURE
# ============================================================

BASE_DIR = Path("data/cleaned")

QS_FILE = BASE_DIR / "qs_world_university_rankings_2025_cleaned.csv"
THE_2024_FILE = BASE_DIR / "the_world_university_rankings_2024_cleaned.csv"
THE_2023_FILE = BASE_DIR / "the_world_university_rankings_2023_cleaned.csv"

# ============================================================
# STEP 1 - LOAD DATASETS
# ============================================================

print("=" * 70)
print("STEP 1 - LOADING CLEANED DATASETS")
print("=" * 70)

qs = pd.read_csv(QS_FILE)
the_2024 = pd.read_csv(THE_2024_FILE)
the_2023 = pd.read_csv(THE_2023_FILE)

print(f"QS 2025 shape: {qs.shape}")
print(f"THE 2024 shape: {the_2024.shape}")
print(f"THE 2023 shape: {the_2023.shape}")


# ============================================================
# STEP 2 - STANDARDIZE UNIVERSITY NAMES
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 - STANDARDIZING UNIVERSITY NAMES")
print("=" * 70)


def clean_university_name(series):
    return (
        series
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


qs["university_name_clean"] = clean_university_name(
    qs["institution_name"]
)

the_2024["university_name_clean"] = clean_university_name(
    the_2024["name"]
)

the_2023["university_name_clean"] = clean_university_name(
    the_2023["Name of University"]
)

print("QS 2025 university names standardized")
print("THE 2024 university names standardized")
print("THE 2023 university names standardized")


# ============================================================
# STEP 3 - STANDARDIZE COUNTRY NAMES
# ============================================================

print("\n" + "=" * 70)
print("STEP 3 - STANDARDIZING COUNTRY NAMES")
print("=" * 70)


def clean_country_name(series):
    return (
        series
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


qs["country_name_clean"] = clean_country_name(qs["location"])
the_2024["country_name_clean"] = clean_country_name(the_2024["location"])
the_2023["country_name_clean"] = clean_country_name(the_2023["Location"])

print("Country names standardized.")


# ============================================================
# STEP 4 - CREATE COMMON QS STRUCTURE
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 - QS 2025 COMMON STRUCTURE")
print("=" * 70)

qs_common = pd.DataFrame()

qs_common["university_name"] = qs["institution_name"]
qs_common["university_name_clean"] = qs["university_name_clean"]
qs_common["country_name"] = qs["location"]
qs_common["country_name_clean"] = qs["country_name_clean"]
qs_common["country_code"] = qs["country_code"]

qs_common["qs_rank_2025"] = qs["rank_2025"]
qs_common["qs_overall_score"] = qs["overall_score"]

qs_common["qs_academic_reputation_score"] = qs[
    "academic_reputation_score"
]

qs_common["qs_employer_reputation_score"] = qs[
    "employer_reputation_score"
]

qs_common["qs_faculty_student_score"] = qs[
    "faculty_student_score"
]

qs_common["qs_citations_per_faculty_score"] = qs[
    "citations_per_faculty_score"
]

qs_common["qs_international_students_score"] = qs[
    "international_students_score"
]

qs_common["qs_international_faculty_score"] = qs[
    "international_faculty_score"
]

qs_common["qs_employment_outcomes_score"] = qs[
    "employment_outcomes_score"
]

qs_common["qs_sustainability_score"] = qs[
    "sustainability_score"
]


# ============================================================
# STEP 5 - CREATE COMMON THE 2024 STRUCTURE
# ============================================================

print("\n" + "=" * 70)
print("STEP 5 - THE 2024 COMMON STRUCTURE")
print("=" * 70)

the24_common = pd.DataFrame()

the24_common["university_name"] = the_2024["name"]
the24_common["university_name_clean"] = the_2024[
    "university_name_clean"
]

the24_common["country_name"] = the_2024["location"]
the24_common["country_name_clean"] = the_2024[
    "country_name_clean"
]

the24_common["the_rank_2024"] = the_2024["rank_numeric"]

the24_common["the_overall_score_2024"] = the_2024[
    "scores_overall"
]

the24_common["the_teaching_score_2024"] = the_2024[
    "scores_teaching"
]

the24_common["the_research_score_2024"] = the_2024[
    "scores_research"
]

the24_common["the_citations_score_2024"] = the_2024[
    "scores_citations"
]

the24_common["the_industry_income_score_2024"] = the_2024[
    "scores_industry_income"
]

the24_common["the_international_outlook_score_2024"] = the_2024[
    "scores_international_outlook"
]

the24_common["the_student_staff_ratio_2024"] = the_2024[
    "stats_student_staff_ratio"
]

the24_common["the_international_students_pct_2024"] = the_2024[
    "stats_pc_intl_students"
]

the24_common["the_female_percentage_2024"] = the_2024[
    "female_percentage"
]


# ============================================================
# STEP 6 - CREATE COMMON THE 2023 STRUCTURE
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 - THE 2023 COMMON STRUCTURE")
print("=" * 70)

the23_common = pd.DataFrame()

the23_common["university_name"] = the_2023[
    "Name of University"
]

the23_common["university_name_clean"] = the_2023[
    "university_name_clean"
]

the23_common["country_name"] = the_2023["Location"]

the23_common["country_name_clean"] = the_2023[
    "country_name_clean"
]

the23_common["the_rank_2023"] = the_2023[
    "rank_numeric"
]

the23_common["the_overall_score_2023"] = the_2023[
    "OverAll Score"
]

the23_common["the_teaching_score_2023"] = the_2023[
    "Teaching Score"
]

the23_common["the_research_score_2023"] = the_2023[
    "Research Score"
]

the23_common["the_citations_score_2023"] = the_2023[
    "Citations Score"
]

the23_common["the_industry_income_score_2023"] = the_2023[
    "Industry Income Score"
]

the23_common["the_international_outlook_score_2023"] = the_2023[
    "International Outlook Score"
]

the23_common["the_student_staff_ratio_2023"] = the_2023[
    "No of student per staff"
]

the23_common["the_international_students_pct_2023"] = the_2023[
    "International Student"
]

the23_common["the_female_percentage_2023"] = the_2023[
    "female_percentage"
]


# ============================================================
# STEP 7 - VALIDATE COMMON STRUCTURES
# ============================================================

print("\n" + "=" * 70)
print("STEP 7 - COMMON STRUCTURE VALIDATION")
print("=" * 70)

print(f"QS common shape: {qs_common.shape}")
print(f"THE 2024 common shape: {the24_common.shape}")
print(f"THE 2023 common shape: {the23_common.shape}")

print("\nMissing university names:")
print("QS:", qs_common["university_name_clean"].isna().sum())
print("THE 2024:", the24_common["university_name_clean"].isna().sum())
print("THE 2023:", the23_common["university_name_clean"].isna().sum())

print("\nDuplicate university names:")
print(
    "QS:",
    qs_common["university_name_clean"].duplicated().sum()
)

print(
    "THE 2024:",
    the24_common["university_name_clean"].duplicated().sum()
)

print(
    "THE 2023:",
    the23_common["university_name_clean"].duplicated().sum()
)


# ============================================================
# STEP 8 - SAVE RAW COMMON UNIVERSITY DATA
# ============================================================

print("\n" + "=" * 70)
print("STEP 8 - SAVING COMMON DATA")
print("=" * 70)

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

qs_common.to_csv(
    output_dir / "qs_2025_common.csv",
    index=False
)

the24_common.to_csv(
    output_dir / "the_2024_common.csv",
    index=False
)

the23_common.to_csv(
    output_dir / "the_2023_common.csv",
    index=False
)

print("Saved:")
print("data/processed/qs_2025_common.csv")
print("data/processed/the_2024_common.csv")
print("data/processed/the_2023_common.csv")

print("\n" + "=" * 70)
print("STEP 4 COMPLETED SUCCESSFULLY")
print("=" * 70)