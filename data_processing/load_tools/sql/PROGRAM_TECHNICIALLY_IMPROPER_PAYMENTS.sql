SELECT
    a.[Agency],
    a.[Program_Name],
    a.[Fiscal_Year],
    a.[Payment_Type],
    a.[Program_Design_or_Structural_Issue],
    b.Column_values AS [Technical_IP_Causes],
    d.[Multiselect_Text] AS [Technical_IP_Actions_Taken],
    e.[Multiselect_Text] AS [Technical_IP_Actions_Planned],
    f.Column_values AS [Technical_IP_Amount]
FROM (SELECT
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type],
    SUM([Program_Design_or_Structural_Issue]) AS [Program_Design_or_Structural_Issue]
FROM (SELECT DISTINCT * FROM ip_root_causes) subquery
GROUP BY
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type]) a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'cyp6_1' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN principal_table_columns AS f
    ON a.Agency = f.Agency
    AND a.[Program_Name] = f.[Program_Name]
    AND a.Fiscal_Year = f.Fiscal_Year
    AND f.Column_names = 'cyp6'
    AND f.Column_values <> ''
LEFT JOIN (
    SELECT
        Agency,
        Fiscal_Year,
        Program_Name,
        group_concat(COALESCE(Multiselect_Text,''),', ') AS Multiselect_Text
    FROM (
        SELECT * FROM mitigation_strategies
        WHERE Column_names = 'cyp6_atp1_8'
        ORDER BY Multiselect_Text
    ) subquery1
    GROUP BY Agency, Fiscal_Year, Program_Name
) AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Multiselect_Text <> ''
LEFT JOIN (
    SELECT
        Agency,
        Fiscal_Year,
        Program_Name,
        group_concat(COALESCE(Multiselect_Text,''),', ') AS Multiselect_Text
    FROM (
        SELECT * FROM mitigation_strategies
        WHERE Column_names = 'cyp6_app1_8'
        ORDER BY Multiselect_Text
    ) subquery2
    GROUP BY Agency, Fiscal_Year, Program_Name
) AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Multiselect_Text <> ''
WHERE a.[Program_Name] = ?
    AND a.[Payment_Type] = 'Technically Improper'
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?