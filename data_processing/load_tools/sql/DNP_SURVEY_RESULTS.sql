SELECT
    [agency] AS [Agency],
    [Fiscal_Year],
    [Key],
    [Title] AS [Question],
    [value] AS [Answer],
    CASE LOWER([Key])
        WHEN 'dpa5' THEN 0
    END AS [SortOrder]
FROM [congressional_reports]
WHERE LOWER([Key]) IN (
    'dpa5'
)
AND [Fiscal_Year] = ?