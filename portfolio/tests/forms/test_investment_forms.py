from datetime import date

from django.forms import *
from django.test import TestCase

from portfolio.forms import InvestmentForm, InvestorChoiceField, ContractRightForm, InvestorCompanyCreateForm, \
    InvestorIndividualCreateForm, InvestorEditForm
from portfolio.models import Company, Portfolio_Company, Investment, Individual
from portfolio.models.investment_model import ContractRight
from portfolio.models.investor_model import Investor


class InvestmentFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.form_input = {'investor': self.investorCompany,
                           'startup': self.portfolioCompany,
                           'typeOfFoundingRounds': 'Series A',
                           'investmentAmount': 10_000_000,
                           # 'dateInvested': datetime.now().date(),
                           'dateInvested': '2023-03-05',
                           }

    def test_valid_investment_create_form(self):
        form = InvestmentForm(data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = InvestmentForm()
        self.assertIn("investor", form.fields)
        self.assertTrue(isinstance(form.fields['investor'], InvestorChoiceField))
        self.assertIn("startup", form.fields)
        self.assertTrue(isinstance(form.fields['startup'], ModelChoiceField))
        self.assertIn("typeOfFoundingRounds", form.fields)
        self.assertTrue(isinstance(form.fields['typeOfFoundingRounds'], ChoiceField))
        self.assertIn("investmentAmount", form.fields)
        self.assertTrue(isinstance(form.fields['investmentAmount'], DecimalField))
        self.assertIn("dateInvested", form.fields)
        self.assertTrue(isinstance(form.fields['dateInvested'], DateField))
        self.assertTrue(isinstance(form.fields['dateInvested'].widget, DateInput))

    def test_forms_uses_model_validation(self):
        self.form_input['dateInvested'] = "INVALID_DATE"
        form = InvestmentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = InvestmentForm(data=self.form_input)
        before_count = Investment.objects.count()
        form.save()
        after_count = Investment.objects.count()
        self.assertEqual(after_count, before_count + 1)
        investment = Investment.objects.get(investor=self.investorCompany, startup=self.portfolioCompany,
                                            dateInvested=date(year=2023, month=3, day=5))
        self.assertEqual(investment.investor, self.form_input['investor'])
        self.assertEqual(investment.startup.id, self.form_input['startup'].id)
        self.assertEqual(investment.typeOfFoundingRounds, self.form_input['typeOfFoundingRounds'])
        self.assertEqual(investment.investmentAmount, self.form_input['investmentAmount'])
        self.assertEqual(investment.dateInvested, date(year=2023, month=3, day=5))


class ContractRightFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.investment = Investment.objects.create(investor=self.investorCompany,
                                                    startup=self.portfolioCompany,
                                                    typeOfFoundingRounds='Series A',
                                                    investmentAmount=10_000_000,
                                                    dateInvested='2023-03-05')
        self.form_input = {
            'right': 'Default Right',
            'details': 'Default Detail'
        }

    def test_valid_contract_right_create_form(self):
        form = ContractRightForm(data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = ContractRightForm()
        self.assertIn("right", form.fields)
        self.assertTrue(isinstance(form.fields['right'], CharField))
        self.assertIn("details", form.fields)
        self.assertTrue(isinstance(form.fields['details'], CharField))

    def test_forms_uses_model_validation(self):
        self.form_input['right'] = None
        form = ContractRightForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = ContractRightForm(data=self.form_input)
        before_count = ContractRight.objects.count()
        form.saveInvestment(self.investment)
        form.save()
        after_count = ContractRight.objects.count()
        self.assertEqual(after_count, before_count + 1)
        contractRight = ContractRight.objects.get(investment=self.investment)
        self.assertEqual(contractRight.right, self.form_input['right'])
        self.assertEqual(contractRight.details, self.form_input['details'])


class InvestorCompanyCreateFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'company': self.defaultCompany,
            'classification': 'VENTURE_CAPITAL'
        }

    def test_valid_investor_company_create_form(self):
        form = InvestorCompanyCreateForm(data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = InvestorCompanyCreateForm()
        self.assertIn("company", form.fields)
        self.assertTrue(isinstance(form.fields['company'], ModelChoiceField))
        self.assertTrue(isinstance(form.fields['company'].widget, Select))

        self.assertIn("classification", form.fields)
        self.assertTrue(isinstance(form.fields['classification'], ChoiceField))

    def test_forms_uses_model_validation(self):
        self.form_input['company'] = None
        form = InvestorCompanyCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = InvestorCompanyCreateForm(data=self.form_input)
        before_count = Investor.objects.count()
        form.save()
        after_count = Investor.objects.count()
        self.assertEqual(after_count, before_count + 1)
        investor = Investor.objects.get(company=self.defaultCompany)
        self.assertEqual(investor.company, self.form_input['company'])
        self.assertEqual(investor.individual, None)
        self.assertEqual(investor.classification, self.form_input['classification'])


class InvestorIndividualCreateFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.defaultIndividual = Individual.objects.get(id=1)
        self.form_input = {
            'individual': self.defaultIndividual,
            'classification': 'ANGEL_GROUP'
        }

    def test_valid_investor_company_create_form(self):
        form = InvestorIndividualCreateForm(data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = InvestorIndividualCreateForm()
        self.assertIn("individual", form.fields)
        self.assertTrue(isinstance(form.fields['individual'], ModelChoiceField))
        self.assertTrue(isinstance(form.fields['individual'].widget, Select))

        self.assertIn("classification", form.fields)
        self.assertTrue(isinstance(form.fields['classification'], ChoiceField))

    def test_forms_uses_model_validation(self):
        self.form_input['individual'] = None
        form = InvestorIndividualCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = InvestorIndividualCreateForm(data=self.form_input)
        before_count = Investor.objects.count()
        form.save()
        after_count = Investor.objects.count()
        self.assertEqual(after_count, before_count + 1)
        investor = Investor.objects.get(individual=self.defaultIndividual)
        self.assertEqual(investor.individual, self.form_input['individual'])
        self.assertEqual(investor.company, None)
        self.assertEqual(investor.classification, self.form_input['classification'])


class InvestorEditFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.defaultIndividual = Individual.objects.get(id=1)
        self.investor = Investor.objects.create(
            individual=self.defaultIndividual,
            classification='ANGEL_GROUP'
        )
        self.form_input = {
            'classification': 'INCUBATOR'
        }

    def test_valid_investor_company_create_form(self):
        form = InvestorEditForm(instance=self.investor, data=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = InvestorEditForm(instance=self.investor)
        self.assertIn("classification", form.fields)
        self.assertTrue(isinstance(form.fields['classification'], ChoiceField))

    def test_forms_uses_model_validation(self):
        self.form_input['classification'] = None
        form = InvestorEditForm(instance=self.investor, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = InvestorEditForm(instance=self.investor, data=self.form_input)
        before_count = Investor.objects.count()
        form.save()
        after_count = Investor.objects.count()
        self.assertEqual(after_count, before_count)
        investor = Investor.objects.get(individual=self.defaultIndividual)
        self.assertEqual(investor.individual, self.defaultIndividual)
        self.assertEqual(investor.company, None)
        self.assertEqual(investor.classification, self.form_input['classification'])
