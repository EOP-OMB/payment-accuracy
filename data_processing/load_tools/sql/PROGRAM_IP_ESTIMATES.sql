SELECT
    [Fiscal_Year],
    [Payment_Accuracy_Rate],
    [IP_Rate],
    [Unknown_Payments_Rate],
    [Start_Date],
    [End_Date],
    [CY_Confidence_Level],
    [CY_Margin_of_Error]
FROM all_programs_data_aggregation
WHERE [Program_Name] = ? AND
    (
        [Payment_Accuracy_Rate] IS NOT NULL OR
        [IP_Rate] IS NOT NULL OR
        [Unknown_Payments_Rate] IS NOT NULL
    )
    AND [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
ORDER BY [Fiscal_Year]