"""
Apply overrides to extracted CSV files.

    python data_processing/override_extract.py

When extracted/overrides/Program_Names.csv exists, replace column 1 with column 2
in the program-name field of each extract listed below. Matching is case
insensitive. The replacement keeps the case from the overrides file, except
RiskAssessmentMethodologyChanges.csv, which is written in uppercase.

When extracted/overrides/Risk_Assessments.csv exists, update
Risk_Assessment_FULL_FY25.csv. A Remove/Add value containing "remove" deletes
rows with the same Agency, Fiscal_Year, and Program_Name. A value containing
"add" appends the first five columns. Matching is case insensitive.
"""

import os

from fix_extract import (
    csv_records,
    extracted_path,
    parse_record,
    read_text,
    render_row,
    write_text,
)

# filename, program-name column, write the replacement in uppercase
PROGRAM_NAME_FILES = [
    ("FPIMapping.csv", "Program Name", False),
    ("KPI_ImproperPaymentsSurveyOverpaymentRecovery_vw_IP.csv", "Program Name", False),
    ("KPI_ImproperPaymentsSurveyProgressGoal_vw_IP.csv", "Program Name", False),
    ("KPI_ImproperPaymentsSurveyRecentAccomplishment_vw_IP.csv", "Program Name", False),
    ("KPI_ImproperPaymentSurveyRootCause_vw_IP.csv", "Program Name", False),
    ("LastRiskAssessmentByProgram.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Mitigation_Strategies_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Payment_Accuracy_Principal_Table_Columns_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Payment_Confirmed_Fraud_vw.csv", "Program_or_Activity", False),
    ("MY_OMB_ImproperPayment_Payment_IP_Root_Causes_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Payment_Program_Compliance_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_Payment_Recovery_Details_unpivotted_vw.csv", "Program_Name", False),
    ("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw-Congressional.csv", "Program Name", False),
    ("MY_OMB_ImproperPayment_PaymentAccuracy_ProgramData_raw_vw.csv", "Program Name", False),
    ("Program_Scorecard_Links.csv", "Program_Name", False),
    ("Risk_Assessment_FULL_FY25.csv", "Program_Name", False),
    ("RiskAssessmentMethodologyChanges.csv", "Program_Name", True),
]


RISK_ASSESSMENT_FILENAME = "Risk_Assessment_FULL_FY25.csv"
RISK_ASSESSMENT_COLUMNS = [
    "Agency",
    "Fiscal_Year",
    "Program_Name",
    "Fiscal_Year_Last_Conducted",
    "Susceptible",
]
RISK_ASSESSMENT_KEY = ["Agency", "Fiscal_Year", "Program_Name"]
RISK_ASSESSMENT_ACTION = "Remove/Add"


def overrides_path(filename):
    return extracted_path(os.path.join("overrides", filename))


def row_value(row, index):
    if index >= len(row):
        return ""
    return row[index].strip()


def render_quoted_nonempty(row):
    """Quote populated fields and leave empty fields bare, matching the extract."""
    parts = []
    for value in row:
        if value == "":
            parts.append("")
        else:
            parts.append(render_row([value], True))
    return ",".join(parts)


def load_program_name_overrides(path):
    """Map casefolded current names to the replacement text in column 2."""
    text, _, _ = read_text(path)
    records, _ = csv_records(text)
    mapping = {}
    for record in records[1:]:
        row = parse_record(record)
        if len(row) < 2:
            continue
        current = row[0].strip()
        new = row[1].strip()
        if current == "" or new == "":
            continue
        mapping[current.casefold()] = new
    return mapping


def apply_program_name_overrides(filename, column, mapping, uppercase):
    path = extracted_path(filename)
    text, bom, newline = read_text(path)
    records, trailing_newline = csv_records(text)
    if not records:
        return

    header = parse_record(records[0])
    column_index = header.index(column)
    replacements = 0
    for index, record in enumerate(records[1:], start=1):
        row = parse_record(record)
        if len(row) <= column_index:
            continue
        new = mapping.get(row[column_index].strip().casefold())
        if new is None:
            continue
        if uppercase:
            new = new.upper()
        if row[column_index] == new:
            continue
        row[column_index] = new
        records[index] = render_row(row, record.startswith('"'))
        replacements += 1

    if replacements:
        text = newline.join(records)
        if trailing_newline:
            text += newline
        write_text(path, text, bom, newline)
        print(f"{replacements} program name(s) updated in {filename}")


def apply_program_name_override_file():
    path = overrides_path("Program_Names.csv")
    if not os.path.exists(path):
        print("Program name overrides file not found.")
        return

    mapping = load_program_name_overrides(path)
    if not mapping:
        print("No program name overrides to apply.")
        return

    for filename, column, uppercase in PROGRAM_NAME_FILES:
        apply_program_name_overrides(filename, column, mapping, uppercase)


def load_risk_assessment_overrides(path):
    """Return keys to delete and rows to append from Risk_Assessments.csv."""
    text, _, _ = read_text(path)
    records, _ = csv_records(text)
    if not records:
        return set(), []

    header = parse_record(records[0])
    action_index = header.index(RISK_ASSESSMENT_ACTION)
    key_indexes = [header.index(name) for name in RISK_ASSESSMENT_KEY]
    remove_keys = set()
    add_rows = []
    for record in records[1:]:
        row = parse_record(record)
        action = row_value(row, action_index).casefold()
        if "remove" in action:
            remove_keys.add(tuple(row_value(row, index).casefold() for index in key_indexes))
        elif "add" in action:
            add_rows.append([row_value(row, index) for index in range(len(RISK_ASSESSMENT_COLUMNS))])
    return remove_keys, add_rows


def apply_risk_assessment_overrides():
    filename = RISK_ASSESSMENT_FILENAME
    path = overrides_path("Risk_Assessments.csv")
    if not os.path.exists(path):
        print("Risk assessment overrides file not found.")
        return

    remove_keys, add_rows = load_risk_assessment_overrides(path)
    if not remove_keys and not add_rows:
        print("No risk assessment overrides to apply.")
        return

    text, bom, newline = read_text(extracted_path(filename))
    records, trailing_newline = csv_records(text)
    if not records:
        return

    header = parse_record(records[0])
    key_indexes = [header.index(name) for name in RISK_ASSESSMENT_KEY]
    kept = [records[0]]
    removals = 0
    for record in records[1:]:
        row = parse_record(record)
        key = tuple(row_value(row, index).casefold() for index in key_indexes)
        if key in remove_keys:
            removals += 1
            continue
        kept.append(record)

    for add_row in add_rows:
        kept.append(render_quoted_nonempty(add_row))

    if removals or add_rows:
        updated = newline.join(kept)
        if trailing_newline:
            updated += newline
        write_text(extracted_path(filename), updated, bom, newline)
    if removals:
        print(f"{removals} risk assessment row(s) removed from {filename}")
    if add_rows:
        print(f"{len(add_rows)} risk assessment row(s) added to {filename}")


def main():
    print("Applying data overrides to extracted CSV files...")
    apply_program_name_override_file()
    apply_risk_assessment_overrides()
    print("Data overrides applied.")


if __name__ == "__main__":
    main()
