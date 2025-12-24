SELECT
    [action_data].[Fiscal_Year],
    [action_data].[Agency],
    [action_data].[Program_Name],
    [action_data].[Column_names] AS [Mitigation_Strategy],
    [action_data].[Column_values] AS [Description_Action_Taken],
    CASE
        WHEN [action_data].Column_names LIKE 'app%\_1' ESCAPE '\' AND [date_lookup].[Column_values] NOT LIKE 'The corrective action was not fully completed%' THEN 'Planned'
        WHEN ([action_data].Column_names LIKE 'atp%\_1' ESCAPE '\' OR [action_data].Column_names LIKE 'app%\_1' ESCAPE '\') AND [date_lookup].[Column_values] LIKE 'The corrective action was not fully completed%' THEN 'Not Completed'
        ELSE 'Completed'
    END as [Action_Taken],
    [date_lookup].[Column_values] AS [Completion_Date],
    COALESCE([type_lookup].[Type], [action_data].Column_names) AS [Action_Type]
FROM [principal_table_columns] [action_data]
LEFT JOIN [actions_date_mapping] ON
    [action_data].[Column_names] = [actions_date_mapping].[Action]
LEFT JOIN (
    SELECT
        [Fiscal_Year],
        [Agency],
        [Program_Name],
        [Column_names],
        [Column_values]
    FROM [principal_table_columns]
) [date_lookup] ON
    [action_data].[Fiscal_Year] = [date_lookup].[Fiscal_Year] AND
    [action_data].[Agency] = [date_lookup].[Agency] AND
    [action_data].[Program_Name] = [date_lookup].[Program_Name] AND
    [actions_date_mapping].[Date] = [date_lookup].[Column_names]
LEFT JOIN (
    SELECT
        [Type],
        [Action]
    FROM [actions_date_mapping]
) [type_lookup] ON [action_data].Column_names = [type_lookup].[Action]
WHERE [action_data].Column_values <> ''
    AND ([action_data].Column_names LIKE 'atp%\_1' ESCAPE '\' OR [action_data].Column_names LIKE 'app%\_1' ESCAPE '\')
    -- not showing on old site
    AND [action_data].Column_names <> 'atp17_1'
    AND [action_data].Column_names <> 'app17_1'
    AND [action_data].[Program_Name] = ? AND [action_data].[Fiscal_Year] = ?
ORDER BY [action_data].[Column_names]