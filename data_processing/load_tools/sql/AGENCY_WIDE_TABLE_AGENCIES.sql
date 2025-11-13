SELECT
    reported_any_year.Agency,
    reported_any_year.Agency_Name,
    COALESCE(ROUND(cy.Outlays, 2),0) AS [Total_Spent_Federal_Funding],
    COALESCE(compliance.Num_Programs,0) AS [Num_Programs],
    COALESCE(cy.Susceptible_Programs,0) AS [Susceptible_Programs],
    COALESCE(cy.High_Priority_Programs,0) AS [High_Priority_Programs],
    COALESCE(ROUND(cy.Improper_Payments_Rate, 2),0) AS [Improper_Payments_Rate],
    CASE
        WHEN py.Improper_Payments_Rate IS NULL THEN NULL
        ELSE ROUND(cy.Improper_Payments_Rate - py.Improper_Payments_Rate, 2)
    END AS [Relative_Change]
FROM (
    SELECT DISTINCT
        Agency,
        Agency_Name
    FROM all_agencies_years
    WHERE [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
) reported_any_year
    LEFT JOIN (
        SELECT *
        FROM all_agencies_data_aggregation
        WHERE Fiscal_Year = ?
    ) cy
    ON reported_any_year.[Agency] = cy.[Agency]
    LEFT JOIN (
        SELECT
            Agency,
            Improper_Payments_Rate
        FROM all_agencies_data_aggregation
        WHERE Fiscal_Year = ?
    ) py
    ON cy.Agency = py.Agency
    LEFT JOIN (
        SELECT
            [Agency],
            [Fiscal_Year],
            COUNT(*) AS [Num_Programs]
        FROM [program_compliance]
        WHERE Fiscal_Year = ?
        GROUP BY [Agency], [Fiscal_Year]
    ) compliance ON reported_any_year.Agency = compliance.Agency
ORDER BY COALESCE(ROUND(cy.Outlays, 2),0) DESC, reported_any_year.Agency_Name ASC