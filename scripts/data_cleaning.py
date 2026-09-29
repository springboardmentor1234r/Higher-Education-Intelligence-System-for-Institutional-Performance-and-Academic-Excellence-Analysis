"""
EduVision_DV - Data Cleaning Script
Infosys Springboard Virtual Internship Project

This script performs standardized cleaning on:
1. QS World University Rankings 2025 (infosys dataset.csv)
2. Times Higher Education (THE) World University Rankings (Top_Universities_THE.xlsx)

Outputs:
- data/processed/qs_cleaned.csv
- data/processed/the_cleaned.csv
"""

import os
import sys
import pandas as pd
import numpy as np


def clean_rank_numeric(val):
    """
    Parses ranking field into a numeric rank:
    - Numeric rank: keep numeric (e.g. '1' -> 1.0)
    - Equal ranks with '=': strip '=' (e.g. '15=' -> 15.0)
    - Ranges like '1201-1400': midpoint 1300.5
    - '1401+': 1401.0
    """
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace('=', '')
    if s.endswith('+'):
        try:
            return float(s[:-1])
        except ValueError:
            return np.nan
    if '-' in s:
        parts = s.split('-')
        try:
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2.0
        except ValueError:
            return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def clean_qs_data(raw_path):
    """
    Loads and cleans the QS dataset.
    """
    print(f"Loading QS raw data from: {raw_path}")
    # Read with latin-1 encoding
    try:
        df = pd.read_csv(raw_path, encoding='latin-1')
    except Exception as e:
        print(f"Failed with latin-1, trying ISO-8859-1: {e}")
        df = pd.read_csv(raw_path, encoding='ISO-8859-1')

    print(f"Loaded QS raw data: {df.shape[0]} rows, {df.shape[1]} columns")
    assert len(df) == 1503, f"Expected 1,503 rows in QS dataset, found {len(df)}"

    # Clean string fields: strip leading/trailing whitespace
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].astype(str).str.strip()
        # Replace 'nan' string resulting from astype(str) back to actual NaN if empty
        df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

    # Rank handling: Preserve RANK_2025, create Rank_2025_Numeric
    df['Rank_2025_Numeric'] = df['RANK_2025'].apply(clean_rank_numeric)

    # Clean Overall_Score:
    # If value is '-' or empty: convert to NaN. Do NOT replace missing with 0.
    df['Overall_Score'] = df['Overall_Score'].replace('-', np.nan)
    df['Overall_Score'] = pd.to_numeric(df['Overall_Score'], errors='coerce')

    # Convert numeric score columns to numeric float
    score_cols = [
        'Academic_Reputation_Score', 'Employer_Reputation_Score',
        'Faculty_Student_Score', 'Citations_per_Faculty_Score',
        'International_Faculty_Score', 'International_Students_Score',
        'International_Research_Network_Score', 'Employment_Outcomes_Score',
        'Sustainability_Score'
    ]
    for col in score_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace('-', np.nan), errors='coerce')

    # Clean rank reference columns
    rank_cols = [
        'Academic_Reputation_Rank', 'Employer_Reputation_Rank',
        'Faculty_Student_Rank', 'Citations_per_Faculty_Rank',
        'International_Faculty_Rank', 'International_Students_Rank',
        'International_Research_Network_Rank', 'Employment_Outcomes_Rank',
        'Sustainability_Rank'
    ]
    for col in rank_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({'nan': np.nan, '-': np.nan})

    # Validate RES. field categories
    res_counts = df['RES.'].value_counts().to_dict()
    print(f"QS RES. field counts: {res_counts}")
    assert res_counts.get('VH', 0) == 1021, f"Expected 1021 VH, found {res_counts.get('VH')}"
    assert res_counts.get('HI', 0) == 362, f"Expected 362 HI, found {res_counts.get('HI')}"
    assert res_counts.get('MD', 0) == 104, f"Expected 104 MD, found {res_counts.get('MD')}"
    assert res_counts.get('LO', 0) == 16, f"Expected 16 LO, found {res_counts.get('LO')}"

    # Validate Overall_Score non-null count
    non_null_scores = df['Overall_Score'].notna().sum()
    null_scores = df['Overall_Score'].isna().sum()
    print(f"QS Overall_Score: {non_null_scores} non-null, {null_scores} null")
    assert non_null_scores == 600, f"Expected 600 non-null Overall_Score, found {non_null_scores}"
    assert null_scores == 903, f"Expected 903 null Overall_Score, found {null_scores}"

    return df


