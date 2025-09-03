import config
import sqlite3
from enum import Enum

class QUERY_TYPES(Enum):
    AGENCY_NAMES = 1
    AGENCIES_HAVING_CONGRESSIONAL_DATA = 2
    SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS = 3
    ACTIONS_TAKEN = 4
    RISK_ASSESSMENTS = 5
    HIGH_PRIORITY_SCORECARD_LINKS = 6
    DNP_SURVEY_RESULTS = 7
    DNP_GW_STATS = 8
    IP_GW_SURVEY_RESULTS = 9
    IP_GW_STATS = 10
    ACTIONS_TAKEN_ADDITIONAL_INFO = 11

class KEY_TYPES(Enum):
    RISKS_ADDITIONAL_INFORMATION = 1
    RISKS_SUBSTANTIAL_CHANGES_MADE = 2

class query():
    def __init__(self, cursor: sqlite3.Cursor, query_type: QUERY_TYPES, year = config.FISCAL_YEAR):
        self.cursor = cursor
        query_config = query_type_by_year[query_type]

        # some queries have never changed
        if "query" in query_config:
            self.query = query_config
        else:
            self.query = query_config[year]

    def exec(self, params):
        self.cursor.execute(self.query["query"], params)
        results = self.cursor.fetchall()
        return self.query["mapper"](self.cursor, results)

def fetch_all(cursor: sqlite3.Cursor, query_type: QUERY_TYPES, params, year = config.FISCAL_YEAR):
    query_instance = query(cursor, query_type, year)
    return query_instance.exec(params)

agency_results_cache = {}
def fetch_cr_survey_agency_results(cursor: sqlite3.Cursor, view_name, year):
    global agency_results_cache
    if agency_results_cache.get(year, None) == None or agency_results_cache[year].get(view_name, None) is None:
        cursor.execute(f"SELECT * FROM {view_name} WHERE [Fiscal_Year] = ? AND [Answer] IS NOT NULL ORDER BY [Agency], [SortOrder]", (year,))
        results = cursor.fetchall()

        if agency_results_cache.get(year, None) == None:
            agency_results_cache[year] = {}

        agency_results_cache[year][view_name] = [dict(row) for row in results]
    return agency_results_cache[year][view_name]

program_results_cache = {}
def fetch_cr_survey_program_results(cursor: sqlite3.Cursor, view_name, year):
    global program_results_cache
    if program_results_cache.get(year, None) == None or program_results_cache[year].get(view_name, None) is None:
        cursor.execute(f"SELECT * FROM {view_name} WHERE [Fiscal_Year] = ? AND [Answer] IS NOT NULL ORDER BY [Agency], [Program_Name], [SortOrder]", (year,))
        results = cursor.fetchall()

        if program_results_cache.get(year, None) == None:
            program_results_cache[year] = {}

        program_results_cache[year][view_name] = [dict(row) for row in results]
    return program_results_cache[year][view_name]

cr_years_to_generate = list(range(config.FISCAL_YEAR - config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED + 1, config.FISCAL_YEAR + 1))
cr_years_to_generate_placeholder = ','.join(['?'] * len(cr_years_to_generate))

agency_survey_details_cache = {}
def get_agency_survey_details(cursor, year, agency):
    global agency_survey_details_cache
    if agency not in agency_survey_details_cache or year not in agency_survey_details_cache[agency]:
        agencyQuery = f"""
            SELECT
                [agency],
                [Key],
                [Title],
                [value],
                [Fiscal_Year]
            FROM [agency_data_raw]
            WHERE [Fiscal_Year] = ? AND [Agency] = ?
        """
        cursor.execute(agencyQuery, (year, agency))
        details = cursor.fetchall()
        if agency not in agency_survey_details_cache:
            agency_survey_details_cache[agency] = {}
        agency_survey_details_cache[agency][year] = {row["Key"]: row for row in details}
    return agency_survey_details_cache[agency][year]

def get_agency_survey_answer(cursor, year, agency, key_type: KEY_TYPES):
    details = get_agency_survey_details(cursor, year, agency)

    key_config = keys_by_year[key_type]
    key = ''
    # some keys have never changed
    if isinstance(key_config, str):
        key = key_config
    else:
        key = key_config[year]

    row = details.get(key, None)
    value = None
    if row is not None:
        value = row["value"]
    return value

agency_names_lookup = {}
def get_agency_name(cursor, agency_code, year = config.FISCAL_YEAR):
    global agency_names_lookup
    if not agency_names_lookup:
        agencies = fetch_all(cursor, QUERY_TYPES.AGENCY_NAMES, (year,), year)
        agency_names_lookup = { agencyNameRow["Agency_Acronym"]: agencyNameRow["Agency_Name"] for agencyNameRow in agencies }
    if agency_code in agency_names_lookup:
        return agency_names_lookup[agency_code]
    else:
        return None

def default_mapper(cursor, results):
    return [dict(row) for row in results]

keys_by_year = {
    KEY_TYPES.RISKS_ADDITIONAL_INFORMATION: "raa9",
    KEY_TYPES.RISKS_SUBSTANTIAL_CHANGES_MADE: "raa8"
}

