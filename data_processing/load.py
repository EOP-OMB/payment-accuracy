"""
Creates markdown files for static site generation.
"""

import config
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
import json
import os
import shutil
import sqlite3
from load_tools import query, congressional_reports
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = os.path.join(BASE_DIR, "..", "website")

DB_FILE_PATH = os.path.join("transformed", "transformed_data.db")
HOME_MARKUP_FILE_PATH = os.path.join(WEBSITE_DIR, "pages", "home.md")
AGENY_WIDE_FILE_PATH = os.path.join(WEBSITE_DIR, "pages", "agenciesPrograms.md")
AGENCY_SPECIFIC_DIR = os.path.join(WEBSITE_DIR, "pages", "agencies")
PROGRAM_SPECIFIC_DIR = os.path.join(WEBSITE_DIR, "pages", "programs")
CONGRESSIONAL_REPORTS_MARKUP_PATH = os.path.join(WEBSITE_DIR, "pages", "congressional_reports.md")
CONGRESSIONAL_REPORTS_DIR = os.path.join(WEBSITE_DIR, "pages", "congressional_reports")
SHARED_DATA_DIR = os.path.join(WEBSITE_DIR, "_data")
SHARED_DATA_PATH = os.path.join(SHARED_DATA_DIR, "shared.yml")
CONGRESSIONAL_REPORTS_SHARED_DATA_PATH = os.path.join(SHARED_DATA_DIR, "congressional_reports.yml")
AGENCY_DATA_POINTS_FILE_PATH = os.path.join(WEBSITE_DIR, "data", "agency_data_points.json")
DB_FULL_PATH = os.path.join(BASE_DIR, DB_FILE_PATH)

def generate_home_page(cursor: sqlite3.Cursor):
    """
    Generate the home page using transformed all_programs_min_max_rates database.
    """
    governmentWideFiscalYearRange = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_GOVERNMENT_WIDE_YEARS_DISPLAYED + 1]
    rateExtremes = query.fetch_all(cursor, query.QUERY_TYPES.IP_GW_RATE_EXTREMES, governmentWideFiscalYearRange)[0]
    highest_performing_agencies = query.fetch_all(cursor, query.QUERY_TYPES.IP_HIGHEST_PERFORMING_AGENCIES, (config.FISCAL_YEAR,))
    lowest_performing_agencies = query.fetch_all(cursor, query.QUERY_TYPES.IP_WORST_PERFORMING_AGENCIES, (config.FISCAL_YEAR,))
    rates = query.fetch_all(cursor, query.QUERY_TYPES.IP_GW_RATES, governmentWideFiscalYearRange)

    page = {
        'title': 'Home',
        'layout': 'index',
        'permalink': '/',
        'payment_accuracy_rate_min': rateExtremes["Payment_Accuracy_Rate_Min"],
        'payment_accuracy_rate_max': rateExtremes["Payment_Accuracy_Rate_Max"],
        'improper_payments_rate_min': rateExtremes["Improper_Payments_Rate_Min"],
        'improper_payments_rate_max': rateExtremes["Improper_Payments_Rate_Max"],
        'unknown_payments_rate_min': rateExtremes["Unknown_Payments_Rate_Min"],
        'unknown_payments_rate_max': rateExtremes["Unknown_Payments_Rate_Max"],
        'highest_performing_agencies': highest_performing_agencies,
        'lowest_performing_agencies': lowest_performing_agencies,
        'fiscal_year': config.FISCAL_YEAR,
        'payment_accuracy_rates': str(extract_column_from_results("Payment_Accuracy_Rate", rates)),
        'improper_payments_rates': str(extract_column_from_results("Improper_Payments_Rate", rates)),
        'unknown_payments_rates': str(extract_column_from_results("Unknown_Payments_Rate", rates)),
        'improper_payments_years': str(extract_column_from_results("Fiscal_Year", rates))
    }

    os.makedirs(os.path.dirname(HOME_MARKUP_FILE_PATH), exist_ok=True)
    with open(HOME_MARKUP_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('---\n')
        yaml.dump(page, file, allow_unicode=True)
        file.write('---\n')
    print("Successfully generated homepage md file")

def generate_agency_programs_page(cursor: sqlite3.Cursor):
    program_rows = query.fetch_all(
        cursor,
        query.QUERY_TYPES.AGENCY_WIDE_TABLE_PROGRAMS,
        (config.FISCAL_YEAR-1,config.FISCAL_YEAR)
    )

    agencyFiscalYearRange = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED + 1]
    agency_rows = query.fetch_all(
        cursor,
        query.QUERY_TYPES.AGENCY_WIDE_TABLE_AGENCIES,
        agencyFiscalYearRange + [config.FISCAL_YEAR, config.FISCAL_YEAR-1, config.FISCAL_YEAR]
    )

    programs_by_agency = {}
    for row in program_rows:
        agency = row['agency']
        del row['agency']
        programs_by_agency.setdefault(agency, []).append(row)

    agencies_data = []
    for row in agency_rows:
        row['programs'] = programs_by_agency.get(row['agency'], [])
        agencies_data.append(row)
    
    page = {
        'title': 'Agencies & Programs',
        'layout': 'agency-wide',
        'permalink': '/agencies-and-programs',
        'agencies': agencies_data
    }

    os.makedirs(os.path.dirname(AGENY_WIDE_FILE_PATH), exist_ok=True)
    with open(AGENY_WIDE_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('---\n')
        yaml.dump(page, file, allow_unicode=True)
        file.write('---\n')
    print("Successfully generated agency-wide md file")

def extract_column_from_results(fieldName, results):
    return list(map(lambda x: x[fieldName], results))

def generate_agency_specific_pages_for_year(cursor: sqlite3.Cursor, year):
    os.makedirs(AGENCY_SPECIFIC_DIR, exist_ok=True)
    agencies = query.fetch_all(cursor, query.QUERY_TYPES.ALL_AGENCIES_YEARS, (year,))
    agencyFiscalYearRange = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED + 1]

    for agency in agencies:
        yearsAvailable = query.fetch_all(cursor, query.QUERY_TYPES.ALL_AGENCIES_YEARS_AVAILABLE, [agency["Agency"]] + agencyFiscalYearRange, year)

        # this object is used to merge agency data and raw detail data
        agencyObj = {
            "Agency": agency["Agency"],
            "Agency_Name": agency["Agency_Name"],
            "Fiscal_Year": agency["Fiscal_Year"],
            "Confirmed_Fraud": agency["Confirmed_Fraud"],
            "layout": "agency-specific",
            "Years_Available": list(map(lambda x: x["Fiscal_Year"], yearsAvailable)),
            "Is_Placeholder": False
        }

        details = query.get_agency_survey_details(cursor, year, agency["Agency"])

        # this relies on the assumption that there is one record per year-agency-key 
        # if multiselect values are ever needed, use a separate extract file and table
        for detail in details.values():
            key = "detail_" + detail["Name"]
            agencyObj[key] = detail["value"]

        recoveryDetails = query.fetch_all(cursor, query.QUERY_TYPES.PAYMENT_RECOVERY_DETAILS, (year, agency["Agency"]), year)

        for recoveryDetail in recoveryDetails:
            key = "recovery_" + str(recoveryDetail["key"]).replace(" ","_")
            agencyObj[key] = recoveryDetail["value"]

        recoveryYears = [year, year - config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED_FOR_RECOVERY + 1]
        recoveryAmountDetails = query.fetch_all(cursor, query.QUERY_TYPES.PAYMENT_RECOVERY_AMOUNTS, [agency["Agency"]] + recoveryYears, year)

        agencyObj["Overpayment_Amounts_Identified"] = str(extract_column_from_results("Overpayment_Amount_Identified_For_Recapture_($M)", recoveryAmountDetails))
        agencyObj["Overpayment_Amounts_Recovered"] = str(extract_column_from_results("Overpayment_Amount_Recovered_($M)", recoveryAmountDetails))
        agencyObj["Overpayment_Years"] = str(extract_column_from_results("Fiscal_Year", recoveryAmountDetails))

        dataPointsDetails = query.fetch_all(cursor, query.QUERY_TYPES.AGENCY_RATE_EXTREMES, [agency["Agency"]] + agencyFiscalYearRange, year)

        accuracyRates = extract_column_from_results("Payment_Accuracy_Rate", dataPointsDetails)
        improperRates = extract_column_from_results("Improper_Payments_Rate", dataPointsDetails)
        unknownRates = extract_column_from_results("Unknown_Payments_Rate", dataPointsDetails)
        agencyObj["Payment_Accuracy_Rates"] = str(accuracyRates)
        agencyObj["Improper_Payments_Rates"] = str(improperRates)
        agencyObj["Unknown_Payments_Rates"] = str(unknownRates)
        agencyObj["Payment_Accuracy_Amounts"] = str(extract_column_from_results("Payment_Accuracy_Amount", dataPointsDetails))
        agencyObj["Overpayment_Amounts"] = str(extract_column_from_results("Overpayment_Amount", dataPointsDetails))
        agencyObj["Underpayment_Amounts"] = str(extract_column_from_results("Underpayment_Amount", dataPointsDetails))
        agencyObj["Technically_Improper_Amounts"] = str(extract_column_from_results("Technically_Improper_Amount", dataPointsDetails))
        agencyObj["Unknown_Amounts"] = str(extract_column_from_results("Unknown_Amount", dataPointsDetails))
        agencyObj["Payment_Accuracy_Rate_Min"] = round(min(accuracyRates, default=0),1)
        agencyObj["Payment_Accuracy_Rate_Max"] = round(max(accuracyRates, default=0),1)
        agencyObj["Improper_Payments_Rate_Min"] = round(min(improperRates, default=0),1)
        agencyObj["Improper_Payments_Rate_Max"] = round(max(improperRates, default=0),1)
        agencyObj["Unknown_Payments_Rate_Min"] = round(min(unknownRates, default=0),1)
        agencyObj["Unknown_Payments_Rate_Max"] = round(max(unknownRates, default=0),1)
        agencyObj["Improper_Payments_Data_Years"] = str(extract_column_from_results("Fiscal_Year", dataPointsDetails))

        piiaProgramDetails = query.fetch_all(cursor, query.QUERY_TYPES.PIIA_NON_COMPLIANT_PROGRAMS, (agency["Agency"], year), year)
        agencyObj["PIIA2019_NonCompliant_Programs"] = list(filter(lambda x: not x['Compliant_Overall'], piiaProgramDetails))
        agencyObj["PIIA2019_Compliant_Programs"] = list(filter(lambda x: x['Compliant_Overall'], piiaProgramDetails))

        agencyObj["Risks"] = get_risks(cursor, year, agency["Agency"])

        eligibilityThemeDetails = query.fetch_all(cursor, query.QUERY_TYPES.ELIGIBILITY_THEME_DETAILS, (agency["Agency"], year), year)

        # group themes for easier use in jekyll
        agencyObj["Eligibility_Themes"] = []
        lastProgram = None
        for eligibilityThemeDetail in eligibilityThemeDetails:
            if lastProgram == None or lastProgram['Program_Name'] != eligibilityThemeDetail["Program Name"]:
                lastProgram = {
                    'Program_Name': eligibilityThemeDetail["Program Name"],
                    'Themes': []
                }
                agencyObj["Eligibility_Themes"].append(lastProgram)
            lastProgram['Themes'].append({
                "Theme": eligibilityThemeDetail["theme"],
                "Barriers": eligibilityThemeDetail["Barriers"],
                "Info": eligibilityThemeDetail["Info"]
            })

        hide_agency_specific_sections(agencyObj)

        write_agency_md_files(agency["Agency"], agencyObj, year)

    print("Successfully generated agency-specific md files for FY " + str(year))

