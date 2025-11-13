SELECT DISTINCT
    a.Fiscal_Year,
    a.[Program_Name],
    c.[Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis],
    c.[Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data],
    c.[Failure_to_Access_Data],
    c.[Address_Location],
    c.[Contractor_or_Provider_Status],
    c.[Financial],
    d.Column_values AS [Overpayments_Outside_Control_Amount],
    e.Column_values AS [Overpayments_Outside_Control_Why]
FROM principal_table_columns AS a
LEFT JOIN (
    SELECT * FROM principal_table_columns
    WHERE Column_names = 'cyp2_1' AND Column_values <> ''
) AS b
    ON a.Agency = b.Agency
    AND a.Program_Name = b.Program_Name
    AND a.Fiscal_Year = b.Fiscal_Year
LEFT JOIN (
    SELECT
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
    FROM ip_root_causes
    GROUP BY
        [Agency],
        [Program_Name],
        [Fiscal_Year],
        [Payment_Type]
) AS c
    ON a.Agency = c.Agency
    AND a.[Program_Name] = c.[Program_Name]
    AND a.Fiscal_Year = c.Fiscal_Year
    AND c.[Payment_Type] = 'Overpayments outside agency control'
LEFT JOIN principal_table_columns AS d
    ON a.Agency = d.Agency
    AND a.[Program_Name] = d.[Program_Name]
    AND a.Fiscal_Year = d.Fiscal_Year
    AND d.Column_names = 'cyp3'
    AND d.Column_values <> ''
LEFT JOIN principal_table_columns AS e
    ON a.Agency = e.Agency
    AND a.[Program_Name] = e.[Program_Name]
    AND a.Fiscal_Year = e.Fiscal_Year
    AND e.Column_names = 'cyp4_1'
    AND e.Column_values <> ''
WHERE a.[Program_Name] = ?
    AND a.[Fiscal_Year] <= ? AND a.[Fiscal_Year] >= ?