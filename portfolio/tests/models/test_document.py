import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from portfolio.models import Company
from portfolio.models import Document


class DocumentModelTestCase(TestCase):
    """Unit tests for the Document model."""

    fixtures = ["portfolio/tests/fixtures/default_company.json"]

    def setUp(self):
        self.document = Document.objects.create(
            file_name="test.document",
            file_type="document",
            company=Company.objects.get(id=1),
            individual=None,
            programme=None,
            file=SimpleUploadedFile("test.document", b"file contents")
        )

    def test_valid_document(self):
        self._assert_document_is_valid()

    def test_both_url_and_file_cannot_be_null(self):
        self.document.company = None
        self._assert_document_is_invalid()

    def test_auto_delete_file_on_delete(self):
        # Ensure the file exists.
        file_path = self.document.file.path
        self.assertTrue(os.path.isfile(file_path))

        # Test if the file is deleted when its record in the database is deleted.
        self.document.delete()
        self.assertFalse(os.path.isfile(file_path))

    def test_auto_delete_file_on_change(self):
        second_document = self._create_second_document()

        # Ensure the old file is deleted when a new file is uploaded.
        old_file_path = self.document.file.path
        new_file_path = second_document.file.path
        self.assertTrue(os.path.isfile(old_file_path))
        self.assertTrue(os.path.isfile(new_file_path))

        # Update the first document with the second document's file.
        self.document.file = second_document.file
        self.document.save()
        self.assertFalse(os.path.isfile(old_file_path))
        self.assertTrue(os.path.isfile(new_file_path))

    """Helper functions"""

    # Assert a document is valid
    def _assert_document_is_valid(self):
        try:
            self.document.full_clean()
        except ValidationError:
            self.fail("Test document is not valid.")

    # Assert a document is invalid
    def _assert_document_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.document.full_clean()

    # Create a second document
    def _create_second_document(self):
        document = Document.objects.create(
            file_name="test2.document",
            file_type="document",
            company=Company.objects.get(id=1),
            file=SimpleUploadedFile("test2.document", b"file contents")
        )
        return document
