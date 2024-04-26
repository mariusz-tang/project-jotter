from django.test import TestCase
from django.urls import reverse

from users.models import User


class ProfilePageTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse("profile")
        cls.user_url = reverse("profile", kwargs={"username": "tester"})
        super().setUpClass()

    def test_expected_no_username_url(self):
        self.assertEqual(self.url, "/users/profile/")

    def test_expected_username_url(self):
        self.assertEqual(self.user_url, "/users/tester/profile/")

    def test_redirects_unauthenticated_user_on_no_username_provided(self):
        request = self.client.get(self.url)
        self.assertRedirects(request, reverse("login"))

    def test_redirects_authenticated_user_on_no_username_provided(self):
        user = User.objects.create(username="tester")
        self.client.force_login(user)
        request = self.client.get(self.url)
        self.assertRedirects(request, self.user_url)

    def test_correct_templates_used(self):
        User.objects.create(username="tester")
        request = self.client.get(self.user_url)
        self.assertTemplateUsed(request, "user_profiles/user-profile.html")

        request = self.client.get(reverse("profile", kwargs={"username": "blah"}))
        self.assertTemplateUsed(request, "user_profiles/profile-does-not-exist.html")

    def test_correct_context_passed(self):
        user = User.objects.create(username="tester")
        named_user = User.objects.create(username="tester2", email="test@hello.yo")
        named_user.profile.name = "Name"
        named_user.profile.save()

        request = self.client.get(
            reverse("profile", kwargs={"username": user.username})
        )
        self.assertEqual(request.context["profile"], user.profile)
        self.assertEqual(request.context["title"], user.username)

        request = self.client.get(
            reverse("profile", kwargs={"username": named_user.username})
        )
        self.assertEqual(request.context["profile"], named_user.profile)
        self.assertEqual(request.context["title"], named_user.profile.name)
