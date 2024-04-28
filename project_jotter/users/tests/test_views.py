from django.test import TestCase
from django.urls import reverse

from users.models import User


class RegistrationPageTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse("register")
        cls.url_string = "/auth/register/"
        cls.template_name = "users/register.html"
        super().setUpClass()

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


class LoginPageTestCase(RegistrationPageTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse("login")
        cls.url_string = "/auth/login/"
        cls.template_name = "users/login.html"
        super().setUpClass()
