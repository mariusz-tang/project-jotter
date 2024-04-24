from django.test import TestCase

from project_jotter.test_utils import ModelFieldDeclarationTestCase
from user_profiles.models import UserProfile
from users.models import User


class UserProfileDeclarationTestCase(ModelFieldDeclarationTestCase):
    model = UserProfile

    def test_user_field(self):
        self.assertFieldDeclaredAs(
            "user",
            verbose_name="user",
            unique=True,
            blank=False,
        )

    def test_name_field(self):
        self.assertFieldDeclaredAs(
            "name",
            verbose_name="display name",
            blank=True,
            max_length=150,
            help_text="The name displayed on the user's profile page.",
        )

    def test_pronouns_field(self):
        self.assertFieldDeclaredAs(
            "pronouns", verbose_name="pronouns", blank=True, max_length=50
        )

    def test_bio_field(self):
        self.assertFieldDeclaredAs(
            "bio", verbose_name="bio", blank=True, max_length=400
        )


class UserProfileTestCase(TestCase):
    def test_automatic_creation(self):
        """A profile is created automatically on user creation"""
        user = User.objects.create()
        self.assertEqual(UserProfile.objects.count(), 1)
        profile = UserProfile.objects.get()
        self.assertEqual(user.profile, profile)

    def test_str(self):
        user = User.objects.create(username="tester")
        self.assertEqual(str(user.profile), "tester's profile")
