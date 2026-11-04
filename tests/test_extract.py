"""
These tests ensure that the current set of CSVs are correct
"""

import ast
import config
import csv
import os
import pandas as pd
import pytest
import re
import sys
from io import StringIO
from load_tools import query

csv.field_size_limit(sys.maxsize)

REPO_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTRACTED_FILES_DIRECTORY = os.path.join(REPO_DIRECTORY, "data_processing", "extracted")
SCORECARD_FILES_DIRECTORY = os.path.join(REPO_DIRECTORY, "website", "assets", "scorecards")
FISCAL_YEAR = config.FISCAL_YEAR
LAST_QUARTERLY_SURVEY = config.LAST_QUARTERLY_SURVEY

@pytest.fixture
def get_agency_codes():
    df = csv_to_dataframe(get_csv_path("IP_Agency_POCs.csv"))
    codes = []
    for i in range(df.shape[0]):
        codes.append(str(df.iloc[i, 0]).upper().strip())

    # exceptions that are known and expected
    codes.append("BBG")
    codes.append("USAGM (BBG)")

    return codes

def get_csv_path(filename):
    return os.path.join(EXTRACTED_FILES_DIRECTORY, filename)

def csv_to_dataframe(path):
    with open(path, encoding="utf-8-sig") as f:
        csv_data = f.read()
    return pd.read_csv(StringIO(csv_data))

def assert_file_exists(path):
    assert os.path.exists(path)

def assert_has_rows(df):
    assert df.shape[0] > 0

def assert_column_count_is_consistent(path):
    assert verify_csv_columns(path)

def assert_fiscal_year_found(df, columnIndex):
    assert FISCAL_YEAR in df.iloc[:, columnIndex].values

def assert_last_quarter_found(df, columnIndex):
    assert LAST_QUARTERLY_SURVEY in df.iloc[:, columnIndex].values

def assert_all_agencies_mapped(df, columnIndex, codes):
    assert all_agencies_mapped(df, columnIndex, codes)

def all_agencies_mapped(df, columnIndex, codes):
    for i in range(df.shape[0]):
        if str(df.iloc[i, columnIndex]).upper().strip() not in codes:
            print("Mapping error:  Agency code " + str(df.iloc[i, columnIndex]) + " not found!")
            return False
    return True

def assert_alns_valid(df, columnIndex):
    valid = True
    # expect 2 characters, a dot, and then 3 characters
    pattern = r"^..\....$"
    for i in range(df.shape[0]):
        text = str(df.iloc[i, columnIndex])
        if not re.fullmatch(pattern, text):
            print("Invalid ALN error: " + text)
            valid = False
    assert valid

def assert_no_duplicates(df, keysList):
    duplicates = df.groupby(keysList).filter(lambda x: len(x) > 1)
    if (duplicates.size > 0):
        print('*** Duplicates found for fields ' + str(keysList))
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(duplicates[keysList])
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
    assert duplicates.size == 0

def verify_csv_columns(path):
    """
    verifies that all rows in a CSV file have the same number of columns
    """
    with open(path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)

        try:
            first_row = next(reader)
            num_columns = len(first_row)
        except StopIteration:
            return True  # Empty file

        for row in reader:
            if len(row) != num_columns:
                return False
    return True

def assert_column_count(df, count):
    assert df.shape[1] == count

def sql_for_fiscal_year(mapping, year):
    if "query" in mapping:
        return mapping["query"]
    return mapping[year]["query"]

def table_name_pattern(table_name):
    # Underscore is a word character, so congressional_reports does not match
    # congressional_reports_program.
    return rf"(?<![A-Za-z0-9_]){re.escape(table_name)}(?![A-Za-z0-9_])"

def enclosing_statement_span(sql, position):
    depth = 0
    start = None
    for index in range(position, -1, -1):
        if sql[index] == ")":
            depth += 1
        elif sql[index] == "(":
            if depth == 0:
                start = index
                break
            depth -= 1
    if start is None:
        return 0, len(sql)

    depth = 0
    end = len(sql)
    for index in range(start, len(sql)):
        if sql[index] == "(":
            depth += 1
        elif sql[index] == ")":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    return start, end

def statements_for_table(sql, table_name):
    spans = []
    for match in re.finditer(table_name_pattern(table_name), sql, flags=re.IGNORECASE):
        spans.append(enclosing_statement_span(sql, match.start()))

    merged = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return "\n".join(sql[start:end] for start, end in merged)

