# EduVision_DV: Quality Assurance Checklist

**Overall Test Accuracy:** 100.0%

| Test ID | Category | Test Description | Status | Details |
|---------|----------|------------------|--------|---------|
| QA-01 | Key Integrity | Zero Duplicate University IDs in Dimension | **PASSED** | 0 duplicates found |
| QA-02 | Key Integrity | Zero Duplicate Country IDs in Dimension | **PASSED** | 0 duplicates found |
| QA-03 | Referential Integrity | 100% University Foreign Keys Valid in fact_performance | **PASSED** | All performance rows map to valid master universities |
| QA-04 | Referential Integrity | 100% University Foreign Keys Valid in fact_research | **PASSED** | All research rows map to valid master universities (zero orphan keys) |
| QA-05 | Referential Integrity | 100% University Foreign Keys Valid in fact_student | **PASSED** | All student rows map to valid master universities (zero orphan keys) |
| QA-06 | Referential Integrity | 100% Country Foreign Keys Valid in fact_country_education | **PASSED** | All country education rows map to valid master countries |
| QA-KPI-kpi_gl | KPI Validity | KPI 1: Global Ranking Score Bound Validation | **PASSED** | Min: 0.07, Max: 100.0 (Valid range: [0.0, 100.0]) |
| QA-KPI-kpi_re | KPI Validity | KPI 2: Research Impact Score Bound Validation | **PASSED** | Min: 1.0, Max: 100.0 (Valid range: [0.0, 100.0]) |
| QA-KPI-kpi_ac | KPI Validity | KPI 5: Academic Reputation Score Bound Validation | **PASSED** | Min: 1.3, Max: 100.0 (Valid range: [0.0, 100.0]) |
| QA-KPI-kpi_re | KPI Validity | KPI 6: Research Productivity Index Bound Validation | **PASSED** | Min: 2.34, Max: 99.87 (Valid range: [0.0, 100.0]) |
| QA-KPI-FSR | KPI Validity | Faculty-to-Student Ratio Non-Negative | **PASSED** | Min ratio: 3.8, Max ratio: 232.2 |
| QA-KPI-INTL | KPI Validity | International Student Percentage Bounds | **PASSED** | Min pct: 0.0%, Max pct: 91.0% |
