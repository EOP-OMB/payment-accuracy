SELECT [Assistance Listing Number]
FROM [program_to_aln]
WHERE [Agency] = ? AND [Program Name] = ?
ORDER BY [Assistance Listing Number]
LIMIT 1