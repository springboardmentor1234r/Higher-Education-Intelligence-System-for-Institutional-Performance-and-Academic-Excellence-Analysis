"""
EduVision_DV - KPI Engineering & Validation Script
Infosys Springboard Virtual Internship Project

This script calculates the 6 required project KPIs and 3 display tooltip fields,
validates all mathematical and count constraints, and exports:
- university_final_dataset.csv
- university_final_dataset.xlsx
"""

import os
import sys
import pandas as pd
import numpy as np


def engineer_kpis(integrated_csv_path):
    """
    Computes KPIs and display formatting fields from the integrated dataset.
    """
    print(f"Loading integrated dataset from: {integrated_csv_path}")
    df = pd.read_csv(integrated_csv_path)
    assert len(df) == 1503, f"Expected 1,503 rows, found {len(df)}"

    # ---------------------------------------------------------
    # KPI 1: KPI_Global_Ranking_Score (QS Overall_Score)
    # ---------------------------------------------------------
    df['KPI_Global_Ranking_Score'] = pd.to_numeric(df['Overall_Score'], errors='coerce')

    # ---------------------------------------------------------
    # KPI 2: KPI_Academic_Reputation_Score (QS Academic_Reputation_Score)
    # ---------------------------------------------------------
    df['KPI_Academic_Reputation_Score'] = pd.to_numeric(df['Academic_Reputation_Score'], errors='coerce')

    # ---------------------------------------------------------
    # KPI 3: KPI_Faculty_to_Student_Ratio (THE No. of Students per Staff)
    # Represents Average Students per Staff (not 1:X)
    # ---------------------------------------------------------
    df['KPI_Faculty_to_Student_Ratio'] = pd.to_numeric(df['THE_No_of_Students_per_Staff'], errors='coerce')

    # ---------------------------------------------------------
    # KPI 4: KPI_International_Student_Pct (THE International Students * 100)
    # Raw values are 0-1 proportions e.g. 0.43 -> 43.0%
    # ---------------------------------------------------------
    raw_intl = pd.to_numeric(df['THE_International_Students'], errors='coerce')
    df['KPI_International_Student_Pct'] = raw_intl * 100.0

    # ---------------------------------------------------------
    # KPI 5: KPI_Research_Impact_Score (QS Citations_per_Faculty_Score)
    # ---------------------------------------------------------
    df['KPI_Research_Impact_Score'] = pd.to_numeric(df['Citations_per_Faculty_Score'], errors='coerce')

    # ---------------------------------------------------------
    # KPI 6: KPI_Research_Productivity_Proxy (THE Research Environment)
    # Analytical proxy only, NOT official THE Research Productivity metric
    # ---------------------------------------------------------
    df['KPI_Research_Productivity_Proxy'] = pd.to_numeric(df['THE_Research_Environment'], errors='coerce')

    # ---------------------------------------------------------
    # Tooltip / Presentation Display Fields
    # ---------------------------------------------------------
    df['Display_Students_per_Staff'] = df['KPI_Faculty_to_Student_Ratio'].apply(
        lambda x: f"{x:.1f} students/staff" if pd.notna(x) else "Sourced from THE (Data not available)"
    )

    df['Display_Int_Student_Pct'] = df['KPI_International_Student_Pct'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "Sourced from THE (Data not available)"
    )

    df['Display_Research_Productivity'] = df['KPI_Research_Productivity_Proxy'].apply(
        lambda x: f"{x:.1f} pts" if pd.notna(x) else "THE Environment Proxy (Data not available)"
    )

    return df


