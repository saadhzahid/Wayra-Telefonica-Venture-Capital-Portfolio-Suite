"""Unit tests of the company create form."""
from django import forms
from django.test import TestCase

from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company


class CompanyCreateFormTestCase(TestCase):

    # Set up an examplery input to use for the tests
    def setUp(self):
        self.form_input = {
            "name": "Wayra Ltd",
            "company_registration_number": "00000000",
            "trading_names": "Wayra Ltd",
            "previous_names": "Wayra UK Ltd",
            "registered_address": "default address, London",
            "jurisdiction": "United Kingdom",
        }

    # Default Tests
    def test_valid_company_create_form(self):
        form = CompanyCreateForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CompanyCreateForm()
        self.assertIn('name', form.fields)
        name_field = form.fields['name']
        self.assertTrue(isinstance(name_field, forms.CharField))
        self.assertIn('company_registration_number', form.fields)
        CRN_field = form.fields['company_registration_number']
        self.assertTrue(isinstance(CRN_field, forms.CharField))
        self.assertIn('trading_names', form.fields)
        trading_names_field = form.fields['trading_names']
        self.assertTrue(isinstance(trading_names_field, forms.CharField))
        self.assertIn('previous_names', form.fields)
        previous_names_field = form.fields['previous_names']
        self.assertTrue(isinstance(previous_names_field, forms.CharField))
        self.assertIn('registered_address', form.fields)
        registered_address_field = form.fields['registered_address']
        self.assertTrue(isinstance(registered_address_field, forms.CharField))
        self.assertIn('jurisdiction', form.fields)
        jurisdiction_field = form.fields['jurisdiction']
        self.assertTrue(isinstance(jurisdiction_field, forms.CharField))

    # Test the form using model validation
    def test_form_uses_model_validation(self):
        self.form_input['name'] = 'x' * 61
        form = CompanyCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test if the form saves correctly
    def test_form_must_save_correctly(self):
        form = CompanyCreateForm(data=self.form_input)
        before_count = Company.objects.count()
        form.save()
        after_count = Company.objects.count()
        self.assertEqual(after_count, before_count + 1)
        company = Company.objects.get(company_registration_number='00000000')
        self.assertEqual(company.name, self.form_input['name'])
        self.assertEqual(company.company_registration_number, self.form_input['company_registration_number'])
        self.assertEqual(company.trading_names, self.form_input['trading_names'])
        self.assertEqual(company.previous_names, self.form_input['previous_names'])
        self.assertEqual(company.registered_address, self.form_input['registered_address'])
        self.assertEqual(company.jurisdiction, self.form_input['jurisdiction'])
