"""Unit tests for the founder form."""
from django import forms
from django.test import TestCase
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.forms import FounderForm
from portfolio.models import Founder, Individual, Company


class FounderFormTestCase(TestCase):
    """Unit tests for the founder form."""

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

        self.form_input = {
            "companyFounded": self.company.pk,
            "individualFounder": self.individual.pk,
        }

    def test_valid_founder_form(self):
        form = FounderForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = FounderForm()
        self.assertIn('companyFounded', form.fields)
        self.assertTrue(isinstance(form.fields['companyFounded'], forms.ModelChoiceField))
        self.assertIn('individualFounder', form.fields)
        self.assertTrue(isinstance(form.fields['individualFounder'], forms.ModelChoiceField))

    def test_form_saves_correctly(self):
        form = FounderForm(data=self.form_input)
        before_count = Founder.objects.count()
        form.save()
        after_count = Founder.objects.count()
        self.assertEqual(after_count, before_count + 1)
        founder = Founder.objects.get(companyFounded=self.company)
        self.assertEqual(founder.companyFounded, self.company)
        self.assertEqual(founder.individualFounder, self.individual)
