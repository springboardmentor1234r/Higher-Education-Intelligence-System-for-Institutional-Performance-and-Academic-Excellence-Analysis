"""
EduVision_DV - Milestone 1 / Module 1: University Data Collection
Author: Sujay S
Date: 2026-09-20

Purpose:
Collects, validates, organizes, and integrates global university ranking datasets:
1. QS World University Rankings 2025
2. Times Higher Education (THE) World University Rankings 2024
3. World University Rankings (WUR) 2023
4. World Bank Education Statistics (EdStats)

Deliverables:
- scripts/data_collection.py
- data/Module_1/university_raw_data.csv
- 01_raw_datasets/university_raw_data.csv
- 01_raw_datasets/qs_2025_raw.csv
- 01_raw_datasets/the_2024_raw.csv
- 01_raw_datasets/wur_2023_raw.csv
- 01_raw_datasets/world_bank_education_raw.csv
"""

import os
import shutil
import pandas as pd
import numpy as np

def main():
    print("================================================================================")
    print("   EduVision_DV - Module 1: University Data Collection & Ingestion Pipeline")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_source_dir = os.path.join(base_dir, "data", "Module_1")
    raw_dest_dir = os.path.join(base_dir, "01_raw_datasets")
    os.makedirs(raw_dest_dir, exist_ok=True)
    os.makedirs(raw_source_dir, exist_ok=True)

    dataset_map = {
        "qs_2025_raw.csv": "QS World University Rankings 2025 (Top global universities).csv",
        "the_2024_raw.csv": "TIMES_WorldUniversityRankings_2024.csv",
        "wur_2023_raw.csv": "World University Rankings 2023.csv",
        "world_bank_education_raw.csv": "World Bank Education Statistics.csv"
    }

    loaded_dfs = {}

    for target_name, src_name in dataset_map.items():
        src_path = os.path.join(raw_source_dir, src_name)
        dest_path = os.path.join(raw_dest_dir, target_name)
        
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        print(f"\n[+] Processing {src_name} -> {target_name}")
        shutil.copy2(src_path, dest_path)
        
        # Load sample / metadata
        df = pd.read_csv(dest_path, encoding="latin1", low_memory=False)
        loaded_dfs[target_name] = df
        print(f"    - Dimensions: {df.shape[0]:,} rows x {df.shape[1]} columns")
        print(f"    - Missing Values: {df.isnull().sum().sum():,} cells ({df.isnull().mean().mean()*100:.2f}%)")

    # Build university_raw_data.csv as consolidated reference for university ranking systems
    print("\n[+] Constructing integrated 'university_raw_data.csv'...")
    qs = loaded_dfs["qs_2025_raw.csv"]
    
    # Create consolidated raw performance table
    raw_integrated = pd.DataFrame()
    raw_integrated["raw_id"] = ["RAW_" + str(i + 1).zfill(5) for i in range(len(qs))]
    raw_integrated["institution_name"] = qs["Institution_Name"].astype(str).str.strip()
    raw_integrated["location"] = qs["Location"].astype(str).str.strip()
    raw_integrated["region"] = qs["Region"].astype(str).str.strip()
    raw_integrated["qs_rank_2025"] = qs["RANK_2025"]
    raw_integrated["qs_overall_score"] = pd.to_numeric(qs["Overall_Score"], errors="coerce")
    raw_integrated["qs_academic_reputation"] = pd.to_numeric(qs["Academic_Reputation_Score"], errors="coerce")
    raw_integrated["qs_citations_per_faculty"] = pd.to_numeric(qs["Citations_per_Faculty_Score"], errors="coerce")
    raw_integrated["qs_faculty_student_score"] = pd.to_numeric(qs["Faculty_Student_Score"], errors="coerce")
    raw_integrated["qs_intl_students_score"] = pd.to_numeric(qs["International_Students_Score"], errors="coerce")
    raw_integrated["qs_intl_research_network"] = pd.to_numeric(qs["International_Research_Network_Score"], errors="coerce")
    
    # Completeness check on required dimensions
    completeness = (1.0 - (raw_integrated[["institution_name", "location", "region", "qs_rank_2025"]].isnull().mean().mean())) * 100.0
    print(f"    - Dataset Completeness on Core Identifiers: {completeness:.2f}% (Target: >95%)")
    assert completeness >= 95.0, "Completeness target of 95% not met!"

    # Save university_raw_data.csv to both data/Module_1 and 01_raw_datasets
    output_p1 = os.path.join(raw_source_dir, "university_raw_data.csv")
    output_p2 = os.path.join(raw_dest_dir, "university_raw_data.csv")
    raw_integrated.to_csv(output_p1, index=False)
    raw_integrated.to_csv(output_p2, index=False)
    print(f"    - Successfully exported: {output_p1}")
    print(f"    - Successfully exported: {output_p2}")

    print("\n[SUCCESS] Module 1 Data Collection completed successfully!")

if __name__ == "__main__":
    main()
