WITH [key_map]([Key],[Name]) AS (
	SELECT * FROM (VALUES
		('exs1', 'Executive_Summary'),
		('arp5', 'Aging_of_Outstanding_OP_Identified_Remaining_Unrecovered'),
		('arp18','Recovery_Additional_Details'),
		('arp17','Overpayment_Conditions'),
		('arp17_1','Overpayment_Conditions_And_Methods'),
        ('ara2', 'Recovery_Audits_Skipped'),
		('ara2_1','Recovery_Methods_Audits'),
		('ara2_2','Recovery_Justifications_Audits'),
		('ara2_3_2','Recovery_Not_Cost_Effective_Programs'),
		('ara2_3','Recovery_Not_Cost_Effective_Justification'),
		('dis1','Disposition_of_Funds'),
		('dpa2','DNP_Reduced'),
		('dpa3','DNP_Frequency_Identify'),
		('dpa4','DNP_Frequency_Correction'),
		('dpa5','DNP_Discussion'),
		('com1','Compliance_Status'),
		('pcp12_1','NonCompliant_Consecutive_Years'),
		('pcp14','Recommendations_To_Reduce_IP'),
		('cap3','PIIA_Official'),
		('cap4','PIIA_Incentives'),
		('cap5','OIG_Recommendations'),
		('agy1','Additional_IP_Information'),
        ('raa8','Risks_Substantial_Changes_Made'),
        ('raa9','Risks_Additional_Information')
	) AS temp_table
)
SELECT
	[agency_data_raw].[agency],
	[agency_data_raw].[Key],
	[key_map].[Name],
	[agency_data_raw].[Title],
	[agency_data_raw].[value],
	[agency_data_raw].[Fiscal_Year]
FROM [agency_data_raw]
JOIN [key_map] ON LOWER([agency_data_raw].[Key]) = LOWER([key_map].[Key])
WHERE [Fiscal_Year] = ? AND [Agency] = ?