"""
This file contains all the test fixtures and mock setup we need for testing
the data processing modules. I'm using pytest fixtures to avoid repeating
setup code across different test files.
"""
import os
import sys
import pytest
import pandas as pd
import sqlite3

# Project root to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Making sure config is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_processing')))

# Import modules for patching
import config

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def mock_csv_data(tmp_path):
    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()

    all_programs = extracted_dir / "MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw.csv"
    program_data_raw = extracted_dir / "MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw.csv"
    agency_data_raw = extracted_dir / "MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw.csv"
    ip_agency_pocs = extracted_dir / "IP_Agency_POCs.csv"
    principal_table_columns = extracted_dir / "MY_OMB_ImproperPayment_Payment_Accuracy_Principal_Table_Columns_vw.csv"
    payment_recovery_details = extracted_dir / "MY_OMB_ImproperPayment_Payment_Recovery_Details_unpivotted_vw.csv"
    payment_confirmed_fraud = extracted_dir / "MY_OMB_ImproperPayment_Payment_Confirmed_Fraud_vw.csv"
    eligibility_themes = extracted_dir / "Eligibility_Themes.csv"
    risks = extracted_dir / "MY_OMB_ImproperPayment_Payment_Risk_Assessments_vw.csv"
    new_risks = extracted_dir / "MY_OMB_ImproperPayment_Payment_New_Risk_Assessments_vw.csv"
    recovery_amounts = extracted_dir / "MY_OMB_ImproperPayment_Payment_Accuracy_Rate_and_Amt_of_Recovery_vw.csv"
    program_compliance = extracted_dir / "MY_OMB_ImproperPayment_Payment_Program_Compliance_vw.csv"
    survey_root_cause = extracted_dir / "KPI_ImproperPaymentSurveyRootCause_vw_IP.csv"
    ip_root_causes = extracted_dir / "MY_OMB_ImproperPayment_Payment_IP_Root_Causes_vw.csv"
    congressional_reports = extracted_dir / "MY_OMB_ImproperPayment_PaymentAccuracy_AgencyData_raw_vw-Congressional.csv"

    all_programs_sample_csv_data = (
        "Agency,Program_Name,Fiscal_Year,Outlays_($M),IP_Amount($M),IP_Unknown_Amount_($M)"
        "\nA,Program_Name_1,2022,100000,10000,1000"
        "\nB,Program_Name_2,2022,200000,20000,2000"
        "\nC,Program_Name_3,2022,300000,30000,3000"
    )

    program_data_raw_sample_csv_data = (
        "agency,Program Name,key,value,title,Fiscal_Year"
        "\nA,Program_Name_1,key_1,value_1,title_1,2022"
        "\nB,Program_Name_2,key_2,value_2,title_2,2023"
        "\nC,Program_Name_3,key_3,value_3,title_3,2024"
    )

    agency_data_raw_sample_csv_data = (
        "agency,Key,Title,value,Fiscal_Year"
        "\nA,key_1,title_1,value_1,2022"
        "\nB,key_2,title_2,value_2,2023"
        "\nC,key_3,title_3,value_3,2024"
    )

    ip_agency_pocs_sample_csv_data = (
        "Agency_Acronym,Agency_Name,Fiscal_Year"
        "\nA,Agency1,2024"
        "\nB,Agency2,2024"
        "\nC,Agency3,2024"
    )

    principal_table_columns_sample_csv_data = (
        "Fiscal_Year,Agency,Program_Name,Column_names,Column_values,Question,Section,Reporting_Phases_Current_FY"
        "\n2024,Agency1,Program1,cyp19,no,question1,section1,2024"
        "\n2024,Agency2,Program2,cyp19,yes,question2,section2,2024"
        "\n2023,Agency3,Program3,cyp19,no,question3,section3,2024"
    )

    payment_recovery_details_sample_csv_data = (
        "Agency,Program_Name,Fiscal_Year,key,value"
        "\nAgency1,Program1,2024,OP Amt Identified outside of Payment Recapture Audits,1"
        "\nAgency2,Program2,2024,OP Amt Identified outside of Payment Recapture Audits,2"
        "\nAgency3,Program3,2024,OP Amt Identified outside of Payment Recapture Audits,3"
    )

    payment_confirmed_fraud_sample_csv_data = (
        "Agency,Program_or_Activity,Confirmed_Fraud,Fiscal_Year"
        "\nAgency1,,1,2024"
        "\nAgency1,Program1,2,2024"
    )

    eligibility_themes_sample_csv_data = (
        "key,theme"
        "\ndit1,Address/Location"
        "\ndit10,Marital Status"
    )

    risks_sample_csv_data = (
        "Agency,Fiscal_Year,Program_Name,in_draft,Was_the_Program_or_Activity_Susceptible_to_Significant_Improper_,raa6_2,raa7_2,Updated_Program_Name,Original_Program_Name"
        "\nAgency1,2024,Program1,0.0,,,,Program1,Program1"
        "\nAgency1,2024,Program2,0.0,,Yes,No,Program2,Program2"
    )

    new_risks_sample_csv_data = (
        "Agency,Fiscal_Year,Program_Name,Gaa1,raa7,raa6"
        "\nAgency1,2024,Program1,No,,"
        "\nAgency1,2024,Program2,Yes,Yes,Yes"
    )

    recovery_amounts_sample_csv_data = (
        "Agency,Fiscal_Year,Overpayment_Amount_Identified_For_Recapture_($M),Overpayment_Amount_Recovered_($M),Recovery_Rate"
        "\nAgency1,2024,10,9,0.9"
        "\nAgency1,2024,0,0,"
    )

    program_compliance_sample_csv_data = (
        "Agency,Fiscal_Year,Program_Name,Agency_Compliance,pcp01_1,pcp2_2,pcp3_2,pcp4_2,pcp5_2,pcp6_2,pcp7_2,pcp8_2,pcp9_2,pcp10_2,pcp11_2,pcp12_1"
        "\nAgency1,2024,Program1,Compliant,Yes,Yes,Yes,Yes,Yes,Yes,Yes,Yes,Yes,Yes,Yes,"
        "\nAgency1,2024,Program2,Non-Compliant,No,Yes,Yes,Yes,Yes,No,Yes,Yes,Yes,Yes,Yes,3.0"
    )

    survey_root_cause_sample_csv_data = (
        "End Date,Recorded Date,Agency,Program Name,Please provide a brief 1-2 sentence high level description of yo,RootCauseNumber,RootCause,RootCauseDescription,RootCauseValue,MitigationStrategy,AnticipatedImpactMitigation,Provide a detailed description of the actions taken and planned,Quarter Year"
        "\nFeb 12 2024  4:37PM,Feb 12 2024  4:37PM,Agency1,Program1,Description1,RootCauseNum1,RootCause1,RootCauseDescription1,RootCauseValue1,MitigationStrategy1,AnticipatedImpactMitigation1,ActionsTakenPlanned1,Q1 2024"
        "\nFeb 12 2024  4:37PM,Feb 12 2024  4:37PM,Agency2,Program2,Description2,RootCauseNum2,RootCause2,RootCauseDescription2,RootCauseValue2,MitigationStrategy2,AnticipatedImpactMitigation2,ActionsTakenPlanned2,Q1 2024"
    )

    ip_root_causes_sample_csv_data = (
        "Agency,Program_Name,Fiscal_Year,Payment_Type,Program_Design_or_Structural_Issue,Inability_to_Authenticate_Eligibility,Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data,Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis,Insufficient_Documentation_to_Determine,Failure_to_Access_Data,Address_Location,Contractor_or_Provider_Status,Financial"
        "\nAgency1,Program_Name1,2024,Overpayments,Program_Design_or_Structural_Issue1,Inability_to_Authenticate_Eligibility1,Inability_to_Authenticate_Eligibility_Inability_to_Access_Data1,Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis1,Insufficient_Documentation_to_Determine1,Failure_to_Access_Data1,Address_Location1,Contractor_or_Provider_Status1,Financial1"
        "\nAgency2,Program_Name2,2024,Overpayments,Program_Design_or_Structural_Issue2,Inability_to_Authenticate_Eligibility2,Inability_to_Authenticate_Eligibility_Inability_to_Access_Data2,Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis2,Insufficient_Documentation_to_Determine2,Failure_to_Access_Data2,Address_Location2,Contractor_or_Provider_Status2,Financial2"
    )

    congressional_reports_sample_csv_data = (
        "agency,Key,Title,value,Fiscal_Year"
        "\nCFTC,raa6_1,[raa6_1]Did the agency perform any Improper Payment Risk Assessments for programs in Phase 1 in the current reporting period? (Unit - Yes/No),No,2023"
        "\nCFTC,raa6_1,[raa6_1]Did the agency perform any Improper Payment Risk Assessments for programs in Phase 1 in the current reporting period? (Unit - Yes/No),No,2024"
    )

    all_programs.write_text(all_programs_sample_csv_data, encoding="utf-8-sig")
    program_data_raw.write_text(program_data_raw_sample_csv_data, encoding="utf-8-sig")
    agency_data_raw.write_text(agency_data_raw_sample_csv_data, encoding="utf-8-sig")
    ip_agency_pocs.write_text(ip_agency_pocs_sample_csv_data, encoding="utf-8-sig")
    principal_table_columns.write_text(principal_table_columns_sample_csv_data, encoding="utf-8-sig")
    payment_recovery_details.write_text(payment_recovery_details_sample_csv_data, encoding="utf-8-sig")
    payment_confirmed_fraud.write_text(payment_confirmed_fraud_sample_csv_data, encoding="utf-8-sig")
    eligibility_themes.write_text(eligibility_themes_sample_csv_data, encoding="utf-8-sig")
    risks.write_text(risks_sample_csv_data, encoding="utf-8-sig")
    new_risks.write_text(new_risks_sample_csv_data, encoding="utf-8-sig")
    recovery_amounts.write_text(recovery_amounts_sample_csv_data, encoding="utf-8-sig")
    program_compliance.write_text(program_compliance_sample_csv_data, encoding="utf-8-sig")
    survey_root_cause.write_text(survey_root_cause_sample_csv_data, encoding="utf-8-sig")
    ip_root_causes.write_text(ip_root_causes_sample_csv_data, encoding="utf-8-sig")
    congressional_reports.write_text(congressional_reports_sample_csv_data, encoding="utf-8-sig")

    return {
        "ALL_PROGRAMS_DATA_PATH": str(all_programs),
        "PROGRAM_DATA_RAW_PATH": str(program_data_raw),
        "AGENCY_DATA_RAW_PATH": str(agency_data_raw),
        "IP_AGENCY_POCS_PATH": str(ip_agency_pocs),
        "PRINCIPAL_TABLE_COLUMNS_PATH": str(principal_table_columns),
        "PAYMENT_RECOVERY_DETAILS_PATH": str(payment_recovery_details),
        "PAYMENT_CONFIRMED_FRAUD_PATH": str(payment_confirmed_fraud),
        "ELIGIBILITY_THEMES_PATH": str(eligibility_themes),
        "RISKS_PATH": str(risks),
        "NEW_RISKS_PATH": str(new_risks),
        "RECOVERY_AMOUNTS_PATH": str(recovery_amounts),
        "PROGRAM_COMPLIANCE_PATH": str(program_compliance),
        "SURVEY_ROOT_CAUSE_PATH": str(survey_root_cause),
        "IP_ROOT_CAUSES_PATH": str(ip_root_causes),
        "CONGRESSIONAL_REPORTS_PATH": str(congressional_reports),
    }
