"""
data_integration.py — REAL DATA EDITION
------------------------------------------
STAGE 3. Integrates 4 independently-published university ranking sources
(THE/timesData, CWUR, ARWU/Shanghai, and a 2023 snapshot) plus 2 country-level
indicator sources into a coherent, BI-ready model.

This is the genuinely hard part of working with real multi-source ranking
data: THE, CWUR, and ARWU are run by three different organizations with
different methodologies, different score scales, and they don't agree on
how to spell "Massachusetts Institute of Technology" consistently across
years. We do NOT force their scores onto one blended number — that would
misrepresent each methodology. Instead:

  1. ENTITY RESOLUTION — build one dim_university from the union of every
     university name seen across all 4 ranking sources + the school/country
     lookup table, using a normalized key (lowercased, punctuation-stripped).
  2. SOURCE-FAITHFUL FACTS — each ranking source keeps its own fact table
     (fact_times, fact_cwur, fact_shanghai, fact_qs2023) linked to
     dim_university by FK, preserving its original columns/scale.
  3. CROSS-SOURCE CORE FACT — a unified fact_ranking_core table with just
     (university_id, year, source, world_rank, score_0_100) for the charts
     that DO want to compare methodologies side by side (each source's raw
     score is independently min-max rescaled to 0-100 for that comparison
     only — the per-source fact tables keep the untouched original scores).
  4. COUNTRY INDICATORS — expenditure + attainment long tables combined into
     one fact_country_indicator table, joined to dim_university's countries
     via name standardization.

Run: python3 data_integration.py   (after data_cleaning.py)
"""
import os
import re
import pandas as pd
import numpy as np

IN_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUT_DIR = IN_DIR


def norm_key(name):
    if pd.isna(name):
        return None
    s = str(name).lower().strip()
    s = re.sub(r"^the\s+", "", s)  # 'The University of Tokyo' -> 'University of Tokyo'
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


# Targeted aliases for cases a general rule can't safely handle without
# risking false merges elsewhere (e.g. stripping ", Singapore" generally
# would wrongly merge "University of California, Berkeley" with
# "University of California, San Diego" — different real campuses).
NAME_ALIASES = {
    "nanyangtechnologicaluniversitysingapore": "nanyangtechnologicaluniversity",
}


def resolve_key(name):
    k = norm_key(name)
    return NAME_ALIASES.get(k, k)


def minmax_0_100(s):
    lo, hi = s.min(), s.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(np.nan, index=s.index)
    return (s - lo) / (hi - lo) * 100


def build_dim_university():
    times = pd.read_csv(os.path.join(IN_DIR, "clean_times.csv"))
    cwur = pd.read_csv(os.path.join(IN_DIR, "clean_cwur.csv"))
    shanghai = pd.read_csv(os.path.join(IN_DIR, "clean_shanghai.csv"))
    qs2023 = pd.read_csv(os.path.join(IN_DIR, "clean_qs2023.csv"))
    school_country = pd.read_csv(os.path.join(IN_DIR, "clean_school_country.csv"))

    names_countries = []
    names_countries += list(zip(times["university_name"], times["country"]))
    names_countries += list(zip(cwur["institution"], cwur["country"]))
    names_countries += list(zip(shanghai["university_name"], [None] * len(shanghai)))  # no country col
    names_countries += list(zip(qs2023["university_name"], qs2023["country"]))
    names_countries += list(zip(school_country["school_name"], school_country["country"]))

    dim = pd.DataFrame(names_countries, columns=["university_name", "country"])
    dim["_key"] = dim["university_name"].apply(resolve_key)
    dim = dim.dropna(subset=["_key"])

    # prefer a non-null country for each key; fall back to school_and_country_table (most authoritative)
    country_lookup = school_country.copy()
    country_lookup["_key"] = country_lookup["school_name"].apply(resolve_key)
    country_map = dict(zip(country_lookup["_key"], country_lookup["country"]))

    dim = dim.sort_values("country", na_position="last").drop_duplicates(subset=["_key"], keep="first")
    dim["country"] = dim.apply(lambda r: country_map.get(r["_key"], r["country"]), axis=1)
    dim = dim.reset_index(drop=True)
    dim.insert(0, "university_id", ["UNI_%05d" % (i + 1) for i in range(len(dim))])

    unresolved_country = dim["country"].isna().sum()
    print(f"[dim_university] {len(dim)} distinct universities resolved across 4 ranking sources + lookup table")
    print(f"[dim_university] {unresolved_country} universities still missing a country after all lookups "
          f"({unresolved_country/len(dim)*100:.1f}%) — left null, not guessed")

    key_to_id = dict(zip(dim["_key"], dim["university_id"]))
    return dim.drop(columns=["_key"]), key_to_id


def attach_university_id(df, name_col, key_to_id):
    df = df.copy()
    df["_key"] = df[name_col].apply(resolve_key)
    df["university_id"] = df["_key"].map(key_to_id)
    unmatched = df["university_id"].isna().sum()
    return df.drop(columns=["_key"]), unmatched


