"""
Script to generate EduVision_DV_Colab.ipynb notebook.
"""

import json
import os

def make_cell(cell_type, source_text):
    lines = [line + '\n' for line in source_text.split('\n')]
    if lines and lines[-1] == '\n':
        lines[-1] = ''
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

cells = []

# ==========================================
# 1. Project Introduction
# ==========================================
cells.append(make_cell("markdown", """# EduVision_DV: Global Higher Education Performance Analytics
### Infosys Springboard Virtual Internship Project
---
**Objective:**
EduVision_DV is an advanced data visualization and comparative analytics project that evaluates global higher education institutions across academic reputation, research impact, international diversity, and teaching environment.

This Google Colab notebook serves as the primary data processing engine of the project pipeline:
1. **Raw Data Ingestion:** QS World University Rankings 2025 (`infosys dataset.csv`) & Times Higher Education World University Rankings (`Top_Universities_THE.xlsx`).
2. **Standardized Data Cleaning:** Encoding resolution, string normalization, numeric conversions, rank mid-point conversions, and rigorous missing value handling (preserving true analytical nulls without zero-imputation).
3. **Entity Matching & Left-Integration:** Country normalization and 195 verified institution matches between QS (base) and THE.
4. **KPI Engineering:** Formulating 6 core project KPIs and 3 presentation display fields.
5. **Data Validation:** Automated mathematical assertion checks verifying row counts, coverage, and distribution metrics.
6. **Exploratory Data Analysis (EDA):** Pre-Tableau visual exploration across 8 analytical dimensions.
7. **Final Export:** Generating `university_final_dataset.csv` and `university_final_dataset.xlsx` for Tableau Desktop dashboard creation.

---
"""))

# ==========================================
# 2. Import Libraries
# ==========================================
cells.append(make_cell("markdown", """## 2. Import Libraries & Setup
We import core scientific and data processing libraries (`pandas`, `numpy`, `openpyxl`, `matplotlib`, `seaborn`).
All plots are configured with high-contrast formatting suitable for previewing dark/modern dashboard palettes.
"""))

cells.append(make_cell("code", """import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Attempt seaborn import if available
try:
    import seaborn as sns
    sns.set_theme(style="whitegrid")
except ImportError:
    sns = None

# Configure plot aesthetics
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

print("Python version:", sys.version)
print("Pandas version:", pd.__version__)
print("NumPy version:", np.__version__)
"""))

# ==========================================
# 3. Upload / Load Raw Datasets
# ==========================================
cells.append(make_cell("markdown", """## 3. Upload / Load Raw Datasets
This cell handles path resolution automatically:
- Checks Google Colab's default working directory (`/content/`)
- Checks local relative project directories (`../data/raw/`, `./data/raw/`, `./`)
- If running in Google Colab and files are not found, it provides an interactive file upload prompt.
"""))

cells.append(make_cell("code", """def find_file(filename_list):
    search_dirs = [
        '/content',
        '../data/raw',
        './data/raw',
        './EduVision_DV/data/raw',
        '../EduVision_DV/data/raw',
        '.'
    ]
    for d in search_dirs:
        for fname in filename_list:
            path = os.path.join(d, fname)
            if os.path.exists(path):
                return path
    return None

qs_path = find_file(['infosys_dataset.csv', 'infosys dataset.csv'])
the_path = find_file(['Top_Universities_THE.xlsx'])

# If not found and in Google Colab, prompt user to upload
if (qs_path is None or the_path is None) and 'google.colab' in sys.modules:
    from google.colab import files
    print("Please upload 'infosys dataset.csv' and 'Top_Universities_THE.xlsx'...")
    uploaded = files.upload()
    qs_path = find_file(['infosys_dataset.csv', 'infosys dataset.csv'])
    the_path = find_file(['Top_Universities_THE.xlsx'])

print(f"QS dataset path: {qs_path}")
print(f"THE dataset path: {the_path}")

assert qs_path is not None, "Error: QS dataset file could not be located!"
assert the_path is not None, "Error: THE dataset file could not be located!"
"""))

