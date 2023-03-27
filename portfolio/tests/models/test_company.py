from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from portfolio.models import Company


class CompanyModelTestCase(TestCase):
    """Unit tests for the Company model."""

    # Sets up the default company to be used for tests
    def setUp(self):
        self.company = Company.objects.create(
            name="Default Ltd",
            company_registration_number="00000000",
            trading_names="Default Ltd",
            previous_names="Default Ltd",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now(),
        )

    def test_valid_company(self):
        self._assert_company_is_valid()

    def test_name_must_be_unique(self):
        second_company = self._create_second_company()
        self.company.name = second_company.name
        self._assert_company_is_invalid()

    def test_name_must_contain_at_least_three_characters(self):
        self.company.name = "jo"
        self._assert_company_is_invalid()

    def test_name_cannot_be_longer_than_sixty_characters(self):
        self.company.name = "x" * 61
        self._assert_company_is_invalid()

    """Helper functions"""

    # Assert a company is valid
    def _assert_company_is_valid(self):
        try:
            self.company.full_clean()
        except ValidationError:
            self.fail("Test company is not valid.")

    # Assert a company is invalid
    def _assert_company_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.company.full_clean()

    # Create a second company
    def _create_second_company(self):
        company = Company.objects.create(
            name="Company Name",
            company_registration_number="00000001",
            trading_names="Company Ltd",
            previous_names="Company Ltd",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now()
        )
        return company
