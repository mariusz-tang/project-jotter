from django.test import TestCase

from project_jotter.test_utils import ModelFieldDeclarationTestCase
from projects.models import Project
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

    def test_contents_field(self):
        self.assertFieldDeclaredAs("contents", verbose_name="contents", blank=True)

    def test_completed_field(self):
        self.assertFieldDeclaredAs(
            "completed", verbose_name="completed", blank=True, default=False
        )

    def test_author_name_unique_together(self):
        self.assertTupleEqual((("author", "name"),), Project._meta.unique_together)


class ProjectMethodsTestCase(TestCase):
    def test_string_representation(self):
        user = User.objects.create(username="Tester")
        project = Project.objects.create(author=user, name="My Project")
        self.assertEqual(str(project), "My Project (Tester)")
