from django import forms
from django.contrib.auth.models import Group, Permission
from django_select2.forms import Select2MultipleWidget

MODEL_NAMES = ['company', 'individual']
CHOICES = [
    ("add_user", "Create user"),
    ("change_user", "Edit user"),
    ("delete_user", "Delete user"),
    ("view_user", "View user"),

    ("add_company", "Create company"),
    ("change_company", "Edit company"),
    ("delete_company", "Delete company"),
    ("view_company", "View company"),

    ("add_individual", "Create individual"),
    ("change_individual", "Edit individual"),
    ("delete_individual", "Delete individual"),
    ("view_individual", "View individual"),

    ("add_residentialaddress", "Create residential address"),
    ("change_residentialaddress", "Edit residential address"),
    ("delete_residentialaddress", "Delete residential address"),
    ("view_residentialaddress", "View residential address")
]


#
# class GroupWidget(ModelSelect2MultipleWidget):
#     search_fields = ['name__icontains']


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')

    name = forms.CharField(label='Group Name', max_length=100)

    permissions = forms.MultipleChoiceField(
        label='Permissions',
        # queryset=Permission.objects.filter(content_type__model__in=MODEL_NAMES),
        choices=CHOICES,
        widget=Select2MultipleWidget(),
    )

    def clean(self):
        super().clean()
        if Group.objects.filter(name=self.cleaned_data.get("name")).exists():
            self.add_error("name", "Group already exists")

    def save(self):
        super().save(commit=False)
        new_group = Group.objects.create(
            name=self.cleaned_data.get("name"),
        )
        for permission_name in self.cleaned_data.get("permissions"):
            permission = Permission.objects.get(codename=permission_name)
            new_group.permissions.add(permission)
        new_group.save()


class EditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')

    name = forms.CharField(label='Group Name', max_length=100)

    permissions = forms.MultipleChoiceField(
        label='Permissions',
        # queryset=Permission.objects.filter(content_type__model__in=MODEL_NAMES),
        choices=CHOICES,
        widget=Select2MultipleWidget(),
    )

    def clean(self):
        super().clean()
        current_group = self.instance
        if Group.objects.filter(name=self.cleaned_data.get("name")).exists() and self.cleaned_data.get(
                "name") != current_group.name:
            self.add_error("name", "Group already exists")

    def save(self):
        super().save(commit=False)
        group = self.instance
        group.name = self.cleaned_data.get("name")
        group.permissions.clear()
        for permission_name in self.cleaned_data.get("permissions"):
            permission = Permission.objects.get(codename=permission_name)
            group.permissions.add(permission)
        group.save()

    # KEEP BELOW FOR NOW IN CASE CODES ABOVE DO NOT WORK
    # name = forms.CharField()

    # permissions = forms.MultipleChoiceField(label = "Permissions", choices = CHOICES, widget=forms.CheckboxSelectMultiple())

    # def save(self):
    #     new_group, created = Group.objects.get_or_create(name=self.cleaned_data.get("name"))
