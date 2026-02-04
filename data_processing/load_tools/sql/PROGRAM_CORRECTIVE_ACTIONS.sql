SELECT DISTINCT
    a.Fiscal_Year,
    a.[Program_Name],
    b.Column_values AS [Corrective_Actions_Proportion],
    d.Column_values AS [Corrective_Actions_Adequacy],
    e.Column_values AS [Corrective_Actions_Association],
    f.Column_values AS [Corrective_Actions_Implementation],
    g.Column_values AS [Corrective_Actions_Appropriateness],
    h.Column_values AS [Corrective_Actions_Adequacy_Association_Implementation]
FROM principal_table_columns AS a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'rnp3' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN principal_table_columns AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Column_names = 'act17_2'
    AND d.Column_values <> ''
LEFT JOIN principal_table_columns AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Column_names = 'act17_1'
    AND e.Column_values <> ''
LEFT JOIN principal_table_columns AS f
    ON a.Agency = f.Agency
    AND a.[Program_Name] = f.[Program_Name]
    AND a.Fiscal_Year = f.Fiscal_Year
    AND f.Column_names = 'act17_3'
    AND f.Column_values <> ''
LEFT JOIN principal_table_columns AS g
    ON a.Agency = g.Agency
    AND a.[Program_Name] = g.[Program_Name]
    AND a.Fiscal_Year = g.Fiscal_Year
    AND g.Column_names = 'atpapp30_1'
    AND g.Column_values <> ''
LEFT JOIN principal_table_columns AS h
    ON a.Agency = h.Agency
    AND a.[Program_Name] = h.[Program_Name]
    AND a.Fiscal_Year = h.Fiscal_Year
    AND h.Column_names = 'act17_4'
    AND h.Column_values <> ''
WHERE a.[Program_Name] = ?
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?