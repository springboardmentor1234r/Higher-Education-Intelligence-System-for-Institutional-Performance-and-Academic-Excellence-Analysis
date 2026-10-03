import os
import json
import pandas as pd
import numpy as np

raw_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\raw"
doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"

os.makedirs(doc_dir, exist_ok=True)

# Helper to read csv safely
def safe_read_csv(path):
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='latin1', low_memory=False)

qs_path = os.path.join(raw_dir, "QS_Ranking", "QS World University Rankings 2025 (Top global universities).csv")
the_path = os.path.join(raw_dir, "World_Ranking", "World University Rankings 2023.csv")
ed_data_path = os.path.join(raw_dir, "archive (8)", "edstats-csv-zip-32-mb-", "EdStatsData.csv")
ed_country_path = os.path.join(raw_dir, "archive (8)", "edstats-csv-zip-32-mb-", "EdStatsCountry.csv")

print("Loading datasets...", flush=True)
df_qs = safe_read_csv(qs_path)
df_the = safe_read_csv(the_path)
df_ed_data = safe_read_csv(ed_data_path)
df_ed_country = safe_read_csv(ed_country_path)

dict_entries = []

def profile_df(df, dataset_name):
    entries = []
    num_rows = len(df)
    for col in df.columns:
        col_str = str(col)
        dtype = str(df[col].dtype)
        
        null_cnt = int(df[col].isnull().sum())
        missing_pct = round((null_cnt / num_rows * 100), 2)
        
        valid_series = df[col].dropna()
        if len(valid_series) > 0:
            example_val = str(valid_series.iloc[0])
            if len(example_val) > 50:
                example_val = example_val[:47] + "..."
        else:
            example_val = "N/A (All Null)"
            
        lcol = col_str.lower().strip()
        
        std_col = col_str.lower().replace(" ", "_").replace(":", "_").replace(".", "_").replace("-", "_")
        meaning = ""
        unit = "N/A"
        is_identifier = "No"
        univ_overview = "No"
        research_analytics = "No"
        student_analytics = "No"
        country_comp = "No"
        kpi_support = "None"
        
        # 1. QS 2025 Specific Mapping
        if dataset_name == "QS World University Rankings 2025":
            if lcol in ["rank_2025", "rank_2024"]:
                std_col = lcol
                meaning = f"Global rank position assigned by QS for year {lcol[-4:]}"
                unit = "Rank Position"
                univ_overview = "Yes"
                country_comp = "Yes"
                kpi_support = "KPI 1: Global Ranking Score (Rank component)"
            elif lcol == "institution_name":
                std_col = "university_name"
                meaning = "Official name of the higher education institution"
                is_identifier = "Yes (Primary)"
                univ_overview = "Yes"
                research_analytics = "Yes"
                student_analytics = "Yes"
            elif lcol in ["location", "region"]:
                std_col = "country" if lcol == "location" else "region"
                meaning = "Country location of the university" if lcol == "location" else "Geographic world region"
                univ_overview = "Yes"
                country_comp = "Yes"
            elif lcol in ["size", "focus", "res.", "status"]:
                std_col = lcol.replace(".", "")
                meaning = f"QS Institutional classification category for {lcol}"
                univ_overview = "Yes"
            elif "academic_reputation" in lcol:
                std_col = lcol
                meaning = "Academic reputation survey score or rank"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                univ_overview = "Yes"
                research_analytics = "Yes"
                if "score" in lcol:
                    kpi_support = "KPI 5: Academic Reputation Score (Actual Score)"
            elif "employer_reputation" in lcol:
                std_col = lcol
                meaning = "Employer reputation survey score or rank"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                univ_overview = "Yes"
            elif "faculty_student" in lcol:
                std_col = lcol
                meaning = "Faculty-to-student score or rank (Note: Benchmark Score 0-100, not actual ratio)"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                student_analytics = "Yes"
                if "score" in lcol:
                    kpi_support = "KPI 3: Faculty-to-Student Ratio (Proxy Score; Actual Ratio requires derived calculation)"
            elif "citations_per_faculty" in lcol:
                std_col = lcol
                meaning = "Citations per faculty score or rank (Note: Benchmark Score 0-100, not raw citation count)"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                research_analytics = "Yes"
                if "score" in lcol:
                    kpi_support = "KPI 2: Research Impact Score (Actual Score)"
            elif "international_faculty" in lcol:
                std_col = lcol
                meaning = "Proportion of international faculty score or rank"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                student_analytics = "Yes"
            elif "international_students" in lcol:
                std_col = lcol
                meaning = "Proportion of international students score or rank (Note: Benchmark Score 0-100, not actual percentage)"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                student_analytics = "Yes"
                if "score" in lcol:
                    kpi_support = "KPI 4: International Student Percentage (Proxy Score; Actual % requires derived calculation)"
            elif "international_research_network" in lcol:
                std_col = lcol
                meaning = "Diversity of international research collaboration score or rank"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                research_analytics = "Yes"
                if "score" in lcol:
                    kpi_support = "KPI 6: Research Productivity Index (Proxy Score; Raw productivity requires derived calculation)"
            elif "employment_outcomes" in lcol or "sustainability" in lcol:
                std_col = lcol
                meaning = f"{lcol.replace('_', ' ').capitalize()} metric score or rank"
                unit = "Score (0-100)" if "score" in lcol else "Rank Position"
                univ_overview = "Yes"
            elif lcol == "overall_score":
                std_col = "overall_score"
                meaning = "Consolidated overall QS global benchmark score"
                unit = "Score (0-100)"
                univ_overview = "Yes"
                country_comp = "Yes"
                kpi_support = "KPI 1: Global Ranking Score (Actual Score)"

        # 2. THE 2023 Specific Mapping
        elif dataset_name == "THE World University Rankings 2023":
            if lcol == "university rank":
                std_col = "world_rank"
                meaning = "Global rank position assigned by Times Higher Education 2023"
                unit = "Rank Position"
                univ_overview = "Yes"
                country_comp = "Yes"
                kpi_support = "KPI 1: Global Ranking Score (Rank component)"
            elif lcol == "name of university":
                std_col = "university_name"
                meaning = "Official institution name"
                is_identifier = "Yes (Primary)"
                univ_overview = "Yes"
                research_analytics = "Yes"
                student_analytics = "Yes"
            elif lcol == "location":
                std_col = "country"
                meaning = "Country or territory where institution is located"
                univ_overview = "Yes"
                country_comp = "Yes"
            elif lcol == "no of student":
                std_col = "num_students"
                meaning = "Total full-time equivalent (FTE) student enrollment"
                unit = "Count (Headcount)"
                student_analytics = "Yes"
                univ_overview = "Yes"
                kpi_support = "KPI 3 & 4: Supporting metric for actual student counts"
            elif lcol == "no of student per staff":
                std_col = "student_staff_ratio"
                meaning = "Actual number of FTE students per staff member"
                unit = "Ratio (Students : 1 Staff)"
                student_analytics = "Yes"
                kpi_support = "KPI 3: Faculty-to-Student Ratio (Actual Ratio)"
            elif lcol == "international student":
                std_col = "pct_international_students"
                meaning = "Actual percentage of international students enrolled"
                unit = "Percentage (%)"
                student_analytics = "Yes"
                country_comp = "Yes"
                kpi_support = "KPI 4: International Student Percentage (Actual Percentage)"
            elif lcol == "female:male ratio":
                std_col = "female_male_ratio"
                meaning = "Proportion of female to male students"
                unit = "Ratio (Female : Male)"
                student_analytics = "Yes"
            elif lcol == "overall score":
                std_col = "overall_score"
                meaning = "Consolidated overall THE benchmark score"
                unit = "Score (0-100)"
                univ_overview = "Yes"
                country_comp = "Yes"
                kpi_support = "KPI 1: Global Ranking Score (Actual Score)"
            elif lcol == "teaching score":
                std_col = "teaching_score"
                meaning = "Teaching environment score (includes academic reputation & staff ratios)"
                unit = "Score (0-100)"
                univ_overview = "Yes"
                student_analytics = "Yes"
                kpi_support = "KPI 5: Academic Reputation Score (Partial teaching/reputation proxy)"
            elif lcol == "research score":
                std_col = "research_score"
                meaning = "Research reputation, income, and volume score"
                unit = "Score (0-100)"
                research_analytics = "Yes"
                kpi_support = "KPI 6: Research Productivity Index (Score component)"
            elif lcol == "citations score":
                std_col = "citations_score"
                meaning = "Research citation impact score"
                unit = "Score (0-100)"
                research_analytics = "Yes"
                kpi_support = "KPI 2: Research Impact Score (Actual Score)"
            elif lcol == "industry income score":
                std_col = "industry_income_score"
                meaning = "Knowledge transfer and industry research funding score"
                unit = "Score (0-100)"
                research_analytics = "Yes"
            elif lcol == "international outlook score":
                std_col = "international_outlook_score"
                meaning = "Combined international staff, student, and research collaboration score"
                unit = "Score (0-100)"
                student_analytics = "Yes"
                country_comp = "Yes"

        # 3. EdStatsData Specific Mapping
        elif dataset_name == "World Bank Education Statistics (Data)":
            if lcol == "country name":
                std_col = "country_name"
                meaning = "Standardized country or region name"
                is_identifier = "Yes"
                country_comp = "Yes"
            elif lcol == "country code":
                std_col = "country_code"
                meaning = "ISO 3-letter country/region code"
                is_identifier = "Yes (ISO Alpha-3)"
                country_comp = "Yes"
            elif lcol == "indicator name":
                std_col = "indicator_name"
                meaning = "Description of global education / economic indicator"
                country_comp = "Yes"
                kpi_support = "Country Comparison macro metrics (e.g. Tertiary Enrollment %)"
            elif lcol == "indicator code":
                std_col = "indicator_code"
                meaning = "Unique World Bank series code"
                is_identifier = "Yes (Series ID)"
                country_comp = "Yes"
            elif col_str.isdigit() and len(col_str) == 4:
                std_col = f"year_{col_str}"
                meaning = f"Annual indicator value recorded or projected for year {col_str}"
                unit = "Varies by Indicator Code"
                country_comp = "Yes"
            else:
                std_col = col_str.lower().replace(" ", "_")
                meaning = "Auxiliary metadata column"
                
        # 4. EdStatsCountry Metadata
        elif dataset_name == "World Bank Country Metadata":
            if lcol == "country code":
                std_col = "country_code"
                meaning = "ISO 3-letter country code"
                is_identifier = "Yes (ISO Alpha-3)"
                country_comp = "Yes"
            elif lcol == "region":
                std_col = "region"
                meaning = "Geographic region classification (e.g., East Asia & Pacific)"
                country_comp = "Yes"
                univ_overview = "Yes"
            elif lcol == "income group":
                std_col = "income_group"
                meaning = "World Bank income level tier (e.g., High income, Upper middle income)"
                country_comp = "Yes"
                univ_overview = "Yes"
            else:
                std_col = lcol.replace(" ", "_")
                meaning = f"Country demographic/economic metadata: {col_str}"
                country_comp = "Yes"

        entry = {
            "Dataset": dataset_name,
            "Original Column Name": col_str,
            "Proposed Standardized Column Name": std_col,
            "Data Type": dtype,
            "Meaning": meaning,
            "Unit": unit,
            "Example Value": example_val,
            "Missing Percentage": f"{missing_pct}%",
            "Is Identifier": is_identifier,
            "Useful for University Overview": univ_overview,
            "Useful for Research Analytics": research_analytics,
            "Useful for Student Analytics": student_analytics,
            "Useful for Country Comparison": country_comp,
            "KPI Support Mapping": kpi_support
        }
        entries.append(entry)
    return entries

