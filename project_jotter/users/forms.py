from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms.fields import EmailField

from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given
    username, email, and password.

    Rejects usernames differing only in case.
    """

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField, "email": EmailField}
