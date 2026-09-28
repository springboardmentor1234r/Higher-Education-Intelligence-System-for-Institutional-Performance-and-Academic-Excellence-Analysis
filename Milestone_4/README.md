# Milestone 4 – Testing and Delivery

## Purpose

Milestone 4 covers testing, validation, documentation and final delivery of the EduVision DV dashboard suite.

## Deliverables

### Testing
- `testing/QA_Checklist.md`
- `testing/Dashboard_Testing_Report.md`

### Documentation
- `docs/Dataset_Sources.md`
- `docs/KPI_Definitions.md`
- `docs/Dashboard_Guide.md`
- `docs/Education_Analytics_Methodology.md`

### Tableau Workbook
- `dashboard/EduVision_DV.twbx`

## Testing coverage

The QA work covers:
- KPI field and calculation configuration
- Ranking structure
- Dashboard navigation
- Filter/interaction configuration
- Educational metric coverage
- Visual/layout checks

## Final QA status

**CONDITIONAL PASS**

The workbook is structurally complete and contains all four required dashboards and navigation. A known interaction behavior remains: some dashboard-level visual filter selections can cause KPI cards to become blank. This is documented in the testing report and should be reviewed before final “no major issues” sign-off.

No unsupported numerical KPI-accuracy percentage is claimed because the packaged Hyper extracts were not independently queried in the execution environment.

## Repository structure

```text
Milestone_4/
├── README.md
├── dashboard/
│   └── EduVision_DV.twbx
├── testing/
│   ├── QA_Checklist.md
│   └── Dashboard_Testing_Report.md
└── docs/
    ├── Dataset_Sources.md
    ├── KPI_Definitions.md
    ├── Dashboard_Guide.md
    └── Education_Analytics_Methodology.md
```
