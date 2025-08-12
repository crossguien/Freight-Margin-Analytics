-- Load the processed CSV into DuckDB
-- To run programmatically, see scripts/run_sql_examples.py

-- Top 15 shippers by total margin
SELECT shipper_id,
       COUNT(*) AS loads,
       SUM(gross_revenue) AS revenue,
       SUM(gross_margin)  AS margin,
       AVG(margin_pct)    AS avg_margin_pct,
       AVG(on_time)       AS on_time_rate
FROM loads
GROUP BY 1
ORDER BY margin DESC
LIMIT 15;

-- Lane profitability (origin_state -> dest_state)
SELECT lane,
       COUNT(*) AS loads,
       SUM(gross_margin) AS margin,
       AVG(margin_pct)   AS avg_margin_pct,
       AVG(on_time)      AS on_time_rate
FROM loads
GROUP BY 1
ORDER BY margin DESC
LIMIT 20;

-- Late-delivery hotspots (by lane)
SELECT lane,
       COUNT(*) AS loads,
       AVG(on_time) AS on_time_rate
FROM loads
GROUP BY 1
HAVING AVG(on_time) < 0.9
ORDER BY on_time_rate ASC
LIMIT 20;

-- What looks like high revenue but low margin?
SELECT load_id, shipper_id, lane, gross_revenue, gross_margin, margin_pct, on_time
FROM loads
WHERE gross_revenue > (SELECT AVG(gross_revenue) FROM loads)
  AND margin_pct < (SELECT AVG(margin_pct) FROM loads)
ORDER BY margin_pct ASC
LIMIT 25;
