import config
import hashlib
import os
import re
import sqlite3
from enum import Enum

QUERY_TYPES = Enum('QUERY_TYPES', [
    'ACTIONS_TAKEN',
    'ACTIONS_TAKEN_ADDITIONAL_INFO',
    'AGENCIES_HAVING_CONGRESSIONAL_DATA',
    'AGENCY_NAMES',
    'AGENCY_RATE_EXTREMES',
    'AGENCY_SURVEY_KEY_AGNOSTIC',
    'AGENCY_WIDE_TABLE_AGENCIES',
    'AGENCY_WIDE_TABLE_PROGRAMS',
    'ALL_AGENCIES_YEARS',
    'ALL_AGENCIES_YEARS_AVAILABLE',
    'ALL_PROGRAMS',
    'DISTINCT_AGENCIES',
    'DNP_GW_STATS',
    'DNP_SURVEY_RESULTS',
    'ELIGIBILITY_THEME_DETAILS',
    'FPI_LINK',
    'HIGH_PRIORITY_SCORECARD_LINKS',
    'IP_HIGHEST_PERFORMING_AGENCIES',
    'IP_GW_RATE_EXTREMES',
    'IP_GW_RATES',
    'IP_GW_STATS',
    'IP_GW_SURVEY_RESULTS',
    'IP_WORST_PERFORMING_AGENCIES',
    'PAYMENT_RECOVERY_AMOUNTS',
    'PAYMENT_RECOVERY_DETAILS',
    'PIIA_NON_COMPLIANT_PROGRAMS',
    'PROGRAM_ADDITIONAL_INFORMATION',
    'PROGRAM_CORRECTIVE_ACTIONS',
    'PROGRAM_DATA_POINTS',
    'PROGRAM_ELIGIBILITY_INFORMATION',
    'PROGRAM_ELIGIBILITY_INFORMATION_AGGREGATED',
    'PROGRAM_FUTURE_OUTLOOK',
    'PROGRAM_IP_ESTIMATES',
    'PROGRAM_OVERPAYMENTS',
    'PROGRAM_OVERPAYMENTS_OUTSIDE',
    'PROGRAM_PAYMENTS_VISIBILITY',
    'PROGRAM_SCORECARD_LINKS',
    'PROGRAM_SURVEY_KEY_AGNOSTIC',
    'PROGRAM_TECHNICIALLY_IMPROPER_PAYMENTS',
    'PROGRAM_UNDERPAYMENTS',
    'PROGRAM_UNKNOWN_PAYMENTS',
    'PROGRAM_UNKNOWN_PAYMENTS_BREAKDOWN',
    'RISK_ASSESSMENTS',
    'SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS',
])

KEY_TYPES = Enum('KEY_TYPES', [
    'Risks_Additional_Information',
    'Risks_Substantial_Changes_Made'
])

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

        mapper = self.query.get("mapper", default_mapper)

        return mapper(self.cursor, results)

def fetch_all(cursor: sqlite3.Cursor, query_type: QUERY_TYPES, params = (), year = config.FISCAL_YEAR):
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

agency_survey_details_cache = {}
def get_agency_survey_details(cursor, year, agency):
    global agency_survey_details_cache
    if agency not in agency_survey_details_cache or year not in agency_survey_details_cache[agency]:
        details = fetch_all(cursor, QUERY_TYPES.AGENCY_SURVEY_KEY_AGNOSTIC, (year, agency), year)
        if agency not in agency_survey_details_cache:
            agency_survey_details_cache[agency] = {}
        agency_survey_details_cache[agency][year] = {row["Name"]: row for row in details}
    return agency_survey_details_cache[agency][year]

def get_agency_survey_answer(cursor, year, agency, key: KEY_TYPES):
    details = get_agency_survey_details(cursor, year, agency)
    row = details.get(key.name, None)
    value = None
    if row is not None:
        value = row["value"]
    return value

