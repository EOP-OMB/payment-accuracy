WITH [key_map]([Key],[Name]) AS (
	SELECT * FROM (VALUES
		('cyp2', 'Overpayments_Within_Control_Amount'),
		('cyp2_cop1','Overpayments_Within_Data_Needed_Does_Not_Exist'),
		('cyp2_cop2','Overpayments_Within_Inability_to_Access_Data'),
        ('cyp2_cop3', 'Overpayments_Within_Failure_to_Access_Data'),
		('cyp3','Overpayments_Outside_Control_Amount'),
		('cyp3_cop1','Overpayments_Outside_Data_Needed_Does_Not_Exist'),
		('cyp3_cop2','Overpayments_Outside_Inability_to_Access_Data'),
		('cyp3_cop3','Overpayments_Outside_Failure_to_Access_Data'),
        ('cyp3_cop4','Overpayments_Outside_Data_Needed_Does_Not_Exist_2'),
		('cyp3_cop5','Overpayments_Outside_Inability_to_Access_Data_2'),
		('cyp3_cop6','Overpayments_Outside_Failure_to_Access_Data_2'),
        ('cyp5', 'Underpayments_Amount'),
		('cyp5_cup1','Underpayments_Data_Needed_Does_Not_Exist'),
		('cyp5_cup2','Underpayments_Inability_to_Access_Data'),
        ('cyp5_cup3', 'Underpayments_Failure_to_Access_Data'),
        ('cyp6', 'Technical_IP_Amount')
	) AS temp_table
)
SELECT
    a.[Agency],
    a.[Fiscal_Year],
    a.[Program_Name],
    c.[Name],
    c.[Key] AS [Column_names],
    b.[Column_values]
FROM (
    SELECT DISTINCT [Fiscal_Year], [Agency], [Program_Name] FROM principal_table_columns
    WHERE [Program_Name] = ? AND [Fiscal_Year] <= ? AND [Fiscal_Year] >= ?
) AS a
CROSS JOIN [key_map] c
LEFT JOIN principal_table_columns b
    ON a.[Agency] = b.[Agency]
    AND a.[Program_Name] = b.[Program_Name]
    AND a.[Fiscal_Year] = b.[Fiscal_Year]
    AND LOWER(c.[Key]) = LOWER(b.Column_names)
WHERE b.[Column_values] IS NULL