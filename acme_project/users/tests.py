from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'new_user',
            'password1': 'Secure-Registration-729!',
            'password2': 'Secure-Registration-729!',
        }

    def test_registration_page(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/registration_form.html'
        )

    def test_registration_and_login(self):
        response = self.client.post(
            reverse('registration'), self.credentials
        )
        self.assertRedirects(response, reverse('login'))
        user = get_user_model().objects.get(username='new_user')
        self.assertTrue(user.check_password(self.credentials['password1']))
        response = self.client.post(reverse('login'), {
            'username': self.credentials['username'],
            'password': self.credentials['password1'],
        })
        self.assertRedirects(response, reverse('pages:homepage'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(username='new_user')
        response = self.client.post(
            reverse('registration'), self.credentials
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_mismatched_passwords_are_rejected(self):
        self.credentials['password2'] = 'Different-Password-729!'
        response = self.client.post(
            reverse('registration'), self.credentials
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)
        self.assertFalse(get_user_model().objects.exists())
