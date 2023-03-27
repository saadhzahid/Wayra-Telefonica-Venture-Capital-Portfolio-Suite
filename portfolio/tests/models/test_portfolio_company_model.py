from django.core.exceptions import ValidationError
from django.test import TestCase

from portfolio.models import Company, Portfolio_Company


class PortfolioCompanyTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/other_companies.json']

    def setUp(self) -> None:
        self.company = Company.objects.get(id=1)
        self.portfolio_company = Portfolio_Company.objects.create(parent_company=self.company, wayra_number='WN-1')

    def _assert_portfolio_company_is_valid(self):
        try:
            self.portfolio_company.full_clean()
        except ValidationError:
            self.fail("Test company is not valid.")

    # Assert a company is invalid
    def _assert_portfolio_company_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.portfolio_company.full_clean()

    def test_valid_portfolio_company(self):
        self._assert_portfolio_company_is_valid()

    def _create_second_portfolio_company(self):
        other_p_company = Portfolio_Company.objects.create(parent_company=Company.objects.get(id=201),
                                                           wayra_number='WN-2')
        return other_p_company

    def test_parent_company_cannot_be_repeated(self):
        other_p_company = self._create_second_portfolio_company()
        self.portfolio_company.parent_company = other_p_company.parent_company
        self._assert_portfolio_company_is_invalid()

    def test_wayra_number_cannot_be_repeated(self):
        other_p_company = self._create_second_portfolio_company()
        self.portfolio_company.wayra_number = other_p_company.wayra_number
        self._assert_portfolio_company_is_invalid()

    def test_wayra_number_can_be_255_chr(self):
        self.portfolio_company.wayra_number = 'WN-' + '1' * 252
        self._assert_portfolio_company_is_valid()

    def test_wayra_number_cannot_exceed_be_255_chr(self):
        self.portfolio_company.wayra_number = 'WN-' + '1' * 253
        self._assert_portfolio_company_is_invalid()
