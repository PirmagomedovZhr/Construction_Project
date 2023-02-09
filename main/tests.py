from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import SignInForm
from .models import User


class SignInViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('signin')
        self.user = User.objects.create_user(
            username='testuser', password='secretpassword'
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main/signin.html')

    def test_view_displays_form(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsInstance(form, SignInForm)

    def test_view_authenticates_valid_credentials(self):
        data = {'username': 'testuser', 'password': 'secretpassword'}
        response = self.client.post(self.url, data)
        user = authenticate(username='testuser', password='secretpassword')
        self.assertEqual(user, response.context['user'])

    def test_view_does_not_authenticate_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
