from django.test import TestCase
from django.urls import reverse
from django.conf import settings


def signup_testuser(client):
    return client.post(SignUpViewTests.url, settings.TESTING['SIGNUP_CREDS'])


class SignUpViewTests(TestCase):
    url = reverse('users:signup')

    @staticmethod
    def fields(a, b, c):
        """ Helper method to arrange form data """
        return {'username': a, 'password1': b, 'password2': c}

    def test_invalid_data(self):
        """ Should get 200 on invalid data cause no redirects happen """
        resp = self.client.post(self.url, self.fields('q', 'q', 'q'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(self.url, {'username': 'nopasswords'})
        self.assertEqual(resp.status_code, 200)

    def test_valid_data(self):
        """ Should be redirected on successful signup """
        resp = signup_testuser(self.client)

        self.assertEqual(resp.status_code, 302)


class SignInViewTests(TestCase):
    url = reverse('users:signin')

    @staticmethod
    def fields(a, b):
        """ Helper method to arrange form data """
        return {'username': a, 'password': b}

    def test_invalid_data(self):
        """ Status code 200 """
        resp = self.client.post(self.url, self.fields('q', 'q'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(self.url, {'username': 'nopasswords'})
        self.assertEqual(resp.status_code, 200)

    def test_valid_data(self):
        """ Redirect on successful login to `polls:index` """
        signup_testuser(self.client)
        resp = self.client.post(self.url, settings.TESTING['SIGNIN_CREDS'])

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('polls:index'))
