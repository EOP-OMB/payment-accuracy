WITH [key_map]([Key],[Name]) AS (
	SELECT * FROM (VALUES
		('cyp30_1', 'IP_Causes'),
		('cyp21_cop7','Overpayments_Due_To_Data_DNE'),
		('cyp21_cop8','Overpayments_Due_To_Inability'),
		('cyp21_cop9','Overpayments_Due_To_Failure'),
		('cyp20_1','Reduction_Target'),
		('rac3','No_Estimates_Why')
	) AS temp_table
)
SELECT * FROM (
	SELECT
		[program_data_raw].[Agency],
		[program_data_raw].[Program Name] AS [Program_Name],
		[program_data_raw].[key],
		[key_map].[Name],
		[program_data_raw].[title],
		[program_data_raw].[value],
		[program_data_raw].[Fiscal_Year]
	FROM [program_data_raw]
	JOIN [key_map] ON LOWER([program_data_raw].[Key]) = LOWER([key_map].[Key])
	UNION
	SELECT
		[principal_table_columns].[Agency],
		[principal_table_columns].[Program_Name],
		[principal_table_columns].[Column_names] AS [key],
		[key_map].[Name],
		[principal_table_columns].[Question] AS [title],
		[principal_table_columns].[Column_values] as [value],
		[principal_table_columns].[Fiscal_Year]
	FROM [principal_table_columns]
	JOIN [key_map] ON LOWER([principal_table_columns].[Column_names]) = LOWER([key_map].[Key])) union_query
WHERE [union_query].[Program_Name] = ? AND
	[union_query].[Fiscal_Year] = ?