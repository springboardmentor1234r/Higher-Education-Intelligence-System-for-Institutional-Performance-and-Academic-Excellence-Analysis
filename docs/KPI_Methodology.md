# KPI Methodology — EduVision_DV

## Purpose

This document records the KPI definitions used in the Milestone 2 output.

The formal project KPI names are retained. Where the mentor repository's
existing Milestone 1 & 2 precedent provides a calculation methodology, that
methodology is used as the implementation precedent.

## KPI definitions

| KPI | Source / calculation | Unit |
|---|---|---|
| Global Ranking Score | QS Overall Score | Score |
| Research Impact Score | Citation Score | Score (0–100) |
| Faculty-to-Student Ratio | `100 / Students per Staff` | Staff per 100 students |
| International Student Percentage | International student percentage from source | % |
| Academic Reputation Score | QS Academic Reputation | Score (0–100) |
| Research Productivity Index | `0.5 × Research Score + 0.5 × Citation Score` | Index |

## Missing-value policy

Missing values are retained as missing (`NaN`). They are not blindly converted
to zero because a missing observation is not equivalent to a measured value of
zero.

## Ratio interpretation

The source field `Students per Staff` is converted using:

`Staff per 100 Students = 100 / Students per Staff`

This makes the KPI direction and unit explicit.

## RPI interpretation

Research Productivity Index is calculated only when both research score and
citation score are available:

`RPI = 0.5 × Research Score + 0.5 × Citation Score`

## Important naming note

The formal project documentation uses the KPI name `Global Ranking Score`,
while the mentor repository precedent contains a slightly different KPI list.
This implementation keeps the formal project KPI names while using the
approved precedent's calculation where applicable.
