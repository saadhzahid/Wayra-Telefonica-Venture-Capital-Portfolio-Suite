""" Unit test for permission views"""
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import UserCreationForm, CreateGroupForm, EditGroupForm, EditUserForm
from portfolio.models import User, Company
from portfolio.tests.helpers import reverse_with_next
from portfolio.tests.helpers import set_session_variables
from vcpms import settings


class UserListViewTestCase(TestCase):
    """ Unit test for user list """
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('permission_user_list')
        self.user = User.objects.get(email='petra.pickles@example.org')
        set_session_variables(self.client)

    def test_user_list_url(self):
        self.assertEqual(self.url, '/permissions/users/')

    def test_get_user_list(self):
        self.client.login(username=self.user.email, password="Password123")
        self._create_test_users(15 - 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15 - 1):
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'+447312345678')
            self.assertIsNotNone(User.objects.get(email=f'user{user_id}@test.org'))

    def test_user_list_pagination(self):
        self.client.login(email=self.user.email, password="Password123")
        # minus John doe
        self._create_test_users(settings.ADMINS_USERS_PER_PAGE * 2 + 1 - 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')

        page_obj = response.context['page_obj']
        page_one_url = reverse('permission_user_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        self.assertEqual(len(response.context['users']), settings.ADMINS_USERS_PER_PAGE)
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('permission_user_list') + '?page=2'
        response = self.client.get(page_two_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        self.assertEqual(len(response.context['users']), settings.ADMINS_USERS_PER_PAGE)
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('permission_user_list') + '?page=3'
        response = self.client.get(page_three_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        self.assertEqual(len(response.context['users']), 1)
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    def test_non_admin_cannot_access_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(email=f'user{user_id}@test.org',
                                     password='Password123',
                                     first_name=f'First{user_id}',
                                     last_name=f'Last{user_id}',
                                     phone=f'+447312345678'
                                     )


class UserSignUpFormViewTestCase(TestCase):
    """ Unit test for UserSignUpFormView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.url = reverse('permission_create_user')
        self.grp = Group.objects.create(name="DefaultGrp")
        content_type = ContentType.objects.get_for_model(Company)
        for permission in list(Permission.objects.filter(content_type=content_type)):
            self.grp.permissions.add(permission)
        self.form_input = {"email": "jane.doe@example.org",
                           "first_name": "Jane",
                           "last_name": "Doe",
                           "phone": "+447312345678",
                           "password": 'Password123',
                           "is_active": True,
                           "group": [1],
                           }
        set_session_variables(self.client)

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/permissions/create_user/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_sign_up_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_user_sign_up(self):
        before_count = User.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('permission_user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        user = User.objects.get(email='jane.doe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_equal = check_password('Password123', user.password)
        self.assertTrue(is_password_equal)
        self.assertEqual(user.phone, "+447312345678")
        self.assertEqual(user.is_active, True)
        self.assertEqual(list(user.groups.all()), [self.grp])

    def test_unsuccessful_user_sign_up(self):
        before_count = User.objects.count()
        self.form_input["email"] = "INVALID_EMAIL"
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserCreationForm))
        self.assertTrue(form.is_bound)


class GroupCreationViewTestCase(TestCase):
    """ Unit test for GroupCreationView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.url = reverse('permission_create_group')
        self.form_input = {
            "name": "UserGrp",
            "permissions": ['add_user', 'change_user', 'view_user', 'delete_user']
        }
        set_session_variables(self.client)

    def test_create_group_url(self):
        self.assertEqual(self.url, '/permissions/create_group/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_sign_up_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_group_create(self):
        before_count = Group.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('permission_group_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        group = Group.objects.get(name="UserGrp")
        self.assertEqual(group.name, 'UserGrp')

        content_type = ContentType.objects.get_for_model(User)
        self.assertEqual(set(group.permissions.all()), set(Permission.objects.filter(content_type=content_type)))

    def test_unsuccessful_group_create(self):
        before_count = Group.objects.count()
        self.form_input["permissions"] = []
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateGroupForm))
        self.assertTrue(form.is_bound)


class UserDeleteViewTestCase(TestCase):
    """ Unit test for UserDeleteView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.test_user = User.objects.get(email="john.doe@example.org")
        self.url = reverse('permission_delete_user', kwargs={'id': self.test_user.id})
        set_session_variables(self.client)

    def test_delete_user_url(self):
        self.assertEqual(self.url, f'/permissions/{self.test_user.id}/delete_user/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_delete_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_user_delete(self):
        before_count = User.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count - 1)
        response_url = reverse('permission_user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')

    def test_cannot_get_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_delete_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_delete_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_delete_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_delete_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class GroupListViewTestCase(TestCase):
    """ Unit test for group list """
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.url = reverse('permission_group_list')
        self.user = User.objects.get(email='petra.pickles@example.org')
        set_session_variables(self.client)

    def test_group_list_url(self):
        self.assertEqual(self.url, '/permissions/group_list/')

    def test_get_group_list(self):
        self.client.login(username=self.user.email, password="Password123")
        self._create_test_group(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        self.assertEqual(len(response.context['groups']), 15)
        for group_id in range(15):
            self.assertContains(response, f'Group{group_id}')
            self.assertContains(response, f'Can add user')
            self.assertIsNotNone(Group.objects.get(name=f'Group{group_id}'))

    def _create_test_group(self, group_count):
        for group_id in range(group_count):
            group = Group.objects.create(name=f'Group{group_id}')
            group.permissions.add(Permission.objects.get(codename='add_user'))

    def test_non_admin_cannot_access_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_group_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_group_list_pagination(self):
        self.client.login(email=self.user.email, password="Password123")
        self._create_test_group(settings.ADMINS_USERS_PER_PAGE * 2 + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')

        page_obj = response.context['page_obj']
        page_one_url = reverse('permission_group_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        self.assertEqual(len(response.context['groups']), settings.ADMINS_USERS_PER_PAGE)
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('permission_group_list') + '?page=2'
        response = self.client.get(page_two_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        self.assertEqual(len(response.context['groups']), settings.ADMINS_USERS_PER_PAGE)
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('permission_group_list') + '?page=3'
        response = self.client.get(page_three_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        self.assertEqual(len(response.context['groups']), 1)
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())


class GroupEditViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.test_group = Group.objects.create(name="OriginalGroup")
        self.test_group.permissions.add(Permission.objects.get(codename='add_user'))
        self.form_input = {
            "name": "UserGrp",
            "permissions": ['add_user', 'change_user', 'view_user', 'delete_user']
        }
        self.url = reverse('permission_edit_group', kwargs={'id': self.test_group.id})
        set_session_variables(self.client)

    def test_group_edit_url(self):
        self.assertEqual(self.url, f'/permissions/{self.test_group.id}/edit_group/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_delete_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_invalid_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_edit_group', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_invalid_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_edit_group', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_admin_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_edit_group', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_admin_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_edit_group', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_group_edit(self):
        before_count = Group.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('permission_group_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')
        group = Group.objects.get(name="UserGrp")
        self.assertEqual(group.name, 'UserGrp')

        content_type = ContentType.objects.get_for_model(User)
        self.assertEqual(set(group.permissions.all()), set(Permission.objects.filter(content_type=content_type)))

    def test_unsuccessful_group_edit(self):
        before_count = Group.objects.count()
        self.form_input["permissions"] = []
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/group_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditGroupForm))
        self.assertTrue(form.is_bound)


class GroupDeleteViewTestCase(TestCase):
    """ Unit tests for GroupDeleteView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.test_group = Group.objects.create(name="OriginalGroup")
        self.test_group.permissions.add(Permission.objects.get(codename='add_user'))
        self.url = reverse('permission_delete_group', kwargs={'id': self.test_group.id})
        set_session_variables(self.client)

    def test_delete_user_url(self):
        self.assertEqual(self.url, f'/permissions/{self.test_group.id}/delete_group/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_delete_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_group_delete(self):
        before_count = Group.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count - 1)
        response_url = reverse('permission_group_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/group_list_page.html')

    def test_cannot_get_invalid_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_delete_group', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_invalid_id(self):
        redirect_url = reverse('permission_group_list')
        self.url = reverse('permission_delete_group', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class EditUserViewTestCase(TestCase):
    """ Unit tests for EditUserView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.test_group = Group.objects.create(name="OriginalGroup")
        self.test_group.permissions.add(Permission.objects.get(codename='add_user'))
        self.test_user = User.objects.get(email="john.doe@example.org")
        self.url = reverse('permission_edit_user', kwargs={'id': self.test_user.id})
        self.form_input = {"email": self.test_user.email,
                           "first_name": self.test_user.first_name,
                           "last_name": self.test_user.last_name,
                           "password": "Password123",
                           "phone": self.test_user.phone,
                           "is_active": self.test_user.is_active,
                           'group': [1]
                           }
        set_session_variables(self.client)

    def test_get_edit_user_url(self):
        self.assertEqual(self.url, f'/permissions/{self.test_user.id}/edit_user/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_edit_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_user_edit(self):
        before_count = User.objects.count()
        self.form_input['first_name'] = 'Jane'
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('permission_user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/user_list.html')
        user = User.objects.get(email=self.test_user.email)
        self.assertEqual(user.first_name, 'Jane')

    def test_unsuccessful_user_edit(self):
        before_count = User.objects.count()
        self.form_input['email'] = "INVALID_EMAIL"
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_edit.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditUserForm))
        self.assertTrue(form.is_bound)


class UserResetPasswordViewTestCase(TestCase):
    """ Unit tests for UserResetPasswordView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.test_user = User.objects.get(email="john.doe@example.org")
        self.url = reverse('permission_reset_password', kwargs={'id': self.test_user.id})
        set_session_variables(self.client)

    def test_get_edit_user_url(self):
        self.assertEqual(self.url, f'/permissions/{self.test_user.id}/reset_password/')

    def test_get_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_invalid_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 99999})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_get_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_post_admin_id(self):
        redirect_url = reverse('permission_user_list')
        self.url = reverse('permission_edit_user', kwargs={'id': 2})
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_password_reset(self):
        self.test_user.set_password('Aa12345678')
        self.test_user.save()
        is_password_equal = check_password('Aa12345678', self.test_user.password)
        self.assertTrue(is_password_equal)
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, follow=True)
        response_url = reverse('permission_user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        user = User.objects.get(email=self.test_user.email)
        is_new_password_equal = check_password('Password123', user.password)
        self.assertTrue(is_new_password_equal)
