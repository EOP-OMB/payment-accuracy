SELECT
    [Agency],
    [Fiscal_Year],
    [key],
    SUM([value]) AS [value]
FROM [payment_recovery_details]
WHERE [Fiscal_Year] = ? AND [Agency] = ? AND [Program_Name] IS NULL
GROUP BY [Agency], [Fiscal_Year], [key]