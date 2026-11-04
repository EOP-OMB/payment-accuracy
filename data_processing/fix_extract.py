"""
Apply known corrections to extracted CSV files.

    python data_processing/fix_extract.py
"""

import csv
import os
from io import StringIO

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_DIR = os.path.join(SCRIPT_DIR, "extracted")


def extracted_path(filename):
    return os.path.join(EXTRACTED_DIR, filename)


def read_text(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf"), newline


def write_text(path, text, bom, newline):
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if newline != "\n":
        normalized = normalized.replace("\n", newline)
    raw = normalized.encode("utf-8")
    if bom:
        raw = b"\xef\xbb\xbf" + raw
    with open(path, "wb") as handle:
        handle.write(raw)


def csv_records(text):
    """Split CSV text into records, keeping quoted newlines inside a record."""
    records = []
    start = 0
    in_quotes = False
    index = 0
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    length = len(normalized)
    while index < length:
        char = normalized[index]
        if char == '"':
            if in_quotes and index + 1 < length and normalized[index + 1] == '"':
                index += 2
                continue
            in_quotes = not in_quotes
        elif char == "\n" and not in_quotes:
            records.append(normalized[start:index])
            start = index + 1
        index += 1
    if start < length:
        records.append(normalized[start:])
    return records, normalized.endswith("\n")


def parse_record(record):
    if record == "":
        return []
    return next(csv.reader([record]))


def render_row(row, quote_all):
    buffer = StringIO()
    writer = csv.writer(
        buffer,
        quoting=csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL,
        lineterminator="",
    )
    writer.writerow(row)
    return buffer.getvalue()


def fix_contractor_of_provider():
    filename = "Eligibility_Themes.csv"
    path = extracted_path(filename)
    text, bom, newline = read_text(path)
    replacements = text.count("Contractor of Provider")
    if replacements:
        text = text.replace("Contractor of Provider", "Contractor or Provider")
        write_text(path, text, bom, newline)
        print(f"{replacements} Contractor or Provider item(s) fixed in {filename}")


def fix_dod_acronyms():
    filename = "IP_Agency_POCs.csv"
    path = extracted_path(filename)
    text, bom, newline = read_text(path)
    records, trailing_newline = csv_records(text)
    if not records:
        return

    header = parse_record(records[0])
    acronym_index = header.index("Agency_Acronym")
    replacements = 0
    for index, record in enumerate(records[1:], start=1):
        row = parse_record(record)
        if len(row) <= acronym_index or row[acronym_index].strip() != "DOD":
            continue
        row[acronym_index] = "DOW"
        records[index] = render_row(row, record.startswith('"'))
        replacements += 1

    if replacements:
        text = newline.join(records)
        if trailing_newline:
            text += newline
        write_text(path, text, bom, newline)
        print(f"{replacements} DOD acronym(s) replaced in {filename}")

def fix_dod_name():
    filename = "IP_Agency_POCs.csv"
    path = extracted_path(filename)
    text, bom, newline = read_text(path)
    records, trailing_newline = csv_records(text)
    if not records:
        return

    header = parse_record(records[0])
    name_index = header.index("Agency_Name")
    replacements = 0
    for index, record in enumerate(records[1:], start=1):
        row = parse_record(record)
        if len(row) <= name_index or row[name_index].strip() != "Department of Defense":
            continue
        row[name_index] = "Department of War"
        records[index] = render_row(row, record.startswith('"'))
        replacements += 1

    if replacements:
        text = newline.join(records)
        if trailing_newline:
            text += newline
        write_text(path, text, bom, newline)
        print(f"{replacements} DOD names(s) replaced in {filename}")


def remove_blank_agency_lines(filename):
    path = extracted_path(filename)
    text, bom, newline = read_text(path)
    records, trailing_newline = csv_records(text)
    if not records:
        return 0

    header = parse_record(records[0])
    agency_index = header.index("Agency")
    kept = [records[0]]
    removals = 0
    for record in records[1:]:
        row = parse_record(record)
        agency = row[agency_index].strip() if len(row) > agency_index else ""
        if agency == "":
            removals += 1
            continue
        kept.append(record)

    if removals:
        text = newline.join(kept)
        if trailing_newline:
            text += newline
        write_text(path, text, bom, newline)
        print(f"{removals} blank agency line(s) removed in {filename}")
    return removals


def remove_blank_agencies_from_all_programs():
    remove_blank_agency_lines("MY_OMB_ImproperPayment_Payment_Accuracy_All_Program_vw.csv")


def remove_blank_agencies_from_root_causes():
    remove_blank_agency_lines("MY_OMB_ImproperPayment_Payment_IP_Root_Causes_vw.csv")


def main():
    print("Fixing known quality issues in extracted CSV files...")
    fix_contractor_of_provider()
    fix_dod_acronyms()
    fix_dod_name()
    remove_blank_agencies_from_all_programs()
    remove_blank_agencies_from_root_causes()
    print("Quality issues fixed.")


if __name__ == "__main__":
    main()
