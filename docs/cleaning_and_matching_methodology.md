# EduVision Cleaning and Matching Methodology

This document details the standardization, entity resolution, numeric parsing, and dimensional modeling methodology.

---

## 1. Data Cleaning & Type Conversion
1. **String Normalization**:
   - Stripped leading/trailing whitespace.
   - Removed accents/diacritics using Unicode `NFKD` decomposition.
   - Converted all string identifiers to lowercase for matching, while preserving original title-case display names in dimension tables.
2. **Numeric Type Coercion**:
   - `pd.to_numeric(..., errors="coerce")` applied across all score and indicator fields.
   - Ranks containing text or range notation (e.g. `101=`, `501-510`, `1200+`) parsed into numeric midpoint or lower bound values (`parse_rank`).
   - Percentages containing `%` symbols stripped and converted to 0-100 float values.
   - Student counts containing commas (`20,774`) converted to numeric float values.

---

## 2. Country Standardization Methodology
1. **Canonical Dictionary**:
   - Mapped 140 unique country strings across 4 raw datasets into 258 canonical World Bank country entities (`COUNTRY_MAP`).
   - Synonyms such as `"USA"`, `"United States of America"`, `"US"` collapsed into `"United States"`.
   - `"China (Mainland)"` mapped to `"China"`; `"South Korea"` mapped to `"Korea, Rep."`.
2. **Dimension Key Generation**:
   - Generated sequential `country_id` surrogate keys (`CTY_001`, `CTY_002`, ...).

---

## 3. University Entity Resolution Methodology
1. **Candidate Identification**:
   - Cleaned university strings by removing parenthetical suffixes (e.g., `(UK)`), stripping punctuation, and removing leading articles (`"The "`).
   - Created a stop-word filtered token key for each university within its canonical country.
2. **Entity Grouping & Matching**:
   - Grouped university records by `(country_id, token_key)`.
   - Assigned a single canonical display name (prioritizing QS name -> THE name -> WUR name).
   - Generated sequential `university_id` surrogate keys (`UNI_0001` ... `UNI_3402`).
3. **Validation & Non-Aggressive Rule Enforcement**:
   - No cross-country matching allowed.
   - No aggressive fuzzy merging between distinct branch campuses or affiliated institutes.
