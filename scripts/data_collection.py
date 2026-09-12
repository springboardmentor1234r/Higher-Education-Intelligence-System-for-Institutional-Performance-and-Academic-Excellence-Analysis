"""
data_collection.py
-------------------
STAGE 1 of the EduVision_DV pipeline — REAL DATA EDITION.

Unlike the earlier synthetic-demo build, every file this stage points to is
REAL, PUBLICLY RELEASED higher-education data, collected from 7 sources
across 3 independent university-ranking methodologies plus 2 country-level
supplementary indicator sets. Nothing here is generated or fabricated.

  SOURCE                                    FORMAT  ROWS    YEARS       GRAIN
  ------------------------------------------------------------------------------
  timesData.csv                             CSV     2,603   2011-2016   university x year
  cwurData.csv                              CSV     2,200   2012-2015   university x year
  shanghaiData.csv                          CSV     4,897   2005-2015   university x year
  WorldUniversityRankings2023.csv           CSV       100   2023        university (top 100)
  school_and_country_table.csv              CSV       818   -           university -> country lookup
  education_expenditure_supplementary_data  CSV       333   1995-2011   country x institute type
  educational_attainment_supplementary_data CSV    79,055   1985-2015   country x attainment series

  TOTAL: ~90,000 real records

PROVENANCE & LICENSING
-----------------------
- timesData.csv / cwurData.csv / shanghaiData.csv / school_and_country_table.csv /
  education_expenditure_supplementary_data.csv / educational_attainment_supplementary_data.csv
  originate from the "World University Rankings" dataset originally compiled
  and released on Kaggle (CC0 / public domain) by Kaggle user mylesoneill,
  combining published rankings from Times Higher Education (THE), the Center
  for World University Rankings (CWUR), and the Shanghai Academic Ranking of
  World Universities (ARWU), plus World Bank/Barro-Lee supplementary
  indicators. Mirrored here from a public GitHub repository:
  https://github.com/arnaudbenard/university-ranking

- WorldUniversityRankings2023.csv is a 2023-edition ranking snapshot mirrored
  in a public coursework repository:
  https://github.com/nogibjj/IDS-Week7_MiniProject_us26
  Treat this one as DEMO/EDUCATIONAL USE — verify licensing with the original
  publisher (Times Higher Education) before any commercial or redistributive
  use; it is not confirmed CC0 like the others.

IMPORTANT — these rankings are HISTORICAL (2005-2016, plus a 2023 snapshot),
not live/current data. This pipeline treats them as exactly what they are:
real historical ranking editions, suitable for trend analysis, methodology
comparison, and BI demonstration — not as a live QS/THE feed.

Run: python3 data_collection.py
(This stage just verifies the raw files are present and prints their real
 shape — the files themselves were already fetched into data/raw/.)
"""
import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

SOURCES = [
    ("timesData.csv", "Times Higher Education (THE) World University Rankings, 2011-2016"),
    ("cwurData.csv", "Center for World University Rankings (CWUR), 2012-2015"),
    ("shanghaiData.csv", "Academic Ranking of World Universities / Shanghai (ARWU), 2005-2015"),
    ("WorldUniversityRankings2023.csv", "2023-edition ranking snapshot (top 100)"),
    ("school_and_country_table.csv", "University -> country reference lookup"),
    ("education_expenditure_supplementary_data.csv", "Country-level education expenditure, 1995-2011"),
    ("educational_attainment_supplementary_data.csv", "Country-level Barro-Lee educational attainment, 1985-2015"),
]

if __name__ == "__main__":
    total_rows = 0
    for fname, desc in SOURCES:
        path = os.path.join(RAW_DIR, fname)
        if not os.path.exists(path):
            print(f"[MISSING] {fname} — expected in data/raw/")
            continue
        needs_python_engine = fname in (
            "educational_attainment_supplementary_data.csv",
            "education_expenditure_supplementary_data.csv",
        )
        df = pd.read_csv(path, engine="python" if needs_python_engine else "c")
        total_rows += len(df)
        print(f"[verified] {fname:48s} {df.shape[0]:>7,} rows x {df.shape[1]:>2} cols  — {desc}")
    print(f"\nTotal real records collected across {len(SOURCES)} sources: {total_rows:,}")
