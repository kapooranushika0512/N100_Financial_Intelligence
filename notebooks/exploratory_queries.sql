--Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

--Top 10 ROCE Companies
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

--Top 10 ROE Companies
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

--Highest Net Profit Companies
SELECT company_id,
       MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10;

--Highest Sales Records
SELECT company_id,
       year,
       sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

--Largest Companies by Assets
SELECT company_id,
       total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

--Companies by Sector
SELECT broad_sector,
       COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

--Largest Market Cap Companies
SELECT company_id,
       market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

--Highest Stock Prices
SELECT company_id,
       close_price
FROM stock_prices
ORDER BY close_price DESC
LIMIT 10;

--Best Average Net Profit Margin
SELECT company_id,
       AVG(net_profit_margin_pct) AS avg_margin
FROM financial_ratios
GROUP BY company_id
ORDER BY avg_margin DESC
LIMIT 10;