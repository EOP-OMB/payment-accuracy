import config
import os
import pytest
import yaml
import load
from unittest.mock import MagicMock, mock_open, patch

@pytest.fixture
def mock_cursor():
    return MagicMock()

@pytest.fixture
def homepage_sample_data():
    return {
        "min_max_rates": (90.5, 98.3, 1.2, 5.6, 0.3, 0.9),
        "highest_agencies": [
            ("A1", "Agency 1", 2, 1.2),
            ("A2", "Agency 2", 1, 2.3),
            ("A3", "Agency 3", 3, 2.5),
        ],
        "lowest_agencies": [
            ("B1", "Agency B1", 4, 25.1),
            ("B2", "Agency B2", 2, 24.8),
            ("B3", "Agency B3", 1, 23.3),
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

def test_generate_home_page(mock_cursor, homepage_sample_data):
    mock_cursor.fetchone.return_value = homepage_sample_data["min_max_rates"]
    mock_cursor.description = [
        ("Agency",), ("Agency_Name",), ("High_Priority_Programs",), ("Improper_Payments_Rate",)
    ]
    mock_cursor.fetchall.side_effect = [
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
            ("A1", "Program 1", 1200.12, 1, 1, 12.23, -3.2),
            ("A2", "Program 2", 1300.13, 0, 1, 13.03, 1.2),
            ("A2", "Program 3", 1300.13, 1, 0, 14.53, None)
        ],
        "agency_specific_data_points": [
            ("A1", "Agency 1", 2400.12, 1, 1, 1, 12.23, -3.2),
            ("A2", "Agency 2", 2500.45, 2, 1, 1, 2.03, 1.2),
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
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "A1",
                "Key": "key_2",
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
            }
        ],
        "risks_data_points_A1": [
            {
                "Agency": "Agency1",
                "Fiscal_Year": 2024,
                "Program_Name": "program1",
                "Susceptible": "Yes"
            },
            {
                "Agency": "Agency1",
                "Fiscal_Year": 2022,
                "Program_Name": "program2",
                "Susceptible": "Yes"
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
                "CY_Margin_of_Error": "+/-1.23"
            },
            {
                "Fiscal_Year": 2024,
                "Payment_Accuracy_Rate": 86,
                "IP_Rate": 5,
                "Unknown_Payments_Rate": 7,
                "Start_Date": "2024-01-01",
                "End_Date": "2024-12-31",
                "CY_Confidence_Level": ">82%",
                "CY_Margin_of_Error": "+/-4.34"
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
            "Column_names" : "cyp6"
        }],
        "program_overpayments_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp2_1" : "cyp2_1 value1",
                "cyp2" : "cyp2 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value11",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value12",
                "Failure_to_Access_Data": "Value13",
                "Address_Location": "Value14",
                "Contractor_or_Provider_Status": "Value15",
                "Financial": "Value16",
                "cyp2_atp1_8": "Value17",
                "cyp2_app1_8": "Value18"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp2_1" : "cyp2_1 value2",
                "cyp2" : "cyp2 value1",
                "Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis": "Value21",
                "Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data": "Value22",
                "Failure_to_Access_Data": "Value23",
                "Address_Location": "Value24",
                "Contractor_or_Provider_Status": "Value25",
                "Financial": "Value26",
                "cyp2_atp1_8": "Value27",
                "cyp2_app1_8": "Value28"
            }
        ],
        "program_overpayments_outside_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp3" : "cyp3 value1",
                "cyp4_1" : "cyp4_1 value1",
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
                "cyp3" : "cyp3 value1",
                "cyp4_1" : "cyp4_1 value1",
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
                "cyp5_atp1_8" : "Value17",
                "cyp5_app1_8": "Value18",
                "cyp5": "Value18a"
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
                "cyp5_atp1_8" : "Value27",
                "cyp5_app1_8": "Value28",
                "cyp5": "Value18a"
            }
        ],
        "program_technically_ip_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp6": "Value1",
                "cyp6_1": "Value11",
                "Program_Design_or_Structural_Issue": "Value12",
                "cyp6_atp1_8": "Value13",
                "cyp6_app1_8": "Value14"
            },
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp6": "Value1",
                "cyp6_1": "Value11",
                "Program_Design_or_Structural_Issue": "Value12",
                "cyp6_atp1_8": "Value15",
                "cyp6_app1_8": "Value16"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp6": "Value1",
                "cyp6_1": "Value21",
                "Program_Design_or_Structural_Issue": "Value22",
                "cyp6_atp1_8": "Value23",
                "cyp6_app1_8": "Value24"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp6": "Value1",
                "cyp6_1": "Value21",
                "Program_Design_or_Structural_Issue": "Value22",
                "cyp6_atp1_8": "Value25",
                "cyp6_app1_8": "Value26"
            }
        ],
        "program_eligibility_information_data_points": [{
            "Column_names": "cyp5_dit5_1",
            "Column_values": "4.10",
            "theme": "Address",
            "Payment_Type": "Underpayments",
            "Fiscal_Year": 2024
        }],
        "program_unknown_payments_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp8": "Value11",
                "Insufficient_Documentation_to_Determine": "Value12",
                "cyp7_ucp4_1": "Value13",
                "cyp7_atp1_8": "Value14",
                "cyp7_app1_8": "Value15",
                "rac3": "rac3",
                "cyp26": "cyp26"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp8": "Value21",
                "Insufficient_Documentation_to_Determine": "Value12",
                "cyp7_ucp4_1": "Value23",
                "cyp7_atp1_8": "Value24",
                "cyp7_app1_8": "Value25",
                "rac3": "rac3",
                "cyp26": "cyp26"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp8": "Value21",
                "Insufficient_Documentation_to_Determine": "Value12",
                "cyp7_ucp4_1": "Value23",
                "cyp7_atp1_8": "Value26",
                "cyp7_app1_8": "Value27",
                "rac3": "rac3",
                "cyp26": "cyp26"
            }
        ],
        "program_unknown_payments_breakdown_data_points": [
            {
                "Fiscal_Year": 2023,
                "Column_names": "cyp7_ucp3",
                "Column_values": "4"
            }
        ],
        "program_corrective_actions_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "rnp3": "Value11",
                "act17_2": "Value12",
                "act17_1": "Value13",
                "act17_3": "Value14"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "rnp3": "Value21",
                "act17_2": "Value22",
                "act17_1": "Value23",
                "act17_3": "Value24"
            }
        ],
        "program_future_outlook_data_points": [
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "cyp15" : "Value11",
                "cyp20_2": "Value12",
                "cyp29": "Value12_29",
                "rtp4_1": "Value13_1",
                "rtp4_2": "Value13",
                "rtp4_3": "Value13_3",
                "rtp1": "Value13a",
                "rap5": "Value14",
                "rap6": "Value15",
                "Outlays_Current_Year+1_Amount": "Value16",
                "IP_Current_Year+1_Amount": "Value17",
                "Unknown_Curent_Year+1_Amount": "Value18",
                "IP_Unknown_Current_Year+1_Rate": "Value19",
                "IP_Unknown_Target_Rate": "Value111"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "cyp15" : "Value21",
                "cyp20_2": "Value22",
                "cyp29": "Value22_29",
                "rtp4_1": "Value23_1",
                "rtp4_2": "Value23",
                "rtp4_3": "Value23_3",
                "rtp1": "Value23a",
                "rap5": "Value24",
                "rap6": "Value25",
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
                "pro1": "Value11",
                "rnp4": "Value12"
            },
            {
                "Fiscal_Year": 2023,
                "Program_Name": "Program 1",
                "pro1": "Value13",
                "rnp4": "Value12"
            },
            {
                "Fiscal_Year": 2024,
                "Program_Name": "Program 1",
                "pro1": "Value21",
                "rnp4": "Value22"
            }
        ],
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
                "Question": "question1",
                "Answer": "answer1_2023",
                "SortOrder": 0
            },
            {
                "Agency": "AG2",
                "Fiscal_Year": 2023,
                "Key": "key1",
                "Question": "question1",
                "Answer": "answer1a_2023",
                "SortOrder": 0
            }
        ],
        "risks_2023_AG1": [{
            "Agency": "AG1",
            "Fiscal_Year": 2023,
            "Program_Name": "PR1",
            "Susceptible": "No"
        }],
        "AG1_raw_data_points_2023": [
            {
                "agency": "AG1",
                "Key": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2023
            },
            {
                "agency": "AG1",
                "Key": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2023
            }
        ],
        "risks_2023_AG2": [{
            "Agency": "AG2",
            "Fiscal_Year": 2023,
            "Program_Name": "PR2",
            "Susceptible": "No"
        }],
        "AG2_raw_data_points_2023": [
            {
                "agency": "AG2",
                "Key": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2023
            },
            {
                "agency": "AG2",
                "Key": "raa8",
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
                "Question": "question1",
                "Answer": "answer1_2024",
                "SortOrder": 0
            },
            {
                "Agency": "AG2",
                "Fiscal_Year": 2024,
                "Key": "key2",
                "Question": "question2",
                "Answer": "answer2_2024",
                "SortOrder": 0
            }
        ],
        "risks_2024_AG1": [{
            "Agency": "AG1",
            "Fiscal_Year": 2024,
            "Program_Name": "PR1",
            "Susceptible": "No"
        }],
        "AG1_raw_data_points_2024": [
            {
                "agency": "AG1",
                "Key": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "A1",
                "Key": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2024
            }
        ],
        "risks_2024_AG2": [{
            "Agency": "AG2",
            "Fiscal_Year": 2024,
            "Program_Name": "PR2",
            "Susceptible": "No"
        }],
        "AG2_raw_data_points_2024": [
            {
                "agency": "AG2",
                "Key": "raa9",
                "Title": "title_1",
                "value": "value_1",
                "Fiscal_Year": 2024
            },
            {
                "agency": "AG2",
                "Key": "raa8",
                "Title": "title_2",
                "value": "value_2",
                "Fiscal_Year": 2024
            }
        ]
    }

