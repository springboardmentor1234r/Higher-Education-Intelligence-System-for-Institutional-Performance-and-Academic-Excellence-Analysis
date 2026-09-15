
import os
import numpy as np
import pandas as pd

IN_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUT_XLSX = os.path.join(IN_DIR, "university_final_dataset.xlsx")
OUT_CSV = os.path.join(IN_DIR, "university_final_dataset.csv")



REGION_MAP = {
    "United States": "North America", "Canada": "North America", "Mexico": "North America",
    "Puerto Rico": "North America",
    "United Kingdom": "Europe", "Germany": "Europe", "France": "Europe", "Netherlands": "Europe",
    "Switzerland": "Europe", "Sweden": "Europe", "Austria": "Europe", "Belgium": "Europe",
    "Bulgaria": "Europe", "Croatia": "Europe", "Cyprus": "Europe", "Czech Republic": "Europe",
    "Denmark": "Europe", "Estonia": "Europe", "Finland": "Europe", "Greece": "Europe",
    "Hungary": "Europe", "Iceland": "Europe", "Italy": "Europe", "Latvia": "Europe",
    "Lithuania": "Europe", "Luxembourg": "Europe", "Norway": "Europe", "Poland": "Europe",
    "Portugal": "Europe", "Republic of Ireland": "Europe", "Romania": "Europe", "Russia": "Europe",
    "Serbia": "Europe", "Slovakia": "Europe", "Slovenia": "Europe", "Spain": "Europe",
    "Ukraine": "Europe", "Belarus": "Europe",
    "China": "Asia", "Japan": "Asia", "South Korea": "Asia", "Singapore": "Asia", "India": "Asia",
    "Hong Kong SAR": "Asia", "Macau": "Asia", "Taiwan": "Asia", "Malaysia": "Asia",
    "Indonesia": "Asia", "Thailand": "Asia", "Pakistan": "Asia", "Bangladesh": "Asia",
    "Israel": "Asia", "Turkey": "Asia", "Saudi Arabia": "Asia", "United Arab Emirates": "Asia",
    "Qatar": "Asia", "Jordan": "Asia", "Lebanon": "Asia", "Oman": "Asia", "Iran": "Asia",
    "Australia": "Oceania", "New Zealand": "Oceania",
    "Brazil": "South America", "Chile": "South America", "Argentina": "South America",
    "Colombia": "South America", "Uruguay": "South America",
    "South Africa": "Africa", "Egypt": "Africa", "Nigeria": "Africa", "Kenya": "Africa",
    "Ghana": "Africa", "Morocco": "Africa", "Uganda": "Africa",
}


def minmax_0_100(series):
    lo, hi = series.min(), series.max()
    if pd.isna(lo) or hi == lo:
        return pd.Series(np.nan, index=series.index)
    return ((series - lo) / (hi - lo) * 100).clip(0, 100)


def invert_rank_to_impact(rank_series, year_series):
    """CWUR publishes several fields as WORLD RANKS (1 = best), not scores.
    To use them as a 0-100 'higher is better' component, min-max normalize
    the rank within its year, then invert (100 - x) so rank 1 -> ~100."""
    df = pd.DataFrame({"rank": rank_series, "year": year_series})
    scaled = df.groupby("year")["rank"].transform(minmax_0_100)
    return 100 - scaled


def load_tables():
    dim = pd.read_csv(os.path.join(IN_DIR, "dim_university.csv"))
    times = pd.read_csv(os.path.join(IN_DIR, "fact_times.csv"))
    cwur = pd.read_csv(os.path.join(IN_DIR, "fact_cwur.csv"))
    shanghai = pd.read_csv(os.path.join(IN_DIR, "fact_shanghai.csv"))
    qs2023 = pd.read_csv(os.path.join(IN_DIR, "fact_qs2023.csv"))
    core = pd.read_csv(os.path.join(IN_DIR, "fact_ranking_core.csv"))
    return dim, times, cwur, shanghai, qs2023, core


def kpi_global_ranking_score(core):
    """1. GLOBAL RANKING SCORE
    Average of each covering source's within-year min-max-normalized score
    (fact_ranking_core.score_0_100), per (university_id, year). A university
    covered by more sources gets a score averaged across all of them; a
    university covered by only one source uses that source's score alone."""
    g = core.groupby(["university_id", "year"]).agg(
        global_ranking_score=("score_0_100", "mean"),
        sources_covered=("source", lambda s: ", ".join(sorted(s.unique()))),
        num_sources=("source", "nunique"),
    ).reset_index()
    g["global_ranking_score"] = g["global_ranking_score"].round(1)
    return g


