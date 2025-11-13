SELECT
    ROUND(MIN(Payment_Accuracy_Rate), 1) AS [Payment_Accuracy_Rate_Min],
    ROUND(MAX(Payment_Accuracy_Rate), 1) AS [Payment_Accuracy_Rate_Max],
    ROUND(MIN(Improper_Payments_Rate), 1) AS [Improper_Payments_Rate_Min],
    ROUND(MAX(Improper_Payments_Rate), 1) AS [Improper_Payments_Rate_Max],
    ROUND(MIN(Unknown_Payments_Rate), 1) AS [Unknown_Payments_Rate_Min],
    ROUND(MAX(Unknown_Payments_Rate), 1) AS [Unknown_Payments_Rate_Max]
FROM government_wide_data_aggregation
WHERE Fiscal_Year <= ? AND Fiscal_Year >= ?