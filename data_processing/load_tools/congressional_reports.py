import config
from itertools import groupby
from load_tools import query
import os
import re
import sqlite3
import yaml

class Report():
    def __init__(self, cursor: sqlite3.Cursor, year, id):
        self.cursor = cursor
        self.year = year
        self.id = id
        self.report_config = self.get_config()
        self.data = {
            'title': self.report_config["Name"],
            'layout': 'congressional-reports',
            'Fiscal_Year': year,
            'Report_Id': str(id),
            'Requirements': self.get_requirements()
        }

    def format_answer(self, answer, type):
        if type["type"] == config.CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT:
            parts = re.split(r'(?<!\\),', answer)
            parts.sort()
            # unescape commas that were previously escaped in extract queries
            answer = [re.sub(r'\\\\,', ',', part) for part in parts]
        return answer

    def get_requirements(self):
        return list(map(lambda x: {
            "Indent": x["indent"],
            "Type": x["type"].name,
            "Text": x["text"]
        }, config.CONGRESSIONAL_REPORTS_REQUIREMENTS_MAPPING[str(self.year)][str(self.id)]))

    def get_config(self):
        return next((item for item in config.CONGRESSIONAL_REPORTS if item["Id"] == self.id), None)

    def to_yaml(self, directory):
        with open(os.path.join(directory, self.filename + ".md"), 'w', encoding='utf-8') as file:
            file.write('---\n')
            yaml.dump(self.data, file, allow_unicode=True)
            file.write('---\n')

class GovernmentWideReport(Report):
    def __init__(self, cursor: sqlite3.Cursor, year, id):
        super().__init__(cursor, year, id)
        self.filename = str(year) + '_' + str(self.id)

        self.data['permalink'] = '/resources/congressional-reports/' + self.filename
        self.data['Agency'] = '*'
        self.data['Agency_Name'] = "Government Wide"
        self.data['Page_Name'] = self.filename

        # Set data for report-specific sections
        self.fetch_improper_estimates_data()
        self.fetch_dnp_data()

    # Special section for congressional report #6 only
    def fetch_improper_estimates_data(self):
        if (self.id != 6):
            return

        self.data["IPData"] = {
            "Compliance": query.fetch_all(self.cursor, query.QUERY_TYPES.IP_GW_SURVEY_RESULTS, (self.year,), self.year),
            "Stats": query.fetch_all(self.cursor, query.QUERY_TYPES.IP_GW_STATS, (self.year,), self.year)[0]
        }

    # Special section for congressional report #9 only
    def fetch_dnp_data(self):
        if (self.id != 9):
            return

        self.data["DoNotPayData"] = {
            "Evaluations": query.fetch_all(self.cursor, query.QUERY_TYPES.DNP_SURVEY_RESULTS, (self.year,), self.year),
            "Stats": query.fetch_all(self.cursor, query.QUERY_TYPES.DNP_GW_STATS, (self.year,), self.year)[0]
        }