def kpi_research_impact_score(times, cwur):
    """2. RESEARCH IMPACT SCORE
    Composite of every available real citation-impact signal:
      - THE 'citations' sub-score (already published 0-100 by THE)
      - CWUR 'citations' world rank, inverted+normalized to 0-100
    Averaged where more than one source covers a given university-year."""
    the_part = times[["university_id", "year", "citations"]].rename(
        columns={"citations": "the_citations_0_100"})

    cwur_c = cwur[["university_id", "year", "citations"]].copy()
    cwur_c["cwur_citations_impact"] = invert_rank_to_impact(cwur_c["citations"], cwur_c["year"])
    cwur_part = cwur_c[["university_id", "year", "cwur_citations_impact"]]

    merged = the_part.merge(cwur_part, on=["university_id", "year"], how="outer")
    merged["research_impact_score"] = merged[["the_citations_0_100", "cwur_citations_impact"]].mean(
        axis=1, skipna=True).round(1)
    return merged[["university_id", "year", "research_impact_score"]]


def kpi_faculty_student_ratio(times, qs2023):
    """3. FACULTY-TO-STUDENT RATIO
    Ratio = Total Students / Faculty. Sourced directly from published
    student_staff_ratio in THE (2011-2016) or QS2023 (2023) — whichever
    covers that university-year. Displayed as "1 : X"."""
    the_r = times[["university_id", "year", "student_staff_ratio"]]
    qs_r = qs2023[["university_id", "year", "student_staff_ratio"]]
    combined = pd.concat([the_r, qs_r], ignore_index=True).drop_duplicates(
        subset=["university_id", "year"])
    combined = combined.rename(columns={"student_staff_ratio": "faculty_student_ratio"})
    combined["faculty_student_ratio_display"] = combined["faculty_student_ratio"].apply(
        lambda x: f"1 : {x:.0f}" if pd.notna(x) else None)
    return combined


def kpi_international_student_pct(times, qs2023):
    """4. INTERNATIONAL STUDENT PERCENTAGE
    = International Students / Total Students * 100. Sourced directly from
    published international_students % in THE or QS2023 (already computed
    as a percentage by the original publisher)."""
    the_i = times[["university_id", "year", "international_students"]]
    qs_i = qs2023[["university_id", "year", "international_students"]]
    combined = pd.concat([the_i, qs_i], ignore_index=True).drop_duplicates(
        subset=["university_id", "year"])
    return combined.rename(columns={"international_students": "international_student_pct"})


def kpi_academic_reputation_score(times):
    """5. ACADEMIC REPUTATION SCORE
    DOCUMENTED PROXY: none of the 4 source extracts in this pipeline publish
    a standalone 'academic reputation survey' column (QS's real methodology
    has one, but it is not present in the WorldUniversityRankings2023.csv
    extract used here). THE's 'teaching' pillar score is used as the closest
    available real signal, since THE's own published methodology states the
    Teaching pillar incorporates a reputation survey component. This is
    reported as a proxy, not presented as a direct reputation measurement.
    Rows outside THE's 2011-2016 coverage (i.e. all 2023 QS rows) are left
    NULL rather than approximated further."""
    r = times[["university_id", "year", "teaching"]].rename(
        columns={"teaching": "academic_reputation_score"})
    return r


def kpi_research_productivity_index(cwur, shanghai):
    """6. RESEARCH PRODUCTIVITY INDEX
    Composite of every available real publication-VOLUME signal:
      - ARWU/Shanghai 'pub' sub-score (already published 0-100 by ARWU,
        representing papers indexed in Web of Science)
      - CWUR 'publications' world rank, inverted+normalized to 0-100
    Averaged where more than one source covers a given university-year."""
    shanghai_p = shanghai[["university_id", "year", "pub"]].rename(
        columns={"pub": "shanghai_pub_0_100"})

    cwur_p = cwur[["university_id", "year", "publications"]].copy()
    cwur_p["cwur_pub_impact"] = invert_rank_to_impact(cwur_p["publications"], cwur_p["year"])
    cwur_p = cwur_p[["university_id", "year", "cwur_pub_impact"]]

    merged = shanghai_p.merge(cwur_p, on=["university_id", "year"], how="outer")
    merged["research_productivity_index"] = merged[["shanghai_pub_0_100", "cwur_pub_impact"]].mean(
        axis=1, skipna=True).round(1)
    return merged[["university_id", "year", "research_productivity_index"]]