def get_risks(cursor, year, agency):
    assessments = query.fetch_all(
        cursor,
        query.QUERY_TYPES.RISK_ASSESSMENTS, (agency, year),
        year
    )

    return {
        "Assessments": assessments,
        "AdditionalInformation": query.get_agency_survey_answer(cursor, year, agency, query.KEY_TYPES.Risks_Additional_Information),
        "SubstantialChangesMade": query.get_agency_survey_answer(cursor, year, agency, query.KEY_TYPES.Risks_Substantial_Changes_Made)
    }

def hide_agency_specific_sections(agencyObj):
    hasRecoveryKey = False
    for key in agencyObj.keys():
        # 0 check added for cases where survey edits cause answers to be submitted unnecessarily
        if key.startswith("recovery_") and agencyObj[key] > 0:
            hasRecoveryKey = True
            break

    recoveryAuditsSkipped = "detail_Recovery_Audits_Skipped" in agencyObj and \
        agencyObj["detail_Recovery_Audits_Skipped"] is not None and \
        agencyObj["detail_Recovery_Audits_Skipped"].upper() == 'NO'
    recoveryAuditsNotAnswered = "detail_Recovery_Audits_Skipped" not in agencyObj or \
        agencyObj["detail_Recovery_Audits_Skipped"] is None

    agencyObj["Hide_Integrity_Results"] = "Improper_Payments_Data_Years" not in agencyObj or \
        agencyObj["Improper_Payments_Data_Years"] is None or \
        agencyObj["Improper_Payments_Data_Years"] == '[]'
    # Sparklines with one datapoint are not useful
    agencyObj["Hide_Sparklines"] = agencyObj["Hide_Integrity_Results"] or \
        "," not in agencyObj["Improper_Payments_Data_Years"]

    agencyObj["Hide_Recovery_Details"] = (recoveryAuditsSkipped or recoveryAuditsNotAnswered) and (not hasRecoveryKey and \
        ("detail_Recovery_Additional_Details" not in agencyObj or agencyObj["detail_Recovery_Additional_Details"] is None or agencyObj["detail_Recovery_Additional_Details"] == ''))
    agencyObj["Hide_Recovery_Audits"] = \
        ("detail_Overpayment_Conditions" not in agencyObj or agencyObj["detail_Overpayment_Conditions"] is None or agencyObj["detail_Overpayment_Conditions"] == '') and \
        ("detail_Recovery_Methods_Audits" not in agencyObj or agencyObj["detail_Recovery_Methods_Audits"] is None or agencyObj["detail_Recovery_Methods_Audits"] == '') and \
        ("detail_Recovery_Not_Cost_Effective_Justification" not in agencyObj or agencyObj["detail_Recovery_Not_Cost_Effective_Justification"] is None or agencyObj["detail_Recovery_Not_Cost_Effective_Justification"] == '') and \
        ("detail_Recovery_Not_Cost_Effective_Programs" not in agencyObj or agencyObj["detail_Recovery_Not_Cost_Effective_Programs"] is None or agencyObj["detail_Recovery_Not_Cost_Effective_Programs"] == '')
    agencyObj["Hide_Disposition_of_Funds_Table"] = recoveryAuditsSkipped or (("recovery_Disposition_of_Funds_through_recovery_audit_Administer_Auditor" not in agencyObj or agencyObj["recovery_Disposition_of_Funds_through_recovery_audit_Administer_Auditor"] is None) and \
        ("recovery_Disposition_of_Funds_through_FM_Improvement_Activities" not in agencyObj or agencyObj["recovery_Disposition_of_Funds_through_FM_Improvement_Activities"] is None) and \
        ("recovery_Disposition_of_Funds_Through_Original_Purpose" not in agencyObj or agencyObj["recovery_Disposition_of_Funds_Through_Original_Purpose"] is None) and \
        ("recovery_Disposition_of_Funds_Through_Office_of_Inspector_General" not in agencyObj or agencyObj["recovery_Disposition_of_Funds_Through_Office_of_Inspector_General"] is None) and \
        ("recovery_Disposition_of_Funds_Through_Returned_to_Treasury" not in agencyObj or agencyObj["recovery_Disposition_of_Funds_Through_Returned_to_Treasury"] is None) and \
        ("recovery_Returned_to_Original_Account" not in agencyObj or agencyObj["recovery_Returned_to_Original_Account"] is None))
    agencyObj["Hide_Disposition_of_Funds"] = recoveryAuditsSkipped or (agencyObj["Hide_Disposition_of_Funds_Table"] and \
        ("detail_Aging_of_Outstanding_OP_Identified_Remaining_Unrecovered" not in agencyObj or agencyObj["detail_Aging_of_Outstanding_OP_Identified_Remaining_Unrecovered"] is None) and \
        ("recovery_Aging_of_Outstanding_OP_Identified_Amt_0_-_6_months" not in agencyObj or agencyObj["recovery_Aging_of_Outstanding_OP_Identified_Amt_0_-_6_months"] is None) and \
        ("recovery_Aging_of_Outstanding_OP_Identified_Amt_6_months_to_1_year" not in agencyObj or agencyObj["recovery_Aging_of_Outstanding_OP_Identified_Amt_6_months_to_1_year"] is None) and \
        ("recovery_Aging_of_Outstanding_OP_Identified_Amt_over_1_year" not in agencyObj or agencyObj["recovery_Aging_of_Outstanding_OP_Identified_Amt_over_1_year"] is None) and \
        ("recovery_Aging_of_Outstanding_OP_Identified_determined_not_collectable" not in agencyObj or agencyObj["recovery_Aging_of_Outstanding_OP_Identified_determined_not_collectable"] is None) and \
        ("recovery_Recovery_Audit_Amount_Identified_In_Prior_Reporting_Periods_Determined_Not_Collectable_During_This_Reporting_Period" not in agencyObj or agencyObj["recovery_Recovery_Audit_Amount_Identified_In_Prior_Reporting_Periods_Determined_Not_Collectable_During_This_Reporting_Period"] is None) and \
        ("detail_Recovery_Justifications_Audits" not in agencyObj or agencyObj["detail_Recovery_Justifications_Audits"] is None))
    agencyObj["Hide_Recovery_Info"] = agencyObj["Hide_Recovery_Details"] and agencyObj["Hide_Recovery_Audits"] and \
        agencyObj["Hide_Disposition_of_Funds"] and \
        ("Overpayment_Years" not in agencyObj or agencyObj["Overpayment_Years"] is None or agencyObj["Overpayment_Years"] == '[]')

    agencyObj["Hide_Do_Not_Pay"] = ("detail_DNP_Discussion" not in agencyObj or agencyObj["detail_DNP_Discussion"] is None or agencyObj["detail_DNP_Discussion"] == '') and \
        ("detail_DNP_Reduced" not in agencyObj or agencyObj["detail_DNP_Reduced"] is None or agencyObj["detail_DNP_Reduced"] == '') and \
        ("detail_DNP_Frequency_Identify" not in agencyObj or agencyObj["detail_DNP_Frequency_Identify"] is None or agencyObj["detail_DNP_Frequency_Identify"] == '')
    agencyObj["Hide_PIIA2019"] = ("detail_Compliance_Status" not in agencyObj or agencyObj["detail_Compliance_Status"] is None) and \
        ("PIIA2019_Compliant_Programs" not in agencyObj or agencyObj["PIIA2019_Compliant_Programs"] is None or len(agencyObj["PIIA2019_Compliant_Programs"]) == 0) and \
        ("PIIA2019_NonCompliant_Programs" not in agencyObj or agencyObj["PIIA2019_NonCompliant_Programs"] is None or len(agencyObj["PIIA2019_NonCompliant_Programs"]) == 0) and \
        ("detail_Recommendations_To_Reduce_IP" not in agencyObj or agencyObj["detail_Recommendations_To_Reduce_IP"] is None) and \
        ("detail_OIG_Recommendations" not in agencyObj or agencyObj["detail_OIG_Recommendations"] is None) and \
        ("detail_PIIA_Official" not in agencyObj or agencyObj["detail_PIIA_Official"] is None) and \
        ("detail_PIIA_Incentives" not in agencyObj or agencyObj["detail_PIIA_Incentives"] is None)
    agencyObj["Hide_Risk_Assessment_Results"] = \
        ("Risks" not in agencyObj or agencyObj["Risks"] is None) or \
        (
            (agencyObj["Risks"]["Assessments"] is None or len(agencyObj["Risks"]["Assessments"]) == 0) and \
            agencyObj["Risks"]["AdditionalInformation"] is None and \
            agencyObj["Risks"]["SubstantialChangesMade"] is None
        )
    agencyObj["Hide_Eligibility_Criteria"] = \
        ("Eligibility_Themes" not in agencyObj or agencyObj["Eligibility_Themes"] is None or len(agencyObj["Eligibility_Themes"]) == 0)
    agencyObj["Hide_Supplemental_Payment_Integrity"] = \
        ("detail_Additional_IP_Information" not in agencyObj or agencyObj["detail_Additional_IP_Information"] is None or agencyObj["detail_Additional_IP_Information"] == '')
    agencyObj["Hide_Supplemental_Info"] = agencyObj["Hide_Do_Not_Pay"] and \
        agencyObj["Hide_PIIA2019"] and \
        agencyObj["Hide_Risk_Assessment_Results"] and agencyObj["Hide_Eligibility_Criteria"] and \
        agencyObj["Hide_Supplemental_Payment_Integrity"]

