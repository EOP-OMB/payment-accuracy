"""
This is a simple set of tests to make sure constants are properly defined
"""

import os
import pytest
import re

# Import the module
from data_processing import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORECARDS_DIR = os.path.join(BASE_DIR, "..", "website", "assets", "scorecards")

class TestConstants:
    """Tests for our config module"""
    def test_fiscal_year_defined(self):
        """
        Check that the fiscal year is defined.
        """
        assert hasattr(config, 'FISCAL_YEAR')
        assert isinstance(config.FISCAL_YEAR, int)
        assert 2000 <= config.FISCAL_YEAR <= 2100

    def test_government_wide_range_defined(self):
        """
        Check that the count of government wide years displayed is defined.
        """
        assert hasattr(config, 'COUNT_GOVERNMENT_WIDE_YEARS_DISPLAYED')
        assert isinstance(config.COUNT_GOVERNMENT_WIDE_YEARS_DISPLAYED, int)
        assert 0 <= config.COUNT_GOVERNMENT_WIDE_YEARS_DISPLAYED <= 10

    def test_agency_specific_range_defined(self):
        """
        Check that the count of agency-specific years displayed is defined.
        """
        assert hasattr(config, 'COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED')
        assert isinstance(config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED, int)
        assert 0 <= config.COUNT_AGENCY_SPECIFIC_YEARS_DISPLAYED <= 10

    def test_last_quarter_defined(self):
        """
        Check that the count of government wide years displayed is defined.
        """
        assert hasattr(config, 'LAST_QUARTERLY_SURVEY')
        assert isinstance(config.LAST_QUARTERLY_SURVEY, str)
        match = re.search(r"^Q[1-4] [0-9]{4}$", config.LAST_QUARTERLY_SURVEY)
        assert bool(match)

    def test_congressional_reports_range_defined(self):
        """
        Check that the count of congressional report years is defined.
        """
        assert hasattr(config, 'COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED')
        assert isinstance(config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED, int)
        assert 0 <= config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED <= 10

    def test_congressional_reports_mappings(self):
        """
        Check that the mappings are complete and consistent.
        """
        assert hasattr(config, 'CONGRESSIONAL_REPORTS')
        assert hasattr(config, 'CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING')
        assert hasattr(config, 'CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING')
        assert hasattr(config, 'CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING_PROGRAMS')
        assert hasattr(config, 'CONGRESSIONAL_REPORTS_REQUIREMENTS_MAPPING')
        ids = list(map(lambda x: str(x['Id']), config.CONGRESSIONAL_REPORTS))
        yearsToMap = list(range(config.FISCAL_YEAR - config.COUNT_CONGRESSIONAL_REPORTS_YEARS_DISPLAYED + 1, config.FISCAL_YEAR + 1))
        for year in yearsToMap:
            assert year in list(map(lambda x: x['Year'], config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING))
            assert str(year) in list(config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING.keys())
            assert str(year) in list(config.CONGRESSIONAL_REPORTS_FIELD_TO_TYPE_MAPPING_PROGRAMS.keys())
            assert str(year) in list(config.CONGRESSIONAL_REPORTS_REQUIREMENTS_MAPPING.keys())
        for mapping in config.CONGRESSIONAL_REPORTS_YEAR_TO_VIEW_MAPPING:
            for id in mapping["AgencyReports"].keys():
                assert id in ids

    def test_last_quarter_scorecards_exist(self):
        assert os.path.isdir(os.path.join(SCORECARDS_DIR, config.LAST_QUARTERLY_SURVEY))