def build_final_dataset():
    dim, times, cwur, shanghai, qs2023, core = load_tables()

    grs = kpi_global_ranking_score(core)
    ris = kpi_research_impact_score(times, cwur)
    fsr = kpi_faculty_student_ratio(times, qs2023)
    isp = kpi_international_student_pct(times, qs2023)
    ars = kpi_academic_reputation_score(times)
    rpi = kpi_research_productivity_index(cwur, shanghai)


    final = grs.merge(ris, on=["university_id", "year"], how="left")
    final = final.merge(fsr, on=["university_id", "year"], how="left")
    final = final.merge(isp, on=["university_id", "year"], how="left")
    final = final.merge(ars, on=["university_id", "year"], how="left")
    final = final.merge(rpi, on=["university_id", "year"], how="left")


    final = final.merge(dim, on="university_id", how="left")
    final["region"] = final["country"].map(REGION_MAP)


    final = final[[
        "university_id", "university_name", "country", "region", "year",
        "num_sources", "sources_covered",
        "global_ranking_score", "research_impact_score",
        "faculty_student_ratio", "faculty_student_ratio_display",
        "international_student_pct", "academic_reputation_score",
        "research_productivity_index",
    ]].sort_values(["university_name", "year"]).reset_index(drop=True)


    final["year"] = final["year"].astype(int)

    return final


def print_kpi_completeness(df):
    kpi_cols = [
        "global_ranking_score", "research_impact_score", "faculty_student_ratio",
        "international_student_pct", "academic_reputation_score", "research_productivity_index",
    ]
    print("\n--- KPI COMPLETENESS (real data — gaps are genuine source limitations) ---")
    for col in kpi_cols:
        pct = df[col].notna().mean() * 100
        print(f"  {col:32s}: {pct:5.1f}% populated  ({df[col].notna().sum():>5} / {len(df)} rows)")


if __name__ == "__main__":
    final = build_final_dataset()
    print(f"[kpi] Final dataset: {len(final)} rows "
          f"({final['university_id'].nunique()} universities x up to "
          f"{final['year'].nunique()} years)")
    print_kpi_completeness(final)

    final.to_csv(OUT_CSV, index=False)
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        final.to_excel(writer, sheet_name="university_final_dataset", index=False)

        pd.DataFrame({
            "KPI": [
                "Global Ranking Score", "Research Impact Score", "Faculty-to-Student Ratio",
                "International Student %", "Academic Reputation Score", "Research Productivity Index",
            ],
            "Formula": [
                "mean(score_0_100) across all ranking sources covering that university-year; "
                "each source's raw score is min-max normalized to 0-100 within its own year first",
                "mean(THE citations sub-score [0-100], CWUR citations rank inverted+normalized [0-100])",
                "Total Students / Faculty Count, from THE or QS2023's published student_staff_ratio",
                "International Students / Total Students * 100, from THE or QS2023",
                "PROXY: THE 'Teaching' pillar score (THE's own methodology folds a reputation survey "
                "into this pillar). No source in this pipeline publishes a standalone academic "
                "reputation column. NULL for all non-THE-covered rows (e.g. 2023).",
                "mean(ARWU 'pub' sub-score [0-100], CWUR publications rank inverted+normalized [0-100])",
            ],
            "Source fields used": [
                "fact_ranking_core.score_0_100 (all 4 sources)",
                "fact_times.citations, fact_cwur.citations",
                "fact_times.student_staff_ratio, fact_qs2023.student_staff_ratio",
                "fact_times.international_students, fact_qs2023.international_students",
                "fact_times.teaching",
                "fact_shanghai.pub, fact_cwur.publications",
            ],
        }).to_excel(writer, sheet_name="KPI_Methodology", index=False)
    print(f"\n[kpi] wrote {OUT_XLSX}")
    print(f"[kpi] wrote {OUT_CSV}")
