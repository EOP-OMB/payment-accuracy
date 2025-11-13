WITH [key_map]([Key],[Name]) AS (
	SELECT * FROM (VALUES
		('cyp7_ucp1', 'Unknown_Due_To_Vendors_Amount'),
		('cyp7_ucp2','Unknown_Due_To_Eligibility_Amount'),
		('cyp7_ucp3','Unknown_Due_To_States_Amount'),
        ('cyp7_ucp4', 'Unknown_Due_To_Scenario_Not_Specified_Amount'),
		('cyp7_ucp1_1','Unknown_Due_To_Vendors_Description'),
		('cyp7_ucp2_1','Unknown_Due_To_Eligibility_Description'),
		('cyp7_ucp3_1','Unknown_Due_To_States_Description'),
		('cyp7_ucp4_1','Unknown_Due_To_Scenario_Not_Specified_Description')
	) AS temp_table
)
SELECT DISTINCT
    Fiscal_Year,
    Column_names,
    Column_values,
    [key_map].[Name]
FROM principal_table_columns
JOIN key_map ON principal_table_columns.Column_names = key_map.[Key]
WHERE Program_Name = ? AND Fiscal_Year <= ? AND Fiscal_Year >= ? AND
    Column_values IS NOT NULL AND
    Column_values <> '' AND
    Column_values <> '0' AND
    Column_values <> '0.0' AND
    Column_values <> '0.00'