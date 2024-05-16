from django.core.exceptions import ValidationError
from django.test import TestCase

from project_jotter.test_utils import ModelFieldDeclarationTestCase
from projects.models import Project, ProjectSection
from users.models import User


class ProjectDeclarationTestCase(ModelFieldDeclarationTestCase):
    model = Project

    def test_author_field(self):
        self.assertFieldDeclaredAs("author", verbose_name="author", blank=False)

    def test_name_field(self):
        self.assertFieldDeclaredAs(
            "name",
            verbose_name="project name",
            blank=False,
            max_length=80,
            help_text="Required. Your project name should consist of only letters, numbers, hypens, underscores, and spaces. "
            "It should not be named the same as any of your other projects.",
        )

    def test_image_field(self):
        self.assertFieldDeclaredAs("image", verbose_name="image", blank=True)

    def test_is_completed_field(self):
        self.assertFieldDeclaredAs(
            "is_completed", verbose_name="completed", blank=True, default=False
        )

    def test_is_private_field(self):
        self.assertFieldDeclaredAs(
            "is_private",
            verbose_name="private",
            blank=True,
            default=False,
            help_text="Private projects are not displayed to other users who visit your profile",
        )

    def test_url_field(self):
        self.assertFieldDeclaredAs("url", editable=False, max_length=255)

    def test_author_name_unique_together(self):
        self.assertTupleEqual((("author", "name"),), Project._meta.unique_together)


class ProjectModelTestCase(TestCase):
    def test_string_representation(self):
        user = User.objects.create(username="Tester")
        project = Project.objects.create(author=user, name="My Project")
        self.assertEqual(str(project), "My Project (Tester)")


class ProjectSectionDeclarationTestCase(ModelFieldDeclarationTestCase):
    model = ProjectSection

    def test_parent_field(self):
        self.assertFieldDeclaredAs(
            "parent",
            verbose_name="parent project",
            blank=False,
        )

    def test_heading_field(self):
        self.assertFieldDeclaredAs(
            "heading", verbose_name="heading", max_length=80, blank=True
        )

    def test_body_field(self):
        self.assertFieldDeclaredAs("body", verbose_name="body", blank=True)
