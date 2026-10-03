import os
import re
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

# Load cleaned datasets & dimension tables
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_wur = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)
dim_country = pd.read_csv(os.path.join(final_dir, "dim_country.csv"))
dim_univ = pd.read_csv(os.path.join(final_dir, "dim_university.csv"))

# Map country names to country_id
country_map = dict(zip(dim_country['country_name'], dim_country['country_id']))

# Known deterministic abbreviation / alternate name map
known_aliases = {
    "mit": "massachusetts institute of technology",
    "massachusetts institute of technology mit": "massachusetts institute of technology",
    "ucl": "university college london",
    "ucl university college london": "university college london",
    "lse": "london school of economics and political science",
    "london school of economics and political science lse": "london school of economics and political science",
    "caltech": "california institute of technology",
    "california institute of technology caltech": "california institute of technology",
    "eth zurich": "eth zurich swiss federal institute of technology",
    "epfl": "ecole polytechnique federale de lausanne",
    "nus": "national university of singapore",
    "ntu": "nanyang technological university"
}

def clean_name_for_matching(name):
    if pd.isna(name):
        return ""
    text = str(name).lower()
    # Strip parenthetical text
    text = re.sub(r'\s*\([^)]*\)\s*', ' ', text)
    if text.startswith("the "):
        text = text[4:]
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return known_aliases.get(text, text)

df_qs['clean_name'] = df_qs['university_name'].apply(clean_name_for_matching)
df_wur['clean_name'] = df_wur['university_name'].apply(clean_name_for_matching)

# Map country_id to each row
country_clean_map = {
    "United States": "United States", "US": "United States", "USA": "United States", "United States of America": "United States",
    "United Kingdom": "United Kingdom", "UK": "United Kingdom",
    "China (Mainland)": "China", "Hong Kong SAR": "Hong Kong", "Macau SAR": "Macao",
    "South Korea": "South Korea", "Korea, Rep.": "South Korea", "Taiwan": "Taiwan",
    "Russian Federation": "Russian Federation", "Russia": "Russian Federation",
    "Czech Republic": "Czechia", "Turkey": "Türkiye"
}

df_qs['std_country'] = df_qs['country'].replace(country_clean_map)
df_wur['std_country'] = df_wur['country'].replace(country_clean_map)

df_qs['country_id'] = df_qs['std_country'].map(country_map).fillna("C999")
df_wur['country_id'] = df_wur['std_country'].map(country_map).fillna("C999")

print(f"QS dataset rows: {len(df_qs)}")
print(f"THE/WUR dataset rows: {len(df_wur)}")

crosswalk_records = []
crosswalk_id_counter = 1

# Group by country_id to ensure strict country boundaries
all_country_ids = set(df_qs['country_id']).union(set(df_wur['country_id']))

matched_wur_indices = set()

for cid in all_country_ids:
    qs_subset = df_qs[df_qs['country_id'] == cid].copy()
    wur_subset = df_wur[df_wur['country_id'] == cid].copy()
    
    for q_idx, q_row in qs_subset.iterrows():
        q_raw = q_row['university_name']
        q_clean = q_row['clean_name']
        
        best_match = None
        best_sim = 0.0
        best_method = "UNMATCHED"
        best_status = "NOT_MATCHED"
        best_w_raw = np.nan
        best_w_idx = None
        notes = "No matching institution found in same country"
        
        for w_idx, w_row in wur_subset.iterrows():
            w_raw = w_row['university_name']
            w_clean = w_row['clean_name']
            
            # Exact clean match
            if q_clean == w_clean and len(q_clean) > 3:
                best_match = w_clean
                best_sim = 1.0
                best_method = "EXACT_STANDARDIZED_NAME"
                best_status = "APPROVED"
                best_w_raw = w_raw
                best_w_idx = w_idx
                notes = "Exact standardized name match within same country"
                break
                
            # Known alias match
            elif (q_clean in known_aliases and known_aliases[q_clean] == w_clean) or (w_clean in known_aliases and known_aliases[w_clean] == q_clean):
                best_match = w_clean
                best_sim = 0.98
                best_method = "KNOWN_ABBREVIATION_MAPPING"
                best_status = "APPROVED"
                best_w_raw = w_raw
                best_w_idx = w_idx
                notes = "Match via known institutional abbreviation mapping"
                break
                
            else:
                sim = SequenceMatcher(None, q_clean, w_clean).ratio()
                # Check for word-overlap safety (e.g., distinguishing "University of Delhi" vs "Delhi Technological University")
                q_words = set(q_clean.split())
                w_words = set(w_clean.split())
                
                # If key word differs significantly (e.g., 'technological' vs 'delhi'), do NOT auto match
                diff_words = q_words.symmetric_difference(w_words)
                ignorable_words = {'of', 'the', 'and', 'for', 'at', 'in', 'de', 'la', 'university', 'college', 'institute'}
                significant_diff = diff_words - ignorable_words
                
                if sim > best_sim:
                    best_sim = sim
                    if sim >= 0.92 and len(significant_diff) == 0:
                        best_method = "HIGH_CONFIDENCE_FUZZY"
                        best_status = "APPROVED"
                        best_w_raw = w_raw
                        best_w_idx = w_idx
                        notes = "High-confidence fuzzy string match with identical core key terms"
                    elif sim >= 0.78:
                        best_method = "FUZZY_CANDIDATE_MATCH"
                        best_status = "REVIEW_REQUIRED"
                        best_w_raw = w_raw
                        best_w_idx = w_idx
                        notes = f"Candidate match with similarity {round(sim, 2)}; requires manual approval due to word differences ({list(significant_diff)[:3]})"

        uid = f"U{crosswalk_id_counter:06d}"
        crosswalk_id_counter += 1
        
        if best_status == "APPROVED" and best_w_idx is not None:
            matched_wur_indices.add(best_w_idx)
            
        crosswalk_records.append({
            "university_id": uid,
            "qs_name": q_raw,
            "the_name": best_w_raw if best_status != "NOT_MATCHED" else np.nan,
            "wur_name": best_w_raw if best_status != "NOT_MATCHED" else np.nan,
            "country_id": cid,
            "match_method": best_method if best_status != "NOT_MATCHED" else "NO_MATCH",
            "match_status": best_status,
            "confidence": round(best_sim, 4) if best_status != "NOT_MATCHED" else 0.0,
            "notes": notes
        })

