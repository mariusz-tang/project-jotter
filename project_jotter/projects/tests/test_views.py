from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from projects import forms
from projects.models import Project
from users.models import User


class ProjectCreationPageTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse("create-project")
        cls.url_string = "/projects/create"
        cls.template_name = "projects/create-project.html"
        cls.form_class = forms.ProjectCreationForm

    def test_expected_url(self):
        self.assertEqual(self.url, self.url_string)

    def test_correct_template_used(self):
        user = User.objects.create(username="Test", email="test@test.com")
        self.client.force_login(user)
        request = self.client.get(self.url)
        self.assertTemplateUsed(request, self.template_name)

    def test_redirects_unauthenticated_user(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 302)
        self.assertTrue(request.url.startswith(reverse("login")))
        messages = list(get_messages(request.wsgi_request))
        self.assertTrue(len(messages) == 1)
        self.assertTrue(messages[0].message == "Please log in to create a project.")

    def test_correct_form(self):
        user = User.objects.create(username="Test", email="test@test.com")
        self.client.force_login(user)
        request = self.client.get(self.url)
        self.assertTrue(isinstance(request.context["form"], self.form_class))

    def test_valid_form(self):
        """
        The project is created and the user is redirected to the
        edit-project page
        """
        user = User.objects.create(username="Test", email="test@test.com")
        self.client.force_login(user)
        request = self.client.post(self.url, {"name": "Test"})
        self.assertEqual(request.status_code, 302)
        # ! TEMP: URL needs to change one edit-profile page is
        # ! implemented
        self.assertEqual(request.url, reverse("profile"))
        projects = Project.objects.all()
        self.assertEqual(len(projects), 1)
        project = projects.get()
        self.assertEqual(project.author, user)
        self.assertEqual(project.name, "Test")
