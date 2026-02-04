SELECT
    Agency,
    Agency_Name,
    High_Priority_Programs AS High_Priority_Programs,
    ROUND(Improper_Payments_Rate, 1) AS Improper_Payments_Rate
FROM all_agencies_data_aggregation
WHERE Fiscal_Year = ?
ORDER BY Improper_Payments_Rate DESC
LIMIT 3