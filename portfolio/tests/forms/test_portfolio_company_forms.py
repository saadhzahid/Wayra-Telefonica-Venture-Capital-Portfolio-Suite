from django.forms import Select, CharField
from django.test import TestCase

from portfolio.forms import PortfolioCompanyCreateForm, PortfolioCompanyEditForm
from portfolio.forms.company_form import ModelChoiceField
from portfolio.models import Company, Portfolio_Company


class PortfolioCompanyCreateFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/other_companies.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'parent_company': self.defaultCompany,
            'wayra_number': 'WN-1'
        }

    def _create_second_portfolio_company(self):
        other_p_company = Portfolio_Company.objects.create(parent_company=Company.objects.get(id=201),
                                                           wayra_number='WN-2')
        return other_p_company

    def test_valid_portfolio_company_create_form(self):
        form = PortfolioCompanyCreateForm(data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PortfolioCompanyCreateForm()
        self.assertIn("parent_company", form.fields)
        self.assertTrue(isinstance(form.fields['parent_company'], ModelChoiceField))
        self.assertTrue(isinstance(form.fields['parent_company'].widget, Select))

        self.assertIn("wayra_number", form.fields)
        self.assertTrue(isinstance(form.fields['wayra_number'], CharField))

    def test_form_must_save_correctly(self):
        form = PortfolioCompanyCreateForm(data=self.form_input)
        before_count = Portfolio_Company.objects.count()
        form.save()
        after_count = Portfolio_Company.objects.count()
        self.assertEqual(after_count, before_count + 1)
        p_company = Portfolio_Company.objects.get(parent_company=self.defaultCompany)
        self.assertEqual(p_company.parent_company, self.form_input['parent_company'])
        self.assertEqual(p_company.wayra_number, self.form_input['wayra_number'])


class PortfolioCompanyEditFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/other_companies.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.p_company = Portfolio_Company.objects.create(
            parent_company=self.defaultCompany,
            wayra_number='WN-1'
        )
        self.form_input = {
            'wayra_number': 'WN-3'
        }

    def _create_second_portfolio_company(self):
        other_p_company = Portfolio_Company.objects.create(parent_company=Company.objects.get(id=201),
                                                           wayra_number='WN-2')
        return other_p_company

    def test_valid_portfolio_company_create_form(self):
        form = PortfolioCompanyEditForm(instance=self.p_company, data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PortfolioCompanyEditForm(instance=self.p_company)
        self.assertIn("wayra_number", form.fields)
        self.assertTrue(isinstance(form.fields['wayra_number'], CharField))

    def test_forms_uses_model_validation(self):
        other_p_company = self._create_second_portfolio_company()
        self.form_input['wayra_number'] = other_p_company.wayra_number
        form = PortfolioCompanyEditForm(instance=self.p_company, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = PortfolioCompanyEditForm(instance=self.p_company, data=self.form_input)
        before_count = Portfolio_Company.objects.count()
        form.save()
        after_count = Portfolio_Company.objects.count()
        self.assertEqual(after_count, before_count)
        p_company = Portfolio_Company.objects.get(parent_company=self.defaultCompany)
        self.assertEqual(p_company.parent_company, self.defaultCompany)
        self.assertEqual(p_company.wayra_number, self.form_input['wayra_number'])
