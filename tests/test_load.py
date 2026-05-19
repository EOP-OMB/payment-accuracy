import config
import os
import load
from load_tools import query
import pytest
import yaml
from unittest.mock import MagicMock, mock_open, patch

load.WEBSITE_DIR = "/tmp"
load.HOME_MARKUP_FILE_PATH = os.path.join(load.WEBSITE_DIR, "pages", "home.md")
load.AGENY_WIDE_FILE_PATH = os.path.join(load.WEBSITE_DIR, "pages", "agenciesPrograms.md")
load.AGENCY_SPECIFIC_DIR = os.path.join(load.WEBSITE_DIR, "pages", "agencies")
load.PROGRAM_SPECIFIC_DIR = os.path.join(load.WEBSITE_DIR, "pages", "programs")
load.CONGRESSIONAL_REPORTS_MARKUP_PATH = os.path.join(load.WEBSITE_DIR, "pages", "congressional_reports.md")
load.CONGRESSIONAL_REPORTS_DIR = os.path.join(load.WEBSITE_DIR, "pages", "congressional_reports")
load.SHARED_DATA_PATH = os.path.join(load.WEBSITE_DIR, "shared.yml")
load.CONGRESSIONAL_REPORTS_SHARED_DATA_PATH = os.path.join(load.WEBSITE_DIR, "congressional_reports.yml")

@pytest.fixture
def mock_cursor():
    return MagicMock()

@pytest.fixture
def fpi_output_file_data():
    return {
        "slugify_query": [
            {
                "Agency": "A1",
                "Program_Name": "Salaries & Expenses"
            },
            {
                "Agency": "A1",
                "Program_Name": "Plant and Animal Disease, Pest Control, and Animal Care"
            }
        ],
        "output_query": [
            {
                "program_id": "10.001",
                "improper_payment_program_name": "Salaries & Expenses",
                "agency": "AG1",
                "fiscal_year": 2025,
                "outlays": None,
                "improper_payment_amount": None,
                "start_date": "2021-04-01",
                "end_date": "2021-04-30",
                "insufficient_documentation_amount": None
            },
            {
                "program_id": "10.025",
                "improper_payment_program_name": "Plant and Animal Disease, Pest Control, and Animal Care",
                "agency": "AG2",
                "fiscal_year": 2021,
                "outlays": 2,
                "improper_payment_amount": 1,
                "start_date": "2022-05-01",
                "end_date": "2022-05-31",
                "insufficient_documentation_amount": 0
            }
        ]
    }

@pytest.fixture
def homepage_sample_data():
    return {
        "min_max_rates": [{
            "Payment_Accuracy_Rate_Min": 90.5,
            "Payment_Accuracy_Rate_Max": 98.3,
            "Improper_Payments_Rate_Min": 1.2,
            "Improper_Payments_Rate_Max": 5.6,
            "Unknown_Payments_Rate_Min": 0.3,
            "Unknown_Payments_Rate_Max": 0.9
        }],
        "highest_agencies": [
            {
                "Agency": "A1",
                "Agency_Name": "Agency 1",
                "High_Priority_Programs": 2,
                "Improper_Payments_Rate": 1.2
            },
            {
                "Agency": "A2",
                "Agency_Name": "Agency 2",
                "High_Priority_Programs": 1,
                "Improper_Payments_Rate": 2.3
            },
            {
                "Agency": "A3",
                "Agency_Name": "Agency 3",
                "High_Priority_Programs": 3,
                "Improper_Payments_Rate": 2.5
            }
        ],
        "lowest_agencies": [
            {
                "Agency": "B1",
                "Agency_Name": "Agency B1",
                "High_Priority_Programs": 4,
                "Improper_Payments_Rate": 25.1
            },
            {
                "Agency": "B2",
                "Agency_Name": "Agency B2",
                "High_Priority_Programs": 2,
                "Improper_Payments_Rate": 24.8
            },
            {
                "Agency": "B3",
                "Agency_Name": "Agency B3",
                "High_Priority_Programs": 1,
                "Improper_Payments_Rate": 23.3
            }
        ],
        "rate_datapoints": [
            {
                "Payment_Accuracy_Rate": 0.11,
                "Improper_Payments_Rate": 0.12,
                "Unknown_Payments_Rate": 0.13,
                "Fiscal_Year": 2022
            },
            {
                "Payment_Accuracy_Rate": 0.21,
                "Improper_Payments_Rate": 0.22,
                "Unknown_Payments_Rate": 0.23,
                "Fiscal_Year": 2023
            },
            {
                "Payment_Accuracy_Rate": 0.31,
                "Improper_Payments_Rate": 0.32,
                "Unknown_Payments_Rate": 0.33,
                "Fiscal_Year": 2024
            }
        ]
    }

