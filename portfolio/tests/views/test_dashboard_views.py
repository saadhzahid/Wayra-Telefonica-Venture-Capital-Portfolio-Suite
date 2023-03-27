"""Unit tests of the dashboard views"""
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import CompanyCreateForm
from portfolio.models import User, Company, Portfolio_Company, Investor
from portfolio.tests.helpers import LogInTester, reverse_with_next
from portfolio.tests.helpers import set_session_variables, set_session_company_filter_variable


class DashboardViewTestCase(TestCase, LogInTester):
    """Unit tests of the dashboard view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/default_portfolio_company.json",
        "portfolio/tests/fixtures/other_companies.json",
        "portfolio/tests/fixtures/other_portfolio_companies.json",
        "portfolio/tests/fixtures/default_investor_company.json",
        "portfolio/tests/fixtures/other_investor_companies.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('dashboard')
        self.search_url = reverse('company_search_result')
        self.portfolio_company_url = reverse('portfolio_company', kwargs={'company_id': 1})
        self.create_company_url = reverse('create_company')
        self.update_company_url = reverse('update_company', kwargs={'company_id': 1})
        self.delete_company_url = reverse('delete_company', kwargs={'company_id': 1})
        self.archive_company_url = reverse('archive_company', kwargs={'company_id': 1})
        self.unarchive_company_url = reverse('unarchive_company', kwargs={'company_id': 1})
        self.change_company_layout_url = reverse('change_company_layout')
        self.change_company_filter_url = reverse('change_company_filter')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        self.create_company_form_input = {
            "name": "Wayra Ltd",
            "company_registration_number": "00000007",
            "trading_names": "Wayra Ltd",
            "previous_names": "Wayra UK Ltd",
            "registered_address": "default address, London",
            "jurisdiction": "United Kingdom",
        }
        set_session_variables(self.client)

    def test_dashboard_urls(self):
        self.assertEqual(self.url, '/dashboard/')
        self.assertEqual(self.search_url, '/search_result')
        self.assertEqual(self.portfolio_company_url, '/portfolio_company/1')
        self.assertEqual(self.create_company_url, '/portfolio_company/company_create/')
        self.assertEqual(self.update_company_url, '/portfolio_company/company_update/1')
        self.assertEqual(self.delete_company_url, '/portfolio_company/company_delete/1')
        self.assertEqual(self.archive_company_url, '/portfolio_company/archive/1')
        self.assertEqual(self.unarchive_company_url, '/portfolio_company/unarchive/1')
        self.assertEqual(self.change_company_layout_url, '/change_company_layout/')
        self.assertEqual(self.change_company_filter_url, '/change_company_filter/')

    ##  Dashboard tests
    def test_get_dashboard(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/main_dashboard.html')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_dashboard_filters_all_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        companies = response.context['companies']
        self.assertEqual(len(companies), 6)

    def test_get_dashboard_filters_portfolio_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 2)
        response = self.client.get(self.url)
        companies = response.context['companies']
        self.assertEqual(len(companies), 3)

    def test_get_dashboard_filters_investor_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 3)
        response = self.client.get(self.url)
        companies = response.context['companies']
        self.assertEqual(len(companies), 3)

    ##  Search Comp Tests
    def test_get_search_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.search_url, data={'searchresult': 'l'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_get_search_company_returns_correct_data_for_all_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.search_url, data={'searchresult': 'l'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Company.objects.filter(name__contains="l", is_archived=False).values()[:5]
        for company in company_search_result:
            self.assertContains(response, company['name'])
        self.assertEqual(len(company_search_result), 5)

    def test_get_search_company_returns_correct_data_for_portfolio_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 2)
        response = self.client.get(self.search_url, data={'searchresult': 'lt'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Portfolio_Company.objects.filter(parent_company__is_archived=False,
                                                                 parent_company__name__contains='lt')[:5]
        for company in company_search_result:
            self.assertContains(response, company.parent_company.name)
        self.assertEqual(len(company_search_result), 3)

    def test_get_search_company_returns_correct_data_for_investor_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 3)
        response = self.client.get(self.search_url, data={'searchresult': 'lt'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        investors = Investor.objects.all()
        search_result = Company.objects.filter(id__in=investors.values('company'), is_archived=False,
                                               name__contains='lt').order_by('id')[:5]
        for company in search_result:
            self.assertContains(response, company.name)
        self.assertEqual(len(search_result), 3)

    def test_search_company_with_blank_query(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.search_url, {'searchresult': ''})
        self.assertEqual(response.status_code, 200)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("partials/search/search_results_table.html", template_names)
        self.assertNotContains(response, 'No Search Results Found.')

    def test_post_search_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.search_url, follow=True, data={'searchresult': 'l'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/main_dashboard.html')

    def test_post_search_company_filters_all_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.search_url, follow=True, data={'searchresult': 'l'})
        companies = response.context['companies']
        self.assertEqual(len(companies), 5)

    def test_post_search_company_filters_portfolio_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 2)
        response = self.client.post(self.search_url, follow=True, data={'searchresult': 'l'})
        companies = response.context['companies']
        self.assertEqual(len(companies), 3)

    def test_post_search_company_filters_investor_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 3)
        response = self.client.post(self.search_url, follow=True, data={'searchresult': 'l'})
        companies = response.context['companies']
        self.assertEqual(len(companies), 0)

    ## Portfolio Company Tests
    def test_get_portfolio_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.portfolio_company_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/company_page.html')
        company = response.context['company']
        self.assertEqual(company.id, 1)

    ##  Create Company Tests
    def test_get_create_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.create_company_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/company_create.html')
        form = response.context['form']
        self.assertIsInstance(form, CompanyCreateForm)

    def test_post_create_company(self):
        self.client.login(email=self.user.email, password="Password123")
        form = CompanyCreateForm(data=self.create_company_form_input)
        self.assertIsInstance(form, CompanyCreateForm)
        self.assertTrue(form.is_valid())
        before_count = Company.objects.count()
        response = self.client.post(self.create_company_url, self.create_company_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Company.objects.count()
        self.assertEqual(before_count, after_count - 1)

        ##  Update Company Tests

    def test_get_update_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.update_company_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/company_update.html')
        form = response.context['form']
        self.assertIsInstance(form, CompanyCreateForm)

    def test_post_update_company(self):
        self.client.login(email=self.user.email, password="Password123")
        self.create_company_form_input['company_registration_number'] = '00000001'
        form = CompanyCreateForm(data=self.create_company_form_input)
        self.assertIsInstance(form, CompanyCreateForm)
        self.assertTrue(form.is_valid())
        company = Company.objects.get(id=1)
        form = CompanyCreateForm(data=self.create_company_form_input, instance=company)
        self.assertTrue(form.is_valid())
        name_before = company.name
        response = self.client.post(self.create_company_url, self.create_company_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        company = Company.objects.get(id=1)
        name_after = company.name
        self.assertNotEqual(name_before, name_after)

    ##  Delete Company Tests
    def test_get_delete_company(self):
        self.client.login(email=self.user.email, password="Password123")
        count_before = Company.objects.count()
        response = self.client.get(self.delete_company_url)
        count_after = Company.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_after, count_before - 1)

    ##  Archive Company Tests
    def test_get_archive_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.archive_company_url)
        company = Company.objects.get(id=1)
        self.assertTrue(company.is_archived)

    ##  Unarchive Company Tests
    def test_get_unarchive_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.unarchive_company_url)
        company = Company.objects.get(id=1)
        self.assertFalse(company.is_archived)

    ## Change layout Number Tests
    def test_get_change_layout(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.change_company_layout_url, data={'layout_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['company_layout']), 1)

    def test_get_change_layout_returns_correct_data_for_all_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.change_company_layout_url, data={'layout_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Company.objects.filter(is_archived=False).values()
        self.assertEqual(len(company_search_result), 8)

    def test_get_change_layout_returns_correct_data_for_portfolio_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 2)
        response = self.client.get(self.change_company_layout_url, data={'layout_number': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Portfolio_Company.objects.filter(parent_company__is_archived=False)
        self.assertEqual(len(company_search_result), 3)

    def test_get_cahnge_layout_returns_correct_data_for_investor_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 3)
        response = self.client.get(self.change_company_layout_url, data={'layout_number': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        investors = Investor.objects.all()
        result = Company.objects.filter(id__in=investors.values('company'), is_archived=False).order_by('id')
        for company in result:
            self.assertContains(response, company.name)
        self.assertEqual(len(result), 3)

    ## Change filter Number Tests
    def test_get_change_filter(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.change_company_filter_url, data={'filter_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    # def test_get_change_filter_with_no_filter_number(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     response = self.client.get(self.change_company_filter_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response, HttpResponse)

    def test_get_change_filter_returns_correct_data_for_all_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.change_company_filter_url, data={'filter_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Company.objects.filter(is_archived=False).values()
        self.assertEqual(len(company_search_result), 8)

    def test_get_change_filter_returns_correct_data_for_portfolio_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 2)
        response = self.client.get(self.change_company_filter_url, data={'filter_number': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        company_search_result = Portfolio_Company.objects.filter(parent_company__is_archived=False)
        for company in company_search_result:
            self.assertContains(response, company.parent_company.name)
        self.assertEqual(len(company_search_result), 3)

    def test_get_change_filtetr_returns_correct_data_for_investor_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_company_filter_variable(self.client, 3)
        response = self.client.get(self.change_company_filter_url, data={'filter_number': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        investors = Investor.objects.all()
        result = Company.objects.filter(id__in=investors.values('company'), is_archived=False).order_by('id')
        for company in result:
            self.assertContains(response, company.name)
        self.assertEqual(len(result), 3)
