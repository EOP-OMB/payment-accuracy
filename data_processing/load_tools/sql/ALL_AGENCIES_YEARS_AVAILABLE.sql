SELECT
    [Fiscal_Year]
FROM [all_agencies_years]
WHERE [Agency] = ? AND [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
ORDER BY [Fiscal_Year] DESC