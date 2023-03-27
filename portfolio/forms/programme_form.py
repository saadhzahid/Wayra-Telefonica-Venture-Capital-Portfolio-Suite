from django import forms
from django_select2 import forms as d2forms

from portfolio.models import Company, Individual, Programme


class MultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CompanySelectWidget(d2forms.ModelSelect2MultipleWidget):
    search_fields = ['name__icontains']


class IndividualSelectWidget(d2forms.ModelSelect2MultipleWidget):
    search_fields = ['name__icontains']


class CreateProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ["name", "cohort", "cover", "description"]
        widgets = {
            'cohort': forms.NumberInput(attrs={'min': 1}),
            'cover': forms.FileInput(),
            'description': forms.Textarea()
        }

    partners = MultipleChoiceField(
        queryset=Company.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        widget=CompanySelectWidget(
            attrs={'data-minimum-input-length': 3},
            options={'placeholder': 'Search for a company...',
                     'minimumInputLength': 3
                     })
    )

    participants = MultipleChoiceField(
        queryset=Company.objects.all(),
        widget=CompanySelectWidget(
            attrs={'data-minimum-input-length': 3},
            options={'placeholder': 'Search for a company...',
                     'minimumInputLength': 3
                     })
    )

    coaches_mentors = MultipleChoiceField(
        queryset=Individual.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        widget=IndividualSelectWidget(attrs={'data-minimum-input-length': 3},
                                      options={'placeholder': 'Search for an Individual...',
                                               'minimumInputLength': 3
                                               })

    )

    def clean(self):
        super().clean()
        programme_name = self.cleaned_data.get("name")
        programme_cohort = self.cleaned_data.get("cohort")
        if Programme.objects.filter(name=programme_name, cohort=programme_cohort).count() > 0:
            self.add_error("cohort", "Cohort for this programme already exists")

    def save(self):
        super().save(commit=False)
        new_programme = Programme.objects.create(
            name=self.cleaned_data.get("name"),
            cohort=self.cleaned_data.get("cohort"),
            cover=self.cleaned_data.get("cover"),
            description=self.cleaned_data.get("description")
        )
        for partner in self.cleaned_data.get("partners"):
            new_programme.partners.add(partner)
        for participant in self.cleaned_data.get("participants"):
            new_programme.participants.add(participant)
        for coach in self.cleaned_data.get("coaches_mentors"):
            new_programme.coaches_mentors.add(coach)
        new_programme.save()
    # SAVE THE BELOW FOR NOW IN CASE THIS DOESN'T WORK

    # #Populating partner choices
    # partners_list = Company.objects.all()
    # PARTNER_CHOICES = []
    # for partner in partners_list:
    #     PARTNER_CHOICES.append((partner, partner.name))
    # partners = forms.MultipleChoiceField(label="Partners", choices = PARTNER_CHOICES, required = True)

    # #Populating portfolio company choices
    # participant_list = Portfolio_Company.objects.all()
    # PARTICIPANT_CHOICES = []
    # for parti in participant_list:
    #     PARTICIPANT_CHOICES.append((parti, parti.name))
    # participants = forms.MultipleChoiceField(label="Participants", choices = PARTICIPANT_CHOICES, required = True)

    # #Populating coaches and mentors
    # coaches_list = Individual.objects.all()
    # COACHES_CHOICES = []
    # for coach in coaches_list:
    #     COACHES_CHOICES.append((coach, coach.name))
    # coaches_mentors = forms.MultipleChoiceField(label="Coaches and Mentors", choices = COACHES_CHOICES, required = True)


class EditProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ["name", "cohort", "cover", "description"]
        widgets = {
            'cohort': forms.NumberInput(attrs={'min': 1}),
            'cover': forms.FileInput(),
            'description': forms.Textarea()
        }

    partners = MultipleChoiceField(
        queryset=Company.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        widget=CompanySelectWidget(
            attrs={'data-minimum-input-length': 3},
            options={'placeholder': 'Search for a company...',
                     'minimumInputLength': 3
                     })
    )

    participants = MultipleChoiceField(
        queryset=Company.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        widget=CompanySelectWidget(
            attrs={'data-minimum-input-length': 3},
            options={'placeholder': 'Search for a company...',
                     'minimumInputLength': 3
                     })
    )

    coaches_mentors = MultipleChoiceField(
        queryset=Individual.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        widget=IndividualSelectWidget(attrs={'data-minimum-input-length': 3},
                                      options={'placeholder': 'Search for an Individual...',
                                               'minimumInputLength': 3
                                               })

    )

    def save(self):
        super().save(commit=False)
        programme = self.instance
        programme.name = self.cleaned_data.get("name")
        programme.cohort = self.cleaned_data.get("cohort")
        programme.description = self.cleaned_data.get("description")
        programme.partners.clear()
        programme.participants.clear()
        programme.coaches_mentors.clear()
        for partner in self.cleaned_data.get("partners"):
            programme.partners.add(partner)
        for participant in self.cleaned_data.get("participants"):
            programme.participants.add(participant)
        for coach in self.cleaned_data.get("coaches_mentors"):
            programme.coaches_mentors.add(coach)
        programme.cover = self.cleaned_data.get("cover")
        programme.save()