dict_entries.extend(profile_df(df_qs, "QS World University Rankings 2025"))
dict_entries.extend(profile_df(df_the, "THE World University Rankings 2023"))
dict_entries.extend(profile_df(df_ed_data, "World Bank Education Statistics (Data)"))
dict_entries.extend(profile_df(df_ed_country, "World Bank Country Metadata"))

# Save CSV
df_dict = pd.DataFrame(dict_entries)
csv_out = os.path.join(doc_dir, "data_dictionary.csv")
df_dict.to_csv(csv_out, index=False, encoding="utf-8")
print(f"Saved {csv_out}", flush=True)

# Generate Markdown Document
md_lines = []
md_lines.append("# EduVision_DV – Master Data Dictionary\n")
md_lines.append("## Overview\n")
md_lines.append("This document provides a comprehensive data dictionary for all four core datasets analyzed in the **EduVision_DV** project. It documents variable definitions, standardized naming conventions, data types, units of measure, missing value statistics, and mapping towards the project's four Tableau dashboards and six required KPIs.\n")

md_lines.append("### KPI Categorization Rule\n")
md_lines.append("Per analytical rigor guidelines, metric fields are distinguished carefully into:\n")
md_lines.append("- **Actual Percentage**: Exact percentage value (e.g., `International Student` in THE 2023: `24%`).\n")
md_lines.append("- **Actual Ratio**: Exact mathematical ratio (e.g., `No of student per staff` in THE 2023: `9.6`).\n")
md_lines.append("- **Score**: Standardized index score scaled from 0–100 (e.g., `Citations_per_Faculty_Score` in QS 2025).\n")
md_lines.append("- **Rank**: Ordinal global position integer/range (e.g., `RANK_2025` in QS 2025).\n")
md_lines.append("- **Derived Metric**: Engineered metric combining multi-dataset fields during ETL.\n\n")

