from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from portfolio.forms import UserCreationForm, CreateGroupForm, EditGroupForm, EditUserForm
from portfolio.models import User
from portfolio.views.mixins import FindObjectMixin
from vcpms import settings


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'permissions/user_list.html'
    http_method_names = ['get']
    context_object_name = 'users'
    paginate_by = settings.ADMINS_USERS_PER_PAGE

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('id')


class UserSignUpFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'permissions/user_create.html'
    http_method_names = ['get', 'post']
    form_class = UserCreationForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_user_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'permissions/user_delete.html'
    http_method_names = ['get', 'post']
    model = User
    pk_url_kwarg = 'id'
    redirect_when_no_object_found_url = 'permission_user_list'

    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
            if user.is_staff:
                return redirect('permission_user_list')
            return super().dispatch(request, id, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('permission_user_list')

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = self.get_object().id
        return context

    def get_success_url(self):
        return reverse('permission_user_list')


class UserEditFormView(LoginRequiredMixin, UserPassesTestMixin, FindObjectMixin, UpdateView):
    template_name = 'permissions/user_edit.html'
    model = User
    pk_url_kwarg = 'id'
    redirect_when_no_object_found_url = 'permission_user_list'
    form_class = EditUserForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def dispatch(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
            if user.is_staff:
                return redirect('permission_user_list')
            return super().dispatch(request, id, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('permission_user_list')

    def get_success_url(self):
        return reverse('permission_user_list')


class UserResetPasswordView(LoginRequiredMixin, UserPassesTestMixin, FindObjectMixin, UpdateView):
    http_method_names = ['get', 'post']
    model = User
    pk_url_kwarg = 'id'
    redirect_when_no_object_found_url = 'permission_user_list'

    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
            if user.is_staff:
                return redirect('permission_user_list')
            user.set_password("Password123")
            user.save()
            return redirect('permission_user_list')
        except ObjectDoesNotExist:
            return redirect('permission_user_list')

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_user_list')


class GroupCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'permissions/group_create.html'
    http_method_names = ['get', 'post']
    form_class = CreateGroupForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_group_list')


class GroupEditView(LoginRequiredMixin, UserPassesTestMixin, FindObjectMixin, UpdateView):
    template_name = 'permissions/group_create.html'
    http_method_names = ['get', 'post']
    model = Group
    form_class = EditGroupForm
    pk_url_kwarg = 'id'
    redirect_when_no_object_found_url = 'permission_group_list'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_initial(self):
        initial = super().get_initial()
        group_instance = self.get_object()
        codenames = list(group_instance.permissions.values_list('codename', flat=True))
        initial['permissions'] = codenames
        return initial

    def get_success_url(self):
        return reverse('permission_group_list')


class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'permissions/group_list_page.html'
    http_method_names = ['get']
    model = Group
    context_object_name = 'groups'
    paginate_by = settings.ADMINS_USERS_PER_PAGE

    def get_queryset(self):
        return Group.objects.all().order_by('id')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, FindObjectMixin, DeleteView):
    template_name = 'permissions/group_delete_page.html'
    http_method_names = ['get', 'post']
    model = Group
    pk_url_kwarg = 'id'
    redirect_when_no_object_found_url = 'permission_group_list'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_group_list')
