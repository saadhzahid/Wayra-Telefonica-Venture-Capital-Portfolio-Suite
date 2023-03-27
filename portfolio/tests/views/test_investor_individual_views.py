from django.test import TestCase
from django.urls import reverse

from portfolio.forms import InvestorIndividualCreateForm, InvestorEditForm
from portfolio.models import User, Investor, Individual
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class InvestorIndividualCreateView(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        set_session_variables(self.client)
        self.defaultIndividual = Individual.objects.get(id=1)
        self.form_input = {
            'individual': self.defaultIndividual.pk,
            'classification': 'VENTURE_CAPITAL'
        }
        self.url = reverse('investor_individual_create')

    def test_create_investor_individual_url(self):
        self.assertEqual(self.url, '/individual_page/investor_individual_create/')

    def test_get_create_investor_individual_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/investor_individual_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorIndividualCreateForm))
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
        self.assertTemplateUsed(response, 'individual/individual_page.html')
        self.assertEqual(before_count + 1, after_count)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['classification'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/investor_individual_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorIndividualCreateForm))
        self.assertTrue(form.is_bound)


class InvestorIndividualUpdateView(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_individual.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultIndividual = Individual.objects.get(id=1)
        self.investorCompany = Investor.objects.create(
            individual=self.defaultIndividual,
            classification='VENTURE_CAPITAL'
        )
        self.form_input = {
            'individual': self.defaultIndividual,
            'classification': 'INCUBATOR'
        }
        self.url = reverse('investor_individual_modify', kwargs={'id': 1})

    def test_update_investor_individual_url(self):
        self.assertEqual(self.url, '/individual_page/1/investor_individual_modify/')

    def test_get_update_investor_individual_url(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/investor_individual_modify.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorEditForm))
        self.assertFalse(form.is_bound)

    def test_get_update_investor_individual_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_update_investor_individual_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Investor.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Investor.objects.count()
        self.assertTemplateUsed(response, 'individual/individual_about_page.html')
        self.assertEqual(response.context['individual'], self.defaultIndividual)
        self.assertEqual(before_count, after_count)

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['classification'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/investor_individual_modify.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, InvestorEditForm))
        self.assertTrue(form.is_bound)
