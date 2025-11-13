WITH [key_map]([Key],[Name]) AS (
	SELECT * FROM (VALUES
		('cyp30_1', 'IP_Causes'),
		('cyp21_cop7','Overpayments_Due_To_Data_DNE'),
		('cyp21_cop8','Overpayments_Due_To_Inability'),
		('cyp21_cop9','Overpayments_Due_To_Failure'),
		('cyp20_1','Reduction_Target')
	) AS temp_table
)
SELECT
	[program_data_raw].[Agency],
    [program_data_raw].[Program Name] AS [Program_Name],
	[program_data_raw].[key],
	[key_map].[Name],
	[program_data_raw].[title],
	[program_data_raw].[value],
	[program_data_raw].[Fiscal_Year]
FROM [program_data_raw]
JOIN [key_map] ON [program_data_raw].[Key] = [key_map].[Key]
WHERE [program_data_raw].[Program Name] = ? AND
	[program_data_raw].[Fiscal_Year] <= ? AND
	[program_data_raw].[Fiscal_Year] >= ?