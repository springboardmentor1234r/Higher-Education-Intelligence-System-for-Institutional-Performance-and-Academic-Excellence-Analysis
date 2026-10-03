import os

doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"
os.makedirs(doc_dir, exist_ok=True)

md = []
md.append("# EduVision_DV – Research Productivity Index: Methodological Formula Options\n")
md.append("## Overview\n")
md.append("This document outlines **three scientifically and analytically defensible formula options** for calculating the **Research Productivity Index** KPI. Each option is constructed strictly using legitimate research variables available in the cleaned and approved project datasets (`QS World University Rankings 2025` and `THE World University Rankings 2023`).\n")

md.append("--- \n")
md.append("## Available Research Variables in Project Datasets\n")
md.append("| Variable Name | Dataset Source | Column Name in `fact_research.csv` | Description | Scale / Unit |")
md.append("| --- | --- | --- | --- | --- |")
md.append("| **Citations per Faculty Score** | QS 2025 | `citations_per_faculty_score` | Normalized citation count per academic staff member. | Index Score (0–100) |")
md.append("| **Citations Score** | THE 2023 | `citation_score` | Field-weighted citation impact of published research. | Index Score (0–100) |")
md.append("| **Research Score** | THE 2023 | `research_score` | Institutional research volume, income, and reputation survey score. | Index Score (0–100) |")
md.append("| **International Research Network** | QS 2025 | `international_research_network_score` | Diversity and volume of international co-authored research papers. | Index Score (0–100) |")
md.append("| **Industry Income Score** | THE 2023 | `industry_income_score` | Commercial research funding and knowledge transfer per academic staff. | Index Score (0–100) |")

md.append("\n---\n")
md.append("## Proposed Formula Options\n\n")

# Option 1
md.append("### Option 1: Tri-Pillar Balanced Research Index (Impact + Volume + Collaboration)\n")
md.append("#### 1. Formula\n")
md.append("$$\\text{Research Productivity Index}_{\\text{Option 1}} = 0.40 \\cdot S_{\\text{citations}} + 0.35 \\cdot S_{\\text{research}} + 0.25 \\cdot S_{\\text{network}}$$\n")
md.append("Where:\n")
md.append("- $S_{\\text{citations}} = \\text{mean}(\\text{citations\\_per\\_faculty\\_score}_{\\text{QS}}, \\text{citation\\_score}_{\\text{THE}})$\n")
md.append("- $S_{\\text{research}} = \\text{research\\_score}_{\\text{THE}}$\n")
md.append("- $S_{\\text{network}} = \\text{international\\_research\\_network\\_score}_{\\text{QS}}$\n\n")

md.append("#### 2. Input Variables\n")
md.append("- `citations_per_faculty_score` (QS 2025)\n- `citation_score` (THE 2023)\n- `research_score` (THE 2023)\n- `international_research_network_score` (QS 2025)\n\n")

md.append("#### 3. Normalization Required\n")
md.append("None required for raw inputs since all input components are published on a pre-normalized 0–100 scale by QS and THE.\n\n")

md.append("#### 4. Weighting Scheme\n")
md.append("- **40% Citation Impact** ($S_{\\text{citations}}$): Reflects peer usage and scientific impact.\n")
md.append("- **35% Research Reputation & Volume** ($S_{\\text{research}}$): Reflects publication output and academic standing.\n")
md.append("- **25% Global Collaboration Network** ($S_{\\text{network}}$): Reflects international research reach.\n\n")

md.append("#### 5. Component Rationale\n")
md.append("- Citation impact ensures high quality over sheer quantity.\n")
md.append("- Research volume score captures overall institutional productivity.\n")
md.append("- International research network captures collaborative cross-border productivity.\n\n")

md.append("#### 6. Advantages\n")
md.append("- Highly balanced: prevents single-metric bias.\n")
md.append("- Combines evidence from both QS and THE datasets.\n")
md.append("- Intuitive 0–100 bounded scale.\n\n")

md.append("#### 7. Limitations\n")
md.append("- Unranked institutions with only single-source coverage will rely on available sub-components.\n\n")

md.append("#### 8. Handling of Missing Values\n")
md.append("If a university has values in only one dataset (e.g. QS only), the index computes the weighted mean over available valid components normalized by the sum of available weights. Preserves `NaN` if all research fields are missing.\n\n")

md.append("#### 9. Expected Range\n")
md.append("`0.00` to `100.00`\n\n")

md.append("#### 10. Direction of Performance\n")
md.append("**Higher values indicate stronger research performance**.\n\n")

md.append("---\n")

# Option 2
md.append("### Option 2: Core Output & Citation Impact Index (Pure Academic Focus)\n")
md.append("#### 1. Formula\n")
md.append("$$\\text{Research Productivity Index}_{\\text{Option 2}} = 0.50 \\cdot S_{\\text{citations}} + 0.50 \\cdot S_{\\text{research}}$$\n")
md.append("Where:\n")
md.append("- $S_{\\text{citations}} = \\text{mean}(\\text{citations\\_per\\_faculty\\_score}_{\\text{QS}}, \\text{citation\\_score}_{\\text{THE}})$\n")
md.append("- $S_{\\text{research}} = \\text{research\\_score}_{\\text{THE}}$\n\n")

