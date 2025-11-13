SELECT DISTINCT
    a.Fiscal_Year,
    a.[Program_Name],
    b.Column_values AS [Future_Outlook_Has_Baseline],
    d.Column_values AS [Future_Outlook_Reduction_Vs_Estimated],
    i.Column_values AS [Is_Tolerable_Why],
    e.Column_values AS [Tolerable_Rate_Not_Determined_Reason],
    j.Column_values AS [Is_Not_Tolerable_Why],
    h.Column_values AS [Is_Lowest_IP_And_Unknown_Rate],
    f.Column_values AS [Agency_Needs_Satisfied],
    g.Column_values AS [Resources_Requested_For_IP],
    c.[Outlays_Current_Year+1_Amount],
    c.[IP_Current_Year+1_Amount],
    c.[Unknown_Curent_Year+1_Amount],
    c.[IP_Unknown_Current_Year+1_Rate],
    c.[IP_Unknown_Target_Rate]
FROM principal_table_columns AS a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'cyp15' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN all_programs_data_aggregation c
    ON a.Agency = c.Agency
    AND a.Program_Name = c.Program_Name
    AND a.Fiscal_Year = c.Fiscal_Year
LEFT JOIN principal_table_columns AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Column_names = 'cyp20_2'
    AND d.Column_values <> ''
LEFT JOIN principal_table_columns AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Column_names = 'rtp4_2'
    AND e.Column_values <> ''
LEFT JOIN principal_table_columns AS f
    ON a.Agency = f.Agency
    AND a.[Program_Name] = f.[Program_Name]
    AND a.Fiscal_Year = f.Fiscal_Year
    AND f.Column_names = 'rap5'
    AND f.Column_values <> ''
LEFT JOIN principal_table_columns AS g
    ON a.Agency = g.Agency
    AND a.[Program_Name] = g.[Program_Name]
    AND a.Fiscal_Year = g.Fiscal_Year
    AND g.Column_names = 'rap6'
    AND g.Column_values <> ''
LEFT JOIN principal_table_columns AS h
    ON a.Agency = h.Agency
    AND a.[Program_Name] = h.[Program_Name]
    AND a.Fiscal_Year = h.Fiscal_Year
    AND h.Column_names = 'rtp1'
    AND h.Column_values <> ''
LEFT JOIN principal_table_columns AS i
    ON a.Agency = i.Agency
    AND a.[Program_Name] = i.[Program_Name]
    AND a.Fiscal_Year = i.Fiscal_Year
    AND i.Column_names = 'rtp4_1'
    AND i.Column_values <> ''
LEFT JOIN principal_table_columns AS j
    ON a.Agency = j.Agency
    AND a.[Program_Name] = j.[Program_Name]
    AND a.Fiscal_Year = j.Fiscal_Year
    AND j.Column_names = 'rtp4_3'
    AND j.Column_values <> ''
WHERE a.[Program_Name] = ?
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?