-- <= 2021 did not have a pro1 question
SELECT [Program_Name] FROM [all_programs_data_aggregation]
WHERE
	([Outlays] = 0 OR [Outlays] IS NULL) AND
    [Agency] = ? AND
	[Program_Name] = ? AND
    [Fiscal_Year] = ?