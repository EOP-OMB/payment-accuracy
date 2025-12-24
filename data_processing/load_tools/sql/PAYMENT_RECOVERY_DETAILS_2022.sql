SELECT
    [Agency],
    [Fiscal_Year],
    [key],
    SUM([value]) AS [value]
FROM [payment_recovery_details]
WHERE [Fiscal_Year] = ? AND [Agency] = ? AND [Program_Name] IS NULL AND
    -- only retrieve keys that are displayed in the UI
    LOWER([key]) IN (
        'op amt identified outside of payment recapture audits',
        'op amt recapture outside of payment recapture audits',
        'op amt identified through payment recapture audits',
        'op amt recaptured through payment recapture audits',
        'aging of outstanding op identified amt 0 - 6 months',
        'aging of outstanding op identified amt 6 months to 1 year',
        'aging of outstanding op identified determined not collectable',
        'total overpayment amount recovered',
        'total overpayment amount identified'
    )
GROUP BY [Agency], [Fiscal_Year], [key]