import os
import json
import pandas as pd
import numpy as np

raw_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\raw"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

os.makedirs(reports_dir, exist_ok=True)

data_files = []
for root, dirs, files in os.walk(raw_dir):
    for f in files:
        if f.endswith('.csv') or f.endswith('.xlsx') or f.endswith('.xls'):
            data_files.append(os.path.join(root, f))

print(f"Found {len(data_files)} data files:", flush=True)
for f in data_files:
    print(" -", os.path.relpath(f, raw_dir), flush=True)

profiles = []

for filepath in data_files:
    rel_path = os.path.relpath(filepath, raw_dir)
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()[1:]
    
    print(f"\nProcessing {filename}...", flush=True)
    
    try:
        if ext == 'csv':
            try:
                df = pd.read_csv(filepath, low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, encoding='latin1', low_memory=False)
        else:
            # Excel file
            print(f" Reading excel file {filename} (this may take a moment)...", flush=True)
            df = pd.read_excel(filepath)
            
        num_rows = len(df)
        num_cols = len(df.columns)
        col_names = [str(c) for c in df.columns]
        dtypes = {col: str(df[col].dtype) for col in df.columns}
        
        # Missing values
        missing_count = int(df.isnull().sum().sum())
        total_cells = num_rows * num_cols
        missing_pct = round((missing_count / total_cells * 100), 2) if total_cells > 0 else 0.0
        
        # Duplicate rows
        duplicate_rows = int(df.duplicated().sum())
        
        # Specific column identification tailored to higher education & edstats datasets
        cols_lower = {col: str(col).lower() for col in col_names}
        
        # 7. University Name Column
        univ_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['institution', 'university_name', 'university', 'univ', 'school']) and not any(k in lcol for k in ['country', 'code', 'series']):
                univ_cols.append(col)
        univ_col_str = ", ".join(univ_cols) if univ_cols else "N/A"
        
        # 8. Country/Location Column
        country_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['country', 'location', 'region', 'nation', 'economy', 'iso', 'country_name', 'country_code', 'country_series']):
                country_cols.append(col)
        country_col_str = ", ".join(country_cols) if country_cols else "N/A"
        
        # 9. Year Information
        year_cols = []
        for col, lcol in cols_lower.items():
            if 'year' in lcol or lcol in ['yr', 'time'] or (lcol.isdigit() and len(lcol)==4):
                year_cols.append(col)
        if year_cols:
            year_info = ", ".join(year_cols)
        else:
            digit_cols = [c for c in col_names if str(c).strip().isdigit() and len(str(c).strip()) == 4]
            if len(digit_cols) > 0:
                year_info = f"Year Columns ({digit_cols[0]} - {digit_cols[-1]})"
            else:
                year_info = "N/A"
                
        # 10. Important Ranking Fields
        ranking_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['rank', 'score', 'overall', 'tier', 'national_rank', 'world_rank']):
                ranking_cols.append(col)
        ranking_col_str = ", ".join(ranking_cols) if ranking_cols else "N/A"
        
        # 11. Research-Related Fields
        research_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['research', 'publication', 'paper', 'h-index', 'output', 'patents']):
                research_cols.append(col)
        research_col_str = ", ".join(research_cols) if research_cols else "N/A"
        
        # 12. Student-Related Fields
        student_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['student', 'enrollment', 'pupil', 'gender', 'ratio', 'faculty_count', 'staff']) and not any(k in lcol for k in ['international', 'foreign']):
                student_cols.append(col)
        student_col_str = ", ".join(student_cols) if student_cols else "N/A"
        
        # 13. International Student Fields
        intl_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['international', 'foreign', 'intl']):
                intl_cols.append(col)
        intl_col_str = ", ".join(intl_cols) if intl_cols else "N/A"
        
        # 14. Academic Reputation Fields
        rep_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['reputation', 'academic', 'employer', 'survey', 'quality_of_education', 'quality_of_faculty']):
                rep_cols.append(col)
        rep_col_str = ", ".join(rep_cols) if rep_cols else "N/A"
        
        # 15. Citation Fields
        citation_cols = []
        for col, lcol in cols_lower.items():
            if any(k in lcol for k in ['citation', 'cite', 'impact']):
                citation_cols.append(col)
        citation_col_str = ", ".join(citation_cols) if citation_cols else "N/A"
        
        # 19. Duplicate University Name Count
        dup_univ_count = 0
        if univ_cols:
            p_col = univ_cols[0]
            dup_univ_count = int(df[p_col].dropna().duplicated().sum())
            
        profile = {
            "relative_path": rel_path,
            "filename": filename,
            "file_type": ext.upper(),
            "num_rows": num_rows,
            "num_cols": num_cols,
            "column_names": col_names,
            "data_types": dtypes,
            "university_name_column": univ_col_str,
            "country_location_column": country_col_str,
            "year_information": year_info,
            "ranking_fields": ranking_col_str,
            "research_fields": research_col_str,
            "student_fields": student_col_str,
            "international_student_fields": intl_col_str,
            "academic_reputation_fields": rep_col_str,
            "citation_fields": citation_col_str,
            "missing_value_count": missing_count,
            "missing_value_percentage": missing_pct,
            "duplicate_row_count": duplicate_rows,
            "duplicate_university_count": dup_univ_count
        }
        profiles.append(profile)
        print(f" Done profiling {filename}. Rows: {num_rows}, Cols: {num_cols}", flush=True)
        
    except Exception as e:
        print(f" Error processing {filename}: {e}", flush=True)