# ==========================================
# 4. Inspect QS Dataset
# ==========================================
cells.append(make_cell("markdown", """## 4. Inspect QS Dataset
We load the raw QS dataset using `latin-1` encoding (necessary due to non-ASCII university names) and examine its structure.
"""))

cells.append(make_cell("code", """df_qs_raw = pd.read_csv(qs_path, encoding='latin-1')
print(f"QS Raw Shape: {df_qs_raw.shape[0]} rows, {df_qs_raw.shape[1]} columns")
print("\\nColumns in QS Dataset:")
print(df_qs_raw.columns.tolist())
df_qs_raw.head(3)
"""))

# ==========================================
# 5. Inspect THE Dataset
# ==========================================
cells.append(make_cell("markdown", """## 5. Inspect THE Dataset
We load the raw THE dataset from the Excel workbook (`Top_Universities_THE.xlsx`) and examine its structure.
"""))

cells.append(make_cell("code", """df_the_raw = pd.read_excel(the_path)
print(f"THE Raw Shape: {df_the_raw.shape[0]} rows, {df_the_raw.shape[1]} columns")
print("\\nColumns in THE Dataset:")
print(df_the_raw.columns.tolist())
df_the_raw.head(3)
"""))

# ==========================================
# 6. Data Cleaning
# ==========================================
cells.append(make_cell("markdown", """## 6. Data Cleaning Pipeline

### 6.1 QS Cleaning Rules:
1. **String Whitespace:** Strip leading and trailing whitespace across all string columns.
2. **RANK Handling:** Preserve original `RANK_2025` string field. Create `Rank_2025_Numeric`:
   - Exact ranks keep numeric value (e.g. `1` -> `1.0`, `15=` -> `15.0`)
   - Banded ranks convert to midpoint (e.g. `1201-1400` -> `1300.5`, `601-610` -> `605.5`)
   - Bounded open ranks convert to floor (e.g. `1401+` -> `1401.0`)
3. **Overall Score Handling:** If value is `'-'`, convert to `NaN`. **Do NOT replace missing scores with 0**, preserving the true scored sample (top 600).
4. **Research Intensity (`RES.`):** Validate categories (`VH`, `HI`, `MD`, `LO`).

### 6.2 THE Cleaning Rules:
1. **Preserve Original Location:** Store in `THE_Location`.
2. **Country Normalization:**
   - THE `China` -> QS `China (Mainland)`
   - THE `Hong Kong` -> QS `Hong Kong SAR`
   - THE `Macao` -> QS `Macau SAR`
3. **Numeric Type Cleaning:** Ensure scores, FTE students, students per staff, and international student ratios are numeric floats.
"""))

cells.append(make_cell("code", """# --- Clean QS Dataset ---
df_qs = df_qs_raw.copy()

# Strip whitespace
for col in df_qs.select_dtypes(include=['object', 'string']).columns:
    df_qs[col] = df_qs[col].astype(str).str.strip()
    df_qs[col] = df_qs[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# Parse numeric rank
def clean_rank_numeric(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace('=', '')
    if s.endswith('+'):
        try:
            return float(s[:-1])
        except ValueError:
            return np.nan
    if '-' in s:
        parts = s.split('-')
        try:
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2.0
        except ValueError:
            return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan

df_qs['Rank_2025_Numeric'] = df_qs['RANK_2025'].apply(clean_rank_numeric)

# Clean Overall_Score: '-' to NaN, strictly no zero-imputation
df_qs['Overall_Score'] = df_qs['Overall_Score'].replace('-', np.nan)
df_qs['Overall_Score'] = pd.to_numeric(df_qs['Overall_Score'], errors='coerce')

# Convert numeric scores to float
qs_numeric_cols = [
    'Academic_Reputation_Score', 'Employer_Reputation_Score',
    'Faculty_Student_Score', 'Citations_per_Faculty_Score',
    'International_Faculty_Score', 'International_Students_Score',
    'International_Research_Network_Score', 'Employment_Outcomes_Score',
    'Sustainability_Score'
]
for col in qs_numeric_cols:
    df_qs[col] = pd.to_numeric(df_qs[col].replace('-', np.nan), errors='coerce')

print(f"QS Cleaning Done: {df_qs.shape[0]} rows")
print(f"QS Overall_Score: {df_qs['Overall_Score'].notna().sum()} non-null, {df_qs['Overall_Score'].isna().sum()} null")
print(f"QS RES. Distribution:\\n{df_qs['RES.'].value_counts()}")
"""))

