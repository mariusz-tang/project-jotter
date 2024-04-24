from django.contrib import admin

from users.admin import UserAdmin
from .models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# We add profiles as an inline to the UserAdmin instead of creating
# and/or registering a ProfileAdmin separately.
UserAdmin.inlines = (*UserAdmin.inlines, ProfileInline)