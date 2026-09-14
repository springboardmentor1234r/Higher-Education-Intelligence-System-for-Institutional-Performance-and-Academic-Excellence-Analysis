import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("STEP 8F.9 - FINAL ANALYTICAL DATASET VALIDATION")
print("=" * 70)

# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FINAL_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank_education.csv"
)

# ============================================================
# EXPECTED VALUES
# ============================================================

EXPECTED_ROWS = 3530
EXPECTED_COLUMNS = 53

# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    # University
    "university_id",
    "university_name",
    "country_name",
    "country_code",

    # QS 2025
    "qs_rank_2025",
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",
    "qs_present",

    # THE 2024
    "the_rank_2024",
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "the_female_percentage_2024",
    "the24_present",

    # THE 2023
    "the_rank_2023",
    "the_overall_score_2023",
    "the_teaching_score_2023",
    "the_research_score_2023",
    "the_citations_score_2023",
    "the_industry_income_score_2023",
    "the_international_outlook_score_2023",
    "the_student_staff_ratio_2023",
    "the_international_students_pct_2023",
    "the_female_percentage_2023",
    "the23_present",

    # World Bank metadata
    "worldbank_match_key",
    "wb_country_code",
    "wb_country_name",
    "wb_long_name",
    "wb_2alpha_code",
    "wb_region",
    "wb_income_group",
    "worldbank_linked",

    # World Bank education 2015
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015",
    "worldbank_education_2015_linked",
]

# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading final analytical dataset...")

if not FINAL_FILE.exists():
    raise FileNotFoundError(
        f"Final dataset not found:\n{FINAL_FILE}"
    )

df = pd.read_csv(FINAL_FILE)

print("Dataset loaded successfully.")

# ============================================================
# 1. DATASET SHAPE
# ============================================================

print("\n" + "=" * 70)
print("1. DATASET SHAPE")
print("=" * 70)

rows, columns = df.shape

print("Rows    :", rows)
print("Columns :", columns)

if rows == EXPECTED_ROWS:
    print("Row count check: PASS")
else:
    print("Row count check: FAIL")

if columns == EXPECTED_COLUMNS:
    print("Column count check: PASS")
else:
    print("Column count check: FAIL")

# ============================================================
# 2. REQUIRED COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("2. REQUIRED COLUMN CHECK")
print("=" * 70)

missing_columns = [
    col for col in REQUIRED_COLUMNS
    if col not in df.columns
]

if len(missing_columns) == 0:
    print("All required columns present: PASS")
else:
    print("Missing columns: FAIL")

    for col in missing_columns:
        print(" -", col)

# ============================================================
# 3. UNIVERSITY ID VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("3. UNIVERSITY ID VALIDATION")
print("=" * 70)

missing_ids = df["university_id"].isna().sum()
duplicate_ids = df["university_id"].duplicated().sum()

print("Missing university IDs  :", missing_ids)
print("Duplicate university IDs:", duplicate_ids)

if missing_ids == 0:
    print("Missing ID check: PASS")
else:
    print("Missing ID check: FAIL")

if duplicate_ids == 0:
    print("Duplicate ID check: PASS")
else:
    print("Duplicate ID check: FAIL")

# ============================================================
# 4. UNIVERSITY NAME VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("4. UNIVERSITY NAME VALIDATION")
print("=" * 70)

missing_names = df["university_name"].isna().sum()
empty_names = (
    df["university_name"]
    .astype(str)
    .str.strip()
    .eq("")
    .sum()
)

print("Missing university names:", missing_names)
print("Empty university names  :", empty_names)

if missing_names == 0 and empty_names == 0:
    print("University name check: PASS")
else:
    print("University name check: FAIL")

# ============================================================
# 5. COUNTRY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("5. COUNTRY VALIDATION")
print("=" * 70)

missing_countries = df["country_name"].isna().sum()

unique_countries = df["country_name"].nunique()

print("Missing country names:", missing_countries)
print("Unique countries     :", unique_countries)

