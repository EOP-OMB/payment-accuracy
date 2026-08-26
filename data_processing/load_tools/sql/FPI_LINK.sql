SELECT [Assistance Listing Number]
FROM [program_to_aln]
LEFT JOIN [active_alns] ON
    [program_to_aln].[Assistance Listing Number] = [active_alns].[aln]
WHERE [Agency] = ? AND [Program Name] = ? AND (
    -- should be active in SAM.gov or a special case
    [active_alns].[aln] IS NOT NULL OR
    [program_to_aln].[Assistance Listing Number] LIKE 'TC.%' OR
    [program_to_aln].[Assistance Listing Number] LIKE 'IN.%'
)
ORDER BY [Assistance Listing Number]
LIMIT 1