from django.conf import settings as django_settings
from django.urls import reverse


class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()


def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


# Helper functions
def set_session_cookies(client, session):
    # Set the cookie to represent the session
    session_cookie = django_settings.SESSION_COOKIE_NAME
    client.cookies[session_cookie] = session.session_key
    cookie_data = {
        'max-age': None,
        'path': '/',
        'domain': django_settings.SESSION_COOKIE_DOMAIN,
        'secure': django_settings.SESSION_COOKIE_SECURE or None,
        'expires': None}
    client.cookies[session_cookie].update(cookie_data)


def set_session_variables(client):
    session = client.session
    session['company_filter'] = 1
    session['company_layout'] = 1
    session['individual_filter'] = 1
    session['individual_layout'] = 1
    session['archived_company_filter'] = 1
    session['archived_individual_filter'] = 1
    session.save()
    set_session_cookies(client, session)


def set_session_company_filter_variable(client, filter_number):
    session = client.session
    session['company_filter'] = filter_number
    session.save()
    set_session_cookies(client, session)


def set_session_individual_filter_variable(client, filter_number):
    session = client.session
    session['individual_filter'] = filter_number
    session.save()
    set_session_cookies(client, session)


def set_session_archived_individual_filter_variable(client, filter_number):
    session = client.session
    session['archived_individual_filter'] = filter_number
    session.save()
    set_session_cookies(client, session)


def set_session_archived_company_filter_variable(client, filter_number):
    session = client.session
    session['archived_company_filter'] = filter_number
    session.save()
    set_session_cookies(client, session)
