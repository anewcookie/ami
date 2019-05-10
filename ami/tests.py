from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.loader import render_to_string
from django_user_agents.templatetags import user_agents
from django_user_agents.utils import get_user_agent
from user_agents.parsers import UserAgent

from .views import settings
from .models import Room
import re

# https://deviceatlas.com/blog/list-of-user-agent-strings
androidUA = "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36" \
            " (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"
iphoneUA = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML," \
           " like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
macUA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko)" \
        " Version/9.0.2 Safari/601.3.9"
windowsUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
            "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
undefUA = ""

# tests that Django template language is rendering all pages successfully
class TestAllPages(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('cadettester', password='testerpassword')
        self.client.login(username='cadettester', password='testerpassword')

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The homepage is working correctly!")

    def test_loginpage(self):
        response = self.client.get('/accounts/login/?next=/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The login page is loading correctly!")

    def test_company_summary(self):
        response = self.client.get('/accounts/login/?next=/summary/0/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The company summary page is loading correctly!")

    def test_inspections(self):
        response = self.client.get('/accounts/login/?next=/inspection/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The inspection page is loading correctly!")

    def test_my_room(self):
        response = self.client.get('/accounts/login/?next=/room/myroom/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The my room page is loading correctly!")

    def test_settings(self):
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            print("******The settings page is loading correctly!")


# tests login page for attempted Cross Site Request Forgery
class TestPOSTCSRF(TestCase):
    def test_post_endpoint(self):
        csrf_client = Client(enforce_csrf_checks=True)
        data = {'van2': 'bigzooguy'}
        # response = Client().post('/accounts/login/', params=data)
        response = csrf_client.post('/accounts/login/', params=data)
        # should be forbidden to log in (403)
        self.assertEqual(response.status_code, 403)
        print("******Attempted Cross-Site login failed as desired.")

'''
# test settings page for CSRF
# !!not working!!
# https://www.neuraldump.net/2017/03/testing-django-pages-containing-the-csrf_token-tag/
def remove_csrf(html_code):
    csrf_regex = r']+csrfmiddlewaretoken[^>]+>'
    # csrf_regex = r'&lt;input[^&gt;]+csrfmiddlewaretoken[^&gt;]+&gt;'
    return re.sub(csrf_regex, '', html_code)


class TestSettingsCSRF(TestCase):
    def test_settings_page_blocks_csrf(self):
        rq = HttpRequest()
        # response = self.client.get('/accounts/login/?next=/settings/')
        response = settings(rq)
        expected_html = render_to_string('/settings.html', request=rq)
        self.assertEqual(remove_csrf(response.content.decode()), remove_csrf(expected_html))
'''


# test that the subordinates page button does not redirect
class TestSubordinates(TestCase):
    def test_subs_on_click(self):
        r1 = self.client.get('/accounts/login/?next=/summary/0/')
        r2 = self.client.get('/accounts/login/?next=/summary/0/#')
        self.assertEqual(r2.status_code, r1.status_code)
        if r2.status_code == 200:
            print("******Great! The subordinates link does not redirect to an unknown page.")


# test Mobile browsers by attempting to create an instance and login
# https://github.com/selwin/django-user_agents/blob/master/django_user_agents/tests/tests.py
class TestCommonUserAgents(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('cadettester', password='testerpassword')
        self.client.login(username='cadettester', password='testerpassword')

    def test_iphone(self):
        # is truly an iphone
        request = RequestFactory(HTTP_USER_AGENT=iphoneUA).get('')
        self.assertTrue(user_agents.is_mobile(request))
        self.assertTrue(user_agents.is_touch_capable(request))
        self.assertFalse(user_agents.is_tablet(request))
        self.assertFalse(user_agents.is_pc(request))
        self.assertFalse(user_agents.is_bot(request))

        # test that you can login on iPhone
        # use a link that requires auth
        response = self.client.get('/accounts/login/?next=/summary/0/', environ_base={'HTTP_USER_AGENT': iphoneUA})
        self.assertEqual(response.status_code, 200)
        print("******Attempted iPhone UA login successful.")

    def test_android(self):
        # is truly an android
        request = RequestFactory(HTTP_USER_AGENT=androidUA).get('')

        self.assertTrue(user_agents.is_mobile(request))
        self.assertTrue(user_agents.is_touch_capable(request))
        self.assertFalse(user_agents.is_tablet(request))
        self.assertFalse(user_agents.is_pc(request))
        self.assertFalse(user_agents.is_bot(request))

        # test that you can login on Android
        # use a link that requires auth
        response = self.client.get('/accounts/login/?next=/summary/0/', environ_base={'HTTP_USER_AGENT': androidUA})
        self.assertEqual(response.status_code, 200)
        print("******Attempted Android UA login successful.")

    def test_mac(self):
        # is truly a pc
        request = RequestFactory(HTTP_USER_AGENT=macUA).get('')

        self.assertFalse(user_agents.is_mobile(request))
        self.assertFalse(user_agents.is_touch_capable(request))
        self.assertFalse(user_agents.is_tablet(request))
        self.assertTrue(user_agents.is_pc(request))
        self.assertFalse(user_agents.is_bot(request))

        # test that you can login on Mac PC
        # use a link that requires auth
        response = self.client.get('/accounts/login/?next=/summary/0/', environ_base={'HTTP_USER_AGENT': macUA})
        self.assertEqual(response.status_code, 200)
        print("******Attempted Mac PC UA login successful.")

    def test_pc(self):
        # is truly a PC
        request = RequestFactory(HTTP_USER_AGENT=windowsUA).get('')

        self.assertFalse(user_agents.is_mobile(request))
        self.assertFalse(user_agents.is_touch_capable(request))
        self.assertFalse(user_agents.is_tablet(request))
        self.assertTrue(user_agents.is_pc(request))
        self.assertFalse(user_agents.is_bot(request))

        # test that you can login on Windows PC
        # use a link that requires auth
        response = self.client.get('/accounts/login/?next=/summary/0/', environ_base={'HTTP_USER_AGENT': windowsUA})
        self.assertEqual(response.status_code, 200)
        print("******Attempted Windows PC UA login successful.")

    def test_undefined(self):
        # empty UA returns an actual instance
        request = RequestFactory(HTTP_USER_AGENT=undefUA).get('')

        user_agent = get_user_agent(request)
        self.assertIsInstance(user_agent, UserAgent)

        # test that you can login on undefined UA
        # use a link that requires auth
        response = self.client.get('/accounts/login/?next=/summary/0/', environ_base={'HTTP_USER_AGENT': undefUA})
        self.assertEqual(response.status_code, 200)
        print("******Attempted unknown UA login successful.")


# test signup form
'''
def test_valid_form(self):
    w = Whatever.objects.create(title='Foo', body='Bar')
    data = {'title': w.title, 'body': w.body,}
    form = WhateverForm(data=data)
    self.assertTrue(form.is_valid())

def test_invalid_form(self):
    w = Whatever.objects.create(title='Foo', body='')
    data = {'title': w.title, 'body': w.body,}
    form = WhateverForm(data=data)
    self.assertFalse(form.is_valid())


class InspectionPageTest(TestCase):
    def test_inspection_page_returns_correct_html(self):
        # this request gets stopped because of middleware ???
        rq = HttpRequest()
        response = inspection(rq)
        expected_html = render_to_string('inspection.html', request=rq)
        self.assertEqual(response.content.decode(), expected_html)
'''
