# Dashboard Storyboard & Planning Notes — Milestone 2

## Executive Summary & Planning Goals
This document outlines the visual layout, user journey, and wireframe architecture for the 4 core interactive dashboards in **EduVision_DV**.

## Dashboard Storyboard Architecture

### Dashboard 1: University Overview (Executive Level)
- **Target Audience**: University chancellors, policy planners, international education analysts.
- **Top BAN Cards**: Global Ranking Score, Research Impact, Faculty-Student Ratio, Intl Student %, Academic Reputation, Research Productivity.
- **Visuals**:
  - Top 20 Global Universities (Sorted Bar Chart).
  - Regional Performance Distribution (Grouped Bar / Donut Chart).
- **Interactivity**: Country & Ranking Source Filter Selectors.

### Dashboard 2: Research Analytics
- **Target Audience**: Research directors, grant committees, academic deans.
- **Top BAN Cards**: Average Research Impact Score, Composite Research Index.
- **Visuals**:
  - Citation Impact vs Research Score (Scatter Plot with bubble size = productivity index).
  - Multi-Year Research Performance Trend (Line Chart).
- **Interactivity**: University selection filter action carry-forward from Dashboard 1.

### Dashboard 3: Student Analytics
- **Target Audience**: Admissions officers, international student advisors, enrollment managers.
- **Top BAN Cards**: Faculty-Student Ratio Index, International Student Percentage BAN.
- **Visuals**:
  - International Student Ratio by Top Institutions (Bar Chart).
  - Student Headcount vs International Diversity (Scatter Plot).
- **Interactivity**: Cross-filtering by region and income group.

### Dashboard 4: Country Comparison & Public Benchmarking
- **Target Audience**: Government education ministries, World Bank analysts, regional consortia.
- **Visuals**:
  - Global Education Performance & University Density Map (Choropleth Map).
  - Tertiary Enrollment Rate vs Education Spend (% GDP) (Dual Bar/Line Chart).
  - Institutional Count & Avg Score by World Bank Income Group.
- **Interactivity**: Global country selector and income group parameter controls.
