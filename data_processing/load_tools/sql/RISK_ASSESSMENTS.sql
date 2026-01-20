SELECT
    [fy25_risks].[Agency]
    ,[fy25_risks].[Program_Name]
    ,[fy25_risks].[Fiscal_Year_Last_Conducted] AS [Fiscal_Year]
    ,CASE
        WHEN [Susceptible] IS NULL THEN NULL
        WHEN UPPER([Susceptible]) = 'NO' THEN 'No'
        ELSE 'Yes' END AS [Susceptible]
	,CASE WHEN [risks_methodology_changed].[Program_Name] IS NULL THEN 0 ELSE 1 END AS [MethodologyChanged]
FROM [fy25_risks]
LEFT JOIN (
    SELECT * FROM [risks_methodology_changed]
) [risks_methodology_changed] ON
    [fy25_risks].[Agency] = [risks_methodology_changed].[Agency] AND
    UPPER([fy25_risks].[Program_Name]) = UPPER([risks_methodology_changed].[Program_Name]) AND
	[fy25_risks].[Fiscal_Year] = [risks_methodology_changed].[Fiscal_Year]
WHERE [fy25_risks].[Agency] = ? AND [fy25_risks].[Fiscal_Year] = ?