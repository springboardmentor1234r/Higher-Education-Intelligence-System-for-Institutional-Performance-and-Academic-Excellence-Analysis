# EduVision DV – Dashboard Testing Report

## 1. Purpose

This report documents Milestone 4 testing for the EduVision DV Tableau dashboard suite.

The testing covers:
- KPI configuration and field validation
- Ranking configuration
- Dashboard navigation
- Dashboard filter actions
- Educational metric coverage
- Visual/layout structure

## 2. Workbook Tested

**File:** `EduVision_DV.twbx`

The packaged workbook was inspected and contains four dashboards:

1. University Overview
2. Research Analytics
3. Students Analytics
4. Country Comparison

The workbook contains 44 worksheets across the dashboard suite.

## 3. University Overview Testing

The University Overview contains the following KPI worksheets:

- Avg Overall Score
- Academic Reputation Score
- Research Impact Score
- Student Per Staff Ratio
- International Student Percentage
- Global Ranking

The main analytical visuals include:

- Top University Rankings
- Top 10 Countries by University Count
- Overall Score Distribution
- Top 10 Universities by Academic Reputation
- Research Performance by University
- Top 10 Universities by International Students Score

The configured source fields were inspected and correspond to the intended measures.

## 4. Research Analytics Testing

The Research Analytics dashboard contains:

- Research Score
- Citations Score
- Student–Staff Ratio
- International Students %
- Top 10 Universities by Research Score
- Top 10 Universities by Citations Score
- Research Score Distribution
- Teaching vs Research Performance
- International Outlook by University
- Student Staff Ratio by University

The workbook structure confirms the expected research-related fields are used.

## 5. Students Analytics Testing

The Students Analytics dashboard contains:

- Total Students
- Student Staff Ratio
- International Students Percentage
- Female Students %
- Top 10 Universities by Total Students
- Top 10 Universities by International Students %
- Female vs Male Students by University
- Student–Staff Ratio by University
- Teaching vs Research vs Citations
- Total Students Distribution

The configured measures correspond to student population, diversity and student/staff analysis.

## 6. Country Comparison Testing

The Country Comparison dashboard contains six KPI worksheets:

- Education Expenditure % GDP
- Tertiary Enrollment
- Adult Literacy Rate
- Primary Completion Rate (%)
- Tertiary Teachers
- GDP per Capita

It also contains six country comparison/ranking visuals covering education expenditure, tertiary enrollment, adult literacy, population, primary completion and government expenditure on education.

## 7. Navigation Testing

The workbook contains four navigation button objects on each dashboard. The navigation actions point to the four dashboard destinations.

During project testing, the user confirmed that the dashboard navigation works.

**Result: PASS**

## 8. Filter / Interaction Testing

Generated filter actions are present across University Overview, Research Analytics and Students Analytics. These actions use the dashboard as the target.

This configuration allows visual selections to act as filters, but it can also cause KPI cards to become blank when the selected value eliminates the KPI's available records.

This behavior was observed during project testing.

### Recommendation

Before final portfolio release, review each “Use as Filter” action in Tableau and exclude KPI sheets from visual-selection targets where appropriate, or replace dashboard-wide filtering with explicitly selected target worksheets.

## 9. Ranking Testing

The University Overview ranking worksheets use `Rank 2025 Numeric`.

The workbook includes dedicated Top 10 university and country ranking worksheets.

**Structural result: PASS**

## 10. Educational Metric Testing

The Country Comparison dashboard includes the required country-level education measures, while Students Analytics and Research Analytics contain university-level student and academic indicators.

**Coverage result: PASS**

## 11. Limitations

The packaged workbook's Hyper extracts could not be independently queried in this execution environment because the Tableau Hyper API was unavailable. Therefore:

- Workbook structure and field configuration were inspected directly from the Tableau workbook XML.
- Navigation and interaction configuration were inspected.
- Previously observed dashboard behavior was recorded.
- A numerical KPI accuracy percentage was not fabricated.

## 12. Final Result

The dashboard suite is structurally complete and suitable for Milestone 4 documentation.

**Overall testing status: CONDITIONAL PASS**

The remaining issue is the observed behavior where some dashboard-level filter selections can make KPI cards blank. This should be reviewed before a final “no major issues” sign-off.
