from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a user with the given username, email and
        password.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a staff superuser with the given username, email
        and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user


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
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        return self.given_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