def literal_survey_keys(sql):
    keys = set(re.findall(
        r"LOWER\(\s*\[[^\]]*Key\]\s*\)\s*=\s*'([^']+)'",
        sql,
        flags=re.IGNORECASE,
    ))
    for match in re.finditer(
        r"LOWER\(\s*\[[^\]]*Key\]\s*\)\s*IN\s*\(([^)]*)\)",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        keys.update(re.findall(r"'([^']+)'", match.group(1)))
    return keys

def key_map_survey_keys(sql):
    key_map = re.search(
        r"WITH\s+\[key_map\].*?SELECT\s+\*\s+FROM\s+\(VALUES(.*?)\)\s+AS",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not key_map:
        return set()
    return set(re.findall(r"\(\s*'([^']+)'\s*,", key_map.group(1)))

def survey_keys_from_sql(sql, table_name):
    """Survey keys a query selects from table_name."""
    if not re.search(table_name_pattern(table_name), sql, re.IGNORECASE):
        return set()

    statements = statements_for_table(sql, table_name)
    keys = literal_survey_keys(statements)
    # key_map values live in a leading CTE, outside the statement that joins them.
    if re.search(table_name_pattern("key_map"), statements, re.IGNORECASE):
        keys.update(key_map_survey_keys(sql))

    return {key.lower().strip() for key in keys}

def queried_survey_keys(year, table_name):
    keys = set()
    for mapping in query.query_type_by_year.values():
        keys.update(survey_keys_from_sql(sql_for_fiscal_year(mapping, year), table_name))
    return keys

def congressional_field_mapping_keys(year, mapping=None):
    if mapping is None:
        mapping = config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING
    year_mapping = mapping[str(year)]
    return {
        field["key"].lower().strip()
        for fields in year_mapping.values()
        for field in fields
        if field.get("key")
    }

def congressional_create_view_sql():
    # transform.py runs the load pipeline on import, so read the constant without executing it.
    path = os.path.join(REPO_DIRECTORY, "data_processing", "transform.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "CONGRESSIONAL_REPORTS_CREATE_VIEW_SQL":
                return ast.literal_eval(node.value)
    raise AssertionError("CONGRESSIONAL_REPORTS_CREATE_VIEW_SQL was not found in transform.py")

def current_year_report_views(year, report_group):
    views = set()
    for mapping in config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING:
        if mapping["Year"] == year:
            views.update(name.lower() for name in mapping[report_group].values())
    return views

def congressional_report_view_keys(year, report_group, table_name):
    views = current_year_report_views(year, report_group)
    keys = set()
    for sql in congressional_create_view_sql():
        match = re.search(r"CREATE\s+VIEW\s+([A-Za-z0-9_]+)", sql, flags=re.IGNORECASE)
        if match and match.group(1).lower() in views:
            keys.update(survey_keys_from_sql(sql, table_name))
    return keys

# Survey keys still listed in current-year SQL that the agency survey no longer collects.
UNUSED_AGENCY_SURVEY_KEYS = {
    "ara2_1",
    "ara2_3_2",
    "arp17",
    "arp18",
    "dpa4",
    "pcp12_1",
    "pcp14",
    "raa9",
}

# Survey keys still listed in current-year SQL that the program survey no longer collects.
UNUSED_PROGRAM_SURVEY_KEYS = {
    "rac3",
    "atp1_1",
    "atp2_1",
    "atp3_1",
    "atp4_1",
    "atp5_1",
    "atp6_1",
    "atp7_1",
    "atp8_1",
    "cyp16"
}

def test_Eligibility_Themes():
    path = get_csv_path("Eligibility_Themes.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 2)
    assert_column_count_is_consistent(path)

def test_Eligibility_Themes():
    themes_path = path = get_csv_path("Eligibility_Themes.csv")
    description_path = get_csv_path("Eligibility_Themes_Descriptions.csv")
    assert_file_exists(description_path)

    description_df = csv_to_dataframe(description_path)
    assert_has_rows(description_df)
    assert_column_count(description_df, 2)
    assert_column_count_is_consistent(path)

    # ensure all themes have descriptions
    themes_df = csv_to_dataframe(themes_path)
    themes_lookup = {}
    for _, row in description_df.iterrows():
        themes_lookup[row['theme']] = True

    for _, row in themes_df.iterrows():
        assert row['theme'] in themes_lookup

def test_Eligibility_Theme_Answers_Match_Descriptions():
    # FY2026 answers prefix themes with [ditN]. The load query strips that
    # prefix before joining eligibility_themes_descriptions.
    descriptions = csv_to_dataframe(get_csv_path("Eligibility_Themes_Descriptions.csv"))
    known_themes = set(descriptions["theme"].dropna())
    answers = csv_to_dataframe(get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw.csv"))
    answers = answers[answers["key"].astype(str).str.lower() == "cyp30_dit1_19"]

    missing = set()
    for value in answers["value"].dropna():
        for theme in str(value).split(","):
            theme = re.sub(r"^\[dit\d+\]\s+", "", theme).strip()
            if theme and theme != "Other (please explain)" and theme not in known_themes:
                missing.add(theme)

    if missing:
        print("Eligibility themes with no description after stripping [ditN] prefix:")
        for theme in sorted(missing):
            print(theme)
    assert not missing

def test_IP_Agency_POCs():
    path = get_csv_path("IP_Agency_POCs.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 3)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 2)

def test_KPI_ImproperPaymentsSurveyOverpaymentRecovery_vw_IP():
    path = get_csv_path("KPI_ImproperPaymentsSurveyOverpaymentRecovery_vw_IP.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 9)
    assert_column_count_is_consistent(path)
    assert_last_quarter_found(df, 8)

def test_KPI_ImproperPaymentsSurveyProgressGoal_vw_IP():
    path = get_csv_path("KPI_ImproperPaymentsSurveyProgressGoal_vw_IP.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 10)
    assert_column_count_is_consistent(path)
    assert_last_quarter_found(df, 9)

def test_KPI_ImproperPaymentsSurveyRecentAccomplishment_vw_IP():
    path = get_csv_path("KPI_ImproperPaymentsSurveyRecentAccomplishment_vw_IP.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 7)
    assert_column_count_is_consistent(path)
    assert_last_quarter_found(df, 6)

def test_KPI_ImproperPaymentSurveyRootCause_vw_IP():
    path = get_csv_path("KPI_ImproperPaymentSurveyRootCause_vw_IP.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 13)
    assert_column_count_is_consistent(path)
    assert_last_quarter_found(df, 12)

def test_LastRiskAssessmentByProgram(get_agency_codes):
    path = get_csv_path("LastRiskAssessmentByProgram.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 3)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 1)
    assert_all_agencies_mapped(df, 0, get_agency_codes)

def test_RiskAssessmentMethodologyChanges(get_agency_codes):
    path = get_csv_path("RiskAssessmentMethodologyChanges.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 3)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 2)
    assert_all_agencies_mapped(df, 0, get_agency_codes)

def test_MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 26)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 2)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    assert_no_duplicates(df, ["Agency","Fiscal_Year","Program_Name"])

def test_MY_OMB_ImproperPayment_Payment_Accuracy_Principal_Table_Columns_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Accuracy_Principal_Table_Columns_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 8)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 0)
    assert_all_agencies_mapped(df, 1, get_agency_codes)
    # if multiselect data is ever needed, ETL using a new query, file, and sqllite table
    assert_no_duplicates(df, ['Agency','Program_Name', 'Column_names','Fiscal_Year'])

def test_MY_OMB_ImproperPayment_Payment_Accuracy_Rate_and_Amt_of_Recovery_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Accuracy_Rate_and_Amt_of_Recovery_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 5)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 1)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    assert_no_duplicates(df, ["Agency", "Fiscal_Year"])

def test_MY_OMB_ImproperPayment_Payment_Confirmed_Fraud_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Confirmed_Fraud_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 4)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 3)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # program-level duplicates are summed during transform
    # blank program rows are agency-wide totals; the agency aggregation joins
    # each one, so more than one per agency and year multiplies outlays
    agency_wide = df[df["Program_or_Activity"].isna() | (df["Program_or_Activity"].astype(str).str.strip() == "")].copy()
    agency_wide["Program_or_Activity"] = ""
    assert_no_duplicates(agency_wide, ["Agency", "Fiscal_Year"])

def test_MY_OMB_ImproperPayment_Payment_IP_Root_Causes_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_IP_Root_Causes_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 13)
    assert_column_count_is_consistent(path)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # duplicates handled by summing

def test_MY_OMB_ImproperPayment_Payment_Risk_Assessments_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Risk_Assessments_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 7)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 1)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    assert_no_duplicates(df, ["Agency", "Program_Name", "Fiscal_Year"])

def test_MY_OMB_ImproperPayment_Payment_Program_Compliance_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Program_Compliance_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 16)
    assert_column_count_is_consistent(path)
    assert_all_agencies_mapped(df, 1, get_agency_codes)
    assert_no_duplicates(df, ["Agency", "Program_Name", "Fiscal_Year"])

