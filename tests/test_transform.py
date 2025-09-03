import pandas as pd
from data_processing import transform
from unittest.mock import patch, call, MagicMock, ANY

# Mock the sqlite3.connect
# This helps with error when connecting to non-existent database files
with patch('sqlite3.connect', return_value=MagicMock()):    
    # Also patch the database connections in the module
    transform.conn = MagicMock()
    transform.cur = MagicMock()

def test_load_all_programs_file(mock_csv_data, in_memory_db):
    transform.ALL_PROGRAMS_DATA_PATH = mock_csv_data["ALL_PROGRAMS_DATA_PATH"]
    transform.load_all_programs_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM all_programs_data", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency", "Program_Name", "Fiscal_Year", "Outlays_($M)", "IP_Amount($M)", "IP_Unknown_Amount_($M)"]
    assert len(df) == 3

def test_load_program_data_raw_file(mock_csv_data, in_memory_db):
    transform.PROGRAM_DATA_RAW_PATH = mock_csv_data["PROGRAM_DATA_RAW_PATH"]
    transform.load_program_data_raw_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM program_data_raw", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["agency","Program Name","key","value","title","Fiscal_Year"]
    assert len(df) == 3

def test_load_agency_data_raw_file(mock_csv_data, in_memory_db):
    transform.AGENCY_DATA_RAW_PATH = mock_csv_data["AGENCY_DATA_RAW_PATH"]
    transform.load_agency_data_raw_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM agency_data_raw", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["agency","Key","Title","value","Fiscal_Year"]
    assert len(df) == 3

def test_load_ip_agency_pocs_file(mock_csv_data, in_memory_db):
    transform.IP_AGENCY_POCS_PATH = mock_csv_data["IP_AGENCY_POCS_PATH"]
    transform.load_ip_agency_pocs_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM ip_agency_pocs", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency_Acronym", "Agency_Name", "Fiscal_Year"]
    assert len(df) == 3

def test_load_principal_table_columns_file(mock_csv_data, in_memory_db):
    transform.PRINCIPAL_TABLE_COLUMNS_PATH = mock_csv_data["PRINCIPAL_TABLE_COLUMNS_PATH"]
    transform.load_principal_table_columns_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM principal_table_columns", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Fiscal_Year","Agency","Program_Name","Column_names","Column_values","Question","Section","Reporting_Phases_Current_FY"]
    assert len(df) == 3

def test_payment_recovery_details_file(mock_csv_data, in_memory_db):
    transform.PAYMENT_RECOVERY_DETAILS_PATH = mock_csv_data["PAYMENT_RECOVERY_DETAILS_PATH"]
    transform.load_payment_recovery_details_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM payment_recovery_details", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Program_Name","Fiscal_Year","key","value"]
    assert len(df) == 3

def test_payment_confirmed_fraud_file(mock_csv_data, in_memory_db):
    transform.PAYMENT_CONFIRMED_FRAUD_PATH = mock_csv_data["PAYMENT_CONFIRMED_FRAUD_PATH"]
    transform.load_payment_confirmed_fraud_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM payment_confirmed_fraud", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Program_or_Activity","Confirmed_Fraud","Fiscal_Year"]
    assert len(df) == 2

def test_eligibility_themes_file(mock_csv_data, in_memory_db):
    transform.ELIGIBILITY_THEMES_PATH = mock_csv_data["ELIGIBILITY_THEMES_PATH"]
    transform.load_eligibility_themes_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM eligibility_themes", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["key","theme"]
    assert len(df) == 2

def test_risks_file(mock_csv_data, in_memory_db):
    transform.RISKS_PATH = mock_csv_data["RISKS_PATH"]
    transform.load_risks_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM risks", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Fiscal_Year","Program_Name","in_draft","Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_","raa6_2","raa7_2","Updated_Program_Name","Original_Program_Name"]
    assert len(df) == 2

def test_program_compliance_file(mock_csv_data, in_memory_db):
    transform.PROGRAM_COMPLIANCE_PATH = mock_csv_data["PROGRAM_COMPLIANCE_PATH"]
    transform.load_program_compliance_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM program_compliance", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Fiscal_Year","Program_Name","Agency_Compliance","pcp01_1","pcp2_2","pcp3_2","pcp4_2","pcp5_2","pcp6_2","pcp7_2","pcp8_2","pcp9_2","pcp10_2","pcp11_2","pcp12_1"]
    assert len(df) == 2

def test_recovery_amounts_file(mock_csv_data, in_memory_db):
    transform.RECOVERY_AMOUNTS_PATH = mock_csv_data["RECOVERY_AMOUNTS_PATH"]
    transform.load_recovery_amounts_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM recovery_amounts", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Fiscal_Year","Overpayment_Amount_Identified_For_Recapture_($M)","Overpayment_Amount_Recovered_($M)","Recovery_Rate"]
    assert len(df) == 2

