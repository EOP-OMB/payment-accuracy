SELECT
    [Program Name] AS [Program_Name],
    min([value]) filter (where [seq] = 1) as [pcp01],
    min([value]) filter (where [seq] = 4) as [pcp2],
    min([value]) filter (where [seq] = 5) as [pcp3],
    min([value]) filter (where [seq] = 6) as [pcp4],
    min([value]) filter (where [seq] = 7) as [pcp5],
    min([value]) filter (where [seq] = 8) as [pcp6],
    min([value]) filter (where [seq] = 9) as [pcp7],
    min([value]) filter (where [seq] = 10) as [pcp8],
    min([value]) filter (where [seq] = 11) as [pcp9],
    min([value]) filter (where [seq] = 2) as [pcp10],
    min([value]) filter (where [seq] = 3) as [pcp11]
FROM (select [Program Name],[value],
    row_number() over (partition by [Program Name] order by [key]) as seq
    from [program_data_raw]
    where [key] IN (
        'pcp01'
        ,'pcp2'
        ,'pcp3'
        ,'pcp4'
        ,'pcp5'
        ,'pcp6'
        ,'pcp7'
        ,'pcp8'
        ,'pcp9'
        ,'pcp10'
        ,'pcp11'
    ) AND [Agency] = ? AND [Fiscal_Year] = ?
) t
GROUP BY [Program Name]