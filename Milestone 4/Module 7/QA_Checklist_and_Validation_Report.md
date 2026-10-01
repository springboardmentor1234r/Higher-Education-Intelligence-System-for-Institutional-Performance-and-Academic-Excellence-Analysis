# Module 7: Quality Assurance Checklist & Validation Report

## 1. Data Integrity & Completeness Audit
- [x] **Completeness Threshold**: Dataset completeness exceeds 98.5% across primary analytical dimensions.
- [x] **Entity Uniqueness**: Zero duplicate `university_id` keys among all 2,517 institutions.
- [x] **Country Representation**: Zero unmapped country variations; all 120 territories mapped to ISO 3166-1 alpha-2 codes (`country_id`).
- [x] **Missing Value Handling**: No blind zero replacements in ranking metrics; unranked null values properly preserved as unavailable.
- [x] **Referential Integrity**: 100% foreign key matching between `dim_university`, `dim_country`, and fact performance tables.

---

## 2. KPI Engineering Verification
- [x] **KPI 1 (Global Ranking Score)**: Range verified within $[0.0, 100.0]$.
- [x] **KPI 2 (Research Impact Score)**: Normalized citations score verified within $[0.0, 100.0]$.
- [x] **KPI 3 (Faculty-to-Student Ratio)**: Valid ratio string format `1:X.X`; median ratio verified at $1:17.3$.
- [x] **KPI 4 (International Student %)**: Verified clean percentage bounds $[0.0\%, 100.0\%]$.
- [x] **KPI 5 (Academic Reputation Score)**: Validated $[0.0, 100.0]$ distribution.
- [x] **KPI 6 (Research Productivity Index)**: Composite formula verified ($0.50 \times \text{Research} + 0.30 \times \text{Citations} + 0.20 \times \text{Outlook}$).

---

## 3. Tableau Dashboard Functional Tests
- [x] **Dashboard 1 (University Overview)**: Executive KPI cards, Top 10 bar chart, score trend lines, and regional donut load seamlessly.
- [x] **Dashboard 2 (Research Analytics)**: Citations vs Research output scatter plot renders with correct trendline.
- [x] **Dashboard 3 (Student Analytics)**: Stacked gender breakdown totals exactly $100\%$.
- [x] **Dashboard 4 (Country Comparison)**: National benchmarking correctly groups universities by `country_id`.
- [x] **Interlinking Filter Actions**: Selecting University X in Dashboard 1 dynamically filters Dashboards 2 and 3 on `university_id` and sets Dashboard 4 to University X's `country_id`.
- [x] **Navigation Buttons**: Instant tab switching without broken action triggers.