# Include remaining unmatched WUR institutions
for w_idx, w_row in df_wur.iterrows():
    if w_idx not in matched_wur_indices:
        uid = f"U{crosswalk_id_counter:06d}"
        crosswalk_id_counter += 1
        crosswalk_records.append({
            "university_id": uid,
            "qs_name": np.nan,
            "the_name": w_row['university_name'],
            "wur_name": w_row['university_name'],
            "country_id": w_row['country_id'],
            "match_method": "NO_MATCH",
            "match_status": "NOT_MATCHED",
            "confidence": 0.0,
            "notes": "Unmatched institution present only in THE/WUR 2023 dataset"
        })

df_crosswalk = pd.DataFrame(crosswalk_records)
crosswalk_path = os.path.join(final_dir, "university_crosswalk.csv")
df_crosswalk.to_csv(crosswalk_path, index=False, encoding="utf-8")
print(f"Saved university_crosswalk.csv with {len(df_crosswalk)} crosswalk entries")

# Summary of match statuses
status_counts = df_crosswalk['match_status'].value_counts()
print("\nMatch Status Summary:")
print(status_counts)

method_counts = df_crosswalk['match_method'].value_counts()
print("\nMatch Method Summary:")
print(method_counts)

# Generate Markdown Matching Report
md_report = []
md_report.append("# EduVision_DV – University Cross-Dataset Matching Report\n")
md_report.append("## Executive Summary\n")
md_report.append("This report details the cross-dataset entity resolution performed between **QS World University Rankings 2025** and **THE / World University Rankings 2023**. Deterministic and controlled candidate matching rules were applied strictly within country boundaries to prevent false merges.\n")

md_report.append("### Key Results Summary\n")
md_report.append(f"- **Total University Entities Registered**: **{len(df_crosswalk):,}**\n")
md_report.append(f"- **APPROVED Cross-Dataset Matches**: **{status_counts.get('APPROVED', 0):,}**\n")
md_report.append(f"- **REVIEW_REQUIRED Candidates**: **{status_counts.get('REVIEW_REQUIRED', 0):,}**\n")
md_report.append(f"- **NOT_MATCHED Single-Source Entities**: **{status_counts.get('NOT_MATCHED', 0):,}**\n\n")

md_report.append("## Hierarchy of Matching Methods Applied\n")
md_report.append("1. **Exact Standardized Name Match**: Exact match on clean normalized name within the same `country_id` (**APPROVED**).\n")
md_report.append("2. **Known Abbreviation / Alternate Mapping**: Mapped known abbreviations (e.g. `MIT` $\\leftrightarrow$ `Massachusetts Institute of Technology`) within the same country (**APPROVED**).\n")
md_report.append("3. **Country Boundary Enforcement**: Institutions in different countries are NEVER matched regardless of name similarity.\n")
md_report.append("4. **Controlled Fuzzy Candidate Review**: High-similarity pairs with distinct non-ignorable words (e.g. `University of Delhi` vs `Delhi Technological University`) are categorized as **NOT_MATCHED** or **REVIEW_REQUIRED** to prevent false merges.\n\n")

md_report.append("## Breakdown by Match Method\n")
md_report.append("| Match Method | Match Status | Count | Description |")
md_report.append("| --- | --- | --- | --- |")

for method, cnt in method_counts.items():
    status = df_crosswalk[df_crosswalk['match_method'] == method]['match_status'].iloc[0]
    md_report.append(f"| `{method}` | `{status}` | {cnt:,} | Cross-dataset entity resolution method |")

md_report.append("\n---\n")
md_report.append("## Sample Approved Matches\n")
md_report.append("| University ID | QS Name | THE/WUR Name | Country ID | Method | Confidence |")
md_report.append("| --- | --- | --- | --- | --- | --- |")

app_samples = df_crosswalk[df_crosswalk['match_status'] == 'APPROVED'].head(10)
for _, r in app_samples.iterrows():
    md_report.append(f"| `{r['university_id']}` | {r['qs_name']} | {r['the_name']} | `{r['country_id']}` | `{r['match_method']}` | {r['confidence']} |")

md_report.append("\n---\n")
md_report.append("## Sample Review Required Candidates (Pending User Approval)\n")
md_report.append("| University ID | QS Name | THE/WUR Name | Country ID | Method | Confidence | Notes |")
md_report.append("| --- | --- | --- | --- | --- | --- | --- |")

rev_samples = df_crosswalk[df_crosswalk['match_status'] == 'REVIEW_REQUIRED'].head(10)
for _, r in rev_samples.iterrows():
    md_report.append(f"| `{r['university_id']}` | {r['qs_name']} | {r['the_name']} | `{r['country_id']}` | `{r['match_method']}` | {r['confidence']} | {r['notes']} |")

md_report_path = os.path.join(reports_dir, "university_matching_report.md")
with open(md_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_report))

print(f"Saved {md_report_path}")