def test_MY_OMB_ImproperPayment_Payment_Recovery_Details_unpivotted_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_Payment_Recovery_Details_unpivotted_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 5)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 2)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # duplicates handled by summing

def test_MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 5)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 4)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # if multiselect data is ever needed, ETL using a new query, file, and sqllite table
    assert_no_duplicates(df, ['agency','Key','Fiscal_Year'])

def test_MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw_survey_keys():
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw.csv")
    df = csv_to_dataframe(path)
    current_year = df[pd.to_numeric(df["Fiscal_Year"], errors="coerce") == FISCAL_YEAR]
    extracted_keys = {key.lower() for key in current_year["Key"].dropna().astype(str).str.strip()}
    queried_keys = {key.lower() for key in queried_survey_keys(FISCAL_YEAR, "agency_data_raw")}
    unused_keys = {key.lower() for key in UNUSED_AGENCY_SURVEY_KEYS}
    assert queried_keys, "No agency_data_raw survey keys found in current fiscal year queries"

    missing = sorted(queried_keys - extracted_keys - unused_keys)
    if missing:
        print(f"Missing agency survey keys for fiscal year {FISCAL_YEAR}:")
        for key in missing:
            print(key)
    assert not missing

def test_MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw_Congressional(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw-Congressional.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 5)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 4)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # multiselect data is flattened here, so key should never be duplicated for a given year-agency
    assert_no_duplicates(df, ['agency','Key','Fiscal_Year'])