def test_generate_fpi_output_file(mock_cursor, fpi_output_file_data):
    mock_cursor.fetchall.side_effect = [
        fpi_output_file_data['slugify_query'],
        fpi_output_file_data['output_query']
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            query.slugifyProgramNames(mock_cursor)
            load.generate_fpi_output_file(mock_cursor)

            mocked_file.assert_called_once_with(load.FPI_OUTPUT_FILE, 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            assert 'program_id,improper_payment_program_name,agency,fiscal_year,outlays,improper_payment_amount,start_date,end_date,insufficient_documentation_amount,slug' in written_content
            assert '10.001,Salaries & Expenses,AG1,2025,,,2021-04-01,2021-04-30,,' in written_content
            assert '10.025,"Plant and Animal Disease, Pest Control, and Animal Care",AG2,2021,2,1,2022-05-01,2022-05-31,0,' in written_content

def test_generate_home_page(mock_cursor, homepage_sample_data):
    mock_cursor.fetchall.side_effect = [
        homepage_sample_data["min_max_rates"],
        homepage_sample_data["highest_agencies"],
        homepage_sample_data["lowest_agencies"],
        homepage_sample_data["rate_datapoints"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            load.generate_home_page(mock_cursor)

            mocked_file.assert_called_once_with(load.HOME_MARKUP_FILE_PATH, 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            assert 'title: Home' in written_content
            assert 'layout: index' in written_content
            assert 'payment_accuracy_rate_min' in written_content
            assert 'payment_accuracy_rate_max' in written_content
            assert 'improper_payments_rate_min' in written_content
            assert 'improper_payments_rate_max' in written_content
            assert 'unknown_payments_rate_min' in written_content
            assert 'unknown_payments_rate_max' in written_content
            assert 'highest_performing_agencies' in written_content
            assert 'lowest_performing_agencies' in written_content
            assert 'payment_accuracy_rates' in written_content
            assert 'improper_payments_rates' in written_content
            assert 'unknown_payments_rates' in written_content

            mocked_makedirs.assert_called_once_with(
                os.path.dirname(load.HOME_MARKUP_FILE_PATH), exist_ok=True
            )

@pytest.fixture
def agency_programs_sample_data():
    return {
        "program_specific_data_points": [
            {
                "Agency": "A1",
                "Program_Name": "Program 1",
                "Total_Spent_Federal_Funding": 1200.12,
                "High_Priority_Program": 1,
                "IP_Rate": 1,
                "Relative_Change": 12.23
            },
            {
                "Agency": "A2",
                "Program_Name": "Program 2",
                "Total_Spent_Federal_Funding": 1300.13,
                "High_Priority_Program": 0,
                "IP_Rate": 1,
                "Relative_Change": 13.03
            },
            {
                "Agency": "A2",
                "Program_Name": "Program 3",
                "Total_Spent_Federal_Funding": 1300.13,
                "High_Priority_Program": 1,
                "IP_Rate": 0,
                "Relative_Change": 14.53
            }
        ],
        "agency_specific_data_points": [
            {
                "Agency": "A1",
                "Agency_Name": "Agency 1",
                "Total_Spent_Federal_Funding": 2400.12,
                "Num_Programs": 1,
                "Susceptible_Programs": 1,
                "High_Priority_Programs": 1,
                "Improper_Payments_Rate": 12.23,
                "Relative_Change": -3.2
            },
            {
                "Agency": "A2",
                "Agency_Name": "Agency 2",
                "Total_Spent_Federal_Funding": 2500.45,
                "Num_Programs": 2,
                "Susceptible_Programs": 1,
                "High_Priority_Programs": 1,
                "Improper_Payments_Rate": 2.03,
                "Relative_Change": 1.2
            }
        ],
        "programs_for_slugging": [
            {
                "Agency": "A1",
                "Program_Name": "Program 1"
            },
            {
                "Agency": "A2",
                "Program_Name": "Program 2"
            },
            {
                "Agency": "A2",
                "Program_Name": "Program 3"
            }
        ]
    }

@pytest.fixture
def agency_specific_sample_data():
    return {
        "agency_data_points": [
            {
                "Agency": "A1",
                "Agency_Name": "Agency 1",
                "Fiscal_Year": 2024,
                "High_Priority_Programs": 11,
                "IP_Amount": 12,
                "CY_Unknown_Payments": 13,
                "Outlays": 14,
                "Improper_Payments_Rate": 15,
                "Unknown_Payments_Rate": 16,
                "Payment_Accuracy_Rate": 17,
                "Num_Programs": 18,
                "Susceptible_Programs": 19,
                "Confirmed_Fraud": 20
            }
        ],
        "agency_data_years_available_A1": [
            {
                "Fiscal_Year": 2024
            }
        ],
        "agency_data_raw_data_points_A1": [
            {
                "agency": "A1",
                "Key": "key_1",
                "Name": "key_1",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "A1",
                "Key": "key_2",
                "Name": "key_2",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2024
            }
        ],
        "agency_data_recovery_data_points_A1": [
            {
                "Agency": "A1",
                "Program_Name": None,
                "Fiscal_Year": 2024,
                "key": "Aging of Outstanding OP Identified Amt 6 months to 1 year",
                "value": 2.2
            }
        ],
        "agency_data_recovery_amounts_A1": [
            {
                "Fiscal_Year": 2024,
                "Overpayment_Amount_Identified_For_Recapture_($M)": 10,
                "Overpayment_Amount_Recovered_($M)": 9
            },
            {
                "Fiscal_Year": 2023,
                "Overpayment_Amount_Identified_For_Recapture_($M)": 8,
                "Overpayment_Amount_Recovered_($M)": 7
            },
        ],
        "agency_rate_data_points_A1": [
            {
                "Payment_Accuracy_Rate": 0.11,
                "Improper_Payments_Rate": 0.12,
                "Unknown_Payments_Rate": 0.13,
                "Payment_Accuracy_Amount": 10,
                "Overpayment_Amount": 1,
                "Underpayment_Amount": 2,
                "Technically_Improper_Amount": 3,
                "Unknown_Amount": 5,
                "Fiscal_Year": 2022
            },
            {
                "Payment_Accuracy_Rate": 0.21,
                "Improper_Payments_Rate": 0.22,
                "Unknown_Payments_Rate": 0.23,
                "Payment_Accuracy_Amount": 9,
                "Overpayment_Amount": 1,
                "Underpayment_Amount": 2,
                "Technically_Improper_Amount": 3,
                "Unknown_Amount": 5,
                "Fiscal_Year": 2023
            },
            {
                "Payment_Accuracy_Rate": 0.31,
                "Improper_Payments_Rate": 0.32,
                "Unknown_Payments_Rate": 0.33,
                "Payment_Accuracy_Amount": 8,
                "Overpayment_Amount": 1,
                "Underpayment_Amount": 2,
                "Technically_Improper_Amount": 3,
                "Unknown_Amount": 5,
                "Fiscal_Year": 2024
            }
        ],
        "program_compliance_data_points_A1": [
            {
                "Program_Name": "program1",
                "pcp01_1": "Yes",
                "pcp2_2": "Yes",
                "pcp3_2": "Yes",
                "pcp4_2": "Yes",
                "pcp5_2": "Yes",
                "pcp6_2": "Yes",
                "pcp7_2": "Yes",
                "pcp8_2": "Yes",
                "pcp9_2": "Yes",
                "pcp10_2": "Yes",
                "pcp11_2": "Yes",
                "pcp12_1": None,
                "Hide_Compliance_Section": 0,
            },
            {
                "Program_Name": "program2",
                "pcp01_1": "No",
                "pcp2_2": "Yes",
                "pcp3_2": "Yes",
                "pcp4_2": "Yes",
                "pcp5_2": "Yes",
                "pcp6_2": "Yes",
                "pcp7_2": "No",
                "pcp8_2": "Yes",
                "pcp9_2": "Yes",
                "pcp10_2": "Yes",
                "pcp11_2": "Yes",
                "pcp12_1": 3.0,
                "Hide_Compliance_Section": 0,
            }
        ],
        "risks_data_points_A1": [
            {
                "Agency": "Agency1",
                "Fiscal_Year": 2024,
                "Program_Name": "program1",
                "Susceptible": "Yes",
                "MethodologyChanged": 0
            },
            {
                "Agency": "Agency1",
                "Fiscal_Year": 2022,
                "Program_Name": "program2",
                "Susceptible": "Yes",
                "MethodologyChanged": 0
            }
        ],
        "eligibility_themes_data_points_A1": [
            {
                "Program Name": "program1",
                "theme": "Financial",
                "Barriers": "barriers1",
                "Info": "info1"
            },
            {
                "Program Name": "program1",
                "theme": "Military Status",
                "Barriers": "barriers2",
                "Info": "info2"
            },
            {
                "Program Name": "program2",
                "theme": "Financial",
                "Barriers": "barriers3",
                "Info": "info3"
            }
        ],
        "agency_stats_A1": {
            "Payment_Accuracy_Rate_Min": 0,
            "Payment_Accuracy_Rate_Max": 100,
            "Improper_Payments_Rate_Min": 25,
            "Improper_Payments_Rate_Max": 75,
            "Unknown_Payments_Rate_Min": 50,
            "Unknown_Payments_Rate_Max": 50
        }
    }

@pytest.fixture
def program_specific_sample_data():
    return {
        "all_agency_program_names": [
            {
                "Agency": "A1",
                "Program_Name": "Program 1"
            }
        ],
        "program_survey_details": [],
        "program_fpi_links": [
            {
                "Assistance Listing Number": "11.000"
            }
        ],
        "program_data_points": [
            {
                "Agency": "A1",
                "Agency_Name": "Agency 1",
                "Program_Name": "Program 1",
                "High_Priority_Program": 1,
                "Phase_2_Program": 1,
                "Outlays": 1000,
                "Payment_Accuracy_Rate": 98,
                "Description": "Description 1"
            }
        ],
        "program_chart_data_points_A1": [
            {
                "Payment_Accuracy_Amount": 1200,
                "Overpayment_Amount": 100,
                "Underpayment_Amount": 29,
                "Technically_Improper_Amount": 38,
                "Unknown_Amount": 8,
                "Fiscal_Year": 2024
            },
            {
                "Payment_Accuracy_Amount": 1483,
                "Overpayment_Amount": 456,
                "Underpayment_Amount": 32,
                "Technically_Improper_Amount": 12,
                "Unknown_Amount": 6,
                "Fiscal_Year": 2023
            }
        ],
        "program_improper_payment_estimates_data_points": [
            {
                "Fiscal_Year": 2023,
                "Payment_Accuracy_Rate": 97,
                "IP_Rate": 3,
                "Unknown_Payments_Rate": 2,
                "Start_Date": "2023-01-01",
                "End_Date": "2023-12-31",
                "CY_Confidence_Level": ">90%",
                "CY_Margin_of_Error": "+/-1.23",
                "Outlays": 2000
            },
            {
                "Fiscal_Year": 2024,
                "Payment_Accuracy_Rate": 86,
                "IP_Rate": 5,
                "Unknown_Payments_Rate": 7,
                "Start_Date": "2024-01-01",
                "End_Date": "2024-12-31",
                "CY_Confidence_Level": ">82%",
                "CY_Margin_of_Error": "+/-4.34",
                "Outlays": 1000
            }
        ],
        "program_actions_data_points_2023": [
            {
                "Fiscal_Year": 2023,
                "Agency": "A1",
                "Program_Name": "Program 1",
                "Mitigation_Strategy": "Mitigation Strategy 1",
                "Description_Action_Taken": "Description Action Taken 1",
                "Action_Taken": "Action Taken 1",
                "Completion_Date": "FY2028+",
                "Action_Type": "Automation"
            }
        ],
        "program_actions_data_points_2024": [
            {
                "Fiscal_Year": 2024,
                "Agency": "A1",
                "Program_Name": "Program 1",
                "Mitigation_Strategy": "Mitigation Strategy 2",
                "Description_Action_Taken": "Description Action Taken 2",
                "Action_Taken": "Action Taken 2",
                "Completion_Date": "FY2028+",
                "Action_Type": "Automation"
            }
        ],
        "visibility_data_points": [{
            "Fiscal_Year": 2024,
            "Program_Name": "Program 1",
            "Column_values" : "cyp6 value1",
            "Name": "Technical_IP_Amount",
            "Column_names" : "cyp6"
        }],
        "program_overpayments_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Overpayments_Within_Control_Why" : "cyp2_1 value1",
                "Overpayments_Within_Control_Amount" : "cyp2 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value11",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value12",
                "Failure_to_Access_Data": "Value13",
                "Address_Location": "Value14",
                "Contractor_or_Provider_Status": "Value15",
                "Financial": "Value16",
                "Overpayment_Mitigations_Taken": "Value17",
                "Overpayment_Mitigations_Planned": "Value18",
                "Overpayment_Combined_Mitigations_Taken": "Value19",
                "Overpayment_Combined_Mitigations_Planned": "Value19b"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Overpayments_Within_Control_Why" : "cyp2_1 value2",
                "Overpayments_Within_Control_Amount" : "cyp2 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value21",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value22",
                "Failure_to_Access_Data": "Value23",
                "Address_Location": "Value24",
                "Contractor_or_Provider_Status": "Value25",
                "Financial": "Value26",
                "Overpayment_Mitigations_Taken": "Value27",
                "Overpayment_Mitigations_Planned": "Value28",
                "Overpayment_Combined_Mitigations_Taken": "Value29",
                "Overpayment_Combined_Mitigations_Planned": "Value30"
            }
        ],
        "program_overpayments_outside_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Overpayments_Outside_Control_Amount" : "cyp3 value1",
                "Overpayments_Outside_Control_Why" : "cyp4_1 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value11",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value12",
                "Failure_to_Access_Data": "Value13",
                "Address_Location": "Value14",
                "Contractor_or_Provider_Status": "Value15",
                "Financial": "Value16"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Overpayments_Outside_Control_Amount" : "cyp3 value1",
                "Overpayments_Outside_Control_Why" : "cyp4_1 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value21",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value22",
                "Failure_to_Access_Data": "Value23",
                "Address_Location": "Value24",
                "Contractor_or_Provider_Status": "Value25",
                "Financial": "Value26"
            }
        ],
        "program_underpayments_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value11",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value12",
                "Failure_to_Access_Data": "Value13",
                "Address_Location": "Value14",
                "Contractor_or_Provider_Status": "Value15",
                "Financial": "Value16",
                "Underpayment_Mitigations_Taken" : "Value17",
                "Underpayment_Mitigations_Planned": "Value18",
                "Underpayments_Amount": "Value18a"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value21",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value22",
                "Failure_to_Access_Data": "Value23",
                "Address_Location": "Value24",
                "Contractor_or_Provider_Status": "Value25",
                "Financial": "Value26",
                "Underpayment_Mitigations_Taken" : "Value27",
                "Underpayment_Mitigations_Planned": "Value28",
                "Underpayments_Amount": "Value18a"
            }
        ],
        "program_technically_ip_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Technical_IP_Amount": "Value1",
                "Technical_IP_Causes": "Value11",
                "Program_Design_or_Structural_Issue": "Value12",
                "Technical_IP_Actions_Taken": "Value13",
                "Technical_IP_Actions_Planned": "Value14"
            },
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Technical_IP_Amount": "Value1",
                "Technical_IP_Causes": "Value11",
                "Program_Design_or_Structural_Issue": "Value12",
                "Technical_IP_Actions_Taken": "Value15",
                "Technical_IP_Actions_Planned": "Value16"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Technical_IP_Amount": "Value1",
                "Technical_IP_Causes": "Value21",
                "Program_Design_or_Structural_Issue": "Value22",
                "Technical_IP_Actions_Taken": "Value23",
                "Technical_IP_Actions_Planned": "Value24"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Technical_IP_Amount": "Value1",
                "Technical_IP_Causes": "Value21",
                "Program_Design_or_Structural_Issue": "Value22",
                "Technical_IP_Actions_Taken": "Value25",
                "Technical_IP_Actions_Planned": "Value26"
            }
        ],
        "program_eligibility_information_data_points": [{
            "Column_names": "cyp5_dit5_1",
            "Column_values": "4.10",
            "theme": "Address",
            "description": "The address",
            "Payment_Type": "Underpayments",
            "Fiscal_Year": 2024
        }],
        "program_eligibility_information_aggregated_data_points": [],
        "program_unknown_payments_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Unknown_Why": "Value11",
                "Insufficient_Documentation_to_Determine": "Value12",
                "Unknown_Documentation_Why": "Value13",
                "Unknown_Mitigations_Taken": "Value14",
                "Unknown_Mitigations_Planned": "Value15",
                "Non_Monetary_Loss_Amount": "cyp26"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Unknown_Why": "Value21",
                "Insufficient_Documentation_to_Determine": "Value12",
                "Unknown_Documentation_Why": "Value23",
                "Unknown_Mitigations_Taken": "Value24",
                "Unknown_Mitigations_Planned": "Value25",
                "Non_Monetary_Loss_Amount": "cyp26"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Unknown_Why": "Value21",
                "Insufficient_Documentation_to_Determine": "Value12",
                "Unknown_Documentation_Why": "Value23",
                "Unknown_Mitigations_Taken": "Value26",
                "Unknown_Mitigations_Planned": "Value27",
                "Non_Monetary_Loss_Amount": "cyp26"
            }
        ],
        "program_unknown_payments_breakdown_data_points": [
            {
                "Fiscal_Year": 2023,
                "Column_names": "cyp7_ucp3",
                "Name": "Unknown_Due_To_States_Amount",
                "Column_values": "4"
            }
        ],
        "program_corrective_actions_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Corrective_Actions_Proportion": "Value11",
                "Corrective_Actions_Adequacy": "Value12",
                "Corrective_Actions_Association": "Value13",
                "Corrective_Actions_Implementation": "Value14",
                "Corrective_Actions_Appropriateness": "Value15",
                "Corrective_Actions_Adequacy_Association_Implementation": "Value26"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Corrective_Actions_Proportion": "Value21",
                "Corrective_Actions_Adequacy": "Value22",
                "Corrective_Actions_Association": "Value23",
                "Corrective_Actions_Implementation": "Value24",
                "Corrective_Actions_Appropriateness": "Value25",
                "Corrective_Actions_Adequacy_Association_Implementation": "Value26"
            }
        ],
        "program_future_outlook_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Future_Outlook_Has_Baseline" : "Value11",
                "Future_Outlook_Reduction_Vs_Estimated": "Value12",
                "IP_And_Unknown_Rate": "Value12_29",
                "Is_Tolerable_Why": "Value13_1",
                "Tolerable_Rate_Not_Determined_Reason": "Value13",
                "Is_Not_Tolerable_Why": "Value13_3",
                "Is_Lowest_IP_And_Unknown_Rate": "Value13a",
                "Agency_Needs_Satisfied": "Value14",
                "Resources_Requested_For_IP": "Value15",
                "Outlays_Current_Year+1_Amount": "Value16",
                "IP_Current_Year+1_Amount": "Value17",
                "Unknown_Curent_Year+1_Amount": "Value18",
                "IP_Unknown_Current_Year+1_Rate": "Value19",
                "IP_Unknown_Target_Rate": "Value111"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Future_Outlook_Has_Baseline" : "Value21",
                "Future_Outlook_Reduction_Vs_Estimated": "Value22",
                "IP_And_Unknown_Rate": "Value22_29",
                "Is_Tolerable_Why": "Value23_1",
                "Tolerable_Rate_Not_Determined_Reason": "Value23",
                "Is_Not_Tolerable_Why": "Value23_3",
                "Is_Lowest_IP_And_Unknown_Rate": "Value23a",
                "Agency_Needs_Satisfied": "Value24",
                "Resources_Requested_For_IP": "Value25",
                "Outlays_Current_Year+1_Amount": "Value26",
                "IP_Current_Year+1_Amount": "Value27",
                "Unknown_Curent_Year+1_Amount": "Value28",
                "IP_Unknown_Current_Year+1_Rate": "Value29",
                "IP_Unknown_Target_Rate": "Value211"
            }
        ],
        "program_additional_information_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Program_Additional_Information": "Value11",
                "IP_Accountability_Description": "Value12"
            },
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "Program_Additional_Information": "Value13",
                "IP_Accountability_Description": "Value12"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "Program_Additional_Information": "Value21",
                "IP_Accountability_Description": "Value22"
            }
        ],
        "did_not_report_programs": [],
        "scorecard_links": [
            {
                "QuarterYear": "Q1 2024",
                "Link": "example_link",
            }
        ]
    }

