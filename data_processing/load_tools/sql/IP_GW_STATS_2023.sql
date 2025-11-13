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
    100 * ([cy_target].[total_unknown_and_improper_next_year]) / CAST([sums].[total_outlays_next_year] AS REAL) AS [reduction_target_rate_current_year],
    100 * ([py_target].[total_unknown_and_improper_next_year]) / CAST([py_sums].[total_outlays_next_year] AS REAL) AS [reduction_target_rate_prior_year],
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
            SUM(CASE WHEN [Key] = 'cyp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_current_year,
            SUM(CASE WHEN [Key] = 'cyp27' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_improper_current_year,
            SUM(CASE WHEN [Key] = 'cyp7' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_unknown_current_year,
            SUM(CASE WHEN [Key] = 'cyp16' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_next_year,
            SUM(CASE WHEN [Key] = 'atp1_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_automation_responses,
            SUM(CASE WHEN [Key] = 'atp2_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_behavioral_responses,
            SUM(CASE WHEN [Key] = 'atp3_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_training_responses,
            SUM(CASE WHEN [Key] = 'atp4_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_change_responses,
            SUM(CASE WHEN [Key] = 'atp5_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_sharing_responses,
            SUM(CASE WHEN [Key] = 'atp6_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_audit_responses,
            SUM(CASE WHEN [Key] = 'atp7_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_analytics_responses,
            SUM(CASE WHEN [Key] = 'atp8_1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS total_statutory_responses,
            [Fiscal_Year]
        FROM [congressional_reports_program]
        GROUP BY [Fiscal_Year]) [sums]
LEFT JOIN (
    SELECT
            SUM(CASE WHEN [Key] = 'cyp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_current_year,
            SUM(CASE WHEN [Key] = 'cyp27' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_improper_current_year,
            SUM(CASE WHEN [Key] = 'cyp7' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_unknown_current_year,
            SUM(CASE WHEN [Key] = 'cyp16' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_outlays_next_year,
            [Fiscal_Year]
        FROM [congressional_reports_program]
        GROUP BY [Fiscal_Year]) [py_sums]
ON [sums].[Fiscal_Year] = [py_sums].[Fiscal_Year] + 1
LEFT JOIN (
    SELECT
        [Fiscal_Year],
        SUM([value]) AS [total_unknown_and_improper_next_year]
    FROM (
        SELECT
            [cyp20].[agency],
            [cyp20].[Program Name],
            [cyp20].[Fiscal_Year],
            ([cyp16].[value]/ 100.0) * [cyp20].[value] AS [value]
        FROM [congressional_reports_program] [cyp20]
        LEFT JOIN (
            SELECT
                *
            FROM [congressional_reports_program]
            WHERE [key] = 'cyp16' AND [value] IS NOT NULL
        ) [cyp16]
        ON
            [cyp20].[agency] = [cyp16].[agency] AND
            [cyp20].[Program Name] = [cyp16].[Program Name] AND
            [cyp20].[Fiscal_Year] = [cyp16].[Fiscal_Year]
        WHERE
            [cyp20].[key] = 'cyp20_1' AND
            [cyp20].[value] IS NOT NULL AND
            [cyp16].[value] IS NOT NULL) [cy_targets]
    GROUP BY [Fiscal_Year]
) [cy_target]
ON [sums].[Fiscal_Year] = [cy_target].[Fiscal_Year]
LEFT JOIN (
    SELECT
            SUM(CASE WHEN [key] = 'arp1' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp1,
            SUM(CASE WHEN [key] = 'arp2' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp2,
            SUM(CASE WHEN [key] = 'arp3' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp3,
            SUM(CASE WHEN [key] = 'arp6' AND [value] IS NOT NULL AND [value] <> '' THEN [value] ELSE 0 END) AS total_arp6,
            [Fiscal_Year]
        FROM [congressional_reports]
        GROUP BY [Fiscal_Year]) [agency_sums]
ON [sums].[Fiscal_Year] = [agency_sums].[Fiscal_Year]
LEFT JOIN (
    SELECT
        [Fiscal_Year],
        SUM([value]) AS [total_unknown_and_improper_next_year]
    FROM (
        SELECT
            [cyp20].[agency],
            [cyp20].[Program Name],
            [cyp20].[Fiscal_Year],
            ([cyp16].[value]/ 100.0) * [cyp20].[value] AS [value]
        FROM [congressional_reports_program] [cyp20]
        LEFT JOIN (
            SELECT
                *
            FROM [congressional_reports_program]
            WHERE [key] = 'cyp16' AND [value] IS NOT NULL
        ) [cyp16]
        ON
            [cyp20].[agency] = [cyp16].[agency] AND
            [cyp20].[Program Name] = [cyp16].[Program Name] AND
            [cyp20].[Fiscal_Year] = [cyp16].[Fiscal_Year]
        WHERE
            [cyp20].[key] = 'cyp20_1' AND
            [cyp20].[value] IS NOT NULL AND
            [cyp16].[value] IS NOT NULL) [cy_targets]
    GROUP BY [Fiscal_Year]
) [py_target]
ON [sums].[Fiscal_Year] = [py_target].[Fiscal_Year] + 1
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
        WHERE [key] = 'cyp1' AND [value] IS NOT NULL and [value] > 0) [programs]
    GROUP BY [Fiscal_Year]
) [program]
ON [sums].[Fiscal_Year] = [program].[Fiscal_Year]
WHERE [sums].[Fiscal_Year] = ?