def test_survey_root_cause_file(mock_csv_data, in_memory_db):
    transform.SURVEY_ROOT_CAUSE_PATH = mock_csv_data["SURVEY_ROOT_CAUSE_PATH"]
    transform.load_survey_root_cause_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM survey_root_cause", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["End Date","Recorded Date","Agency","Program Name","Please provide a brief 1-2 sentence high level description of yo","RootCauseNumber","RootCause","RootCauseDescription","RootCauseValue","MitigationStrategy","AnticipatedImpactMitigation","Provide a detailed description of the actions taken and planned","Quarter Year"]

    assert len(df) == 2

def test_ip_root_causes_file(mock_csv_data, in_memory_db):
    transform.IP_ROOT_CAUSES_PATH = mock_csv_data["IP_ROOT_CAUSES_PATH"]
    transform.load_ip_root_causes_file(in_memory_db)

    df = pd.read_sql("SELECT * FROM ip_root_causes", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["Agency","Program_Name","Fiscal_Year","Payment_Type","Program_Design_or_Structural_Issue","Inability_to_Authenticate_Eligibility","Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data","Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis","Insufficient_Documentation_to_Determine","Failure_to_Access_Data","Address_Location","Contractor_or_Provider_Status","Financial"]

    assert len(df) == 2

def test_load_congressional_reports_files(mock_csv_data, in_memory_db):
    transform.CONGRESSIONAL_REPORTS_AGENCY_PATH = mock_csv_data["CONGRESSIONAL_REPORTS_PATH"]
    transform.load_congressional_reports_files(in_memory_db)

    df = pd.read_sql("SELECT * FROM congressional_reports", in_memory_db)
    assert not df.empty
    assert list(df.columns) == ["agency","Key","Title","value","Fiscal_Year"]

    assert len(df) == 2

@patch("data_processing.transform.conn", new_callable=MagicMock)
@patch("data_processing.transform.cur", new_callable=MagicMock)
def test_transform_and_insert_all_programs_data_aggregation_data_mocks(mock_cur, mock_conn):
    transform.transform_and_insert_all_programs_data_aggregation_data()

    expected_sql_calls = [
        call(transform.ALL_PROGRAMS_DATA_AGGREGATION_DROP_TABLE_SQL),
        call(transform.ALL_PROGRAMS_DATA_AGGREGATION_CREATE_TABLE_SQL),
        call(transform.ALL_PROGRAMS_DATA_AGGREGATION_SELECT_AND_INSERT_SQL)
    ]

    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=False)
    mock_conn.commit.assert_called_once()

@patch("data_processing.transform.conn", new_callable=MagicMock)
@patch("data_processing.transform.cur", new_callable=MagicMock)
def test_transform_and_insert_all_agencies_data_aggregation_data_mocks(mock_cur, mock_conn):
    transform.transform_and_insert_all_agencies_data_aggregation_data()

    expected_sql_calls = [
        call(transform.ALL_AGENCIES_DATA_AGGREGATION_DROP_TABLE_SQL),
        call(transform.ALL_AGENCIES_DATA_AGGREGATION_CREATE_TABLE_SQL),
        call(transform.ALL_AGENCIES_DATA_AGGREGATION_SELECT_AND_INSERT_TABLE_SQL)
    ]

    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=False)
    mock_conn.commit.assert_called_once()

@patch("data_processing.transform.conn", new_callable=MagicMock)
@patch("data_processing.transform.cur", new_callable=MagicMock)
def test_transform_and_insert_government_wide_data_aggregation_data_mocks(mock_cur, mock_conn):
    transform.transform_and_insert_government_wide_data_aggregation_data()

    expected_sql_calls = [
        call(transform.GOVERNMENT_WIDE_DATA_AGGREGATION_DROP_VIEW_SQL),
        call(transform.GOVERNMENT_WIDE_DATA_AGGREGATION_CREATE_VIEW_SQL)
    ]

    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=False)
    mock_conn.commit.assert_called_once()

@patch("data_processing.transform.conn", new_callable=MagicMock)
@patch("data_processing.transform.cur", new_callable=MagicMock)
def test_recreate_congressional_report_views_mocks(mock_cur, mock_conn):
    transform.recreate_year_mapped_views()

    expected_sql_calls = []
    for drop_query in transform.CONGRESSIONAL_REPORTS_DROP_VIEW_SQL:
        expected_sql_calls.append(call(drop_query))

    for create_query in transform.CONGRESSIONAL_REPORTS_CREATE_VIEW_SQL:
        expected_sql_calls.append(call(create_query))

    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=True)
    mock_conn.commit.assert_called_once()
