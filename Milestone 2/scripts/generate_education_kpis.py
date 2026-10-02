import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

input_file = "data/university_cleaned.csv"
output_file = "data/university_final_dataset.xlsx"

df = pd.read_csv(input_file)

print("Original shape:", df.shape)


# ==========================================
# 2. HELPER FUNCTION FOR RANKING
# ==========================================

def extract_rank(value):
    """
    Converts ranking values such as:
    1
    25
    801-850
    1001-1200
    into a numeric representative rank.
    """

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if "-" in value:
        parts = value.split("-")
        try:
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return np.nan

    try:
        return float(value)
    except:
        return np.nan


# ==========================================
# 3. CONVERT RANK COLUMNS
# ==========================================

df["QS_Rank_Numeric"] = df["QS_Rank"].apply(extract_rank)
df["THE_Rank_Numeric"] = df["THE_Rank"].apply(extract_rank)


# ==========================================
# 4. GLOBAL RANKING SCORE
# ==========================================

# Lower ranking number = better university.
# Convert rank into a 0-100 score.

qs_score = 100 * (
    1 - (df["QS_Rank_Numeric"] - df["QS_Rank_Numeric"].min()) /
    (df["QS_Rank_Numeric"].max() - df["QS_Rank_Numeric"].min())
)

the_score = 100 * (
    1 - (df["THE_Rank_Numeric"] - df["THE_Rank_Numeric"].min()) /
    (df["THE_Rank_Numeric"].max() - df["THE_Rank_Numeric"].min())
)

df["Global_Ranking_Score"] = pd.concat(
    [qs_score, the_score], axis=1
).mean(axis=1)


# ==========================================
# 5. RESEARCH IMPACT SCORE
# ==========================================

# Use THE Research Score as the primary
# research-performance measure.

df["Research_Impact_Score"] = pd.to_numeric(
    df["THE_Research_Score"],
    errors="coerce"
)


# ==========================================
# 6. FACULTY-TO-STUDENT RATIO
# ==========================================

df["Total_Students"] = pd.to_numeric(
    df["Total_Students"],
    errors="coerce"
)

df["Student_Staff_Ratio"] = pd.to_numeric(
    df["Student_Staff_Ratio"],
    errors="coerce"
)

# Student-to-faculty/staff ratio is already
# provided in the cleaned dataset.

df["Faculty_to_Student_Ratio"] = np.where(
    df["Student_Staff_Ratio"] > 0,
    1 / df["Student_Staff_Ratio"],
    np.nan
)


# ==========================================
# 7. INTERNATIONAL STUDENT PERCENTAGE
# ==========================================

df["International_Student_Percentage"] = (
    pd.to_numeric(df["QS_International_Students"], errors="coerce")
    / df["Total_Students"]
) * 100


# ==========================================
# 8. ACADEMIC REPUTATION SCORE
# ==========================================

df["Academic_Reputation_Score"] = pd.to_numeric(
    df["QS_Academic_Reputation"],
    errors="coerce"
)


# ==========================================
# 9. RESEARCH PRODUCTIVITY INDEX
# ==========================================

# QS citations per faculty represents research
# productivity/impact relative to faculty size.

df["Research_Productivity_Index"] = pd.to_numeric(
    df["QS_Citations_Per_Faculty"],
    errors="coerce"
)


# ==========================================
# 10. CLEAN KPI VALUES
# ==========================================

kpi_columns = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

for column in kpi_columns:
    df[column] = df[column].replace(
        [np.inf, -np.inf],
        np.nan
    )


# ==========================================
# 11. ROUND KPI VALUES
# ==========================================

df["Global_Ranking_Score"] = df["Global_Ranking_Score"].round(2)
df["Research_Impact_Score"] = df["Research_Impact_Score"].round(2)
df["Faculty_to_Student_Ratio"] = df["Faculty_to_Student_Ratio"].round(4)
df["International_Student_Percentage"] = df[
    "International_Student_Percentage"
].round(2)
df["Academic_Reputation_Score"] = df[
    "Academic_Reputation_Score"
].round(2)
df["Research_Productivity_Index"] = df[
    "Research_Productivity_Index"
].round(2)


# ==========================================
# 12. SAVE FINAL DATASET
# ==========================================

df.to_excel(
    output_file,
    index=False
)

print("\nKPI calculation completed.")
print("Final shape:", df.shape)
print("Saved:", output_file)

print("\nKPI columns:")

for column in kpi_columns:
    print(
        f"{column}: "
        f"{df[column].notna().sum()} valid values"
    )

print("\nSample KPI results:")
print(df[
    [
        "University_Name_QS",
        "Global_Ranking_Score",
        "Research_Impact_Score",
        "Faculty_to_Student_Ratio",
        "International_Student_Percentage",
        "Academic_Reputation_Score",
        "Research_Productivity_Index"
    ]
].head(10))