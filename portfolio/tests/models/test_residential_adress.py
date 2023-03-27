from django.core.exceptions import ValidationError
from django.test import TestCase
from django_countries.fields import Country
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import Individual
from portfolio.models import ResidentialAddress


class ResidentialAdressTests(TestCase):
    """Unit tests for the individual model."""

    # Sets up example individual to be used for tests
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

        self.residential_adress = ResidentialAddress.objects.create(
            address_line1="testAdress1",
            address_line2="testAdress2",
            postal_code="testCode",
            city="testCity",
            state="testState",
            country=Country("AD"),
            individual=self.individual
        )

    def test_valid_residential_adress(self):
        self._assert_residential_adress_is_valid()

    def test_address_line1_cannot_be_blank(self):
        self.residential_adress.address_line1 = ''
        self._assert_residential_adress_is_invalid()

    def test_address_line1_can_be_50_characters_long(self):
        self.residential_adress.address_line1 = 'x' * 50
        self._assert_residential_adress_is_valid()

    def test_address_line1_cannot_be_over_50_characters_long(self):
        self.residential_adress.address_line1 = 'x' * 51
        self._assert_residential_adress_is_invalid()

    def test_address_line2_can_be_blank(self):
        self.residential_adress.address_line2 = ''
        self._assert_residential_adress_is_valid()

    def test_address_line2_can_be_50_characters_long(self):
        self.residential_adress.address_line2 = 'x' * 50
        self._assert_residential_adress_is_valid()

    def test_address_line2_cannot_be_over_50_characters_long(self):
        self.residential_adress.address_line2 = 'x' * 51
        self._assert_residential_adress_is_invalid()

    def test_postal_code_can_be_10_characters_long(self):
        self.residential_adress.postal_code = 'x' * 10
        self._assert_residential_adress_is_valid()

    def test_postal_code_cannot_be_over_10_characters_long(self):
        self.residential_adress.postal_code = 'x' * 11
        self._assert_residential_adress_is_invalid()

    def test_city_cannot_be_blank(self):
        self.residential_adress.city = ''
        self._assert_residential_adress_is_invalid()

    def test_city_can_be_50_characters_long(self):
        self.residential_adress.city = 'x' * 50
        self._assert_residential_adress_is_valid()

    def test_city_cannot_be_over_50_characters_long(self):
        self.residential_adress.city = 'x' * 51
        self._assert_residential_adress_is_invalid()

    def test_state_can_be_blank(self):
        self.residential_adress.state = ''
        self._assert_residential_adress_is_valid()

    def test_state_can_be_50_characters_long(self):
        self.residential_adress.state = 'x' * 50
        self._assert_residential_adress_is_valid()

    def test_state_cannot_be_over_50_characters_long(self):
        self.residential_adress.state = 'x' * 51
        self._assert_residential_adress_is_invalid()

    def test_country_has_to_be_valid(self):
        self.residential_adress.country = Country("ababa")
        self._assert_residential_adress_is_invalid()

    def test_individual_cannot_be_none(self):
        self.residential_adress.individual = None
        self._assert_residential_adress_is_invalid()

    """Helper functions"""

    # Assert a residential adress is valid
    def _assert_residential_adress_is_valid(self):
        try:
            self.residential_adress.full_clean()
        except ValidationError:
            self.fail('Test individual is not valid.')

    # Assert a residential adress is invalid
    def _assert_residential_adress_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.residential_adress.full_clean()
