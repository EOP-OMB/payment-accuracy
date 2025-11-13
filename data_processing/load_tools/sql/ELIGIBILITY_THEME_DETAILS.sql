SELECT
    b.[Program Name],
    a.[theme],
    b.[value] AS [Barriers],
    c.[value] AS [Info]
FROM eligibility_themes a
LEFT JOIN (SELECT * FROM program_data_raw) b ON concat(a.key,'_2') = b.key
LEFT JOIN (SELECT * FROM program_data_raw) c ON concat(a.key,'_3') = c.key
WHERE
    b.[agency] = c.[agency]
    AND b.[Program Name] = c.[Program Name]
    AND b.[Fiscal_Year] = c.[Fiscal_Year]
    AND b.[Agency] = ?
    AND b.[Fiscal_Year] = ?
    AND b.[value] IS NOT NULL
    AND c.[value] IS NOT NULL
ORDER BY b.[Program Name], a.[theme]