SELECT
    [Payment_Accuracy_Rate],
    [Improper_Payments_Rate],
    [Unknown_Payments_Rate],
    [Fiscal_Year]
FROM government_wide_data_aggregation
WHERE [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
ORDER BY [Fiscal_Year]