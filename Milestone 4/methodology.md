# EduVision_DV: Technical Methodology Document
### Infosys Springboard Virtual Internship Project

---

## 1. Project Overview & Scope
EduVision_DV is a comparative higher education business intelligence project designed to synthesize institutional data from the **QS World University Rankings 2025** and the **Times Higher Education (THE) World University Rankings**.

The primary objective is to deliver an end-to-end data pipeline: from raw, heterogenous source files to a validated, harmonized master dataset, and finally to 4 interactive, production-grade dashboards in **Tableau Desktop**.

---

## 2. Source Datasets & Architecture

### 2.1 QS World University Rankings 2025 (`infosys dataset.csv`)
- **Nature of Data:** Macro institutional rankings covering 1,503 universities globally across 106 countries.
- **File Characteristics:** CSV formatted, encoded with Latin-1 (`ISO-8859-1`) due to diacritical characters in non-English university names.
- **Key Columns:** `RANK_2025`, `Institution_Name`, `Location`, `Region`, `SIZE`, `FOCUS`, `RES.`, `STATUS`, `Academic_Reputation_Score`, `Faculty_Student_Score`, `Citations_per_Faculty_Score`, `International_Students_Score`, and `Overall_Score`.
- **Role in Pipeline:** Foundational base dataset (Primary Key: `Institution_Name`).

### 2.2 Times Higher Education World University Rankings (`Top_Universities_THE.xlsx`)
- **Nature of Data:** Specialized performance indicators for 200 premier global research universities across 29 jurisdictions.
- **File Characteristics:** Microsoft Excel OpenXML Spreadsheet (`.xlsx`).
- **Key Columns:** `Rank`, `Dense Rank`, `University Name`, `Location`, `Overall Score`, `Teaching`, `Research Environment`, `Research Quality`, `Industry`, `International Outlook`, `No. of FTE Students`, `No. of Students per Staff`, `International Students`.
- **Role in Pipeline:** Supplementary granular metrics provider (Secondary Source).

---

## 3. Data Cleaning Pipeline

### 3.1 QS Cleaning Procedures
1. **Encoding Handling:** The file contains European accented characters (e.g., *Université PSL*, *Technische Universität Dresden*, *École Polytechnique*). Ingestion explicitly uses `latin-1` to prevent Unicode decode errors.
2. **String Trimming:** All string categorical variables (`Institution_Name`, `Location`, `Region`, `SIZE`, `FOCUS`, `RES.`, `STATUS`) undergo whitespace stripping (`.str.strip()`) to prevent merge failures.
3. **Rank Normalization (`Rank_2025_Numeric`):**
   - Pure numeric strings (`1`, `2`, ..., `600`) and tied ranks (`15=`, `34=`) are converted to their direct numeric float equivalents (`1.0`, `15.0`).
   - Banded ranks (e.g., `601-610`, `1201-1400`) are mapped to the statistical midpoint:
     $$\text{Midpoint} = \frac{\text{Lower Band} + \text{Upper Band}}{2}$$
     *Example:* `1201-1400` $\rightarrow 1300.5$.
   - Bounded open-ended rank `1401+` is mapped to `1401.0`.
   - The original `RANK_2025` is preserved intact for display and categorical sorting.
4. **Overall Score Cleaning & Ethical Null Handling:**
   - QS only publishes exact composite scores for the top ~600 institutions. For institutions ranked below 600, the raw data encodes `Overall_Score` as `'-'`.
   - All `'-'` characters are strictly transformed to `NaN`.
   - **Crucial Rule:** Missing scores are **never imputed with zero or cohort means**. Imputing zero would distort regional averages, while mean imputation would artificially inflate unranked institutions.
   - Result: Exactly 600 non-null scores, 903 true analytical nulls.
5. **Research Intensity (`RES.`):** Verified categories and exact cohort sizes:
   - `VH` (Very High): 1,021 institutions
   - `HI` (High): 362 institutions
   - `MD` (Medium): 104 institutions
   - `LO` (Low): 16 institutions

### 3.2 THE Cleaning Procedures
1. **Preservation of Raw Geography:** The raw `Location` is preserved in `THE_Location`.
2. **Country Normalization:** Geo-political naming conventions differ between QS and THE. The following mapping aligns THE with the QS standard:
   - `China` $\rightarrow$ `China (Mainland)` (13 universities)
   - `Hong Kong` $\rightarrow$ `Hong Kong SAR` (5 universities)
   - `Macao` $\rightarrow$ `Macau SAR` (1 university)
3. **Numeric Type Standardization:**
   - Removal of non-numeric characters (commas, percent signs) from `No. of FTE Students`, `No. of Students per Staff`, and `International Students`.
   - Coercion to standard IEEE floating-point representation.

---

## 4. Entity Matching & Data Integration

### 4.1 Integration Architecture
A strict **LEFT JOIN** is executed using QS as the master left table and the cleaned THE dataset as the right table:
$$\text{Dataset}_{\text{Integrated}} = \text{QS} \bowtie_{\text{Institution\_Name}} \text{THE}$$