class AgencyReport(Report):
    def __init__(self, cursor: sqlite3.Cursor, year, agency_code, id, SLUGIFIED_PROGRAM_NAME_MAPPINGS):
        super().__init__(cursor, year, id)
        self.agency_code = agency_code
        self.SLUGIFIED_PROGRAM_NAME_MAPPINGS = SLUGIFIED_PROGRAM_NAME_MAPPINGS
        self.filename = str(year) + '_' + str(agency_code) + '_' + str(self.id)

        self.data['permalink'] = '/resources/congressional-reports/' + self.filename
        self.data['Agency'] = agency_code
        self.data['Agency_Name'] = query.get_agency_name(cursor, agency_code)
        self.data['Page_Name'] = self.filename

        # Set data for general sections
        self.fetch_agency_data()
        self.fetch_program_data()

        # Set data for report-specific sections
        self.fetch_risk_assessments()
        self.fetch_high_priority_links()
        self.fetch_actions_taken_data()

    def get_agency_survey_view(self):
        current_year_config = next((cfg for cfg in config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING if cfg["Year"] == self.year), None)

        if current_year_config is None:
            return None
        else:
            return current_year_config["AgencyReports"].get(str(self.id), None)

    def get_program_survey_view(self):
        current_year_config = next((cfg for cfg in config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING if cfg["Year"] == self.year), None)

        if current_year_config is None:
            return None
        else:
            return current_year_config["ProgramReports"].get(str(self.id), None)

    def get_agency_survey_name(self):
        return self.report_config.get("SurveyName", None)

    def get_agency_survey_field_mapping(self):
        return config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING[str(self.year)].get(str(self.id), None)

    def get_program_survey_field_mapping(self):
        return config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING_PROGRAMS[str(self.year)].get(str(self.id), None)

    def fetch_agency_data(self):
        agency_survey_view = self.get_agency_survey_view()
        agency_survey_field_mapping = self.get_agency_survey_field_mapping()

        if agency_survey_view is None:
            return

        survey_results = query.fetch_cr_survey_agency_results(self.cursor, agency_survey_view, self.year)
        survey_results_filtered = [result for result in survey_results if result["Agency"] == self.agency_code]

        if len(survey_results_filtered) > 0:
            self.data["SurveyName"] = self.get_agency_survey_name()
            self.data["SurveyData"] = []

        for survey_result in survey_results_filtered:
            mapping = agency_survey_field_mapping[survey_result["Key"]]
            self.data["SurveyData"].append({
                "Heading": mapping["heading"],
                "Subheading": mapping["subheading"],
                "Answer": self.format_answer(survey_result["Answer"], mapping),
                "SortOrder": survey_result["SortOrder"],
                "Key": survey_result["Key"],
                "Type": mapping["type"].name
            })

    def fetch_program_data(self):
        program_survey_view = self.get_program_survey_view()
        program_survey_field_mapping = self.get_program_survey_field_mapping()

        if program_survey_view is None:
            return

        survey_results = query.fetch_cr_survey_program_results(self.cursor, program_survey_view, self.year)
        survey_results_filtered = [result for result in survey_results if result["Agency"] == self.agency_code]
        survey_results_by_program = groupby(survey_results_filtered, key=lambda x: x["Program_Name"])

        if len(survey_results_filtered) > 0:
            self.data["ProgramSurveyData"] = []

        program_sort_order = 0
        for program_name, survey_results in survey_results_by_program:
            answers = list(map(lambda row: {
                "Agency": row["Agency"],
                "Heading": program_survey_field_mapping[row["Key"]]["heading"],
                "Subheading": program_survey_field_mapping[row["Key"]]["subheading"],
                "Answer": self.format_answer(row["Answer"], program_survey_field_mapping[row["Key"]]),
                "SortOrder": row["SortOrder"],
                "Key": row["Key"],
                "Type": program_survey_field_mapping[row["Key"]]["type"].name
            }, survey_results))

            if len(answers) > 0:
                self.data["ProgramSurveyData"].append({
                    "Program": program_name,
                    "Answers": answers,
                    "SortOrder": program_sort_order
                })
                program_sort_order += 1

    # Special section for congressional report #1 only
    def fetch_risk_assessments(self):
        if self.id != 1:
            return

        assessments = query.fetch_all(
            self.cursor,
            query.QUERY_TYPES.RISK_ASSESSMENTS, (self.agency_code, self.year),
            self.year
        )

        self.data["Hide_Survey"] = True
        if len(assessments) > 0:
            self.data["Risks"] = {
                "Assessments": list(map(lambda risk: {
                    "Program_Name": risk["Program_Name"],
                    "Susceptible": risk["Susceptible"],
                    "Fiscal_Year": risk["Fiscal_Year"],
                    "Slug": self.SLUGIFIED_PROGRAM_NAME_MAPPINGS[risk["Program_Name"]] if risk["Program_Name"] in self.SLUGIFIED_PROGRAM_NAME_MAPPINGS else None
                }, assessments)),
                "AdditionalInformation": query.get_agency_survey_answer(self.cursor, self.year, self.agency_code, query.KEY_TYPES.RISKS_ADDITIONAL_INFORMATION),
                "SubstantialChangesMade": query.get_agency_survey_answer(self.cursor, self.year, self.agency_code, query.KEY_TYPES.RISKS_SUBSTANTIAL_CHANGES_MADE)
            }

    # Special section for congressional report #2 only
    def fetch_high_priority_links(self):
        if self.id != 2:
            return

        self.data["High_Priority_Links"] = query.fetch_all(
            self.cursor,
            query.QUERY_TYPES.HIGH_PRIORITY_SCORECARD_LINKS,
            (self.year, self.agency_code),
            self.year
        )

    # Special sections for congressional report #4 only
    def fetch_actions_taken_data(self):
        if self.id != 4:
            return

        if "ProgramSurveyData" not in self.data:
            return

        for program_data in self.data["ProgramSurveyData"]:
            actions_taken = query.fetch_all(self.cursor, query.QUERY_TYPES.ACTIONS_TAKEN, (program_data["Program"], self.year), self.year)

            if len(actions_taken) > 0:
                program_data["ActionsTaken"] = actions_taken

            additional_data = query.fetch_all(self.cursor, query.QUERY_TYPES.ACTIONS_TAKEN_ADDITIONAL_INFO, (program_data["Program"], self.agency_code, self.year), self.year)
            if len(additional_data) > 0:
                program_data["ActionsTakenAdditionalData"] = additional_data