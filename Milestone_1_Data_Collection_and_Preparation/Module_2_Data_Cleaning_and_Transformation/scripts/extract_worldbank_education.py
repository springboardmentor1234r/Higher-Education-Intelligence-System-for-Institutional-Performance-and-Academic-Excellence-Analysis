import pandas as pd
from pathlib import Path


# ============================================================
# STEP 8F.5 - WORLD BANK EDUCATION INDICATOR EXTRACTION
# ============================================================

print("=" * 70)
print("STEP 8F.5 - WORLD BANK EDUCATION INDICATOR EXTRACTION")
print("=" * 70)


# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

WB_FILE = BASE_DIR / "data" / "raw" / "EdStatsData.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "worldbank_education_2015.csv"


# ------------------------------------------------------------
# 2. SELECT INDICATORS
# ------------------------------------------------------------

INDICATORS = {
    "SE.TER.ENRR":
        "wb_tertiary_enrollment_ratio_2015",

    "SE.TER.CMPL.ZS":
        "wb_tertiary_graduation_ratio_2015",

    "SE.TER.ENRL.FE.ZS":
        "wb_female_tertiary_students_pct_2015",

    "UIS.PTRHC.56":
        "wb_tertiary_pupil_teacher_ratio_2015",

    "SE.ADT.1524.LT.ZS":
        "wb_youth_literacy_15_24_pct_2015",

    "SE.TER.GRAD":
        "wb_tertiary_graduates_2015",
}


# ------------------------------------------------------------
# 3. LOAD REQUIRED COLUMNS ONLY
# ------------------------------------------------------------

print("\nLoading World Bank Education Statistics...")

df = pd.read_csv(
    WB_FILE,
    usecols=[
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code",
        "2015"
    ]
)

print(f"Loaded shape: {df.shape}")


# ------------------------------------------------------------
# 4. FILTER SELECTED INDICATORS
# ------------------------------------------------------------

df = df[df["Indicator Code"].isin(INDICATORS.keys())].copy()

print(f"Rows after indicator filtering: {len(df)}")


# ------------------------------------------------------------
# 5. KEEP IMPORTANT COLUMNS
# ------------------------------------------------------------

df = df[
    [
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code",
        "2015"
    ]
].copy()


# ------------------------------------------------------------
# 6. RENAME INDICATOR VALUES
# ------------------------------------------------------------

df["indicator_column"] = df["Indicator Code"].map(INDICATORS)


# ------------------------------------------------------------
# 7. PIVOT TO ONE ROW PER COUNTRY
# ------------------------------------------------------------

education = df.pivot_table(
    index=["Country Name", "Country Code"],
    columns="indicator_column",
    values="2015",
    aggfunc="first"
).reset_index()


# Remove pivot column index name
education.columns.name = None


# ------------------------------------------------------------
# 8. ENSURE ALL EXPECTED COLUMNS EXIST
# ------------------------------------------------------------

for column in INDICATORS.values():

    if column not in education.columns:
        education[column] = pd.NA


# ------------------------------------------------------------
# 9. ORDER COLUMNS
# ------------------------------------------------------------

education = education[
    [
        "Country Name",
        "Country Code",

        "wb_tertiary_enrollment_ratio_2015",
        "wb_tertiary_graduation_ratio_2015",
        "wb_female_tertiary_students_pct_2015",
        "wb_tertiary_pupil_teacher_ratio_2015",
        "wb_youth_literacy_15_24_pct_2015",
        "wb_tertiary_graduates_2015",
    ]
]


# ------------------------------------------------------------
# 10. VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATING EXTRACTED DATA")
print("=" * 70)

print(f"\nCountries extracted: {len(education)}")
print(f"Columns extracted: {len(education.columns)}")


print("\nMissing values by indicator:")

for column in INDICATORS.values():

    missing = education[column].isna().sum()
    total = len(education)

    available = total - missing

    percentage = (
        available / total * 100
        if total > 0
        else 0
    )

    print(
        f"{column:<50} "
        f"Available: {available:>3} "
        f"Missing: {missing:>3} "
        f"Coverage: {percentage:>6.2f}%"
    )


# ------------------------------------------------------------
# 11. DUPLICATE COUNTRY CHECK
# ------------------------------------------------------------

duplicate_countries = education["Country Code"].duplicated().sum()

print(f"\nDuplicate country codes: {duplicate_countries}")


# ------------------------------------------------------------
# 12. SAVE
# ------------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

education.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("STEP 8F.5 COMPLETED")
print("=" * 70)

print(f"\nSaved file:")
print(OUTPUT_FILE)

print(f"\nFinal shape: {education.shape}")

print("\nFirst 10 rows:")
print(
    education.head(10).to_string(index=False)
)

print("\n" + "=" * 70)