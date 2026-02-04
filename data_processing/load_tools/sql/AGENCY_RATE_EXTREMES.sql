SELECT
    COALESCE([Payment_Accuracy_Rate],0) AS [Payment_Accuracy_Rate],
    COALESCE([Improper_Payments_Rate],0) AS [Improper_Payments_Rate],
    COALESCE([Unknown_Payments_Rate],0) AS [Unknown_Payments_Rate],
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
FROM all_agencies_data_aggregation
WHERE
    [Agency] = ? AND
    [Fiscal_Year] <= ? AND [Fiscal_Year] >= ? AND
    [Payment_Accuracy_Rate] IS NOT NULL
ORDER BY [Fiscal_Year]