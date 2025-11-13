SELECT
    [Program_Name],
    [pcp01_1],
    [pcp2_2],
    [pcp3_2],
    [pcp4_2],
    [pcp5_2],
    [pcp6_2],
    [pcp7_2],
    [pcp8_2],
    [pcp9_2],
    [pcp10_2],
    [pcp11_2]
FROM program_compliance
WHERE [Agency] = ? AND [Fiscal_Year] = ?
ORDER BY [Program_Name]