if missing_countries == 0:
    print("Country name check: PASS")
else:
    print("Country name check: FAIL")

# ============================================================
# 6. UNIVERSITY RANKING PRESENCE
# ============================================================

print("\n" + "=" * 70)
print("6. RANKING DATA COVERAGE")
print("=" * 70)

qs_count = df["qs_present"].sum()
the24_count = df["the24_present"].sum()
the23_count = df["the23_present"].sum()

print("QS 2025 universities :", qs_count)
print("THE 2024 universities:", the24_count)
print("THE 2023 universities:", the23_count)

all_three = (
    (df["qs_present"] == True)
    & (df["the24_present"] == True)
    & (df["the23_present"] == True)
).sum()

print("Present in all 3 ranking datasets:", all_three)

# ============================================================
# 7. WORLD BANK METADATA VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("7. WORLD BANK METADATA VALIDATION")
print("=" * 70)

wb_linked = df["worldbank_linked"].sum()
wb_not_linked = (~df["worldbank_linked"]).sum()

print("World Bank linked    :", wb_linked)
print("World Bank not linked:", wb_not_linked)

wb_linkage_rate = (
    wb_linked / len(df) * 100
)

print(
    f"World Bank linkage rate: "
    f"{wb_linkage_rate:.2f}%"
)

# ============================================================
# 8. WORLD BANK EDUCATION VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. WORLD BANK EDUCATION VALIDATION")
print("=" * 70)

education_columns = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015",
]

for col in education_columns:

    available = df[col].notna().sum()
    missing = df[col].isna().sum()

    coverage = (
        available / len(df) * 100
    )

    print(
        f"{col:<50}"
        f"Available: {available:4d} "
        f"Missing: {missing:4d} "
        f"Coverage: {coverage:6.2f}%"
    )

education_linked = df[
    "worldbank_education_2015_linked"
].sum()

education_not_linked = (
    ~df["worldbank_education_2015_linked"]
).sum()

print(
    "\nUniversities with education data:",
    education_linked
)

print(
    "Universities without education data:",
    education_not_linked
)

# ============================================================
# 9. EDUCATION LINKAGE CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("9. EDUCATION LINKAGE CONSISTENCY")
print("=" * 70)

calculated_linked = (
    df[education_columns]
    .notna()
    .any(axis=1)
)

stored_linked = (
    df["worldbank_education_2015_linked"]
    .fillna(False)
    .astype(bool)
)

inconsistent = (
    calculated_linked != stored_linked
).sum()

print(
    "Inconsistent education linkage flags:",
    inconsistent
)

if inconsistent == 0:
    print("Education linkage consistency: PASS")
else:
    print("Education linkage consistency: FAIL")

# ============================================================
# 10. DUPLICATE ROW CHECK
# ============================================================

print("\n" + "=" * 70)
print("10. DUPLICATE ROW CHECK")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print("Duplicate complete rows:", duplicate_rows)

if duplicate_rows == 0:
    print("Duplicate row check: PASS")
else:
    print("Duplicate row check: FAIL")

# ============================================================
# 11. NUMERIC COLUMN VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("11. NUMERIC COLUMN VALIDATION")
print("=" * 70)

numeric_columns = [
    "qs_rank_2025",
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",

    "the_rank_2024",
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "the_female_percentage_2024",

    "the_rank_2023",
    "the_overall_score_2023",
    "the_teaching_score_2023",
    "the_research_score_2023",
    "the_citations_score_2023",
    "the_industry_income_score_2023",
    "the_international_outlook_score_2023",
    "the_student_staff_ratio_2023",
    "the_international_students_pct_2023",
    "the_female_percentage_2023",

    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015",
]

non_numeric = []

for col in numeric_columns:

    if not pd.api.types.is_numeric_dtype(df[col]):
        non_numeric.append(col)

if len(non_numeric) == 0:
    print("All expected numeric columns are numeric: PASS")
