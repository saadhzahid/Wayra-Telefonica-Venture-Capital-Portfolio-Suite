from datetime import date

from django.test import TestCase
from django.urls import reverse

from portfolio.forms import ContractRightForm
from portfolio.models import User, Company, Portfolio_Company, Individual
from portfolio.models.investment_model import Investor, Investment, ContractRight
from portfolio.tests.helpers import LogInTester, reverse_with_next, set_session_variables
from vcpms import settings


class ContractRightCreateViewTestCase(TestCase, LogInTester):
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
        self.investment = Investment.objects.create(investor=self.investorCompany,
                                                    startup=self.portfolioCompany,
                                                    typeOfFoundingRounds='Series A',
                                                    investmentAmount=10_000_000,
                                                    dateInvested=date(year=2023, month=3, day=5))

        self.form_input = {
            'right': 'Default Right',
            'details': 'Default Detail'
        }

        self.url = reverse('contract_right_create', kwargs={'investment_id': self.investment.id})

    def test_create_investment_url(self):
        self.assertEqual(self.url, '/contract_right/create/1')

    def test_get_create_investment_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ContractRightForm))
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
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(response.context['investment_id'], self.investment.id)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['right'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ContractRightForm))
        self.assertTrue(form.is_bound)


class ContractRightDeleteViewTestCase(TestCase, LogInTester):
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
        self.investment = Investment.objects.create(investor=self.investorCompany,
                                                    startup=self.portfolioCompany,
                                                    typeOfFoundingRounds='Series A',
                                                    investmentAmount=10_000_000,
                                                    dateInvested=date(year=2023, month=3, day=5))

        self.contractRight = ContractRight.objects.create(
            investment=self.investment,
            right='Default Right',
            details='Default Detail'
        )

        self.url = reverse('contract_right_delete', kwargs={'id': self.contractRight.id})

    def test_delete_contract_right_url(self):
        self.assertEqual(self.url, '/contract_right/delete/1')

    def test_get_delete_contract_right_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_delete.html')

    def test_get_delete_contract_right_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_delete_contract_right_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_invalid_investment_id_redirects_to_dashboard(self):
        self.client.login(username=self.user.email, password="Password123")
        set_session_variables(self.client)
        self.url = reverse('contract_right_delete', kwargs={'id': 2})
        redirect_url = reverse('dashboard')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_delete(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = ContractRight.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = ContractRight.objects.count()
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(response.context['investment_id'], self.investment.id)
        self.assertEqual(before_count - 1, after_count)


class ContractRightListViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_individual.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            company=self.defaultCompany,
            classification='VENTURE CAPITAL'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(pk=101)
        self.investment = Investment.objects.create(investor=self.investorCompany,
                                                    startup=self.portfolioCompany,
                                                    typeOfFoundingRounds='Series A',
                                                    investmentAmount=10_000_000,
                                                    dateInvested=date(year=2023, month=3, day=5))

        self.url = reverse('contract_right_list', kwargs={'investment_id': self.investment.id})

    def _create_contract_rights(self, count):
        for i in range(count):
            self.contractRight = ContractRight.objects.create(
                investment=self.investment,
                right=f'Default Right {i}',
                details=f'Default Detail {i}'
            )

    def test_get_contract_right_url(self):
        self.assertEqual(self.url, '/contract_right_list/1')

    def test_get_contract_right_list(self):
        self.client.login(username=self.user.email, password="Password123")
        self._create_contract_rights(settings.ITEM_ON_PAGE)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(len(response.context['contract_rights']), settings.ITEM_ON_PAGE)
        self.assertEqual(response.context['company_id'], self.defaultCompany.id)
        for i in range(settings.ITEM_ON_PAGE):
            self.assertContains(response, f'Default Right {i}')
            self.assertContains(response, f'Default Detail {i}')

    def test_get_contract_right_list_for_individual_investor(self):

        self.investorIndividual = Investor.objects.create(individual=Individual.objects.first(), classification='Angel')
        self.investment.investor = self.investorIndividual
        self.investment.save()
        self._create_contract_rights(settings.ITEM_ON_PAGE)

        self.client.login(username=self.user.email, password="Password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(len(response.context['contract_rights']), settings.ITEM_ON_PAGE)
        self.assertEqual(response.context['individual_id'], self.investorIndividual.individual_id)
        for i in range(settings.ITEM_ON_PAGE):
            self.assertContains(response, f'Default Right {i}')
            self.assertContains(response, f'Default Detail {i}')

    def test_get_contract_right_list_pagination(self):
        self.client.login(username=self.user.email, password="Password123")
        self._create_contract_rights(2 * settings.ITEM_ON_PAGE + 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')

        page_two_url = reverse('contract_right_list', kwargs={'investment_id': self.investment.id}) + '?page=1'
        response = self.client.get(page_two_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(len(response.context['contract_rights']), settings.ITEM_ON_PAGE)
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('contract_right_list', kwargs={'investment_id': self.investment.id}) + '?page=2'
        response = self.client.get(page_two_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(len(response.context['contract_rights']), settings.ITEM_ON_PAGE)
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('contract_right_list', kwargs={'investment_id': self.investment.id}) + '?page=3'
        response = self.client.get(page_three_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investment/contract_rights/contract_right_list.html')
        self.assertEqual(len(response.context['contract_rights']), 1)
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    def test_invalid_investment_id_redirects_to_dashboard(self):
        self.client.login(username=self.user.email, password="Password123")
        set_session_variables(self.client)
        self.url = reverse('contract_right_list', kwargs={'investment_id': 2})
        redirect_url = reverse('dashboard')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_user_not_logged_in_redirects(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