cells.append(make_cell("code", """# --- Clean THE Dataset ---
df_the = df_the_raw.copy()

# Strip whitespace
for col in df_the.select_dtypes(include=['object', 'string']).columns:
    df_the[col] = df_the[col].astype(str).str.strip()
    df_the[col] = df_the[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# Preserve original THE Location in THE_Location
df_the['THE_Location'] = df_the['Location'].copy()
df_the = df_the.drop(columns=['Location'])

# Country Normalization
the_country_map = {
    'China': 'China (Mainland)',
    'Hong Kong': 'Hong Kong SAR',
    'Macao': 'Macau SAR'
}
df_the['THE_Normalized_Location'] = df_the['THE_Location'].replace(the_country_map)

# Clean numeric columns
the_numeric_cols = [
    'Overall Score', 'Teaching', 'Research Environment',
    'Research Quality', 'Industry', 'International Outlook',
    'No. of FTE Students', 'No. of Students per Staff',
    'International Students'
]
for col in the_numeric_cols:
    if col in df_the.columns:
        if df_the[col].dtype == object:
            df_the[col] = df_the[col].astype(str).str.replace(',', '').str.replace('%', '').str.strip()
        df_the[col] = pd.to_numeric(df_the[col], errors='coerce')

# Rename columns with standard prefixes
df_the = df_the.rename(columns={
    'Rank': 'THE_Rank',
    'Dense Rank': 'THE_Dense_Rank',
    'University Name': 'THE_University_Name',
    'Overall Score': 'THE_Overall_Score',
    'Teaching': 'THE_Teaching',
    'Research Environment': 'THE_Research_Environment',
    'Research Quality': 'THE_Research_Quality',
    'Industry': 'THE_Industry',
    'International Outlook': 'THE_International_Outlook',
    'No. of FTE Students': 'THE_No_of_FTE_Students',
    'No. of Students per Staff': 'THE_No_of_Students_per_Staff',
    'International Students': 'THE_International_Students'
})

print(f"THE Cleaning Done: {df_the.shape[0]} rows")
df_the.head(3)
"""))

# ==========================================
# 7. Data Integration & University Matching
# ==========================================
cells.append(make_cell("markdown", """## 7. Data Integration & University Name Matching

### Strict Business Logic:
1. **Base Dataset:** QS World University Rankings is the foundational reference dataset (exactly 1,503 rows).
2. **Match Target:** Exactly **195** QS institutions matched to THE.
3. **Explicitly Excluded / Unmatched Institutions (5 THE entities):**
   - `Karolinska Institute`: Medical specialist institution not ranked in QS overall top 1500.
   - `Charité - Universitätsmedizin Berlin`: Specialist medical university affiliated with Humboldt/FU Berlin, not ranked as a standalone entity in QS overall.
   - `Scuola Normale Superiore di Pisa`: Italian elite collegiate institution not ranked in QS overall.
   - `University of Massachusetts`: Ambiguous multi-campus system (QS separately ranks *UMass Amherst* and *UMass Boston*).
   - `Indiana University`: Ambiguous multi-campus system (QS separately ranks *Indiana University Bloomington* and *IUPUI*).
4. **Left Integration:** All 1,308 unmatched institutions retain strictly `NaN` for all THE-derived attributes. **No imputation, no zero-filling.**
"""))

