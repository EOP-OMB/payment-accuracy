SELECT
    [sums].[total_outlays_current_year],
    [sums].[total_outlays_current_year] - [sums].[total_improper_current_year] - [sums].[total_unknown_current_year] AS [total_proper_current_year],
    100 * ([sums].[total_outlays_current_year] - [sums].[total_improper_current_year] - [sums].[total_unknown_current_year]) / CAST([sums].[total_outlays_current_year] AS REAL) AS [proper_rate_current_year],
    [sums].[total_improper_current_year],
    100 * ([sums].[total_improper_current_year]) / CAST([sums].[total_outlays_current_year] AS REAL) AS [improper_rate_current_year],
    [sums].[total_unknown_current_year],
    100 * ([sums].[total_unknown_current_year]) / CAST([sums].[total_outlays_current_year] AS REAL) AS [unknown_rate_current_year],
    [sums].[total_improper_current_year] + [sums].[total_unknown_current_year] AS [total_unknown_and_improper_amount],
    100 * ([sums].[total_improper_current_year] + [sums].[total_unknown_current_year]) / CAST([sums].[total_outlays_current_year] AS REAL) AS [unknown_and_improper_rate_current_year],
    [cy_target].[reduction_target_rate_current_year],
    100 * [sums].[total_automation_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_automation],
    100 * [sums].[total_behavioral_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_behavioral],
    100 * [sums].[total_training_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_training],
    100 * [sums].[total_change_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_change],
    100 * [sums].[total_sharing_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_sharing],
    100 * [sums].[total_audit_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_audit],
    100 * [sums].[total_analytics_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_analytics],
    100 * [sums].[total_statutory_responses] / CAST([program].[unique_program_count] AS REAL) AS [response_rate_statutory],
    [agency_sums].[total_arp1] + [agency_sums].[total_arp3] AS [identified_for_recovery],
    [agency_sums].[total_arp2] + [agency_sums].[total_arp6] AS [recovered],
    100 * ([agency_sums].[total_arp2] + [agency_sums].[total_arp6]) / CAST(([agency_sums].[total_arp1] + [agency_sums].[total_arp3]) AS REAL) AS [recovery_rate],
    [sums].[Fiscal_Year]
FROM (
    SELECT
            SUM(CASE WHEN LOWER([key]) = 'cyp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp27' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_improper_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp7' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_unknown_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp16' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_next_year,
            SUM(CASE WHEN LOWER([key]) = 'atp1_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_automation_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp2_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_behavioral_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp3_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_training_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp4_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_change_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp5_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_sharing_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp6_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_audit_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp7_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_analytics_responses,
            SUM(CASE WHEN LOWER([key]) = 'atp8_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_statutory_responses,
            [Fiscal_Year]
        FROM [congressional_reports_program]
        GROUP BY [Fiscal_Year]) [sums]
LEFT JOIN (
    SELECT
            SUM(CASE WHEN LOWER([key]) = 'cyp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp27' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_improper_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp7' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_unknown_current_year,
            SUM(CASE WHEN LOWER([key]) = 'cyp16' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_next_year,
            [Fiscal_Year]
        FROM [congressional_reports_program]
        GROUP BY [Fiscal_Year]) [py_sums]
ON [sums].[Fiscal_Year] = [py_sums].[Fiscal_Year] + 1
LEFT JOIN (
    SELECT
	    SUM([outlays]) AS [total_outlays_for_programs_with_targets],
        SUM([target_ip]) AS [total_unknown_and_improper_next_year],
		100 * CASE WHEN SUM([outlays]) = 0 THEN 0 ELSE SUM([target_ip])/SUM([outlays]) END AS [reduction_target_rate_current_year],
        [program_outlays_and_targets].[Fiscal_Year] FROM (
            SELECT
                COALESCE([cy_outlays].[value],0) AS [outlays],
                COALESCE([ny_targets].[value],0) AS [target_rate],
                COALESCE([cy_outlays].[value],0) * COALESCE([ny_targets].[value],0) / 100 AS [target_ip],
                [cy_outlays].[Fiscal_Year]
            FROM (
                SELECT
                    *
                FROM [congressional_reports_program]
                WHERE [key] = 'cyp1') [cy_outlays]
            JOIN (
                SELECT
                    *
                FROM [congressional_reports_program]
                -- exclude programs that did not report a target rate from the denominator
                WHERE [key] = 'cyp20_1'  AND COALESCE(CAST([value] AS REAL),0) > 0) [ny_targets]
            ON
                [cy_outlays].[Program Name] = [ny_targets].[Program Name] AND
                [cy_outlays].[Fiscal_Year] = [ny_targets].[Fiscal_Year]) [program_outlays_and_targets]
    GROUP BY [program_outlays_and_targets].[Fiscal_Year]
) [cy_target]
ON [sums].[Fiscal_Year] = [cy_target].[Fiscal_Year]
LEFT JOIN (
    SELECT
            SUM(CASE WHEN LOWER([key]) = 'arp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp1,
            SUM(CASE WHEN LOWER([key]) = 'arp2' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp2,
            SUM(CASE WHEN LOWER([key]) = 'arp3' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp3,
            SUM(CASE WHEN LOWER([key]) = 'arp6' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp6,
            [Fiscal_Year]
        FROM [congressional_reports]
        GROUP BY [Fiscal_Year]) [agency_sums]
ON [sums].[Fiscal_Year] = [agency_sums].[Fiscal_Year]
-- count of programs that provided estimates
--  (denominator for actions taken response rates)
LEFT JOIN (
    SELECT
        COUNT(*) AS [unique_program_count],
        [Fiscal_Year]
    FROM (
        SELECT
            [Program Name],
            [Fiscal_Year]
        FROM [congressional_reports_program]
        WHERE LOWER([key]) = 'cyp1' AND [value] IS NOT NULL and [value] > 0) [programs]
    GROUP BY [Fiscal_Year]
) [program]
ON [sums].[Fiscal_Year] = [program].[Fiscal_Year]
WHERE [sums].[Fiscal_Year] = ?