def validate_dataset(df):
    """
    Executes validation checks against specified thresholds.
    """
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE DATA VALIDATION CHECKS")
    print("=" * 60)

    # 1. Row counts
    total_rows = len(df)
    print(f"[CHECK] Total institutions: {total_rows} (Expected: 1,503)")
    assert total_rows == 1503, f"Failed: {total_rows} != 1503"

    total_countries = df['Location'].nunique()
    print(f"[CHECK] Total countries: {total_countries} (Expected: 106)")
    assert total_countries == 106, f"Failed: {total_countries} != 106"

    us_count = (df['Location'] == 'United States').sum()
    print(f"[CHECK] United States institutions: {us_count} (Expected: 197)")
    assert us_count == 197, f"Failed: {us_count} != 197"

    matched_the = df['THE_University_Name'].notna().sum()
    print(f"[CHECK] Matched QS-THE institutions: {matched_the} (Expected: 195)")
    assert matched_the == 195, f"Failed: {matched_the} != 195"

    unmatched_the = df['THE_University_Name'].isna().sum()
    print(f"[CHECK] Unmatched THE institutions: {unmatched_the} (Expected: 1,308)")
    assert unmatched_the == 1308, f"Failed: {unmatched_the} != 1308"

    # 2. RES. field counts
    res_counts = df['RES.'].value_counts().to_dict()
    print(f"[CHECK] Research intensity (RES.): {res_counts}")
    assert res_counts.get('VH') == 1021, "RES. VH count mismatch"
    assert res_counts.get('HI') == 362, "RES. HI count mismatch"
    assert res_counts.get('MD') == 104, "RES. MD count mismatch"
    assert res_counts.get('LO') == 16, "RES. LO count mismatch"

    # 3. KPI 1: KPI_Global_Ranking_Score
    kpi1 = df['KPI_Global_Ranking_Score']
    kpi1_nonnull = kpi1.notna().sum()
    kpi1_null = kpi1.isna().sum()
    kpi1_min = round(kpi1.min(), 2)
    kpi1_max = round(kpi1.max(), 2)
    kpi1_mean = round(kpi1.mean(), 2)
    print(f"[CHECK] KPI 1 (Global Ranking Score): non-null={kpi1_nonnull}, null={kpi1_null}, min={kpi1_min}, max={kpi1_max}, mean={kpi1_mean}")
    assert kpi1_nonnull == 600, f"KPI 1 non-null mismatch: {kpi1_nonnull} != 600"
    assert kpi1_null == 903, f"KPI 1 null mismatch: {kpi1_null} != 903"
    assert kpi1_min == 20.80, f"KPI 1 min mismatch: {kpi1_min} != 20.80"
    assert kpi1_max == 100.0, f"KPI 1 max mismatch: {kpi1_max} != 100.0"
    assert kpi1_mean == 41.84, f"KPI 1 mean mismatch: {kpi1_mean} != 41.84"

    # 4. KPI 2: KPI_Academic_Reputation_Score
    kpi2 = df['KPI_Academic_Reputation_Score']
    kpi2_nonnull = kpi2.notna().sum()
    kpi2_min = round(kpi2.min(), 2)
    kpi2_max = round(kpi2.max(), 2)
    kpi2_mean = round(kpi2.mean(), 2)
    print(f"[CHECK] KPI 2 (Academic Reputation): non-null={kpi2_nonnull}, min={kpi2_min}, max={kpi2_max}, mean={kpi2_mean}")
    assert kpi2_nonnull == 1503, f"KPI 2 non-null mismatch: {kpi2_nonnull} != 1503"
    assert kpi2_min == 1.30, f"KPI 2 min mismatch: {kpi2_min} != 1.30"
    assert kpi2_max == 100.0, f"KPI 2 max mismatch: {kpi2_max} != 100.0"
    assert kpi2_mean == 20.29, f"KPI 2 mean mismatch: {kpi2_mean} != 20.29"

    # 5. KPI 3: KPI_Faculty_to_Student_Ratio (Students per Staff)
    kpi3 = df['KPI_Faculty_to_Student_Ratio']
    kpi3_nonnull = kpi3.notna().sum()
    kpi3_null = kpi3.isna().sum()
    kpi3_min = round(kpi3.min(), 2)
    kpi3_max = round(kpi3.max(), 2)
    kpi3_mean = round(kpi3.mean(), 2)
    print(f"[CHECK] KPI 3 (Students per Staff): non-null={kpi3_nonnull}, null={kpi3_null}, min={kpi3_min}, max={kpi3_max}, mean={kpi3_mean}")
    assert kpi3_nonnull == 195, f"KPI 3 non-null mismatch: {kpi3_nonnull} != 195"
    assert kpi3_null == 1308, f"KPI 3 null mismatch: {kpi3_null} != 1308"
    assert kpi3_min == 3.80, f"KPI 3 min mismatch: {kpi3_min} != 3.80"
    assert kpi3_max == 58.0, f"KPI 3 max mismatch: {kpi3_max} != 58.0"
    assert kpi3_mean == 17.44, f"KPI 3 mean mismatch: {kpi3_mean} != 17.44"

    # 6. KPI 4: KPI_International_Student_Pct
    kpi4 = df['KPI_International_Student_Pct']
    kpi4_nonnull = kpi4.notna().sum()
    kpi4_null = kpi4.isna().sum()
    kpi4_min = round(kpi4.min(), 2)
    kpi4_max = round(kpi4.max(), 2)
    kpi4_mean = round(kpi4.mean(), 2)
    print(f"[CHECK] KPI 4 (Intl Student Pct): non-null={kpi4_nonnull}, null={kpi4_null}, min={kpi4_min}%, max={kpi4_max}%, mean={kpi4_mean}%")
    assert kpi4_nonnull == 195, f"KPI 4 non-null mismatch: {kpi4_nonnull} != 195"
    assert kpi4_null == 1308, f"KPI 4 null mismatch: {kpi4_null} != 1308"
    assert kpi4_min == 1.0, f"KPI 4 min mismatch: {kpi4_min} != 1.0"
    assert kpi4_max == 72.0, f"KPI 4 max mismatch: {kpi4_max} != 72.0"
    assert kpi4_mean == 25.48, f"KPI 4 mean mismatch: {kpi4_mean} != 25.48"

    # 7. KPI 5: KPI_Research_Impact_Score
    kpi5 = df['KPI_Research_Impact_Score']
    kpi5_nonnull = kpi5.notna().sum()
    kpi5_min = round(kpi5.min(), 2)
    kpi5_max = round(kpi5.max(), 2)
    kpi5_mean = round(kpi5.mean(), 2)
    print(f"[CHECK] KPI 5 (Research Impact): non-null={kpi5_nonnull}, min={kpi5_min}, max={kpi5_max}, mean={kpi5_mean}")
    assert kpi5_nonnull == 1503, f"KPI 5 non-null mismatch: {kpi5_nonnull} != 1503"
    assert kpi5_min == 1.0, f"KPI 5 min mismatch: {kpi5_min} != 1.0"
    assert kpi5_max == 100.0, f"KPI 5 max mismatch: {kpi5_max} != 100.0"
    assert kpi5_mean == 23.50, f"KPI 5 mean mismatch: {kpi5_mean} != 23.50"

    # 8. KPI 6: KPI_Research_Productivity_Proxy
    kpi6 = df['KPI_Research_Productivity_Proxy']
    kpi6_nonnull = kpi6.notna().sum()
    kpi6_null = kpi6.isna().sum()
    kpi6_min = round(kpi6.min(), 2)
    kpi6_max = round(kpi6.max(), 2)
    kpi6_mean = round(kpi6.mean(), 2)
    print(f"[CHECK] KPI 6 (Research Productivity Proxy): non-null={kpi6_nonnull}, null={kpi6_null}, min={kpi6_min}, max={kpi6_max}, mean={kpi6_mean}")
    assert kpi6_nonnull == 195, f"KPI 6 non-null mismatch: {kpi6_nonnull} != 195"
    assert kpi6_null == 1308, f"KPI 6 null mismatch: {kpi6_null} != 1308"
    assert kpi6_min == 34.90, f"KPI 6 min mismatch: {kpi6_min} != 34.90"
    assert kpi6_max == 100.0, f"KPI 6 max mismatch: {kpi6_max} != 100.0"
    assert kpi6_mean == 61.23, f"KPI 6 mean mismatch: {kpi6_mean} != 61.23"

    print("=" * 60)
    print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
    print("=" * 60 + "\n")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_dir = os.path.dirname(base_dir)
    processed_dir = os.path.join(base_dir, 'data', 'processed')

    integrated_path = os.path.join(processed_dir, 'qs_the_integrated.csv')
    df = engineer_kpis(integrated_path)

    # Validate dataset
    validate_dataset(df)

    # Export locations:
    # 1. Inside EduVision_DV
    csv_path_edu = os.path.join(base_dir, 'university_final_dataset.csv')
    xlsx_path_edu = os.path.join(base_dir, 'university_final_dataset.xlsx')

    # 2. Workspace root for convenience
    csv_path_ws = os.path.join(workspace_dir, 'university_final_dataset.csv')
    xlsx_path_ws = os.path.join(workspace_dir, 'university_final_dataset.xlsx')

    print(f"Exporting final CSV to: {csv_path_edu}")
    df.to_csv(csv_path_edu, index=False, encoding='utf-8')
    if csv_path_ws != csv_path_edu:
        df.to_csv(csv_path_ws, index=False, encoding='utf-8')

    print(f"Exporting final Excel to: {xlsx_path_edu}")
    df.to_excel(xlsx_path_edu, index=False, engine='openpyxl')
    if xlsx_path_ws != xlsx_path_edu:
        df.to_excel(xlsx_path_ws, index=False, engine='openpyxl')

    print("Final datasets successfully exported in CSV and XLSX formats.")


if __name__ == '__main__':
    main()
