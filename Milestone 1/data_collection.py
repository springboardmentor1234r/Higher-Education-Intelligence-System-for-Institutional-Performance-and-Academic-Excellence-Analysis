import os
import pandas as pd
import numpy as np

# Define directories
BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
RAW_DIR = os.path.join(BASE_DIR, "raw")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

def load_and_inspect_qs():
    path = os.path.join(RAW_DIR, "qs_2025.csv")
    df = pd.read_csv(path, encoding='latin1')
    report = {
        'name': 'QS 2025',
        'file': 'qs_2025.csv',
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        'duplicates': df.duplicated().sum(),
        'columns': list(df.columns)
    }
    return df, report

def load_and_inspect_the():
    path = os.path.join(RAW_DIR, "the_2024.csv")
    df = pd.read_csv(path, encoding='latin1')
    report = {
        'name': 'THE 2024',
        'file': 'the_2024.csv',
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        'duplicates': df.duplicated().sum(),
        'columns': list(df.columns)
    }
    return df, report

def load_and_inspect_wur():
    path = os.path.join(RAW_DIR, "wur_2023.csv")
    df = pd.read_csv(path, encoding='latin1')
    report = {
        'name': 'WUR 2023',
        'file': 'wur_2023.csv',
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        'duplicates': df.duplicated().sum(),
        'columns': list(df.columns)
    }
    return df, report

def load_and_inspect_edstats():
    ed_dir = os.path.join(RAW_DIR, "world_bank_edstats")
    df_data = pd.read_csv(os.path.join(ed_dir, "EdStatsData.csv"), low_memory=False)
    df_data.columns = [c.replace('﻿', '').replace('"', '').strip() for c in df_data.columns]
    
    df_country = pd.read_csv(os.path.join(ed_dir, "EdStatsCountry.csv"))
    df_series = pd.read_csv(os.path.join(ed_dir, "EdStatsSeries.csv"))
    
    report = {
        'name': 'World Bank EdStats (EdStatsData.csv)',
        'file': 'world_bank_edstats/EdStatsData.csv',
        'shape': df_data.shape,
        'country_metadata_shape': df_country.shape,
        'series_metadata_shape': df_series.shape,
        'duplicates': df_data.duplicated(subset=['Country Code', 'Indicator Code']).sum(),
        'columns': list(df_data.columns)
    }
    return df_data, df_country, df_series, report

def generate_validation_report_md(reports):
    md = "# Raw Data Validation Report\n\n"
    md += "This report summarizes the schema, shape, missingness, and duplicate statistics for all four raw input datasets.\n\n"
    
    for r in reports:
        md += f"## 1. Dataset: {r['name']} (`{r['file']}`)\n"
        md += f"- **Shape**: {r['shape'][0]:,} rows x {r['shape'][1]} columns\n"
        md += f"- **Duplicate Rows**: {r['duplicates']}\n"
        md += f"- **Columns ({len(r['columns'])})**: `{', '.join(r['columns'][:10])}`"
        if len(r['columns']) > 10:
            md += f", ... (+{len(r['columns'])-10} more)\n\n"
        else:
            md += "\n\n"
            
        md += "### Missing Data Summary (% Null)\n\n"
        md += "| Column Name | Dtype | Missing % |\n"
        md += "|---|---|---|\n"
        if 'missing' in r:
            for col, pct in r['missing'].items():
                if pct > 0:
                    dt = str(r['dtypes'][col])
                    md += f"| `{col}` | `{dt}` | {pct}% |\n"
        else:
            md += "| (EdStats composite inspection) | - | - |\n"
        md += "\n"
        
    report_path = os.path.join(DOCS_DIR, "raw_data_validation_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Validation report saved to {report_path}")

if __name__ == "__main__":
    df_qs, rep_qs = load_and_inspect_qs()
    df_the, rep_the = load_and_inspect_the()
    df_wur, rep_wur = load_and_inspect_wur()
    df_ed_data, df_ed_country, df_ed_series, rep_ed = load_and_inspect_edstats()
    
    generate_validation_report_md([rep_qs, rep_the, rep_wur, rep_ed])
    print("Step 1 (01_data_loading.py) complete!")
