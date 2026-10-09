"""
EduVision_DV - Milestone 1, Module 1: University Data Collection
Infosys Springboard Virtual Internship Project

PURPOSE
-------
Collects the two source ranking datasets, audits their completeness, and merges
them into a single common raw structure for downstream cleaning.

SOURCES
-------
1. QS World University Rankings 2025   -> data/raw/infosys_dataset.csv   (1,503 institutions)
2. Times Higher Education Rankings     -> data/raw/Top_Universities_THE.xlsx (200 institutions)

OUTPUT
------
Milestone 1/university_raw_data.csv

MERGE STRATEGY
--------------
This is the *collection* stage, so no cleaning, normalisation or entity matching is
performed here. The two rankings publish different indicator sets, so they are unioned
into a common long structure rather than joined: every institution from either source
becomes one row, tagged with its Source_Ranking_System. Common descriptive fields are
harmonised into shared column names; source-specific indicators are retained verbatim
under their own prefixed names so that nothing is lost before cleaning.

Entity matching between the two systems happens later, in Milestone 1 Module 2, where
institution names have been standardised and a reliable join key exists.

NOTE ON RANK FORMATS
--------------------
Ranks are deliberately left as published strings at this stage ('15', '621-630',
'1401+'). They are parsed to numerics during cleaning.
"""

import os
import sys
import pandas as pd


def resolve_paths():
    """Locate the raw source files relative to this script."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw = os.path.join(base, 'data', 'raw')
    qs = os.path.join(raw, 'infosys_dataset.csv')
    the = os.path.join(raw, 'Top_Universities_THE.xlsx')
    for p in (qs, the):
        if not os.path.exists(p):
            sys.exit(f"ERROR: required source file not found: {p}")
    return base, qs, the


def audit(name, df):
    """Report dimensions and completeness for a source dataset."""
    cells = df.shape[0] * df.shape[1]
    missing = int(df.isna().sum().sum())
    completeness = 100.0 - (missing / cells * 100.0)
    print(f"  {name}")
    print(f"    rows x cols   : {df.shape[0]:,} x {df.shape[1]}")
    print(f"    missing cells : {missing:,} ({missing / cells * 100:.2f}%)")
    print(f"    completeness  : {completeness:.2f}%")
    return completeness


def collect_qs(path):
    """Load the QS World University Rankings 2025 export."""
    print(f"Loading QS source: {os.path.basename(path)}")
    # latin-1: the QS export contains accented institution names
    df = pd.read_csv(path, encoding='latin-1')
    return df


def collect_the(path):
    """Load the Times Higher Education rankings export."""
    print(f"Loading THE source: {os.path.basename(path)}")
    return pd.read_excel(path)


def merge_common_structure(qs, the):
    """
    Union both sources into one common raw structure.

    Common columns: Source_Ranking_System, Institution_Name, Location,
                    Rank_Published, Overall_Score_Published
    All remaining source columns are kept, prefixed QS_ or THE_.
    """
    qs_part = pd.DataFrame({
        'Source_Ranking_System': 'QS_2025',
        'Institution_Name': qs['Institution_Name'],
        'Location': qs['Location'],
        'Rank_Published': qs['RANK_2025'],
        'Overall_Score_Published': qs['Overall_Score'],
    })
    for c in qs.columns:
        if c not in ('Institution_Name', 'Location', 'RANK_2025', 'Overall_Score'):
            qs_part[f'QS_{c}'] = qs[c]

    the_name = 'University_Name' if 'University_Name' in the.columns else the.columns[1]
    the_loc = 'Location' if 'Location' in the.columns else None
    the_rank = 'Rank' if 'Rank' in the.columns else the.columns[0]
    the_overall = 'Overall_Score' if 'Overall_Score' in the.columns else None

    the_part = pd.DataFrame({
        'Source_Ranking_System': 'THE',
        'Institution_Name': the[the_name],
        'Location': the[the_loc] if the_loc else pd.NA,
        'Rank_Published': the[the_rank],
        'Overall_Score_Published': the[the_overall] if the_overall else pd.NA,
    })
    for c in the.columns:
        if c not in (the_name, the_loc, the_rank, the_overall):
            the_part[f'THE_{c}'] = the[c]

    merged = pd.concat([qs_part, the_part], ignore_index=True, sort=False)
    return merged


def main():
    base, qs_path, the_path = resolve_paths()

    print("=" * 70)
    print("MILESTONE 1 / MODULE 1 - UNIVERSITY DATA COLLECTION")
    print("=" * 70)

    qs = collect_qs(qs_path)
    the = collect_the(the_path)

    print("\nSource completeness audit:")
    qs_completeness = audit('QS World University Rankings 2025', qs)
    the_completeness = audit('Times Higher Education Rankings', the)

    print("\nMerging into a common raw structure ...")
    merged = merge_common_structure(qs, the)
    print(f"  merged rows   : {len(merged):,}  ({len(qs):,} QS + {len(the):,} THE)")
    print(f"  merged columns: {merged.shape[1]}")
    print(f"  institutions per source: "
          f"{merged['Source_Ranking_System'].value_counts().to_dict()}")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, 'university_raw_data.csv')
    merged.to_csv(out, index=False, encoding='utf-8')
    print(f"\nWrote {out} ({os.path.getsize(out):,} bytes)")

    print("\nEvaluation criterion - dataset completeness above 95%:")
    print(f"  QS  : {qs_completeness:.2f}%  -> {'PASS' if qs_completeness > 95 else 'FAIL'}")
    print(f"  THE : {the_completeness:.2f}% -> {'PASS' if the_completeness > 95 else 'FAIL'}")
    print("\nNote: completeness is reported per source universe. The QS figure includes")
    print("Overall_Score, which QS itself publishes only for its top 600 institutions.")
    print("=" * 70)


if __name__ == '__main__':
    main()
