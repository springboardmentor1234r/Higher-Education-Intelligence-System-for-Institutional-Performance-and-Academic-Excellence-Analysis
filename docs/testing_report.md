# EduVision_DV: Comprehensive Testing & Validation Report
### Infosys Springboard Virtual Internship Project

---

## 1. Quality Assurance Overview
This document details the complete validation audit executed across all phases of the **EduVision_DV** project. Every data transformation, join logic, KPI formula, and visual filter constraint was verified against predefined benchmark targets.

---

## 2. Integrity of Raw Datasets
To ensure reproducibility and analytical honesty, raw source files were inspected and left unmodified:

| File Name | Original Path | File Size | MD5 Checksum | Status |
| :--- | :--- | :--- | :--- | :--- |
| `infosys dataset.csv` | Project Root | 231,206 bytes | `7dacd93560c7d7158971c364b902e2f7` | **Preserved / Untouched** |
| `Top_Universities_THE.xlsx` | Project Root | 29,594 bytes | `4d73bb53db719fb5bf5543af11ec9be3` | **Preserved / Untouched** |
| `Feature_Mapping_Table infosys.pdf` | Project Root | 178,407 bytes | Reference document | **Preserved / Untouched** |

---

## 3. Data Integration & Matching Validation

### 3.1 Universe Dimensions:
- **Base Universe (QS):** 1,503 institutions across 106 countries.
- **Secondary Universe (THE):** 200 institutions across 29 jurisdictions.
- **Integrated Dataset Count:** **1,503 rows** (100% preservation of base universe via left join).

### 3.2 University Match Audit:
- **Expected Matches:** Exactly 195 institutions.
- **Actual Matches:** Exactly 195 institutions.
- **Match Rate:** $195 / 200 = 97.5\%$ of THE sample; $195 / 1503 = 12.97\%$ of QS global sample.

### 3.3 Audit of Unmatched THE Institutions:
All 5 expected unmatchable institutions were verified to have remained strictly unmatched with zero synthetic imputation:

| THE University Name | Location | Analytical Reason for Exclusion | Null Preservation Verified |
| :--- | :--- | :--- | :--- |
| **Karolinska Institute** | Sweden | Medical specialist university; omitted from QS general league table | **Yes (`NaN`)** |
| **Charité - Universitätsmedizin Berlin** | Germany | Medical faculty evaluated via parent institutions in QS | **Yes (`NaN`)** |
| **Scuola Normale Superiore di Pisa** | Italy | Elite collegiate institution not included in QS top 1500 | **Yes (`NaN`)** |
| **University of Massachusetts** | United States | Ambiguous multi-campus entity; QS splits *Amherst* and *Boston* | **Yes (`NaN`)** |
| **Indiana University** | United States | Ambiguous multi-campus entity; QS splits *Bloomington* and *IUPUI* | **Yes (`NaN`)** |

---

## 4. Comprehensive KPI Validation Table

All 6 engineered KPIs were verified against theoretical benchmarks and statistical boundaries:

| KPI Indicator | Technical Field | Expected Non-Null | Actual Non-Null | Expected Nulls | Actual Nulls | Min Value (Exp / Act) | Max Value (Exp / Act) | Mean Value (Exp / Act) | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Global Ranking Score** | `KPI_Global_Ranking_Score` | 600 | **600** | 903 | **903** | 20.80 / **20.80** | 100.00 / **100.00** | 41.84 / **41.84** | **PASSED** |
| **Academic Reputation** | `KPI_Academic_Reputation_Score` | 1503 | **1503** | 0 | **0** | 1.30 / **1.30** | 100.00 / **100.00** | 20.29 / **20.29** | **PASSED** |
| **Students per Staff** | `KPI_Faculty_to_Student_Ratio` | 195 | **195** | 1308 | **1308** | 3.80 / **3.80** | 58.00 / **58.00** | 17.44 / **17.44** | **PASSED** |
| **International Student %** | `KPI_International_Student_Pct` | 195 | **195** | 1308 | **1308** | 1.00% / **1.00%** | 72.00% / **72.00%** | 25.48% / **25.48%** | **PASSED** |
| **Research Impact** | `KPI_Research_Impact_Score` | 1503 | **1503** | 0 | **0** | 1.00 / **1.00** | 100.00 / **100.00** | 23.50 / **23.50** | **PASSED** |
| **Research Productivity (Proxy)** | `KPI_Research_Productivity_Proxy` | 195 | **195** | 1308 | **1308** | 34.90 / **34.90** | 100.00 / **100.00** | 61.23 / **61.23** | **PASSED** |

