"""
data_collection.py
============================================================================
MILESTONE 1 — Data Collection

Collects the 4 real university-ranking sources (THE, CWUR, ARWU/Shanghai,
QS2023-style) and stacks them into ONE consolidated raw file,
university_raw_data.csv — genuinely raw, i.e. BEFORE any cleaning:
column names, casing, and formatting are exactly as each source published
them (percent signs, comma-thousands, inconsistent country spelling, all
still present). This is deliberate: Milestone 1's cleaning stage needs real
messiness to demonstrate real cleaning.

The 3 country-level supplementary/reference sources (school_and_country
lookup, education expenditure, educational attainment) are kept as
separate files in data/raw/ — they're a different grain (country, not
university-year) and stacking them into the same table would just create
a wall of NULLs, not a meaningful "raw dataset."

Because the 4 sources have different column names for the same real-world
concepts (e.g. 'university_name' vs 'institution' vs 'Name of University'),
this script does ONE minimal, honest thing before stacking: renames each
source's own key identifying columns (name/country/year/rank) to a common
set of column names so they land in the SAME columns when stacked, while
leaving every source-specific column (citations, publications, teaching
score, etc.) completely untouched under its own original name. This is
NOT cleaning — it's the minimum alignment needed to stack rows at all.
Real cleaning (parsing "42%", standardizing "USA"/"United States", removing
duplicates) happens in Milestone 1's next stage, data_cleaning /
education_cleaning.ipynb, operating on this file.

Run: python3 data_collection.py
Output: university_raw_data.csv (in the same directory)
============================================================================
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_SOURCES_DIR = os.path.join(HERE, "raw_sources")  # the 4 original per-source files
OUT_PATH = os.path.join(HERE, "university_raw_data.csv")


def load_times():
    df = pd.read_csv(os.path.join(RAW_SOURCES_DIR, "timesData.csv"))
    df = df.rename(columns={"world_rank": "rank", "university_name": "name"})
    df["source"] = "THE"
    return df


def load_cwur():
    df = pd.read_csv(os.path.join(RAW_SOURCES_DIR, "cwurData.csv"))
    df = df.rename(columns={"world_rank": "rank", "institution": "name"})
    df["source"] = "CWUR"
    return df


def load_shanghai():
    df = pd.read_csv(os.path.join(RAW_SOURCES_DIR, "shanghaiData.csv"))
    df = df.rename(columns={"world_rank": "rank", "university_name": "name"})
    df["source"] = "ARWU"
    # ARWU's raw export has no country column at all — leave genuinely
    # absent rather than guessing one in, consistent with "don't fabricate."
    return df


def load_qs2023():
    df = pd.read_csv(os.path.join(RAW_SOURCES_DIR, "WorldUniversityRankings2023.csv"))
    df = df.rename(columns={
        "University Rank": "rank", "Name of University": "name", "Location": "country",
    })
    df["source"] = "QS2023"
    df["year"] = 2023  # this source is a single-year snapshot with no year column
    return df


if __name__ == "__main__":
    frames = [load_times(), load_cwur(), load_shanghai(), load_qs2023()]
    for f, label in zip(frames, ["THE", "CWUR", "ARWU", "QS2023"]):
        print(f"[collect] {label}: {len(f)} rows, {len(f.columns)} columns")

    # sort=False: preserve each source's own column order where possible,
    # union columns rather than intersect — a row from one source simply
    # has NaN for another source's columns it doesn't share, which is
    # correct (never fabricate a value that source didn't publish).
    raw = pd.concat(frames, ignore_index=True, sort=False)

    # Put the common identifying columns first for readability; everything
    # else keeps its original source-specific name and order.
    lead_cols = [c for c in ["source", "name", "country", "year", "rank"] if c in raw.columns]
    other_cols = [c for c in raw.columns if c not in lead_cols]
    raw = raw[lead_cols + other_cols]

    raw.to_csv(OUT_PATH, index=False)
    print(f"\n[collect] wrote {OUT_PATH}")
    print(f"[collect] {len(raw)} total raw rows, {len(raw.columns)} columns, "
          f"{raw['source'].value_counts().to_dict()}")
