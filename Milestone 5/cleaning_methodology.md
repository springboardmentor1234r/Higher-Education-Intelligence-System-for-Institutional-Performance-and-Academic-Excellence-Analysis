# EduVision_DV: Data Cleaning & Preprocessing Methodology

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Higher Education Data Analytics  
**Date:** September 2026  

---

## 1. Overview & Data Pipeline Architecture

In the **EduVision_DV** project, transforming disparate higher education data into an integrated, audit-compliant star schema required resolving complex entity mismatches, formatting inconsistencies, and varying data granularities. Rather than relying on superficial, error-prone transformations, a systematic 6-stage ETL pipeline was engineered in Python:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         RAW DATA INGESTION                               │
│   QS 2025 (1,503 rows) | THE 2024 (2,673 rows) | WUR 2023 (2,341 rows)  │
│             World Bank EdStats (886,930 rows)                            │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    STAGE 1: HEADER STANDARDIZATION                       │
│   Trim spaces, lowercase, replace ' ' and '-' with '_', strip UTF-8 BOM  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│             STAGE 2: HIGH-FIDELITY UNIVERSITY RESOLUTION                 │
│   Regex acronym removal r"\(.*?\)", strip punctuation r"[^\w\s]",      │
│   collapse whitespace r"\s+", lowercase, canonical alias lookup         │
│   Outcome: 849 validated research matches, 804 student matches, 0 false  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│              STAGE 3: COUNTRY NOMENCLATURE HARMONIZATION                 │
│   Resolve geopolitical aliases (USA/US -> United States, UK -> United    │
│   Kingdom) and assign conformed country surrogate keys (C0001..C0106)    │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│          STAGE 4: MISSING VALUE & NUMERIC TYPE SANITIZATION              │
│   Enforce Category A/B/C rules; preserve NaN on non-evaluated metrics;   │
│   impute unranked tier scores via inverse percentile formula             │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│              STAGE 5: WORLD BANK INDICATOR SCOPING & RESHAPING           │
│   Filter to 6 core indicators, 2010-2023 window, unpivot wide to long    │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     EXPORT STAR SCHEMA & KPI MASTER                      │
│   dim_university, dim_country, fact_performance, fact_research,          │
│   fact_student, fact_country_education, kpi_master.csv                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Column Header Normalization

Raw source files contained inconsistent casing, arbitrary spaces, hyphens, and invisible UTF-8 byte-order marks (`\ufeff`). These inconsistencies cause silent lookup errors in Python and broken calculations in Tableau.

### Normalization Logic:
```python
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace(r"[^\w\s]", "", regex=True)
    )
    return df
```

### Mapping Examples:
- `Institution Name` -> `institution_name`
- `No of student per staff` -> `no_of_student_per_staff`
- `Female : Male Ratio` -> `female_male_ratio`
- `International Student` -> `international_student`
- `Citations_per_Faculty_Score` -> `citations_per_faculty_score`

---

## 3. University Name Normalization & High-Fidelity Entity Resolution

University names serve as the primary join spine connecting institutional performance (QS 2025), research impact (THE 2024), and student demographics (WUR 2023). However, naming conventions differ significantly across ranking organizations.

### 3.1 The Normalization Algorithm
To achieve maximum join accuracy without risking false positives, a deterministic 5-step string cleaning pipeline was implemented:

1. **Parenthetical Acronym Extraction & Stripping:** Ranking organizations often append acronyms in parentheses.
   ```python
   # Regex stripping of all content inside parentheses
   clean_name = re.sub(r"\(.*?\)", "", raw_name)
   ```
   *Example:* `"Massachusetts Institute of Technology (MIT)"` becomes `"Massachusetts Institute of Technology"`.
2. **Punctuation & Special Character Removal:** Removed apostrophes, commas, periods, and slashes.
   ```python
   clean_name = re.sub(r"[^\w\s]", "", clean_name)
   ```
   *Example:* `"King's College London"` becomes `"Kings College London"`.
3. **Whitespace Compression:** Collapsed multiple contiguous spaces into a single space and stripped boundaries.
   ```python
   clean_name = re.sub(r"\s+", " ", clean_name).strip()
   ```
4. **Lowercasing:** Converted all characters to lowercase to enable case-insensitive string hashing.
5. **Canonical Alias Resolution:** For recognized premier institutions with distinct institutional acronyms in secondary datasets, an explicit alias mapping table was utilized (e.g., `"IIT Bombay"` -> `"Indian Institute of Technology Bombay"`, `"IIT Delhi"` -> `"Indian Institute of Technology Delhi"`).

### 3.2 Join Outcome Verification
- **QS 2025 to THE 2024:** **849 exact, validated matches** out of 1,503 QS institutions.
- **QS 2025 to WUR 2023:** **804 exact, validated matches** out of 1,503 QS institutions.
- **False Positive Matches:** **0 false matches** detected across all manual and automated audits.

### 3.3 Strict Rejection of Row-Fallback Indexing
During initial prototyping in `education_cleaning.ipynb`, an un-normalized string comparison failed on institutions with parenthetical acronyms (such as MIT). An exploratory fallback mechanism that assigned secondary attributes by sequential row index (`iloc`) was identified. This caused catastrophic data corruption: University of Oxford's data was assigned to MIT, creating cascading misalignments throughout the fact tables.

This fallback logic was completely eliminated. The finalized pipeline relies strictly on deterministic string entity resolution, preserving data provenance and audit integrity.

---

## 4. Country Nomenclature Harmonization

