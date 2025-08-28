from enum import Enum

"""
Store various constants used across the data processing process.
"""

FISCAL_YEAR = 2024

# expected format:  Q<1-4> YYYY
LAST_QUARTERLY_SURVEY = "Q1 2025"
COUNT_GOVERNMENT_WIDE_YEARS_DISPLAYED = 5
COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED = 4
COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED_FOR_RECOVERY = 5
COUNT_PROGRAM_SPECIFIC_YEARS_DISPLAYED = 4
COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED = 2

DEFAULT_SURVEY_NAME = "Survey Responses"

CONGRESSIONAL_REPORTS = [
    {
        "Id": 1,
        "Name": "Agency Risk Assessments Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 2,
        "Name": "Agency High-Priority Program Report",
        "SurveyName": "Actions to Recover Improper Payments",
        "IsGovernmentWide": False
    },
    {
        "Id": 3,
        "Name": "Improper Payment and Unknown Payment Estimation Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 4,
        "Name": "Agency Actions to Reduce Improper Payments Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 5,
        "Name": "Agency Actions to Recover Improper Payments Identified in a Recovery Audit Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 6,
        "Name": "OMB Government Wide Improper Payment Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": True
    },
    {
        "Id": 7,
        "Name": "Agency Compliance Plan",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 8,
        "Name": "Agency Noncompliance Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": False
    },
    {
        "Id": 9,
        "Name": "OMB Do Not Pay Initiative Report",
        "SurveyName": "Survey Responses",
        "IsGovernmentWide": True
    }
]

CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING = [
    {
        "Year": 2023,
        "AgencyReports": {
            "1": "congressional_report_1_2024",
            "2": "congressional_report_2_2024",
            "5": "congressional_report_5_2024",
            "7": "congressional_report_7_2024",
            "8": "congressional_report_8_2024",
        },
        "ProgramReports": {
            "2": "congressional_report_2_2024_programs",
            "3": "congressional_report_3_2024_programs",
            "4": "congressional_report_4_2024_programs",
        }
    },
    {
        "Year": 2024,
        "AgencyReports": {
            "1": "congressional_report_1_2024",
            "2": "congressional_report_2_2024",
            "5": "congressional_report_5_2024",
            "7": "congressional_report_7_2024",
            "8": "congressional_report_8_2024",
        },
        "ProgramReports": {
            "2": "congressional_report_2_2024_programs",
            "3": "congressional_report_3_2024_programs",
            "4": "congressional_report_4_2024_programs",
        }
    },
    {
        "Year": 2025,
        "AgencyReports": {
            "1": "congressional_report_1_2025",
            "2": "congressional_report_2_2025",
            "5": "congressional_report_5_2025",
            "7": "congressional_report_7_2024",
            "8": "congressional_report_8_2024",
        },
        "ProgramReports": {
            "2": "congressional_report_2_2025_programs",
            "3": "congressional_report_3_2024_programs",
            "4": "congressional_report_4_2025_programs",
        }
    }
]

class CONGRESSIONAL_REPORTS_FIELD_TYPES(Enum):
    TEXT = 1
    MILLIONS_OF_DOLLARS = 2
    PERCENTAGE = 3
    MULTISELECT_TEXT = 4

class CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES(Enum):
    BOLD = 1
    ITALICIZED = 2
    REGULAR = 3

CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING = {
    "2023": {
        "1": {
            "raa6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa6_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            }
        },
        "2": {
            "ara2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            }
        },
        "5": {
            "arp17": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Conditions Giving Rise to Improper Payments Identified in Recovery Audits, How Those Conditions are Being Resolved, & Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            },
            "ara2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Conditions Giving Rise to Improper Payments Identified in Recovery Audits, How Those Conditions are Being Resolved, & Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            },
            "arp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "arp3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "arp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used to administer the Recovery Audits and Activities Program"
            },
            "arp8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for a Financial Management Improvement Program"
            },
            "arp9": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for the original purpose"
            },
            "arp10": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for Inspector General Activities"
            },
            "arp11": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Returned to Treasury"
            },
            "arp12": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Returned to the Original Account"
            },
            "arp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp5_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp14": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "0 to 6 Months Outstanding"
            },
            "arp15": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "6 to 12 Months Outstanding"
            },
            "arp4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "arp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Justification for the Determination that Performing Recovery Audits are Not Cost-Effective",
                "subheading": ""
            }
        },
        "7": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "Non-Compliant Programs",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Measurable Milestones To Be Accomplished in Order to Achieve Compliance For Each Program",
                "subheading": ""
            },
            "cap3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Senior Agency Official Accountable for Bringing Each Program into Compliance",
                "subheading": ""
            },
            "cap4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Accountability Mechanism Tied to the Success of the Senior Agency Official Bringing Each Program into Compliance",
                "subheading": ""
            }
        },
        "8": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "List of Each Program That Was Determined To Not Be In Compliance",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Actions That Are Planned to Bring Each Program into Compliance",
                "subheading": ""
            }
        }
    },
    "2024": {
        "1": {
            "raa6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa6_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            }
        },
        "2": {
            "ara2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            }
        },
        "5": {
            "arp17": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Conditions Giving Rise to Improper Payments Identified in Recovery Audits, How Those Conditions are Being Resolved, & Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            },
            "ara2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Conditions Giving Rise to Improper Payments Identified in Recovery Audits, How Those Conditions are Being Resolved, & Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            },
            "arp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "arp3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "arp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used to administer the Recovery Audits and Activities Program"
            },
            "arp8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for a Financial Management Improvement Program"
            },
            "arp9": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for the original purpose"
            },
            "arp10": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Used for Inspector General Activities"
            },
            "arp11": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Returned to Treasury"
            },
            "arp12": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": "Returned to the Original Account"
            },
            "arp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp5_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp14": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "0 to 6 Months Outstanding"
            },
            "arp15": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "6 to 12 Months Outstanding"
            },
            "arp4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "arp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Justification for the Determination that Performing Recovery Audits are Not Cost-Effective",
                "subheading": ""
            }
        },
        "7": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "Non-Compliant Programs",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Measurable Milestones To Be Accomplished in Order to Achieve Compliance For Each Program",
                "subheading": ""
            },
            "cap3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Senior Agency Official Accountable for Bringing Each Program into Compliance",
                "subheading": ""
            },
            "cap4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Accountability Mechanism Tied to the Success of the Senior Agency Official Bringing Each Program into Compliance",
                "subheading": ""
            }
        },
        "8": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "List of Each Program That Was Determined To Not Be In Compliance",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Actions That Are Planned to Bring Each Program into Compliance",
                "subheading": ""
            }
        }
    },
    "2025": {
        "1": {
            "raa6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa6_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa7_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "",
                "subheading": ""
            },
            "raa8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "",
                "subheading": ""
            }
        },
        "2": {
            "arp17_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Methods Used to Recover Improper Payments Identified in Recovery Audits"
                "",
                "subheading": ""
            }
        },
        "5": {
            "arp17_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Conditions Giving Rise to Improper Payments Identified in Recovery Audits, How Those Conditions are Being Resolved, & Methods Used to Recover Improper Payments Identified in Recovery Audits",
                "subheading": ""
            },
            "arp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "arp3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Recovered",
                "subheading": ""
            },
            "dis1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "How Recovered Amounts Have Been Disposed Of",
                "subheading": ""
            },
            "arp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp5_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Outstanding",
                "subheading": ""
            },
            "arp14": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "0 to 6 Months Outstanding"
            },
            "arp15": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Aging Schedule of the Amounts Outstanding",
                "subheading": "6 to 12 Months Outstanding"
            },
            "arp4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "arp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Overpayment Amount Determined to Not Be Collectible",
                "subheading": ""
            },
            "ara2_3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Justification for the Determination that Performing Recovery Audits are Not Cost-Effective",
                "subheading": ""
            }
        },
        "7": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "Non-Compliant Programs",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Measurable Milestones To Be Accomplished in Order to Achieve Compliance For Each Program",
                "subheading": ""
            },
            "cap3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Senior Agency Official Accountable for Bringing Each Program into Compliance",
                "subheading": ""
            },
            "cap4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Accountability Mechanism Tied to the Success of the Senior Agency Official Bringing Each Program into Compliance",
                "subheading": ""
            }
        },
        "8": {
            "com1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Compliance Status",
                "subheading": ""
            },
            "pcp01_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "heading": "List of Each Program That Was Determined To Not Be In Compliance",
                "subheading": ""
            },
            "CAP5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "heading": "Actions That Are Planned to Bring Each Program into Compliance",
                "subheading": ""
            }
        }
    }
}