md.append("#### 2. Input Variables\n")
md.append("- `citations_per_faculty_score` (QS 2025)\n- `citation_score` (THE 2023)\n- `research_score` (THE 2023)\n\n")

md.append("#### 3. Normalization Required\n")
md.append("None. Pre-normalized 0–100 input scores.\n\n")

md.append("#### 4. Weighting Scheme\n")
md.append("- **50% Citation Impact** ($S_{\\text{citations}}$)\n- **50% Research Volume & Reputation** ($S_{\\text{research}}$)\n\n")

md.append("#### 5. Component Rationale\n")
md.append("Eliminates network diversity metrics to focus strictly on core academic output volume and peer citation impact.\n\n")

md.append("#### 6. Advantages\n")
md.append("- Simple, transparent, and easy to explain to academic stakeholders.\n- Focuses strictly on core academic publishing outputs.\n\n")

md.append("#### 7. Limitations\n")
md.append("Ignores international research collaboration breadth.\n\n")

md.append("#### 8. Handling of Missing Values\n")
md.append("Averages valid components when one dataset source is missing. Preserves `NaN` if no citation or research score is available.\n\n")

md.append("#### 9. Expected Range\n")
md.append("`0.00` to `100.00`\n\n")

md.append("#### 10. Direction of Performance\n")
md.append("**Higher values indicate stronger research performance**.\n\n")

md.append("---\n")

# Option 3
md.append("### Option 3: Quad-Pillar Research & Knowledge Transfer Index (Comprehensive Industry + Academia)\n")
md.append("#### 1. Formula\n")
md.append("$$\\text{Research Productivity Index}_{\\text{Option 3}} = 0.35 \\cdot S_{\\text{citations}} + 0.30 \\cdot S_{\\text{research}} + 0.20 \\cdot S_{\\text{network}} + 0.15 \\cdot S_{\\text{industry}}$$\n")
md.append("Where:\n")
md.append("- $S_{\\text{citations}} = \\text{mean}(\\text{citations\\_per\\_faculty\\_score}_{\\text{QS}}, \\text{citation\\_score}_{\\text{THE}})$\n")
md.append("- $S_{\\text{research}} = \\text{research\\_score}_{\\text{THE}}$\n")
md.append("- $S_{\\text{network}} = \\text{international\\_research\\_network\\_score}_{\\text{QS}}$\n")
md.append("- $S_{\\text{industry}} = \\text{industry\\_income\\_score}_{\\text{THE}}$\n\n")

md.append("#### 2. Input Variables\n")
md.append("- `citations_per_faculty_score` (QS 2025)\n- `citation_score` (THE 2023)\n- `research_score` (THE 2023)\n- `international_research_network_score` (QS 2025)\n- `industry_income_score` (THE 2023)\n\n")

md.append("#### 3. Normalization Required\n")
md.append("None. Pre-normalized 0–100 input scores.\n\n")

md.append("#### 4. Weighting Scheme\n")
md.append("- **35% Citation Impact**\n- **30% Academic Research Volume**\n- **20% International Research Collaboration**\n- **15% Industry Knowledge Transfer & Commercial Income**\n\n")

md.append("#### 5. Component Rationale\n")
md.append("Includes commercial innovation and industry funding (`industry_income_score`) to evaluate real-world applied research impact alongside pure academic citations.\n\n")

md.append("#### 6. Advantages\n")
md.append("- Most comprehensive: captures academic impact, global collaboration, and industrial research commercialization.\n\n")

md.append("#### 7. Limitations\n")
md.append("Higher missingness on `industry_income_score` for smaller/humanities-focused institutions.\n\n")

md.append("#### 8. Handling of Missing Values\n")
md.append("Computes dynamic weighted average across available valid components. Preserves `NaN` if all components are missing.\n\n")

md.append("#### 9. Expected Range\n")
md.append("`0.00` to `100.00`\n\n")

md.append("#### 10. Direction of Performance\n")
md.append("**Higher values indicate stronger research performance**.\n\n")

md.append("---\n")
md.append("## Summary Comparison Table of Formula Options\n")
md.append("| Option | Pillars Included | Input Count | Focus Area | Recommended Use Case |")
md.append("| --- | --- | --- | --- | --- |")
md.append("| **Option 1** | Citations + Volume + Network | 4 Fields | Balanced Academic Research | **Recommended Default** (Balanced academic representation) |")
md.append("| **Option 2** | Citations + Volume | 3 Fields | Pure Citation & Volume | Secondary / Academic Pure Focus |")
md.append("| **Option 3** | Citations + Volume + Network + Industry Income | 5 Fields | Holistic Academic & Industry Innovation | Applied Research & STEM Analysis |")

doc_path = os.path.join(doc_dir, "research_productivity_formula_options.md")
with open(doc_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Exported {doc_path}")
