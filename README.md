# 📊 Nifty 100 Financial Intelligence Dashboard

## Overview

The **Nifty 100 Financial Intelligence Dashboard** is a comprehensive financial analytics platform built using **Python, Streamlit, FastAPI, SQLite, and Plotly**. It enables users to explore the financial performance of Nifty 100 companies through interactive dashboards, stock screening, peer comparison, valuation analysis, sector insights, and downloadable reports.

The project automates financial data processing through an ETL pipeline, stores cleaned data in a SQLite database, exposes REST APIs using FastAPI, and presents insights through an intuitive Streamlit dashboard.

---

## Features

- 🏠 Industry Overview Dashboard
- 🏢 Company Profile
- 🔎 Stock Screener
- 👥 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports
- 📊 Valuation Analysis
- 🤖 AI Financial Insights
- 📑 PDF Tearsheet Generation
- 📥 CSV Export Functionality
- 🌐 FastAPI REST API
- 📖 Swagger API Documentation

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.11 |
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly, Matplotlib |
| API Documentation | OpenAPI / Swagger |
| Testing | Pytest |
| Code Formatting | Black |
| Linting | Ruff |

---

# Project Structure

```text
N100_Financial_Intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── analyst_guide.pdf
│   ├── openapi.json
│   └── acceptance_checklist.pdf
│
├── output/
│   ├── cluster_labels.csv
│   ├── outlier_report.csv
│   ├── portfolio_stats.csv
│   └── final_deliverables/
│
├── reports/
│   ├── tearsheets/
│   ├── elbow_plot.png
│   ├── correlation_heatmap.png
│   └── pytest_report.html
│
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   ├── reports/
│   ├── screener/
│   └── validation/
│
├── tests/
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd N100_Financial_Intelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the ETL Pipeline

Generate the SQLite database from the raw financial datasets.

```bash
python src/etl/create_database.py
```

---

# Running the Streamlit Dashboard

Launch the dashboard:

```bash
streamlit run src/dashboard/app.py
```

The application will open automatically in your browser.

---

# Running the FastAPI Server

```bash
uvicorn src.api.main:app --reload
```

Server URL:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

OpenAPI Specification:

```
docs/openapi.json
```

---

# Running the Test Suite

Execute all automated tests:

```bash
pytest
```

Generate HTML report:

```bash
pytest --html=reports/pytest_report.html
```

---

# Code Quality

Format the project:

```bash
black src tests
```

Run Ruff:

```bash
ruff check src tests
```

---

# Dashboard Modules

## 🏠 Home

Provides an overview of the dashboard and navigation.

## 🏢 Company Profile

Displays company information, financial statements, financial ratios, valuation metrics, and historical trends.

## 🔎 Stock Screener

Filters companies using customizable financial parameters and exports results to CSV.

## 👥 Peer Comparison

Compares companies within the same industry using financial ratios and interactive charts.

## 📈 Trend Analysis

Visualizes historical financial trends for selected companies.

## 🏭 Sector Analysis

Compares sector-level performance using interactive charts.

## 💰 Capital Allocation

Displays capital allocation metrics, profitability, and valuation indicators.

## 📄 Annual Reports

Provides quick access to company annual reports.

## 📊 Valuation Dashboard

Analyzes valuation metrics including P/E, P/B, EPS, ROE, and ROCE.

---

# Generated Outputs

The project generates the following outputs:

- output/cluster_labels.csv
- output/outlier_report.csv
- output/portfolio_stats.csv
- reports/elbow_plot.png
- reports/correlation_heatmap.png
- reports/pytest_report.html
- docs/openapi.json
- docs/analyst_guide.pdf
- reports/tearsheets/
- output/final_deliverables/

---

# Dashboard Screens

## Home

![Home](reports/Screens/Home%20Screen.png)

---

## Company Profile

![Company Profile](reports/Screens/Company%20Profile.png)

---

## Stock Screener

![Stock Screener](reports/Screens/Stock%20Screener.png)

---

## Peer Comparison

![Peer Comparison](reports/Screens/Peer%20Comparison.png)

---

## Trend Analysis

![Trend Analysis](reports/Screens/Trend%20Analysis.png)

---

## Sector Analysis

![Sector Analysis](reports/Screens/Sector%20Analysis.png)

---

## Capital Allocation

![Capital Allocation](reports/Screens/Capital%20Allocation.png)

---

## Annual Reports

![Annual Reports](reports/Screens/Annual%20Reports.png)

---

## Valuation Dashboard

![Valuation Dashboard](reports/Screens/Valuation%20Dashboard.png)

---

# Project Deliverables

- ✅ Interactive Streamlit Dashboard
- ✅ FastAPI Backend (16 REST API Endpoints)
- ✅ SQLite Database
- ✅ ETL Pipeline
- ✅ Company Financial Analysis
- ✅ Stock Screener
- ✅ Peer Comparison
- ✅ Sector Analysis
- ✅ Valuation Dashboard
- ✅ AI Financial Insights
- ✅ PDF Tearsheet Generation
- ✅ CSV Export
- ✅ Automated Testing
- ✅ OpenAPI Documentation
- ✅ Analyst Guide
- ✅ Final Deliverables Archive

---

# Author

**Anushika Kapoor**  
**Bluestock Data Science Internship**  
B.Tech Computer Science Engineering