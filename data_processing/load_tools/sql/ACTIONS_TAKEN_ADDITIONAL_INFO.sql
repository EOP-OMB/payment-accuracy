SELECT
    [value] AS [Answer],
    CASE LOWER([Key])
        WHEN 'rnp3' THEN 'Sufficiency'
        WHEN 'rnp4' THEN 'Accountability'
        WHEN 'rap5' THEN 'Needs1'
        WHEN 'rap6' THEN 'Needs2'
        WHEN 'atpapp30_1' THEN 'Description'
    END AS [ViewKey]
FROM [congressional_reports_program]
WHERE LOWER([Key]) IN (
    'rnp3',
    'rnp4',
    'rap5',
    'rap6',
    'atpapp30_1'
) AND [Program Name] = ? AND [agency] = ? AND [Fiscal_Year] = ?