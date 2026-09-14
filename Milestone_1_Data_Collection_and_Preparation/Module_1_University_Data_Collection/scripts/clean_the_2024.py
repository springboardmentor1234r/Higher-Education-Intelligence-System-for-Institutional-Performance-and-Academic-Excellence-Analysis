import pandas as pd

file_path = "data/raw/The World University Rankings 2024.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nMissing Value Percentage:")
print((df.isnull().sum() / len(df) * 100).sort_values(ascending=False))

# ============================================================
# STEP 2.2 - DUPLICATE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.2 - DUPLICATE ANALYSIS")
print("=" * 60)

# Duplicate complete rows
duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)

# Duplicate university names
duplicate_universities = df["name"].duplicated().sum()

print("\nDuplicate University Names:")
print(duplicate_universities)

# Show duplicate university names if any
if duplicate_universities > 0:
    print("\nDuplicate University Names:")
    print(
        df.loc[
            df["name"].duplicated(keep=False),
            ["name", "location", "rank"]
        ].sort_values("name")
    )
else:
    print("\nNo duplicate university names found.")

# ============================================================
# STEP 2.3 - RANK ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.3 - RANK ANALYSIS")
print("=" * 60)

print("\nSample Rank Values:")
print(df["rank"].head(20).to_string(index=False))

print("\nLast 20 Rank Values:")
print(df["rank"].tail(20).to_string(index=False))

print("\nUnique Rank Value Count:")
print(df["rank"].nunique())

print("\nRank Data Type:")
print(df["rank"].dtype)

# ============================================================
# STEP 2.4 - CATEGORICAL VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.4 - CATEGORICAL VALUE ANALYSIS")
print("=" * 60)

print("\nClosed Value Counts:")
print(df["closed"].value_counts(dropna=False))

print("\nUnaccredited Value Counts:")
print(df["unaccredited"].value_counts(dropna=False))

print("\nLocation Unique Count:")
print(df["location"].nunique())

print("\nTop Locations:")
print(df["location"].value_counts().head(30))

# ============================================================
# STEP 2.5 - SCORE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.5 - SCORE ANALYSIS")
print("=" * 60)

score_columns = [
    "scores_overall",
    "scores_teaching",
    "scores_research",
    "scores_citations",
    "scores_industry_income",
    "scores_international_outlook"
]

for column in score_columns:
    print(f"\n{column}")
    print("Data Type:", df[column].dtype)
    print("Missing:", df[column].isna().sum())
    print("Unique Values:", df[column].nunique())
    print("Sample Values:")
    print(df[column].dropna().head(10).to_list())

# ============================================================
# STEP 2.6 - MISSING SCORE RECORD ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.6 - MISSING SCORE RECORD ANALYSIS")
print("=" * 60)

missing_overall = df[df["scores_overall"].isna()]

print("\nNumber of Universities Without Overall Score:")
print(len(missing_overall))

print("\nSample Universities Without Overall Score:")

print(
    missing_overall[
        [
            "rank_order",
            "rank",
            "name",
            "location",
            "scores_overall",
            "closed",
            "unaccredited"
        ]
    ].head(30).to_string(index=False)
)

# ============================================================
# STEP 2.7 - MISSING LOCATION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.7 - MISSING LOCATION ANALYSIS")
print("=" * 60)

missing_location = df[df["location"].isna()]

print("\nUniversities With Missing Location:")
print(len(missing_location))

if len(missing_location) > 0:
    print("\nMissing Location Record:")
    print(
        missing_location[
            [
                "rank_order",
                "rank",
                "name",
                "scores_overall",
                "closed",
                "unaccredited"
            ]
        ].to_string(index=False)
    )

# ============================================================
# STEP 2.8 - HANDLE MISSING LOCATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.8 - HANDLE MISSING LOCATION")
print("=" * 60)

# Replace missing location with Unknown
df["location"] = df["location"].fillna("Unknown")

print("\nMissing Location Values After Handling:")
print(df["location"].isna().sum())

print("\nLocation Value for UBT:")
print(df.loc[df["name"].str.strip() == "UBT", ["name", "location"]])

# ============================================================
# STEP 2.9 - RANK CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.9 - RANK CLEANING")
print("=" * 60)

# Convert numeric ranks to numbers.
# Reporter rows will become missing (NaN).
df["rank_numeric"] = pd.to_numeric(df["rank"], errors="coerce")
df["ranking_status"] = df["rank_numeric"].apply(
    lambda x: "Ranked" if pd.notna(x) else "Reporter"
)

