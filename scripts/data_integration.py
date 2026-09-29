"""
EduVision_DV - Data Integration Script
Infosys Springboard Virtual Internship Project

This script performs left-join integration of the cleaned QS dataset (base)
with the cleaned THE dataset based on university names and approved manual mappings.

Strict constraints:
- QS is the base dataset (exactly 1,503 rows).
- Exactly 195 QS institutions matched to THE.
- Five THE institutions remain UNMATCHED:
    1. Karolinska Institute (not in QS)
    2. Charité - Universitätsmedizin Berlin (not in QS)
    3. Scuola Normale Superiore di Pisa (not in QS)
    4. University of Massachusetts (ambiguous multi-campus system: Amherst vs Boston)
    5. Indiana University (ambiguous multi-campus system: Bloomington vs IUPUI)
- All unmatched THE fields remain strictly NaN (no imputation, no zero-filling).

Outputs:
- data/processed/qs_the_integrated.csv
"""

import os
import sys
import pandas as pd
import numpy as np

# Approved manual mappings from THE name to QS Institution_Name
# Built from empirical analysis of identical entities with naming variations
THE_TO_QS_MANUAL_MAPPING = {
    'Massachusetts Institute of Technology': 'Massachusetts Institute of Technology (MIT)',
    'California Institute of Technology': 'California Institute of Technology (Caltech)',
    'University of California Berkeley': 'University of California, Berkeley (UCB)',
    'ETH Zurich': 'ETH Zurich - Swiss Federal Institute of Technology',
    'The University of Chicago': 'University of Chicago',
    'National University of Singapore': 'National University of Singapore (NUS)',
    'University of California Los Angeles': 'University of California, Los Angeles (UCLA)',
    'University of Edinburgh': 'The University of Edinburgh',
    'Nanyang Technological University Singapore': 'Nanyang Technological University, Singapore (NTU)',
    'École Polytechnique Fédérale de Lausanne': 'EPFL',
    'New York University': 'New York University (NYU)',
    'University of California San Diego': 'University of California, San Diego (UCSD)',
    'University of Hong Kong': 'The University of Hong Kong',
    'King’s College London': "King's College London",
    'LMU Munich': 'Ludwig-Maximilians-Universität München',
    'University of Melbourne': 'The University of Melbourne',
    'Paris Sciences et Lettres – PSL Research University Paris': 'Université PSL',
    'The Chinese University of Hong Kong': 'The Chinese University of Hong Kong (CUHK)',
    'Universität Heidelberg': 'Ruprecht-Karls-Universität Heidelberg',
    'London School of Economics and Political Science': 'The London School of Economics and Political Science (LSE)',
    'University of Manchester': 'The University of Manchester',
    'University of California Davis': 'University of California, Davis',
    'University of California Santa Barbara': 'University of California, Santa Barbara (UCSB)',
    'Washington University in St Louis': 'Washington University in St. Louis',
    'University of North Carolina at Chapel Hill': 'University of North Carolina, Chapel Hill',
    'Australian National University': 'The Australian National University',
    'Purdue University West Lafayette': 'Purdue University',
    'Korea Advanced Institute of Science and Technology (KAIST)': 'KAIST - Korea Advanced Institute of Science & Technology',
    'UNSW Sydney': 'The University of New South Wales (UNSW Sydney)',
    'Humboldt University of Berlin': 'Humboldt-Universität zu Berlin',
    'University of Minnesota': 'University of Minnesota Twin Cities',
    'University of Bonn': 'Rheinische Friedrich-Wilhelms-Universität Bonn',
    'University of California Irvine': 'University of California, Irvine',
    'University of Sheffield': 'The University of Sheffield',
    'Penn State (Main campus)': 'Pennsylvania State University',
    'University of Tübingen': 'Eberhard Karls Universität Tübingen',
    'Sungkyunkwan University (SKKU)': 'Sungkyunkwan University(SKKU)',
    'Yonsei University (Seoul campus)': 'Yonsei University',
    'Free University of Berlin': 'Freie Universitaet Berlin',
    'University of Warwick': 'The University of Warwick',
    'University of Maryland College Park': 'University of Maryland, College Park',
    'Ohio State University (Main campus)': 'The Ohio State University',
    'University of Adelaide': 'The University of Adelaide',
    'University of Freiburg': 'Albert-Ludwigs-Universitaet Freiburg',
    'University of Hamburg': 'Universität Hamburg',
    'University of Arizona': 'The University of Arizona',
    'Trinity College Dublin': 'Trinity College Dublin, The University of Dublin',
    'Technical University of Berlin': 'Technische Universität Berlin (TU Berlin)',
    'University of Pittsburgh-Pittsburgh campus': 'University of Pittsburgh',
    'Radboud University Nijmegen': 'Radboud University',
    'University of Bologna': 'Alma Mater Studiorum - University of Bologna',
    'University of Barcelona': 'Universitat de Barcelona',
    'Pohang University of Science and Technology (POSTECH)': 'Pohang University of Science And Technology (POSTECH)',
    'University of Auckland': 'The University of Auckland',
    'TU Dresden': 'Technische Universität Dresden',
    'University of Virginia (Main campus)': 'University of Virginia',
    'University of Würzburg': 'Julius-Maximilians-Universität Würzburg',
    'Karlsruhe Institute of Technology': 'KIT, Karlsruhe Institute of Technology',
    'University of Exeter': 'The University of Exeter',
    'Université Catholique de Louvain': 'Université catholique de Louvain (UCLouvain)',
    'King Fahd University of Petroleum and Minerals': 'King Fahd University of Petroleum & Minerals',
    'Pompeu Fabra University': 'Universitat Pompeu Fabra (Barcelona)',
    'Southern University of Science and Technology (SUSTech)': 'Southern University of Science and Technology',
    'University of Münster': 'Westfälische Wilhelms-Universität Münster',
    'Tokyo Institute of Technology': 'Tokyo Institute of Technology (Tokyo Tech)',
    'University of California Santa Cruz': 'University of California, Santa Cruz',
    'Ulm University': 'University Ulm',
    'Universitat Autònoma de Barcelona (UAB)': 'Universitat Autònoma de Barcelona'
}

