"""Tests of the individual create view."""
from django.test import TestCase
from django.urls import reverse
from django_countries.fields import Country

from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress, PastExperience, User
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class IndividualCreateViewTestCase(TestCase):
    """Tests of the individual create view."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('individual_create')
        set_session_variables(self.client)

        self.post_input = {
            "form1-name": "Jemma Doe",
            "form1-AngelListLink": "https://www.AngelList.com",
            "form1-CrunchbaseLink": "https://www.Crunchbase.com",
            "form1-LinkedInLink": "https://www.LinkedIn.com",
            "form1-Company": "exampleCompany",
            "form1-Position": "examplePosition",
            "form1-Email": "test@gmail.com",
            "form1-PrimaryNumber_0": "UK",
            "form1-PrimaryNumber_1": "+447975777666",
            "form1-SecondaryNumber_0": "UK",
            "form1-SecondaryNumber_1": "+441325777655",
            "form2-address_line1": "testAdress1",
            "form2-address_line2": "testAdress2",
            "form2-postal_code": "testCode",
            "form2-city": "testCity",
            "form2-state": "testState",
            "form2-country": Country("AD"),
            "0-companyName": "exampleCompany",
            "0-workTitle": "exampleWork",
            "0-start_year": 2033,
            "0-end_year": 2035,
            "0-Description": "testCase",
            "1-companyName": "exampleCompany2",
            "1-workTitle": "exampleWork2",
            "1-start_year": 2034,
            "1-end_year": 2036,
            "1-Description": "testCase2",
        }

    def test_individual_create_view_url(self):
        self.assertEqual(self.url, '/individual_page/individual_create/')

    # Tests if the individual_create_view page renders correctly with the correct forms and html
    def test_get_individual_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        individual_form = response.context['individualForm']
        self.assertTrue(isinstance(individual_form, IndividualCreateForm))
        adress_form = response.context['addressForms']
        self.assertTrue(isinstance(adress_form, AddressCreateForm))
        past_experience_forms = response.context['pastExperienceForms']
        for past_form in past_experience_forms:
            self.assertTrue(isinstance(past_form, PastExperienceForm))
            self.assertFalse(past_form.is_bound)
        self.assertFalse(adress_form.is_bound)
        self.assertFalse(individual_form.is_bound)

    def test_redirect_when_user_access_investor_individual_create_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccessful_individual_create_view_due_to_individual_form(self):
        self.post_input['form1-AngelListLink'] = 'A'
        before_count = Individual.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Individual.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        form = response.context['individualForm']
        self.assertTrue(isinstance(form, IndividualCreateForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_individual_create_view_due_to_adress_form(self):
        self.post_input['form2-country'] = Country("")
        before_count = ResidentialAddress.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = ResidentialAddress.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        form = response.context['addressForms']
        self.assertTrue(isinstance(form, AddressCreateForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_individual_create_view_due_to_past_experience_form(self):
        self.post_input['0-start_year'] = -1
        before_count = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = PastExperience.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        forms = response.context['pastExperienceForms']
        self.assertTrue(isinstance(forms[0], PastExperienceForm))
        self.assertTrue(forms[0].is_bound)

    # Tests if an successful individual_create produces the desired results
    def test_successful_individual_create_view(self):
        before_count_individual = Individual.objects.count()
        before_count_adress = ResidentialAddress.objects.count()
        before_count_past_work = PastExperience.objects.count()
        self.client.post(self.url, self.post_input)
        after_count_individual = ResidentialAddress.objects.count()
        after_count_adress = ResidentialAddress.objects.count()
        after_count_past_work = PastExperience.objects.count()

        self.assertEqual(after_count_individual, before_count_individual + 1)
        individual = Individual.objects.get(Company='exampleCompany')
        self.assertEqual(individual.name, "Jemma Doe")
        self.assertEqual(individual.AngelListLink, "https://www.AngelList.com")
        self.assertEqual(individual.CrunchbaseLink, "https://www.Crunchbase.com")
        self.assertEqual(individual.LinkedInLink, "https://www.LinkedIn.com")
        self.assertEqual(individual.Company, "exampleCompany")
        self.assertEqual(individual.Position, "examplePosition")
        self.assertEqual(individual.Email, "test@gmail.com")
        self.assertEqual(individual.PrimaryNumber, "+447975777666")
        self.assertEqual(individual.SecondaryNumber, "+441325777655")

        self.assertEqual(after_count_adress, before_count_adress + 1)
        residential_adress = ResidentialAddress.objects.get(address_line1='testAdress1')
        self.assertEqual(residential_adress.address_line1, "testAdress1")
        self.assertEqual(residential_adress.address_line2, "testAdress2")
        self.assertEqual(residential_adress.postal_code, "testCode")
        self.assertEqual(residential_adress.city, "testCity")
        self.assertEqual(residential_adress.state, "testState")
        self.assertEqual(residential_adress.country, Country("AD"))
        self.assertEqual(residential_adress.individual, individual)

        self.assertEqual(after_count_past_work, before_count_past_work + 2)
        past_work_1 = PastExperience.objects.get(companyName="exampleCompany")
        self.assertEqual(past_work_1.companyName, "exampleCompany")
        self.assertEqual(past_work_1.workTitle, "exampleWork")
        self.assertEqual(past_work_1.start_year, 2033)
        self.assertEqual(past_work_1.end_year, 2035)
        self.assertEqual(past_work_1.duration, "2")
        self.assertEqual(past_work_1.Description, "testCase")
        self.assertEqual(past_work_1.individual, individual)

        past_work_2 = PastExperience.objects.get(companyName="exampleCompany2")
        self.assertEqual(past_work_2.companyName, "exampleCompany2")
        self.assertEqual(past_work_2.workTitle, "exampleWork2")
        self.assertEqual(past_work_2.start_year, 2034)
        self.assertEqual(past_work_2.end_year, 2036)
        self.assertEqual(past_work_2.duration, "2")
        self.assertEqual(past_work_2.Description, "testCase2")
        self.assertEqual(past_work_2.individual, individual)
