# Connecting a BI Tool to EduVision_DV

After running the pipeline, `data/warehouse/` contains the same star schema
in three formats. Pick whichever your BI tool connects to most natively.

```
data/warehouse/
├── eduvision_real.db                  SQLite database (3 tables, indexed)
├── EduVision_Real_BI_Workbook.xlsx    1 workbook, 1 sheet per table
├── dim_university.csv
├── dim_year.csv
└── fact_university_year.csv
```

**Star schema** — one fact table, two dimensions, joined on `university_id` / `year`:

```
dim_university(university_id PK, university_name, country, region)
dim_year(year PK)
fact_university_year(university_id FK, year FK, overall_score_final,
    global_rank, academic_reputation, research_impact_the, publications,
    citations, research_productivity_index, research_impact_score,
    total_enrollment, international_students, faculty_headcount,
    international_student_pct, faculty_student_ratio)
```

---

## Power BI

1. **Home → Get Data → More… → Database → SQLite database**
   (if the SQLite connector isn't listed, install the [SQLite ODBC driver](http://www.ch-werner.de/sqliteodbc/) once, then use **Get Data → ODBC**)
2. Point it at `data/warehouse/eduvision_real.db`, select all 3 tables, **Load**.
3. In **Model view**, confirm/create relationships:
   - `fact_university_year[university_id]` → `dim_university[university_id]` (many-to-one)
   - `fact_university_year[year]` → `dim_year[year]` (many-to-one)
4. Alternative with zero drivers: **Get Data → Excel workbook**, select `EduVision_Real_BI_Workbook.xlsx`, load all 3 sheets, then wire the same two relationships manually.

## Tableau

1. **Connect → To a File → More… → SQLite** (Tableau ships a native SQLite connector — no driver install needed).
2. Open `data/warehouse/eduvision_real.db`.
3. Drag `fact_university_year` onto the canvas, then drag `dim_university` and `dim_year` on top of it — Tableau will prompt you to set the join keys (`university_id`, `year`); confirm.
4. Alternative: **Connect → Text File / Excel**, load the 3 CSVs or the workbook, then build the same two joins in the Data Source tab.

## Looker Studio (Google)

Looker Studio has no native SQLite/local-file connector, so:

1. Import `EduVision_Real_BI_Workbook.xlsx` into **Google Sheets** (File → Import), or upload the 3 CSVs as separate Sheets tabs.
2. In Looker Studio: **Create → Data Source → Google Sheets**, select each tab, add all three as data sources to the same report.
3. **Resource → Manage blended data** (or use a **Blend** on a chart) to join `fact_university_year` to `dim_university` on `university_id` and to `dim_year` on `year`.

## Metabase / Apache Superset (self-hosted, open source)

1. **Admin → Databases → Add database → SQLite**, point it at the absolute path to `eduvision_real.db`.
2. Both tools auto-detect the foreign keys from column names; verify/set them manually in the schema editor if not (`university_id`, `year`).
3. Build questions/charts directly against `fact_university_year`, joining dimensions as needed.

## Excel (PivotTable, no BI tool)

1. Open `EduVision_Real_BI_Workbook.xlsx`.
2. **Insert → PivotTable**, choose **Use this workbook's Data Model**, then in Power Pivot's **Diagram View** draw the same two relationships (`university_id`, `year`).
3. Build pivot tables/charts as usual — this gives you most of the cross-filtering behavior of a real BI tool for free.

---

## Suggested first dashboard (any tool)

| Visual | Fields |
|---|---|
| KPI card | `AVG(overall_score_final)`, `SUM(publications)`, `AVG(international_student_pct)` |
| Bar — Top 10 universities | `university_name` × `overall_score_final`, sorted desc, filtered `global_rank <= 10` |
| Line — trend | `year` (x) × `overall_score_final` (y), one line per selected `university_name` |
| Map / bar by region | `dim_university.region` × `COUNT(university_id)` and `AVG(overall_score_final)` |
| Scatter | `academic_reputation` (x) × `research_impact_the` (y), size = `total_enrollment`, color = `region` |
| Table | all fact columns, filterable by `year` slicer/parameter |

Re-run `python3 scripts/run_pipeline.py` any time the raw sources change — the
warehouse files are fully regenerated, so refreshing your BI tool's connection
(or re-importing the workbook) picks up the new data with no schema changes.
