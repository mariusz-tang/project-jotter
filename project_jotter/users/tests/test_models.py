from django.core.mail import outbox
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
