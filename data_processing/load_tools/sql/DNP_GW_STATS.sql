SELECT
    CAST([counts].[dpa1_yes] as REAL) * 100 / [counts].[dpa1_all] AS use_yes,
    CAST([counts].[dpa1_no] as REAL) * 100 / [counts].[dpa1_all] AS use_no,
    CAST([counts].[dpa2_yes] as REAL) * 100 / [counts].[dpa2_all] AS helpful_yes,
    CAST([counts].[dpa2_no] as REAL) * 100 / [counts].[dpa2_all] AS helpful_no,
    CAST([counts].[dpa3_daily] as REAL) * 100 / [counts].[dpa3_all] AS frequency_daily,
    CAST([counts].[dpa3_weekly] as REAL) * 100 / [counts].[dpa3_all] AS frequency_weekly,
    CAST([counts].[dpa3_monthly] as REAL) * 100 / [counts].[dpa3_all] AS frequency_monthly,
    CAST([counts].[dpa3_quarterly] as REAL) * 100 / [counts].[dpa3_all] AS frequency_quarterly,
    CAST([counts].[dpa3_annually] as REAL) * 100 / [counts].[dpa3_all] AS frequency_annually,
    CAST([counts].[dpa3_na] as REAL) * 100 / [counts].[dpa3_all] AS frequency_na
FROM (
    SELECT
        SUM(CASE WHEN [Key] = 'dpa1' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS dpa1_all,
        SUM(CASE WHEN [Key] = 'dpa1' AND LOWER([value]) = 'yes' THEN 1 ELSE 0 END) AS dpa1_yes,
        SUM(CASE WHEN [Key] = 'dpa1' AND LOWER([value]) = 'no' THEN 1 ELSE 0 END) AS dpa1_no,
        SUM(CASE WHEN [Key] = 'dpa2' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS dpa2_all,
        SUM(CASE WHEN [Key] = 'dpa2' AND LOWER([value]) = 'yes' THEN 1 ELSE 0 END) AS dpa2_yes,
        SUM(CASE WHEN [Key] = 'dpa2' AND LOWER([value]) = 'no' THEN 1 ELSE 0 END) AS dpa2_no,
        SUM(CASE WHEN [Key] = 'dpa3' AND [value] IS NOT NULL AND [value] <> '' THEN 1 ELSE 0 END) AS dpa3_all,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) = 'daily' THEN 1 ELSE 0 END) AS dpa3_daily,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) = 'weekly' THEN 1 ELSE 0 END) AS dpa3_weekly,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) = 'monthly' THEN 1 ELSE 0 END) AS dpa3_monthly,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) = 'quarterly' THEN 1 ELSE 0 END) AS dpa3_quarterly,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) = 'annually' THEN 1 ELSE 0 END) AS dpa3_annually,
        SUM(CASE WHEN [Key] = 'dpa3' AND LOWER([value]) LIKE '%did not identify any incorrect information%' THEN 1 ELSE 0 END) AS dpa3_na,
        [Fiscal_Year]
    FROM [congressional_reports]
    WHERE [Fiscal_Year] = ?
    GROUP BY [Fiscal_Year]) [counts]