def test_MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw_Congressional_survey_keys():
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw-Congressional.csv")
    df = csv_to_dataframe(path)
    current_year = df[pd.to_numeric(df["Fiscal_Year"], errors="coerce") == FISCAL_YEAR]
    extracted_keys = {key.lower() for key in current_year["Key"].dropna().astype(str).str.strip()}
    queried_keys = {key.lower() for key in queried_survey_keys(FISCAL_YEAR, "congressional_reports")}
    queried_keys.update(congressional_field_mapping_keys(FISCAL_YEAR))
    queried_keys.update(congressional_report_view_keys(FISCAL_YEAR, "AgencyReports", "congressional_reports"))
    unused_keys = {key.lower() for key in UNUSED_AGENCY_SURVEY_KEYS}
    assert queried_keys, "No congressional_reports survey keys found in current fiscal year queries"

    missing = sorted(queried_keys - extracted_keys - unused_keys)
    if missing:
        print(f"Missing congressional agency survey keys for fiscal year {FISCAL_YEAR}:")
        for key in missing:
            print(key)
    assert not missing

def test_MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 6)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 5)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    assert_no_duplicates(df, ['agency','Program Name', 'key','Fiscal_Year'])

def test_MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw_survey_keys():
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw.csv")
    df = csv_to_dataframe(path)
    current_year = df[pd.to_numeric(df["Fiscal_Year"], errors="coerce") == FISCAL_YEAR]
    extracted_keys = {key.lower() for key in current_year["key"].dropna().astype(str).str.strip()}
    queried_keys = {key.lower() for key in queried_survey_keys(FISCAL_YEAR, "program_data_raw")}
    unused_keys = {key.lower() for key in UNUSED_PROGRAM_SURVEY_KEYS}
    assert queried_keys, "No program_data_raw survey keys found in current fiscal year queries"

    missing = sorted(queried_keys - extracted_keys - unused_keys)
    if missing:
        print(f"Missing program survey keys for fiscal year {FISCAL_YEAR}:")
        for key in missing:
            print(key)
    assert not missing

def test_MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw_Congressional(get_agency_codes):
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw-Congressional.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 6)
    assert_column_count_is_consistent(path)
    assert_fiscal_year_found(df, 5)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    # multiselect data is flattened here, so key should never be duplicated for a given year-program
    assert_no_duplicates(df, ['agency','Program Name','key','Fiscal_Year'])

