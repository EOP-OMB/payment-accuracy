SELECT
    all_agencies_years.Agency,
    a.Program_Name,
    COALESCE(ROUND(a.Outlays, 2),0) AS [Total_Spent_Federal_Funding],
    COALESCE(a.High_Priority_Program,0) AS [High_Priority_Program],
    COALESCE(ROUND(a.IP_Rate, 2),0) AS [IP_Rate],
    CASE
        WHEN b.IP_Rate IS NULL THEN NULL
        ELSE ROUND(a.IP_Rate - b.IP_Rate, 2)
    END AS [Relative_Change]
FROM all_agencies_years
    LEFT JOIN all_programs_data_aggregation a
    ON all_agencies_years.[Agency] = a.[Agency] AND all_agencies_years.[Fiscal_Year] = a.[Fiscal_Year]
    LEFT JOIN (
        SELECT
            Agency,
            Program_Name,
            IP_Rate
        FROM all_programs_data_aggregation
        WHERE Fiscal_Year = ?
    ) b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
WHERE all_agencies_years.Fiscal_Year = ?