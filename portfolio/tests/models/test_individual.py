"""Unit tests for the individual model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import Individual


class IndividualTests(TestCase):
    """Unit tests for the individual model."""

    def setUp(self):
        self.individual = Individual.objects.create(
            name="Jemma Doe",
            AngelListLink="https://www.AngelList.com",
            CrunchbaseLink="https://www.Crunchbase.com",
            LinkedInLink="https://www.LinkedIn.com",
            Company="exampleCompany",
            Position="examplePosition",
            Email="test@gmail.com",
            PrimaryNumber=PhoneNumber.from_string("+447975777666"),
            SecondaryNumber=PhoneNumber.from_string("+441325777655")
        )

    # Tests if individual is valid
    def test_valid_individual(self):
        self._assert_individual_is_valid()

    def test_name_cannot_be_blank(self):
        self.individual.name = ''
        self._assert_individual_is_invalid()

    def test_name_can_be_200_characters_long(self):
        self.individual.name = 'A' * 200
        self._assert_individual_is_valid()

    def test_name_cannot_exceed_200_characters(self):
        self.individual.name = 'A' * 201
        self._assert_individual_is_invalid()

    def test_angellistlink_cannot_be_blank(self):
        self.individual.AngelListLink = ''
        self._assert_individual_is_invalid()

    def test_angellistlink_can_be_200_characters_long(self):
        self.individual.AngelListLink = "https://www.google.com/search?q=created+a+lot+of+things+for+all+of+my+friends+andajv&oq=created+a+lot+of+things+for+all+of+my+friends+andajv&aqs=chrome..69i57j69i59l4.483j0j9&sourcesid=chrome&ie=UTF-8"
        self._assert_individual_is_valid()

    def test_angellistlink_cannot_be_over_200_characters_long(self):
        self.individual.AngelListLink = "https://www.google.com/search?q=generate+a+url+with+200+characters+long+long+long&sxsrf=AJOqlzUy02dw8aZyAEwLl5Bkc6A_o8sCuQ%3A1676293616530&ei=8DXqY7OJIJH_gAaIzZKABQ&ved=0ahUKEwizwbWsyJL9AhWRP8AKHYimBFAQ4dUDCA8&uact=5&oq=generate+a+url+with+200+characters+long+long+long&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAE6CggAEEcQ1gQQsAM6BwghEKABEApKBAhBGABKBAhGGABQigJYyRBgoBNoAXABeACAAWKIAdEHkgECMTWYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp"
        self._assert_individual_is_invalid()

    def test_crunchbaselink_cannot_be_blank(self):
        self.individual.CrunchbaseLink = ''
        self._assert_individual_is_invalid()

    def test_crunchbaselink_can_be_200_characters_long(self):
        self.individual.CrunchbaseLink = "https://www.google.com/search?q=created+a+lot+of+things+for+all+of+my+friends+andajv&oq=created+a+lot+of+things+for+all+of+my+friends+andajv&aqs=chrome..69i57j69i59l4.483j0j9&sourcesid=chrome&ie=UTF-8"
        self._assert_individual_is_valid()

    def test_crunchbaselink_cannot_be_over_200_characters_long(self):
        self.individual.CrunchbaseLink = "https://www.google.com/search?q=generate+a+url+with+200+characters+long+long+long&sxsrf=AJOqlzUy02dw8aZyAEwLl5Bkc6A_o8sCuQ%3A1676293616530&ei=8DXqY7OJIJH_gAaIzZKABQ&ved=0ahUKEwizwbWsyJL9AhWRP8AKHYimBFAQ4dUDCA8&uact=5&oq=generate+a+url+with+200+characters+long+long+long&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAE6CggAEEcQ1gQQsAM6BwghEKABEApKBAhBGABKBAhGGABQigJYyRBgoBNoAXABeACAAWKIAdEHkgECMTWYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp"
        self._assert_individual_is_invalid()

    def test_linkedinlink_cannot_be_blank(self):
        self.individual.LinkedInLink = ''
        self._assert_individual_is_invalid()

    def test_linkedinlink_can_be_200_characters_long(self):
        self.individual.LinkedInLink = "https://www.google.com/search?q=created+a+lot+of+things+for+all+of+my+friends+andajv&oq=created+a+lot+of+things+for+all+of+my+friends+andajv&aqs=chrome..69i57j69i59l4.483j0j9&sourcesid=chrome&ie=UTF-8"
        self._assert_individual_is_valid()

    def test_linkedinlink_cannot_be_over_200_characters_long(self):
        self.individual.LinkedInLink = 'https://www.google.com/search?q=generate+a+url+with+200+characters+long+long+long&sxsrf=AJOqlzUy02dw8aZyAEwLl5Bkc6A_o8sCuQ%3A1676293616530&ei=8DXqY7OJIJH_gAaIzZKABQ&ved=0ahUKEwizwbWsyJL9AhWRP8AKHYimBFAQ4dUDCA8&uact=5&oq=generate+a+url+with+200+characters+long+long+long&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAE6CggAEEcQ1gQQsAM6BwghEKABEApKBAhBGABKBAhGGABQigJYyRBgoBNoAXABeACAAWKIAdEHkgECMTWYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp'
        self._assert_individual_is_invalid()

    def test_company_cannot_be_blank(self):
        self.individual.Company = ''
        self._assert_individual_is_invalid()

    def test_company_can_be_100_characters_long(self):
        self.individual.Company = 'x' * 100
        self._assert_individual_is_valid()

    def test_company_cannot_be_over_100_characters_long(self):
        self.individual.Company = 'x' * 101
        self._assert_individual_is_invalid()

    def test_position_cannot_be_blank(self):
        self.individual.Position = ''
        self._assert_individual_is_invalid()

    def test_position_can_be_100_characters_long(self):
        self.individual.Position = 'x' * 100
        self._assert_individual_is_valid()

    def test_position_cannot_be_over_100_characters_long(self):
        self.individual.Position = 'x' * 101
        self._assert_individual_is_invalid()

    # Tests the fact that the email field of a individual shouldn't be blank
    def test_email_must_not_be_blank(self):
        self.individual.Email = ''
        self._assert_individual_is_invalid()

    # Tests the fact that the email field of a individual can be not unique
    def test_email_can_be_not_unique(self):
        second_individual = self._create_second_individual()
        self.individual.Email = second_individual.Email
        self._assert_individual_is_valid()

    def test_primarynumber_must_not_be_blank(self):
        self.individual.PrimaryNumber = ''
        self._assert_individual_is_invalid()

    def test_secondarynumber_can_be_blank(self):
        self.individual.SecondaryNumber = ''
        self._assert_individual_is_valid()

    """Helper functions"""

    # Assert a individual is valid
    def _assert_individual_is_valid(self):
        try:
            self.individual.full_clean()
        except ValidationError:
            self.fail('Test individual is not valid.')

    # Assert a individual is invalid
    def _assert_individual_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.individual.full_clean()

    # Create a second individual
    def _create_second_individual(self):
        individual = Individual.objects.create(
            AngelListLink="www.AngelList2.com",
            CrunchbaseLink="www.Crunchbase2.com",
            LinkedInLink="www.LinkedInLink2.com",
            Company="exampleCompany2",
            Position="examplePosition2",
            Email="test2@gmail.com",
            PrimaryNumber=PhoneNumber.from_string("+447975777662"),
            SecondaryNumber=PhoneNumber.from_string("+441325777651")
        )
        return individual
