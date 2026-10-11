# Higher Education Analytics Methodology

## 1. Entity Resolution
Higher education datasets from disparate publishers utilize diverse institutional naming styles (e.g. "MIT" vs. "Massachusetts Institute of Technology"). A rule-based alias mapping dictionary was combined with country-scoped validation to match 822 global institutions with 100% confidence.

## 2. Metric Normalization
Because QS and THE utilize differing grading scales, all institutional metrics were normalized to a standardized 0–100 scale using min-max linear scaling, ensuring fair cross-institutional evaluation.
