SELECT DISTINCT
    a.Fiscal_Year,
    a.[Program_Name],
    b.Column_values AS [Program_Additional_Information],
    d.Column_values AS [IP_Accountability_Description]
FROM principal_table_columns AS a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'pro1' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN principal_table_columns AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Column_names = 'rnp4'
    AND d.Column_values <> ''
WHERE a.[Program_Name] = ?
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?