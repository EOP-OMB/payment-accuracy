SELECT
    [Column_names],
    [Column_values],
    b.[theme],
	c.[description],
    CASE
        WHEN a.[Column_names] LIKE 'cyp2_%' THEN 'Overpayments Within Agency Control'
        WHEN a.[Column_names] LIKE 'cyp3_%' THEN 'Overpayments Outside Agency Control'
        ELSE 'Underpayments'
    END AS [Payment_Type],
    a.[Fiscal_Year]
FROM principal_table_columns a
LEFT JOIN eligibility_themes b ON
    substr([Column_names],instr(a.[Column_names],'_') + 1) = concat(b.key,'_1')
LEFT JOIN eligibility_themes_descriptions c ON
    b.[theme] = c.[theme]
WHERE
    a.[Column_names] LIKE 'cyp%\_dit%\_1' ESCAPE '\' AND
    LENGTH(a.[Column_names]) <= 13 AND
    a.[Program_Name] = ? AND
    a.[Column_values] IS NOT NULL AND
	a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?
ORDER BY [Payment_Type], b.[theme]