cells.append(make_cell("code", """THE_TO_QS_MANUAL_MAPPING = {
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

EXCLUDED_THE_INSTITUTIONS = [
    'Karolinska Institute',
    'Charité - Universitätsmedizin Berlin',
    'Scuola Normale Superiore di Pisa',
    'University of Massachusetts',
    'Indiana University'
]

# Prepare merge keys
df_qs['clean_name'] = df_qs['Institution_Name'].astype(str).str.strip()
df_the['clean_name'] = df_the['THE_University_Name'].astype(str).str.strip()

# Filter eligible THE institutions
the_eligible = df_the[~df_the['clean_name'].isin(EXCLUDED_THE_INSTITUTIONS)].copy()
the_eligible['matched_qs_name'] = the_eligible['clean_name'].map(THE_TO_QS_MANUAL_MAPPING).fillna(the_eligible['clean_name'])

print(f"Eligible THE institutions: {len(the_eligible)}")

# Perform LEFT JOIN on QS
df_integrated = df_qs.merge(
    the_eligible.drop(columns=['clean_name']),
    left_on='clean_name',
    right_on='matched_qs_name',
    how='left'
)
df_integrated = df_integrated.drop(columns=['clean_name', 'matched_qs_name'], errors='ignore')

print(f"Integrated dataset shape: {df_integrated.shape}")
matched_count = df_integrated['THE_University_Name'].notna().sum()
unmatched_count = df_integrated['THE_University_Name'].isna().sum()
print(f"Matched to THE: {matched_count} institutions")
print(f"Unmatched THE data (retained as NaN): {unmatched_count} institutions")
"""))

# ==========================================
# 8. KPI Engineering
# ==========================================
cells.append(make_cell("markdown", """## 8. KPI Engineering

We create the exact 6 project KPIs and 3 presentation display fields:

| KPI Field | Indicator Name | Source Column | Business Description | Expected Coverage |
| :--- | :--- | :--- | :--- | :--- |
| `KPI_Global_Ranking_Score` | Global Ranking Score | QS `Overall_Score` | Overall composite score (scored top 600) | 600 / 1503 (39.9%) |
| `KPI_Academic_Reputation_Score` | Academic Reputation Score | QS `Academic_Reputation_Score` | Survey-based peer evaluation score | 1503 / 1503 (100%) |
| `KPI_Faculty_to_Student_Ratio` | Average Students per Staff | THE `THE_No_of_Students_per_Staff` | Ratio of FTE students per faculty member | 195 / 1503 (13.0%) |
| `KPI_International_Student_Pct` | International Student % | THE `THE_International_Students` * 100 | Percentage of student body that is international | 195 / 1503 (13.0%) |
| `KPI_Research_Impact_Score` | Research Impact Score | QS `Citations_per_Faculty_Score` | Normalized citations per faculty member | 1503 / 1503 (100%) |
| `KPI_Research_Productivity_Proxy` | Research Productivity (Proxy) | THE `THE_Research_Environment` | Analytical proxy for research volume & environment | 195 / 1503 (13.0%) |

> **Critical Methodological Note:** `KPI_Research_Productivity_Proxy` is derived from the THE *Research Environment* metric as an analytical proxy. It is **NOT** the official standalone Research Productivity metric from THE, and must always be labeled with `(Proxy)` in reports and dashboards.
"""))