- Master left row count: **1,503 rows**.
- Matched cohort: **195 universities**.
- Unmatched cohort: **1,308 universities**.
- Unmatched THE fields remain strictly `NaN` / `null`.

### 4.2 University Name Harmonization
Direct string matching yielded 127 exact name matches. The remaining 73 THE institutions were systematically evaluated.

**Excluded Institutions (5 entities remain unmatched):**
1. `Karolinska Institute` (Sweden): Highly specialized medical university; not ranked in the QS general university league table.
2. `Charité - Universitätsmedizin Berlin` (Germany): Joint medical faculty of Free University Berlin and Humboldt University Berlin; ranked via its parent universities in QS, not as a standalone university.
3. `Scuola Normale Superiore di Pisa` (Italy): Elite collegiate institution not included in QS overall top 1,500.
4. `University of Massachusetts` (USA): Multi-campus system in THE; QS separately ranks *University of Massachusetts Amherst* and *University of Massachusetts Boston*. Forcing a match would introduce entity confusion.
5. `Indiana University` (USA): Multi-campus system in THE; QS separately evaluates *Indiana University Bloomington* and *Indiana University–Purdue University Indianapolis (IUPUI)*.

**Approved Manual Mappings (68 validated entities):**
All 68 variations were resolved through verified institutional identity:
- *MIT*: `Massachusetts Institute of Technology` $\rightarrow$ `Massachusetts Institute of Technology (MIT)`
- *Caltech*: `California Institute of Technology` $\rightarrow$ `California Institute of Technology (Caltech)`
- *UC Berkeley*: `University of California Berkeley` $\rightarrow$ `University of California, Berkeley (UCB)`
- *ETH Zurich*: `ETH Zurich` $\rightarrow$ `ETH Zurich - Swiss Federal Institute of Technology`
- *NUS*: `National University of Singapore` $\rightarrow$ `National University of Singapore (NUS)`
- *NTU*: `Nanyang Technological University Singapore` $\rightarrow$ `Nanyang Technological University, Singapore (NTU)`
- *EPFL*: `École Polytechnique Fédérale de Lausanne` $\rightarrow$ `EPFL`
- *NYU*: `New York University` $\rightarrow$ `New York University (NYU)`
- *UCSD*: `University of California San Diego` $\rightarrow$ `University of California, San Diego (UCSD)`
- *UCLA*: `University of California Los Angeles` $\rightarrow$ `University of California, Los Angeles (UCLA)`
- *LSE*: `London School of Economics and Political Science` $\rightarrow$ `The London School of Economics and Political Science (LSE)`
- *LMU Munich*: `LMU Munich` $\rightarrow$ `Ludwig-Maximilians-Universität München`
- *Heidelberg*: `Universität Heidelberg` $\rightarrow$ `Ruprecht-Karls-Universität Heidelberg`
- *Bonn*: `University of Bonn` $\rightarrow$ `Rheinische Friedrich-Wilhelms-Universität Bonn`
- *Freiburg*: `University of Freiburg` $\rightarrow$ `Albert-Ludwigs-Universitaet Freiburg`
- *Tübingen*: `University of Tübingen` $\rightarrow$ `Eberhard Karls Universität Tübingen`
- *Würzburg*: `University of Würzburg` $\rightarrow$ `Julius-Maximilians-Universität Würzburg`
- *Münster*: `University of Münster` $\rightarrow$ `Westfälische Wilhelms-Universität Münster`
- *Dresden*: `TU Dresden` $\rightarrow$ `Technische Universität Dresden`
- *TU Berlin*: `Technical University of Berlin` $\rightarrow$ `Technische Universität Berlin (TU Berlin)`
- *KIT*: `Karlsruhe Institute of Technology` $\rightarrow$ `KIT, Karlsruhe Institute of Technology`
- *Bologna*: `University of Bologna` $\rightarrow$ `Alma Mater Studiorum - University of Bologna`
- *UNSW*: `UNSW Sydney` $\rightarrow$ `The University of New South Wales (UNSW Sydney)`
- *KAIST*: `Korea Advanced Institute of Science and Technology (KAIST)` $\rightarrow$ `KAIST - Korea Advanced Institute of Science & Technology`
- *POSTECH*: `Pohang University of Science and Technology (POSTECH)` $\rightarrow$ `Pohang University of Science And Technology (POSTECH)`
- *PSL*: `Paris Sciences et Lettres – PSL Research University Paris` $\rightarrow$ `Université PSL`
- *(and 41 additional UK, US, European, and Australian universities)*.

---

## 5. KPI Engineering & Definitions

Six primary Key Performance Indicators (KPIs) and three formatted presentation display fields were engineered:

### KPI 1: Global Ranking Score
- **Technical Field Name:** `KPI_Global_Ranking_Score`
- **Source:** QS `Overall_Score`
- **Formula:** `Overall_Score`
- **Mathematical Properties:** Continuous metric $[20.80, 100.00]$, $\mu = 41.84$.
- **Analytical Coverage:** Top 600 ranked institutions (39.92% coverage). 903 unranked institutions are `NaN`.