def test_generate_agency_programs_page(mock_cursor, agency_programs_sample_data):
    mock_cursor.fetchall.side_effect = [
        agency_programs_sample_data["program_specific_data_points"],
        agency_programs_sample_data["agency_specific_data_points"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
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
            load.AGENCY_SPECIFIC_FISCAL_YEARS = [2024]
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
    load.PROGRAM_SPECIFIC_FISCAL_YEARS = [2023, 2024]

    mock_cursor.fetchall.side_effect = [
        program_specific_sample_data["all_agency_program_names"],
        program_specific_sample_data["program_data_points"],
        program_specific_sample_data["program_chart_data_points_A1"],
        program_specific_sample_data["program_improper_payment_estimates_data_points"],
        program_specific_sample_data["program_actions_data_points_2023"],
        program_specific_sample_data["program_actions_data_points_2024"],
        program_specific_sample_data["visibility_data_points"],
        program_specific_sample_data["program_overpayments_data_points"],
        program_specific_sample_data["program_overpayments_outside_data_points"],
        program_specific_sample_data["program_underpayments_data_points"],
        program_specific_sample_data["program_technically_ip_data_points"],
        program_specific_sample_data["program_eligibility_information_data_points"],
        program_specific_sample_data["program_unknown_payments_data_points"],
        program_specific_sample_data["program_unknown_payments_breakdown_data_points"],
        program_specific_sample_data["program_corrective_actions_data_points"],
        program_specific_sample_data["program_future_outlook_data_points"],
        program_specific_sample_data["program_additional_information_data_points"],
        program_specific_sample_data["scorecard_links"]
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            load.slugifyProgramNames(mock_cursor)
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
            assert yaml_data["Outlays"] == 1000
            assert yaml_data["Payment_Accuracy_Rate"] == 98
            assert yaml_data["Description"] == "Description 1"
            assert yaml_data["Payment_Accuracy_Amounts"] == "[1200, 1483]"
            assert yaml_data["Overpayment_Amounts"] == "[100, 456]"
            assert yaml_data["Underpayment_Amounts"] == "[29, 32]"
            assert yaml_data["Technically_Improper_Amounts"] == "[38, 12]"
            assert yaml_data["Unknown_Amounts"] == "[8, 6]"
            assert len(yaml_data["Scorecard_Links"]) == 1
            for year_data in yaml_data["Data_By_Year"]:
                if year_data.get("Year") == 2023:
                    assert year_data["Improper_Payments_Rate"] == 3
                    assert year_data["Payment_Accuracy_Rate"] == 97
                    assert year_data["Actions_Taken"][0]["Action_Taken"] == "Action Taken 1"
                    assert year_data["Actions_Taken"][0]["Description_Action_Taken"] == "Description Action Taken 1"
                    assert year_data["overpayments"]["Address_Location"] == "Value14"
                    assert year_data["underpayments"]["Contractor_Provider_Status"] == "Value15"
                    assert year_data["Program_Design_or_Structural_Issue"] == "Value12"
                    assert year_data["cyp6_app1_8"] == "Value16"
                    assert year_data["Insufficient_Documentation_to_Determine"] == "Value12"
                    assert year_data["cyp8"] == "Value11"
                    assert year_data["rnp3"] == "Value11"
                    assert year_data["act17_2"] == "Value12"
                    assert year_data["Outlays_Current_Year_Plus_1_Amount"] == "Value16"
                    assert year_data["IP_Current_Year_Plus_1_Amount"] == "Value17"
                    assert "pro1" not in year_data
                    assert year_data["rnp4"] == "Value12"
                elif year_data.get("Year") == 2024:
                    assert year_data["Improper_Payments_Rate"] == 5
                    assert year_data["Payment_Accuracy_Rate"] == 86
                    assert year_data["Actions_Taken"][0]["Action_Taken"] == "Action Taken 2"
                    assert year_data["Actions_Taken"][0]["Description_Action_Taken"] == "Description Action Taken 2"
                    assert year_data["overpayments"]["Failure_to_Access_Data"] == "Value23"
                    assert year_data["cyp6_atp1_8"] == "Value25"
                    assert year_data["cyp6_app1_8"] == "Value26"
                    assert year_data["cyp6_1"] == "Value21"
                    assert year_data["cyp7_app1_8"] == "Value27"
                    assert year_data["cyp7_atp1_8"] == "Value26"
                    assert year_data["act17_1"] == "Value23"
                    assert year_data["act17_3"] == "Value24"
                    assert year_data["IP_Unknown_Current_Year_Plus_1_Rate"] == "Value29"
                    assert year_data["Unknown_Curent_Year_Plus_1_Amount"] == "Value28"
                    assert year_data["pro1"] == "Value21"
                    assert year_data["rnp4"] == "Value22"

def test_generate_congressional_reports_pages(mock_cursor, congressional_reports_sample_data):
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
            "1": {
                "key1": {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": ""
                }
            }
        },
        "2024": {
            "1": {
                "key1": {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": ""
                },
                "key2": {
                    "type": config.CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                    "heading": "",
                    "subheading": ""
                }
            }
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

            mocked_file.assert_called_with(os.path.join(load.CONGRESSIONAL_REPORTS_DIR, "2024_AG2_1.md"), 'w', encoding='utf-8')
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