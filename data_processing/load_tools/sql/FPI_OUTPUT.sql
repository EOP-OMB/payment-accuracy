SELECT
    [program_to_aln].[Assistance Listing Number] AS [program_id],
	[program_to_aln].[Program Name] AS [improper_payment_program_name],
	[ip_data].[Fiscal_Year] AS [fiscal_year],
	[ip_data].[Outlays] AS [outlays],
	[ip_data].[IP_Amount] AS [improper_payment_amount],
	[insufficient_documentation].[Amount] AS [insufficient_documentation_amount]
FROM
    [program_to_aln]
JOIN
    [all_programs_data_aggregation] [ip_data]
ON
    [ip_data].[Agency] = [program_to_aln].[Agency] AND
	[ip_data].[Program_Name] = [program_to_aln].[Program Name]
LEFT JOIN
    (
	    SELECT
		    SUM([Insufficient_Documentation_to_Determine]) AS [Amount],
			[Agency],
			[Program_Name],
			[Fiscal_Year]
		FROM [ip_root_causes]
		GROUP BY [Agency], [Program_Name], [Fiscal_Year]
	) [insufficient_documentation]
ON
    [ip_data].[Agency] = [insufficient_documentation].[Agency] AND
	[ip_data].[Program_Name] = [insufficient_documentation].[Program_Name] AND
	[ip_data].[Fiscal_Year] = [insufficient_documentation].[Fiscal_Year]
UNION
-- add a null record for the current year for any non-reporting piia programs
SELECT
    [program_to_aln].[Assistance Listing Number] AS [program_id],
	[program_to_aln].[Program Name] AS [improper_payment_program_name],
	? AS [fiscal_year],
	NULL AS [outlays],
	NULL AS [improper_payment_amount],
	NULL AS [insufficient_documentation_amount]
FROM
    [program_to_aln]
LEFT JOIN
    [all_programs_data_aggregation] [ip_data]
ON
    [ip_data].[Agency] = [program_to_aln].[Agency] AND
	[ip_data].[Program_Name] = [program_to_aln].[Program Name]
WHERE [ip_data].[Program_Name] IS NULL
ORDER BY [improper_payment_program_name], [fiscal_year]