from django.core import mail
from django.test import TestCase
from django.utils import timezone

from users.models import User
from project_jotter.test_utils import ModelFieldDeclarationTestCase


class UserModelFieldDeclarationTestCase(ModelFieldDeclarationTestCase):
    model = User

    def test_username_field(self):
        self.assertFieldDeclaredAs(
            "username",
            verbose_name="username",
            blank=False,
            unique=True,
            max_length=150,
            help_text=(
                "Required. The username must be at most 150 charactes long "
                "and consist solely of letters, numbers and @/./+/-/_."
            ),
        )

    def test_email_field(self):
        self.assertFieldDeclaredAs(
            "email",
            verbose_name="email address",
            blank=False,
            unique=True,
            help_text="Required.",
        )

    def test_given_name_field(self):
        self.assertFieldDeclaredAs(
            "given_name",
            verbose_name="preferred name",
            help_text="The name used to refer to the user in communications",
        )

    def test_is_staff_field(self):
        self.assertFieldDeclaredAs(
            "is_staff",
            verbose_name="staff status",
            default=False,
            help_text="Designates whether the user can log into the admin site.",
        )

    def test_is_verified_field(self):
        self.assertFieldDeclaredAs(
            "is_verified", verbose_name="email verification status", default=False
        )

    def test_date_joined(self):
        self.assertFieldDeclaredAs(
            "date_joined", verbose_name="date joined", default=timezone.now
        )


class UserModelMethodTestCase(TestCase):
    def test_clean_normalizes_email(self):
        """
        clean lowercases the domain part of an email but leaves the
        rest untouched.
        """
        user = User.objects.create(email="tESt@TEsting.com")
        self.assertEqual(user.email, "tESt@TEsting.com")
        user.clean()
        user.save()
        self.assertEqual(user.email, "tESt@testing.com")
    
    def test_short_name_returns_given_name(self):
        user = User.objects.create(given_name="Tim")
        self.assertEqual(user.get_short_name(), user.given_name)
        
    def test_email_user(self):
        user = User.objects.create(email="test@testing.com")
        subject = "subject"
        message = "message"
        from_email = "hello@world.com"
        user.email_user(subject, message, from_email)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, message)
        self.assertEqual(email.from_email, from_email)
        self.assertListEqual(email.to, [user.email])