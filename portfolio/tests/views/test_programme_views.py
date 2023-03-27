"""Unit tests of the dashboard views"""
import os
import shutil
import time
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Company, Individual, Programme
from portfolio.models import User, Portfolio_Company
from portfolio.tests.helpers import LogInTester, reverse_with_next
from portfolio.tests.helpers import set_session_variables
from vcpms.settings import MEDIA_ROOT


class ProgrammeCreateViewTestCase(TestCase, LogInTester):
    """Unit tests of the programme list view"""
    DEFAULT_FIXTURES = ['portfolio/tests/fixtures/default_company.json',
                        'portfolio/tests/fixtures/default_individual.json',
                        'portfolio/tests/fixtures/default_portfolio_company.json',
                        'portfolio/tests/fixtures/default_programme.json',
                        'portfolio/tests/fixtures/default_user.json',
                        'portfolio/tests/fixtures/other_users.json',
                        ]

    OTHER_FIXTURES = ['portfolio/tests/fixtures/other_companies.json',
                      'portfolio/tests/fixtures/other_individuals.json',
                      'portfolio/tests/fixtures/other_portfolio_companies.json',
                      'portfolio/tests/fixtures/other_programmes.json',
                      ]
    fixtures = DEFAULT_FIXTURES + OTHER_FIXTURES

    def setUp(self) -> None:
        self.url = reverse('programme_create')
        self.user = User.objects.get(email="john.doe@example.org")
        self.defaultCompany = Company.objects.get(id=1)
        self.portfolioCompany = Company.objects.get(id=101)
        self.individual = Individual.objects.get(id=1)
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        set_session_variables(self.client)

        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")
        self.form_input = {
            "name": "Accelerator Programme",
            "cohort": 2,  # avoid pk of default_programme
            "partners": [self.defaultCompany.pk],  # for pk of default_company
            "participants": [self.portfolioCompany.pk],  # for pk of default_portfolio_company
            "coaches_mentors": [self.individual.pk],  # for pk of default_individual
            "cover": self.file_data
        }
        self.default_programme = Programme.objects.get(id=1)
        # TODO: Reset media directory should write a proper way soon
        # media_files = os.listdir(MEDIA_ROOT)
        # for file in media_files:
        #     file_path = os.path.join(MEDIA_ROOT, file)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        path = os.path.join(MEDIA_ROOT, f'programmes/{self.form_input["name"]}')
        path = os.path.normpath(path)
        for i in range(10):
            # Multithreaded test causes locking
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
            except IOError:
                time.sleep(.1)

    def test_create_programme_url(self):
        self.assertEqual(self.url, '/programme_page/create/')

    # Tests if the programme create page renders correctly with the correct forms and html
    def test_get_programme_create_view(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_create_page.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateProgrammeForm))
        self.assertFalse(form.is_bound)

    def test_programme_create_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # TODO:FIX THIS TEST
    def test_successful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'programmes/programme_list_page.html')

    def test_unsuccessful_form(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['name'] = ""
        response = self.client.post(self.url, self.form_input)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_create_page.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateProgrammeForm))
        self.assertTrue(form.is_bound)


