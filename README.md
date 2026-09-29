# EduVision_DV: Global Higher Education Performance Analytics
### Infosys Springboard Virtual Internship Project

---

## 1. Project Objective
**EduVision_DV** is an advanced business intelligence and higher education performance analytics project developed under the **Infosys Springboard Virtual Internship**. 

The project synthesizes multi-source data from the **QS World University Rankings 2025** and the **Times Higher Education (THE) World University Rankings** into a harmonized data warehouse. It delivers executive-level, interactive visual intelligence across four thematic areas:
1. **Global Institutional Overview:** Macro-level rankings, continental distributions, and institutional profiles.
2. **Research Analytics:** Correlation between research environment, faculty productivity, and citation impact across research intensity classifications.
3. **Student & Learning Analytics:** Student-faculty ratios, global internationalization mobility, and overall enrollment footprint.
4. **Country Benchmarking & Comparison:** Multi-metric national scorecards with interactive geographic cross-filtering.

---

## 2. Project Architecture & Clean Structure

```
EduVision_DV/
│
├── data/
│   ├── raw/
│   │   ├── infosys_dataset.csv          # QS World University Rankings 2025 (1,503 rows)
│   │   └── Top_Universities_THE.xlsx     # Times Higher Education Rankings (200 rows)
│   │
│   └── processed/
│       ├── qs_cleaned.csv                # Cleaned QS dataset
│       ├── the_cleaned.csv               # Cleaned & normalized THE dataset
│       └── qs_the_integrated.csv         # Left-joined integrated dataset
│
├── notebooks/
│   └── EduVision_DV_Colab.ipynb         # Fully runnable, self-contained Google Colab notebook
│
├── scripts/
│   ├── data_cleaning.py                 # Automated data cleaning pipeline
│   ├── data_integration.py              # Entity matching & left-join integration
│   ├── kpi_engineering.py               # KPI formulation & validation suite
│   └── generate_notebook.py             # Notebook builder
│
├── docs/
│   ├── methodology.md                   # Technical methodology, join rules & math formulas
│   ├── dashboard_guide.md               # Exact Tableau Desktop step-by-step construction guide
│   └── testing_report.md                # Comprehensive test audit & statistical validation
│
├── university_final_dataset.csv         # Master exported dataset (CSV format)
├── university_final_dataset.xlsx        # Master exported dataset (Excel format)
├── README.md                            # Main project overview & documentation
└── requirements.txt                     # Project Python dependencies
```

---

## 3. Data Ingestion & Google Colab Workflow

The main data-processing engine is engineered for **Google Colab**:
- **Notebook Location:** `notebooks/EduVision_DV_Colab.ipynb`
- **Environment Compatibility:** Works out of the box in Google Colab (handles `/content/` paths, local relative paths, or automatic upload prompt if files are missing).
- **Key Modules in Colab:**
  1. *Project Introduction & Library Setup* (`pandas`, `numpy`, `openpyxl`, `matplotlib`, `seaborn`)
  2. *Intelligent Data Loader* (Auto-detects Colab environment and loads raw files)
  3. *Data Cleaning* (Latin-1 decoding, string trimming, rank mid-point conversions, null preservation)
  4. *Entity Matching & Left-Integration* (Resolving 195 verified institutions, handling exclusions)
  5. *KPI Engineering* (6 KPIs + 3 tooltip display fields)
  6. *Automated Validation Suite* (Assertion tests verifying 100% data conformance)
  7. *Exploratory Data Analysis (EDA)* (8 complete pre-Tableau charts)
  8. *Master Export* (Direct export to CSV and Excel, with browser auto-download trigger in Colab)

---

## 4. Key Performance Indicators (KPIs)

The project engineers six standardized KPIs and three formatted display fields:

| KPI Indicator | Technical Column Name | Data Source | Coverage | Expected Mean |
| :--- | :--- | :--- | :--- | :--- |
| **Global Ranking Score** | `KPI_Global_Ranking_Score` | QS `Overall_Score` | Top 600 (39.9%) | **41.84** |
| **Academic Reputation** | `KPI_Academic_Reputation_Score` | QS `Academic_Reputation_Score` | All 1,503 (100%) | **20.29** |
| **Students per Staff** | `KPI_Faculty_to_Student_Ratio` | THE `No. of Students per Staff` | Matched 195 (13.0%) | **17.44** |
| **International Student %** | `KPI_International_Student_Pct` | THE `International Students` * 100 | Matched 195 (13.0%) | **25.48%** |
| **Research Impact** | `KPI_Research_Impact_Score` | QS `Citations_per_Faculty_Score` | All 1,503 (100%) | **23.50** |
| **Research Productivity (Proxy)** | `KPI_Research_Productivity_Proxy` | THE `Research Environment` | Matched 195 (13.0%) | **61.23** |

