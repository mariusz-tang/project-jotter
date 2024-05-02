from django.core.exceptions import ValidationError
from django.test import TestCase

from project_jotter.test_utils import ModelFieldDeclarationTestCase
from projects.models import Project, validate_project_contents, get_image_file_name
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

    def test_url_field(self):
        self.assertFieldDeclaredAs("url", editable=False, max_length=255)

    def test_author_name_unique_together(self):
        self.assertTupleEqual((("author", "name"),), Project._meta.unique_together)


class ProjectModelTestCase(TestCase):
    def test_string_representation(self):
        user = User.objects.create(username="Tester")
        project = Project.objects.create(author=user, name="My Project")
        self.assertEqual(str(project), "My Project (Tester)")

    def test_contents_validation(self):
        """Contents should be accepted only in the right format"""
        user = user = User.objects.create()
        valid_data = [
            [],
            [{"heading": "", "content": ""}],
            {},
        ]
        invalid_data = [
            [{"heading": "", "content": []}],
            [
                {"heading": "", "content": ""},
                {"heading": {}, "content": ""},
            ],
            [[]],
            {"hello": []},
        ]
        for item in valid_data:
            project = Project(author=user, name="Test", contents=item)
            project.clean_fields()

        for item in invalid_data:
            with self.assertRaises(ValidationError):
                project = Project(author=user, name="Test", contents=item)
                project.clean_fields()

    def test_contens_validator_function(self):
        """
        Contents should be accepted only in the right format.

        This is a test of the validator function itself rather than of
        the model doing the validating.
        """
        valid_data = [
            [],
            [{"heading": "", "content": ""}],
        ]
        invalid_data = [
            [{"heading": "", "content": []}],
            [
                {"heading": "", "content": ""},
                {"heading": {}, "content": ""},
            ],
            [[]],
            {"hello": []},
            {},
        ]
        for item in valid_data:
            validate_project_contents(item)

        for item in invalid_data:
            with self.assertRaises(ValidationError):
                validate_project_contents(item)
