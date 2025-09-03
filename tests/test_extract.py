"""
These tests ensure that the current set of CSVs are correct
"""

import config
import csv
import os
import pandas as pd
import pytest
from io import StringIO

EXTRACTED_FILES_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_processing", "extracted")
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

def assert_no_duplicates(df, keysList):
    grouped = df.groupby(keysList).size().reset_index(name='counts')
    condition = grouped['counts'] == 1
    assert condition.all()

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

def test_Eligibility_Themes():
    path = get_csv_path("Eligibility_Themes.csv")
    assert_file_exists(path)

    df = csv_to_dataframe(path)
    assert_has_rows(df)
    assert_column_count(df, 2)
    assert_column_count_is_consistent(path)

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
    # duplicates handled by summing

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
    assert_fiscal_year_found(df, 0)
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
