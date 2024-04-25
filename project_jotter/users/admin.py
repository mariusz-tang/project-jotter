from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.display(description="Display name")
def display_name(user):
    return user.profile.name


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

    list_display = ("username", "email", display_name, "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_verified", "groups")
    search_fields = ("username", "profile__name", "email")


admin.site.register(User, UserAdmin)
