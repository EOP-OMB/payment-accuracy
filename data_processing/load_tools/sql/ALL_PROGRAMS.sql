SELECT DISTINCT
    a.Agency,
    b.Agency_Name,
    a.[Program_Name],
    COALESCE([current_year_data].[High_Priority_Program],0) AS [High_Priority_Program],
    COALESCE([current_year_data].[Phase_2_Program],0) AS [Phase_2_Program],
    COALESCE([current_year_data].[Outlays],0) AS [Outlays],
    COALESCE([current_year_data].[Payment_Accuracy_Rate],0) AS [Payment_Accuracy_Rate],
    c.[Description]
FROM [all_programs_data_aggregation] a
    LEFT JOIN ip_agency_pocs b
        ON a.[Agency] = b.[Agency_Acronym]
    LEFT JOIN (
        SELECT DISTINCT
            [Agency],
            [Program Name],
            [Please provide a brief 1-2 sentence high level description of yo] as [Description]
        FROM survey_root_cause
        WHERE [Quarter Year] = ?
            AND RootCauseNumber = 'Please choose Root Cause 1.'
    ) c
    -- [Agency] in survey_root_cause is inconsistent, so it cannot be used in the join
    -- this will work until / unless a high priority program name is duplicated
    ON a.[Program_Name] = c.[Program Name]
    LEFT JOIN (
        SELECT
            [Agency],
            [Program_Name],
            [High_Priority_Program],
            [Phase_2_Program],
            [Outlays],
            [Payment_Accuracy_Rate]
        FROM [all_programs_data_aggregation]
        WHERE [Fiscal_Year] = ?
    ) [current_year_data] ON
        a.[Program_Name] = [current_year_data].[Program_Name] AND
        a.[Agency] = [current_year_data].[Agency]
    JOIN [significant_or_high_priority_programs] ON
        a.[Program_Name] = [significant_or_high_priority_programs].[Program_Name] AND
        a.[Agency] = [significant_or_high_priority_programs].[Agency]