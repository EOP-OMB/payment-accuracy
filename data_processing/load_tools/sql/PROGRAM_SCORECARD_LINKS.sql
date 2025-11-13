SELECT
    [QuarterYear],
    [Link]
FROM [program_scorecard_links]
WHERE [Program_Name] = ?
ORDER BY [Year], [Quarter]