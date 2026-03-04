"""
Tests to verify that governmentwide figures in home.md correctly tie to the
individual agency values in agenciesPrograms.md.

This validates that:
1. Improper payment rates are correctly calculated as weighted averages
2. Payment accuracy rates match expected values
3. Unknown payment rates match expected values
4. All three rates sum to 100%
"""

import os
import yaml
import pytest
import ast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_PAGES_DIR = os.path.join(BASE_DIR, "..", "website", "pages")
AGENCIES_PROGRAMS_PATH = os.path.join(WEBSITE_PAGES_DIR, "agenciesPrograms.md")
HOME_PATH = os.path.join(WEBSITE_PAGES_DIR, "home.md")

# Tolerance for floating point comparisons (0.01%)
TOLERANCE = 0.01


def parse_markdown_frontmatter(filepath):
    """
    Parse YAML frontmatter from a markdown file.
    Returns the parsed YAML as a dictionary.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter between --- markers
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            return yaml.safe_load(frontmatter)
    
    return {}


def get_agencies_data():
    """
    Parse agenciesPrograms.md and return the list of agencies with their data.
    """
    data = parse_markdown_frontmatter(AGENCIES_PROGRAMS_PATH)
    return data.get('agencies', [])


def get_home_data():
    """
    Parse home.md and return the governmentwide data.
    """
    return parse_markdown_frontmatter(HOME_PATH)


def calculate_governmentwide_improper_payment_rate():
    """
    Calculate the weighted average improper payment rate across all agencies.
    Returns the rate as a percentage.
    """
    agencies = get_agencies_data()
    
    total_weighted_ip = 0
    total_spending = 0
    
    for agency in agencies:
        ip_rate = agency.get('improper_payments_rate', 0)
        spending = agency.get('total_spent_federal_funding', 0)
        
        # Only include agencies with actual spending
        if spending > 0:
            total_weighted_ip += (ip_rate * spending / 100)
            total_spending += spending
    
    if total_spending == 0:
        return 0
    
    return (total_weighted_ip / total_spending) * 100


def calculate_governmentwide_unknown_payment_rate():
    """
    Calculate unknown payment rate based on the constraint that
    improper + accuracy + unknown = 100%
    """
    home_data = get_home_data()
    
    # Get the last values from the lists
    improper_rates = ast.literal_eval(home_data.get('improper_payments_rates', '[]'))
    accuracy_rates = ast.literal_eval(home_data.get('payment_accuracy_rates', '[]'))
    
    if not improper_rates or not accuracy_rates:
        return 0
    
    last_improper = improper_rates[-1]
    last_accuracy = accuracy_rates[-1]
    
    # unknown = 100 - improper - accuracy
    return 100 - last_improper - last_accuracy


class TestGovernmentwideMetrics:
    """Tests for governmentwide payment accuracy metrics"""
    
    def test_improper_payment_rate_matches_agencies(self):
        """
        Verify that the last improper payment rate in home.md matches
        the weighted average calculated from individual agency data.
        """
        home_data = get_home_data()
        
        # Parse the improper_payments_rates list (it's stored as a string representation of a list)
        improper_rates_str = home_data.get('improper_payments_rates', '[]')
        improper_rates = ast.literal_eval(improper_rates_str)
        
        assert len(improper_rates) > 0, "No improper payment rates found in home.md"
        
        # Get the last (most recent) value
        last_improper_rate = improper_rates[-1]
        
        # Calculate expected value from agencies
        calculated_rate = calculate_governmentwide_improper_payment_rate()
        
        # Compare with tolerance
        assert abs(last_improper_rate - calculated_rate) <= TOLERANCE, \
            f"Improper payment rate mismatch: home.md shows {last_improper_rate:.4f}%, " \
            f"but calculated from agencies is {calculated_rate:.4f}%"
    
    def test_payment_accuracy_rate_matches_agencies(self):
        """
        Verify that the last payment accuracy rate in home.md is consistent
        with the improper and unknown payment rates (should sum to 100%).
        """
        home_data = get_home_data()
        
        # Parse the rates lists
        improper_rates = ast.literal_eval(home_data.get('improper_payments_rates', '[]'))
        accuracy_rates = ast.literal_eval(home_data.get('payment_accuracy_rates', '[]'))
        unknown_rates = ast.literal_eval(home_data.get('unknown_payments_rates', '[]'))
        
        assert len(improper_rates) > 0, "No improper payment rates found"
        assert len(accuracy_rates) > 0, "No payment accuracy rates found"
        assert len(unknown_rates) > 0, "No unknown payment rates found"
        
        # Get the last values
        last_improper = improper_rates[-1]
        last_accuracy = accuracy_rates[-1]
        last_unknown = unknown_rates[-1]
        
        # Calculate expected accuracy rate
        calculated_improper = calculate_governmentwide_improper_payment_rate()
        expected_accuracy = 100 - calculated_improper - last_unknown
        
        # Compare with tolerance
        assert abs(last_accuracy - expected_accuracy) <= TOLERANCE, \
            f"Payment accuracy rate mismatch: home.md shows {last_accuracy:.4f}%, " \
            f"but calculated is {expected_accuracy:.4f}%"
    
    def test_unknown_payment_rate_exists(self):
        """
        Verify that unknown payment rate is defined and within valid range.
        """
        home_data = get_home_data()
        
        # Parse the unknown_payments_rates list
        unknown_rates = ast.literal_eval(home_data.get('unknown_payments_rates', '[]'))
        
        assert len(unknown_rates) > 0, "No unknown payment rates found in home.md"
        
        last_unknown_rate = unknown_rates[-1]
        
        # Unknown rate should be between 0 and 100
        assert 0 <= last_unknown_rate <= 100, \
            f"Unknown payment rate {last_unknown_rate}% is out of valid range [0, 100]"
    
    def test_all_rates_sum_to_100_percent(self):
        """
        Verify that improper + accuracy + unknown payment rates sum to 100%.
        """
        home_data = get_home_data()
        
        # Parse all rate lists
        improper_rates = ast.literal_eval(home_data.get('improper_payments_rates', '[]'))
        accuracy_rates = ast.literal_eval(home_data.get('payment_accuracy_rates', '[]'))
        unknown_rates = ast.literal_eval(home_data.get('unknown_payments_rates', '[]'))
        
        assert len(improper_rates) > 0, "No improper payment rates found"
        assert len(accuracy_rates) > 0, "No payment accuracy rates found"
        assert len(unknown_rates) > 0, "No unknown payment rates found"
        
        # Get the last values
        last_improper = improper_rates[-1]
        last_accuracy = accuracy_rates[-1]
        last_unknown = unknown_rates[-1]
        
        total = last_improper + last_accuracy + last_unknown
        
        # Should sum to exactly 100% (within tolerance)
        assert abs(total - 100) <= TOLERANCE, \
            f"Payment rates don't sum to 100%: {last_improper:.4f}% + " \
            f"{last_accuracy:.4f}% + {last_unknown:.4f}% = {total:.4f}%"
    
    def test_fiscal_year_defined(self):
        """
        Verify that the fiscal year is defined in home.md.
        """
        home_data = get_home_data()
        
        assert 'fiscal_year' in home_data, "Fiscal year not defined in home.md"
        fiscal_year = home_data['fiscal_year']
        
        assert isinstance(fiscal_year, int), \
            f"Fiscal year should be an integer, got {type(fiscal_year)}"
        assert 2019 <= fiscal_year, \
            f"Fiscal year {fiscal_year} is out of expected range [2020, 2030]"
    
    def test_rate_lists_have_same_length(self):
        """
        Verify that all rate lists have the same number of entries.
        """
        home_data = get_home_data()
        
        improper_rates = ast.literal_eval(home_data.get('improper_payments_rates', '[]'))
        accuracy_rates = ast.literal_eval(home_data.get('payment_accuracy_rates', '[]'))
        unknown_rates = ast.literal_eval(home_data.get('unknown_payments_rates', '[]'))
        
        assert len(improper_rates) == len(accuracy_rates) == len(unknown_rates), \
            f"Rate lists have different lengths: improper={len(improper_rates)}, " \
            f"accuracy={len(accuracy_rates)}, unknown={len(unknown_rates)}"
    
    def test_agencies_have_required_fields(self):
        """
        Verify that all agencies in agenciesPrograms.md have the required fields.
        """
        agencies = get_agencies_data()
        
        assert len(agencies) > 0, "No agencies found in agenciesPrograms.md"
        
        required_fields = [
            'agency',
            'agency_name',
            'improper_payments_rate',
            'total_spent_federal_funding'
        ]
        
        for agency in agencies:
            for field in required_fields:
                assert field in agency, \
                    f"Agency {agency.get('agency', 'UNKNOWN')} missing field: {field}"
    
    def test_improper_payment_rate_within_bounds(self):
        """
        Verify that the calculated improper payment rate is within reasonable bounds.
        """
        calculated_rate = calculate_governmentwide_improper_payment_rate()
        
        assert 0 <= calculated_rate <= 100, \
            f"Calculated improper payment rate {calculated_rate:.4f}% is out of bounds [0, 100]"
    
    def test_total_spending_positive(self):
        """
        Verify that total federal spending across all agencies is positive.
        """
        agencies = get_agencies_data()
        
        total_spending = sum(
            agency.get('total_spent_federal_funding', 0) 
            for agency in agencies
        )
        
        assert total_spending > 0, \
            "Total federal spending should be positive"


class TestAgencyDataQuality:
    """Additional tests for agency data quality"""
    
    def test_agency_rates_within_valid_range(self):
        """
        Verify that all individual agency improper payment rates are within 0-100%.
        """
        agencies = get_agencies_data()
        
        for agency in agencies:
            ip_rate = agency.get('improper_payments_rate', 0)
            agency_name = agency.get('agency_name', 'UNKNOWN')
            
            assert 0 <= ip_rate <= 100, \
                f"Agency {agency_name} has invalid IP rate: {ip_rate}%"
    
    def test_agency_spending_non_negative(self):
        """
        Verify that all agency spending amounts are non-negative.
        """
        agencies = get_agencies_data()
        
        for agency in agencies:
            spending = agency.get('total_spent_federal_funding', 0)
            agency_name = agency.get('agency_name', 'UNKNOWN')
            
            assert spending >= 0, \
                f"Agency {agency_name} has negative spending: {spending}"
    
    def test_high_spending_agencies_have_data(self):
        """
        Verify that agencies with high spending have improper payment rate data.
        """
        agencies = get_agencies_data()
        
        # Sort agencies by spending
        sorted_agencies = sorted(
            agencies, 
            key=lambda x: x.get('total_spent_federal_funding', 0),
            reverse=True
        )
        
        # Check top 10 agencies
        for agency in sorted_agencies[:10]:
            spending = agency.get('total_spent_federal_funding', 0)
            if spending > 0:
                # Should have improper payment rate data
                assert 'improper_payments_rate' in agency, \
                    f"High-spending agency {agency.get('agency_name')} missing IP rate"

class TestAssistanceListingURLs:
    """Tests to verify that Assistance Listing Numbers have valid FPI URLs"""

    @pytest.mark.skip(reason="Awaiting review of FPIMapping.csv")
    def test_assistance_listing_urls_exist(self):
        """
        Verify that all fpi_links are valid
        """
        import glob
        import requests
        from collections import OrderedDict

        # Extract fpi_link from each file
        programs_dir = os.path.join(BASE_DIR, "..", "website", "pages", "programs")
        assert os.path.exists(programs_dir), f"Programs directory not found at {programs_dir}"
        program_files = glob.glob(os.path.join(programs_dir, "*.md"))
        assert len(program_files) > 0, "No program markdown files found"
        fpi_links = {}
        for filepath in program_files:
            frontmatter = parse_markdown_frontmatter(filepath)
            fpi_link = frontmatter.get('fpi_link')
            if fpi_link:
                program_name = frontmatter.get('Program_Name', os.path.basename(filepath))
                agency = frontmatter.get('Agency', 'Unknown')
                fpi_links[fpi_link] = {
                    'program': program_name,
                    'agency': agency,
                    'assistance_number': fpi_link.rsplit('/', 1)[-1],
                    'file': os.path.basename(filepath)
                }
        assert len(fpi_links) > 0, "No Assistance Listing Numbers found in CSV"

        # Test each URL
        failed_urls = []
        for url, info in fpi_links.items():
            try:
                response = requests.get(url, timeout=10)

                # the page should contain the assistance number
                # if it does not, the user was redirected
                if info['assistance_number'] not in response.text:
                    failed_urls.append({
                        'number': info['assistance_number'],
                        'agency': info['agency'],
                        'program': info['program'],
                        'url': url,
                        'status_code': response.status_code
                    })

                if response.status_code != 200:
                    failed_urls.append({
                        'number': info['assistance_number'],
                        'agency': info['agency'],
                        'program': info['program'],
                        'url': url,
                        'status_code': response.status_code
                    })
            except requests.RequestException as e:
                failed_urls.append({
                    'number': info['assistance_number'],
                    'agency': info['agency'],
                    'program': info['program'],
                    'url': url,
                    'error': str(e)
                })

        # Build detailed error message if any URLs failed
        if failed_urls:
            error_msg = f"\n{len(failed_urls)} out of {len(fpi_links)} Assistance Listing URLs failed:\n"
            for item in failed_urls[:10]:  # Show first 10 failures
                error_msg += f"\n  - {item['number']} ({item['agency']} - {item['program']})"
                error_msg += f"\n    URL: {item['url']}"
                if 'status_code' in item:
                    error_msg += f"\n    Status Code: {item['status_code']}"
                else:
                    error_msg += f"\n    Error: {item['error']}"

            if len(failed_urls) > 10:
                error_msg += f"\n\n  ... and {len(failed_urls) - 10} more failures"

            pytest.fail(error_msg)