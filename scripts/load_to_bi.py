"""
load_to_bi.py — REAL DATA EDITION
------------------------------------
STAGE 5 (final). Loads the real, integrated, validated EduVision_DV dataset
into a BI-ready warehouse: one SQLite database, one multi-sheet Excel
workbook, and flat CSVs — pick whichever your BI tool prefers.

Schema (6 tables):
  dim_university(university_id, university_name, country)
  fact_times(university_id, year, world_rank, total_score, teaching, research,
             citations, income, international, num_students,
             student_staff_ratio, international_students, female_male_ratio)
  fact_cwur(university_id, year, world_rank, national_rank, quality_of_education,
            alumni_employment, quality_of_faculty, publications, influence,
            citations, broad_impact, patents, score)
  fact_shanghai(university_id, year, world_rank, national_rank, total_score,
                alumni, award, hici, ns, pub, pcp)
  fact_qs2023(university_id, year, world_rank, overall_score, teaching_score,
              research_score, citations_score, industry_income_score,
              international_outlook_score, num_students, ...)
  fact_ranking_core(university_id, year, source, world_rank, raw_score, score_0_100)
      -- the cross-source comparable table; start here for most BI charts
  fact_country_indicator(country, year, indicator, value, category)

Run: python3 load_to_bi.py   (after validate_data.py)
"""
import os
import sqlite3
import pandas as pd

IN_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
WH_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "warehouse")
os.makedirs(WH_DIR, exist_ok=True)

TABLES = [
    "dim_university", "fact_times", "fact_cwur", "fact_shanghai",
    "fact_qs2023", "fact_ranking_core", "fact_country_indicator",
]


def load():
    frames = {name: pd.read_csv(os.path.join(IN_DIR, f"{name}.csv")) for name in TABLES}

    db_path = os.path.join(WH_DIR, "eduvision_real.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    for name, df in frames.items():
        df.to_sql(name, conn, index=False)
    conn.execute("CREATE INDEX idx_core_uni ON fact_ranking_core(university_id)")
    conn.execute("CREATE INDEX idx_core_year ON fact_ranking_core(year)")
    conn.execute("CREATE INDEX idx_core_source ON fact_ranking_core(source)")
    conn.execute("CREATE INDEX idx_ctry_country ON fact_country_indicator(country)")
    conn.execute("CREATE INDEX idx_ctry_year ON fact_country_indicator(year)")
    conn.commit()
    conn.close()
    print(f"[load] SQLite  -> {db_path}  ({len(TABLES)} tables, indexed)")

    xlsx_path = os.path.join(WH_DIR, "EduVision_Real_BI_Workbook.xlsx")
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        for name, df in frames.items():
            # Excel sheet cell limit guard — country_indicator/attainment can be large
            df.to_excel(writer, sheet_name=name[:31], index=False)
    print(f"[load] Excel   -> {xlsx_path}  ({len(TABLES)} sheets)")

    for name, df in frames.items():
        df.to_csv(os.path.join(WH_DIR, f"{name}.csv"), index=False)
    print(f"[load] CSVs    -> {WH_DIR}/*.csv ({len(TABLES)} files)")

    total = sum(len(df) for df in frames.values())
    print(f"\nLoad complete: {total:,} total rows across {len(TABLES)} tables, ready for BI import.")


if __name__ == "__main__":
    load()