cells.append(make_cell("code", """# KPI 1: Global Ranking Score (QS Overall_Score)
df_integrated['KPI_Global_Ranking_Score'] = pd.to_numeric(df_integrated['Overall_Score'], errors='coerce')

# KPI 2: Academic Reputation Score (QS Academic_Reputation_Score)
df_integrated['KPI_Academic_Reputation_Score'] = pd.to_numeric(df_integrated['Academic_Reputation_Score'], errors='coerce')

# KPI 3: Faculty to Student Ratio (THE Students per Staff)
df_integrated['KPI_Faculty_to_Student_Ratio'] = pd.to_numeric(df_integrated['THE_No_of_Students_per_Staff'], errors='coerce')

# KPI 4: International Student % (THE International Students * 100)
df_integrated['KPI_International_Student_Pct'] = pd.to_numeric(df_integrated['THE_International_Students'], errors='coerce') * 100.0

# KPI 5: Research Impact Score (QS Citations_per_Faculty_Score)
df_integrated['KPI_Research_Impact_Score'] = pd.to_numeric(df_integrated['Citations_per_Faculty_Score'], errors='coerce')

# KPI 6: Research Productivity Proxy (THE Research Environment)
df_integrated['KPI_Research_Productivity_Proxy'] = pd.to_numeric(df_integrated['THE_Research_Environment'], errors='coerce')

# Presentation Display Fields (formatted tooltips)
df_integrated['Display_Students_per_Staff'] = df_integrated['KPI_Faculty_to_Student_Ratio'].apply(
    lambda x: f"{x:.1f} students/staff" if pd.notna(x) else "Sourced from THE (Data not available)"
)
df_integrated['Display_Int_Student_Pct'] = df_integrated['KPI_International_Student_Pct'].apply(
    lambda x: f"{x:.1f}%" if pd.notna(x) else "Sourced from THE (Data not available)"
)
df_integrated['Display_Research_Productivity'] = df_integrated['KPI_Research_Productivity_Proxy'].apply(
    lambda x: f"{x:.1f} pts" if pd.notna(x) else "THE Environment Proxy (Data not available)"
)

print("KPI Engineering successfully completed.")
"""))

# ==========================================
# 9. Data Validation
# ==========================================
cells.append(make_cell("markdown", """## 9. Comprehensive Data Validation
We programmatically verify all mathematical and distributional requirements.
"""))