def clean_the_data(raw_path):
    """
    Loads and cleans the THE dataset.
    """
    print(f"Loading THE raw data from: {raw_path}")
    df = pd.read_excel(raw_path)
    print(f"Loaded THE raw data: {df.shape[0]} rows, {df.shape[1]} columns")
    assert len(df) == 200, f"Expected 200 rows in THE dataset, found {len(df)}"

    # Clean whitespace on string columns
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

    # Preserve original THE Location in THE_Location
    df['THE_Location'] = df['Location'].copy()
    df = df.drop(columns=['Location'])

    # Country Normalization:
    # THE China -> QS China (Mainland)
    # THE Hong Kong -> QS Hong Kong SAR
    # THE Macao -> QS Macau SAR
    country_mapping = {
        'China': 'China (Mainland)',
        'Hong Kong': 'Hong Kong SAR',
        'Macao': 'Macau SAR'
    }
    df['THE_Normalized_Location'] = df['THE_Location'].replace(country_mapping)

    # Clean numeric fields appropriately
    numeric_cols = [
        'Overall Score', 'Teaching', 'Research Environment',
        'Research Quality', 'Industry', 'International Outlook',
        'No. of FTE Students', 'No. of Students per Staff',
        'International Students'
    ]
    for col in numeric_cols:
        if col in df.columns:
            # If string with commas or percentages
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(',', '').str.replace('%', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Rename columns to standard THE prefixes
    df = df.rename(columns={
        'Rank': 'THE_Rank',
        'Dense Rank': 'THE_Dense_Rank',
        'University Name': 'THE_University_Name',
        'Overall Score': 'THE_Overall_Score',
        'Teaching': 'THE_Teaching',
        'Research Environment': 'THE_Research_Environment',
        'Research Quality': 'THE_Research_Quality',
        'Industry': 'THE_Industry',
        'International Outlook': 'THE_International_Outlook',
        'No. of FTE Students': 'THE_No_of_FTE_Students',
        'No. of Students per Staff': 'THE_No_of_Students_per_Staff',
        'International Students': 'THE_International_Students'
    })

    print(f"THE cleaning complete: {len(df)} universities across {df['THE_Normalized_Location'].nunique()} normalized countries")
    return df


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    # Paths
    qs_raw = os.path.join(raw_dir, 'infosys_dataset.csv')
    if not os.path.exists(qs_raw):
        qs_raw = os.path.join(raw_dir, 'infosys dataset.csv')

    the_raw = os.path.join(raw_dir, 'Top_Universities_THE.xlsx')

    # Clean QS
    df_qs_cleaned = clean_qs_data(qs_raw)
    qs_out = os.path.join(processed_dir, 'qs_cleaned.csv')
    df_qs_cleaned.to_csv(qs_out, index=False, encoding='utf-8')
    print(f"Saved cleaned QS data to: {qs_out} (Shape: {df_qs_cleaned.shape})")

    # Clean THE
    df_the_cleaned = clean_the_data(the_raw)
    the_out = os.path.join(processed_dir, 'the_cleaned.csv')
    df_the_cleaned.to_csv(the_out, index=False, encoding='utf-8')
    print(f"Saved cleaned THE data to: {the_out} (Shape: {df_the_cleaned.shape})")


if __name__ == '__main__':
    main()
