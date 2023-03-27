"""Unit test for the founder model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import Founder, Individual, Company


class FounderModelTestCase(TestCase):
    """Unit test for the founder model."""
    DEFAULT_FIXTURES = [
        'portfolio/tests/fixtures/default_company.json',
        'portfolio/tests/fixtures/default_individual.json',
        'portfolio/tests/fixtures/default_portfolio_company.json',
        'portfolio/tests/fixtures/default_programme.json',
    ]

    def setUp(self):
        self.individual = Individual.objects.create(
            AngelListLink="https://www.AngelList.com",
            CrunchbaseLink="https://www.Crunchbase.com",
            LinkedInLink="https://www.LinkedIn.com",
            Company="exampleCompany",
            Position="examplePosition",
            Email="test@gmail.com",
            PrimaryNumber=PhoneNumber.from_string("+447975777666"),
            SecondaryNumber=PhoneNumber.from_string("+441325777655")
        )

        self.company = Company.objects.create(
            name="Default Ltd",
            company_registration_number="00000000",
            trading_names="Default Ltd",
            previous_names="Default Ltd",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now(),
        )

        self.founder = Founder.objects.create(
            companyFounded=self.company,
            individualFounder=self.individual,
        )

    def test_valid_founder(self):
        self._assert_founder_is_valid()

    def test_founder_create(self):
        self.assertTrue(isinstance(self.founder, Founder))
        self.assertEqual(self.founder.companyFounded, self.company)
        self.assertEqual(self.founder.individualFounder, self.individual)

    def test_company_founded_cascade_delete(self):
        self.company.delete()
        self.assertFalse(Founder.objects.filter(pk=self.founder.pk).exists())

    def test_individual_founded_cascade_delete(self):
        self.individual.delete()
        self.assertFalse(Founder.objects.filter(pk=self.founder.pk).exists())

    # Assert a founder is valid.
    def _assert_founder_is_valid(self):
        try:
            self.founder.full_clean()
        except ValidationError:
            self.fail('Test founder is not valid.')

    # Assert a founder is invalid
    def _assert_founder_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.founder.full_clean()
