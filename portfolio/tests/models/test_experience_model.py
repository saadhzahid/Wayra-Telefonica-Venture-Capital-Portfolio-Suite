from django.core.exceptions import ValidationError
from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import PastExperience, Individual


class ExperienceModelTestCase(TestCase):
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

        self.pastExperience = PastExperience.objects.create(
            companyName="Startup",
            workTitle="CEO",
            start_year=1995,
            end_year=1998,
            duration="3",
            Description="I'm the founder of the Startup.",
            individual=self.individual
        )

    def test_valid_past_experience(self):
        self._assert_past_experience_is_valid()

    def test_company_name_has_max_length_of_100_characters(self):
        self.pastExperience.companyName = "x" * 101
        self._assert_past_experience_is_invalid()

    def test_workTitle_has_max_length_of_100_characters(self):
        self.pastExperience.workTitle = "x" * 101
        self._assert_past_experience_is_invalid()

    def test_end_year_cannot_be_blank(self):
        self.pastExperience.end_year = ""
        self._assert_past_experience_is_invalid()

    def test_duration_has_max_length_of_50_characters(self):
        self.pastExperience.duration = "x" * 51
        self._assert_past_experience_is_invalid()

    def test_description_can_be_blank(self):
        self.pastExperience.Description = ""
        self._assert_past_experience_is_valid()

    def test_individual_cannot_be_none(self):
        self.pastExperience.individual = None
        self._assert_past_experience_is_invalid()

        """Helper functions"""

    # Assert a past experience is valid
    def _assert_past_experience_is_valid(self):
        try:
            self.pastExperience.full_clean()
        except ValidationError:
            self.fail('Test individual is not valid.')

    # Assert a past experience is invalid
    def _assert_past_experience_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.pastExperience.full_clean()