agency_names_lookup = {}
def get_agency_name(cursor, agency_code, year = config.FISCAL_YEAR):
    global agency_names_lookup
    if not agency_names_lookup:
        agencies = fetch_all(cursor, QUERY_TYPES.AGENCY_NAMES, (), year)
        agency_names_lookup = { agencyNameRow["Agency_Acronym"]: agencyNameRow["Agency_Name"] for agencyNameRow in agencies }
    if agency_code in agency_names_lookup:
        return agency_names_lookup[agency_code]
    else:
        return None

def slugify(name, max_length=60):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
    if len(slug) > max_length:
        # Truncate and add hash to preserve uniqueness
        slug = slug[:max_length] + '-' + hashlib.md5(name.encode()).hexdigest()[:8]
    return slug

slugs_lookup = {}
def slugifyProgramNames(cursor: sqlite3.Cursor):
    programs = fetch_all(cursor, QUERY_TYPES.SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS, ())
    for program in programs:
        slugs_lookup[program["Program_Name"]] = slugify(program["Agency"] + "-" + program["Program_Name"])
    print("Successfully slugified program names")

def get_slug(cursor, name):
    if not slugs_lookup:
        slugifyProgramNames(cursor)
    return slugs_lookup.get(name, None)

def get_sql_file(filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_directory, 'sql',filename)
    file_content = ''
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{full_path}' was not found.")
        raise

    return file_content

def default_mapper(cursor, results):
    return [dict(row) for row in results]

def agency_wide_table_programs_mapper(cursor, programs):
    mapped_programs = []
    for program in programs:
        mapped_program = {
            "program_name": program["Program_Name"],
            "total_spent_federal_funding": program["Total_Spent_Federal_Funding"],
            "high_priority_program": bool(program["High_Priority_Program"]),
            "ip_rate": program["IP_Rate"],
            "relative_change": program["Relative_Change"],
            "agency": program["Agency"]
        }
        slug = get_slug(cursor, program["Program_Name"])
        if slug:
            mapped_program["slug"] = slug
        mapped_programs.append(mapped_program)

    return mapped_programs

def agency_wide_table_agencies_mapper(cursor, agencies):
    mapped_agencies = []
    for row in agencies:
        mapped_agency = {
            "agency": row["Agency"],
            "agency_name": row["Agency_Name"],
            "total_spent_federal_funding": row["Total_Spent_Federal_Funding"],
            "num_programs": row["Num_Programs"],
            "susceptible_programs": row["Susceptible_Programs"],
            "high_priority_programs": row["High_Priority_Programs"],
            "improper_payments_rate": row["Improper_Payments_Rate"],
            "relative_change": row["Relative_Change"]
        }
        mapped_agencies.append(mapped_agency)

    return mapped_agencies

def risk_assessments_mapper(cursor, assessments):
    assessments = default_mapper(cursor, assessments)
    for assessment in assessments:
        assessment["Slug"] = get_slug(cursor, assessment["Program_Name"])
        del assessment["Agency"]

    return assessments

def actions_taken_mapper(cursor, actions):
    return list(map(lambda x: {
        "Mitigation_Strategy": x["Mitigation_Strategy"],
        "Description_Action_Taken": x["Description_Action_Taken"],
        "Action_Taken": x["Action_Taken"],
        "Completion_Date": x["Completion_Date"],
        "Action_Type": x["Action_Type"]
    }, actions))

def return_nothing(cursor, actions):
    return []

def all_programs_mapper(cursor, programs):
    programs = default_mapper(cursor, programs)
    for program in programs:
        program["Slug"] = str(get_slug(cursor, program["Program_Name"]))

    return programs

