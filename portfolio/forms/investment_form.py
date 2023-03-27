"""Forms to input investment between an investor and a startup"""
from django import forms
from django.db.models import Exists, OuterRef

from portfolio.models import Portfolio_Company
from portfolio.models.company_model import Company
from portfolio.models.individual_model import Individual
from portfolio.models.investment_model import Investment, ContractRight
from portfolio.models.investor_model import Investor


class InvestorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.company is not None:
            return obj.company.name
        else:
            return obj.individual.name


class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class PortfolioCompanyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.parent_company.name


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["investor", "startup", "typeOfFoundingRounds", "investmentAmount", "dateInvested"]
        widgets = {
            'dateInvested': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    investor = InvestorChoiceField(
        queryset=Investor.objects.all(),
        widget=forms.Select()
    )

    startup = PortfolioCompanyChoiceField(
        queryset=Portfolio_Company.objects.all(),
        widget=forms.Select()
    )


class ContractRightForm(forms.ModelForm):
    class Meta:
        model = ContractRight
        fields = ["right", "details"]

    right_investment = None

    def saveInvestment(self, invest):
        self.right_investment = invest

    def save(self):
        super().save(commit=False)
        ContractRight.objects.create(
            investment=self.right_investment,
            right=self.cleaned_data.get("right"),
            details=self.cleaned_data.get("details")
        )


# Form for setting company or individual as investor
class InvestorCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ["company", "classification"]

    company = ModelChoiceField(
        queryset=Company.objects.filter(~Exists(Investor.objects.filter(company=OuterRef('id'))),
                                        ~Exists(Portfolio_Company.objects.filter(parent_company=OuterRef('id')))),
        widget=forms.Select()
    )


class InvestorIndividualCreateForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ["individual", "classification"]

    individual = ModelChoiceField(
        queryset=Individual.objects.filter(~Exists(Investor.objects.filter(individual=OuterRef('id')))),
        widget=forms.Select()
    )


class InvestorEditForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ["classification"]
