-- this splits the comma-delimited multiselect answer into multiple records
SELECT * FROM (
	WITH RECURSIVE split_values AS (
		-- base case
		SELECT
			[Fiscal_Year],
			[Program Name],
			TRIM(SUBSTR([value], 1, INSTR([value] || ',', ',') - 1)) AS [theme],
			SUBSTR([value], INSTR([value] || ',', ',') + 1) AS [remaining],
			1 AS position
		FROM program_data_raw 
		WHERE
			LOWER([key]) = 'cyp30_dit1_19' AND
			[value] != ''
		UNION ALL
		-- remaining
		SELECT
			[Fiscal_Year],
			[Program Name],
			TRIM(SUBSTR([remaining], 1, INSTR([remaining] || ',', ',') - 1)) AS [theme],
			SUBSTR([remaining], INSTR([remaining] || ',', ',') + 1) AS [remaining],
			position + 1
		FROM split_values 
		WHERE [remaining] != ''
	)
	SELECT
		[Fiscal_Year],
		[Program Name],
		[themes].[theme],
		[description]
	FROM (
		SELECT
			[Fiscal_Year],
			[Program Name],
			CASE
				WHEN [theme] GLOB '[[]dit[0-9]*] *'
				THEN TRIM(SUBSTR([theme], INSTR([theme], '] ') + 2))
				ELSE [theme]
			END AS [theme]
		FROM split_values
	) themes
	LEFT JOIN eligibility_themes_descriptions e ON [themes].[theme] = e.[theme]
	WHERE [themes].[theme] != 'Other (please explain)'
	UNION
	SELECT
		[Fiscal_Year],
		[Program Name],
		'Other' AS [theme],
		program_data_raw.[value] AS [description]
	FROM program_data_raw
	WHERE
		LOWER([key]) = 'cyp30_dit19' AND
		[value] IS NOT NULL
) themes WHERE
[Program Name] = ? AND
[Fiscal_Year] <= ? AND [Fiscal_Year] >= ?