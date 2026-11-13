# Retail Sales & Business Performance Analytics

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQL-SQLite-003B57?logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75?logo=plotly&logoColor=white)

**🔗 [Live Dashboard](https://retail-sales-business-analytics.streamlit.app/)**

An end-to-end data analytics project that examines retail sales performance, uncovers profitability issues, and turns the findings into actionable business recommendations using **Python, SQL, and Streamlit**.

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Dashboard Features](#dashboard-features)
- [Business Recommendations](#business-recommendations)
- [Getting Started](#getting-started)
- [Skills Demonstrated](#skills-demonstrated)
- [Author](#author)

---

## Overview

This project analyses the **Sample Superstore** retail dataset (9,994 transactions across multiple product categories, regions, and customer segments) to answer a central business question:

> *Where is the business growing, and where is it losing money?*

The work covers the full analytics workflow: data cleaning, exploratory analysis, SQL-based business querying, and an interactive dashboard that lets stakeholders explore performance by region, category, and time period.

---

## Key Findings

| Metric | Result |
|---|---:|
| Total Revenue | $2,297,201 |
| Total Profit | $286,397 |
| Overall Profit Margin | 12.47% |
| Unique Orders | 5,009 |
| Unique Customers | 793 |

### Insights

1. **Furniture is a low-margin category.** It generated roughly $742K in revenue but earned a profit margin of only **2.49%**, far below Technology and Office Supplies.
2. **The Central region underperforms.** It has the lowest profit margin (about **7.92%**) and warrants further investigation at product and state level.
3. **Heavy discounting erodes profit.** Discount levels of **30% and above** showed negative profitability in the aggregated analysis.
4. **Revenue alone is misleading.** Some of the highest-revenue customers were loss-making, which shows why profitability must be tracked alongside sales.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data analysis and processing |
| Pandas, NumPy | Data cleaning and manipulation |
| Matplotlib | Static data visualisation |
| SQL (SQLite) | Business queries and analysis |
| Plotly | Interactive charts |
| Streamlit | Interactive analytics dashboard |

---

## Dataset

| Attribute | Detail |
|---|---|
| Source | [Sample Superstore Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| Records | 9,994 |
| Columns | 21 |
| Period | 2014 – 2017 |
| Categories | Furniture, Office Supplies, Technology |
| Regions | Central, East, South, West |

---

## Project Structure

```text
Retail Sales & Business Analytics/
├── analysis/
│   ├── analysis.py          # Cleaning, feature engineering, EDA
│   └── run_sql.py           # Builds SQLite DB and runs SQL queries
├── data/
│   └── Sample - Superstore.csv
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── sql/
│   └── analysis.sql         # Business queries
├── visuals/
│   ├── category_sales.png
│   ├── regional_profit.png
│   └── monthly_sales.png
├── superstore.db            # Generated SQLite database
└── README.md
```

---

## Methodology

### 1. Data Cleaning and Preparation
- Inspected dataset structure and data types.
- Checked for missing values and duplicate records.
- Converted order and ship dates to datetime format.
- Engineered metrics such as **profit margin** and **shipping duration**.

### 2. Exploratory Data Analysis
- Compared revenue and profitability across product categories and regions.
- Identified loss-making products.
- Analysed the relationship between discount levels and profitability.
- Examined monthly sales and profit trends.

### 3. SQL Business Analysis
SQLite queries covering:
- Category-wise revenue and profitability
- Regional performance comparison
- Top 10 loss-making products
- Profitability by discount level
- Monthly revenue trends
- Top 10 customers by revenue

---

## Dashboard Features

The Streamlit dashboard provides:

- **KPIs:** revenue, profit, profit margin, orders, and customers
- **Filters:** region, category, and date range
- **Trends:** separate monthly revenue and profit charts
- **Performance views:** category, regional, and sub-category profitability
- **Risk analysis:** discount impact and loss-making product identification
- **Automated business insights** that update with the selected filters

<!-- Tip: add a screenshot here, e.g. ![Dashboard](visuals/dashboard.png) -->

---

## Business Recommendations

| Area | Recommendation |
|---|---|
| Furniture | Review pricing and discount strategy to lift margins. |
| Central region | Investigate the products and states driving low margins. |
| Discounting | Introduce approval controls for high-discount transactions. |
| Products and customers | Monitor loss-making items and accounts on an ongoing basis. |
| Performance tracking | Evaluate the business on both revenue **and** profit. |

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd "Retail Sales & Business Analytics"

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install pandas numpy matplotlib plotly streamlit
```

### Add the dataset
Download the [Sample Superstore CSV](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place it in the `data/` folder as `Sample - Superstore.csv`.

### Run the project

```bash
# Python analysis
python analysis/analysis.py

# SQL analysis (creates superstore.db and runs queries)
python analysis/run_sql.py

# Launch the dashboard
streamlit run dashboard/app.py
```

The dashboard opens at `http://localhost:8501`.

---

## Skills Demonstrated

- Data cleaning and feature engineering with Pandas and NumPy
- Exploratory data analysis and visual storytelling
- SQL querying for business analysis
- Interactive dashboard development with Streamlit and Plotly
- Translating analytical findings into business recommendations


