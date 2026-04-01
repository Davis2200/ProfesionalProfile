# Banking Churn Predictive System

## Executive Summary
As a Data Science candidate from Instituto Politécnico Nacional (IPN), I am building a high-impact portfolio that bridges hands-on operational reliability from Conduent Solutions with predictive analytics. I transformed field-level incident reports and hardware preventive maintenance concepts into risk modeling workflows for customer portfolio stability. This project demonstrates my appetite for data-driven decision-making and my ability to translate domain knowledge into measurable business outcomes.

## The Business Challenge
Customer churn is a leading cost driver for banking operations. Lost customers generate revenue leakage, higher acquisition costs, and impaired lifetime value. This project addresses the challenge with a structured ML solution that detects high-risk accounts early, enabling prioritized retention campaigns and reduced attrition costs.

## Data Engineering
- Data source: customer transaction and account lifecycle data.
- Feature engineering:
  - Recency/frequency/monetary (RFM) behavior embeddings.
  - Balance trend time-series features (7/30/90-day deltas, exponential moving averages).
  - Ownership signals, product holding, and support interaction frequency.
- Data cleaning: missing value handling, outlier capping, and target leakage filters.
- Scaling: `StandardScaler` applied to continuous features to align model gradients and prevent scale-driven weights.
- Pipeline: `sklearn.pipeline.Pipeline` with imputation, scaling, and model to support reproducible scoring and deployment.

## Model Performance
- Primary evaluation metrics:
  - ROC-AUC: **0.85**
  - F1-Score: **0.75**
- The model is tuned for balanced precision and recall in imbalance settings (churn < 25%).
- Why realistic metrics beat perfect accuracy:
  - `Accuracy = 1.00` on churn typically indicates overfitting, class imbalance bias, or data leakage.
  - ROC-AUC and F1 are robust to imbalance and focus on separability and practical classification tradeoffs.
  - Business value is defined by correct identification of churn risk (true positives) and minimizing low-value outreach (false positives).

## Interactive Deployment
[🚀 Launch Live Risk Simulator](https://profesionalprofile-lynq92g5zrq4uyvv4mce3p.streamlit.app/)

## Technical Stack
- Python 3.11
- pandas, numpy, scikit-learn, xgboost
- Plotly for interactive diagnostics
- Streamlit for rapid proof-of-concept deployment
- GitHub Actions for CI/CD and model validation

## Contact
Validate model decisions with business KPIs, then iterate with A/B-based retention experiments. Reach me at `davis2200 (GitHub profile)`.
