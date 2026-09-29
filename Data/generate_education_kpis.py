#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ============================================================
# EDUVISION_DV - MODULE 3: KPI ENGINEERING
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("EDUVISION_DV - MODULE 3: EDUCATION KPI ENGINEERING")
print("=" * 70)


# ------------------------------------------------------------
# 1. Define project paths
# ------------------------------------------------------------

BASE_DIR = Path(
    r"C:/Users/gdivy/OneDrive/Desktop/Internship 7.0 project"
)

# Module 2 output
INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_cleaned.csv"
)

# Module 3 output
OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_final_dataset.xlsx"
)


# ------------------------------------------------------------
# 2. Check input file
# ------------------------------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"university_cleaned.csv was not found at:\n{INPUT_FILE}"
    )


# ------------------------------------------------------------
# 3. Load cleaned dataset
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("\nCleaned dataset loaded successfully.")

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")


# In[2]:




# In[3]:


# ============================================================
# 5. KPI FORMULA DEFINITIONS
# ============================================================

print("\n" + "=" * 70)
print("KPI FORMULA DEFINITIONS")
print("=" * 70)


# ------------------------------------------------------------
# KPI 1: Global Ranking Score
# ------------------------------------------------------------
# Higher value = better ranking performance.
#
# QS and THE normalized ranks are already converted to a
# 0-100 scale in Module 2.
#
# If both rankings are available:
#     Average of QS and THE normalized ranking scores
#
# If only one is available:
#     Use the available ranking score.
#
# This prevents unnecessary loss of data.
# ------------------------------------------------------------

df["Global_Ranking_Score"] = (
    df[["QS_Normalized_Rank", "THE_Normalized_Rank"]]
    .mean(axis=1, skipna=True)
)


# ------------------------------------------------------------
# KPI 2: Research Impact Score
# ------------------------------------------------------------
# QS Citations per Faculty represents citation impact.
# THE Research Quality represents research quality.
#
# Both are already on approximately a 0-100 scale.
#
# We give equal weight to both indicators.
# ------------------------------------------------------------

df["Research_Impact_Score"] = (
    df[["QS_Citations_Per_Faculty", "THE_Research_Quality"]]
    .mean(axis=1, skipna=True)
)


# ------------------------------------------------------------
# KPI 3: Faculty-to-Student Ratio
# ------------------------------------------------------------
# THE Student-to-Staff Ratio is available directly.
#
# We retain the original value as a faculty/student KPI,
# but convert it mathematically to:
#
# Faculty per 100 students = 100 / Student-to-Staff Ratio
#
# Higher value means more faculty relative to students.
# ------------------------------------------------------------

df["Faculty_to_Student_Ratio"] = np.where(
    df["THE_Student_Staff_Ratio"] > 0,
    100 / df["THE_Student_Staff_Ratio"],
    np.nan
)


# ------------------------------------------------------------
# KPI 4: International Student Percentage
# ------------------------------------------------------------
# THE already provides International Students as a
# percentage value.
#
# Example:
#     25 = 25% international students
# ------------------------------------------------------------

df["International_Student_Percentage"] = (
    df["THE_International_Students"]
)


# ------------------------------------------------------------
# KPI 5: Academic Reputation Score
# ------------------------------------------------------------
# QS provides Academic Reputation Score directly.
# ------------------------------------------------------------

df["Academic_Reputation_Score"] = (
    df["QS_Academic_Reputation"]
)


# ------------------------------------------------------------
# KPI 6: Research Productivity Index
# ------------------------------------------------------------
# We combine:
#   - THE Research Environment
#   - THE Research Quality
#
# Equal weighting is used to produce a 0-100 index.
# ------------------------------------------------------------

df["Research_Productivity_Index"] = (
    df[["THE_Research_Environment", "THE_Research_Quality"]]
    .mean(axis=1, skipna=True)
)


print("\nSix KPI calculations have been defined.")


# In[4]:


# ============================================================
# 6. KPI OUTPUT INSPECTION
# ============================================================

kpi_columns = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]




# In[5]:


# ============================================================
# 7. KPI VALIDATION
# ============================================================

print("=" * 70)
print("KPI VALIDATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Check minimum, maximum and missing values
# ------------------------------------------------------------

kpi_validation = pd.DataFrame({
    "KPI": kpi_columns,
    "Minimum": [df[col].min() for col in kpi_columns],
    "Maximum": [df[col].max() for col in kpi_columns],
    "Missing": [df[col].isna().sum() for col in kpi_columns]
})

print(kpi_validation.to_string(index=False))


# ------------------------------------------------------------
# 2. Check expected 0-100 KPI ranges
# ------------------------------------------------------------

score_kpis = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

print("\nRange checks for 0-100 KPIs:")

for col in score_kpis:
    invalid = (
        (df[col] < 0) |
        (df[col] > 100)
    ).sum()

    print(f"{col}: {invalid} invalid values")


# ------------------------------------------------------------
# 3. Faculty-to-student ratio validation
# ------------------------------------------------------------

invalid_ratio = (
    df["Faculty_to_Student_Ratio"] <= 0
).sum()

print(
    f"\nFaculty_to_Student_Ratio invalid/non-positive values: "
    f"{invalid_ratio}"
)


# ------------------------------------------------------------
# 4. Check duplicate universities
# ------------------------------------------------------------

duplicate_universities = df["University"].duplicated().sum()

print(
    f"\nDuplicate university names: "
    f"{duplicate_universities}"
)


# In[6]:


# ============================================================
# 8. CREATE FINAL TABLEAU-READY DATASET
# ============================================================

print("=" * 70)
print("CREATING FINAL TABLEAU-READY DATASET")
print("=" * 70)


# ------------------------------------------------------------
# Keep the original Module 2 fields and add the six KPIs
# ------------------------------------------------------------

final_df = df.copy()


# ------------------------------------------------------------
# Arrange the columns in a logical order
# ------------------------------------------------------------

final_columns = [
    # University information
    "University",
    "Country",

    # QS ranking and indicators
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
    "QS_Normalized_Rank",

    # THE ranking and indicators
    "THE_Rank",
    "THE_Overall_Score",
    "THE_Teaching",
    "THE_Research_Environment",
    "THE_Research_Quality",
    "THE_Industry_Impact",
    "THE_International_Outlook",
    "THE_Number_Students",
    "THE_Student_Staff_Ratio",
    "THE_International_Students",
    "THE_Female_Male_Ratio",
    "THE_Year",
    "THE_Normalized_Rank",
    "THE_Female_Percentage",
    "THE_Male_Percentage",

    # Engineered KPIs
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]


# ------------------------------------------------------------
# Select the final columns
# ------------------------------------------------------------

final_df = final_df[final_columns]


# ------------------------------------------------------------
# Display final dataset information
# ------------------------------------------------------------

print(f"\nFinal rows    : {len(final_df):,}")
print(f"Final columns : {len(final_df.columns)}")

print("\nFinal dataset preview:")
print(final_df.head().to_string(index=False))


# In[7]:


# ============================================================
# 9. SAVE FINAL DATASET TO EXCEL
# ============================================================

print("=" * 70)
print("SAVING FINAL DATASET")
print("=" * 70)


# Save as Excel workbook
final_df.to_excel(
    OUTPUT_FILE,
    index=False,
    sheet_name="University_Data"
)


# ------------------------------------------------------------
# Confirm file creation
# ------------------------------------------------------------

if OUTPUT_FILE.exists():
    print("\nExcel file created successfully!")
    print(f"File: {OUTPUT_FILE}")
else:
    raise FileNotFoundError(
        "Excel file could not be created."
    )


# In[ ]:




