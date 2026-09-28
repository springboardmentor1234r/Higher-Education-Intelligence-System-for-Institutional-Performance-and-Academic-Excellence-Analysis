# EduVision DV – Education Analytics Methodology

## 1. Data preparation

The project begins with ranking and education datasets from QS, THE, WUR and World Bank sources.

Data preparation includes:
- Standardizing names
- Standardizing country identifiers
- Removing duplicate records
- Handling missing values
- Normalizing fields required for analysis
- Preparing Tableau-ready analytical datasets

## 2. Analytical grain

The project uses different analytical grains:

- University-level ranking/performance data
- University-level research/student data
- Country-level education indicators
- Country/year/indicator observations

The dashboards use these sources according to their intended grain.

## 3. Dashboard model

The dashboard suite is divided into four analytical views:

1. University Overview
2. Research Analytics
3. Students Analytics
4. Country Comparison

This separation avoids forcing unrelated country-level and university-level records into a single giant table.

## 4. KPI methodology

KPIs are based on fields that represent the intended concept. For example:
- Research impact uses citation-related measures.
- Student/staff ratio uses an actual ratio.
- International student percentage uses an actual percentage.
- Academic reputation uses the reputation measure.
- Ranking uses the ranking field.

Any derived KPI must have a documented and reproducible formula.

## 5. Tableau analysis

Tableau is used for:
- KPI cards
- Ranking comparisons
- Distributions
- Top-10 analysis
- University comparisons
- Country comparisons
- Interactive filtering
- Dashboard navigation

## 6. Quality assurance

Milestone 4 testing checks:
- KPI field configuration
- Ranking structure
- Dashboard navigation
- Dashboard interactions
- Educational metric coverage
- Visual/layout consistency

A numerical accuracy claim should only be made after the KPI outputs have been independently reconciled against the source records.
