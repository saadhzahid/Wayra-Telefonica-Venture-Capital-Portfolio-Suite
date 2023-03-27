"""Unit tests for the founder delete page."""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import Founder, User, Individual, Company
from portfolio.tests.helpers import reverse_with_next, set_session_variables


class FounderDeleteTestCase(TestCase):
    """Unit tests for the founder delete page."""
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
        self.url = reverse('founder_delete', kwargs={'id': self.listUsed.id})

    def test_founder_delete_url(self):
        self.assertEqual(self.url, '/individual_page/{}/deleteFounder/'.format(self.listUsed.id))

    def test_redirect_when_user_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_delete(self):
        before_count = Founder.objects.count()
        self.client.post(self.url, {})
        after_count = Founder.objects.count()
        self.assertEqual(before_count - 1, after_count)
