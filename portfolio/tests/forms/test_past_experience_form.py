from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.forms import PastExperienceForm
from portfolio.models import Individual, PastExperience


class PastExperienceFormTestCase(TestCase):
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

        self.form_input = {
            'companyName': "Startup",
            'workTitle': "CEO",
            'start_year': 1995,
            'end_year': 1998,
            'Description': "I am the CEO of Startup."
        }

    def test_valid_create_form(self):
        form = PastExperienceForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PastExperienceForm()
        self.assertIn("companyName", form.fields)
        self.assertIn("workTitle", form.fields)
        self.assertIn("start_year", form.fields)
        self.assertIn('end_year', form.fields)
        self.assertIn('Description', form.fields)

    def test_form_must_save_correctly(self):
        form = PastExperienceForm(data=self.form_input)
        before_count = PastExperience.objects.count()
        new_experience = form.save(commit=False)
        new_experience.individual = self.individual
        new_experience.save()
        after_count = PastExperience.objects.count()
        self.assertEqual(after_count, before_count + 1)
        experience = PastExperience.objects.get(companyName='Startup')
        self.assertEqual(experience.companyName, "Startup")
        self.assertEqual(experience.workTitle, "CEO")
        self.assertEqual(experience.start_year, 1995)
        self.assertEqual(experience.end_year, 1998)
        self.assertEqual(experience.Description, "I am the CEO of Startup.")
        self.assertEqual(experience.individual, self.individual)