class ProgrammeUpdateViewTestCase(TestCase, LogInTester):
    """Unit tests of the programme list view"""
    DEFAULT_FIXTURES = ['portfolio/tests/fixtures/default_company.json',
                        'portfolio/tests/fixtures/default_individual.json',
                        'portfolio/tests/fixtures/default_portfolio_company.json',
                        'portfolio/tests/fixtures/default_programme.json',
                        'portfolio/tests/fixtures/default_user.json',
                        'portfolio/tests/fixtures/other_users.json',
                        ]

    OTHER_FIXTURES = ['portfolio/tests/fixtures/other_companies.json',
                      'portfolio/tests/fixtures/other_individuals.json',
                      'portfolio/tests/fixtures/other_portfolio_companies.json',
                      'portfolio/tests/fixtures/other_programmes.json',
                      ]
    fixtures = DEFAULT_FIXTURES + OTHER_FIXTURES

    def setUp(self) -> None:
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        set_session_variables(self.client)

        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")

        self.default_programme = Programme.objects.get(id=1)
        self.partner = Company.objects.first()
        self.participant = Portfolio_Company.objects.first().parent_company
        self.coach = Individual.objects.first()

        self.default_programme.cover = self.file_data
        self.default_programme.partners.add(self.partner)
        self.default_programme.participants.add(self.participant)
        self.default_programme.coaches_mentors.add(self.coach)

        self.target_programme = Programme.objects.get(id=1)
        self.url = reverse('programme_update', kwargs={'id': self.target_programme.id})
        # TODO: Reset media directory should write a proper way soon
        # media_files = os.listdir(MEDIA_ROOT)
        # for file in media_files:
        #     file_path = os.path.join(MEDIA_ROOT, file)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        path = os.path.join(MEDIA_ROOT, f'programmes/{self.default_programme.name}')
        path = os.path.normpath(path)
        for i in range(10):
            # Multithreaded test causes locking
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
            except IOError:
                time.sleep(.1)

    def test_update_programme_url(self):
        self.assertEqual(self.url, f'/programme_page/{self.target_programme.id}/update/')

    def test_get_programme_update_view(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_update_page.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProgrammeForm))
        self.assertFalse(form.is_bound)

    def test_programme_update_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # TODO:FIX THIS TEST
    def test_successful_update_programme(self):
        self.client.login(email=self.user.email, password="Password123")
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")
        self.form_input = {
            "name": "Different Name",
            "cohort": 2,  # avoid pk of default_programme
            "partners": [self.partner.pk],  # for pk of default_company
            "participants": [self.participant.pk],  # for pk of default_portfolio_company
            "coaches_mentors": [self.coach.pk],  # for pk of default_individual
            "cover": self.file_data
        }
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'programmes/programme_list_page.html')
        self.assertEqual(Programme.objects.get(id=1).name, 'Different Name')

    def test_unsuccessful_update_programme(self):
        self.client.login(email=self.user.email, password="Password123")
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")
        self.form_input = {
            "name": "",
            "cohort": 2,  # avoid pk of default_programme
            "partners": [1],  # for pk of default_company
            "participants": [1],  # for pk of default_portfolio_company
            "coaches_mentors": [1],  # for pk of default_individual
            "cover": self.file_data
        }
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'programmes/programme_update_page.html')
        self.assertEqual(Programme.objects.get(id=1).name, 'Accelerator Programme')


