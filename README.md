# EduVision: Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis

An end-to-end data analytics system that integrates multi-source global university rankings (QS 2025, Times Higher Education 2024, World University Rankings 2023) and macroeconomic context (World Bank Education Indicators). The system cleans, normalizes, models, and transforms heterogeneous educational datasets into a unified star schema for executive KPI analytics and Tableau dashboards.

---

## 📌 Project Architecture

```text
├── Milestone_1/
│   ├── cleaned/                       # Standardized star-schema dimension & fact CSVs
│   └── raw/                           # Unprocessed source datasets
├── Milestone_2/
│   ├── generate_education_kpis.py     # KPI engineering & master joining pipeline
│   └── university_final_dataset.xlsx  # Master excel dataset ready for Tableau
├── Milestone_3/
│   └── eduvision_dashboard_v1.twbx    # Initial Tableau workbook prototype
├── Milestone_4/
│   ├── EduVision Analytics System - Dashboard Story Document.pdf  # Executive story & architecture doc
│   └── EduVision_DV.twbx              # Final production Tableau workbook suite
├── .gitignore                         # Git ignore configurations
├── LICENSE                            # License agreement
└── README.md                          # Project documentation
```

## 🛠️ Data Pipeline & Ingestion Strategy (Milestone 1)

### 1. Data Cleaning & Encoding Solutions
* **Encoding Artifacts (Mojibake Fix):** Raw multi-language datasets (Spanish/Portuguese accented names like Tucumán, Goiás, Uberlândia) were cleaned using UTF-8 / Latin-1 byte reversal (`fix_mojibake`) to preserve character integrity.
* **Text Normalization:** Lowercasing, regex punctuation stripping, whitespace collapsing, and title-casing across institution names.
* **Country Normalization:** Standardized country names using a global canonical `COUNTRY_MAP` to ensure 100% alignment across distinct ranking sources.

### 2. Star-Schema Design
To eliminate data redundancy, facts and dimensions were modeled using a strict left-join structure anchored on a primary master dimension:

* **Dimension Tables:**
  * `dim_university`: Unique `university_id`, sanitized institution names, and canonical `country_id`.
  * `dim_country`: Unique `country_id`, ISO codes, and macro-region mappings.

* **Fact Tables:**
  * `fact_university_performance`: QS 2025 global ranks, academic, and employer reputation metrics.
  * `fact_research`: THE 2024 research performance, citation impact, and research scores.
  * `fact_student`: WUR 2023 enrollment counts, international student counts, and staff ratios.
  * `fact_country_education`: World Bank tertiary education expenditure and GDP indicators.

### 3. 📊Engineered Key Performance Indicators (Milestone 2)

Each metric follows strict normalization, explicit calculation formulas, and missing-value handling to maintain statistical integrity:

| KPI Metric | Source Table | Calculation / Formula | Unit | Missing Value Policy |
| :--- | :--- | :--- | :--- | :--- |
| **1. Research Impact** | `fact_research` | Scaled `citations_score` | Score (0–100) | Retained as `NaN` (Preserve zero distinction) |
| **2. Research Productivity Index** | `fact_research` | $0.5 \times \text{Research Score} + 0.5 \times \text{Citations Score}$ | Index Score (0–100) | Computed only if components exist; else `NaN` |
| **3. Student Internationalization Ratio** | `fact_student` | $\left(\frac{\text{International Students}}{\text{Total Students}}\right) \times 100$ | Percentage (%) | Retained as `NaN` (No blind zero fills) |
| **4. Faculty-Student Capacity Ratio** | `fact_student` | $\frac{100}{\text{Students per Staff}}$ | Staff / 100 Students | Retained as `NaN` for missing / non-positive values |
| **5. Academic Reputation** | `fact_university_performance` | Raw academic peer evaluation score | Score (0–100) | Retained as `NaN` |
| **6. Employer Reputation Score** | `fact_university_performance` | Raw corporate recruiter rating | Score (0–100) | Retained as `NaN` |

* **Formula Accuracy:** The Research Productivity Index applies equal weighting to productivity and citation impact.
* **Ratio Normalization:** Faculty-Student Capacity Ratio converts student-to-staff ratios into standard headcount per 100 students to ensure intuitive comparative visualization.
* **Missing Value Rationale:** All unmapped or non-reported fields are deliberately maintained as `NaN` rather than imputed with zeros to prevent artificial skewing of regional performance averages in downstream analytics.

### 4. 📁 Master Dataset Deliverable (`eduvision_final_dataset.xlsx`)
The main output is an Excel workbook containing 3 structured sheets:
### Sheet Breakdown
* **`Executive KPI Overview`**: Quick summary cards (3,536 total universities) and KPI definitions.
* **`Master Dataset`**: The complete combined data table (3,536 rows × 12 columns) with clean styling.
* **`Data Dictionary`**: Simple guide explaining every column name, data type, and source.

### 5. 📈 Visual Analytics & Executive Dashboards (Milestone 3 & 4)
The visual platform features a 4-Dashboard Suite built in Tableau Desktop and published for interactive web deployment:

* **Dashboard 1: `University Overview` (Global & National Standing)** — High-level ranks, overall composite scores, and geographic distribution.
* **Dashboard 2: `Research Analytics` (Citations & Academic Output)** — Citation density vs. peer academic reputation scatter plots and research impact leaderboards.
* **Dashboard 3: `Student Analytics` (Diversity & Learning Environment)** — International student proportions, overall enrollment, and student-to-faculty ratios.
* **Dashboard 4: `Country Comparison` (National Benchmarking)** — Cross-country higher education benchmarking and national performance trends.

### 6. Live Deployment & Documentation
* **Interactive Tableau Public Platform:** [EduVision Analytics Suite on Tableau Public](https://public.tableau.com/views/EduViz/ResearchAnalytics?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
* **Official Data Source Attribution:** Source: `public.tableau.com`
* **Executive Story Document:** Located under Milestone_4/EduVision Analytics System - Dashboard Story Document.pdf

