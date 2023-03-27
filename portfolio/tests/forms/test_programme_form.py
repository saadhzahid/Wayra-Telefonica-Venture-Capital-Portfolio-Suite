from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile

from django.forms import Textarea

from django.forms import model_to_dict, FileInput
from django.forms.fields import *
from django.test import TestCase

from portfolio.forms import CreateProgrammeForm, MultipleChoiceField, EditProgrammeForm
from portfolio.models import Company, Portfolio_Company, Individual, Programme


class CreateProgrammeFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json',
                'portfolio/tests/fixtures/default_individual.json',
                'portfolio/tests/fixtures/default_programme.json',

                ]

    def setUp(self) -> None:
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)

        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")
        self.form_input = {
            "name": "Accelerator Programme",
            "cohort": 2,  # avoid pk of default_programme
            "partners": [1],  # for pk of default_company
            "participants": [101],  # for pk of default_portfolio_company
            "coaches_mentors": [1],  # for pk of default_individual
            "cover": self.file_data
        }
        self.default_programme = Programme.objects.get(id=1)

    def test_valid_programme_create_form(self):
        form = CreateProgrammeForm(data=self.form_input, files=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateProgrammeForm()
        self.assertIn("name", form.fields)
        self.assertTrue(isinstance(form.fields['name'], CharField))
        self.assertIn("cohort", form.fields)
        self.assertTrue(isinstance(form.fields['cohort'], IntegerField))
        self.assertIn("partners", form.fields)
        self.assertTrue(isinstance(form.fields['partners'], MultipleChoiceField))
        self.assertIn("participants", form.fields)
        self.assertTrue(isinstance(form.fields['participants'], MultipleChoiceField))
        self.assertIn("coaches_mentors", form.fields)
        self.assertTrue(isinstance(form.fields['coaches_mentors'], MultipleChoiceField))
        self.assertIn("cover", form.fields)
        self.assertTrue(isinstance(form.fields['cover'], ImageField))
        self.assertTrue(isinstance(form.fields['cover'].widget, FileInput))

        self.assertIn("description", form.fields)
        self.assertTrue(isinstance(form.fields['description'], CharField))
        self.assertTrue(isinstance(form.fields['description'].widget, Textarea))

    def test_form_uses_model_validation(self):
        self.form_input['name'] = self.default_programme.name
        self.form_input['cohort'] = self.default_programme.cohort
        form = CreateProgrammeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_create_form_must_save_correctly(self):
        form = CreateProgrammeForm(data=self.form_input, files=self.form_input)
        before_count = Programme.objects.count()
        form.save()
        after_count = Programme.objects.count()
        self.assertEqual(after_count, before_count + 1)
        programme = Programme.objects.get(name=self.form_input['name'], cohort=self.form_input['cohort'])
        self.assertEqual(programme.name, self.form_input['name'])
        self.assertEqual(programme.cohort, self.form_input['cohort'])
        partners = set([Company.objects.get(id=ID) for ID in self.form_input['partners']])
        self.assertTrue(set(programme.partners.all()) == partners)

        participants = set([Company.objects.get(id=ID) for ID in self.form_input['participants']])
        self.assertTrue(set(programme.participants.all()) == participants)

        coaches_mentors = set([Individual.objects.get(id=ID) for ID in self.form_input['coaches_mentors']])
        self.assertTrue(set(programme.coaches_mentors.all()) == coaches_mentors)

        with open("portfolio/tests/forms/wayra_logo.png", "rb") as f:
            self.assertEqual(programme.cover.read(), f.read())


class EditProgrammeFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json',
                'portfolio/tests/fixtures/default_individual.json',
                'portfolio/tests/fixtures/default_programme.json',

                ]

    def setUp(self) -> None:
        image_file = BytesIO()
        image_file.write(open("portfolio/tests/forms/wayra_logo.png", 'rb').read())
        image_file.seek(0)

        self.file_data = SimpleUploadedFile("wayra_logo.png", image_file.read(), content_type="image/png")

        self.default_programme = Programme.objects.get(id=1)
        self.partner = Company.objects.first()
        self.participant = Portfolio_Company.objects.first().parent_company
        self.coach = Individual.objects.first()

        self.default_programme.cover = self.file_data
        self.default_programme.partners.add(self.partner)
        self.default_programme.participants.add(self.participant)
        self.default_programme.coaches_mentors.add(self.coach)

    def test_valid_programme_edit_form(self):
        form = EditProgrammeForm(instance=self.default_programme, data=model_to_dict(self.default_programme))
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = EditProgrammeForm(instance=self.default_programme, data=model_to_dict(self.default_programme))
        self.assertIn("name", form.fields)
        self.assertTrue(isinstance(form.fields['name'], CharField))
        self.assertIn("cohort", form.fields)
        self.assertTrue(isinstance(form.fields['cohort'], IntegerField))
        self.assertIn("partners", form.fields)
        self.assertTrue(isinstance(form.fields['partners'], MultipleChoiceField))
        self.assertIn("participants", form.fields)
        self.assertTrue(isinstance(form.fields['participants'], MultipleChoiceField))
        self.assertIn("coaches_mentors", form.fields)
        self.assertTrue(isinstance(form.fields['coaches_mentors'], MultipleChoiceField))
        self.assertIn("cover", form.fields)
        self.assertTrue(isinstance(form.fields['cover'], ImageField))
        self.assertTrue(isinstance(form.fields['cover'].widget, FileInput))

        self.assertIn("description", form.fields)
        self.assertTrue(isinstance(form.fields['description'], CharField))
        self.assertTrue(isinstance(form.fields['description'].widget, Textarea))

    def test_form_uses_model_validation(self):
        self.default_programme.name = "A" * 256
        form = EditProgrammeForm(instance=self.default_programme, data=model_to_dict(self.default_programme))
        self.assertFalse(form.is_valid())

    def test_edit_form_must_save_correctly(self):
        """TODO:Still missing cover image test but functioning currently"""
        original = self.default_programme
        original_data = model_to_dict(original)
        #
        # image_file = BytesIO()
        # image_file.write(open("portfolio/tests/forms/original_image.jpeg", 'rb').read())
        # image_file.seek(0)
        # file_data = SimpleUploadedFile("original_image.png", image_file.read(), content_type="image/png")
        #
        # original_data["cover"] = file_data

        form = EditProgrammeForm(instance=self.default_programme, data=original_data)

        before_count = Programme.objects.count()
        form.save()
        after_count = Programme.objects.count()
        self.assertEqual(after_count, before_count)
        programme = Programme.objects.get(name=original.name, cohort=original.cohort)
        self.assertEqual(programme.name, original.name)
        self.assertEqual(programme.cohort, original.cohort)
        partners = set([partner for partner in original.partners.all()])
        self.assertTrue(set(programme.partners.all()) == partners)

        participants = set([participant for participant in original.participants.all()])
        self.assertTrue(set(programme.participants.all()) == participants)

        coaches_mentors = set([coach_mentor for coach_mentor in original.coaches_mentors.all()])
        self.assertTrue(set(programme.coaches_mentors.all()) == coaches_mentors)

        # self.assertEqual(programme.cover.read(), file_data.read())