# Save JSON profile
json_path = os.path.join(reports_dir, "dataset_profile.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(profiles, f, indent=2)
print(f"\nSaved {json_path}", flush=True)

# Save CSV profile
csv_rows = []
for p in profiles:
    csv_rows.append({
        "File Name": p["filename"],
        "File Path": p["relative_path"],
        "File Type": p["file_type"],
        "Number of Rows": p["num_rows"],
        "Number of Columns": p["num_cols"],
        "Column Names": " | ".join(p["column_names"]),
        "Data Types": json.dumps(p["data_types"]),
        "University Name Column": p["university_name_column"],
        "Country/Location Column": p["country_location_column"],
        "Year Information": p["year_information"],
        "Important Ranking Fields": p["ranking_fields"],
        "Research-Related Fields": p["research_fields"],
        "Student-Related Fields": p["student_fields"],
        "International Student Fields": p["international_student_fields"],
        "Academic Reputation Fields": p["academic_reputation_fields"],
        "Citation Fields": p["citation_fields"],
        "Missing Value Count": p["missing_value_count"],
        "Missing Value Percentage": p["missing_value_percentage"],
        "Duplicate Row Count": p["duplicate_row_count"],
        "Duplicate University Count": p["duplicate_university_count"]
    })

csv_df = pd.DataFrame(csv_rows)
csv_path = os.path.join(reports_dir, "dataset_validation_report.csv")
csv_df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"Saved {csv_path}", flush=True)

# Generate Markdown Report
md_lines = []
md_lines.append("# EduVision_DV - Dataset Validation & Profiling Report\n")
md_lines.append("## Executive Summary\n")
md_lines.append(f"A total of **{len(profiles)} raw dataset files** were identified, profiled, and inspected in `data/raw/`.\n")

md_lines.append("## Summary Table of Profiled Datasets\n")
md_lines.append("| File Name | File Type | Rows | Cols | Missing Cells (%) | Duplicate Rows | Dup Univ Names | Key Univ/Country Cols |")
md_lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")

for p in profiles:
    md_lines.append(f"| `{p['filename']}` | {p['file_type']} | {p['num_rows']:,} | {p['num_cols']} | {p['missing_value_count']:,} ({p['missing_value_percentage']}%) | {p['duplicate_row_count']:,} | {p['duplicate_university_count']:,} | `{p['university_name_column']}` / `{p['country_location_column']}` |")

md_lines.append("\n---\n")
md_lines.append("## Detailed File Profiles\n")

for i, p in enumerate(profiles, 1):
    md_lines.append(f"### {i}. `{p['filename']}`\n")
    md_lines.append(f"- **Relative Path**: `{p['relative_path']}`")
    md_lines.append(f"- **File Type**: {p['file_type']}")
    md_lines.append(f"- **Dimensions**: {p['num_rows']:,} rows × {p['num_cols']} columns")
    md_lines.append(f"- **Missing Values**: {p['missing_value_count']:,} ({p['missing_value_percentage']}%)")
    md_lines.append(f"- **Duplicate Rows**: {p['duplicate_row_count']:,}")
    md_lines.append(f"- **Duplicate University Names**: {p['duplicate_university_count']:,}")
    md_lines.append(f"- **University-Name Column**: `{p['university_name_column']}`")
    md_lines.append(f"- **Country/Location Column**: `{p['country_location_column']}`")
    md_lines.append(f"- **Year Information**: `{p['year_information']}`")
    md_lines.append(f"- **Important Ranking Fields**: `{p['ranking_fields']}`")
    md_lines.append(f"- **Research-Related Fields**: `{p['research_fields']}`")
    md_lines.append(f"- **Student-Related Fields**: `{p['student_fields']}`")
    md_lines.append(f"- **International Student Fields**: `{p['international_student_fields']}`")
    md_lines.append(f"- **Academic Reputation Fields**: `{p['academic_reputation_fields']}`")
    md_lines.append(f"- **Citation Fields**: `{p['citation_fields']}`\n")
    
    md_lines.append("**Column Schema & Data Types:**")
    md_lines.append("```")
    for col, dt in p['data_types'].items():
        md_lines.append(f"  - {col}: {dt}")
    md_lines.append("```\n")

md_path = os.path.join(reports_dir, "dataset_validation_report.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Saved {md_path}", flush=True)

