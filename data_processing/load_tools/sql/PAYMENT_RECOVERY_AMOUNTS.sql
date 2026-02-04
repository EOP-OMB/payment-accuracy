SELECT
    [recovery_amounts].[Fiscal_Year],
    COALESCE([recovery_amounts].[Overpayment_Amount_Identified_For_Recapture_($M)],0) AS [Overpayment_Amount_Identified_For_Recapture_($M)],
    COALESCE([recovery_amounts].[Overpayment_Amount_Recovered_($M)],0) AS [Overpayment_Amount_Recovered_($M)]
FROM [recovery_amounts]
LEFT JOIN (
    SELECT [Fiscal_Year], [agency], [value] FROM [agency_data_raw]
    WHERE LOWER([Key]) = 'ara1'
) [ara1] ON
    [recovery_amounts].[Fiscal_Year] = [ara1].[Fiscal_Year] AND
    [recovery_amounts].[Agency] = [ara1].[agency]
LEFT JOIN (
    SELECT [Fiscal_Year], [agency], [value] FROM [agency_data_raw]
    WHERE LOWER([Key]) = 'ara2'
) [ara2] ON
    [recovery_amounts].[Fiscal_Year] = [ara2].[Fiscal_Year] AND
    [recovery_amounts].[Agency] = [ara2].[agency]
WHERE
    [recovery_amounts].[Agency] = ? AND
    [recovery_amounts].[Fiscal_Year] <= ? AND [recovery_amounts].[Fiscal_Year] >= ? AND
    -- strip out years where no recovery audit or activities were conducted
    (
        UPPER(COALESCE([ara1].[value],'')) <> 'NO' OR
        UPPER(COALESCE([ara2].[value],'')) <> 'NO'
    ) AND
    -- if nothing was identified for recovery, there's nothing to display
    ROUND([recovery_amounts].[Overpayment_Amount_Identified_For_Recapture_($M)],2) > 0
ORDER BY [recovery_amounts].[Fiscal_Year]