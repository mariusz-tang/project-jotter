from django.test import TestCase
from django.urls import reverse

from users.models import User


class LoginPageTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse("login")
        super().setUpClass()

    def test_expected_url(self):
        self.assertEqual(self.url, "/auth/login/")

    def test_correct_template_used(self):
        request = self.client.get(self.url)
        self.assertTemplateUsed(request, "users/login.html")

    def test_redirects_authenticated_user(self):
        user = User.objects.create()
        self.client.force_login(user)
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, reverse("profile"))