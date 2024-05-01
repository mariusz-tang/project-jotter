from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

from users.models import User
import users.forms as forms


class RegistrationPageTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse("register")
        cls.url_string = "/auth/register/"
        cls.template_name = "users/register.html"
        cls.form_class = forms.UserRegistrationForm

    def test_expected_url(self):
        self.assertEqual(self.url, self.url_string)

    def test_correct_template_used(self):
        request = self.client.get(self.url)
        self.assertTemplateUsed(request, self.template_name)

    def test_redirects_authenticated_user(self):
        user = User.objects.create()
        self.client.force_login(user)
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, reverse("profile"))

    def test_correct_form(self):
        request = self.client.get(self.url)
        self.assertTrue(isinstance(request.context["form"], self.form_class))


class LoginPageTestCase(RegistrationPageTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse("login")
        cls.url_string = "/auth/login/"
        cls.template_name = "users/login.html"
        cls.form_class = AuthenticationForm
