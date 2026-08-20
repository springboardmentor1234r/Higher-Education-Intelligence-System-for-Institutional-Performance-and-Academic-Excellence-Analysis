import pandas as pd
import re
from pathlib import Path

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

QS_FILE = BASE_DIR / "data" / "raw" / "qs-world-rankings-2025.csv"
THE_FILE = BASE_DIR / "data" / "raw" / "TIMES_WorldUniversityRankings_2024.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "university_raw_data.csv"


# ------------------------------------------------------------
# 2. Load datasets
# ------------------------------------------------------------

print("=" * 60)
print("EDUVISION_DV - MODULE 1: DATA COLLECTION")
print("=" * 60)

print("\n[1/6] Loading datasets...")

if not QS_FILE.exists():
    raise FileNotFoundError(
        f"QS dataset not found:\n{QS_FILE}"
    )

if not THE_FILE.exists():
    raise FileNotFoundError(
        f"THE dataset not found:\n{THE_FILE}"
    )

qs_df = pd.read_csv(QS_FILE)
the_df = pd.read_csv(THE_FILE)

print(f"QS records loaded:  {len(qs_df):,}")
print(f"THE records loaded: {len(the_df):,}")


# ------------------------------------------------------------
# 3. Select QS performance indicators
# ------------------------------------------------------------

print("\n[2/6] Collecting QS performance indicators...")

qs_columns = [
    "2025 Rank",
    "Institution Name",
    "Location",
    "Academic Reputation",
    "Employer Reputation",
    "Faculty Student",
    "Citations per Faculty",
    "International Faculty",
    "International Students",
    "International Research Network",
    "Employment Outcomes",
    "Sustainability",
    "QS Overall Score"
]

qs = qs_df[qs_columns].copy()

qs.rename(
    columns={
        "2025 Rank": "QS_Rank",
        "Institution Name": "University_Name",
        "Location": "QS_Country",
        "Academic Reputation": "QS_Academic_Reputation",
        "Employer Reputation": "QS_Employer_Reputation",
        "Faculty Student": "QS_Faculty_Student",
        "Citations per Faculty": "QS_Citations_Per_Faculty",
        "International Faculty": "QS_International_Faculty",
        "International Students": "QS_International_Students",
        "International Research Network": (
            "QS_International_Research_Network"
        ),
        "Employment Outcomes": "QS_Employment_Outcomes",
        "Sustainability": "QS_Sustainability",
        "QS Overall Score": "QS_Overall_Score"
    },
    inplace=True
)


# ------------------------------------------------------------
# 4. Select THE performance indicators
# ------------------------------------------------------------

print("[3/6] Collecting THE performance indicators...")

the_columns = [
    "rank",
    "name",
    "location",
    "scores_overall",
    "scores_teaching",
    "scores_research",
    "scores_citations",
    "scores_industry_income",
    "scores_international_outlook",
    "stats_number_students",
    "stats_student_staff_ratio",
    "stats_pc_intl_students",
    "stats_female_male_ratio"
]


the = the_df[
    the_df["scores_overall"].notna()
][the_columns].copy()

the.rename(
    columns={
        "rank": "THE_Rank",
        "name": "THE_University_Name",
        "location": "THE_Country",
        "scores_overall": "THE_Overall_Score",
        "scores_teaching": "THE_Teaching",
        "scores_research": "THE_Research",
        "scores_citations": "THE_Citations",
        "scores_industry_income": "THE_Industry_Income",
        "scores_international_outlook": (
            "THE_International_Outlook"
        ),
        "stats_number_students": "THE_Number_Students",
        "stats_student_staff_ratio": (
            "THE_Student_Staff_Ratio"
        ),
        "stats_pc_intl_students": (
            "THE_International_Students"
        ),
        "stats_female_male_ratio": (
            "THE_Female_Male_Ratio"
        )
    },
    inplace=True
)

print(f"Ranked THE records selected: {len(the):,}")


