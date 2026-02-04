SELECT
    a.[Agency],
    a.[Agency_Name],
    a.[Fiscal_Year],
    b.[Confirmed_Fraud]
FROM [all_agencies_years] a
LEFT JOIN [all_agencies_data_aggregation] b
ON a.[Agency] = b.[Agency] AND a.[Fiscal_Year] = b.[Fiscal_Year]
WHERE a.[Fiscal_Year] = ?