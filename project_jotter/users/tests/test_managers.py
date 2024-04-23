from django.core.exceptions import ValidationError
from django.test import TestCase

from users.managers import UserManager
from users.models import User


class UserManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.manager = UserManager()
        cls.manager.model = User
        super().setUpTestData()

    def test_create_user_requires_username(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(username="", email="test@testing.com")

    def test_create_user_requires_valid_email(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(username="Test", email="")
        with self.assertRaises(ValidationError):
            self.manager.create_user(username="Test", email="test")

    def test_create_user_normalizes_email(self):
        """
        create_user lowercases the domain part of an email but leaves the
        rest untouched.
        """
        user = self.manager.create_user(username="Test", email="tESt@TEsting.com")
        self.assertEqual(user.email, "tESt@testing.com")

    def test_create_user_creates_regular_unverified_user(self):
        user = self.manager.create_user(username="Test", email="tESt@TEsting.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        superuser = self.manager.create_superuser(
            username="Test", email="tESt@TEsting.com"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_verified)
