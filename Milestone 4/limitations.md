# EduVision Project Limitations & Architectural Decisions

## 1. Entity Resolution & University Matching Policy
- **Strict Matching Boundary**: In accordance with project non-negotiable rules, university matching across QS 2025, THE 2024, and WUR 2023 was constrained to exact normalized token-set matching within the same canonical country.
- **Candidate Merging Avoidance**: Aggressive fuzzy string matching (e.g., matching "University of California, Berkeley" to "University of California System") was explicitly disallowed. False positive joins corrupt multi-year trend analysis; therefore, unconfirmed candidates were kept as separate university entities with distinct `university_id` assignments.

## 2. Missing Value & Null Data Governance
- **No Zero-Filling / No Data Fabrication**: Missing scores in raw sources (e.g., missing employer reputation, unranked tier entries, missing student counts in QS 2025) were preserved strictly as `NaN`/nulls. Zero-filling missing scores would artificially skew average rankings and regional aggregate statistics.
- **KPI Partial Completeness**: Metrics depending on raw student headcounts (such as KPI 4 International Student % and KPI 3 Faculty-to-Student Ratio) are available for THE 2024 and WUR 2023, but null for QS 2025 as QS only publishes proprietary score indices rather than raw student census figures.

## 3. KPI Engineering & Composite Index Decisions
- **KPI 1 (Global Ranking Score)**: Source dataset `overall_score` is prioritized. When `overall_score` is omitted by the publisher for lower-ranked bands, a deterministic rank-decay score was derived (`max(10, 100 - (global_rank - 1) * 0.05)`).
- **KPI 6 (Research Productivity Index)**: Derived composite index combining equal weights of normalized research score (50%) and citation score (50%). In accordance with explicit brief instructions, QS Sustainability Score was excluded from research metrics.

## 4. World Bank EdStats Alignment & Temporal Coverage
- **Temporal Alignment**: QS, THE, and WUR rankings cover 2023-2025. World Bank EdStats metrics cover 1970-2017. For country-level comparisons, the latest available reported indicator value per country is used for baseline education context.
- **Territorial Standardization**: Country names were normalized to ISO-3 standard names (e.g., "China (Mainland)" -> China, "South Korea" -> Korea, Rep.). Special administrative regions (Hong Kong SAR, Macao SAR) and territories were mapped to their respective World Bank ISO entities.
