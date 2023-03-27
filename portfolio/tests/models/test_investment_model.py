import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from portfolio.models import Company, Portfolio_Company, Investment, Individual
from portfolio.models.investor_model import Investor


class InvestmentModelTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json',
                'portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.portfolio_company = Portfolio_Company.objects.get(pk=101)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolio_company,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            investmentAmount=1_000_000_000,
            dateExit=None,
        )

    def _assert_valid_investment(self):
        try:
            self.investment.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_invalid_investment(self):
        with self.assertRaises(ValidationError):
            self.investment.full_clean()

    def test_valid_investment(self):
        self._assert_valid_investment()

    def test_investment_amount_cannot_exceed_15_digits(self):
        self.investment.investmentAmount = 1_000_000_000_000_000
        self._assert_invalid_investment()

    def test_investment_amount_cannot_exceed_2_dp(self):
        self.investment.investmentAmount = 1_000_000.101
        self._assert_invalid_investment()

    def test_investment_amount_can_be_15_digits(self):
        self.investment.investmentAmount = 1_000_000_000_000.00
        self._assert_valid_investment()

    def test_investment_can_hv_two_dp(self):
        self.investment.investmentAmount = Decimal('12345678.12')
        self._assert_valid_investment()

    def test_investment_cannot_be_negative(self):
        self.investment.investmentAmount = - 1_000_000

    def test_date_invested_can_be_today(self):
        self.investment.dateInvested = datetime.date.today()
        self._assert_valid_investment()

    def test_date_invested_cannot_be_tomorrow(self):
        self.investment.dateInvested = datetime.date.today() + datetime.timedelta(days=1)
        self._assert_invalid_investment()

    def test_date_invested_cannot_be_blank(self):
        self.investment.dateInvested = None
        self._assert_invalid_investment()

    def test_date_exit_can_be_blank(self):
        self.investment.dateExit = None
        self._assert_valid_investment()

    def test_date_exit_can_be_after_date_invested(self):
        self.investment.dateExit = self.investment.dateInvested + datetime.timedelta(days=1)
        self._assert_valid_investment()

    def test_date_exit_cannot_be_before_date_invested(self):
        self.investment.dateExit = self.investment.dateInvested + datetime.timedelta(days=-1)
        self._assert_invalid_investment()

    def test_investor_cannot_be_blank(self):
        self.investment.investor = None
        self._assert_invalid_investment()

    def test_investor_delete_deletes_investment(self):
        self.investment.investor.delete()
        self.assertEqual(Investment.objects.count(), 0)

    def test_startup_cannot_be_blank(self):
        self.investment.startup = None
        self._assert_invalid_investment()

    def test_startup_delete_deletes_investment(self):
        self.investment.startup.delete()
        self.assertEqual(Investment.objects.count(), 0)


class InvestorModelTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json', 'portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.defaultIndividual = Individual.objects.get(id=1)
        self.investor = Investor.objects.create(
            company=self.defaultCompany,
            classification=Investor.INVESTOR_TYPES[1][0]
        )

    def _assert_valid_investment(self):
        try:
            self.investor.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_invalid_investment(self):
        with self.assertRaises(ValidationError):
            self.investor.full_clean()

    def test_company_and_individual_cannot_be_null(self):
        self.investor.company = None
        self._assert_invalid_investment()

    def test_individual_is_assigned(self):
        self.investor.company = None
        self.investor.individual = self.defaultIndividual
        self._assert_valid_investment()

    def test_company_is_assigned(self):
        self.investor.company = self.defaultCompany
        self.investor.individual = None
        self._assert_valid_investment()

    def test_delete_company_deletes_investor(self):
        self.defaultCompany.delete()
        self.assertEqual(Investor.objects.count(), 0)

    def test_delete_individual_deletes_investor(self):
        self.investor.company = None
        self.investor.individual = self.defaultIndividual
        self.investor.save()
        self.defaultIndividual.delete()
        self.assertEqual(Investor.objects.count(), 0)

    def test_classification_cannot_be_none(self):
        self.investor.classification = None
        self._assert_invalid_investment()

    def test_classification_can_be_50_chars(self):
        self.investor.classification = "A" * 50
        self._assert_invalid_investment()

    def test_classification_cannot_be_over_50_chars(self):
        self.investor.classification = "A" * 51
        self._assert_invalid_investment()