print("\nRank Data Types:")
print(df["rank_numeric"].dtype)

print("\nNumber of Ranked Universities:")
print((df["ranking_status"] == "Ranked").sum())

print("\nNumber of Reporter Universities:")
print((df["ranking_status"] == "Reporter").sum())

print("\nRanking Status:")
print(df["ranking_status"].value_counts())

print("\nRank Data Types:")
print(df["rank_numeric"].dtype)

print("\nNumber of Ranked Universities:")
print(df["rank_numeric"].notna().sum())

print("\nNumber of Reporter Universities:")
print(df["rank_numeric"].isna().sum())

print("\nSample Cleaned Rank Data:")
print(df[["rank", "rank_numeric", "name"]].head(20))

# ============================================================
# STEP 2.10 - SCORE DATA TYPE CONVERSION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.10 - SCORE DATA TYPE CONVERSION")
print("=" * 60)

# ------------------------------------------------------------
# Clean Overall Score
# ------------------------------------------------------------
# The scores_overall column contains both:
# 1. Single values such as "98.5"
# 2. Score ranges such as "98.5-99.5"
# Reporter universities contain non-score values.
#
# For score ranges, calculate the midpoint.
# Example:
# "98.5-99.5" -> (98.5 + 99.5) / 2 = 99.0