def write_agency_md_files(agencyCode, agencyObj, year):
    longpath = os.path.join(AGENCY_SPECIFIC_DIR, agencyCode)
    os.makedirs(longpath, exist_ok=True)
    with open(os.path.join(longpath, str(year) + ".md"), 'w', encoding='utf-8') as file:
        agencyObj["permalink"] = "agency/" + agencyCode + "/" + str(year) + ".html"
        file.write('---\n')
        yaml.dump(agencyObj, file, allow_unicode=True)
        file.write('---\n')

    # Provide current year as default
    if year == config.FISCAL_YEAR:
        with open(os.path.join(AGENCY_SPECIFIC_DIR, agencyCode + ".md"), 'w', encoding='utf-8') as file:
            agencyObj["permalink"] = "agency/" + str(agencyCode) + ".html"
            file.write('---\n')
            yaml.dump(agencyObj, file, allow_unicode=True)
            file.write('---\n')

def generate_agency_specific_pages(cursor):
    if os.path.exists(AGENCY_SPECIFIC_DIR):
        shutil.rmtree(AGENCY_SPECIFIC_DIR)

    agencyFiscalYears = list(range(config.FISCAL_YEAR - config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED + 1, config.FISCAL_YEAR + 1))
    for year in agencyFiscalYears:
        generate_agency_specific_pages_for_year(cursor, year)

