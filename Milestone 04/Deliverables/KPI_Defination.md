# KPI Definitions & Formula Reference

### 1. Global Ranking Score
- **Formula:** `(1 - (Global_Rank - 1) / (Max_Rank - 1)) * 100`
- **Derivation:** Normalized continuous metric where Rank 1 = 100.0 and lowest rank approaches 0.0.

### 2. Research Impact Score
- **Source:** Cascaded THE 2024 Research Quality with WUR Citations fallback.
- **Aggregation:** Average (`AVG`).

### 3. Faculty-to-Student Ratio
- **Source:** THE Students-to-Staff ratio and QS Faculty-Student ratio.
- **Aggregation:** Average (`AVG`).

### 4. International Student Percentage
- **Source:** Extracted from international student volume indicators.
- **Format:** `n#,##0.0"%"`
- **Aggregation:** Average (`AVG`).

### 5. Female & Male Student Percentage
- **Source:** Derived from WUR Female-to-Male student ratio (`WUR_Female_Male_Ratio`).
- **Formula:** 
  - `Female_Percentage = Female_Ratio / (Female_Ratio + Male_Ratio) * 100`
  - `Male_Percentage = Male_Ratio / (Female_Ratio + Male_Ratio) * 100`
- **Format:** `n#,##0.0"%"`
- **Aggregation:** Average (`AVG`).
