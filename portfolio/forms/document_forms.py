from django import forms
from django.utils.translation import gettext_lazy as _

from portfolio.models import Document


class DocumentUploadForm(forms.ModelForm):
    """A form for storing a document."""

    class Meta:
        model = Document
        fields = ["file", "is_private"]
        exclude = ["file_name", "file_type", "file_size", "url", "company", "individual", "programme", "created_at",
                   "updated_at"]
        labels = {
            "file": _("Select a file to upload:"),
            "is_private": _("Staff only:")
        }

    def __init__(self, *args, **kwargs):
        super(DocumentUploadForm, self).__init__(*args, **kwargs)
        self.fields["file"].required = True

    def save(self, commit=True):
        if commit:
            super().save()
        else:
            document = super().save(commit=False)
            document.file_name = self.cleaned_data["file"].name
            document.file_type = self.cleaned_data["file"].name.split(".")[-1]
            document.file_size = self.cleaned_data["file"].size
            document.is_public = self.cleaned_data["is_private"]

            return document


class URLUploadForm(forms.ModelForm):
    """A form for storing an URL."""

    class Meta:
        model = Document
        fields = ["file_name", "url", "is_private"]
        exclude = ["file_type", "file_size", "file", "company", "individual", "programme", "created_at", "updated_at"]
        labels = {
            "file_name": _("File name:"),
            "url": _("URL:"),
            "is_private": _("Staff only:")
        }

    def __init__(self, *args, **kwargs):
        super(URLUploadForm, self).__init__(*args, **kwargs)
        self.fields["url"].required = True

    def save(self, commit=True):
        document = super().save(commit=False)
        document.file_name = self.cleaned_data["file_name"]
        document.file_type = "URL"
        document.is_public = self.cleaned_data["is_private"]

        if commit:
            document.save()

        return document