query_type_by_year = {
    QUERY_TYPES.AGENCY_NAMES: {
        "query": """
            SELECT DISTINCT
                Agency_Acronym,
                Agency_Name
            FROM ip_agency_pocs
            WHERE [Fiscal_Year] = ?
        """,
        "mapper": default_mapper
    },
    QUERY_TYPES.AGENCIES_HAVING_CONGRESSIONAL_DATA: {
        "query": f"""
            SELECT DISTINCT agency FROM congressional_reports
            UNION
            SELECT DISTINCT agency FROM congressional_reports_program
            WHERE [Fiscal_Year] IN ({cr_years_to_generate_placeholder})
        """,
        "mapper": default_mapper
    },
    QUERY_TYPES.SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS: {
        "query": f"SELECT * FROM [significant_or_high_priority_programs]",
        "mapper": default_mapper
    },
    QUERY_TYPES.ACTIONS_TAKEN: {
        "query": """
            SELECT
                [action_data].[Fiscal_Year],
                [action_data].[Agency],
                [action_data].[Program_Name],
                [action_data].[Column_names] AS [Mitigation_Strategy],
                [action_data].[Column_values] AS [Description_Action_Taken],
                CASE
                    WHEN [action_data].Column_names LIKE 'app%\\_1' ESCAPE '\\' AND [date_lookup].[Column_values] NOT LIKE 'The corrective action was not fully completed%' THEN 'Planned'
                    WHEN ([action_data].Column_names LIKE 'atp%\\_1' ESCAPE '\\' OR [action_data].Column_names LIKE 'app%\\_1' ESCAPE '\\') AND [date_lookup].[Column_values] LIKE 'The corrective action was not fully completed%' THEN 'Not Completed'
                    ELSE 'Completed'
                END as [Action_Taken],
                [date_lookup].[Column_values] AS [Completion_Date],
                COALESCE([type_lookup].[Type], [action_data].Column_names) AS [Action_Type]
            FROM [principal_table_columns] [action_data]
            LEFT JOIN [actions_date_mapping] ON
                [action_data].[Column_names] = [actions_date_mapping].[Action]
            LEFT JOIN (
                SELECT
                    [Fiscal_Year],
                    [Agency],
                    [Program_Name],
                    [Column_names],
                    [Column_values]
                FROM [principal_table_columns]
            ) [date_lookup] ON
                [action_data].[Fiscal_Year] = [date_lookup].[Fiscal_Year] AND
                [action_data].[Agency] = [date_lookup].[Agency] AND
                [action_data].[Program_Name] = [date_lookup].[Program_Name] AND
                [actions_date_mapping].[Date] = [date_lookup].[Column_names]
            LEFT JOIN (
                SELECT
                    [Type],
                    [Action]
                FROM [actions_date_mapping]
            ) [type_lookup] ON [action_data].Column_names = [type_lookup].[Action]
            WHERE [action_data].Column_values <> ''
                AND ([action_data].Column_names LIKE 'atp%\\_1' ESCAPE '\\' OR [action_data].Column_names LIKE 'app%\\_1' ESCAPE '\\')
                -- not showing on old site
                AND [action_data].Column_names <> 'atp17_1'
                AND [action_data].Column_names <> 'app17_1'
                AND [action_data].[Program_Name] = ? AND [action_data].[Fiscal_Year] = ?""",
        "mapper": lambda cursor, actions: list(map(lambda x: {
            "Mitigation_Strategy": x["Mitigation_Strategy"],
            "Description_Action_Taken": x["Description_Action_Taken"],
            "Action_Taken": x["Action_Taken"],
            "Completion_Date": x["Completion_Date"],
            "Action_Type": x["Action_Type"]
        }, actions))
    },
    QUERY_TYPES.RISK_ASSESSMENTS: {
        "query": f"""
            SELECT
                a.[Agency],
                a.[Fiscal_Year],
                a.[Program_Name],
                CASE WHEN
                    (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'NO' OR upper([raa7_2]) = 'NO') THEN 'No'
                    ELSE 'Yes' END AS [Susceptible]
            FROM [risks] a
            JOIN (
                SELECT
                    [Agency],
                    MAX([Fiscal_Year]) AS [LastRiskAssessment],
                    [Program_Name]
                FROM [risks]
                WHERE (upper([raa6_2]) = 'YES' OR [Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_] IS NOT NULL)
                    AND (
                        (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'NO' OR upper([raa7_2]) = 'NO') OR
                        (upper([Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_]) = 'YES' OR upper([raa7_2]) = 'YES')
                    )
                    AND ([Agency] = ? AND [Fiscal_Year] <= ?)
                GROUP BY [Agency], [Program_Name]
            ) b ON a.[Agency] = b.[Agency] AND UPPER(a.[Program_Name]) = UPPER(b.[Program_Name]) AND a.[Fiscal_Year] = b.[LastRiskAssessment]
            ORDER BY a.[Program_Name]
        """,
        "mapper": default_mapper
    },
    QUERY_TYPES.HIGH_PRIORITY_SCORECARD_LINKS: {
        "query": """
            SELECT
                [Link],
                agency.[Program_Name]
            FROM (
                SELECT
                    [Link],
                    [Program_Name]
                FROM program_scorecard_links
                WHERE [Year] = ?
                GROUP BY [Program_Name]
                HAVING MAX(CONCAT([Year],'-',[Quarter]))
            ) links
            JOIN [significant_or_high_priority_programs] agency ON
                links.[Program_Name] = agency.[Program_Name]
            WHERE [Agency] = ?
        """,
        "mapper": default_mapper
    },
    QUERY_TYPES.DNP_SURVEY_RESULTS: {
        "query": """
            SELECT
                [agency] AS [Agency],
                [Fiscal_Year],
                [Key],
                [Title] AS [Question],
                [value] AS [Answer],
                CASE [Key]
                    WHEN 'dpa5' THEN 0
                END AS [SortOrder]
            FROM [congressional_reports]
            WHERE [Key] IN (
                'dpa5'
            )
            AND [Fiscal_Year] = ?
        """,
        "mapper": lambda cursor, answers: list(map(lambda x: {
            "Answer": x["Answer"],
            "Agency": x["Agency"],
            "Agency_Name": get_agency_name(cursor, x["Agency"])
        }, answers))
    },
    QUERY_TYPES.DNP_GW_STATS: {
        "query": """
            SELECT
                CAST([counts].[dpa1_yes] as REAL) * 100 / [counts].[dpa1_all] AS dpa1_yes,
                CAST([counts].[dpa1_no] as REAL) * 100 / [counts].[dpa1_all] AS dpa1_no,
                CAST([counts].[dpa2_yes] as REAL) * 100 / [counts].[dpa2_all] AS dpa2_yes,
                CAST([counts].[dpa2_no] as REAL) * 100 / [counts].[dpa2_all] AS dpa2_no,
                CAST([counts].[dpa3_daily] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_daily,
                CAST([counts].[dpa3_weekly] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_weekly,
                CAST([counts].[dpa3_monthly] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_monthly,
                CAST([counts].[dpa3_quarterly] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_quarterly,
                CAST([counts].[dpa3_annually] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_annually,
                CAST([counts].[dpa3_na] as REAL) * 100 / [counts].[dpa3_all] AS dpa3_na
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
        """,
        "mapper": default_mapper
    },
    QUERY_TYPES.IP_GW_SURVEY_RESULTS: {
        "query": """
            SELECT
                [agency] AS [Agency],
                [Fiscal_Year],
                [Key],
                [Title] AS [Question],
                [value] AS [Answer],
                CASE [Key]
                    WHEN 'com1' THEN 0
                END AS [SortOrder]
            FROM [congressional_reports]
            WHERE [Key] IN (
                'com1'
            ) AND [Fiscal_Year] = ?
        """,
        "mapper": lambda cursor, answers: list(map(lambda x: {
            "Answer": x["Answer"],
            "Agency": x["Agency"],
            "Agency_Name": get_agency_name(cursor, x["Agency"])
        }, answers))
    },
    QUERY_TYPES.IP_GW_STATS: {
        2023: {
            "query": """
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
            """,
            "mapper": default_mapper
        },
        2024: {
            "query": """
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
            """,
            "mapper": default_mapper
        },
        2025: {
            "query": """
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
                    100 * ([cy_target].[total_unknown_and_improper_next_year]) / CAST((
                        CASE WHEN [sums].[total_outlays_next_year] IS NULL OR [sums].[total_outlays_next_year] = 0 THEN [sums].[total_outlays_current_year] ELSE [sums].[total_outlays_next_year] END
                    ) AS REAL) AS [reduction_target_rate_current_year],
                    100 * ([py_target].[total_unknown_and_improper_next_year]) / CAST((
                        CASE WHEN [py_sums].[total_outlays_next_year] IS NULL OR [py_sums].[total_outlays_next_year] = 0 THEN [py_sums].[total_outlays_current_year] ELSE [py_sums].[total_outlays_next_year] END
                    ) AS REAL) AS [reduction_target_rate_prior_year],
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
            """,
            "mapper": default_mapper
        }
    },
    QUERY_TYPES.ACTIONS_TAKEN_ADDITIONAL_INFO: {
        "query": """
            SELECT
                [value] AS [Answer],
                CASE [Key]
                    WHEN 'rnp3' THEN 'Sufficiency'
                    WHEN 'rnp4' THEN 'Accountability'
                    WHEN 'rap5' THEN 'Needs1'
                    WHEN 'rap6' THEN 'Needs2'
                END AS [ViewKey]
            FROM [congressional_reports_program]
            WHERE [Key] IN (
                'rnp3',
                'rnp4',
                'rap5',
                'rap6'
            ) AND [Program Name] = ? AND [agency] = ? AND [Fiscal_Year] = ?
        """,
        "mapper": lambda cursor, answers: { ans["ViewKey"]: ans["Answer"] for ans in answers }
    }
}