### KPI 2: Academic Reputation Score
- **Technical Field Name:** `KPI_Academic_Reputation_Score`
- **Source:** QS `Academic_Reputation_Score`
- **Formula:** `Academic_Reputation_Score`
- **Mathematical Properties:** Continuous survey percentile $[1.30, 100.00]$, $\mu = 20.29$.
- **Analytical Coverage:** 1,503 institutions (100% complete coverage).

### KPI 3: Average Students per Staff (Faculty-to-Student Ratio)
- **Technical Field Name:** `KPI_Faculty_to_Student_Ratio`
- **Source:** THE `No. of Students per Staff` (`THE_No_of_Students_per_Staff`)
- **Formula:** `THE_No_of_Students_per_Staff`
- **Business Interpretation:** Represents the headcount of enrolled full-time students supported by each academic staff member.
- **Reporting Label:** Must be labeled **"Average Students per Staff"** (e.g., `17.4 students/staff`), **never** formatted as a colon ratio like `1:17.4`.
- **Mathematical Properties:** Range $[3.80, 58.00]$, $\mu = 17.44$.
- **Analytical Coverage:** 195 matched institutions (13.0% coverage). 1,308 unmatched institutions are `NaN`.

### KPI 4: International Student Percentage
- **Technical Field Name:** `KPI_International_Student_Pct`
- **Source:** THE `International Students` (`THE_International_Students`)
- **Formula:** `THE_International_Students * 100.0`
- **Business Interpretation:** Converts fractional proportion ($0.01 - 0.72$) into percentage points ($1.0\% - 72.0\%$).
- **Mathematical Properties:** Range $[1.00\%, 72.00\%]$, $\mu = 25.48\%$.
- **Analytical Coverage:** 195 matched institutions (13.0% coverage). 1,308 unmatched institutions are `NaN`.

### KPI 5: Research Impact Score
- **Technical Field Name:** `KPI_Research_Impact_Score`
- **Source:** QS `Citations_per_Faculty_Score`
- **Formula:** `Citations_per_Faculty_Score`
- **Business Interpretation:** Evaluates the relative volume of academic citations generated per faculty member adjusted for institutional size.
- **Mathematical Properties:** Range $[1.00, 100.00]$, $\mu = 23.50$.
- **Analytical Coverage:** 1,503 institutions (100% complete coverage).

### KPI 6: Research Productivity (Proxy)
- **Technical Field Name:** `KPI_Research_Productivity_Proxy`
- **Source:** THE `Research Environment` (`THE_Research_Environment`)
- **Formula:** `THE_Research_Environment`
- **Methodological Context:** QS does not publish a standalone metric measuring pure publication volume or output count. The project mentor explicitly rejected substituting `Sustainability_Score` or `Research Quality`. Publication-volume analysis was not implemented because the available QS/THE source data does not provide a directly comparable publication-count field. In strict adherence to analytical honesty, no publication metric was fabricated; THE *Research Environment* is utilized as a specialized analytical proxy.
- **Critical Policy:** In all dashboards, legends, and executive documentation, this metric must be titled **"Research Productivity (Proxy)"**. It must **never** be cited as the official THE Research Productivity score.
- **Mathematical Properties:** Range $[34.90, 100.00]$, $\mu = 61.23$.
- **Analytical Coverage:** 195 matched institutions (13.0% coverage). 1,308 unmatched institutions are `NaN`.

---

## 6. Presentation / Tooltip Display Calculations

To prevent awkward Tableau tooltips containing blank lines or raw `Null` tokens, three user-friendly string fields were engineered:

1. **`Display_Students_per_Staff`**:
   ```sql
   IF ISNULL([KPI_Faculty_to_Student_Ratio]) THEN
       "Sourced from THE (Data not available)"
   ELSE
       STR(ROUND([KPI_Faculty_to_Student_Ratio], 1)) + " students/staff"
   END
   ```
2. **`Display_Int_Student_Pct`**:
   ```sql
   IF ISNULL([KPI_International_Student_Pct]) THEN
       "Sourced from THE (Data not available)"
   ELSE
       STR(ROUND([KPI_International_Student_Pct], 1)) + "%"
   END
   ```
3. **`Display_Research_Productivity`**:
   ```sql
   IF ISNULL([KPI_Research_Productivity_Proxy]) THEN
       "THE Environment Proxy (Data not available)"
   ELSE
       STR(ROUND([KPI_Research_Productivity_Proxy], 1)) + " pts"
   END
   ```

---

## 7. Data Quality & Limitations Summary
1. **Truncated Scored Sample:** QS overall rankings provide scores for the top 600 universities only. Analyses aggregating `KPI_Global_Ranking_Score` reflect this top-tier cohort.
2. **THE Coverage Limitation:** THE data is integrated for 195 top research universities. Visualizations relying on THE indicators (`KPI_Faculty_to_Student_Ratio`, `KPI_International_Student_Pct`, `KPI_Research_Productivity_Proxy`, `THE_No_of_FTE_Students`) reflect this subset.
3. **No Zero Substitution:** In all analytical aggregations, missing values are excluded via pairwise/listwise deletion rather than replaced with 0, ensuring undistorted means.
