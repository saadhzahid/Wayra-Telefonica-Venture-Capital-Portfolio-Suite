"""Unit tests for the founder modify page."""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import Founder, User, Individual, Company
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class FounderModifyTestCase(TestCase):
    """Unit tests for the founder modify page."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        set_session_variables(self.client)

        self.individual = Individual.objects.create(
            AngelListLink="https://www.AngelList.com",
            CrunchbaseLink="https://www.Crunchbase.com",
            LinkedInLink="https://www.LinkedIn.com",
            Company="exampleCompany",
            Position="examplePosition",
            Email="test@gmail.com",
            PrimaryNumber=PhoneNumber.from_string("+447975777666"),
            SecondaryNumber=PhoneNumber.from_string("+441325777655")
        )

        self.company = Company.objects.create(
            name="Default Ltd",
            company_registration_number="00000000",
            trading_names="Default Ltd",
            previous_names="Default Ltd",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now(),
        )

        self.post_input = {
            "form1-companyFounded": self.company.id,
            "form1-individualFounder": self.individual.id,
        }

        self.url2 = reverse('founder_create')
        self.client.post(self.url2, self.post_input)
        self.listUsed = Founder.objects.filter(companyFounded=self.company)[0]
        self.url = reverse('founder_modify', kwargs={'id': self.listUsed.id})

    def test_founder_modify_url(self):
        self.assertEqual(self.url, '/individual_page/{}/modifyFounder/'.format(self.listUsed.id))

    def test_redirect_when_user_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_founder_update_with_invalid_company_founded_type(self):
        self.post_input['form1-companyFounded'] = 999
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(companyFounded=self.company)[0]
        self.assertEqual(founder.companyFounded, self.company)

    def test_post_founder_update_with_invalid_individual_founder_type(self):
        self.post_input['form1-individualFounder'] = 999
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(companyFounded=self.company)[0]
        self.assertEqual(founder.individualFounder, self.individual)