# this ensures that every agency that has ever had data has a landing page
def generate_placeholder_agency_specific_pages(cursor):
    agencies = query.fetch_all(cursor, query.QUERY_TYPES.DISTINCT_AGENCIES)
    agencyFiscalYearRange = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED + 1]

    for agency in agencies:
        if not os.path.isfile(os.path.join(AGENCY_SPECIFIC_DIR, agency["Agency"] + ".md")):
            with open(os.path.join(AGENCY_SPECIFIC_DIR, agency["Agency"] + ".md"), 'w', encoding='utf-8') as file:
                yearsAvailable = query.fetch_all(cursor, query.QUERY_TYPES.ALL_AGENCIES_YEARS_AVAILABLE, [agency["Agency"]] + agencyFiscalYearRange)

                agencyObj = {
                    "Agency": agency["Agency"],
                    "Agency_Name": agency["Agency_Name"],
                    "Fiscal_Year": config.FISCAL_YEAR,
                    "layout": "agency-specific",
                    "permalink": "agency/" + agency["Agency"] + ".html",
                    "Years_Available": list(map(lambda x: x["Fiscal_Year"], yearsAvailable)),
                    "Is_Placeholder": True
                }

                file.write('---\n')
                yaml.dump(agencyObj, file, allow_unicode=True)
                file.write('---\n')

    print("Successfully generated placeholder agency-specific md files for FY " + str(config.FISCAL_YEAR))