cells.append(make_cell("code", """val_results = []

def record_val(metric, expected, actual, passed):
    val_results.append({
        'Metric': metric,
        'Expected Value': str(expected),
        'Actual Value': str(actual),
        'Status': 'PASS' if passed else 'FAIL'
    })

# Total records
total_rows = len(df_integrated)
record_val("Total Institutions", 1503, total_rows, total_rows == 1503)

# Total countries
total_countries = df_integrated['Location'].nunique()
record_val("Total Countries", 106, total_countries, total_countries == 106)

# US universities
us_count = (df_integrated['Location'] == 'United States').sum()
record_val("US Institutions", 197, us_count, us_count == 197)

# Matched THE
matched_the = df_integrated['THE_University_Name'].notna().sum()
record_val("Matched THE Institutions", 195, matched_the, matched_the == 195)

# KPI 1 (Global Score)
k1 = df_integrated['KPI_Global_Ranking_Score']
record_val("KPI 1 Non-null", 600, k1.notna().sum(), k1.notna().sum() == 600)
record_val("KPI 1 Min", 20.80, round(k1.min(), 2), round(k1.min(), 2) == 20.80)
record_val("KPI 1 Max", 100.0, round(k1.max(), 2), round(k1.max(), 2) == 100.0)
record_val("KPI 1 Mean", 41.84, round(k1.mean(), 2), round(k1.mean(), 2) == 41.84)

# KPI 2 (Academic Reputation)
k2 = df_integrated['KPI_Academic_Reputation_Score']
record_val("KPI 2 Non-null", 1503, k2.notna().sum(), k2.notna().sum() == 1503)
record_val("KPI 2 Min", 1.30, round(k2.min(), 2), round(k2.min(), 2) == 1.30)
record_val("KPI 2 Max", 100.0, round(k2.max(), 2), round(k2.max(), 2) == 100.0)
record_val("KPI 2 Mean", 20.29, round(k2.mean(), 2), round(k2.mean(), 2) == 20.29)

# KPI 3 (Students per Staff)
k3 = df_integrated['KPI_Faculty_to_Student_Ratio']
record_val("KPI 3 Non-null", 195, k3.notna().sum(), k3.notna().sum() == 195)
record_val("KPI 3 Min", 3.80, round(k3.min(), 2), round(k3.min(), 2) == 3.80)
record_val("KPI 3 Max", 58.0, round(k3.max(), 2), round(k3.max(), 2) == 58.0)
record_val("KPI 3 Mean", 17.44, round(k3.mean(), 2), round(k3.mean(), 2) == 17.44)

# KPI 4 (Intl Student Pct)
k4 = df_integrated['KPI_International_Student_Pct']
record_val("KPI 4 Non-null", 195, k4.notna().sum(), k4.notna().sum() == 195)
record_val("KPI 4 Min", 1.0, round(k4.min(), 1), round(k4.min(), 1) == 1.0)
record_val("KPI 4 Max", 72.0, round(k4.max(), 1), round(k4.max(), 1) == 72.0)
record_val("KPI 4 Mean", 25.48, round(k4.mean(), 2), round(k4.mean(), 2) == 25.48)

# KPI 5 (Research Impact)
k5 = df_integrated['KPI_Research_Impact_Score']
record_val("KPI 5 Non-null", 1503, k5.notna().sum(), k5.notna().sum() == 1503)
record_val("KPI 5 Min", 1.0, round(k5.min(), 1), round(k5.min(), 1) == 1.0)
record_val("KPI 5 Max", 100.0, round(k5.max(), 1), round(k5.max(), 1) == 100.0)
record_val("KPI 5 Mean", 23.50, round(k5.mean(), 2), round(k5.mean(), 2) == 23.50)

# KPI 6 (Research Productivity Proxy)
k6 = df_integrated['KPI_Research_Productivity_Proxy']
record_val("KPI 6 Non-null", 195, k6.notna().sum(), k6.notna().sum() == 195)
record_val("KPI 6 Min", 34.90, round(k6.min(), 2), round(k6.min(), 2) == 34.90)
record_val("KPI 6 Max", 100.0, round(k6.max(), 2), round(k6.max(), 2) == 100.0)
record_val("KPI 6 Mean", 61.23, round(k6.mean(), 2), round(k6.mean(), 2) == 61.23)

val_df = pd.DataFrame(val_results)
print(val_df.to_string(index=False))

assert (val_df['Status'] == 'PASS').all(), "Validation failure detected in pipeline!"
print("\\n*** ALL VALIDATION CHECKS PASSED WITH 100% CONFORMANCE! ***")
"""))

# ==========================================
# 10. Exploratory Data Analysis
# ==========================================
cells.append(make_cell("markdown", """## 10. Exploratory Data Analysis (EDA)

We construct 8 pre-Tableau visualizations exploring each core analytical dimension:
1. Top universities by QS Global Score
2. Universities by Region
3. Distribution of Academic Reputation
4. Distribution of Research Impact
5. Research Intensity (`RES.`) vs Research Impact
6. International Student % distribution
7. Students per Staff by Region
8. Country university counts
"""))

# EDA 1
cells.append(make_cell("code", """# EDA 1: Top 10 Universities by QS Global Score
top10_qs = df_integrated.sort_values(by='KPI_Global_Ranking_Score', ascending=False).head(10)

plt.figure(figsize=(10, 5))
bars = plt.barh(top10_qs['Institution_Name'][::-1], top10_qs['KPI_Global_Ranking_Score'][::-1], color='#00D2C4')
plt.title('Top 10 Universities by QS Global Score 2025', fontweight='bold')
plt.xlabel('QS Global Ranking Score')
plt.xlim(85, 102)
for bar in bars:
    plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}", va='center', fontweight='bold')
plt.tight_layout()
plt.show()
"""))

# EDA 2
cells.append(make_cell("code", """# EDA 2: Universities by Region
region_counts = df_integrated['Region'].value_counts()

plt.figure(figsize=(8, 8))
colors = ['#00D2C4', '#2EC4B6', '#FF9F1C', '#E71D36', '#48CAE4', '#7209B7']
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', colors=colors[:len(region_counts)], startangle=140)
plt.title('Distribution of Ranked Institutions by Region', fontweight='bold')
plt.tight_layout()
plt.show()
"""))