datasets = df_dict["Dataset"].unique()

for ds in datasets:
    md_lines.append(f"## Dataset: {ds}\n")
    sub_df = df_dict[df_dict["Dataset"] == ds]
    
    md_lines.append("| Original Column Name | Standardized Name | Data Type | Meaning | Unit | Example | Missing % | Identifier | Dashboard Relevance | KPI Support |")
    md_lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    
    for _, row in sub_df.iterrows():
        dashboards = []
        if row["Useful for University Overview"] == "Yes": dashboards.append("Univ Overview")
        if row["Useful for Research Analytics"] == "Yes": dashboards.append("Research")
        if row["Useful for Student Analytics"] == "Yes": dashboards.append("Student")
        if row["Useful for Country Comparison"] == "Yes": dashboards.append("Country Comp")
        dash_str = ", ".join(dashboards) if dashboards else "General Meta"
        
        md_lines.append(f"| `{row['Original Column Name']}` | `{row['Proposed Standardized Column Name']}` | `{row['Data Type']}` | {row['Meaning']} | {row['Unit']} | `{row['Example Value']}` | {row['Missing Percentage']} | {row['Is Identifier']} | {dash_str} | {row['KPI Support Mapping']} |")
    
    md_lines.append("\n---\n")

# Add KPI Coverage Summary Section
md_lines.append("## Six Required KPIs & Source Mapping Summary\n")
md_lines.append("The table below details how the six required project KPIs are supported across datasets, distinguishing between actual values, benchmark scores, and derived calculations:\n\n")

