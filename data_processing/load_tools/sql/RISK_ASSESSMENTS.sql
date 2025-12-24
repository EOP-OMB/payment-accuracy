SELECT
    [programs].[Agency],
    [programs].[Program_Name],
    [risks].[Fiscal_Year],
    [risks].[Susceptible],
    CASE WHEN [risks_methodology_changed].[Program_Name] IS NULL THEN 0 ELSE 1 END AS [MethodologyChanged]
FROM (
    SELECT DISTINCT [Agency], [Program_Name] FROM [all_programs_data_aggregation]
    UNION
    SELECT DISTINCT [Agency], [Program_Name] FROM [significant_or_high_priority_programs]
    UNION
    SELECT DISTINCT [Agency], [Program_Name] FROM [program_compliance]
    UNION
    SELECT DISTINCT [Agency], [Program_Name] FROM [principal_table_columns]
    UNION
    SELECT DISTINCT [Agency], [Program Name] FROM [program_data_raw]
    UNION
    SELECT DISTINCT [agency], [Program Name] FROM [active_programs] WHERE [Fiscal_Year] = ?
) [programs]
LEFT JOIN (
    SELECT
        a.[Agency],
        a.[Fiscal_Year],
        a.[Program_Name],
        CASE WHEN
            (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'NO' OR upper([raa7_2]) = 'NO') THEN 'No'
            ELSE 'Yes' END AS [Susceptible]
    FROM [risks] a
    JOIN (
        SELECT
            [Agency],
            MAX([Fiscal_Year]) AS [LastRiskAssessment],
            [Program_Name]
        FROM [risks]
        WHERE (upper([raa6_2]) = 'YES' OR [Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_] IS NOT NULL)
            AND (
                (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'NO' OR upper([raa7_2]) = 'NO') OR
                (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'YES' OR upper([raa7_2]) = 'YES')
            )
        GROUP BY [Agency], [Program_Name]
    ) b ON a.[Agency] = b.[Agency] AND UPPER(a.[Program_Name]) = UPPER(b.[Program_Name]) AND a.[Fiscal_Year] = b.[LastRiskAssessment]
    ORDER BY a.[Program_Name]
) [risks] ON
    [programs].[Agency] = [risks].[Agency] AND
    [programs].[Program_Name] = [risks].[Program_Name]
LEFT JOIN (
    SELECT * FROM [risks_methodology_changed] WHERE [Fiscal_Year] = ?
) [risks_methodology_changed] ON
    [risks].[Agency] = [risks_methodology_changed].[Agency] AND
    [risks].[Program_Name] = [risks_methodology_changed].[Program_Name]
WHERE [programs].[Agency] = ? AND ([risks].[Fiscal_Year] <= ? OR [risks].[Fiscal_Year] IS NULL)