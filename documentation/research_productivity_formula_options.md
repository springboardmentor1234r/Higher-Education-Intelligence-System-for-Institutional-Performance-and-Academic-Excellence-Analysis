# EduVision_DV – Research Productivity Index: Methodological Formula Options

## Overview

This document outlines **three scientifically and analytically defensible formula options** for calculating the **Research Productivity Index** KPI. Each option is constructed strictly using legitimate research variables available in the cleaned and approved project datasets (`QS World University Rankings 2025` and `THE World University Rankings 2023`).

--- 

## Available Research Variables in Project Datasets

| Variable Name | Dataset Source | Column Name in `fact_research.csv` | Description | Scale / Unit |
| --- | --- | --- | --- | --- |
| **Citations per Faculty Score** | QS 2025 | `citations_per_faculty_score` | Normalized citation count per academic staff member. | Index Score (0–100) |
| **Citations Score** | THE 2023 | `citation_score` | Field-weighted citation impact of published research. | Index Score (0–100) |
| **Research Score** | THE 2023 | `research_score` | Institutional research volume, income, and reputation survey score. | Index Score (0–100) |
| **International Research Network** | QS 2025 | `international_research_network_score` | Diversity and volume of international co-authored research papers. | Index Score (0–100) |
| **Industry Income Score** | THE 2023 | `industry_income_score` | Commercial research funding and knowledge transfer per academic staff. | Index Score (0–100) |

---

## Proposed Formula Options


### Option 1: Tri-Pillar Balanced Research Index (Impact + Volume + Collaboration)

#### 1. Formula

$$\text{Research Productivity Index}_{\text{Option 1}} = 0.40 \cdot S_{\text{citations}} + 0.35 \cdot S_{\text{research}} + 0.25 \cdot S_{\text{network}}$$

Where:

- $S_{\text{citations}} = \text{mean}(\text{citations\_per\_faculty\_score}_{\text{QS}}, \text{citation\_score}_{\text{THE}})$

- $S_{\text{research}} = \text{research\_score}_{\text{THE}}$

- $S_{\text{network}} = \text{international\_research\_network\_score}_{\text{QS}}$


#### 2. Input Variables

- `citations_per_faculty_score` (QS 2025)
- `citation_score` (THE 2023)
- `research_score` (THE 2023)
- `international_research_network_score` (QS 2025)


#### 3. Normalization Required

None required for raw inputs since all input components are published on a pre-normalized 0–100 scale by QS and THE.


#### 4. Weighting Scheme

- **40% Citation Impact** ($S_{\text{citations}}$): Reflects peer usage and scientific impact.

- **35% Research Reputation & Volume** ($S_{\text{research}}$): Reflects publication output and academic standing.

- **25% Global Collaboration Network** ($S_{\text{network}}$): Reflects international research reach.


#### 5. Component Rationale

- Citation impact ensures high quality over sheer quantity.

- Research volume score captures overall institutional productivity.

- International research network captures collaborative cross-border productivity.


#### 6. Advantages

- Highly balanced: prevents single-metric bias.

- Combines evidence from both QS and THE datasets.

- Intuitive 0–100 bounded scale.


#### 7. Limitations

- Unranked institutions with only single-source coverage will rely on available sub-components.


#### 8. Handling of Missing Values

If a university has values in only one dataset (e.g. QS only), the index computes the weighted mean over available valid components normalized by the sum of available weights. Preserves `NaN` if all research fields are missing.


#### 9. Expected Range

`0.00` to `100.00`


#### 10. Direction of Performance

**Higher values indicate stronger research performance**.


---

### Option 2: Core Output & Citation Impact Index (Pure Academic Focus)

#### 1. Formula

$$\text{Research Productivity Index}_{\text{Option 2}} = 0.50 \cdot S_{\text{citations}} + 0.50 \cdot S_{\text{research}}$$

Where:

- $S_{\text{citations}} = \text{mean}(\text{citations\_per\_faculty\_score}_{\text{QS}}, \text{citation\_score}_{\text{THE}})$

- $S_{\text{research}} = \text{research\_score}_{\text{THE}}$


#### 2. Input Variables

- `citations_per_faculty_score` (QS 2025)
- `citation_score` (THE 2023)
- `research_score` (THE 2023)


#### 3. Normalization Required

None. Pre-normalized 0–100 input scores.


#### 4. Weighting Scheme

- **50% Citation Impact** ($S_{\text{citations}}$)
- **50% Research Volume & Reputation** ($S_{\text{research}}$)


#### 5. Component Rationale

Eliminates network diversity metrics to focus strictly on core academic output volume and peer citation impact.


#### 6. Advantages

- Simple, transparent, and easy to explain to academic stakeholders.
- Focuses strictly on core academic publishing outputs.


#### 7. Limitations

Ignores international research collaboration breadth.


#### 8. Handling of Missing Values

Averages valid components when one dataset source is missing. Preserves `NaN` if no citation or research score is available.


#### 9. Expected Range

`0.00` to `100.00`


#### 10. Direction of Performance

**Higher values indicate stronger research performance**.


---

### Option 3: Quad-Pillar Research & Knowledge Transfer Index (Comprehensive Industry + Academia)

#### 1. Formula

$$\text{Research Productivity Index}_{\text{Option 3}} = 0.35 \cdot S_{\text{citations}} + 0.30 \cdot S_{\text{research}} + 0.20 \cdot S_{\text{network}} + 0.15 \cdot S_{\text{industry}}$$

Where:

- $S_{\text{citations}} = \text{mean}(\text{citations\_per\_faculty\_score}_{\text{QS}}, \text{citation\_score}_{\text{THE}})$

- $S_{\text{research}} = \text{research\_score}_{\text{THE}}$

- $S_{\text{network}} = \text{international\_research\_network\_score}_{\text{QS}}$

- $S_{\text{industry}} = \text{industry\_income\_score}_{\text{THE}}$


#### 2. Input Variables

- `citations_per_faculty_score` (QS 2025)
- `citation_score` (THE 2023)
- `research_score` (THE 2023)
- `international_research_network_score` (QS 2025)
- `industry_income_score` (THE 2023)


#### 3. Normalization Required

None. Pre-normalized 0–100 input scores.


#### 4. Weighting Scheme

- **35% Citation Impact**
- **30% Academic Research Volume**
- **20% International Research Collaboration**
- **15% Industry Knowledge Transfer & Commercial Income**


#### 5. Component Rationale

Includes commercial innovation and industry funding (`industry_income_score`) to evaluate real-world applied research impact alongside pure academic citations.


#### 6. Advantages

- Most comprehensive: captures academic impact, global collaboration, and industrial research commercialization.


#### 7. Limitations

Higher missingness on `industry_income_score` for smaller/humanities-focused institutions.


#### 8. Handling of Missing Values

Computes dynamic weighted average across available valid components. Preserves `NaN` if all components are missing.


#### 9. Expected Range

`0.00` to `100.00`


#### 10. Direction of Performance

**Higher values indicate stronger research performance**.


---

## Summary Comparison Table of Formula Options

| Option | Pillars Included | Input Count | Focus Area | Recommended Use Case |
| --- | --- | --- | --- | --- |
| **Option 1** | Citations + Volume + Network | 4 Fields | Balanced Academic Research | **Recommended Default** (Balanced academic representation) |
| **Option 2** | Citations + Volume | 3 Fields | Pure Citation & Volume | Secondary / Academic Pure Focus |
| **Option 3** | Citations + Volume + Network + Industry Income | 5 Fields | Holistic Academic & Industry Innovation | Applied Research & STEM Analysis |