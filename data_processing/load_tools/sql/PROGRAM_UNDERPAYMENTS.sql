SELECT
    a.[Agency],
    a.[Program_Name],
    a.[Fiscal_Year],
    a.[Payment_Type],
    a.[Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis],
    a.[Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data],
    a.[Failure_to_Access_Data],
    a.[Address_Location],
    a.[Contractor_or_Provider_Status],
    a.[Financial],
    d.[Multiselect_Text] AS [Underpayment_Mitigations_Taken],
    e.[Multiselect_Text] AS [Underpayment_Mitigations_Planned],
    f.Column_values AS [Underpayments_Amount]
FROM (SELECT
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type],
    SUM([Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis]) AS [Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis],
    SUM([Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data]) AS [Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data],
    SUM([Failure_to_Access_Data]) AS [Failure_to_Access_Data],
    SUM([Address_Location]) AS [Address_Location],
    SUM([Contractor_or_Provider_Status]) AS [Contractor_or_Provider_Status],
    SUM([Financial]) AS [Financial]
FROM (SELECT DISTINCT * FROM ip_root_causes) subquery
GROUP BY
    [Agency],
    [Program_Name],
    [Fiscal_Year],
    [Payment_Type]) a
LEFT JOIN principal_table_columns AS f
    ON a.Agency = f.Agency
    AND a.[Program_Name] = f.[Program_Name]
    AND a.Fiscal_Year = f.Fiscal_Year
    AND f.Column_names = 'cyp5'
    AND f.Column_values <> ''
LEFT JOIN (
    SELECT
        Agency,
        Fiscal_Year,
        Program_Name,
        group_concat(COALESCE(Multiselect_Text,''),', ') AS Multiselect_Text
    FROM (
        SELECT * FROM mitigation_strategies
        WHERE Column_names = 'cyp5_atp1_8'
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
        WHERE Column_names = 'cyp5_app1_8'
        ORDER BY Multiselect_Text
    ) subquery2
    GROUP BY Agency, Fiscal_Year, Program_Name
) AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Multiselect_Text <> ''
WHERE a.[Program_Name] = ?
    AND a.[Payment_Type] = 'Underpayments'
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?