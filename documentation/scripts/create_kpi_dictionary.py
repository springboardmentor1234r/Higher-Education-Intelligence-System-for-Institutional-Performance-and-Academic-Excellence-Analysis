import os
import pandas as pd

doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"
os.makedirs(doc_dir, exist_ok=True)

kpis_data = [
    {
        "kpi_name": "Global Ranking Score",
        "status": "DIRECT / DERIVED",
        "definition": "Quantitative overall institutional benchmark score representing global academic standing and performance.",
        "source_dataset": "QS World University Rankings 2025 / THE World University Rankings 2023",
        "source_fields": "overall_score (QS 2025), overall_score (THE 2023)",
        "formula": "Single Source: overall_score. Composite: mean(qs_overall_score, the_overall_score).",
        "unit": "Index Score (0–100 scale)",
        "normalization_method": "Pre-normalized by ranking bodies (0–100 scale based on weighted indicator components).",
        "missing_value_treatment": "Preserve NaN. Unranked / unassigned institutions remain null; no zero-imputation.",
        "interpretation": "Higher score signifies superior overall global institutional standing and excellence.",
        "limitations": "QS and THE use distinct weighting methodologies (QS weights employer reputation; THE weights research environment)."
    },
    {
        "kpi_name": "Research Impact Score",
        "status": "DIRECT / DERIVED",
        "definition": "Measure of scholarly citation volume and research influence per faculty member.",
        "source_dataset": "QS World University Rankings 2025 / THE World University Rankings 2023",
        "source_fields": "citations_per_faculty_score (QS 2025), citations_score (THE 2023)",
        "formula": "Single Source: citations_per_faculty_score (QS) or citations_score (THE). Composite: mean(qs_citations_score, the_citations_score).",
        "unit": "Index Score (0–100 scale)",
        "normalization_method": "Pre-normalized by ranking bodies using field-adjusted citation impact scaling.",
        "missing_value_treatment": "Preserve NaN; do not impute with zero.",
        "interpretation": "Higher score indicates greater global academic research influence and citation density per staff.",
        "limitations": "Measures normalized citation impact per paper/faculty, not absolute institutional citation volume."
    },
    {
        "kpi_name": "Faculty-to-Student Ratio",
        "status": "DIRECT (THE) / DERIVED",
        "definition": "Number of academic staff members relative to enrolled students, indicating teaching capacity and individualized attention.",
        "source_dataset": "THE World University Rankings 2023 (Actual Ratio) / QS World University Rankings 2025 (Benchmark Score)",
        "source_fields": "students_per_staff (THE 2023), faculty_student_score (QS 2025)",
        "formula": "Actual Ratio (per 100 students) = 100 / students_per_staff. QS Benchmark Score = faculty_student_score.",
        "unit": "Faculty per 100 Students (Actual Ratio) / Index Score (0–100 for QS)",
        "normalization_method": "Mathematical inversion (100 / students_per_staff) for actual ratio; none needed for QS score.",
        "missing_value_treatment": "Preserve NaN; do not impute.",
        "interpretation": "Higher ratio value (Faculty per 100 students) indicates smaller student-to-faculty ratios and higher teaching support capacity.",
        "limitations": "THE provides actual headcount ratio (Students:Staff); QS provides a relative 0–100 benchmark score. Score must not be confused with actual ratio."
    },
    {
        "kpi_name": "International Student Percentage",
        "status": "DIRECT (THE) / DERIVED",
        "definition": "Proportion of total student enrollment comprised of international (foreign national) students.",
        "source_dataset": "THE World University Rankings 2023 (Actual %) / QS World University Rankings 2025 (Score)",
        "source_fields": "pct_international_students (THE 2023), international_students_score (QS 2025)",
        "formula": "Actual Percentage = pct_international_students (THE). QS Benchmark Score = international_students_score.",
        "unit": "Percentage (%) for actual metric / Index Score (0–100) for QS score",
        "normalization_method": "Direct numeric percentage (%) for THE; 0–100 normalized score for QS.",
        "missing_value_treatment": "Preserve NaN; do not fill missing values with 0%.",
        "interpretation": "Higher percentage reflects a highly globalized campus student body and strong international attraction.",
        "limitations": "QS publishes a relative 0–100 benchmark score, NOT the raw percentage of international students."
    },
    {
        "kpi_name": "Academic Reputation Score",
        "status": "DIRECT (QS) / DERIVED (THE)",
        "definition": "Academic peer perception of institutional research quality and academic excellence.",
        "source_dataset": "QS World University Rankings 2025 / THE World University Rankings 2023",
        "source_fields": "academic_reputation_score (QS 2025), teaching_score (THE 2023 proxy)",
        "formula": "Direct Score: academic_reputation_score (QS). Proxy Score: teaching_score (THE).",
        "unit": "Index Score (0–100 scale)",
        "normalization_method": "Standardized 0–100 survey score based on international academic peer survey returns.",
        "missing_value_treatment": "Preserve NaN; do not impute.",
        "interpretation": "Higher score indicates stronger global recognition and peer prestige among academic scholars.",
        "limitations": "Subject to academic survey sample distribution and brand familiarity."
    },
    {
        "kpi_name": "Research Productivity Index",
        "status": "DERIVED",
        "definition": "Synthetic index measuring global research collaboration breadth and institutional research output volume.",
        "source_dataset": "QS World University Rankings 2025 / THE World University Rankings 2023",
        "source_fields": "international_research_network_score (QS 2025), research_score (THE 2023)",
        "formula": "Research Productivity Index = mean(international_research_network_score, research_score).",
        "unit": "Composite Index Score (0–100 scale)",
        "normalization_method": "Arithmetic mean of pre-normalized 0–100 research volume and international collaboration scores.",
        "missing_value_treatment": "Preserve NaN if neither component score is available.",
        "interpretation": "Higher index reflects broader international research networks and stronger institutional research productivity.",
        "limitations": "Raw publication counts per faculty are NOT directly available in raw files; this derived index relies on normalized indicator proxies."
    }
]

