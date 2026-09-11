"""
validate_data.py — REAL DATA EDITION
--------------------------------------
STAGE 4. Quality-checks the integrated real dataset before it's loaded into
a BI tool.
"""
import os
import json
import pandas as pd

DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def validate():
    dim_university = pd.read_csv(os.path.join(DIR, "dim_university.csv"))
    core = pd.read_csv(os.path.join(DIR, "fact_ranking_core.csv"))
    country_ind = pd.read_csv(os.path.join(DIR, "fact_country_indicator.csv"))

    report = {}
    report["dim_university_rows"] = len(dim_university)
    report["dim_university_missing_country"] = int(dim_university["country"].isna().sum())
    report["dim_university_country_completeness_pct"] = round(
        (1 - dim_university["country"].isna().mean()) * 100, 2)

    report["fact_ranking_core_rows"] = len(core)
    report["fact_ranking_core_sources"] = core["source"].nunique()
    report["fact_ranking_core_year_range"] = f"{core['year'].min()}-{core['year'].max()}"
    dup_core = core.duplicated(subset=["university_id", "year", "source"]).sum()
    report["fact_ranking_core_duplicate_keys"] = int(dup_core)
    report["fact_ranking_core_missing_score"] = int(core["score_0_100"].isna().sum())
    report["fact_ranking_core_score_completeness_pct"] = round(
        (1 - core["score_0_100"].isna().mean()) * 100, 2)
    invalid_rank = int((core["world_rank"] < 1).sum())
    report["fact_ranking_core_invalid_rank"] = invalid_rank

    report["fact_country_indicator_rows"] = len(country_ind)
    report["fact_country_indicator_countries"] = int(country_ind["country"].nunique())
    report["fact_country_indicator_missing_value"] = int(country_ind["value"].isna().sum())

    total_records = report["dim_university_rows"] + report["fact_ranking_core_rows"] + report["fact_country_indicator_rows"]
    total_issues = (report["dim_university_missing_country"] + report["fact_ranking_core_duplicate_keys"]
                     + report["fact_ranking_core_missing_score"] + invalid_rank
                     + report["fact_country_indicator_missing_value"])
    report["total_records_checked"] = total_records
    report["total_issues_flagged"] = total_issues
    report["overall_completeness_pct"] = round((1 - total_issues / total_records) * 100, 2)

    with open(os.path.join(DIR, "data_quality_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    pd.DataFrame([report]).to_csv(os.path.join(DIR, "data_quality_report.csv"), index=False)

    print("=" * 64)
    print("DATA QUALITY REPORT — REAL EDUVISION_DV DATASET")
    print("=" * 64)
    for k, v in report.items():
        print(f"{k:42s}: {v}")
    print("=" * 64)
    return report


if __name__ == "__main__":
    validate()