Sovereignty and nation names exhibit substantial variance across international organizations. For instance, the United States was recorded as `"USA"`, `"United States"`, `"United States of America"`, and `"US"` across different sources.

### 4.1 Harmonization Reference Table
A canonical geopolitical reference mapping was implemented:

| Raw Input Strings | Standardized Name | Assigned `country_id` | Geographic Region |
|---|---|---|---|
| `USA`, `United States of America`, `US` | `United States` | `C0001` | North America |
| `UK`, `Great Britain`, `England`, `Scotland`, `Wales` | `United Kingdom` | `C0002` | Europe |
| `Korea (the Republic of)`, `Republic of Korea`, `Korea, South` | `South Korea` | `C0005` | Asia |
| `China (Mainland)`, `People's Republic of China` | `China` | `C0004` | Asia |
| `Czechia` | `Czech Republic` | `C0042` | Europe |
| `Turkey` | `Turkiye` | `C0051` | Europe / Asia |
| `Russian Federation` | `Russia` | `C0034` | Europe |
| `Hong Kong SAR`, `Hong Kong (SAR)` | `Hong Kong` | `C0008` | Asia |

---

## 5. Missing Value Treatment & Audit Rules

In strict compliance with Sections 16–17 of the project guidelines, missing values were categorized into three distinct tiers:

### 5.1 Category A: Critical Identifiers (Zero Tolerance)
- **Fields:** `university_id`, `university_name`, `country_id`, `country_name`.
- **Policy:** 0.0% missing values permitted. Any record missing a primary or foreign key was rejected at ingestion.
- **Audit Outcome:** 100% complete (0 missing keys across all 1,503 dimension records).

### 5.2 Category B: Numeric Performance Indicators (No Blind Zero-Filling)
- **Fields:** `overall_score`, `academic_reputation`, `citations_score`, `research_score`.
- **Policy:** Missing values were **never replaced with zero** without clear justification.
- **Methodological Rationale:** In higher education evaluation, an institution with a missing citation score is an institution whose research output was not surveyed or published by that ranking body for that year. Replacing `NaN` with `0.0` penalizes the institution as if it produced zero citations, severely distorting summary statistics (means, medians, standard deviations) and misrepresenting reality.
- **Rank Tier Percentile Imputation:** For QS 2025 institutions ranked outside the top 500 (where QS publishes rank bands rather than raw overall scores), an inverse percentile rank formula was applied:
  $$\text{Global Ranking Score} = \left( \frac{\text{Max Rank} - \text{Global Rank} + 1}{\text{Max Rank}} \right) \times 100$$
  This preserves relative global hierarchy without introducing artificial zeros.

### 5.3 Category C: Secondary & Optional Fields
- **Fields:** `sustainability_score`, `industry_income_score`, `female_male_ratio`.
- **Policy:** Where optional indicators were not provided by the ranking authority, values were preserved as nulls and clearly noted in data dictionary documentation.

---

## 6. Duplicate Detection & Key Validation

### Duplicate Verification Protocol:
1. **Row-Level Duplicates:** Executed `df.duplicated().sum()` on all raw datasets. Result: **0 full row duplicates**.
2. **Entity-Level Duplicates:** Executed `df['university_name'].duplicated().sum()` to verify institutional uniqueness.
3. **Surrogate Key Generation:** Generated structured surrogate keys with guaranteed uniqueness:
   - `university_id`: Sequential padded keys (`U0001` to `U1503`).
   - `country_id`: Conformed sovereign keys (`C0001` to `C0106`).

---

## 7. World Bank EdStats Scoping & Reshaping

The raw World Bank EdStats file contains 886,930 rows and 69 columns. Directly querying this file in Tableau created severe latency.

### Reshaping Pipeline:
1. **Indicator Selection:** Filtered strictly to six key indicators:
   - `SE.XPD.TOTL.GD.ZS`: Government expenditure on education (% of GDP)
   - `SE.TER.ENRR`: Gross enrolment ratio, tertiary (both sexes) (%)
   - `SE.TER.ENRR.FE`: Gross enrolment ratio, tertiary (female) (%)
   - `SE.TER.ENRR.MA`: Gross enrolment ratio, tertiary (male) (%)
   - `SE.SEC.ENRR`: Gross enrolment ratio, secondary (both sexes) (%)
   - `SE.ADT.LITR.ZS`: Adult literacy rate (% aged 15 and older)
2. **Temporal Window:** Restricted years to 2010–2023.
3. **Unpivoting (Wide to Long):** Reshaped wide year columns into an unpivoted long format (`country_id`, `country_name`, `year`, `indicator`, `value`).
4. **Result:** Reduced file size by 99.7% (down to 2,243 clean rows), enabling sub-second filtering in Tableau.

---

## 8. Summary of Cleaned Deliverables

| File Name | Record Count | Column Count | Primary Grain |
|---|---|---|---|
| `dim_university.csv` | 1,503 | 5 | One row per university (`university_id`) |
| `dim_country.csv` | 106 | 3 | One row per country (`country_id`) |
| `fact_university_performance.csv` | 1,503 | 12 | One row per university per year (`university_id`, `year`) |
| `fact_research.csv` | 849 | 8 | One row per university per year (`university_id`, `year`) |
| `fact_student.csv` | 804 | 7 | One row per university per year (`university_id`, `year`) |
| `fact_country_education.csv` | 2,243 | 5 | One row per country, year, indicator (`country_id`, `year`, `indicator`) |
| `kpi_master.csv` | 1,503 | 16 | Consolidated pre-joined master table for Tableau |

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**
