#!/usr/bin/env python3
"""
prepare_eduvision_data.py  -  EduVision_DV data preparation (Milestones 1-2)

What it does, in order:
  1. Loads your CSV/XLSX (tries several encodings)
  2. Repairs garbled text (Ã¤ -> ä, etc.)
  3. Maps your column names to the names your Tableau sheets already use
  4. Optionally merges student columns from a second file (--extra)
  5. Standardizes country names and adds Region
  6. Adds Year if missing, removes duplicates, converts numbers
  7. Derives International Students / International Student % when possible
  8. Adds Global Rank and 0-100 normalized KPI columns
  9. Writes Tableau-ready files + country summary + radar-chart data
 10. Writes a data-quality report and expected KPI values for QA

Usage:
  python prepare_eduvision_data.py university_cleaned.csv
  python prepare_eduvision_data.py university_cleaned.csv --extra students.csv --year 2024
  python prepare_eduvision_data.py university_cleaned.csv --impute
"""
import argparse
import math
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

KPIS = [
    "Academic Reputation Score",
    "Faculty Student Ratio",
    "Global Ranking Score",
    "Research Impact Score",
    "Research Productivity Index",
]

# --------------------------------------------------------------------------
# Country standardization and regions
# --------------------------------------------------------------------------
COUNTRY_FIX = {
    "usa": "United States", "us": "United States", "u.s.": "United States",
    "united states of america": "United States",
    "uk": "United Kingdom", "u.k.": "United Kingdom", "great britain": "United Kingdom",
    "england": "United Kingdom", "scotland": "United Kingdom", "wales": "United Kingdom",
    "northern ireland": "United Kingdom",
    "russian federation": "Russia", "korea, south": "South Korea",
    "republic of korea": "South Korea", "korea": "South Korea",
    "mainland china": "China", "china (mainland)": "China", "peoples republic of china": "China",
    "hong kong sar": "Hong Kong", "hong kong sar, china": "Hong Kong",
    "taiwan, china": "Taiwan", "türkiye": "Turkey", "turkiye": "Turkey",
    "czechia": "Czech Republic", "viet nam": "Vietnam", "uae": "United Arab Emirates",
    "iran, islamic republic of": "Iran", "macau": "Macao", "macau sar": "Macao",
    "republic of ireland": "Ireland", "the netherlands": "Netherlands",
    "brunei darussalam": "Brunei", "palestinian territory, occupied": "Palestine",
    "palestinian territory": "Palestine", "syrian arab republic": "Syria",
    "lao people's democratic republic": "Laos", "libyan arab jamahiriya": "Libya",
    "bolivia, plurinational state of": "Bolivia", "venezuela, bolivarian republic of": "Venezuela",
    "tanzania, united republic of": "Tanzania", "moldova, republic of": "Moldova",
    "korea, republic of": "South Korea", "cote d'ivoire": "Ivory Coast",
    "côte d'ivoire": "Ivory Coast", "macedonia": "North Macedonia",
}

