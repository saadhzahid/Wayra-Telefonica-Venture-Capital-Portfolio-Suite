import mimetypes
import os
import shutil
import time
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import DocumentUploadForm
from portfolio.models import Company, Document, User
from portfolio.tests.helpers import reverse_with_next
from vcpms.settings import MEDIA_ROOT


class DocumentViewsTestCase(TestCase):
    """Tests for the URLUploadForm."""

    fixtures = ["portfolio/tests/fixtures/default_company.json",
                'portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json'
                ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.defaultCompany = Company.objects.get(id=1)
        self.url = reverse('company_document_upload', kwargs={'company_id': self.defaultCompany.id})
        self.url_form_data = {
            "upload_url": 'True',
            "file_name": "test_file.txt",
            "url": "https://www.wayra.uk",
            "is_private": True
        }
        file = BytesIO()
        file.write(open("portfolio/tests/forms/TestingExcel.xlsx", 'rb').read())
        file.seek(0)

        self.defaultCompany = Company.objects.get(id=1)
        self.file_data = SimpleUploadedFile("TestingExcel.xlsx", file.read(), content_type=mimetypes.guess_type(
            "portfolio/tests/forms/TestingExcel.xlsx")[0])
        self.document_form_input = {
            "upload_file": 'True',
            "file": self.file_data,
            "is_private": True
        }
        directory = os.path.join(MEDIA_ROOT, f'documents/{self.defaultCompany.name}')
        directory = os.path.normpath(directory)
        for i in range(10):
            # Multi-threaded test causes locking
            try:
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
            except IOError:
                time.sleep(.1)

    def test_document_upload_url(self):
        self.assertEqual(self.url, f'/portfolio_company/{self.defaultCompany.id}/upload_document/')

    def test_get_document_upload_view(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document/document_upload.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, DocumentUploadForm))
        self.assertFalse(form.is_bound)

    def test_document_upload_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_upload_url(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Document.objects.count()
        response = self.client.post(self.url, self.url_form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Document.objects.count()
        self.assertEqual(before_count, after_count - 1)

    def test_post_upload_document(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Document.objects.count()
        response = self.client.post(self.url, self.document_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Document.objects.count()
        self.assertEqual(before_count, after_count - 1)

    def test_download_document_url(self):
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('download_document', kwargs={'file_id': 1})
        self.assertEqual(self.url, f'/download_document/1')

    def test_download_document(self):
        self.client.login(email=self.user.email, password="Password123")
        self.client.post(self.url, self.document_form_input, follow=True)
        document = Document.objects.get(file_id=1)
        self.url = reverse('download_document', kwargs={'file_id': document.file_id})
        response = self.client.get(self.url)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=TestingExcel.xlsx"
        )

    def test_document_download_redirects_when_not_logged_in(self):
        self.url = reverse('download_document', kwargs={'file_id': 1})
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_delete_document_url(self):
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('delete_document', kwargs={'file_id': 1})
        self.assertEqual(self.url, f'/delete_document/1')

    def test_delete_document(self):
        self.client.login(email=self.user.email, password="Password123")
        self.client.post(self.url, self.document_form_input, follow=True)
        before_count = Document.objects.count()
        self.url = reverse('delete_document', kwargs={'file_id': 1})
        self.client.get(self.url)
        after_count = Document.objects.count()
        self.assertEqual(before_count, after_count + 1)

    def test_document_delete_redirects_when_not_logged_in(self):
        self.url = reverse('delete_document', kwargs={'file_id': 1})
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_document_change_permissions_url(self):
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('change_permissions', kwargs={'file_id': 1})
        self.assertEqual(self.url, f'/document_permissions/1')

    def test_document_change_permissions(self):
        self.client.login(email=self.user.email, password="Password123")
        self.client.post(self.url, self.document_form_input, follow=True)
        before_change_permissions = Document.objects.get(file_id=1).is_private
        self.url = reverse('change_permissions', kwargs={'file_id': 1})
        self.client.get(self.url)
        after_change_permissions = Document.objects.get(file_id=1).is_private
        self.assertNotEqual(before_change_permissions, after_change_permissions)

    def test_document_change_permissions_redirects_when_not_logged_in(self):
        self.url = reverse('change_permissions', kwargs={'file_id': 1})
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_open_url(self):
        self.client.login(email=self.user.email, password="Password123")
        self.client.post(self.url, self.url_form_data, follow=True)
        self.url = reverse('open_url', kwargs={'file_id': 1})
        response = self.client.get(self.url)
        redirect_url = "https://www.wayra.uk"
        self.assertEqual(response['Location'], redirect_url)

    def test_document_open_url_redirects_when_not_logged_in(self):
        self.url = reverse('open_url', kwargs={'file_id': 1})
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