else:
    print("Non-numeric columns detected: FAIL")

    for col in non_numeric:
        print(" -", col)

# ============================================================
# 12. INVALID SCORE CHECK
# ============================================================

print("\n" + "=" * 70)
print("12. SCORE RANGE VALIDATION")
print("=" * 70)

score_columns = [
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",

    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",

    "the_overall_score_2023",
    "the_teaching_score_2023",
    "the_research_score_2023",
    "the_citations_score_2023",
    "the_industry_income_score_2023",
    "the_international_outlook_score_2023",
]

invalid_scores = 0

for col in score_columns:

    values = df[col].dropna()

    invalid = (
        (values < 0)
        | (values > 100)
    ).sum()

    if invalid > 0:

        print(
            f"{col}: {invalid} invalid values"
        )

        invalid_scores += invalid

if invalid_scores == 0:
    print("Score range validation: PASS")
else:
    print("Score range validation: FAIL")

# ============================================================
# 13. WORLD BANK PERCENTAGE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("13. WORLD BANK PERCENTAGE VALIDATION")
print("=" * 70)

percentage_columns = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_youth_literacy_15_24_pct_2015",
]

invalid_wb_percentages = 0

for col in percentage_columns:

    values = df[col].dropna()

    invalid = (
        (values < 0)
        | (values > 100)
    ).sum()

    if invalid > 0:

        print(
            f"{col}: {invalid} invalid values"
        )

        invalid_wb_percentages += invalid

if invalid_wb_percentages == 0:
    print(
        "World Bank percentage validation: PASS"
    )
else:
    print(
        "World Bank percentage validation: FAIL"
    )

# ============================================================
# 14. WORLD BANK LINKAGE CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("14. WORLD BANK LINKAGE CONSISTENCY")
print("=" * 70)

expected_wb_linked = (
    df["wb_country_code"].notna()
)

actual_wb_linked = (
    df["worldbank_linked"]
    .fillna(False)
    .astype(bool)
)

wb_inconsistent = (
    expected_wb_linked != actual_wb_linked
).sum()

print(
    "Inconsistent World Bank linkage flags:",
    wb_inconsistent
)

if wb_inconsistent == 0:
    print("World Bank linkage consistency: PASS")
else:
    print("World Bank linkage consistency: FAIL")

# ============================================================
# 15. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

checks = {
    "Expected row count": rows == EXPECTED_ROWS,
    "Expected column count": columns == EXPECTED_COLUMNS,
    "Required columns present": len(missing_columns) == 0,
    "No missing university IDs": missing_ids == 0,
    "No duplicate university IDs": duplicate_ids == 0,
    "No missing university names": (
        missing_names == 0
        and empty_names == 0
    ),
    "No duplicate complete rows": duplicate_rows == 0,
    "Numeric columns valid": len(non_numeric) == 0,
    "Ranking score ranges valid": invalid_scores == 0,
    "World Bank percentage ranges valid": (
        invalid_wb_percentages == 0
    ),
    "Education linkage consistent": inconsistent == 0,
    "World Bank linkage consistent": wb_inconsistent == 0,
}

all_passed = True

for check, result in checks.items():

    status = "PASS" if result else "FAIL"

    print(
        f"{check:<45} {status}"
    )

    if not result:
        all_passed = False

# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)

if all_passed:

    print("STEP 8F.9 COMPLETED - ALL VALIDATION CHECKS PASSED")
    print("=" * 70)

    print("\nFINAL DATASET:")
    print(
        "data/processed/"
        "university_integrated_worldbank_education.csv"
    )

    print("\nFinal shape:")
    print(f"Rows    : {rows}")
    print(f"Columns : {columns}")

    print(
        "\nThe dataset is READY for Exploratory Data Analysis (EDA)."
    )

else:

    print("STEP 8F.9 FAILED - SOME VALIDATION CHECKS FAILED")
    print("=" * 70)

    print(
        "\nPlease review the FAIL results above "
        "before starting EDA."
    )