def generate_program_specific_pages(cursor: sqlite3.Cursor):
    programs = query.fetch_all(cursor, query.QUERY_TYPES.ALL_PROGRAMS, [config.LAST_QUARTERLY_SURVEY, config.FISCAL_YEAR])
    programFiscalYearRange = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_PROGRAM_SPECIFIC_YEARS_DISPLAYED + 1]

    if os.path.exists(PROGRAM_SPECIFIC_DIR):
        shutil.rmtree(PROGRAM_SPECIFIC_DIR)

    os.makedirs(PROGRAM_SPECIFIC_DIR, exist_ok=True)
    for program in programs:
        # this object is used to merge program data and raw detail data
        programObj = {
            "Agency": program["Agency"],
            "Agency_Name": program["Agency_Name"],
            "Program_Name": program["Program_Name"],
            "High_Priority_Program": program["High_Priority_Program"],
            "Phase_2_Program": program["Phase_2_Program"],
            "Description": program["Description"],
            "layout": "program-specific",
            "permalink": "program/" + program["Slug"]
        }

        fpi_link = query.fetch_all(cursor, query.QUERY_TYPES.FPI_LINK, [program["Agency"], program["Program_Name"]], config.FISCAL_YEAR)
        if len(fpi_link) > 0:
            programObj["fpi_link"] = "https://fpi.omb.gov/program/" + fpi_link[0]["Assistance Listing Number"]

        dataPointsDetails = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_DATA_POINTS, [program["Program_Name"]] + programFiscalYearRange)

        programObj["Fiscal_Year"] = config.FISCAL_YEAR
        programObj["Payment_Accuracy_Amounts"] = str(extract_column_from_results("Payment_Accuracy_Amount", dataPointsDetails))
        programObj["Overpayment_Amounts"] = str(extract_column_from_results("Overpayment_Amount", dataPointsDetails))
        programObj["Underpayment_Amounts"] = str(extract_column_from_results("Underpayment_Amount", dataPointsDetails))
        programObj["Technically_Improper_Amounts"] = str(extract_column_from_results("Technically_Improper_Amount", dataPointsDetails))
        programObj["Unknown_Amounts"] = str(extract_column_from_results("Unknown_Amount", dataPointsDetails))
        programObj["Improper_Payments_Data_Years"] = str(extract_column_from_results("Fiscal_Year", dataPointsDetails))

        data_by_year_dict = {}
        improperPaymentEstimates = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_IP_ESTIMATES, [program["Program_Name"]] + programFiscalYearRange)
        
        for row in improperPaymentEstimates:
            outlays = row["Outlays"]
            fiscal_year = row["Fiscal_Year"]
            accuracy_rate = row["Payment_Accuracy_Rate"]
            ip_rate = row["IP_Rate"]
            unknown_rate = row["Unknown_Payments_Rate"]
            start_date = row["Start_Date"]
            end_date = row["End_Date"]
            confidence_level = row["CY_Confidence_Level"]
            margin_of_error = row["CY_Margin_of_Error"]
            hide_improper_payment_estimates_doughnut_chart = accuracy_rate is None
            hide_improper_payment_estimates_doughnut_stats = start_date is None and end_date is None and \
                confidence_level is None and margin_of_error is None

            # Check if at least one of the rates is not None
            if any(rate is not None for rate in (accuracy_rate, ip_rate, unknown_rate)):
                data_by_year_dict[fiscal_year] = {
                    key: value for key, value in {
                        "Outlays": outlays,
                        "Payment_Accuracy_Rate": accuracy_rate,
                        "Improper_Payments_Rate": ip_rate,
                        "Unknown_Payments_Rate": unknown_rate,
                        "Start_Date": start_date[5:7] + "/" + start_date[0:4] if start_date is not None else None,
                        "End_Date": end_date[5:7] + "/" + end_date[0:4] if end_date is not None else None,
                        "Confidence_Level": confidence_level,
                        "Margin_of_Error": margin_of_error,
                        "Hide_Improper_Payment_Estimates_Doughnut_Chart": hide_improper_payment_estimates_doughnut_chart,
                        "Hide_Improper_Payment_Estimates_Doughnut_Stats": hide_improper_payment_estimates_doughnut_stats
                    }.items() if value is not None
                }

            details = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_SURVEY_KEY_AGNOSTIC, [program["Program_Name"], fiscal_year])

            # this relies on the assumption that there is one record per year-agency-key
            # if multiselect values are ever needed, use a separate extract file and table
            for detail in details:
                if fiscal_year not in data_by_year_dict:
                    data_by_year_dict[fiscal_year] = {}
                key = "detail_" + detail["Name"]
                data_by_year_dict[fiscal_year][key] = detail["value"]

        program_specific_fiscal_years = list(range(config.FISCAL_YEAR - config.COUNT_PROGRAM_SPECIFIC_YEARS_DISPLAYED + 1, config.FISCAL_YEAR + 1))
        add_actions_taken(cursor, program_specific_fiscal_years, program["Program_Name"], data_by_year_dict)

        # Ideally, visibility would use the same fields as overpayments, underpayments, etc.
        #   queries below.  For now, creating a separate query due to time constraints.
        visibilityRows = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_PAYMENTS_VISIBILITY, [program["Program_Name"]] + programFiscalYearRange)
        for row in visibilityRows:
            fiscal_year = row["Fiscal_Year"]
            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}
            data_by_year_dict[fiscal_year]["Hide_" + row["Name"]] = True
        overpayments = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_OVERPAYMENTS, [program["Program_Name"]] + programFiscalYearRange)

        for row in overpayments:
            fiscal_year = row["Fiscal_Year"]
            Overpayments_Within_Control_Why = row["Overpayments_Within_Control_Why"]
            Overpayments_Within_Control_Amount = row["Overpayments_Within_Control_Amount"]
            data_needed_does_not_exist = row["Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis"]
            inability_to_access_data = row["Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data"]
            failure_to_access_data = row["Failure_to_Access_Data"]
            address_location = row["Address_Location"]
            contractor_provider_status = row["Contractor_or_Provider_Status"]
            financial = row["Financial"]
            Overpayment_Mitigations_Taken = row["Overpayment_Mitigations_Taken"]
            Overpayment_Mitigations_Planned = row["Overpayment_Mitigations_Planned"]
            Overpayment_Combined_Mitigations_Taken = row["Overpayment_Combined_Mitigations_Taken"]
            Overpayment_Combined_Mitigations_Planned = row["Overpayment_Combined_Mitigations_Planned"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            if Overpayment_Mitigations_Taken:
                data_by_year_dict[fiscal_year]["Overpayment_Mitigations_Taken"] = Overpayment_Mitigations_Taken

            if Overpayment_Mitigations_Planned:
                data_by_year_dict[fiscal_year]["Overpayment_Mitigations_Planned"] = Overpayment_Mitigations_Planned

            if Overpayment_Combined_Mitigations_Taken:
                data_by_year_dict[fiscal_year]["Overpayment_Combined_Mitigations_Taken"] = Overpayment_Combined_Mitigations_Taken

            if Overpayment_Combined_Mitigations_Planned:
                data_by_year_dict[fiscal_year]["Overpayment_Combined_Mitigations_Planned"] = Overpayment_Combined_Mitigations_Planned
            
            for key, value in {
                "Overpayments_Within_Control_Why" : Overpayments_Within_Control_Why,
                "Overpayments_Within_Control_Amount": Overpayments_Within_Control_Amount,
                "Data_Needed_Does_Not_Exist" : data_needed_does_not_exist,
                "Inability_to_Access_Data" : inability_to_access_data,
                "Failure_to_Access_Data" : failure_to_access_data,
                "Address_Location" : address_location,
                "Contractor_Provider_Status" : contractor_provider_status,
                "Financial" : financial,
            }.items():
                if value is not None:
                    if "overpayments" not in data_by_year_dict[fiscal_year]:
                        data_by_year_dict[fiscal_year]["overpayments"] = {}
                    data_by_year_dict[fiscal_year]["overpayments"][key] = value

        overpayments_outside = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_OVERPAYMENTS_OUTSIDE, [program["Program_Name"]] + programFiscalYearRange)

        for row in overpayments_outside:
            fiscal_year = row["Fiscal_Year"]
            Overpayments_Outside_Control_Amount = row["Overpayments_Outside_Control_Amount"]
            Overpayments_Outside_Control_Why = row["Overpayments_Outside_Control_Why"]
            data_needed_does_not_exist = row["Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis"]
            inability_to_access_data = row["Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data"]
            failure_to_access_data = row["Failure_to_Access_Data"]
            address_location = row["Address_Location"]
            contractor_provider_status = row["Contractor_or_Provider_Status"]
            financial = row["Financial"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            for key, value in {
                "Overpayments_Outside_Control_Amount": Overpayments_Outside_Control_Amount,
                "Overpayments_Outside_Control_Why": Overpayments_Outside_Control_Why,
                "Data_Needed_Does_Not_Exist" : data_needed_does_not_exist,
                "Inability_to_Access_Data" : inability_to_access_data,
                "Failure_to_Access_Data" : failure_to_access_data,
                "Address_Location" : address_location,
                "Contractor_Provider_Status" : contractor_provider_status,
                "Financial" : financial,
            }.items():
                if value is not None:
                    if "overpayments_outside" not in data_by_year_dict[fiscal_year]:
                        data_by_year_dict[fiscal_year]["overpayments_outside"] = {}
                    data_by_year_dict[fiscal_year]["overpayments_outside"][key] = value

        underpayments = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_UNDERPAYMENTS, [program["Program_Name"]] + programFiscalYearRange)

        for row in underpayments:
            fiscal_year = row["Fiscal_Year"]
            data_needed_does_not_exist = row["Inability_to_Authenticate_Eligibility:_Data_Needed_Does_Not_Exis"]
            inability_to_access_data = row["Inability_to_Authenticate_Eligibility:_Inability_to_Access_Data"]
            failure_to_access_data = row["Failure_to_Access_Data"]
            address_location = row["Address_Location"]
            contractor_provider_status = row["Contractor_or_Provider_Status"]
            financial = row["Financial"]
            Underpayment_Mitigations_Taken = row["Underpayment_Mitigations_Taken"]
            Underpayment_Mitigations_Planned = row["Underpayment_Mitigations_Planned"]
            Underpayments_Amount = row["Underpayments_Amount"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            if Underpayment_Mitigations_Taken:
                data_by_year_dict[fiscal_year]["Underpayment_Mitigations_Taken"] = Underpayment_Mitigations_Taken

            if Underpayment_Mitigations_Planned:
                data_by_year_dict[fiscal_year]["Underpayment_Mitigations_Planned"] = Underpayment_Mitigations_Planned

            for key, value in {
                "Data_Needed_Does_Not_Exist" : data_needed_does_not_exist,
                "Inability_to_Access_Data" : inability_to_access_data,
                "Failure_to_Access_Data" : failure_to_access_data,
                "Address_Location" : address_location,
                "Contractor_Provider_Status" : contractor_provider_status,
                "Financial": financial,
                "Underpayments_Amount": Underpayments_Amount
            }.items():
                if value is not None:
                    if "underpayments" not in data_by_year_dict[fiscal_year]:
                        data_by_year_dict[fiscal_year]["underpayments"] = {}
                    data_by_year_dict[fiscal_year]["underpayments"][key] = value

        technically_ip = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_TECHNICIALLY_IMPROPER_PAYMENTS, [program["Program_Name"]] + programFiscalYearRange)

        for row in technically_ip:
            fiscal_year = row["Fiscal_Year"]
            Technical_IP_Causes = row["Technical_IP_Causes"]
            Technical_IP_Amount = row["Technical_IP_Amount"]
            program_design_or_structural_issue = row["Program_Design_or_Structural_Issue"]
            Technical_IP_Actions_Taken = row["Technical_IP_Actions_Taken"]
            Technical_IP_Actions_Planned = row["Technical_IP_Actions_Planned"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            if Technical_IP_Actions_Taken:
                data_by_year_dict[fiscal_year]["Technical_IP_Actions_Taken"] = Technical_IP_Actions_Taken

            if Technical_IP_Actions_Planned:
                data_by_year_dict[fiscal_year]["Technical_IP_Actions_Planned"] = Technical_IP_Actions_Planned

            for key, value in {
                "Technical_IP_Causes" : Technical_IP_Causes,
                "Technical_IP_Amount" : Technical_IP_Amount,
                "Program_Design_or_Structural_Issue" : program_design_or_structural_issue
            }.items():
                if value is not None:
                    data_by_year_dict[fiscal_year][key] = value

        eligibility_information = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_ELIGIBILITY_INFORMATION, [program["Program_Name"]] + programFiscalYearRange)

        for row in eligibility_information:
            fiscal_year = row["Fiscal_Year"]
            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            # forces yaml dump to quote carriage returns
            theme_description = row["description"].encode('utf-8').decode('unicode_escape')

            if row["Payment_Type"] == "Underpayments":
                if 'underpayments_eligibility' not in data_by_year_dict[fiscal_year]:
                    data_by_year_dict[fiscal_year]['underpayments_eligibility'] = []
                data_by_year_dict[fiscal_year]['underpayments_eligibility'].append({
                    "Key": row["Column_names"],
                    "Value": row["Column_values"],
                    "Theme": row["theme"],
                    "Payment_Type": row["Payment_Type"],
                    "Theme_Description": theme_description
                })
            else:
                if 'overpayments_eligibility' not in data_by_year_dict[fiscal_year]:
                    data_by_year_dict[fiscal_year]['overpayments_eligibility'] = []
                data_by_year_dict[fiscal_year]['overpayments_eligibility'].append({
                    "Key": row["Column_names"],
                    "Value": row["Column_values"],
                    "Theme": row["theme"],
                    "Payment_Type": row["Payment_Type"],
                    "Theme_Description": theme_description
                })

        eligibility_information_aggregated = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_ELIGIBILITY_INFORMATION_AGGREGATED, [program["Program_Name"]] + programFiscalYearRange)

        for row in eligibility_information_aggregated:
            fiscal_year = row["Fiscal_Year"]
            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            if 'eligibility_aggregated' not in data_by_year_dict[fiscal_year]:
                data_by_year_dict[fiscal_year]['eligibility_aggregated'] = []

            # forces yaml dump to quote carriage returns
            theme_description = row["description"].encode('utf-8').decode('unicode_escape')

            data_by_year_dict[fiscal_year]['eligibility_aggregated'].append({
                "Theme": row["theme"],
                "Theme_Description": theme_description
            })

        unknown_payments = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_UNKNOWN_PAYMENTS, [program["Program_Name"]] + programFiscalYearRange)

        for row in unknown_payments:
            fiscal_year = row["Fiscal_Year"]
            Unknown_Why = row["Unknown_Why"]
            insufficient_documentation_to_determine = row["Insufficient_Documentation_to_Determine"]
            Unknown_Documentation_Why = row["Unknown_Documentation_Why"]
            Unknown_Mitigations_Taken = row["Unknown_Mitigations_Taken"]
            Unknown_Mitigations_Planned = row["Unknown_Mitigations_Planned"]
            Non_Monetary_Loss_Amount = row["Non_Monetary_Loss_Amount"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            if Unknown_Mitigations_Taken:
                data_by_year_dict[fiscal_year]["Unknown_Mitigations_Taken"] = Unknown_Mitigations_Taken

            if Unknown_Mitigations_Planned:
                data_by_year_dict[fiscal_year]["Unknown_Mitigations_Planned"] = Unknown_Mitigations_Planned

            for key, value in {
                "Unknown_Why" : Unknown_Why,
                "Insufficient_Documentation_to_Determine" : insufficient_documentation_to_determine,
                "Unknown_Documentation_Why" : Unknown_Documentation_Why,
                "Non_Monetary_Loss_Amount": Non_Monetary_Loss_Amount
            }.items():
                if value is not None:
                    data_by_year_dict[fiscal_year][key] = value

        unknown_payments_breakdown = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_UNKNOWN_PAYMENTS_BREAKDOWN, [program["Program_Name"]] + programFiscalYearRange)

        for row in unknown_payments_breakdown:
            fiscal_year = row["Fiscal_Year"]
            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            data_by_year_dict[fiscal_year][row["Name"]] = row["Column_values"]

        corrective_actions = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_CORRECTIVE_ACTIONS, [program["Program_Name"]] + programFiscalYearRange)

        for row in corrective_actions:
            fiscal_year = row["Fiscal_Year"]
            Corrective_Actions_Proportion = row["Corrective_Actions_Proportion"]
            Corrective_Actions_Adequacy = row["Corrective_Actions_Adequacy"]
            Corrective_Actions_Association = row["Corrective_Actions_Association"]
            Corrective_Actions_Implementation = row["Corrective_Actions_Implementation"]
            Corrective_Actions_Appropriateness = row["Corrective_Actions_Appropriateness"]
            Corrective_Actions_Adequacy_Association_Implementation = row["Corrective_Actions_Adequacy_Association_Implementation"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            data_by_year_dict[fiscal_year].update({
                key: value for key, value in {
                    "Corrective_Actions_Proportion" : Corrective_Actions_Proportion,
                    "Corrective_Actions_Adequacy" : Corrective_Actions_Adequacy,
                    "Corrective_Actions_Association" : Corrective_Actions_Association,
                    "Corrective_Actions_Implementation" : Corrective_Actions_Implementation,
                    "Corrective_Actions_Appropriateness" : Corrective_Actions_Appropriateness,
                    "Corrective_Actions_Adequacy_Association_Implementation": Corrective_Actions_Adequacy_Association_Implementation
                }.items() if value is not None
            })

        future_outlook = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_FUTURE_OUTLOOK, [program["Program_Name"]] + programFiscalYearRange)

        for row in future_outlook:
            fiscal_year = row["Fiscal_Year"]
            Future_Outlook_Has_Baseline = row["Future_Outlook_Has_Baseline"]
            Future_Outlook_Reduction_Vs_Estimated = row["Future_Outlook_Reduction_Vs_Estimated"]
            Is_Tolerable_Why = row["Is_Tolerable_Why"]
            Tolerable_Rate_Not_Determined_Reason = row["Tolerable_Rate_Not_Determined_Reason"]
            Is_Lowest_IP_And_Unknown_Rate = row["Is_Lowest_IP_And_Unknown_Rate"]
            Agency_Needs_Satisfied = row["Agency_Needs_Satisfied"]
            Resources_Requested_For_IP = row["Resources_Requested_For_IP"]
            outlays_current_year_plus_1_amount = row["Outlays_Current_Year+1_Amount"]
            ip_current_year_plus_1_amount = row["IP_Current_Year+1_Amount"]
            unknown_curent_year_plus_1_amount = row["Unknown_Curent_Year+1_Amount"]
            ip_unknown_current_year_plus_1_rate = row["IP_Unknown_Current_Year+1_Rate"]
            ip_unknown_target_rate = row["IP_Unknown_Target_Rate"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            data_by_year_dict[fiscal_year].update({
                key: value for key, value in {
                    "Future_Outlook_Has_Baseline" : Future_Outlook_Has_Baseline,
                    "Future_Outlook_Reduction_Vs_Estimated" : Future_Outlook_Reduction_Vs_Estimated,
                    "Is_Tolerable_Why" : Is_Tolerable_Why,
                    "Tolerable_Rate_Not_Determined_Reason" : Tolerable_Rate_Not_Determined_Reason,
                    "Is_Lowest_IP_And_Unknown_Rate" : Is_Lowest_IP_And_Unknown_Rate,
                    "Agency_Needs_Satisfied" : Agency_Needs_Satisfied,
                    "Resources_Requested_For_IP" : Resources_Requested_For_IP,
                    "Outlays_Current_Year_Plus_1_Amount" : outlays_current_year_plus_1_amount,
                    "IP_Current_Year_Plus_1_Amount" : ip_current_year_plus_1_amount,
                    "Unknown_Curent_Year_Plus_1_Amount" : unknown_curent_year_plus_1_amount,
                    "IP_Unknown_Current_Year_Plus_1_Rate" : ip_unknown_current_year_plus_1_rate,
                    "IP_Unknown_Target_Rate" : ip_unknown_target_rate
                }.items() if value is not None
            })

        additional_information = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_ADDITIONAL_INFORMATION, [program["Program_Name"]] + programFiscalYearRange)

        # do not populate if more than one value per fiscal year
        program_additional_information_by_year = defaultdict(set)

        for row in additional_information:
            fiscal_year = row["Fiscal_Year"]
            Program_Additional_Information = row["Program_Additional_Information"]
            IP_Accountability_Description = row["IP_Accountability_Description"]

            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}
            
            if Program_Additional_Information:
                program_additional_information_by_year[fiscal_year].add(Program_Additional_Information)

            if IP_Accountability_Description:
                data_by_year_dict[fiscal_year]["IP_Accountability_Description"] = IP_Accountability_Description

        for fiscal_year, values in program_additional_information_by_year.items():
            if len(values) == 1:
                data_by_year_dict[fiscal_year]["Program_Additional_Information"] = next(iter(values))

        for data_year in data_by_year_dict:
            # TODO: change to check for current years' keys / values
            data_by_year_dict[data_year]["Hide_Program_Results_Improper_Payments"] = False
            data_by_year_dict[data_year]["Hide_Program_Results_Unknown_Payments"] = False
            data_by_year_dict[data_year]["Hide_Program_Results_Corrective_Actions"] = \
                (
                    "Corrective_Actions_Proportion" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Corrective_Actions_Proportion"] is None or \
                    data_by_year_dict[data_year]["Corrective_Actions_Proportion"] == ''
                ) and (
                    "Corrective_Actions_Association" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Corrective_Actions_Association"] is None or \
                    data_by_year_dict[data_year]["Corrective_Actions_Association"] == ''
                ) and (
                    "Corrective_Actions_Adequacy" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Corrective_Actions_Adequacy"] is None or \
                    data_by_year_dict[data_year]["Corrective_Actions_Adequacy"] == ''
                ) and (
                    "Corrective_Actions_Implementation" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Corrective_Actions_Implementation"] is None or \
                    data_by_year_dict[data_year]["Corrective_Actions_Implementation"] == ''
                )

            data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Baseline_Table"] = \
                (
                    "Outlays_Current_Year_Plus_1_Amount" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Outlays_Current_Year_Plus_1_Amount"] is None or \
                    data_by_year_dict[data_year]["Outlays_Current_Year_Plus_1_Amount"] == 0
                ) and (
                    "IP_Current_Year_Plus_1_Amount" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["IP_Current_Year_Plus_1_Amount"] is None or \
                    data_by_year_dict[data_year]["IP_Current_Year_Plus_1_Amount"] == 0
                ) and (
                    "Unknown_Curent_Year_Plus_1_Amount" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Unknown_Curent_Year_Plus_1_Amount"] is None or \
                    data_by_year_dict[data_year]["Unknown_Curent_Year_Plus_1_Amount"] == 0
                ) and (
                    "IP_Unknown_Current_Year_Plus_1_Rate" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["IP_Unknown_Current_Year_Plus_1_Rate"] is None or \
                    data_by_year_dict[data_year]["IP_Unknown_Current_Year_Plus_1_Rate"] == 0
                ) and (
                    "IP_Unknown_Target_Rate" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["IP_Unknown_Target_Rate"] is None or \
                    data_by_year_dict[data_year]["IP_Unknown_Target_Rate"] == 0
                )
            data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Baseline"] = \
                (
                    "Future_Outlook_Has_Baseline" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Future_Outlook_Has_Baseline"] is None or \
                    data_by_year_dict[data_year]["Future_Outlook_Has_Baseline"] == ''
                ) and (
                    "Future_Outlook_Reduction_Vs_Estimated" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Future_Outlook_Reduction_Vs_Estimated"] is None or \
                    data_by_year_dict[data_year]["Future_Outlook_Reduction_Vs_Estimated"] == ''
                ) and data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Baseline_Table"]
            data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Explanation"] = \
                (
                    "Payment_Accuracy_Rate" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Payment_Accuracy_Rate"] is None or \
                    data_by_year_dict[data_year]["Payment_Accuracy_Rate"] == 0
                ) and (
                    "Is_Tolerable_Why" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Is_Tolerable_Why"] is None or \
                    data_by_year_dict[data_year]["Is_Tolerable_Why"] == ''
                ) and (
                    "Tolerable_Rate_Not_Determined_Reason" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Tolerable_Rate_Not_Determined_Reason"] is None or \
                    data_by_year_dict[data_year]["Tolerable_Rate_Not_Determined_Reason"] == ''
                ) and (
                    "rtp4_3" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["rtp4_3"] is None or \
                    data_by_year_dict[data_year]["rtp4_3"] == ''
                ) and (
                    "Is_Lowest_IP_And_Unknown_Rate" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Is_Lowest_IP_And_Unknown_Rate"] is None or \
                    data_by_year_dict[data_year]["Is_Lowest_IP_And_Unknown_Rate"] == ''
                )

            data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Needs"] = \
                (
                    "Agency_Needs_Satisfied" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Agency_Needs_Satisfied"] is None or \
                    data_by_year_dict[data_year]["Agency_Needs_Satisfied"] == ''
                ) and (
                    "Resources_Requested_For_IP" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Resources_Requested_For_IP"] is None or \
                    data_by_year_dict[data_year]["Resources_Requested_For_IP"] == ''
                )

            data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook"] = \
                data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Baseline"] and \
                data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Explanation"] and \
                data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook_Needs"]

            data_by_year_dict[data_year]["Hide_Program_Results_Additional_Information"] = \
                (
                    "IP_Accountability_Description" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["IP_Accountability_Description"] is None or \
                    data_by_year_dict[data_year]["IP_Accountability_Description"] == ''
                ) and (
                    "Program_Additional_Information" not in data_by_year_dict[data_year] or \
                    data_by_year_dict[data_year]["Program_Additional_Information"] is None or \
                    data_by_year_dict[data_year]["Program_Additional_Information"] == ''
                )

            # if at least two options are available (i.e. less than 4 sections hidden)
            data_by_year_dict[data_year]["Hide_Program_Results_Tabs"] = sum([
                data_by_year_dict[data_year]["Hide_Program_Results_Improper_Payments"],
                data_by_year_dict[data_year]["Hide_Program_Results_Unknown_Payments"],
                data_by_year_dict[data_year]["Hide_Program_Results_Corrective_Actions"],
                data_by_year_dict[data_year]["Hide_Program_Results_Future_Outlook"],
                data_by_year_dict[data_year]["Hide_Program_Results_Additional_Information"]
            ]) >= 4

        # older surveys submitted data for "Did not report" programs
        # not ideal, but this removes such entries after-the-fact
        keys_to_delete = []
        for key, value in data_by_year_dict.items():
            found = query.fetch_all(cursor, query.QUERY_TYPES.DID_NOT_REPORT, (program["Agency"], program["Program_Name"], key), key)
            if (len(found) > 0):
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data_by_year_dict[key]
        if (len(data_by_year_dict) == 0):
            # this removal could remove all years.  In that case, return without writing a yaml file
            return

        programObj["Data_By_Year"] = [
            {"Year": year, **attributes}
            for year, attributes in sorted(data_by_year_dict.items())
        ]

        scorecard_links = query.fetch_all(cursor, query.QUERY_TYPES.PROGRAM_SCORECARD_LINKS, (program["Program_Name"],))
        programObj["Scorecard_Links"] = []
        for row in scorecard_links:
            programObj["Scorecard_Links"].append({
                'QuarterYear': row['QuarterYear'],
                'Link': row['Link']
            })

        programObj["Hide_Integrity_Results"] = "Improper_Payments_Data_Years" not in programObj or \
            programObj["Improper_Payments_Data_Years"] is None or \
            programObj["Improper_Payments_Data_Years"] == '[]'
        programObj["Hide_Scorecard_Links"] = "Scorecard_Links" not in programObj or \
            programObj["Scorecard_Links"] is None or \
            len(programObj["Scorecard_Links"]) == 0
        programObj["Hide_Program_Results"] = "Data_By_Year" not in programObj or \
            programObj["Data_By_Year"] is None or \
            len(programObj["Data_By_Year"]) == 0

        with open(os.path.join(PROGRAM_SPECIFIC_DIR, program["Slug"] + ".md"), 'w', encoding='utf-8') as file:
            file.write('---\n')
            yaml.dump(programObj, file, allow_unicode=True)
            file.write('---\n')
    print("Successfully generated program-specific md files")

