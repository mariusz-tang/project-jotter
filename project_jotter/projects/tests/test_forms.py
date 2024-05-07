from django.test import TestCase

from projects import forms
from projects.models import Project
from users.models import User


class ProjectCreationFormTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_name_is_required(self):
        form = forms.ProjectCreationForm()
        self.assertTrue(form.fields["name"].required)

    def test_name_is_unique_per_user(self):
        user = User.objects.create(username="Tester", email="Tester@test.com")
        form1 = forms.ProjectCreationForm(
            instance=Project(author=user), data={"name": "Project"}
        )
        self.assertTrue(form1.is_valid())
        form1.save()

        form2 = forms.ProjectCreationForm(
            instance=Project(author=user), data={"name": "Project"}
        )
        self.assertFalse(form2.is_valid())

    def test_name_is_valid(self):
        user = User.objects.create(username="Tester", email="Tester@test.com")
        form1 = forms.ProjectCreationForm(
            instance=Project(author=user), data={"name": "Project"}
        )
        self.assertTrue(form1.is_valid())

        form2 = forms.ProjectCreationForm(
            instance=Project(author=user), data={"name": "."}
        )
        self.assertFalse(form2.is_valid())
        self.assertTrue(
            "Please enter a valid project name. "
            "This value may contain only letters, numbers, hyphens, underscores, and spaces. "
            "It must additionally contain at least one non-space character."
            in form2.errors.as_ul()
        )
