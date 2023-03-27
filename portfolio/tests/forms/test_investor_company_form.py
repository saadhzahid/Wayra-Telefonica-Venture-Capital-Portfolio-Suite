from django.test import TestCase

from portfolio.models import Company, InvestorCompany


class InvestorCompanyCreateForm(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'company': self.defaultCompany,
            'angelListLink': 'https://www.Angelist.com',
            'crunchbaseLink': 'https://www.crunchbase.com',
            'linkedInLink': 'https://www.linked-in.com',
            'classification': 'VC'
        }

    def test_valid_programme_create_form(self):
        pass

    def test_invalid_programme_create_form(self):
        pass

    def test_form_has_necessary_fields(self):
        pass

    def test_form_uses_model_validation(self):
        pass

    def test_form_must_save_correctly(self):
        pass


class InvestorCompanyEditForm(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
        self.form_input = {
            'angelListLink': 'https://www.Angelist.com',
            'crunchbaseLink': 'https://www.crunchbase.com',
            'linkedInLink': 'https://www.linked-in.com',
            'classification': 'VC'
        }

    def test_valid_programme_create_form(self):
        pass

    def test_invalid_programme_create_form(self):
        pass

    def test_form_has_necessary_fields(self):
        pass

    def test_form_uses_model_validation(self):
        pass

    def test_form_must_save_correctly(self):
        pass
