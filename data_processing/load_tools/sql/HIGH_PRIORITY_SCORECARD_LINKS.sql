SELECT
    [Link],
    agency.[Program_Name]
FROM (
    SELECT
        [Link],
        [Program_Name]
    FROM program_scorecard_links
    WHERE [Year] <= ?
    GROUP BY [Program_Name]
    HAVING MAX(CONCAT([Year],'-',[Quarter]))
) links
JOIN [significant_or_high_priority_programs] agency ON
    links.[Program_Name] = agency.[Program_Name]
WHERE [Agency] = ?