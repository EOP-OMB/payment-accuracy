SELECT
    COALESCE([Outlays],0)
        - COALESCE([CY_Overpayment_Amount],0)
        - COALESCE([CY_Underpayment_Amount],0)
        - COALESCE([CY_Technically_Improper_Amount],0)
        - COALESCE([CY_Unknown_Payments],0)
        AS [Payment_Accuracy_Amount],
    COALESCE([CY_Overpayment_Amount],0) AS [Overpayment_Amount],
    COALESCE([CY_Underpayment_Amount],0) AS [Underpayment_Amount],
    COALESCE([CY_Technically_Improper_Amount],0) AS [Technically_Improper_Amount],
    COALESCE([CY_Unknown_Payments],0) AS [Unknown_Amount],
    [Fiscal_Year]
FROM all_programs_data_aggregation
WHERE [Program_Name] = ? AND [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
ORDER BY [Fiscal_Year]