# Explicitly excluded from matching (must remain unmatched)
EXCLUDED_THE_INSTITUTIONS = [
    'Karolinska Institute',
    'Charité - Universitätsmedizin Berlin',
    'Scuola Normale Superiore di Pisa',
    'University of Massachusetts',
    'Indiana University'
]


def integrate_datasets(qs_cleaned_path, the_cleaned_path):
    """
    Integrates QS and THE datasets via LEFT JOIN on Institution_Name.
    """
    print(f"Loading cleaned QS from: {qs_cleaned_path}")
    df_qs = pd.read_csv(qs_cleaned_path)
    print(f"Loading cleaned THE from: {the_cleaned_path}")
    df_the = pd.read_csv(the_cleaned_path)

    assert len(df_qs) == 1503, f"Expected 1,503 rows in QS dataset, found {len(df_qs)}"
    assert len(df_the) == 200, f"Expected 200 rows in THE dataset, found {len(df_the)}"

    # Clean strings
    df_qs['clean_name'] = df_qs['Institution_Name'].astype(str).str.strip()
    df_the['clean_name'] = df_the['THE_University_Name'].astype(str).str.strip()

    # Verify exclusions
    the_eligible = df_the[~df_the['clean_name'].isin(EXCLUDED_THE_INSTITUTIONS)].copy()
    assert len(the_eligible) == 195, f"Expected 195 eligible THE universities, found {len(the_eligible)}"

    # Map THE name to QS name using manual dictionary or identity
    the_eligible['matched_qs_name'] = the_eligible['clean_name'].map(THE_TO_QS_MANUAL_MAPPING).fillna(the_eligible['clean_name'])

    # Verify that all 195 matched names exist in QS
    qs_names_set = set(df_qs['clean_name'])
    unmatched_in_qs = [name for name in the_eligible['matched_qs_name'] if name not in qs_names_set]
    assert len(unmatched_in_qs) == 0, f"Some mapped names not found in QS: {unmatched_in_qs}"

    # Verify no duplicate mappings
    duplicate_mappings = the_eligible['matched_qs_name'].value_counts()
    duplicates = duplicate_mappings[duplicate_mappings > 1]
    assert len(duplicates) == 0, f"Duplicate matches found: {duplicates}"

    # Prepare THE columns for merge (drop temporary helper columns)
    the_to_merge = the_eligible.drop(columns=['clean_name'])

    # Left join from QS
    df_integrated = df_qs.merge(
        the_to_merge,
        left_on='clean_name',
        right_on='matched_qs_name',
        how='left'
    )

    # Drop temporary merge helper columns
    df_integrated = df_integrated.drop(columns=['clean_name', 'matched_qs_name'], errors='ignore')

    # Assertions
    assert len(df_integrated) == 1503, f"Expected 1,503 rows in integrated dataset, found {len(df_integrated)}"
    the_matched_count = df_integrated['THE_University_Name'].notna().sum()
    the_null_count = df_integrated['THE_University_Name'].isna().sum()
    print(f"Integration Results: {the_matched_count} matched to THE, {the_null_count} unmatched (strictly NaN)")
    assert the_matched_count == 195, f"Expected exactly 195 matched institutions, found {the_matched_count}"
    assert the_null_count == 1308, f"Expected exactly 1,308 unmatched institutions, found {the_null_count}"

    return df_integrated


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, 'data', 'processed')

    qs_path = os.path.join(processed_dir, 'qs_cleaned.csv')
    the_path = os.path.join(processed_dir, 'the_cleaned.csv')

    df_integrated = integrate_datasets(qs_path, the_path)

    out_path = os.path.join(processed_dir, 'qs_the_integrated.csv')
    df_integrated.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Saved integrated dataset to: {out_path} (Shape: {df_integrated.shape})")


if __name__ == '__main__':
    main()