def build_source_facts(key_to_id):
    times = pd.read_csv(os.path.join(IN_DIR, "clean_times.csv"))
    cwur = pd.read_csv(os.path.join(IN_DIR, "clean_cwur.csv"))
    shanghai = pd.read_csv(os.path.join(IN_DIR, "clean_shanghai.csv"))
    qs2023 = pd.read_csv(os.path.join(IN_DIR, "clean_qs2023.csv"))

    fact_times, u1 = attach_university_id(times, "university_name", key_to_id)
    fact_cwur, u2 = attach_university_id(cwur, "institution", key_to_id)
    fact_shanghai, u3 = attach_university_id(shanghai, "university_name", key_to_id)
    fact_qs2023, u4 = attach_university_id(qs2023, "university_name", key_to_id)

    print(f"[fact_times] {len(fact_times)} rows, {u1} unmatched university_id (0 expected — built from same source)")
    print(f"[fact_cwur] {len(fact_cwur)} rows, {u2} unmatched")
    print(f"[fact_shanghai] {len(fact_shanghai)} rows, {u3} unmatched")
    print(f"[fact_qs2023] {len(fact_qs2023)} rows, {u4} unmatched")

    fact_times.to_csv(os.path.join(OUT_DIR, "fact_times.csv"), index=False)
    fact_cwur.to_csv(os.path.join(OUT_DIR, "fact_cwur.csv"), index=False)
    fact_shanghai.to_csv(os.path.join(OUT_DIR, "fact_shanghai.csv"), index=False)
    fact_qs2023.to_csv(os.path.join(OUT_DIR, "fact_qs2023.csv"), index=False)
    return fact_times, fact_cwur, fact_shanghai, fact_qs2023


def build_ranking_core(fact_times, fact_cwur, fact_shanghai, fact_qs2023):
    """Cross-source comparable core: each source's score independently
    rescaled 0-100 WITHIN ITS OWN YEAR so 'better' always means higher,
    without blending methodologies together."""
    core_rows = []
    for df, source, rank_col, score_col in [
        (fact_times, "THE", "world_rank", "total_score"),
        (fact_cwur, "CWUR", "world_rank", "score"),
        (fact_shanghai, "ARWU/Shanghai", "world_rank", "total_score"),
        (fact_qs2023, "QS2023", "world_rank", "overall_score"),
    ]:
        tmp = df[["university_id", "year", rank_col, score_col]].copy()
        tmp.columns = ["university_id", "year", "world_rank", "raw_score"]
        tmp["score_0_100"] = tmp.groupby("year")["raw_score"].transform(minmax_0_100).round(1)
        tmp["source"] = source
        core_rows.append(tmp[["university_id", "year", "source", "world_rank", "raw_score", "score_0_100"]])
    core = pd.concat(core_rows, ignore_index=True)
    core = core.dropna(subset=["university_id"])
    core.to_csv(os.path.join(OUT_DIR, "fact_ranking_core.csv"), index=False)
    print(f"[fact_ranking_core] {len(core)} rows spanning {core['source'].nunique()} sources, "
          f"{core['year'].min()}-{core['year'].max()}")
    return core


def build_country_indicators():
    expenditure = pd.read_csv(os.path.join(IN_DIR, "clean_expenditure.csv"))
    attainment = pd.read_csv(os.path.join(IN_DIR, "clean_attainment.csv"))

    exp = expenditure.rename(columns={"expenditure_pct_gdp": "value"}).copy()
    exp["indicator"] = exp["institute_type"].str.strip() + " — " + exp["direct_expenditure_type"].str.strip() + " expenditure (% GDP)"
    exp["category"] = "expenditure"
    exp = exp[["country", "year", "indicator", "value", "category"]]

    att = attainment.rename(columns={"country_name": "country", "series_name": "indicator"}).copy()
    att["category"] = "attainment"
    att = att[["country", "year", "indicator", "value", "category"]]

    combined = pd.concat([exp, att], ignore_index=True)
    combined.to_csv(os.path.join(OUT_DIR, "fact_country_indicator.csv"), index=False)
    print(f"[fact_country_indicator] {len(combined)} rows ({len(exp)} expenditure + {len(att)} attainment), "
          f"{combined['country'].nunique()} countries")
    return combined


if __name__ == "__main__":
    dim_university, key_to_id = build_dim_university()
    dim_university.to_csv(os.path.join(OUT_DIR, "dim_university.csv"), index=False)
    fact_times, fact_cwur, fact_shanghai, fact_qs2023 = build_source_facts(key_to_id)
    build_ranking_core(fact_times, fact_cwur, fact_shanghai, fact_qs2023)
    build_country_indicators()
    print("\nIntegration complete: dim_university + 5 fact tables in data/processed/")