# ------------------------------------------------------------
# 5. Create university matching keys
# ------------------------------------------------------------

print("[4/6] Creating university matching keys...")


def create_university_key(name):
    """
    Creates a normalized university name for dataset matching.

    This is only an integration key.
    Detailed cleaning and standardization will be performed
    during Module 2.
    """

    name = str(name).lower().strip()

    # Remove text inside parentheses.
    # Example:
    # Massachusetts Institute of Technology (MIT)
    # becomes:
    # Massachusetts Institute of Technology
    name = re.sub(r"\([^)]*\)", "", name)

    # Standardize ampersand.
    name = name.replace("&", "and")

    # Remove punctuation.
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    # Remove leading "the".
    name = re.sub(r"^the\s+", "", name)

    # Normalize whitespace.
    name = re.sub(r"\s+", " ", name).strip()

    return name


qs["University_Key"] = qs["University_Name"].apply(
    create_university_key
)

the["University_Key"] = the["THE_University_Name"].apply(
    create_university_key
)


# ------------------------------------------------------------
# 6. Merge QS and THE datasets
# ------------------------------------------------------------

print("[5/6] Merging QS and THE datasets...")

merged_df = pd.merge(
    qs,
    the,
    on="University_Key",
    how="outer",
    indicator=True
)


# ------------------------------------------------------------
# 7. Create common university and country fields
# ------------------------------------------------------------

merged_df["University"] = (
    merged_df["University_Name"]
    .fillna(merged_df["THE_University_Name"])
)

merged_df["Country"] = (
    merged_df["QS_Country"]
    .fillna(merged_df["THE_Country"])
)


# ------------------------------------------------------------
# 8. Arrange final columns
# ------------------------------------------------------------

final_columns = [
    "University",
    "Country",

    # -------------------------
    # QS indicators
    # -------------------------
    "QS_Rank",
    "QS_Overall_Score",
    "QS_Academic_Reputation",
    "QS_Employer_Reputation",
    "QS_Faculty_Student",
    "QS_Citations_Per_Faculty",
    "QS_International_Faculty",
    "QS_International_Students",
    "QS_International_Research_Network",
    "QS_Employment_Outcomes",
    "QS_Sustainability",

    # -------------------------
    # THE indicators
    # -------------------------
    "THE_Rank",
    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research",
    "THE_Citations",
    "THE_Industry_Income",
    "THE_International_Outlook",
    "THE_Number_Students",
    "THE_Student_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_Male_Ratio",

    # Technical merge information.
    "_merge"
]

merged_df = merged_df[final_columns]


# ------------------------------------------------------------
# 9. Validate dataset integration
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATASET INTEGRATION VALIDATION")
print("=" * 60)

matched = (
    merged_df["_merge"] == "both"
).sum()

qs_only = (
    merged_df["_merge"] == "left_only"
).sum()

the_only = (
    merged_df["_merge"] == "right_only"
).sum()

print(f"QS universities:          {len(qs):,}")
print(f"Ranked THE universities:  {len(the):,}")
print(f"Matched universities:     {matched:,}")
print(f"QS-only universities:     {qs_only:,}")
print(f"THE-only universities:    {the_only:,}")

print("\nRaw integrated records:", len(merged_df))


# ------------------------------------------------------------
# 10. Remove technical merge column
# ------------------------------------------------------------

output_df = merged_df.drop(
    columns=["_merge"]
)


# ------------------------------------------------------------
# 11. Save university_raw_data.csv
# ------------------------------------------------------------

print("\n[6/6] Saving university_raw_data.csv...")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

output_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 12. Final validation
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MODULE 1 COMPLETED")
print("=" * 60)

print(f"Output file: {OUTPUT_FILE}")
print(f"Rows:         {len(output_df):,}")
print(f"Columns:      {len(output_df.columns)}")

print("\nUniversity raw data created successfully.")
print("=" * 60)