# EDA 3
cells.append(make_cell("code", """# EDA 3: Distribution of Academic Reputation Score
plt.figure(figsize=(10, 5))
plt.hist(df_integrated['KPI_Academic_Reputation_Score'], bins=40, color='#00D2C4', edgecolor='black', alpha=0.85)
plt.axvline(df_integrated['KPI_Academic_Reputation_Score'].mean(), color='#E71D36', linestyle='dashed', linewidth=2, label=f"Mean: {df_integrated['KPI_Academic_Reputation_Score'].mean():.2f}")
plt.title('Distribution of Academic Reputation Score (All 1,503 Institutions)', fontweight='bold')
plt.xlabel('Academic Reputation Score')
plt.ylabel('Number of Universities')
plt.legend()
plt.tight_layout()
plt.show()
"""))

# EDA 4
cells.append(make_cell("code", """# EDA 4: Distribution of Research Impact Score
plt.figure(figsize=(10, 5))
plt.hist(df_integrated['KPI_Research_Impact_Score'], bins=40, color='#FF9F1C', edgecolor='black', alpha=0.85)
plt.axvline(df_integrated['KPI_Research_Impact_Score'].mean(), color='#E71D36', linestyle='dashed', linewidth=2, label=f"Mean: {df_integrated['KPI_Research_Impact_Score'].mean():.2f}")
plt.title('Distribution of Research Impact (Citations per Faculty Score)', fontweight='bold')
plt.xlabel('Citations per Faculty Score')
plt.ylabel('Number of Universities')
plt.legend()
plt.tight_layout()
plt.show()
"""))

# EDA 5
cells.append(make_cell("code", """# EDA 5: Research Intensity (RES.) vs Research Impact Score
res_order = ['VH', 'HI', 'MD', 'LO']
res_data = [df_integrated[df_integrated['RES.'] == cat]['KPI_Research_Impact_Score'].dropna() for cat in res_order]

plt.figure(figsize=(9, 5))
cat_names = ['Very High (VH)', 'High (HI)', 'Medium (MD)', 'Low (LO)']
try:
    box = plt.boxplot(res_data, tick_labels=cat_names, patch_artist=True)
except TypeError:
    box = plt.boxplot(res_data, labels=cat_names, patch_artist=True)
colors_box = ['#00D2C4', '#2EC4B6', '#FF9F1C', '#E71D36']
for patch, color in zip(box['boxes'], colors_box):
    patch.set_facecolor(color)
plt.title('Research Impact Score across Research Intensity Categories', fontweight='bold')
plt.xlabel('Research Intensity Category (RES.)')
plt.ylabel('Research Impact Score')
plt.tight_layout()
plt.show()
"""))

# EDA 6
cells.append(make_cell("code", """# EDA 6: International Student % Distribution (Matched Cohort)
intl_pct = df_integrated['KPI_International_Student_Pct'].dropna()

plt.figure(figsize=(10, 5))
plt.hist(intl_pct, bins=25, color='#2EC4B6', edgecolor='black', alpha=0.85)
plt.axvline(intl_pct.mean(), color='#E71D36', linestyle='dashed', linewidth=2, label=f"Mean: {intl_pct.mean():.2f}%")
plt.title('Distribution of International Student Percentage (195 Matched Institutions)', fontweight='bold')
plt.xlabel('International Student %')
plt.ylabel('Number of Universities')
plt.legend()
plt.tight_layout()
plt.show()
"""))