@pytest.fixture
def congressional_reports_sample_data():
    return {
        "agency_names": [
            {
                "Agency_Acronym": "AG1",
                "Agency_Name": "Agency 1"
            },
            {
                "Agency_Acronym": "AG2",
                "Agency_Name": "Agency 2"
            }
        ],
        "agencies_with_data": [
            {
                "agency": "AG1"
            },
            {
                "agency": "AG2"
            }
        ],
        "agency_names_2": [
            {
                "Agency_Acronym": "AG1",
                "Agency_Name": "Agency 1"
            },
            {
                "Agency_Acronym": "AG2",
                "Agency_Name": "Agency 2"
            }
        ],
        "report_results_2023": [
            {
                "Agency": "AG1",
                "Fiscal_Year": 2023,
                "Key": "key1",
                "Name": "key1",
                "Question": "question1",
                "Answer": "answer1_2023",
                "SortOrder": 0
            },
            {
                "Agency": "AG2",
                "Fiscal_Year": 2023,
                "Key": "key1",
                "Name": "key1",
                "Question": "question1",
                "Answer": "answer1a_2023",
                "SortOrder": 0
            }
        ],
        "risks_2023_AG1": [{
            "Agency": "AG1",
            "Fiscal_Year": 2023,
            "Program_Name": "PR1",
            "Susceptible": "No",
            "MethodologyChanged": 0
        }],
        "AG1_raw_data_points_2023": [
            {
                "agency": "AG1",
                "Key": "raa9",
                "Name": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2023
            },
            {
                "agency": "AG1",
                "Key": "raa8",
                "Name": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2023
            }
        ],
        "risks_2023_AG2": [{
            "Agency": "AG2",
            "Fiscal_Year": 2023,
            "Program_Name": "PR2",
            "Susceptible": "No",
            "MethodologyChanged": 0
        }],
        "AG2_raw_data_points_2023": [
            {
                "agency": "AG2",
                "Key": "raa9",
                "Name": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2023
            },
            {
                "agency": "AG2",
                "Key": "raa8",
                "Name": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2023
            }
        ],
        "report_results_2024": [
            {
                "Agency": "AG1",
                "Fiscal_Year": 2024,
                "Key": "key1",
                "Name": "key1",
                "Question": "question1",
                "Answer": "answer1_2024",
                "SortOrder": 0
            },
            {
                "Agency": "AG2",
                "Fiscal_Year": 2024,
                "Key": "key2",
                "Name": "key2",
                "Question": "question2",
                "Answer": "answer2_2024",
                "SortOrder": 0
            }
        ],
        "risks_2024_AG1": [{
            "Agency": "AG1",
            "Fiscal_Year": 2024,
            "Program_Name": "PR1",
            "Susceptible": "No",
            "MethodologyChanged": 0
        }],
        "AG1_raw_data_points_2024": [
            {
                "agency": "AG1",
                "Key": "raa9",
                "Name": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "A1",
                "Key": "raa8",
                "Name": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2024
            }
        ],
        "risks_2024_AG2": [{
            "Agency": "AG2",
            "Fiscal_Year": 2024,
            "Program_Name": "PR2",
            "Susceptible": "No",
            "MethodologyChanged": 0
        }],
        "AG2_raw_data_points_2024": [
            {
                "agency": "AG2",
                "Key": "raa9",
                "Name": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "AG2",
                "Key": "raa8",
                "Name": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2024
            }
        ]
    }