df_kpis = pd.DataFrame(kpis_data)

# Export CSV
csv_path = os.path.join(doc_dir, "kpi_dictionary.csv")
df_kpis.to_csv(csv_path, index=False, encoding="utf-8")
print(f"Saved {csv_path}")

# Build Markdown Document
md = []
md.append("# EduVision_DV – Master KPI Specification Dictionary\n")
md.append("## Overview\n")
md.append("This document establishes the official technical specifications for the **six core project KPIs**. All KPI definitions, formulas, and data types are derived strictly from the actual fields available in the finalized data models (`../../data/final/`).\n")

md.append("--- \n")
md.append("## KPI Classification & Availability Summary Table\n")
md.append("Per analytical rigor rules, metrics are distinguished between **DIRECT** (raw field directly represents the target metric), **DERIVED** (engineered from underlying raw metrics), and **NOT DIRECTLY AVAILABLE** (proxy required):\n\n")

md.append("| KPI # | KPI Name | Availability Status | Primary Source Field | Unit | Classification Rule |")
md.append("| --- | --- | --- | --- | --- | --- |")
md.append("| 1 | **Global Ranking Score** | **DIRECT / DERIVED** | `overall_score` (QS / THE) | Index Score (0–100) | Direct score in single-source; derived mean in cross-dataset. |")
md.append("| 2 | **Research Impact Score** | **DIRECT / DERIVED** | `citations_per_faculty_score` / `citations_score` | Index Score (0–100) | Direct citation score in single-source; derived mean in cross-dataset. |")
md.append("| 3 | **Faculty-to-Student Ratio** | **DIRECT (THE) / DERIVED** | `students_per_staff` (THE) / `faculty_student_score` (QS) | Faculty / 100 Students (THE) / Score (QS) | Direct actual ratio in THE (`100 / students_per_staff`); QS provides score proxy. |")
md.append("| 4 | **International Student Percentage** | **DIRECT (THE) / DERIVED** | `pct_international_students` (THE) / `international_students_score` (QS) | Percentage (%) (THE) / Score (QS) | Direct actual percentage in THE (e.g. `42%`); QS provides score proxy. |")
md.append("| 5 | **Academic Reputation Score** | **DIRECT (QS) / DERIVED** | `academic_reputation_score` (QS) / `teaching_score` (THE) | Index Score (0–100) | Direct survey score in QS; proxy teaching environment score in THE. |")
md.append("| 6 | **Research Productivity Index** | **DERIVED** | `international_research_network_score` + `research_score` | Composite Index (0–100) | Derived composite index combining research volume & international network breadth. |")

md.append("\n---\n")
md.append("## Detailed Specifications for Every KPI\n")

for i, k in enumerate(kpis_data, 1):
    md.append(f"### KPI {i}: {k['kpi_name']}\n")
    md.append(f"- **Availability Status**: `{k['status']}`")
    md.append(f"- **Definition**: {k['definition']}")
    md.append(f"- **Source Dataset**: {k['source_dataset']}")
    md.append(f"- **Source Field(s)**: `{k['source_fields']}`")
    md.append(f"- **Formula**: `{k['formula']}`")
    md.append(f"- **Unit**: {k['unit']}")
    md.append(f"- **Normalization Method**: {k['normalization_method']}")
    md.append(f"- **Missing-Value Treatment**: {k['missing_value_treatment']}")
    md.append(f"- **Interpretation**: {k['interpretation']}")
    md.append(f"- **Limitations**: {k['limitations']}\n")

md_path = os.path.join(doc_dir, "kpi_dictionary.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Saved {md_path}")
