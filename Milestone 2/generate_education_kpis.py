"""
EduVision_DV - Milestone 2, Module 3: Education KPI Engineering
Infosys Springboard Virtual Internship Project

PURPOSE
-------
Derives the six required education KPIs from the cleaned and integrated dataset
produced in Milestone 1, validates every one of them, and exports the
Tableau-ready master dataset.

This script does NOT re-implement the KPI formulas. It imports the project's
single source of truth, scripts/kpi_engineering.py, so that the milestone
deliverable and the production pipeline can never drift apart.

INPUT
-----
Milestone 1/university_cleaned.csv
  (identical to data/processed/qs_the_integrated.csv - 1,503 x 43)

OUTPUT
------
Milestone 2/university_final_dataset.xlsx
Milestone 2/university_final_dataset.csv
  (identical to the project root university_final_dataset.* - 1,503 x 52)

THE SIX KPIs
------------
  1. Global Ranking Score          KPI_Global_Ranking_Score          QS Overall Score
  2. Research Impact Score         KPI_Research_Impact_Score         QS Citations per Faculty
  3. Faculty-to-Student Ratio      KPI_Faculty_to_Student_Ratio      THE Students per Staff
  4. International Student %       KPI_International_Student_Pct     THE International Students
  5. Academic Reputation Score     KPI_Academic_Reputation_Score     QS Academic Reputation
  6. Research Productivity Index   KPI_Research_Productivity_Proxy   THE Research Environment

IMPORTANT - KPI 6 NAMING
------------------------
The official specification calls this KPI "Research Productivity Index".
In this project it is implemented as KPI_Research_Productivity_Proxy and is
surfaced everywhere - dashboards, legends, tooltips and documentation - as
"Research Productivity (Proxy)".

It is derived from the THE Research Environment score. It is NOT Times Higher
Education's official Research Productivity metric, which was not available in
the source data. The proxy label is deliberate and must not be removed.

MISSING DATA POLICY
-------------------
KPIs 3, 4 and 6 are THE-derived and therefore exist only for the 195 QS
institutions matched to THE. For the other 1,308 they remain strictly null -
never zero-filled, never imputed.
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'scripts'))

import pandas as pd  # noqa: E402
from kpi_engineering import engineer_kpis, validate_dataset  # noqa: E402


def main():
    src = os.path.join(BASE, 'Milestone 1', 'university_cleaned.csv')
    if not os.path.exists(src):
        src = os.path.join(BASE, 'Milestone_1', 'university_cleaned.csv')
    if not os.path.exists(src):
        src = os.path.join(BASE, 'data', 'processed', 'qs_the_integrated.csv')
    if not os.path.exists(src):
        sys.exit(f"ERROR: cleaned dataset not found. Run Milestone 1 first.")

    print("=" * 70)
    print("MILESTONE 2 / MODULE 3 - EDUCATION KPI ENGINEERING")
    print("=" * 70)
    print(f"Input: {src}")

    df = engineer_kpis(src)
    validate_dataset(df)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, 'university_final_dataset.csv')
    xlsx_path = os.path.join(out_dir, 'university_final_dataset.xlsx')

    df.to_csv(csv_path, index=False, encoding='utf-8')
    df.to_excel(xlsx_path, index=False, engine='openpyxl')

    print(f"\nExported {csv_path} ({os.path.getsize(csv_path):,} bytes)")
    print(f"Exported {xlsx_path} ({os.path.getsize(xlsx_path):,} bytes)")
    print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

    print("\nKPI coverage (evaluation criterion: all KPIs correctly calculated):")
    kpis = [
        ('Global Ranking Score',        'KPI_Global_Ranking_Score'),
        ('Research Impact Score',       'KPI_Research_Impact_Score'),
        ('Faculty-to-Student Ratio',    'KPI_Faculty_to_Student_Ratio'),
        ('International Student %',     'KPI_International_Student_Pct'),
        ('Academic Reputation Score',   'KPI_Academic_Reputation_Score'),
        ('Research Productivity Index (Proxy)', 'KPI_Research_Productivity_Proxy'),
    ]
    for label, col in kpis:
        s = df[col]
        print(f"  {label:38s} non-null {s.notna().sum():5,}  "
              f"mean {s.mean():7.2f}  range {s.min():.1f}-{s.max():.1f}")
    print("=" * 70)


if __name__ == '__main__':
    main()
