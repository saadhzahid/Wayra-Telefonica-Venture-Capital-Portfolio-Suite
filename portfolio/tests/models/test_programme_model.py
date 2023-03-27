"""Unit tests of the Programme model."""
from django.core.exceptions import ValidationError
from django.test import TestCase

from portfolio.models import Programme, Company, Portfolio_Company, Individual


class ProgrammeModelTestCase(TestCase):
    """Unit tests of the Programme model."""
    DEFAULT_FIXTURES = ['portfolio/tests/fixtures/default_company.json',
                        'portfolio/tests/fixtures/default_individual.json',
                        'portfolio/tests/fixtures/default_portfolio_company.json',
                        'portfolio/tests/fixtures/default_programme.json',
                        ]

    OTHER_FIXTURES = ['portfolio/tests/fixtures/other_companies.json',
                      'portfolio/tests/fixtures/other_individuals.json',
                      'portfolio/tests/fixtures/other_portfolio_companies.json',
                      'portfolio/tests/fixtures/other_programmes.json',
                      ]
    fixtures = DEFAULT_FIXTURES + OTHER_FIXTURES

    def setUp(self) -> None:
        self.programme = Programme.objects.get(id=1)
        self.partner = Company.objects.get(id=1)
        self.participant = Company.objects.get(pk=101)
        self.coach = Individual.objects.get(id=1)
        self.programme.partners.add(self.partner)
        self.programme.participants.add(self.participant)
        self.programme.coaches_mentors.add(self.coach)
        self.programme.description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    def _create_second_programme(self):
        second_programme = Programme.objects.get(id=2)
        second_partner = Company.objects.get(id=201)
        second_participant = Company.objects.get(pk=301)
        second_coach = Individual.objects.get(id=2)
        second_programme.partners.add(second_partner)
        second_programme.participants.add(second_participant)
        second_programme.coaches_mentors.add(second_coach)
        return second_programme

    def _assert_programme_is_valid(self):
        try:
            self.programme.full_clean()
        except ValidationError:
            self.fail("Test programme should be valid")

    def _assert_programme_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.programme.full_clean()

    # test name

    def test_valid_programme(self):
        self._assert_programme_is_valid()

    def test_name_can_be_255_chars(self):
        self.programme.name = "A" * 255
        self._assert_programme_is_valid()

    def test_name_cannot_exceed_255_chars(self):
        self.programme.name = "A" * 256
        self._assert_programme_is_invalid()

    def test_name_cannot_be_blank(self):
        self.programme.name = ''
        self._assert_programme_is_invalid()

    def test_name_can_repeat(self):
        second_programme = self._create_second_programme()
        self.programme.name = second_programme.name
        # has to change to 2 to avoid unique_tgt name and cohort
        self.programme.cohort = 2
        self._assert_programme_is_valid()

    def test_cohort_cannot_be_blank(self):
        self.programme.cohort = None
        self._assert_programme_is_invalid()

    def test_cohort_cannot_be_zero(self):
        self.programme.cohort = 0
        self._assert_programme_is_invalid()

    def test_name_and_cohort_cannot_be_the_same(self):
        second_programme = self._create_second_programme()
        self.programme.name = second_programme.name
        self.programme.cohort = second_programme.cohort
        self._assert_programme_is_invalid()

    # test partner field
    def test_partners_can_be_none(self):
        self.programme.partners.remove(self.partner)
        self.assertEqual(0, self.programme.partners.count())

        self._assert_programme_is_valid()

    def test_partners_can_be_added(self):
        second_partner = Company.objects.get(id=201)
        self.programme.partners.add(second_partner)
        self.assertEqual(2, self.programme.partners.count())
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.partners.count(), 2)

    def test_partners_can_be_removed(self):
        self.programme.partners.remove(self.partner)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.partners.count(), 0)

    def test_partners_can_be_added_multiple_times_without_duplicate(self):
        self.programme.partners.add(self.partner)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.partners.count(), 1)

    def test_multiple_programmes_can_have_same_partners(self):
        second_programme = self._create_second_programme()
        self.programme.partners.remove(self.partner)

        partners = list(second_programme.partners.all())
        for company in partners:
            self.programme.partners.add(company)

        self._assert_programme_is_valid()
        self.assertEqual(second_programme.partners.count(), self.programme.partners.count())

    def test_remove_partner_removes_from_programme_correctly(self):
        Company.objects.get(id=1).delete()
        self._assert_programme_is_valid()
        all_programmes = list(Programme.objects.all())
        self.assertIn(self.programme, all_programmes)
        self.assertEqual(self.programme.partners.count(), 0)

    # Test participants relation
    def test_participants_can_be_none(self):
        self.programme.participants.remove(self.participant)
        self.assertEqual(0, self.programme.participants.count())

        self._assert_programme_is_valid()

    def test_participants_can_be_added(self):
        second_participant = Portfolio_Company.objects.get(id=301).parent_company
        self.programme.participants.add(second_participant)
        self.assertEqual(2, self.programme.participants.count())
        self._assert_programme_is_valid()

    def test_participants_can_be_removed(self):
        self.programme.participants.remove(self.participant)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.participants.count(), 0)

    def test_participants_can_be_added_multiple_times_without_duplicate(self):
        self.programme.participants.add(self.participant)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.participants.count(), 1)

    def test_multiple_programmes_can_have_same_participants(self):
        second_programme = self._create_second_programme()
        self.programme.participants.remove(self.participant)

        participants = list(second_programme.participants.all())
        for company in participants:
            self.programme.participants.add(company)

        self._assert_programme_is_valid()
        self.assertEqual(second_programme.participants.count(), self.programme.participants.count())

    def test_remove_participant_removes_from_programme_correctly(self):
        Company.objects.get(pk=101).delete()
        self._assert_programme_is_valid()
        all_programmes = list(Programme.objects.all())
        self.assertIn(self.programme, all_programmes)
        self.assertEqual(self.programme.participants.count(), 0)

    # Test coaches_mentors relationship
    def test_coaches_mentors_can_be_none(self):
        self.programme.coaches_mentors.remove(self.coach)
        self.assertEqual(0, self.programme.coaches_mentors.count())
        self._assert_programme_is_valid()

    def test_coaches_mentors_can_be_added(self):
        second_coach = Individual.objects.get(id=2)
        self.programme.coaches_mentors.add(second_coach)
        self.assertEqual(2, self.programme.coaches_mentors.count())
        self._assert_programme_is_valid()

    def test_coaches_mentors_can_be_removed(self):
        self.programme.coaches_mentors.remove(self.coach)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.coaches_mentors.count(), 0)

    def test_coaches_mentors_can_be_added_multiple_times_without_duplicate(self):
        self.programme.coaches_mentors.add(self.coach)
        self._assert_programme_is_valid()
        self.assertEqual(self.programme.coaches_mentors.count(), 1)

    def test_multiple_programmes_can_have_same_coaches_mentors(self):
        second_programme = self._create_second_programme()
        self.programme.coaches_mentors.remove(self.coach)

        coaches = list(second_programme.coaches_mentors.all())
        for individual in coaches:
            self.programme.coaches_mentors.add(individual)

        self._assert_programme_is_valid()
        self.assertEqual(second_programme.coaches_mentors.count(), self.programme.coaches_mentors.count())

    def test_remove_coach_mentor_removes_from_programme_correctly(self):
        Individual.objects.get(id=1).delete()
        self._assert_programme_is_valid()
        all_programmes = list(Programme.objects.all())
        self.assertIn(self.programme, all_programmes)
        self.assertEqual(self.programme.coaches_mentors.count(), 0)

    def test_cover_can_be_blank(self):
        self.programme.cover = None
        self._assert_programme_is_valid()

    def test_cover_non_image_cannot_be_added(self):
        with open("portfolio/tests/models/test.txt", 'r') as f:
            self.programme.cover = f
            self._assert_programme_is_invalid()
            f.close()

    def test_description_can_be_blank(self):
        self.programme.description = ""
        self._assert_programme_is_valid()
