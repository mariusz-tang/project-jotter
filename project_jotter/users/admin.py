from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Overriden to reflect field mismatches between the default User
    model and the one defined in this application.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("given_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    # ! These may need overriding when the relevant custom forms are created
    # form = UserChangeForm
    # add_form = UserCreationForm

    list_display = ("username", "email", "given_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_verified", "groups")
    search_fields = ("username", "given_name", "email")


admin.site.register(User, UserAdmin)