---

## 5. Specific Cohort & Category Verification

### 5.1 Geographic Cohorts:
- **Total Unique Countries in QS:** 106 (Verified: 106)
- **United States Universities in QS:** 197 (Verified: 197)
- **United Kingdom Universities in QS:** 90 (Verified: 90)
- **China (Mainland) Universities in QS:** 71 (Verified: 71)

### 5.2 Research Intensity (`RES.`) Breakdown:
- `VH` (Very High): Target = 1,021 | Actual = **1,021**
- `HI` (High): Target = 362 | Actual = **362**
- `MD` (Medium): Target = 104 | Actual = **104**
- `LO` (Low): Target = 16 | Actual = **16**
- **Total:** 1,503 institutions (0 missing values).

### 5.3 Rank Bands:
- `1201-1400` mapped to midpoint `1300.5` (Verified)
- `1401+` mapped to `1401.0` (Verified)
- Standard integer ranks preserved without decimal truncation (Verified).

---

## 6. Missing Data Policy & Treatment Audit
1. **Zero-Imputation Prohibited:** None of the missing fields were filled with zeros.
   - Example: Imputing 0 for unranked `KPI_Global_Ranking_Score` would distort the global average from `41.84` down to `16.70`. This error was strictly prevented.
2. **Mean-Imputation Prohibited:** No synthetic means or regression imputations were applied to unmatched THE attributes.
3. **Display Tooltip Handling:** Formatted display fields (`Display_Students_per_Staff`, `Display_Int_Student_Pct`, `Display_Research_Productivity`) provide explicit informational labels (`"Sourced from THE (Data not available)"`) rather than rendering blank gaps or confusing null tags.

---

## 7. Google Colab Notebook Execution Verification
- **Notebook File:** `EduVision_DV/notebooks/EduVision_DV_Colab.ipynb`
- **Execution Environment:** Python 3.10+ / Colab-compatible.
- **Automated Execution Test:** Passed all 18 cells with zero runtime errors.
- **Output Artifacts Generated:**
  - `university_final_dataset.csv` (469,557 bytes)
  - `university_final_dataset.xlsx` (361,353 bytes)

---

## 8. Tableau Desktop Dashboard Compliance Checklist

| Requirement | Implementation Specification | Status |
| :--- | :--- | :--- |
| **Dashboard 1: University Overview** | Dark theme (`#12161A`), MIT #1, 1503 total, 41.84 dynamic avg score, Top 10 bar, Donut by Region, World Map | **Ready for GUI Placement** |
| **Dashboard 2: Research Analytics** | Accent `#FF9F1C`, Scatter plot (Productivity vs Impact), Box plot by `RES.`, Top 10 by Impact, Mandatory Proxy note | **Ready for GUI Placement** |
| **Dashboard 3: Student Analytics** | Accent `#2EC4B6`, 17.4 students/staff, 25.5% intl, 5.46M FTE, Students per staff by Region, Scatter, Top 10 enrollment | **Ready for GUI Placement** |
| **Dashboard 4: Country Comparison** | Accent `#00D2C4`, 106 countries, US 197 unis, Country Heatmap table, World map, Filter/Highlight action | **Ready for GUI Placement** |
| **Filter Logic** | `Location` set to **Only Relevant Values** across dashboards | **Specified** |
| **Proxy Labeling** | `KPI_Research_Productivity_Proxy` strictly labeled `Research Productivity (Proxy)` | **Verified** |
| **Ratio Formatting** | `KPI_Faculty_to_Student_Ratio` displayed as `17.4 students/staff`, not `1:17.4` | **Verified** |