def test_MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw_Congressional_survey_keys():
    path = get_csv_path("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw-Congressional.csv")
    df = csv_to_dataframe(path)
    current_year = df[pd.to_numeric(df["Fiscal_Year"], errors="coerce") == FISCAL_YEAR]
    extracted_keys = {key.lower() for key in current_year["key"].dropna().astype(str).str.strip()}
    queried_keys = {key.lower() for key in queried_survey_keys(FISCAL_YEAR, "congressional_reports_program")}
    queried_keys.update(congressional_field_mapping_keys(FISCAL_YEAR, config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING_PROGRAMS))
    queried_keys.update(congressional_report_view_keys(FISCAL_YEAR, "ProgramReports", "congressional_reports_program"))
    unused_keys = {key.lower() for key in UNUSED_PROGRAM_SURVEY_KEYS}
    assert queried_keys, "No congressional_reports_program survey keys found in current fiscal year queries"

    missing = sorted(queried_keys - extracted_keys - unused_keys)
    if missing:
        print(f"Missing congressional program survey keys for fiscal year {FISCAL_YEAR}:")
        for key in missing:
            print(key)
    assert not missing

def test_ActionsDateMapping():
    path = get_csv_path("ActionsDateMapping.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 4)
    assert_column_count_is_consistent(path)
    assert_no_duplicates(df, ['Action'])
    assert_no_duplicates(df, ['Date'])
    assert_no_duplicates(df, ['Planned', 'Type'])

def test_FPIMapping(get_agency_codes):
    path = get_csv_path("FPIMapping.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 3)
    assert_column_count_is_consistent(path)
    assert_alns_valid(df, 2)
    # spreadsheet contains duplicate entries - they will be ignored during transform
    assert_all_agencies_mapped(df, 0, get_agency_codes)

def test_FY25_Risk_Assessments(get_agency_codes):
    path = get_csv_path("Risk_Assessment_FULL_FY25.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 5)
    assert_column_count_is_consistent(path)
    assert_all_agencies_mapped(df, 0, get_agency_codes)
    assert_no_duplicates(df, ['Agency', 'Fiscal_Year', 'Program_Name'])

def test_ScorecardsMappingFormat():
    path = get_csv_path("Program_Scorecard_Links.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 6)
    assert_column_count_is_consistent(path)
    assert_no_duplicates(df, ['QuarterYear', 'Program_Name'])
    assert_no_duplicates(df, ['QuarterYear', 'Link'])

def test_AllScorecardsPathsExist():
    path = get_csv_path("Program_Scorecard_Links.csv")
    df = csv_to_dataframe(path)

    for _, row in df.iterrows():
        path = os.path.join(REPO_DIRECTORY, "website", row['Link'])
        assert_file_exists(path)

def test_AllScorecardsMappedOnce():
    path = get_csv_path("Program_Scorecard_Links.csv")
    df = csv_to_dataframe(path)

    for dirname in os.listdir(SCORECARD_FILES_DIRECTORY):
        if not os.path.isfile(os.path.join(SCORECARD_FILES_DIRECTORY, dirname)):
            for filename in os.listdir(os.path.join(SCORECARD_FILES_DIRECTORY, dirname)):
                # ignore hidden files, like .DS_Store
                if not filename.startswith('.'):
                    expected_link = os.path.join("assets", "scorecards", dirname, filename)
                    filtered_df = df.query(f'Link == "{expected_link}"')
                    if (len(filtered_df) != 1):
                        print(f"{expected_link} scorecard not mapped once")
                    assert(len(filtered_df) == 1)

# ensures that all scorecards will be displayed on the website (i.e. Program_Name is correct)
def test_ScorecardProgramsActive():
    scorecard_path = get_csv_path("Program_Scorecard_Links.csv")
    scorecard_df = csv_to_dataframe(scorecard_path)

    # there may be a better way to do this, such as pulling the IP program_lookup table
    # this may eventually need to be changed to ignore old, inactive programs
    active_path = get_csv_path("MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw.csv")
    active_df = csv_to_dataframe(active_path)

    for _, row in scorecard_df.iterrows():
        filtered_df = active_df.query(f'Program_Name == "{row["Program_Name"]}"')
        if (len(filtered_df) == 0):
            print(f"{row['Program_Name']} not found in all programs table")
        assert(len(filtered_df) > 0)