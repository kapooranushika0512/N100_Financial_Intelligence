# Performance Notes

## Load Testing
- FastAPI tested with 10 concurrent requests.
- Average API response time remained within acceptable limits.
- No request failures observed.

## Dashboard Performance
- Streamlit dashboard loads company profile in approximately 1 second.
- Target requirement (<3 seconds) achieved.

## Database Optimization
- Added composite indexes on:
  - financial_ratios(company_id, year)
  - balancesheet(company_id, year)
  - profitandloss(company_id, year)
  - cashflow(company_id, year)

## End-to-End Validation
- Dashboard successfully communicates with FastAPI backend.
- SQLite database queries execute successfully.
- API endpoints return expected responses.