# EDA 7
cells.append(make_cell("code", """# EDA 7: Students per Staff by Region (Matched Cohort)
staff_ratio = df_integrated.dropna(subset=['KPI_Faculty_to_Student_Ratio'])
avg_ratio_by_region = staff_ratio.groupby('Region')['KPI_Faculty_to_Student_Ratio'].mean().sort_values()

plt.figure(figsize=(10, 5))
bars = plt.barh(avg_ratio_by_region.index, avg_ratio_by_region.values, color='#48CAE4')
plt.title('Average Students per Staff Member by Region (THE Matched Cohort)', fontweight='bold')
plt.xlabel('Average Students per Staff')
for bar in bars:
    plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}", va='center', fontweight='bold')
plt.tight_layout()
plt.show()
"""))

# EDA 8
cells.append(make_cell("code", """# EDA 8: Top 15 Countries by Number of Ranked Universities
top15_countries = df_integrated['Location'].value_counts().head(15)

plt.figure(figsize=(10, 6))
bars = plt.barh(top15_countries.index[::-1], top15_countries.values[::-1], color='#00D2C4')
plt.title('Top 15 Countries by Number of Ranked Universities (QS 2025)', fontweight='bold')
plt.xlabel('Number of Ranked Universities')
for bar in bars:
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{int(bar.get_width())}", va='center')
plt.tight_layout()
plt.show()
"""))

# ==========================================
# 11. Export Final Dataset
# ==========================================
cells.append(make_cell("markdown", """## 11. Export Final Dataset
We export the final clean, integrated, and KPI-engineered dataset in both CSV and XLSX formats:
- `university_final_dataset.csv`
- `university_final_dataset.xlsx`
"""))

cells.append(make_cell("code", """csv_export_path = 'university_final_dataset.csv'
xlsx_export_path = 'university_final_dataset.xlsx'

df_integrated.to_csv(csv_export_path, index=False, encoding='utf-8')
df_integrated.to_excel(xlsx_export_path, index=False, engine='openpyxl')

print(f"Exported CSV: {csv_export_path} ({os.path.getsize(csv_export_path)} bytes)")
print(f"Exported XLSX: {xlsx_export_path} ({os.path.getsize(xlsx_export_path)} bytes)")

# Colab download helper
if 'google.colab' in sys.modules:
    from google.colab import files
    print("Triggering browser downloads for Google Colab user...")
    try:
        files.download(csv_export_path)
        files.download(xlsx_export_path)
    except Exception as e:
        print(f"Colab download prompt notice: {e}")
"""))

# ==========================================
# 12. Summary & Conclusion
# ==========================================
cells.append(make_cell("markdown", """## 12. Summary & Conclusion

### Data Engineering Summary:
1. **Source Fidelity:** Both raw datasets (`infosys dataset.csv` and `Top_Universities_THE.xlsx`) were thoroughly inspected and cleaned with zero information loss or alteration to raw inputs.
2. **Missing Data Ethics:** True analytical nulls were strictly preserved. 903 unranked QS scores and 1,308 unmatched THE institutions were left as `NaN`, eliminating analytical bias.
3. **Rigorous Validation:** Exactly 1,503 universities, 106 countries, 197 US institutions, and 195 matched institutions verified against expected criteria.
4. **Research Productivity Clarity:** The metric derived from THE Research Environment is explicitly marked as an analytical `(Proxy)`.

### Transition to Tableau Desktop:
With the clean dataset exported to `university_final_dataset.csv` / `university_final_dataset.xlsx`, the next phase transitions to **Tableau Desktop** for the construction of 4 functional interactive dashboards:
1. **University Overview:** Institutional rankings, global distribution, and macro indicators.
2. **Research Analytics:** Deep dive into citations per faculty vs research environment proxy across research intensity bands.
3. **Student Analytics:** Faculty-to-student ratios, international student percentages, and enrollment volumes.
4. **Country Comparison:** Heatmap benchmarking and dynamic interactive country filtering actions.

Consult `docs/dashboard_guide.md` for exact step-by-step instructions on visual design, layout containers, calculated fields, and dashboard actions in Tableau Desktop.
"""))

notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.10"
        },
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'EduVision_DV_Colab.ipynb')
output_path = os.path.abspath(output_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=2)

print(f"Successfully generated notebook at: {output_path}")
