"""Unit tests of the sign up form."""
from django import forms
from django.forms.fields import URLField, CharField
from django.test import TestCase
from phonenumber_field.formfields import PhoneNumberField

from portfolio.forms import IndividualCreateForm
from portfolio.models import Individual


class CreateFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            "name": "Jemma Doe",
            "AngelListLink": "https://www.AngelList.com",
            "CrunchbaseLink": "https://www.Crunchbase.com",
            "LinkedInLink": "https://www.LinkedIn.com",
            "Company": "exampleCompany",
            "Position": "examplePosition",
            "Email": "test@gmail.com",
            "PrimaryNumber_0": "UK",
            "PrimaryNumber_1": "+447975777666",
            "SecondaryNumber_0": "UK",
            "SecondaryNumber_1": "+441325777655"
        }

    # Test if the form accepts valid input
    def test_valid_individual_create_form(self):
        form = IndividualCreateForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = IndividualCreateForm()
        self.assertIn("name", form.fields)
        self.assertTrue(isinstance(form.fields['name'], CharField))
        self.assertIn("AngelListLink", form.fields)
        self.assertTrue(isinstance(form.fields['AngelListLink'], URLField))
        self.assertIn("CrunchbaseLink", form.fields)
        self.assertTrue(isinstance(form.fields['CrunchbaseLink'], URLField))
        self.assertIn("LinkedInLink", form.fields)
        self.assertTrue(isinstance(form.fields['LinkedInLink'], URLField))
        self.assertIn("Company", form.fields)
        self.assertIn("Position", form.fields)
        self.assertIn('Email', form.fields)
        self.assertTrue(isinstance(form.fields['Email'], forms.EmailField))
        self.assertIn('PrimaryNumber', form.fields)
        self.assertTrue(isinstance(form.fields['PrimaryNumber'], PhoneNumberField))
        self.assertIn('SecondaryNumber', form.fields)
        self.assertTrue(isinstance(form.fields['SecondaryNumber'], PhoneNumberField))

    # Test the form using model validation
    def test_form_uses_model_validation(self):
        self.form_input['AngelListLink'] = 'A'
        form = IndividualCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test if the form saves correctly
    def test_form_must_save_correctly(self):
        form = IndividualCreateForm(data=self.form_input)
        before_count = Individual.objects.count()
        form.save()
        after_count = Individual.objects.count()
        self.assertEqual(after_count, before_count + 1)
        individual = Individual.objects.get(Company='exampleCompany')
        self.assertEqual(individual.AngelListLink, "https://www.AngelList.com")
        self.assertEqual(individual.CrunchbaseLink, "https://www.Crunchbase.com")
        self.assertEqual(individual.LinkedInLink, "https://www.LinkedIn.com")
        self.assertEqual(individual.Company, "exampleCompany")
        self.assertEqual(individual.Position, "examplePosition")
        self.assertEqual(individual.Email, "test@gmail.com")
        self.assertEqual(individual.PrimaryNumber, "+447975777666")
        self.assertEqual(individual.SecondaryNumber, "+441325777655")
