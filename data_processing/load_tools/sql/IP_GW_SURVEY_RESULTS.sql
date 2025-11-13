SELECT
    [agency] AS [Agency],
    [Fiscal_Year],
    [Key],
    [Title] AS [Question],
    [value] AS [Answer],
    CASE [Key]
        WHEN 'com1' THEN 0
    END AS [SortOrder]
FROM [congressional_reports]
WHERE [Key] IN (
    'com1'
) AND [Fiscal_Year] = ?