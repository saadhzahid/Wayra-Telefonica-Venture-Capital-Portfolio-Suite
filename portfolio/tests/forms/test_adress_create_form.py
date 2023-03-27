"""Unit tests of the sign up form."""
from django.test import TestCase
from django_countries.fields import Country, LazyTypedChoiceField
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.forms import AddressCreateForm
from portfolio.models import Individual, ResidentialAddress


class CreateFormTestCase(TestCase):

    # Set up an examplery input to use for the tests
    def setUp(self):
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

        self.form_input = {
            "address_line1": "testAdress1",
            "address_line2": "testAdress2",
            "postal_code": "testCode",
            "city": "testCity",
            "state": "testState",
            "country": Country("AD"),
        }

    # Test if the form accepts valid input
    def test_valid_adress_create_form(self):
        form = AddressCreateForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = AddressCreateForm()
        self.assertIn("address_line1", form.fields)
        self.assertIn("address_line2", form.fields)
        self.assertIn("postal_code", form.fields)
        self.assertIn("city", form.fields)
        self.assertIn("state", form.fields)
        self.assertIn('country', form.fields)
        self.assertTrue(isinstance(form.fields['country'], LazyTypedChoiceField))

    # Test the form using model validation
    def test_form_uses_model_validation(self):
        self.form_input['country'] = Country('false')
        form = AddressCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test if the form saves correctly
    def test_form_must_save_correctly(self):
        form = AddressCreateForm(data=self.form_input)
        before_count = ResidentialAddress.objects.count()
        new_address = form.save(commit=False)
        new_address.individual = self.individual
        new_address.save()
        after_count = ResidentialAddress.objects.count()
        self.assertEqual(after_count, before_count + 1)
        adress = ResidentialAddress.objects.get(address_line1='testAdress1')
        self.assertEqual(adress.address_line1, "testAdress1")
        self.assertEqual(adress.address_line2, "testAdress2")
        self.assertEqual(adress.postal_code, "testCode")
        self.assertEqual(adress.city, "testCity")
        self.assertEqual(adress.state, "testState")
        self.assertEqual(adress.country, Country("AD"))
        self.assertEqual(adress.individual, self.individual)
