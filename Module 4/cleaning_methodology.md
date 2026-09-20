# EduVision_DV: Data Cleaning & ETL Methodology

This document outlines the systematic ETL pipeline developed to transform raw higher education datasets into an integrated, audit-compliant star schema.

---

## 1. Column Standardization
All raw table headers were normalized using regular expressions:
- Leading/trailing whitespace trimmed
- Lowercase conversion
- Spaces and hyphens replaced with underscores (`_`)
- BOM characters (`\ufeff`) stripped

---

## 2. University Name Normalization & High-Fidelity Matching
University names exhibit widespread typographical divergence across ranking organizations (e.g., `"Massachusetts Institute of Technology (MIT)"` vs. `"Massachusetts Institute of Technology"`).

### Transformation Algorithm:
1. **Acronym Stripping:** Removed parenthetical abbreviations using regex `r"\(.*?\)"`.
2. **Punctuation Removal:** Stripped all non-alphanumeric punctuation marks using `r"[^\w\s]"`.
3. **Whitespace Compression:** Collapsed multiple contiguous spaces into single spaces.
4. **Deterministic Join:** Merged entities on standardized strings, yielding **849 exact, validated matches** between QS and THE, and **804 matches** between QS and WUR.
5. **Rejection of Fallback Indexing:** Strictly eliminated row-order fallback assignment, preventing erroneous data swaps between distinct institutions.

---

## 3. Country Name Harmonization
Geopolitical nomenclature was reconciled against an international sovereignty reference dictionary:
- `"USA"`, `"United States of America"`, `"US"` $\rightarrow$ `"United States"`
- `"UK"`, `"Great Britain"`, `"England"`, `"Scotland"` $\rightarrow$ `"United Kingdom"`
- `"Korea (the Republic of)"`, `"Republic of Korea"` $\rightarrow$ `"South Korea"`
- `"China (Mainland)"`, `"Mainland China"` $\rightarrow$ `"China"`
- `"Czechia"` $\rightarrow$ `"Czech Republic"`
- `"Turkey"` $\rightarrow$ `"Turkiye"`

---

## 4. Missing Value Treatment
In accordance with Section 16–17 of the Project Guide:
- Primary and Foreign Keys: Zero missing values permitted.
- Critical Dimensions (`university_name`, `country_name`, `region`): Verified 100% populated.
- Scores and Metrics: Missing scores are preserved as `NaN` rather than artificially zero-filled, preserving true statistical variance.

---

## 5. Scope Optimization for World Bank Indicators
The raw World Bank dataset spans 886,930 rows with 4,000 indicators from 1970 onwards. To ensure Tableau high-performance responsiveness, the data was:
1. Filtered strictly to prioritized education indicators (expenditure, tertiary enrollment, completion, pupil-teacher ratios).
2. Constrained to the modern evaluation window (2010–2023).
3. Reshaped into a clean, unpivoted Star Schema fact table (`country_id`, `country_name`, `year`, `indicator`, `value`).
