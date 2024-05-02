from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    The User model. Implements admin-compliant permissions.

    Username, email, and password are required. Other fields are optional.
    """

    username_validator = RegexValidator(
        regex=r"^[\w.@+-]+\Z",
        message=(
            "Please enter a valid username. This value may contain only letters, "
            "numbers, and @/./+/-/_ characters."
        ),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. The username must be at most 150 charactes long "
            "and consist solely of letters, numbers and @/./+/-/_."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        "email address",
        unique=True,
        help_text="Required.",
        error_messages={
            "unique": "A user with that email address already exists.",
        },
    )

    given_name = models.CharField(
        "preferred name",
        max_length=150,
        blank=True,
        help_text="The name used to refer to the user in communications",
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )
    is_verified = models.BooleanField("email verification status", default=False)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def clean(self):
        super().clean()
        cls = self.__class__
        self.email = cls.objects.normalize_email(self.email)

        if (
            cls.objects.filter(username__iexact=self.username)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"username": self.unique_error_message(cls, ["username"])}
            )

    def get_short_name(self):
        return self.given_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