def piia_programs_compliance_mapper_2019(cursor, results):
    compliance_survey_to_criterion_mapping = {
        'pcp01': 'Overall',
        'pcp2': '1A',
        'pcp3': '1B',
        'pcp4': '2A',
        'pcp5': '2B',
        'pcp6': '3',
        'pcp7': '4',
        'pcp8': '5A',
        'pcp9': '5B',
        'pcp10': '5C',
        'pcp11': '6'
    }

    mappedPrograms = []
    for result in results:
        mappedProgram = { 'Name': result['Program_Name'] }
        slug = get_slug(cursor, result['Program_Name'])
        if slug:
            mappedProgram['Slug'] = slug

        for key, value in compliance_survey_to_criterion_mapping.items():
            mappedProgram['Compliant_' + value] = str(result[key]).upper() != 'NON-COMPLIANT'
        mappedPrograms.append(mappedProgram)

    return mappedPrograms

def piia_programs_compliance_mapper_2023(cursor, results):
    compliance_survey_to_criterion_mapping = {
        'pcp01_1': 'Overall',
        'pcp2_2': '1A',
        'pcp3_2': '1B',
        'pcp4_2': '2A',
        'pcp5_2': '2B',
        'pcp6_2': '3',
        'pcp7_2': '4',
        'pcp8_2': '5A',
        'pcp9_2': '5B',
        'pcp10_2': '5C',
        'pcp11_2': '6'
    }

    mappedPrograms = []
    for result in results:
        mappedProgram = { 'Name': result['Program_Name'] }
        slug = get_slug(cursor, result['Program_Name'])
        if slug:
            mappedProgram['Slug'] = slug

        for key, value in compliance_survey_to_criterion_mapping.items():
            mappedProgram['Compliant_' + value] = str(result[key]).upper() == 'YES'
        mappedPrograms.append(mappedProgram)

    return mappedPrograms