def test_generate_agency_programs_page(mock_cursor, agency_programs_sample_data):
    mock_cursor.fetchall.side_effect = [
        agency_programs_sample_data["programs_for_slugging"],
        agency_programs_sample_data["program_specific_data_points"],
        agency_programs_sample_data["agency_specific_data_points"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            query.slugifyProgramNames(mock_cursor)
            load.generate_agency_programs_page(mock_cursor)

            mocked_file.assert_called_once_with(load.AGENY_WIDE_FILE_PATH, 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            yaml_data = yaml.safe_load(written_content.strip("---\n"))

            assert yaml_data["title"] == "Agencies & Programs"
            assert len(yaml_data["agencies"]) == 2
            assert yaml_data["agencies"][0]["agency"] == "A1"
            assert yaml_data["agencies"][1]["agency"] == "A2"
            assert len(yaml_data["agencies"][0]["programs"]) == 1
            assert len(yaml_data["agencies"][1]["programs"]) == 2
            assert yaml_data["agencies"][0]["programs"][0]["program_name"] == "Program 1"
            assert yaml_data["agencies"][1]["programs"][0]["program_name"] == "Program 2"
            assert yaml_data["agencies"][1]["programs"][1]["program_name"] == "Program 3"

            mocked_makedirs.assert_called_once_with(
                os.path.dirname(load.AGENY_WIDE_FILE_PATH), exist_ok=True
            )

def test_generate_agency_specific_pages(mock_cursor, agency_specific_sample_data):
    config.FISCAL_YEAR = 2024

    mock_cursor.fetchall.side_effect = [
        agency_specific_sample_data["agency_data_points"],
        agency_specific_sample_data["agency_data_years_available_A1"],
        agency_specific_sample_data["agency_data_raw_data_points_A1"],
        agency_specific_sample_data["agency_data_recovery_data_points_A1"],
        agency_specific_sample_data["agency_data_recovery_amounts_A1"],
        agency_specific_sample_data["agency_rate_data_points_A1"],
        agency_specific_sample_data["program_compliance_data_points_A1"],
        agency_specific_sample_data["risks_data_points_A1"],
        agency_specific_sample_data["eligibility_themes_data_points_A1"]
    ]

    mock_cursor.fetchone.side_effect = [
        agency_specific_sample_data["agency_stats_A1"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED = 1
            load.generate_agency_specific_pages(mock_cursor)

            mocked_file.assert_any_call(os.path.join(load.AGENCY_SPECIFIC_DIR, "A1.md"), 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            yaml_data = next(yaml.safe_load_all(written_content.strip("---\n")))

            assert yaml_data["Agency"] == "A1"
            assert yaml_data["detail_key_1"] == "value_1"
            assert yaml_data["detail_key_2"] == "value_2"
            assert yaml_data["Unknown_Payments_Rate_Max"] == 0.3
            assert yaml_data["recovery_Aging_of_Outstanding_OP_Identified_Amt_6_months_to_1_year"] == 2.2
            assert yaml_data["Confirmed_Fraud"] == 20
            assert "0.11" in yaml_data["Payment_Accuracy_Rates"]
            assert "," in yaml_data["Overpayment_Amounts_Identified"]
            assert "8" in yaml_data["Overpayment_Amounts_Identified"]
            assert len(yaml_data["PIIA2019_Compliant_Programs"]) == 1
            assert yaml_data["PIIA2019_Compliant_Programs"][0]["Name"] == "program1"
            assert len(yaml_data["PIIA2019_NonCompliant_Programs"]) == 1
            assert len(yaml_data["Risks"]["Assessments"]) == 2
            assert yaml_data["Risks"]["Assessments"][1]["Fiscal_Year"] == 2022
            assert len(yaml_data["Eligibility_Themes"]) == 2
            assert len(yaml_data["Eligibility_Themes"][0]["Themes"]) == 2
            assert len(yaml_data["Eligibility_Themes"][1]["Themes"]) == 1
            assert yaml_data["Eligibility_Themes"][1]["Themes"][0]["Barriers"] == "barriers3"
            assert not yaml_data["Is_Placeholder"]

def test_generate_program_specific_pages(mock_cursor, program_specific_sample_data):
    config.COUNT_PROGRAM_SPECIFIC_YEARS_DISPLAYED = 2
    config.FISCAL_YEAR = 2024

    mock_cursor.fetchall.side_effect = [
        program_specific_sample_data["all_agency_program_names"],
        program_specific_sample_data["program_data_points"],
        program_specific_sample_data["program_fpi_links"],
        program_specific_sample_data["program_chart_data_points_A1"],
        program_specific_sample_data["program_improper_payment_estimates_data_points"],
        program_specific_sample_data["program_survey_details"],
        program_specific_sample_data["program_survey_details"],
        program_specific_sample_data["program_actions_data_points_2023"],
        program_specific_sample_data["program_actions_data_points_2024"],
        program_specific_sample_data["visibility_data_points"],
        program_specific_sample_data["program_overpayments_data_points"],
        program_specific_sample_data["program_overpayments_outside_data_points"],
        program_specific_sample_data["program_underpayments_data_points"],
        program_specific_sample_data["program_technically_ip_data_points"],
        program_specific_sample_data["program_eligibility_information_data_points"],
        program_specific_sample_data["program_eligibility_information_aggregated_data_points"],
        program_specific_sample_data["program_unknown_payments_data_points"],
        program_specific_sample_data["program_unknown_payments_breakdown_data_points"],
        program_specific_sample_data["program_corrective_actions_data_points"],
        program_specific_sample_data["program_future_outlook_data_points"],
        program_specific_sample_data["program_additional_information_data_points"],
        program_specific_sample_data["did_not_report_programs"],
        program_specific_sample_data["did_not_report_programs"],
        program_specific_sample_data["scorecard_links"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            query.slugifyProgramNames(mock_cursor)
            load.generate_program_specific_pages(mock_cursor)

            mocked_file.assert_called_once_with(os.path.join(load.PROGRAM_SPECIFIC_DIR, "a1-program-1.md"), 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            yaml_data = yaml.safe_load(written_content.strip("---\n"))

            yaml_data = yaml.safe_load(written_content.strip("---\n"))

            assert yaml_data["Agency"] == "A1"
            assert yaml_data["Agency_Name"] == "Agency 1"
            assert yaml_data["Program_Name"] == "Program 1"
            assert yaml_data["High_Priority_Program"] == 1
            assert yaml_data["Description"] == "Description 1"
            assert yaml_data["Payment_Accuracy_Amounts"] == "[1200, 1483]"
            assert yaml_data["Overpayment_Amounts"] == "[100, 456]"
            assert yaml_data["Underpayment_Amounts"] == "[29, 32]"
            assert yaml_data["Technically_Improper_Amounts"] == "[38, 12]"
            assert yaml_data["Unknown_Amounts"] == "[8, 6]"
            assert len(yaml_data["Scorecard_Links"]) == 1
            for year_data in yaml_data["Data_By_Year"]:
                if year_data.get("Year") == 2023:
                    assert year_data["Outlays"] == 2000
                    assert year_data["Improper_Payments_Rate"] == 3
                    assert year_data["Payment_Accuracy_Rate"] == 97
                    assert year_data["Actions_Taken"][0]["Action_Taken"] == "Action Taken 1"
                    assert year_data["Actions_Taken"][0]["Description_Action_Taken"] == "Description Action Taken 1"
                    assert year_data["overpayments"]["Address_Location"] == "Value14"
                    assert year_data["underpayments"]["Contractor_Provider_Status"] == "Value15"
                    assert year_data["Program_Design_or_Structural_Issue"] == "Value12"
                    assert year_data["Technical_IP_Actions_Planned"] == "Value16"
                    assert year_data["Insufficient_Documentation_to_Determine"] == "Value12"
                    assert year_data["Unknown_Why"] == "Value11"
                    assert year_data["Corrective_Actions_Proportion"] == "Value11"
                    assert year_data["Corrective_Actions_Adequacy"] == "Value12"
                    assert year_data["Outlays_Current_Year_Plus_1_Amount"] == "Value16"
                    assert year_data["IP_Current_Year_Plus_1_Amount"] == "Value17"
                    assert "Program_Additional_Information" not in year_data
                    assert year_data["IP_Accountability_Description"] == "Value12"
                elif year_data.get("Year") == 2024:
                    assert year_data["Outlays"] == 1000
                    assert year_data["Improper_Payments_Rate"] == 5
                    assert year_data["Payment_Accuracy_Rate"] == 86
                    assert year_data["Actions_Taken"][0]["Action_Taken"] == "Action Taken 2"
                    assert year_data["Actions_Taken"][0]["Description_Action_Taken"] == "Description Action Taken 2"
                    assert year_data["overpayments"]["Failure_to_Access_Data"] == "Value23"
                    assert year_data["Technical_IP_Actions_Taken"] == "Value25"
                    assert year_data["Technical_IP_Actions_Planned"] == "Value26"
                    assert year_data["Technical_IP_Causes"] == "Value21"
                    assert year_data["Unknown_Mitigations_Planned"] == "Value27"
                    assert year_data["Unknown_Mitigations_Taken"] == "Value26"
                    assert year_data["Corrective_Actions_Association"] == "Value23"
                    assert year_data["Corrective_Actions_Implementation"] == "Value24"
                    assert year_data["IP_Unknown_Current_Year_Plus_1_Rate"] == "Value29"
                    assert year_data["Unknown_Curent_Year_Plus_1_Amount"] == "Value28"
                    assert year_data["Program_Additional_Information"] == "Value21"
                    assert year_data["IP_Accountability_Description"] == "Value22"

def test_generate_congressional_reports_pages(mock_cursor, congressional_reports_sample_data):
    config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED = 2
    config.FISCAL_YEAR = 2024

    mock_cursor.fetchall.side_effect = [
        congressional_reports_sample_data["agency_names"],
        congressional_reports_sample_data["agencies_with_data"],
        congressional_reports_sample_data["agency_names_2"],
        congressional_reports_sample_data["report_results_2023"],
        congressional_reports_sample_data["risks_2023_AG1"],
        congressional_reports_sample_data["AG1_raw_data_points_2023"],
        congressional_reports_sample_data["risks_2023_AG2"],
        congressional_reports_sample_data["AG2_raw_data_points_2023"],
        congressional_reports_sample_data["report_results_2024"],
        congressional_reports_sample_data["risks_2024_AG1"],
        congressional_reports_sample_data["AG1_raw_data_points_2024"],
        congressional_reports_sample_data["risks_2024_AG2"],
        congressional_reports_sample_data["AG2_raw_data_points_2024"]
    ]

    config.CONGRESSIONAL_REPORTS = [
        {
            "Id": 1,
            "Name": "Agency Risk Assessments Report",
            "SurveyName": "Survey Responses",
            "IsGovernmentWide": False
        }
    ]

    config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING = {
        "2023": {
            "1": [
                {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": "",
                    "key": "key1"
                }
            ]
        },
        "2024": {
            "1": [
                {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": "",
                    "key": "key1"
                },
                {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": "",
                    "key": "key2"
                }
            ]
        }
    }

    config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING = [
        {
            "Year": 2023,
            "AgencyReports": {
                "1": "example_view"
            },
            "ProgramReports": {}
        },
        {
            "Year": 2024,
            "AgencyReports": {
                "1": "example_view"
            },
            "ProgramReports": {}
        }
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            load.generate_congressional_reports_pages(mock_cursor)

            mocked_file.assert_called_with(load.CONGRESSIONAL_REPORTS_SHARED_DATA_PATH, 'w', encoding='utf-8')
            handle = mocked_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)

            # calls don't store the file that was written to, so testing for the existence of different strings

            # last report page written
            assert "title: Agency Risk Assessments Report" in written_content
            assert "permalink: /resources/congressional-reports/2024_AG2_1" in written_content
            assert "Years_Dropdown:" in written_content
            assert "SurveyData:" in written_content
            assert "Answer: answer2_2024" in written_content
            assert "Agency_Name: Agency 2" in written_content

            # first report page written
            assert "permalink: /resources/congressional-reports/2023_AG1_1" in written_content
            assert "Answer: answer1_2023" in written_content
            assert "Agency_Name: Agency 1" in written_content

            # landing page file
            assert "title: Congressional Reports" in written_content