def add_actions_taken(cursor, years, program, data_by_year_dict):
    for fiscal_year in years:
        actions_taken = query.fetch_all(cursor, query.QUERY_TYPES.ACTIONS_TAKEN, (program, fiscal_year), fiscal_year)

        if len(actions_taken) > 0:
            if fiscal_year not in data_by_year_dict:
                data_by_year_dict[fiscal_year] = {}

            data_by_year_dict[fiscal_year]["Actions_Taken"] = actions_taken

def generate_congressional_reports_pages(cursor: sqlite3.Cursor):
    if os.path.exists(CONGRESSIONAL_REPORTS_DIR):
        shutil.rmtree(CONGRESSIONAL_REPORTS_DIR)

    os.makedirs(CONGRESSIONAL_REPORTS_DIR, exist_ok=True)

    yearsToGenerate = list(range(config.FISCAL_YEAR - config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED + 1, config.FISCAL_YEAR + 1))
    congressionalReportsYears = [config.FISCAL_YEAR, config.FISCAL_YEAR - config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED + 1]

    agencyNameRows = query.fetch_all(
        cursor,
        query.QUERY_TYPES.AGENCY_NAMES,
        ()
    )
    agencyNameRowsLookup = { agencyNameRow["Agency_Acronym"]: agencyNameRow["Agency_Name"] for agencyNameRow in agencyNameRows }

    agencyRows = query.fetch_all(
        cursor,
        query.QUERY_TYPES.AGENCIES_HAVING_CONGRESSIONAL_DATA,
        congressionalReportsYears
    )

    # Landing page
    with open(CONGRESSIONAL_REPORTS_MARKUP_PATH, 'w', encoding='utf-8') as file:
        yamlData = {
            'title': "Congressional Reports",
            'layout': 'congressional-reports',
            'permalink': '/resources/congressional-reports'
        }
        file.write('---\n')
        yaml.dump(yamlData, file, allow_unicode=True)
        file.write('---\n')

    # Generate and write reports
    reports_with_data = [] # (report_id, agency_code, year)
    for year in yearsToGenerate:
        for report in [report for report in config.CONGRESSIONAL_REPORTS if not report["IsGovernmentWide"]]:
            for agency in agencyRows:
                agency_report = congressional_reports.AgencyReport(
                    cursor,
                    year,
                    agency["agency"],
                    report["Id"]
                )

                if agency_report.has_data():
                    agency_report.to_yaml(CONGRESSIONAL_REPORTS_DIR)
                    reports_with_data.append((report["Id"], agency["agency"], year))

        for report in [report for report in config.CONGRESSIONAL_REPORTS if report["IsGovernmentWide"]]:
            governmentwide_report = congressional_reports.GovernmentWideReport(
                cursor,
                year,
                report["Id"]
            )

            if governmentwide_report.has_data():
                governmentwide_report.to_yaml(CONGRESSIONAL_REPORTS_DIR)
                reports_with_data.append((report["Id"], '_', year))

    generate_congressional_shared_data(yearsToGenerate, agencyNameRowsLookup, agencyRows, reports_with_data)

    print("Successfully generated congressional reports md files")