CONGRESSIONAL_REPORTS_REQUIREMENTS_MAPPING = {
    "2023": {
        "1": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(a)(3)(C)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(C) ANNUAL REPORT.—Each executive agency shall publish an annual report that includes—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) a listing of each program or activity (with annual outlays greater than $10M),  including the date on which the program or activity was most recently assessed for risk",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) a listing of any program or activity for which the executive agency makes any substantial changes to the (risk assessment) methodologies",
            }
        ],
        "2": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(b)(2)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(2) REPORT ON HIGH-PRIORITY IMPROPER PAYMENTS.—...each executive agency with a (high-priority) program ...shall on an annual basis submit...a report on that (high-priority) program.",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(B) CONTENTS.— Each report submitted ...",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) shall describe any action the executive agency—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(I) has taken or plans to take to recover improper payments (for the High-Priority Program); and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(II) intends to take to prevent future improper payments (for the High-Priority Program)",
            }
        ],
        "3": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 31 U.S.C. § 3352(c)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(c) ESTIMATION OF IMPROPER PAYMENTS.—With respect to each program and activity identified (as susceptible to significant improper payments during the risk assessment) the head of the relevant executive agency shall— ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) (B) include the (improper payment payment) estimates (in a report on paymentaccuracy.gov)...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) (B) include the (unknown payment) estimates (in a report on paymentaccuracy.gov)",
            }
        ],
        "4": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(d)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(d) REPORTS ON ACTIONS TO REDUCE IMPROPER PAYMENTS.—(For each program that is susceptible to significant improper payments),...the head of the executive agency shall provide...a report on what actions the executive agency is taking to reduce improper payments, including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a description of the causes of the improper payments, actions planned or taken to correct those causes, and the planned or actual completion date of the actions taken to address those causes ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) in order to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments, a statement of whether the ... agency has what is  needed with respect to—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) internal controls;",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) human capital; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) information systems and other infrastructure; ",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if the executive agency does not have sufficient resources to establish and maintain effective internal controls (to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments), a description of the resources...requested in the budget submission... to establish and maintain those internal controls ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) program-specific ...improper payments reduction targets...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a description of the steps ...taken to ensure that ...agency managers, programs, and, where appropriate, States and local governments are held accountable through annual performance appraisal criteria for—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) meeting applicable improper payments reduction targets; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) establishing and maintaining sufficient internal controls, including an appropriate control environment, that effectively—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) prevent improper payments from being made; and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) promptly detect and recover improper payments that are made; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a description of how the level of planned or completed actions ...to address the causes of the improper payments matches the level of improper payments, including a break-down by category of improper payment and specific timelines for completion of those actions.",
            }
        ],
        "5": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(e)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "e) REPORTS ON ACTIONS TO RECOVER IMPROPER PAYMENTS.—... the head of the executive agency shall provide ...a report on all actions the executive agency is taking to recover the improper payments (identified in a recovery audit) ..including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a discussion of the methods used by the executive agency to recover improper payments;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) the amounts recovered, outstanding, and determined to not be collectable, including the percent those amounts represent of the total improper payments of the executive agency;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if a determination has been made that certain improper payments are not collectable, a justification of that determination;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) an aging schedule of the amounts outstanding;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a summary of how recovered amounts have been disposed of;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a discussion of any conditions giving rise to improper payments and how those conditions are being resolved; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(7) if the executive agency has determined ...that performing recovery audits for any applicable program or activity is not cost-effective, a justification for that determination.",
            }
        ],
        "6": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(f)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "f) GOVERNMENTWIDE REPORTING OF IMPROPER PAYMENTS AND ACTIONS TO RECOVER IMPROPER PAYMENTS.—Each fiscal year, the Director of the Office of Management and Budget shall submit a report with respect to the preceding fiscal year on actions that executive agencies have taken to report information regarding improper payments and actions to recover improper payments....Each report ...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a summary of the reports of each executive agency on improper payments and recovery actions submitted...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) an identification of the compliance status of each executive agency, as determined by the Inspector General of the executive agency ...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) Governmentwide improper payment reduction targets;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(D) a Governmentwide estimate of improper payments; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(E) a discussion of progress made towards meeting Governmentwide improper payment reduction targets.",
            }
        ],
        "7": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)(1)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) NONCOMPLIANCE.—If an executive agency is determined by the Inspector General of that executive agency not to be in compliance ...in a fiscal year with respect to a program or activity, the head of the executive agency shall submit to the appropriate authorizing and appropriations committees of Congress a plan describing the actions that the executive agency will take to come into compliance. The plan...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) measurable milestones to be accomplished in order to achieve compliance for each program or activity;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) the designation of a senior executive agency official who shall be accountable for the progress of the executive agency in coming into compliance for each program or activity; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(iii) the establishment of an accountability mechanism, such as a performance agreement, with appropriate incentives and consequences tied to the success of the official designated under clause (ii) in leading the efforts of the executive agency to come into compliance for each program or activity.",
            }
        ],
        "8": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)5",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—Each executive agency shall submit to the appropriate authorizing and appropriations committees of Congress and the Comptroller General of the United States—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a list of each program or activity that was determined to not be in compliance ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) actions that are planned to bring the program or activity into compliance.",
            }
        ],
        "9": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3354",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—The Director of the Office of Management and Budget shall submit to Congress an annual report, which may be included as part of another report submitted to Congress by the Director, regarding the operation of the Do Not Pay Initiative, which shall—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) include an evaluation of whether the Do Not Pay Initiative has reduced improper payments or improper awards; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) provide the frequency of corrections or identification of incorrect information.",
            }
        ]
    },
    "2024": {
        "1": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(a)(3)(C)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(C) ANNUAL REPORT.—Each executive agency shall publish an annual report that includes—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) a listing of each program or activity (with annual outlays greater than $10M),  including the date on which the program or activity was most recently assessed for risk",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) a listing of any program or activity for which the executive agency makes any substantial changes to the (risk assessment) methodologies",
            }
        ],
        "2": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(b)(2)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(2) REPORT ON HIGH-PRIORITY IMPROPER PAYMENTS.—...each executive agency with a (high-priority) program ...shall on an annual basis submit...a report on that (high-priority) program.",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(B) CONTENTS.— Each report submitted ...",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) shall describe any action the executive agency—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(I) has taken or plans to take to recover improper payments (for the High-Priority Program); and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(II) intends to take to prevent future improper payments (for the High-Priority Program)",
            }
        ],
        "3": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 31 U.S.C. § 3352(c)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(c) ESTIMATION OF IMPROPER PAYMENTS.—With respect to each program and activity identified (as susceptible to significant improper payments during the risk assessment) the head of the relevant executive agency shall— ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) (B) include the (improper payment payment) estimates (in a report on paymentaccuracy.gov)...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) (B) include the (unknown payment) estimates (in a report on paymentaccuracy.gov)",
            }
        ],
        "4": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(d)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(d) REPORTS ON ACTIONS TO REDUCE IMPROPER PAYMENTS.—(For each program that is susceptible to significant improper payments),...the head of the executive agency shall provide...a report on what actions the executive agency is taking to reduce improper payments, including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a description of the causes of the improper payments, actions planned or taken to correct those causes, and the planned or actual completion date of the actions taken to address those causes ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) in order to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments, a statement of whether the ... agency has what is  needed with respect to—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) internal controls;",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) human capital; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) information systems and other infrastructure; ",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if the executive agency does not have sufficient resources to establish and maintain effective internal controls (to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments), a description of the resources...requested in the budget submission... to establish and maintain those internal controls ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) program-specific ...improper payments reduction targets...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a description of the steps ...taken to ensure that ...agency managers, programs, and, where appropriate, States and local governments are held accountable through annual performance appraisal criteria for—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) meeting applicable improper payments reduction targets; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) establishing and maintaining sufficient internal controls, including an appropriate control environment, that effectively—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) prevent improper payments from being made; and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) promptly detect and recover improper payments that are made; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a description of how the level of planned or completed actions ...to address the causes of the improper payments matches the level of improper payments, including a break-down by category of improper payment and specific timelines for completion of those actions.",
            }
        ],
        "5": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(e)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "e) REPORTS ON ACTIONS TO RECOVER IMPROPER PAYMENTS.—... the head of the executive agency shall provide ...a report on all actions the executive agency is taking to recover the improper payments (identified in a recovery audit) ..including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a discussion of the methods used by the executive agency to recover improper payments;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) the amounts recovered, outstanding, and determined to not be collectable, including the percent those amounts represent of the total improper payments of the executive agency;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if a determination has been made that certain improper payments are not collectable, a justification of that determination;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) an aging schedule of the amounts outstanding;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a summary of how recovered amounts have been disposed of;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a discussion of any conditions giving rise to improper payments and how those conditions are being resolved; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(7) if the executive agency has determined ...that performing recovery audits for any applicable program or activity is not cost-effective, a justification for that determination.",
            }
        ],
        "6": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(f)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "f) GOVERNMENTWIDE REPORTING OF IMPROPER PAYMENTS AND ACTIONS TO RECOVER IMPROPER PAYMENTS.—Each fiscal year, the Director of the Office of Management and Budget shall submit a report with respect to the preceding fiscal year on actions that executive agencies have taken to report information regarding improper payments and actions to recover improper payments....Each report ...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a summary of the reports of each executive agency on improper payments and recovery actions submitted...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) an identification of the compliance status of each executive agency, as determined by the Inspector General of the executive agency ...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) Governmentwide improper payment reduction targets;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(D) a Governmentwide estimate of improper payments; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(E) a discussion of progress made towards meeting Governmentwide improper payment reduction targets.",
            }
        ],
        "7": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)(1)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) NONCOMPLIANCE.—If an executive agency is determined by the Inspector General of that executive agency not to be in compliance ...in a fiscal year with respect to a program or activity, the head of the executive agency shall submit to the appropriate authorizing and appropriations committees of Congress a plan describing the actions that the executive agency will take to come into compliance. The plan...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) measurable milestones to be accomplished in order to achieve compliance for each program or activity;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) the designation of a senior executive agency official who shall be accountable for the progress of the executive agency in coming into compliance for each program or activity; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(iii) the establishment of an accountability mechanism, such as a performance agreement, with appropriate incentives and consequences tied to the success of the official designated under clause (ii) in leading the efforts of the executive agency to come into compliance for each program or activity.",
            }
        ],
        "8": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)5",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—Each executive agency shall submit to the appropriate authorizing and appropriations committees of Congress and the Comptroller General of the United States—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a list of each program or activity that was determined to not be in compliance ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) actions that are planned to bring the program or activity into compliance.",
            }
        ],
        "9": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3354",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—The Director of the Office of Management and Budget shall submit to Congress an annual report, which may be included as part of another report submitted to Congress by the Director, regarding the operation of the Do Not Pay Initiative, which shall—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) include an evaluation of whether the Do Not Pay Initiative has reduced improper payments or improper awards; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) provide the frequency of corrections or identification of incorrect information.",
            }
        ]
    },
    "2025": {
        "1": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(a)(3)(C)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(C) ANNUAL REPORT.—Each executive agency shall publish an annual report that includes—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) a listing of each program or activity (with annual outlays greater than $10M),  including the date on which the program or activity was most recently assessed for risk",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) a listing of any program or activity for which the executive agency makes any substantial changes to the (risk assessment) methodologies",
            }
        ],
        "2": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(b)(2)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(2) REPORT ON HIGH-PRIORITY IMPROPER PAYMENTS.—...each executive agency with a (high-priority) program ...shall on an annual basis submit...a report on that (high-priority) program.",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(B) CONTENTS.— Each report submitted ...",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) shall describe any action the executive agency—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(I) has taken or plans to take to recover improper payments (for the High-Priority Program); and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(II) intends to take to prevent future improper payments (for the High-Priority Program)",
            }
        ],
        "3": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 31 U.S.C. § 3352(c)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.ITALICIZED,
                "text": "(c) ESTIMATION OF IMPROPER PAYMENTS.—With respect to each program and activity identified (as susceptible to significant improper payments during the risk assessment) the head of the relevant executive agency shall— ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) (B) include the (improper payment payment) estimates (in a report on paymentaccuracy.gov)...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) (B) include the (unknown payment) estimates (in a report on paymentaccuracy.gov)",
            }
        ],
        "4": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(d)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(d) REPORTS ON ACTIONS TO REDUCE IMPROPER PAYMENTS.—(For each program that is susceptible to significant improper payments),...the head of the executive agency shall provide...a report on what actions the executive agency is taking to reduce improper payments, including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a description of the causes of the improper payments, actions planned or taken to correct those causes, and the planned or actual completion date of the actions taken to address those causes ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) in order to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments, a statement of whether the ... agency has what is  needed with respect to—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) internal controls;",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) human capital; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) information systems and other infrastructure; ",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if the executive agency does not have sufficient resources to establish and maintain effective internal controls (to reduce improper payments to a level below which further expenditures to reduce improper payments would cost more than the amount those expenditures would save in prevented or recovered improper payments), a description of the resources...requested in the budget submission... to establish and maintain those internal controls ;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) program-specific ...improper payments reduction targets...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a description of the steps ...taken to ensure that ...agency managers, programs, and, where appropriate, States and local governments are held accountable through annual performance appraisal criteria for—",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) meeting applicable improper payments reduction targets; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) establishing and maintaining sufficient internal controls, including an appropriate control environment, that effectively—",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) prevent improper payments from being made; and",
            },
            {
                "indent": 3,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) promptly detect and recover improper payments that are made; and",
            },
            {
                "indent": 2,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a description of how the level of planned or completed actions ...to address the causes of the improper payments matches the level of improper payments, including a break-down by category of improper payment and specific timelines for completion of those actions.",
            }
        ],
        "5": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(e)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "e) REPORTS ON ACTIONS TO RECOVER IMPROPER PAYMENTS.—... the head of the executive agency shall provide ...a report on all actions the executive agency is taking to recover the improper payments (identified in a recovery audit) ..including—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) a discussion of the methods used by the executive agency to recover improper payments;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(2) the amounts recovered, outstanding, and determined to not be collectable, including the percent those amounts represent of the total improper payments of the executive agency;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(3) if a determination has been made that certain improper payments are not collectable, a justification of that determination;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(4) an aging schedule of the amounts outstanding;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) a summary of how recovered amounts have been disposed of;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(6) a discussion of any conditions giving rise to improper payments and how those conditions are being resolved; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(7) if the executive agency has determined ...that performing recovery audits for any applicable program or activity is not cost-effective, a justification for that determination.",
            }
        ],
        "6": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3352(f)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "f) GOVERNMENTWIDE REPORTING OF IMPROPER PAYMENTS AND ACTIONS TO RECOVER IMPROPER PAYMENTS.—Each fiscal year, the Director of the Office of Management and Budget shall submit a report with respect to the preceding fiscal year on actions that executive agencies have taken to report information regarding improper payments and actions to recover improper payments....Each report ...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a summary of the reports of each executive agency on improper payments and recovery actions submitted...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) an identification of the compliance status of each executive agency, as determined by the Inspector General of the executive agency ...;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(C) Governmentwide improper payment reduction targets;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(D) a Governmentwide estimate of improper payments; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(E) a discussion of progress made towards meeting Governmentwide improper payment reduction targets.",
            }
        ],
        "7": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)(1)",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(1) NONCOMPLIANCE.—If an executive agency is determined by the Inspector General of that executive agency not to be in compliance ...in a fiscal year with respect to a program or activity, the head of the executive agency shall submit to the appropriate authorizing and appropriations committees of Congress a plan describing the actions that the executive agency will take to come into compliance. The plan...shall include—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(i) measurable milestones to be accomplished in order to achieve compliance for each program or activity;",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(ii) the designation of a senior executive agency official who shall be accountable for the progress of the executive agency in coming into compliance for each program or activity; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(iii) the establishment of an accountability mechanism, such as a performance agreement, with appropriate incentives and consequences tied to the success of the official designated under clause (ii) in leading the efforts of the executive agency to come into compliance for each program or activity.",
            }
        ],
        "8": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3353(b)5",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—Each executive agency shall submit to the appropriate authorizing and appropriations committees of Congress and the Comptroller General of the United States—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) a list of each program or activity that was determined to not be in compliance ...",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) actions that are planned to bring the program or activity into compliance.",
            }
        ],
        "9": [
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.BOLD,
                "text": "Summary of Report Requirements from 31 U.S.C. § 3354",
            },
            {
                "indent": 0,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(5) ANNUAL REPORT.—The Director of the Office of Management and Budget shall submit to Congress an annual report, which may be included as part of another report submitted to Congress by the Director, regarding the operation of the Do Not Pay Initiative, which shall—",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(A) include an evaluation of whether the Do Not Pay Initiative has reduced improper payments or improper awards; and",
            },
            {
                "indent": 1,
                "type": CONGRESSIONAL_REPORTS_REQUIREMENT_TYPES.REGULAR,
                "text": "(B) provide the frequency of corrections or identification of incorrect information.",
            }
        ]
    }
}

CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING_PROGRAMS = {
    "2023": {
        "2": {
            "cyp21_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Overpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp5_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Underpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp6_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Technically Improper Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp7_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Unknown Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "app1_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app5_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app7_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app8_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            }
        },
        "3": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Annual Outlay Amount"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Within the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Outside the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp26": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Non-Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            }
        },
        "4": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Annual Outlay Amount",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp20_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Reduction Target",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the States",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the States",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Applicants",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Applicants",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Vendors or Providers",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp1_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Vendors or Providers",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from A Specific Scenario",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from A Specific Scenario",
                "heading": "Causes of Improper Payments"
            }
        }
    },
    "2024": {
        "2": {
            "cyp21_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Overpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp5_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Underpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp6_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Technically Improper Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp7_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Unknown Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "app1_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app5_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app7_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            },
            "app8_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            }
        },
        "3": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Annual Outlay Amount"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Within the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Outside the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp26": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Non-Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            }
        },
        "4": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Annual Outlay Amount",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp20_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Reduction Target",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp2_cop3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp3_cop6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp6_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the States",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp3_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the States",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Applicants",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp2_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Applicants",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Vendors or Providers",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp1_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from the Vendors or Providers",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp4": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from A Specific Scenario",
                "heading": "Causes of Improper Payments"
            },
            "cyp7_ucp4_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "Unknown Due to Insufficient or Lack of Documentation from A Specific Scenario",
                "heading": "Causes of Improper Payments"
            }
        }
    },
    "2025": {
        "2": {
            "cyp21_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Overpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp5_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Underpayments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp6_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Technically Improper Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "cyp7_app1_8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MULTISELECT_TEXT,
                "subheading": "Unknown Payments",
                "heading": "Type(s) of Corrective Actions Planned to Prevent Future Improper Payments (by payment type)"
            },
            "atpapp30_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Actions Intended to Prevent Future Improper Payments and Unknown Payments"
            }
        },
        "3": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Annual Outlay Amount"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment Estimate"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Within the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments Outside the Agency Control",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp26": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Non-Monetary Loss",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Makeup of Improper Payment Estimate"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Unknown Payment Estimate"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "",
                "heading": "Improper Payment and Unknown Payment Estimate"
            }
        },
        "4": {
            "rac3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": ""
            },
            "cyp1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Annual Outlay Amount",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp27": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp28": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp30": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp29": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Estimate",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp20_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Improper Payment and Unknown Payment Reduction Target",
                "heading": "Improper Payment & Unknown Payment Estimates and Reduction Target"
            },
            "cyp30_1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.TEXT,
                "subheading": "",
                "heading": "Causes of Improper Payments"
            },
            "cyp21": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp22": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Overpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp21_cop7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp21_cop8": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp21_cop9": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Overpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp23": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Underpayments",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup1": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment Does Not Exist",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup2": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of an Inability to Access the Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp5_cup3": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Amount of Underpayments that Occurred Because of a Failure to Access Data/Information Needed to Validate Payment Accuracy Prior to Making a Payment",
                "heading": "Causes of Improper Payments"
            },
            "cyp6": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp25": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Technically Improper Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp7": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.MILLIONS_OF_DOLLARS,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            },
            "cyp24": {
                "type": CONGRESSIONAL_REPORTS_FIELD_TYPES.PERCENTAGE,
                "subheading": "Unknown Payments",
                "heading": "Causes of Improper Payments"
            }
        }
    }
}