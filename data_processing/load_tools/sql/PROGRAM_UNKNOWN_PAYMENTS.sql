SELECT
    a.[Agency],
    a.[Program_Name],
    a.[Fiscal_Year],
    a.[Payment_Type],
    a.[Insufficient_Documentation_to_Determine],
    b.Column_values AS [Unknown_Why],
    d.Column_values AS [Unknown_Documentation_Why],
    e.[Multiselect_Text] AS [Unknown_Mitigations_Taken],
    f.[Multiselect_Text] AS [Unknown_Mitigations_Planned],
    g.Column_values AS [No_Estimates_Why],
    h.Column_values AS [Non_Monetary_Loss_Amount]
FROM (SELECT
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type],
    SUM([Insufficient_Documentation_to_Determine]) AS [Insufficient_Documentation_to_Determine]
FROM (SELECT DISTINCT * FROM ip_root_causes) subquery
GROUP BY
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type]) a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'cyp8' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN principal_table_columns AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Column_names = 'cyp7_ucp4_1'
    AND d.Column_values <> ''
LEFT JOIN principal_table_columns AS g
    ON a.Agency = g.Agency
    AND a.[Program_Name] = g.[Program_Name]
    AND a.Fiscal_Year = g.Fiscal_Year
    AND g.Column_names = 'rac3'
    AND g.Column_values <> ''
LEFT JOIN principal_table_columns AS h
    ON a.Agency = h.Agency
    AND a.[Program_Name] = h.[Program_Name]
    AND a.Fiscal_Year = h.Fiscal_Year
    AND h.Column_names = 'cyp26'
    AND h.Column_values <> ''
LEFT JOIN (
    SELECT
        Agency,
        Fiscal_Year,
        Program_Name,
        group_concat(COALESCE(Multiselect_Text,''),', ') AS Multiselect_Text
    FROM (
        SELECT * FROM mitigation_strategies
        WHERE Column_names = 'cyp7_atp1_8'
        ORDER BY Multiselect_Text
    ) subquery1
    GROUP BY Agency, Fiscal_Year, Program_Name
) AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Multiselect_Text <> ''
LEFT JOIN (
    SELECT
        Agency,
        Fiscal_Year,
        Program_Name,
        group_concat(COALESCE(Multiselect_Text,''),', ') AS Multiselect_Text
    FROM (
        SELECT * FROM mitigation_strategies
        WHERE Column_names = 'cyp7_app1_8'
        ORDER BY Multiselect_Text
    ) subquery2
    GROUP BY Agency, Fiscal_Year, Program_Name
) AS f
    ON a.Agency = f.Agency
    AND a.[Program_Name] = f.[Program_Name]
    AND a.Fiscal_Year = f.Fiscal_Year
    AND e.Multiselect_Text <> ''
WHERE a.[Program_Name] = ?
    AND a.[Payment_Type] = 'Unknown'
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?