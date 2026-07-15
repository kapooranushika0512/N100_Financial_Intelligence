# Nifty 100 Financial Intelligence Dashboard

## Overview

The Nifty 100 Financial Intelligence Dashboard is a Streamlit-based analytics platform for exploring financial performance, valuation, sector comparisons, and peer analysis of Nifty 100 companies. The application provides interactive dashboards and financial insights using data stored in SQLite.

---

## Features

- 🏠 Home Dashboard
- 🏢 Company Profile
- 🔎 Stock Screener
- 👥 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports
- 📊 Valuation Analysis

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- SQLite

---

## Project Structure

```
src/
├── analytics/
├── dashboard/
│   ├── app.py
│   ├── views/
│   └── utils/
├── screener/
└── validation/

output/
├── valuation_summary.xlsx
└── valuation_flags.csv
```

---

## Running the Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

## Dashboard Screens

### Home
Provides an overview of the dashboard and navigation.

### Company Profile
Displays company information, financial ratios, and valuation metrics.

### Stock Screener
Allows filtering companies using financial parameters and exporting results as CSV.

### Peer Comparison
Compares companies within the same sector across financial metrics.

### Trend Analysis
Visualizes historical trends for selected financial metrics.

### Sector Analysis
Compares companies within a selected sector using interactive bubble charts.

### Capital Allocation
Displays capital allocation metrics and valuation indicators.

### Annual Reports
Provides direct access to company annual reports.

---

## Generated Outputs

- `output/valuation_summary.xlsx`
- `output/valuation_flags.csv`

---

## Sprint 4 Retrospective

### UX Decisions

- Implemented a consistent sidebar navigation.
- Used Plotly interactive visualizations.
- Added CSV export functionality for the screener.
- Limited trend comparison to three metrics for improved readability.

### Data Edge Cases

- Handled missing financial ratios using appropriate defaults.
- Removed duplicate company records after merges.
- Resolved year format inconsistencies across datasets.

### Performance

- Cached frequently accessed data.
- Optimized joins and filtering for responsive dashboard performance.
- Company Profile page loads in under three seconds.

---
## Dashboard Screens

### 1. Home Screen

![Home Screen](reports/Screens/Home%20Screen.png)

---

### 2. Company Profile

![Company Profile](reports/Screens/Company%20Profile.png)

---

### 3. Stock Screener

![Stock Screener](reports/Screens/Stock%20Screener.png)

---

### 4. Peer Comparison

![Peer Comparison](reports/Screens/Peer%20Comparison.png)

---

### 5. Trend Analysis

![Trend Analysis](reports/Screens/Trend%20Analysis.png)

---

### 6. Sector Analysis

![Sector Analysis](reports/Screens/Sector%20Analysis.png)

---

### 7. Capital Allocation

![Capital Allocation](reports/Screens/Capital%20Allocation.png)

---

### 8. Annual Reports

![Annual Reports](reports/Screens/Annual%20Reports.png)

---

### 9. Valuation Dashboard

![Valuation Dashboard](reports/Screens/Valuation%20Dashboard.png)
## Author

Anushika Kapoor
Bluestock Data Science Internship