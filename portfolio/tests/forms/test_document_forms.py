import mimetypes
import os
import shutil
import time
from io import BytesIO

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase

from portfolio.forms import URLUploadForm, DocumentUploadForm
from portfolio.models import Company, Document
from vcpms.settings import MEDIA_ROOT


class URLUploadFormTest(TestCase):
    """Tests for the URLUploadForm."""

    fixtures = ["portfolio/tests/fixtures/default_company.json"]

    def setUp(self):
        self.form_data = {
            "file_name": "test_file.txt",
            "url": "https://www.wayra.uk",
            "is_private": True
        }

    def test_form_is_valid(self):
        form = URLUploadForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        document = form.save(commit=False)
        document.company = Company.objects.get(id=1)
        document.individual = None
        document.programme = None
        document.save()
        self.assertEqual(document.file_name, self.form_data["file_name"])
        self.assertEqual(document.file_type, "URL")
        self.assertEqual(document.url, self.form_data["url"])
        self.assertTrue(document.is_private)

    def test_forms_save_without_assigning_company_raises_error(self):
        form = URLUploadForm(data=self.form_data)
        with self.assertRaises(IntegrityError):
            form.save()

    def test_form_is_invalid(self):
        form_data = {
            "file_name": None,
            "url": None,
            "is_private": True
        }
        form = URLUploadForm(data=form_data)
        self.assertFalse(form.is_valid())


class DocumentFormTestCase(TestCase):
    fixtures = ["portfolio/tests/fixtures/default_company.json"]

    def setUp(self) -> None:
        file = BytesIO()
        file.write(open("portfolio/tests/forms/TestingExcel.xlsx", 'rb').read())
        file.seek(0)

        self.defaultCompany = Company.objects.get(id=1)
        self.file_data = SimpleUploadedFile("TestingExcel.xlsx", file.read(), content_type=mimetypes.guess_type(
            "portfolio/tests/forms/TestingExcel.xlsx")[0])
        self.form_input = {"file": self.file_data,
                           "is_private": True}

        directory = os.path.join(MEDIA_ROOT, f'documents/{self.defaultCompany.name}')
        directory = os.path.normpath(directory)
        for i in range(10):
            # Multi-threaded test causes locking
            try:
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
            except IOError:
                time.sleep(.1)

    def test_valid_document_create_form(self):
        form = DocumentUploadForm(data=self.form_input, files=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = DocumentUploadForm()
        self.assertIn("file", form.fields)
        self.assertTrue(isinstance(form.fields['file'], forms.FileField))
        self.assertTrue(isinstance(form.fields['file'].widget, forms.FileInput))

        self.assertIn("is_private", form.fields)
        self.assertTrue(isinstance(form.fields['is_private'], forms.BooleanField))

    def test_forms_uses_model_validation(self):
        self.form_input['file'] = None
        form = DocumentUploadForm(data=self.form_input, files=self.form_input)
        self.assertFalse(form.is_valid())

    def test_forms_save_without_assigning_company_raises_error(self):
        form = DocumentUploadForm(data=self.form_input, files=self.form_input)
        with self.assertRaises(ValueError):
            form.save(commit=True)

    def test_form_must_save_correctly(self):
        form = DocumentUploadForm(data=self.form_input, files=self.form_input)
        before_count = Document.objects.count()
        document = form.save(commit=False)
        document.company = self.defaultCompany
        document.individual = None
        document.programme = None
        form.save()
        after_count = Document.objects.count()
        self.assertEqual(after_count, before_count + 1)
        document = Document.objects.get()

        directory = os.path.join(MEDIA_ROOT, f'documents/{self.defaultCompany.name}')
        # print(directory)
        self.assertTrue(os.path.isdir(directory))
        self.assertTrue(os.path.isfile(os.path.join(directory, self.file_data.name)))

        with open("portfolio/tests/forms/TestingExcel.xlsx", "rb") as f:
            self.assertEqual(document.file.read(), f.read())
            self.assertEqual(document.file_name, self.file_data.name)
            self.assertEqual(document.file_type, f.name.split(".")[-1])
            self.assertEqual(document.file_size, self.file_data.size)

        self.assertEqual(document.is_private, self.form_input['is_private'])