def generate_shared_data():
    with open(SHARED_DATA_PATH, 'w', encoding='utf-8') as file:
        yamlData = {
            'Fiscal_Year': config.FISCAL_YEAR
        }
        file.write('---\n')
        yaml.dump(yamlData, file, allow_unicode=True)
        file.write('---\n')

def generate_congressional_shared_data(yearsToGenerate, agencyNameRowsLookup, agencyRows, reportsWithData):
    try:
        os.remove(CONGRESSIONAL_REPORTS_SHARED_DATA_PATH)
    except OSError:
        pass
    with open(CONGRESSIONAL_REPORTS_SHARED_DATA_PATH, 'w', encoding='utf-8') as file:
        agencyDropdown = []
        for row in agencyRows:
            agencyDropdown.append({
                'Code': row["agency"],
                'Name': agencyNameRowsLookup[row["agency"]]
            })

        yearsDropdown = [ year for year in yearsToGenerate ]
        reportsDropdown = [ {
            "Id": str(report["Id"]),
            "Name": report["Name"],
            "IsGovernmentWide": report["IsGovernmentWide"]
        } for report in config.CONGRESSIONAL_REPORTS ]

        reportsWithDataHierarchy = {}
        for report in reportsWithData:
            reportId = report[0]
            agency = report[1]
            year = report[2]
            if reportId not in reportsWithDataHierarchy:
                reportsWithDataHierarchy[reportId] = {}
            if agency not in reportsWithDataHierarchy[reportId]:
                reportsWithDataHierarchy[reportId][agency] = []
            reportsWithDataHierarchy[reportId][agency].append(year)

        yamlData = {
            'Years_Dropdown': yearsDropdown,
            'Agencies_Dropdown': agencyDropdown,
            'Reports_Dropdown': reportsDropdown,
            'Reports_With_Data': reportsWithDataHierarchy
        }
        file.write('---\n')
        yaml.dump(yamlData, file, allow_unicode=True)
        file.write('---\n')

def main():
    try:
        conn = sqlite3.connect(DB_FULL_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        generate_shared_data()
        generate_home_page(cursor)
        generate_agency_programs_page(cursor)
        generate_agency_specific_pages(cursor)
        generate_placeholder_agency_specific_pages(cursor)
        generate_congressional_reports_pages(cursor)
        generate_program_specific_pages(cursor)

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()
if __name__ == "__main__":
    main()