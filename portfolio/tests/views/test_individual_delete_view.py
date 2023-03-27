"""Unit tests for the individual delete page."""
from django.test import TestCase
from django.urls import reverse
from django_countries.fields import Country

from portfolio.models import ResidentialAddress, PastExperience, Individual, User
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class IndividualDeleteTestCase(TestCase):
    """Unit tests for the individual delete page."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
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

        self.url2 = reverse('individual_create')
        self.client.post(self.url2, self.post_input)
        self.listUsed = Individual.objects.filter(name="Jemma Doe")[0]
        self.url = reverse('individual_delete', kwargs={'id': self.listUsed.id})

    def test_individual_delete_url(self):
        self.assertEqual(self.url, '/individual_page/{}/delete/'.format(self.listUsed.id))

    def test_redirect_when_user_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_delete(self):
        before_count = Individual.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        self.client.post(self.url, {})
        after_count = Individual.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count - 1, after_count)
        self.assertEqual(before_count2 - 1, after_count2)
        self.assertEqual(before_count3 - 2, after_count3)