query_type_by_year = {
    QUERY_TYPES.AGENCY_NAMES: {
        "query": get_sql_file("AGENCY_NAMES.sql")
    },
    QUERY_TYPES.AGENCIES_HAVING_CONGRESSIONAL_DATA: {
        "query": get_sql_file("AGENCIES_HAVING_CONGRESSIONAL_DATA.sql")
    },
    QUERY_TYPES.SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS: {
        "query": get_sql_file("SIGNIFICANT_OR_HIGH_PRIORITY_PROGRAMS.sql")
    },
    QUERY_TYPES.ACTIONS_TAKEN: {
        2019: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2020: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2021: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2022: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2023: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2024: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": actions_taken_mapper
        },
        2025: {
            "query": get_sql_file("ACTIONS_TAKEN.sql"),
            "mapper": return_nothing
        }
    },
    QUERY_TYPES.RISK_ASSESSMENTS: {
        "query": get_sql_file("RISK_ASSESSMENTS.sql"),
        "mapper": risk_assessments_mapper
    },
    QUERY_TYPES.HIGH_PRIORITY_SCORECARD_LINKS: {
        "query": get_sql_file("HIGH_PRIORITY_SCORECARD_LINKS.sql")
    },
    QUERY_TYPES.DNP_SURVEY_RESULTS: {
        "query": get_sql_file("DNP_SURVEY_RESULTS.sql"),
        "mapper": lambda cursor, answers: list(map(lambda x: {
            "Answer": x["Answer"],
            "Agency": x["Agency"],
            "Agency_Name": get_agency_name(cursor, x["Agency"])
        }, answers))
    },
    QUERY_TYPES.DNP_GW_STATS: {
        "query": get_sql_file("DNP_GW_STATS.sql")
    },
    QUERY_TYPES.IP_GW_SURVEY_RESULTS: {
        "query": get_sql_file("IP_GW_SURVEY_RESULTS.sql"),
        "mapper": lambda cursor, answers: list(map(lambda x: {
            "Answer": x["Answer"],
            "Agency": x["Agency"],
            "Agency_Name": get_agency_name(cursor, x["Agency"])
        }, answers))
    },
    QUERY_TYPES.IP_GW_STATS: {
        2023: {
            "query": get_sql_file("IP_GW_STATS_2023.sql")
        },
        2024: {
            "query": get_sql_file("IP_GW_STATS_2023.sql")
        },
        2025: {
            "query": get_sql_file("IP_GW_STATS_2025.sql")
        }
    },
    QUERY_TYPES.ACTIONS_TAKEN_ADDITIONAL_INFO: {
        "query": get_sql_file("ACTIONS_TAKEN_ADDITIONAL_INFO.sql"),
        "mapper": lambda cursor, answers: { ans["ViewKey"]: ans["Answer"] for ans in answers }
    },
    QUERY_TYPES.IP_GW_RATE_EXTREMES: {
        "query": get_sql_file("IP_GW_RATE_EXTREMES.sql")
    },
    QUERY_TYPES.IP_HIGHEST_PERFORMING_AGENCIES: {
        "query": get_sql_file("IP_HIGHEST_PERFORMING_AGENCIES.sql")
    },
    QUERY_TYPES.IP_WORST_PERFORMING_AGENCIES: {
        "query": get_sql_file("IP_WORST_PERFORMING_AGENCIES.sql")
    },
    QUERY_TYPES.IP_GW_RATES: {
        "query": get_sql_file("IP_GW_RATES.sql")
    },
    QUERY_TYPES.AGENCY_WIDE_TABLE_PROGRAMS: {
        "query": get_sql_file("AGENCY_WIDE_TABLE_PROGRAMS.sql"),
        "mapper": agency_wide_table_programs_mapper
    },
    QUERY_TYPES.AGENCY_WIDE_TABLE_AGENCIES: {
        "query": get_sql_file("AGENCY_WIDE_TABLE_AGENCIES.sql"),
        "mapper": agency_wide_table_agencies_mapper
    },
    QUERY_TYPES.ALL_AGENCIES_YEARS: {
        "query": get_sql_file("ALL_AGENCIES_YEARS.sql")
    },
    QUERY_TYPES.ALL_AGENCIES_YEARS_AVAILABLE: {
        "query": get_sql_file("ALL_AGENCIES_YEARS_AVAILABLE.sql")
    },
    # prior to 2021, no null record was created for summarization
    QUERY_TYPES.PAYMENT_RECOVERY_DETAILS: {
        2019: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2019.sql")
        },
        2020: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2019.sql")
        },
        2021: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2019.sql")
        },
        2022: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2022.sql")
        },
        2023: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2022.sql")
        },
        2024: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2022.sql")
        },
        2025: {
            "query": get_sql_file("PAYMENT_RECOVERY_DETAILS_2022.sql")
        }
    },
    QUERY_TYPES.PAYMENT_RECOVERY_AMOUNTS: {
        "query": get_sql_file("PAYMENT_RECOVERY_AMOUNTS.sql")
    },
    QUERY_TYPES.AGENCY_RATE_EXTREMES: {
        "query": get_sql_file("AGENCY_RATE_EXTREMES.sql")
    },
    QUERY_TYPES.PIIA_NON_COMPLIANT_PROGRAMS: {
        2019: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2019.sql"),
            "mapper": piia_programs_compliance_mapper_2019
        },
        2020: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2019.sql"),
            "mapper": piia_programs_compliance_mapper_2019
        },
        2021: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2019.sql"),
            "mapper": piia_programs_compliance_mapper_2019
        },
        2022: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2019.sql"),
            "mapper": piia_programs_compliance_mapper_2019
        },
        2023: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2023.sql"),
            "mapper": piia_programs_compliance_mapper_2023
        },
        2024: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2023.sql"),
            "mapper": piia_programs_compliance_mapper_2023
        },
        2025: {
            "query": get_sql_file("PIIA_NON_COMPLIANT_PROGRAMS_2023.sql"),
            "mapper": piia_programs_compliance_mapper_2023
        }
    },
    QUERY_TYPES.ELIGIBILITY_THEME_DETAILS: {
        "query": get_sql_file("ELIGIBILITY_THEME_DETAILS.sql")
    },
    QUERY_TYPES.DISTINCT_AGENCIES: {
        "query": get_sql_file("DISTINCT_AGENCIES.sql")
    },
    QUERY_TYPES.ALL_PROGRAMS: {
        "query": get_sql_file("ALL_PROGRAMS.sql"),
        "mapper": all_programs_mapper
    },
    QUERY_TYPES.PROGRAM_DATA_POINTS: {
        "query": get_sql_file("PROGRAM_DATA_POINTS.sql")
    },
    QUERY_TYPES.PROGRAM_IP_ESTIMATES: {
        "query": get_sql_file("PROGRAM_IP_ESTIMATES.sql")
    },
    QUERY_TYPES.PROGRAM_PAYMENTS_VISIBILITY: {
        "query": get_sql_file("PROGRAM_PAYMENTS_VISIBILITY.sql")
    },
    QUERY_TYPES.PROGRAM_OVERPAYMENTS: {
        "query": get_sql_file("PROGRAM_OVERPAYMENTS.sql")
    },
    QUERY_TYPES.PROGRAM_OVERPAYMENTS_OUTSIDE: {
        "query": get_sql_file("PROGRAM_OVERPAYMENTS_OUTSIDE.sql")
    },
    QUERY_TYPES.PROGRAM_UNDERPAYMENTS: {
        "query": get_sql_file("PROGRAM_UNDERPAYMENTS.sql")
    },
    QUERY_TYPES.PROGRAM_TECHNICIALLY_IMPROPER_PAYMENTS: {
        "query": get_sql_file("PROGRAM_TECHNICIALLY_IMPROPER_PAYMENTS.sql")
    },
    QUERY_TYPES.PROGRAM_ELIGIBILITY_INFORMATION: {
        "query": get_sql_file("PROGRAM_ELIGIBILITY_INFORMATION.sql")
    },
    QUERY_TYPES.PROGRAM_ELIGIBILITY_INFORMATION_AGGREGATED: {
        "query": get_sql_file("PROGRAM_ELIGIBILITY_INFORMATION_AGGREGATED.sql")
    },
    QUERY_TYPES.PROGRAM_UNKNOWN_PAYMENTS: {
        "query": get_sql_file("PROGRAM_UNKNOWN_PAYMENTS.sql")
    },
    QUERY_TYPES.PROGRAM_UNKNOWN_PAYMENTS_BREAKDOWN: {
        "query": get_sql_file("PROGRAM_UNKNOWN_PAYMENTS_BREAKDOWN.sql")
    },
    QUERY_TYPES.PROGRAM_CORRECTIVE_ACTIONS: {
        "query": get_sql_file("PROGRAM_CORRECTIVE_ACTIONS.sql")
    },
    QUERY_TYPES.PROGRAM_FUTURE_OUTLOOK: {
        "query": get_sql_file("PROGRAM_FUTURE_OUTLOOK.sql")
    },
    QUERY_TYPES.PROGRAM_ADDITIONAL_INFORMATION: {
        "query": get_sql_file("PROGRAM_ADDITIONAL_INFORMATION.sql")
    },
    QUERY_TYPES.PROGRAM_SCORECARD_LINKS: {
        "query": get_sql_file("PROGRAM_SCORECARD_LINKS.sql")
    },
    QUERY_TYPES.AGENCY_SURVEY_KEY_AGNOSTIC: {
        2019: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2020: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2021: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2022: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2023: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2024: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        },
        2025: {
            "query": get_sql_file("AGENCY_SURVEY_KEY_AGNOSTIC_2019.sql")
        }
    },
    QUERY_TYPES.PROGRAM_SURVEY_KEY_AGNOSTIC: {
        "query": get_sql_file("PROGRAM_SURVEY_KEY_AGNOSTIC.sql")
    },
    QUERY_TYPES.FPI_LINK: {
        "query": get_sql_file("FPI_LINK.sql")
    }
}