### Display / Tooltip Formatted Fields:
- `Display_Students_per_Staff`: Formats value as `X.X students/staff` or `"Sourced from THE (Data not available)"`.
- `Display_Int_Student_Pct`: Formats value as `X.X%` or `"Sourced from THE (Data not available)"`.
- `Display_Research_Productivity`: Formats value as `X.X pts` or `"THE Environment Proxy (Data not available)"`.

---

## 5. Tableau Desktop Workflow & Dashboards

The final datasets (`university_final_dataset.csv` and `university_final_dataset.xlsx`) serve as the single source of truth for **Tableau Desktop**:

### 5.1 Dashboard 1: University Overview
- **Visual Design:** Dark theme (`#12161A` canvas, `#1B2026` cards, `#00D2C4` teal accent).
- **KPI Summary Cards:** Top Ranked University (MIT #1), Total Universities (`1,503`), Dynamic Average Global Score (`41.84` - Avg of Top 600).
- **Worksheets:**
  - *Top 10 Universities by Global Score* (Horizontal bar chart, descending)
  - *Universities by Region* (Donut chart with total count in center)
  - *Geographic Distribution* (Filled world map colored by university count)
- **Filters:** Region, Location (Only Relevant Values), SIZE, FOCUS.

### 5.2 Dashboard 2: Research Analytics
- **Visual Design:** Dark theme with `#FF9F1C` amber accent.
- **KPI Summary Cards:** Highest Research Impact (`100.0`), Average Citation Score (`23.5`), Average Research Productivity Proxy (`61.2`).
- **Worksheets:**
  - *Research Impact vs Research Productivity (Proxy)* (Scatter plot colored by Region)
  - *Research Intensity Comparison* (Box plot grouped by `RES.`: VH, HI, MD, LO)
  - *Top 10 Research Institutions* (Grouped bars comparing Impact and Productivity Proxy)
- **Mandatory Notice:** `"Research Productivity (Proxy) uses THE Research Environment and is available only for matched QS-THE institutions."`

### 5.3 Dashboard 3: Student Analytics
- **Visual Design:** Dark theme with `#2EC4B6` emerald accent.
- **KPI Summary Cards:** Average Students per Staff (`17.4 students/staff`), Average International Student % (`25.5%`), Total Enrolled FTE Student Headcount (`5.46M`).
- **Worksheets:**
  - *Average Students per Staff by Region* (Horizontal bar chart)
  - *Internationalization Scatter* (Faculty-to-student ratio vs International Student %)
  - *Top 10 Universities by Enrollment* (Horizontal bars by `THE_No_of_FTE_Students`)
- **Filters:** Region, Location (Only Relevant Values), SIZE, FOCUS.

### 5.4 Dashboard 4: Country Comparison
- **Visual Design:** Dark theme with `#00D2C4` cyan accent.
- **KPI Summary Cards:** Top Country by Avg Global Score, Total Ranked Countries (`106`), Most Represented Country (United States - `197` universities).
- **Worksheets:**
  - *Country Benchmarking Heatmap/Table* (Columns: Avg Global Score, Avg Academic Reputation, Avg Research Impact, University Count)
  - *Geographic Country Map* (Choropleth country map)
- **Interactive Action:** Selecting a country row in the benchmarking table dynamically filters and zooms the geographic map.

---

## 6. Critical Analytical Disclosures & Limitations

1. **Truncated Scored Sample:** QS overall rankings provide exact composite scores only for the top 600 universities. The remaining 903 universities are retained as `NaN`. Under no circumstances are missing scores imputed with zero or averages.
2. **THE Coverage Limitations:** Times Higher Education rankings focus on the top 200 institutions. 195 universities match QS; all remaining 1,308 universities retain `NaN` for THE-derived metrics.
3. **Research Productivity is an Analytical Proxy:** Because QS does not evaluate pure research volume, THE *Research Environment* is utilized as a project analytical proxy. It is explicitly labeled **"Research Productivity (Proxy)"** and must not be misrepresented as the official THE Research Productivity metric.
4. **Faculty-to-Student Ratio Labeling:** The metric represents the number of students per staff member. It is labeled **"Average Students per Staff"** and never rendered as a colon ratio (`1:17.4`).

---

## 7. Execution Instructions

### To run the Python pipeline locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run data cleaning
python scripts/data_cleaning.py

# Run data integration
python scripts/data_integration.py

# Run KPI engineering and validation
python scripts/kpi_engineering.py
```

### To run in Google Colab:
1. Open [Google Colab](https://colab.research.google.com).
2. Upload `notebooks/EduVision_DV_Colab.ipynb`.
3. Upload `infosys dataset.csv` and `Top_Universities_THE.xlsx` when prompted (or place them in `/content/`).
4. Run all cells (`Runtime` $\rightarrow$ `Run all`).
5. Download the validated `university_final_dataset.csv` and `university_final_dataset.xlsx`.

### To build dashboards in Tableau Desktop:
Follow the detailed guide in `docs/dashboard_guide.md`.
