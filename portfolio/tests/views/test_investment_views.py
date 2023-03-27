import datetime
from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from portfolio.forms import InvestmentForm, InvestorCompanyCreateForm, InvestorEditForm, PortfolioCompanyCreateForm, \
    PortfolioCompanyEditForm
from portfolio.models import Company, Portfolio_Company, User, Investment
from portfolio.models.investor_model import Investor
from portfolio.tests.helpers import LogInTester, reverse_with_next


class InvestmentCreateViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VENTURE CAPITAL'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.form_input = {'investor': self.investorCompany.pk,
                           'startup': self.portfolioCompany.pk,
                           'typeOfFoundingRounds': 'Series A',
                           'investmentAmount': 10_000_000,
                           'dateInvested': date(year=2023, month=3, day=5),
                           }
        self.url = reverse('investment_create', kwargs={'company_id': self.defaultCompany.id})

    def test_create_investment_url(self):
        self.assertEqual(self.url, '/investment/create/1')

    def test_get_create_investment_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investment_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestmentForm))
        self.assertFalse(form.is_bound)

    def test_get_create_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_create_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        investment = Investment.objects.first()
        self.assertEqual(investment.investor, Investor.objects.get(pk=self.form_input['investor']))
        self.assertEqual(investment.startup, Portfolio_Company.objects.get(pk=self.form_input['startup']))
        self.assertEqual(investment.typeOfFoundingRounds, self.form_input['typeOfFoundingRounds'])
        self.assertEqual(investment.investmentAmount, self.form_input['investmentAmount'])
        self.assertEqual(investment.dateInvested, date(year=2023, month=3, day=5))

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['dateInvested'] = (date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investment_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestmentForm))
        self.assertTrue(form.is_bound)


class InvestmentUpdateViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolioCompany,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            investmentAmount=1_000_000_000,
            dateExit=None,
        )
        self.form_input = {'investor': self.defaultCompany.pk,
                           'startup': self.portfolioCompany.pk,
                           'typeOfFoundingRounds': 'Series A',
                           'investmentAmount': 10_000_000,
                           'dateInvested': '2023-03-05',
                           }
        self.url = reverse('investment_update', kwargs={'id': 1})

    def test_update_investment_url(self):
        self.assertEqual(self.url, '/investment/update/1')

    def test_get_update_investment_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investment_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestmentForm))
        self.assertFalse(form.is_bound)

    def test_get_update_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_update_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Investment.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Investment.objects.count()

        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        self.assertEqual(before_count, after_count)
        investment = Investment.objects.get(id=1)
        self.assertEqual(investment.investor, Investor.objects.get(pk=self.form_input['investor']))
        self.assertEqual(investment.startup, Portfolio_Company.objects.get(pk=self.form_input['startup']))
        self.assertEqual(investment.typeOfFoundingRounds, self.form_input['typeOfFoundingRounds'])
        self.assertEqual(investment.investmentAmount, self.form_input['investmentAmount'])
        self.assertEqual(investment.dateInvested, date(year=2023, month=3, day=5))

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['dateInvested'] = (date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investment_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestmentForm))
        self.assertTrue(form.is_bound)


class InvestmentDeleteViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolioCompany,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            investmentAmount=1_000_000_000,
            dateExit=None,
        )
        self.url = reverse('investment_delete', kwargs={'id': 1})

    def test_delete_investment_url(self):
        self.assertEqual(self.url, '/investment/delete/1')

    def test_get_delete_investment_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investment_delete.html')

    def test_get_delete_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_delete_investment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_delete(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Investment.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Investment.objects.count()
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        self.assertEqual(before_count - 1, after_count)


class InvestorCreateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'company': self.defaultCompany.pk,
            'classification': 'VENTURE_CAPITAL'
        }
        self.url = reverse('investor_company_create')

    def test_create_investor_company_url(self):
        self.assertEqual(self.url, '/investment/create_investor_company/')

    def test_get_create_investor_company_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investor_company_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorCompanyCreateForm))
        self.assertFalse(form.is_bound)

    def test_get_create_investor_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_create_investor_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Investor.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Investor.objects.count()
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        self.assertEqual(before_count + 1, after_count)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['classification'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investor_company_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorCompanyCreateForm))
        self.assertTrue(form.is_bound)


class InvestorUpdateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VC'
        )
        self.form_input = {
            'company': self.defaultCompany,
            'classification': 'INCUBATOR'
        }
        self.url = reverse('investor_company_update', kwargs={'company_id': 1})

    def test_update_investor_company_url(self):
        self.assertEqual(self.url, '/investment/update_investor_company/1')

    def test_get_update_investor_company_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investor_company_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorEditForm))
        self.assertFalse(form.is_bound)

    def test_get_update_investor_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_update_investor_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Investor.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Investor.objects.count()
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        self.assertEqual(before_count, after_count)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['classification'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/investor_company_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorEditForm))
        self.assertTrue(form.is_bound)


class PortfolioCompanyCreateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'parent_company': self.defaultCompany.pk,
            'wayra_number': 'WN123456'
        }
        self.url = reverse('portfolio_company_create')

    def test_create_portfolio_company_url(self):
        self.assertEqual(self.url, '/investment/create_portfolio_company/')

    def test_get_create_portfolio_company_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/portfolio_company_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PortfolioCompanyCreateForm))
        self.assertFalse(form.is_bound)

    def test_get_create_portfolio_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_create_portfolio_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Portfolio_Company.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Portfolio_Company.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['wayra_number'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/portfolio_company_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PortfolioCompanyCreateForm))
        self.assertTrue(form.is_bound)


class PortfolioUpdateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.portfolio_company = Portfolio_Company.objects.create(
            parent_company=self.defaultCompany,
            wayra_number='WN123456'
        )
        self.form_input = {
            'wayra_number': 'WN654321'
        }
        self.url = reverse('portfolio_company_update', kwargs={'company_id': 1})

    def test_update_portfolio_company_url(self):
        self.assertEqual(self.url, '/investment/update_portfolio_company/1')

    def test_get_update_portfolio_company_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/portfolio_company_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PortfolioCompanyEditForm))
        self.assertFalse(form.is_bound)

    def test_get_update_portfolio_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_update_portfolio_company_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Portfolio_Company.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Portfolio_Company.objects.count()
        self.assertTemplateUsed(response, 'company/company_page.html')
        self.assertEqual(response.context['company'], self.defaultCompany)
        self.assertEqual(before_count, after_count)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['wayra_number'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/portfolio_company_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PortfolioCompanyEditForm))
        self.assertTrue(form.is_bound)