md_lines.append("| KPI # | KPI Name | Target Type | Primary Source Column(s) | Dataset Source | Status & Categorization |")
md_lines.append("| --- | --- | --- | --- | --- | --- |")
md_lines.append("| 1 | **Global Ranking Score** | Score & Rank | `Overall_Score`, `RANK_2025`<br>`OverAll Score`, `University Rank` | QS 2025<br>THE 2023 | **Directly Available**: Actual score (0–100) & rank position. |")
md_lines.append("| 2 | **Research Impact Score** | Score | `Citations_per_Faculty_Score`<br>`Citations Score` | QS 2025<br>THE 2023 | **Directly Available**: Normalized citation impact scores (0–100). |")
md_lines.append("| 3 | **Faculty-to-Student Ratio** | Actual Ratio vs Score | `No of student per staff`<br>`Faculty_Student_Score` | THE 2023<br>QS 2025 | **Directly Available** in THE (Actual Ratio: Students/Staff). QS provides Score. Actual Faculty/Student ratio requires derived calculation in QS. |")
md_lines.append("| 4 | **International Student Percentage** | Actual % vs Score | `International Student`<br>`International_Students_Score` | THE 2023<br>QS 2025 | **Directly Available** in THE (Actual Percentage %). QS provides Score. |")
md_lines.append("| 5 | **Academic Reputation Score** | Score | `Academic_Reputation_Score`<br>`Teaching Score` | QS 2025<br>THE 2023 | **Directly Available** in QS 2025 (0–100 score). THE provides teaching/reputation proxy score. |")
md_lines.append("| 6 | **Research Productivity Index** | Derived Metric / Score | `Research Score`<br>`International_Research_Network_Score` | THE 2023<br>QS 2025 | **Requires Derived Calculation**: Raw paper count per faculty is not directly available; supported via normalized score indexes. |")

md_out = os.path.join(doc_dir, "data_dictionary.md")
with open(md_out, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Saved {md_out}", flush=True)

