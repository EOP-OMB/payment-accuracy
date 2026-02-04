SELECT * FROM
(SELECT [Agency], [Program_Name],[Fiscal_Year] FROM [all_programs_data_aggregation]
WHERE
	([Outlays] = 0 OR [Outlays] IS NULL) AND
	[Fiscal_Year] = 2022
INTERSECT
SELECT [Agency], [Program_Name], [Fiscal_Year] FROM [principal_table_columns]
WHERE 
    [Column_names] = 'pro1' AND
	([Column_values] IS NULL OR [Column_values] = '') AND
	[Fiscal_Year] = 2022) AS [2022_Query]
WHERE [Agency] = ? AND [Program_Name] = ? AND [Fiscal_Year] = ?