def clean_overall_score(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    # Single numeric value
    try:
        return float(value)
    except ValueError:
        pass

    # Handle score ranges
    value = value.replace("–", "-").replace("—", "-")

    if "-" in value:
        try:
            parts = value.split("-")

            if len(parts) == 2:
                lower = float(parts[0].strip())
                upper = float(parts[1].strip())

                return (lower + upper) / 2

        except ValueError:
            return None

    return None


df["scores_overall"] = df["scores_overall"].apply(
    clean_overall_score
)

# ------------------------------------------------------------
# Convert remaining score columns to numeric
# ------------------------------------------------------------

remaining_score_columns = [
    "scores_teaching",
    "scores_research",
    "scores_citations",
    "scores_industry_income",
    "scores_international_outlook"
]

for col in remaining_score_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

print("\nScore Data Types After Conversion:")
print(df[score_columns].dtypes)

print("\nMissing Score Values After Conversion:")
print(df[score_columns].isna().sum())

print("\nUniversities With Valid Overall Score:")
print(df["scores_overall"].notna().sum())

print("\nUniversities Without Overall Score:")
print(df["scores_overall"].isna().sum())

df["score_status"] = df["scores_overall"].apply(
    lambda x: "Available" if pd.notna(x) else "Not Available"
)

print("\nScore Status:")
print(df["score_status"].value_counts())

# ============================================================
# STEP 2.11 - STUDENT STATISTICS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.11 - STUDENT STATISTICS CLEANING")
print("=" * 60)

# Number of students
df["stats_number_students"] = (
    df["stats_number_students"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["stats_number_students"] = pd.to_numeric(
    df["stats_number_students"],
    errors="coerce"
)

# Percentage of international students
df["stats_pc_intl_students"] = (
    df["stats_pc_intl_students"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["stats_pc_intl_students"] = pd.to_numeric(
    df["stats_pc_intl_students"],
    errors="coerce"
)

# Female-male ratio
df["stats_female_male_ratio"] = (
    df["stats_female_male_ratio"]
    .astype(str)
    .str.strip()
)

# Proportion of international staff/researchers
df["stats_proportion_of_isr"] = (
    df["stats_proportion_of_isr"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["stats_proportion_of_isr"] = pd.to_numeric(
    df["stats_proportion_of_isr"],
    errors="coerce"
)

print("\nData Types After Student Statistics Cleaning:")
print(
    df[
        [
            "stats_number_students",
            "stats_student_staff_ratio",
            "stats_pc_intl_students",
            "stats_female_male_ratio",
            "stats_proportion_of_isr"
        ]
    ].dtypes
)

# ============================================================
# STEP 2.12 - FEMALE-MALE RATIO CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.12 - FEMALE-MALE RATIO CLEANING")
print("=" * 60)

# Convert female-male ratio such as "52:48" into female percentage
# Example: 52:48 -> 52.0

def extract_female_ratio(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if ":" in value:
        try:
            female = value.split(":")[0]
            return float(female)
        except:
            return None

    return None


df["female_percentage"] = df["stats_female_male_ratio"].apply(
    extract_female_ratio
)

print("\nFemale Percentage Sample:")
print(
    df[
        [
            "stats_female_male_ratio",
            "female_percentage"
        ]
    ].head(20)
)

print("\nMissing Female Percentage:")
print(df["female_percentage"].isna().sum())

# ============================================================
# STEP 2.13 - HANDLE REMAINING MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.13 - HANDLE REMAINING MISSING VALUES")
print("=" * 60)


# ------------------------------------------------------------
# 1. INTERNATIONAL STUDENTS PERCENTAGE
# ------------------------------------------------------------

print("\nMissing International Students Percentage Before:")
print(df["stats_pc_intl_students"].isna().sum())

intl_students_median = df["stats_pc_intl_students"].median()

df["stats_pc_intl_students"] = (
    df["stats_pc_intl_students"]
    .fillna(intl_students_median)
)

print("Median Used:", intl_students_median)

print("Missing International Students Percentage After:")
print(df["stats_pc_intl_students"].isna().sum())


# ------------------------------------------------------------
# 2. INTERNATIONAL STAFF / RESEARCHERS
# ------------------------------------------------------------

print("\nMissing International Staff/Researchers Before:")
print(df["stats_proportion_of_isr"].isna().sum())

isr_median = df["stats_proportion_of_isr"].median()

df["stats_proportion_of_isr"] = (
    df["stats_proportion_of_isr"]
    .fillna(isr_median)
)

print("Median Used:", isr_median)

print("Missing International Staff/Researchers After:")
print(df["stats_proportion_of_isr"].isna().sum())


# ------------------------------------------------------------
# 3. FEMALE PERCENTAGE
# ------------------------------------------------------------

print("\nMissing Female Percentage Before:")
print(df["female_percentage"].isna().sum())

female_median = df["female_percentage"].median()

df["female_percentage"] = (
    df["female_percentage"]
    .fillna(female_median)
)

print("Median Used:", female_median)

print("Missing Female Percentage After:")
print(df["female_percentage"].isna().sum())


# ------------------------------------------------------------
# 4. FEMALE-MALE RATIO
# ------------------------------------------------------------

print("\nMissing Female-Male Ratio Before:")
print(df["stats_female_male_ratio"].isna().sum())

replacement_ratio = (
    f"{female_median:.0f} : {100 - female_median:.0f}"
)

df["stats_female_male_ratio"] = (
    df["stats_female_male_ratio"]
    .fillna(replacement_ratio)
)

print("Replacement Ratio Used:", replacement_ratio)

print("Missing Female-Male Ratio After:")
print(df["stats_female_male_ratio"].isna().sum())


# ------------------------------------------------------------
# 5. SUBJECTS OFFERED
# ------------------------------------------------------------

print("\nMissing Subjects Offered Before:")
print(df["subjects_offered"].isna().sum())

df["subjects_offered"] = (
    df["subjects_offered"]
    .fillna("Unknown")
)

print("Missing Subjects Offered After:")
print(df["subjects_offered"].isna().sum())


# ============================================================
# 6. CREATE SCORE STATUS
# ============================================================

print("\nScore Status:")

df["score_status"] = df["scores_overall"].apply(
    lambda x: "Available" if pd.notna(x)
    else "Not Available"
)

print(df["score_status"].value_counts())


# ============================================================
# FINAL MISSING VALUE CHECK
# ============================================================

print("\n" + "=" * 60)
print("FINAL MISSING VALUE CHECK")
print("=" * 60)

remaining_missing = df.isna().sum()

remaining_missing = remaining_missing[
    remaining_missing > 0
].sort_values(ascending=False)

print("\nRemaining Missing Values:")
print(remaining_missing)


# ============================================================
# EXPECTED MISSING VALUE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("EXPECTED MISSING VALUE VALIDATION")
print("=" * 60)


# Reporter universities should NOT have numeric rank
reporter_with_rank = (
    (df["ranking_status"] == "Reporter") &
    (df["rank_numeric"].notna())
).sum()

print("\nReporter universities incorrectly having numeric rank:")
print(reporter_with_rank)


# Ranked universities MUST have numeric rank
ranked_without_rank = (
    (df["ranking_status"] == "Ranked") &
    (df["rank_numeric"].isna())
).sum()

print("\nRanked universities missing numeric rank:")
print(ranked_without_rank)


# Universities marked as Available MUST have overall score
available_without_score = (
    (df["score_status"] == "Available") &
    (df["scores_overall"].isna())
).sum()

print("\nAvailable score status but missing overall score:")
print(available_without_score)


# Universities marked Not Available should have missing overall score
not_available_with_score = (
    (df["score_status"] == "Not Available") &
    (df["scores_overall"].notna())
).sum()

print("\nNot Available score status but having overall score:")
print(not_available_with_score)

# ============================================================
# STEP 2.14 - UNIVERSITY NAME CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.14 - UNIVERSITY NAME CLEANING")
print("=" * 60)

# Remove extra spaces
df["name"] = (
    df["name"]
    .astype(str)
    .str.strip()
)

# Convert empty names to Unknown
df["name"] = df["name"].replace("", "Unknown")

print("\nMissing University Names:")
print(df["name"].isna().sum())

print("\nSample Cleaned University Names:")
print(df["name"].head(20).to_string(index=False))

print("\nDuplicate University Names After Cleaning:")
print(df["name"].duplicated().sum())


# ============================================================
# STEP 2.15 - LOCATION CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.15 - LOCATION CLEANING")
print("=" * 60)

df["location"] = (
    df["location"]
    .astype(str)
    .str.strip()
)

df["location"] = df["location"].replace(
    ["", "nan", "None"],
    "Unknown"
)

print("\nMissing Locations:")
print(df["location"].isna().sum())

print("\nNumber of Locations:")
print(df["location"].nunique())


# ============================================================
# STEP 2.16 - REPORTER STATUS CREATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.16 - REPORTER STATUS")
print("=" * 60)

# Identify whether the university has an actual numerical rank

df["ranking_status"] = df["rank_numeric"].apply(
    lambda x: "Ranked" if pd.notna(x) else "Reporter"
)

print("\nRanking Status Counts:")
print(df["ranking_status"].value_counts())

print("\nSample Ranking Status:")
print(
    df[
        [
            "name",
            "rank",
            "rank_numeric",
            "ranking_status"
        ]
    ].head(20)
)


# ============================================================
# STEP 2.17 - UNACCREDITED VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.17 - UNACCREDITED VALIDATION")
print("=" * 60)

print("\nUnaccredited Universities:")
print(
    df[df["unaccredited"] == True][
        [
            "name",
            "location",
            "rank",
            "unaccredited"
        ]
    ]
)


# ============================================================
# STEP 2.18 - CLOSED UNIVERSITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.18 - CLOSED UNIVERSITY VALIDATION")
print("=" * 60)

closed_count = df["closed"].sum()

print("\nNumber of Closed Universities:")
print(closed_count)

# ============================================================
# STEP 2.19 - SUBJECTS OFFERED CLEANING
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.19 - SUBJECTS OFFERED CLEANING")
print("=" * 60)

# Remove extra spaces
df["subjects_offered"] = (
    df["subjects_offered"]
    .astype(str)
    .str.strip()
)

# Replace empty or invalid values
df["subjects_offered"] = df["subjects_offered"].replace(
    ["", "nan", "None"],
    "Unknown"
)

print("\nMissing Subjects Offered:")
print(df["subjects_offered"].isna().sum())

 
# ============================================================
# STEP 2.20 - FINAL DATA TYPES
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.20 - FINAL DATA TYPES")
print("=" * 60)

print(df.dtypes)

# ============================================================
# STEP 2.21 -FINAL DATA QUALITY VALIDATION
# ============================================================
 
print("\n" + "=" * 60)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. DUPLICATE VALIDATION
# ------------------------------------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate University Names:")
print(df["name"].duplicated().sum())


# ------------------------------------------------------------
# 2. REQUIRED FIELD VALIDATION
# ------------------------------------------------------------

print("\nMissing University Names:")
print(df["name"].isna().sum())

print("\nMissing Locations:")
print(df["location"].isna().sum())


# ------------------------------------------------------------
# 3. SCORE VALIDATION
# ------------------------------------------------------------

score_columns = [
    "scores_overall",
    "scores_teaching",
    "scores_research",
    "scores_citations",
    "scores_industry_income",
    "scores_international_outlook"
]

for col in score_columns:
    invalid_scores = (
        df[col].dropna().lt(0).sum()
        + df[col].dropna().gt(100).sum()
    )

    print(f"\nInvalid {col}:")
    print(invalid_scores)


# ------------------------------------------------------------
# 4. STUDENT STATISTICS VALIDATION
# ------------------------------------------------------------

print("\nInvalid International Student Percentage:")
print(
    (
        (df["stats_pc_intl_students"] < 0)
        | (df["stats_pc_intl_students"] > 100)
    ).sum()
)

print("\nInvalid Female Percentage:")
print(
    (
        (df["female_percentage"] < 0)
        | (df["female_percentage"] > 100)
    ).sum()
)

print("\nInvalid Student Count:")
print(
    (df["stats_number_students"] < 0).sum()
)


# ------------------------------------------------------------
# 5. RANK VALIDATION
# ------------------------------------------------------------

print("\nRanking Status:")
print(df["ranking_status"].value_counts())

reporter_with_rank = (
    (df["ranking_status"] == "Reporter")
    & (df["rank_numeric"].notna())
).sum()

ranked_without_rank = (
    (df["ranking_status"] == "Ranked")
    & (df["rank_numeric"].isna())
).sum()

print("\nReporter universities incorrectly having numeric rank:")
print(reporter_with_rank)

print("\nRanked universities missing numeric rank:")
print(ranked_without_rank)


# ------------------------------------------------------------
# 6. SCORE STATUS VALIDATION
# ------------------------------------------------------------

available_missing_score = (
    (df["score_status"] == "Available")
    & (df["scores_overall"].isna())
).sum()

not_available_with_score = (
    (df["score_status"] == "Not Available")
    & (df["scores_overall"].notna())
).sum()

print("\nAvailable score status but missing overall score:")
print(available_missing_score)

print("\nNot Available score status but having overall score:")
print(not_available_with_score)


# ============================================================
# 7. EXPECTED VS UNEXPECTED MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("EXPECTED VS UNEXPECTED MISSING VALUES")
print("=" * 60)

# Expected missing values
expected_rank_missing = (
    df["ranking_status"] == "Reporter"
).sum()

expected_score_missing = (
    df["score_status"] == "Not Available"
).sum()

print("\nExpected Missing rank_numeric:")
print(expected_rank_missing)

print("\nExpected Missing Score Values:")
print(expected_score_missing)


# ------------------------------------------------------------
# Check unexpected missing values
# ------------------------------------------------------------

unexpected_missing = {}

# rank_numeric
unexpected_rank_missing = (
    (df["ranking_status"] == "Ranked")
    & (df["rank_numeric"].isna())
).sum()

if unexpected_rank_missing > 0:
    unexpected_missing["rank_numeric"] = unexpected_rank_missing


# score columns
for col in score_columns:
    unexpected_score_missing = (
        (df["score_status"] == "Available")
        & (df[col].isna())
    ).sum()

    if unexpected_score_missing > 0:
        unexpected_missing[col] = unexpected_score_missing


# Other important columns
important_columns = [
    "name",
    "location",
    "stats_number_students",
    "stats_student_staff_ratio",
    "stats_pc_intl_students",
    "female_percentage",
    "stats_proportion_of_isr",
    "subjects_offered"
]

for col in important_columns:
    missing_count = df[col].isna().sum()

    if missing_count > 0:
        unexpected_missing[col] = missing_count


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

print("\nUnexpected Missing Values:")

if len(unexpected_missing) == 0:
    print("None")
    print("\n✅ DATASET CLEANING PASSED")
else:
    print(unexpected_missing)
    print("\n⚠️ DATASET STILL HAS UNEXPECTED MISSING VALUES")


# ============================================================
# FINAL DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATASET SUMMARY")
print("=" * 60)

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nNumber of Ranked Universities:")
print((df["ranking_status"] == "Ranked").sum())

print("\nNumber of Reporter Universities:")
print((df["ranking_status"] == "Reporter").sum())

print("\nUniversities With Available Scores:")
print((df["score_status"] == "Available").sum())

print("\nUniversities Without Scores:")
print((df["score_status"] == "Not Available").sum())

print("\nFinal Dataset Columns:")
print(df.columns.tolist())

# ============================================================
# STEP 2.22 - SAVE CLEANED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 2.22 - SAVE CLEANED DATASET")
print("=" * 60)

output_path = "data/cleaned/the_world_university_rankings_2024_cleaned.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nCleaned Dataset Saved Successfully!")
print(output_path)

print("\nFinal Dataset Shape:")
print(df.shape)

print("\n" + "=" * 60)
print("FINAL THE 2024 DATASET CLEANING COMPLETED")
print("=" * 60)

 