class ProgrammeDeleteViewTestCase(TestCase, LogInTester):
    """Unit tests of the programme list view"""
    DEFAULT_FIXTURES = ['portfolio/tests/fixtures/default_company.json',
                        'portfolio/tests/fixtures/default_individual.json',
                        'portfolio/tests/fixtures/default_portfolio_company.json',
                        'portfolio/tests/fixtures/default_programme.json',
                        'portfolio/tests/fixtures/default_user.json',
                        'portfolio/tests/fixtures/other_users.json',
                        ]

    OTHER_FIXTURES = ['portfolio/tests/fixtures/other_companies.json',
                      'portfolio/tests/fixtures/other_individuals.json',
                      'portfolio/tests/fixtures/other_portfolio_companies.json',
                      'portfolio/tests/fixtures/other_programmes.json',
                      ]
    fixtures = DEFAULT_FIXTURES + OTHER_FIXTURES

    def setUp(self) -> None:
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        set_session_variables(self.client)

        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")
        self.form_input = {
            "name": "Accelerator Programme",
            "cohort": 2,  # avoid pk of default_programme
            "partners": [1],  # for pk of default_company
            "participants": [1],  # for pk of default_portfolio_company
            "coaches_mentors": [1],  # for pk of default_individual
            "cover": self.file_data
        }
        self.default_programme = Programme.objects.get(id=1)
        self.target_programme = Programme.objects.get(id=1)
        self.url = reverse('programme_delete', kwargs={'id': self.target_programme.id})
        # TODO: Reset media directory should write a proper way soon
        # media_files = os.listdir(MEDIA_ROOT)
        # for file in media_files:
        #     file_path = os.path.join(MEDIA_ROOT, file)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        path = os.path.join(MEDIA_ROOT, f'programmes/{self.default_programme.name}')
        path = os.path.normpath(path)

        for i in range(10):
            # Multithreaded test causes locking
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
            except IOError:
                time.sleep(.1)

    def test_delete_programme_url(self):
        self.assertEqual(self.url, f'/programme_page/{self.target_programme.id}/delete/')

    def test_programme_delete_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_delete(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Programme.objects.count()
        self.client.post(self.url, {})
        after_count = Programme.objects.count()
        self.assertEqual(before_count - 1, after_count)


class ProgrammeListViewTestCase(TestCase, LogInTester):
    """Unit tests of the programme list view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('programme_list')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        set_session_variables(self.client)

    def test_programme_url(self):
        self.assertEqual(self.url, '/programme_page/')

    def test_get_list(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_list_page.html')

    def test_get_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class ProgrammeDetailViewTestCase(TestCase, LogInTester):
    """Unit tests of the programme list view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/default_portfolio_company.json",
        "portfolio/tests/fixtures/default_individual.json",
        "portfolio/tests/fixtures/default_programme.json",

        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        self.defaultCompany = Company.objects.get(id=1)
        self.portfolioCompany = Company.objects.get(id=101)
        self.coach = Individual.objects.get(id=1)

        self.programme = Programme.objects.get(id=1)
        self.programme.partners.add(self.defaultCompany)
        self.programme.participants.add(self.portfolioCompany)
        self.programme.coaches_mentors.add(self.coach)

        self.url = reverse('programme_detail', kwargs={'id': 1})
        # set_session_variables(self.client)

    def test_programme_url(self):
        self.assertEqual(self.url, '/programme_page/1')

    def test_get_programme_detail(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_page.html')
        self.assertEqual(response.context['id'], self.programme.id)
        self.assertEqual(set(response.context['partners']), {self.defaultCompany})
        self.assertEqual(set(response.context['participants']), {self.portfolioCompany})
        self.assertEqual(set(response.context['coaches_mentors']), {self.coach})

    def test_get_detail_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class SearchProgrammeViewTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/default_portfolio_company.json",
        "portfolio/tests/fixtures/default_individual.json",
        "portfolio/tests/fixtures/default_programme.json",

        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        self.defaultCompany = Company.objects.get(id=1)
        self.portfolioCompany = Company.objects.get(id=101)
        self.coach = Individual.objects.get(id=1)

        self.programme = Programme.objects.get(id=1)
        self.programme.partners.add(self.defaultCompany)
        self.programme.participants.add(self.portfolioCompany)
        self.programme.coaches_mentors.add(self.coach)

        self.url = reverse('programme_search_result')

    def test_get_search_programme(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'searchresult': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_get_search_programme_returns_correct_data_for_all_companies(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'searchresult': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        programme_search_result = Programme.objects.filter(name__contains="A").values()[:5]
        for programme in programme_search_result:
            self.assertContains(response, programme['name'])
        self.assertEqual(len(programme_search_result), 1)

    def test_search_programme_with_blank_query(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, {'searchresult': ''})
        self.assertEqual(response.status_code, 200)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("programmes/search/search_results_table.html", template_names)
        self.assertNotContains(response, 'No Search Results Found.')

    def test_post_search_company(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, follow=True, data={'searchresult': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes/programme_list_page.html')

    def test_post_search_company_filters_all_companies_successfully(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.post(self.url, follow=True, data={'searchresult': 'A'})
        companies = response.context['programmes']
        self.assertEqual(len(companies), 1)