_REGION_LISTS = {
    "North America": ["United States", "Canada", "Mexico", "Puerto Rico", "Cuba", "Costa Rica",
                      "Panama", "Jamaica", "Guatemala", "Dominican Republic", "Honduras",
                      "El Salvador", "Nicaragua", "Trinidad and Tobago", "Turks and Caicos Islands",
                      "Bahamas", "Barbados", "Haiti", "Bermuda"],
    "South America": ["Brazil", "Argentina", "Chile", "Colombia", "Peru", "Ecuador", "Uruguay",
                      "Venezuela", "Bolivia", "Paraguay"],
    "Europe": ["United Kingdom", "Germany", "France", "Italy", "Spain", "Netherlands", "Switzerland",
               "Sweden", "Denmark", "Norway", "Finland", "Belgium", "Austria", "Ireland", "Poland",
               "Portugal", "Greece", "Czech Republic", "Hungary", "Russia", "Turkey", "Romania",
               "Bulgaria", "Croatia", "Serbia", "Slovenia", "Slovakia", "Estonia", "Latvia",
               "Lithuania", "Ukraine", "Iceland", "Luxembourg", "Cyprus", "Northern Cyprus", "Malta",
               "Belarus", "Bosnia and Herzegovina", "North Macedonia", "Albania", "Montenegro",
               "Moldova", "Kosovo"],
    "Asia": ["China", "Japan", "South Korea", "India", "Singapore", "Hong Kong", "Taiwan", "Macao",
             "Malaysia", "Thailand", "Indonesia", "Philippines", "Vietnam", "Pakistan", "Bangladesh",
             "Sri Lanka", "Nepal", "Iran", "Iraq", "Israel", "Saudi Arabia", "United Arab Emirates",
             "Qatar", "Kuwait", "Oman", "Bahrain", "Jordan", "Lebanon", "Kazakhstan", "Uzbekistan",
             "Kyrgyzstan", "Armenia", "Azerbaijan", "Georgia", "Mongolia", "Brunei", "Cambodia",
             "Myanmar", "Palestine", "Syria", "Yemen", "Afghanistan", "Turkmenistan", "Tajikistan", "Laos"],
    "Oceania": ["Australia", "New Zealand", "Fiji"],
    "Africa": ["South Africa", "Egypt", "Nigeria", "Kenya", "Ghana", "Morocco", "Tunisia", "Algeria",
               "Ethiopia", "Uganda", "Tanzania", "Zimbabwe", "Zambia", "Rwanda", "Senegal",
               "Cameroon", "Namibia", "Botswana", "Mauritius", "Sudan", "Libya", "Mozambique",
               "Malawi", "Angola", "Somalia", "Ivory Coast", "Benin", "Burkina Faso", "Madagascar",
               "Mali", "Niger", "Togo", "Gabon", "Congo", "Sierra Leone", "Liberia", "Gambia"],
}
REGION_OF = {c: r for r, cs in _REGION_LISTS.items() for c in cs}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def load_any(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"\nFile not found: {path}\nLooked in: {Path.cwd()}\n"
                         "Put the file in this folder or give the full path, e.g. --extra \"C:\\path\\to\\file.csv\"")
    if p.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(p)
    for enc in ("utf-8-sig", "cp1252", "latin1"):
        try:
            return pd.read_csv(p, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Could not read {path}")


def fix_text(s):
    """Repair UTF-8 text that was read as Latin-1/cp1252 (e.g. 'Ã¤' -> 'ä')."""
    if not isinstance(s, str) or not re.search("[ÃÂâ]", s):
        return s
    for enc in ("cp1252", "latin1"):
        try:
            return s.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return s


def norm(c):
    return re.sub(r"[^a-z0-9]", "", str(c).lower())


def name_key(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def to_num(s):
    if pd.api.types.is_numeric_dtype(s):
        return s
    cleaned = s.astype(str).str.replace(r"[%,\s]", "", regex=True)
    cleaned = cleaned.replace({"": np.nan, "nan": np.nan, "None": np.nan, "-": np.nan})
    return pd.to_numeric(cleaned, errors="coerce")


def clean_country(x):
    if not isinstance(x, str):
        return x
    x = x.strip()
    return COUNTRY_FIX.get(x.lower(), x)


# --------------------------------------------------------------------------
# Column matching
# --------------------------------------------------------------------------
def _intl(n):
    return "intl" in n or "international" in n


def _is_pct(l, n):
    return (_intl(n) and "student" in n and "score" not in n and "rank" not in n
            and ("%" in l or any(k in n for k in ("pc", "pct", "percent", "ratio"))))


def _is_intl_count(l, n):
    return (_intl(n) and "student" in n and "score" not in n and "rank" not in n
            and not _is_pct(l, n))


def _is_total(l, n):
    if _intl(n) or "ratio" in n or "score" in n or "faculty" in n or "rank" in n:
        return False
    return n == "students" or any(k in n for k in (
        "totalstudents", "numberstudents", "numberofstudents", "studentpopulation",
        "enrollment", "enrolment", "noofstudents", "numstudents"))


MATCHERS = [  # (canonical name, predicate on (lowercase name, normalized name))
    ("University Id", lambda l, n: n in {"universityid", "uniid", "institutionid", "id"}),
    ("University Name", lambda l, n: n in {"universityname", "university", "institution",
                                           "institutionname", "name", "school"}),
    ("Country", lambda l, n: n in {"country", "countryname", "location"}),
    ("Region", lambda l, n: n == "region"),
    ("Year", lambda l, n: n in {"year", "rankingyear"}),
    ("Academic Reputation Score", lambda l, n: "academic" in n and "reputation" in n),
    ("Faculty Student Ratio", lambda l, n: ("faculty" in n and "student" in n and "ratio" in n) or n == "fsr"),
    ("Global Ranking Score", lambda l, n: n in {"globalrankingscore", "overallscore", "overall"}),
    ("Research Impact Score", lambda l, n: "researchimpact" in n or n == "citationsscore"),
    ("Research Productivity Index", lambda l, n: "researchproductivity" in n),
    ("International Student %", _is_pct),          # must come before the count
    ("International Students", _is_intl_count),
    ("Total Students", _is_total),
]


def standardize_columns(df, log):
    used, rename = set(), {}
    log("Column mapping (your file -> dashboard name):")
    for canon, pred in MATCHERS:
        hit = next((c for c in df.columns if c not in used and pred(str(c).lower(), norm(c))), None)
        if hit is None:
            log(f"  {canon:<28} NOT FOUND")
        else:
            used.add(hit)
            rename[hit] = canon
            log(f"  {canon:<28} <- {hit}")
    return df.rename(columns=rename)


def merge_extra(df, path, log):
    ex = load_any(path)
    ex.columns = [fix_text(str(c)).strip() for c in ex.columns]
    for c in ex.columns:
        if not pd.api.types.is_numeric_dtype(ex[c]):
            ex[c] = ex[c].map(fix_text)
    log(f"Extra file: {path}")
    ex = standardize_columns(ex, log)
    if "University Name" not in ex:
        log("  WARNING: extra file has no university-name column; skipped.")
        return df
    keep = [c for c in ("Total Students", "International Students", "International Student %",
                        "Region", "Year", "Country") if c in ex.columns]
    ex = ex[["University Name"] + keep].copy()
    ex["_key"] = ex["University Name"].map(name_key)
    ex = ex.drop_duplicates("_key").drop(columns="University Name")
    df["_key"] = df["University Name"].map(name_key)
    merged = df.merge(ex, on="_key", how="left", suffixes=("", "_x"))
    for c in keep:
        if c + "_x" in merged:
            merged[c] = merged[c].combine_first(merged[c + "_x"]) if c in merged else merged[c + "_x"]
            merged = merged.drop(columns=c + "_x")
    matched = merged[[c for c in keep if c in merged]].notna().any(axis=1).sum()
    log(f"  Matched {matched} of {len(df)} universities by name.")
    return merged.drop(columns="_key")


# --------------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--extra", help="CSV/XLSX with student columns, merged by university name")
    ap.add_argument("--year", type=int, default=2024, help="used only if the file has no Year column")
    ap.add_argument("--impute", action="store_true", help="fill missing KPI values with country/global median")
    ap.add_argument("--min-unis", type=int, default=3, help="min universities per country in radar data")
    ap.add_argument("--out", default="output")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(exist_ok=True)
    report = []

    def log(m):
        print(m)
        report.append(m)

    # 1-2. load + repair text
    df = load_any(a.input)
    log(f"Loaded {len(df)} rows x {df.shape[1]} columns from {a.input}")
    df.columns = [fix_text(str(c)).strip() for c in df.columns]
    for c in df.columns:
        if not pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].map(fix_text).map(lambda s: s.strip() if isinstance(s, str) else s)

    # 3-4. column names + optional student data
    df = standardize_columns(df, log)
    if "University Name" not in df or "Country" not in df:
        raise SystemExit("Need at least a university name and country column. Check the mapping above.")
    if a.extra:
        df = merge_extra(df, a.extra, log)

    # 5. countries + regions
    df["Country"] = df["Country"].map(clean_country)
    mapped = df["Country"].map(REGION_OF)
    df["Region"] = df["Region"].fillna(mapped) if "Region" in df else mapped
    unmapped = sorted(df.loc[df["Region"].isna(), "Country"].dropna().unique())
    df["Region"] = df["Region"].fillna("Other")
    if unmapped:
        log(f"Countries with no region (set to 'Other', add them to _REGION_LISTS): {unmapped}")

    # 6. year, ids, duplicates, numbers
    if "Year" not in df:
        df["Year"] = a.year
        log(f"No Year column found - set Year = {a.year}. Trend charts need 2+ years of data.")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(a.year).astype(int)
    if "University Id" not in df:
        df["University Id"] = pd.factorize(df["University Name"])[0] + 1
        log("No University Id column found - generated one from university names.")
    df["University Id"] = df["University Id"].astype(str)

    num_cols = KPIS + ["Total Students", "International Students", "International Student %"]
    for c in num_cols:
        if c in df:
            df[c] = to_num(df[c])

    before = len(df)
    df = df.dropna(subset=["University Name", "Country"])
    df = df.drop_duplicates(subset=["University Id", "Year"])
    log(f"Removed {before - len(df)} duplicate/blank rows. {len(df)} remain.")

    # 7. derive student fields
    if "International Student %" in df and df["International Student %"].max() <= 1.0:
        df["International Student %"] *= 100
        log("International Student % looked like a 0-1 fraction; converted to 0-100.")
    has = lambda c: c in df and df[c].notna().any()
    if has("Total Students") and has("International Student %") and not has("International Students"):
        df["International Students"] = (df["Total Students"] * df["International Student %"] / 100).round()
        log("Derived International Students = Total Students x International Student % / 100")
    if has("Total Students") and has("International Students") and not has("International Student %"):
        df["International Student %"] = df["International Students"] / df["Total Students"] * 100
        log("Derived International Student % = International / Total x 100")
    for c in ("Total Students", "International Students", "International Student %"):
        if not has(c):
            log(f"WARNING: '{c}' is missing. Student Analytics needs it - use --extra to merge it.")

    # optional imputation
    if a.impute:
        for c in KPIS:
            if c in df:
                df[c] = df[c].fillna(df.groupby("Country")[c].transform("median")).fillna(df[c].median())
        log("Imputed missing KPI values (country median, then global median).")

    # 8. rank + normalized KPIs (0-100)
    if "Global Ranking Score" in df:
        df["Global Rank"] = df.groupby("Year")["Global Ranking Score"].rank(ascending=False, method="min")
    present_kpis = [c for c in KPIS if c in df]
    for c in present_kpis:
        lo, hi = df[c].min(), df[c].max()
        df[f"{c} (Norm)"] = 0.0 if hi == lo else (df[c] - lo) / (hi - lo) * 100

    # 9. outputs
    df.to_csv(out / "university_final_dataset.csv", index=False, encoding="utf-8-sig")
    try:
        df.to_excel(out / "university_final_dataset.xlsx", index=False)
    except Exception as e:  # openpyxl missing
        log(f"(Skipped .xlsx: {e}. Run: pip install openpyxl)")

    agg = {"Number of Universities": ("University Id", "nunique")}
    for c in present_kpis + ["International Student %"]:
        if c in df:
            agg[f"Avg {c}"] = (c, "mean")
    if "Total Students" in df:
        agg["Total Students"] = ("Total Students", "sum")
    cs = df.groupby(["Country", "Region", "Year"], as_index=False).agg(**agg).round(2)
    cs.to_csv(out / "country_summary.csv", index=False, encoding="utf-8-sig")

    # radar data: latest year, normalized KPIs averaged per country, pentagon coordinates
    latest = df[df["Year"] == df["Year"].max()]
    norm_cols = [f"{c} (Norm)" for c in present_kpis]
    rad = latest.groupby("Country")[norm_cols].mean()
    counts = latest.groupby("Country")["University Id"].nunique()
    rad = rad[counts >= a.min_unis]
    rows, n = [], len(norm_cols)
    for country, r in rad.iterrows():
        for i in range(n + 1):  # n+1 closes the polygon
            k = i % n
            ang = math.pi / 2 - 2 * math.pi * k / n
            v = float(r.iloc[k]) if pd.notna(r.iloc[k]) else 0.0
            rows.append({"Country": country, "Metric": present_kpis[k], "Value": round(v, 2),
                         "Path": i + 1, "X": round(v * math.cos(ang), 3), "Y": round(v * math.sin(ang), 3)})
    pd.DataFrame(rows).to_csv(out / "country_radar.csv", index=False, encoding="utf-8-sig")

    # expected KPI values for QA (compare against Tableau KPI cards)
    exp = {"Number of Universities": df["University Id"].nunique(), "Rows": len(df)}
    for c in present_kpis + ["International Student %"]:
        if c in df:
            exp[f"Avg {c}"] = round(df[c].mean(), 2)
    for c in ("Total Students", "International Students"):
        if has(c):
            exp[f"Sum {c}"] = float(df[c].sum())
    if has("Total Students") and has("International Students"):
        exp["Weighted International %"] = round(df["International Students"].sum() / df["Total Students"].sum() * 100, 2)
    pd.Series(exp, name="Expected value").to_csv(out / "expected_kpis.csv", index_label="KPI")

    # 10. quality report
    log("\n=== DATA QUALITY ===")
    key_cols = ["University Name", "Country", "Region", "Year"] + present_kpis + \
               [c for c in ("Total Students", "International Students", "International Student %") if c in df]
    all_ok = True
    for c in key_cols:
        miss = df[c].isna().mean() * 100
        ok = miss < 2
        all_ok &= ok
        log(f"  {c:<30} missing {miss:5.1f}%   {'OK' if ok else 'FAIL (target < 2%)'}")
    overall = (1 - df[key_cols].isna().mean().mean()) * 100
    log(f"Overall completeness: {overall:.1f}%  (target > 95%)  {'PASS' if overall > 95 else 'FAIL'}")
    bad = df["University Name"].astype(str).str.contains("Ã|Â|\ufffd", regex=True).sum()
    log(f"Names still garbled: {bad}" + ("" if bad == 0 else
        "  -> the source file lost those characters; re-download the original dataset and re-run."))
    log(f"Countries: {df['Country'].nunique()} | Regions: {df['Region'].nunique()} | Years: {[int(y) for y in sorted(df['Year'].unique())]}")
    (out / "data_quality_report.txt").write_text("\n".join(report), encoding="utf-8")
    log(f"\nDone. Files written to: {out.resolve()}")


if __name__ == "__main__":
    main()
