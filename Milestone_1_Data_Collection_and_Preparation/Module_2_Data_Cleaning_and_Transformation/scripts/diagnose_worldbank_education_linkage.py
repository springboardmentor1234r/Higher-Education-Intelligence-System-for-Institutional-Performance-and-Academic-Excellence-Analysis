import pandas as pd
from pathlib import Path

print("=" * 70)
print("STEP 8F.7 - WORLD BANK EDUCATION LINKAGE DIAGNOSIS")
print("=" * 70)

BASE_DIR = Path(__file__).resolve().parent.parent

UNIVERSITY_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank_education.csv"
)

EDUCATION_FILE = (
    BASE_DIR / "data" / "processed" /
    "worldbank_education_2015.csv"
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading final university dataset...")

uni = pd.read_csv(UNIVERSITY_FILE)

print("University dataset:", uni.shape)

print("\nLoading World Bank education dataset...")

wb = pd.read_csv(EDUCATION_FILE)

print("World Bank education dataset:", wb.shape)

# ------------------------------------------------------------
# EDUCATION INDICATORS
# ------------------------------------------------------------

education_columns = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015"
]

# ------------------------------------------------------------
# COUNTRY CODE COMPARISON
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COUNTRY CODE COMPARISON")
print("=" * 70)

uni_codes = set(
    uni["wb_country_code"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
)

wb_codes = set(
    wb["Country Code"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
)

common_codes = uni_codes.intersection(wb_codes)

print("Unique university WB codes:", len(uni_codes))
print("Unique education WB codes:", len(wb_codes))
print("Common WB codes:", len(common_codes))

print(
    "University codes NOT found in education file:",
    len(uni_codes - wb_codes)
)

# ------------------------------------------------------------
# UNMATCHED COUNTRY CODES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("UNMATCHED UNIVERSITY COUNTRY CODES")
print("=" * 70)

unmatched_codes = (
    uni[
        uni["wb_country_code"].notna()
        & ~uni["wb_country_code"].astype(str)
        .str.strip()
        .str.upper()
        .isin(wb_codes)
    ]
    [["country_name", "wb_country_code"]]
    .drop_duplicates()
    .sort_values("country_name")
)

print(unmatched_codes.to_string(index=False))

# ------------------------------------------------------------
# COUNTRIES WITH ZERO EDUCATION LINKAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COUNTRIES WITH ZERO EDUCATION LINKAGE")
print("=" * 70)

zero_linkage = (
    uni.groupby(
        ["country_name", "wb_country_code"],
        dropna=False
    )
    .agg(
        universities=("university_id", "count"),
        education_linked=("worldbank_education_2015_linked", "sum")
    )
    .reset_index()
)

zero_linkage = zero_linkage[
    zero_linkage["education_linked"] == 0
].sort_values(
    "universities",
    ascending=False
)

print(zero_linkage.to_string(index=False))

# ------------------------------------------------------------
# CHECK COUNTRY NAMES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COUNTRY NAME SAMPLE FROM EDUCATION DATA")
print("=" * 70)

print(
    wb[
        ["Country Name", "Country Code"]
    ]
    .head(30)
    .to_string(index=False)
)

# ------------------------------------------------------------
# FIND POSSIBLE NAME MATCHES FOR ZERO-LINKED COUNTRIES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("POSSIBLE COUNTRY NAME MATCHES")
print("=" * 70)

wb_names = set(
    wb["Country Name"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
)

for _, row in zero_linkage.head(30).iterrows():

    country = str(row["country_name"]).strip()

    if country.lower() in wb_names:
        name_status = "NAME FOUND"
    else:
        name_status = "NAME NOT FOUND"

    print(
        f"{country:<30} "
        f"WB Code: {str(row['wb_country_code']):<8} "
        f"{name_status}"
    )

# ------------------------------------------------------------
# CHECK ACTUAL LINKED COUNTRIES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EDUCATION-LINKED COUNTRY SAMPLE")
print("=" * 70)

linked_countries = (
    uni[
        uni["worldbank_education_2015_linked"]
    ]
    [["country_name", "wb_country_code"]]
    .drop_duplicates()
    .sort_values("country_name")
)

print(
    linked_countries.head(30).to_string(index=False)
)

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 8F.7 SUMMARY")
print("=" * 70)

print("Total universities:", len(uni))

print(
    "Universities with education data:",
    uni["worldbank_education_2015_linked"].sum()
)

print(
    "Universities without education data:",
    (~uni["worldbank_education_2015_linked"]).sum()
)

print(
    "University WB codes:",
    len(uni_codes)
)

print(
    "World Bank education codes:",
    len(wb_codes)
)

print(
    "Common codes:",
    len(common_codes)
)

print("\nDiagnosis completed.")
print("=" * 70)