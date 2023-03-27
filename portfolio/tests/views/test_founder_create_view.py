"""Unit tests of the founder create view."""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.forms import FounderForm
from portfolio.models import Founder, User, Individual, Company
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class FounderCreateTestCase(TestCase):
    """Unit tests of the founder create view."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('founder_create')
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

    def test_founder_create_url(self):
        self.assertEqual(self.url, '/individual_page/founder_create/')

    def test_founder_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/founder_create.html')
        self.assertIsInstance(response.context['founderForm'], FounderForm)

    def test_founder_create_post(self):
        before_count = Founder.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        self.assertEqual(before_count + 1, after_count)
        redirect_url = reverse('individual_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirect_when_user_access_founder_create_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_founder_request_companyFounded_with_incorrect_type(self):
        self.post_input['form1-companyFounded'] = 999
        before_count = Founder.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)

    def test_post_founder_request_individualFounder_with_incorrect_type(self):
        self.post_input['form1-individualFounder'] = 999
        before_count = Founder.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
