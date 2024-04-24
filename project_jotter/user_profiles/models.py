from django.db import models

from users.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(
        "display name",
        blank=True,
        max_length=150,
        help_text="The name displayed on the user's profile page.",
    )
    pronouns = models.CharField(blank=True, max_length=50)
    bio = models.TextField(blank=True, max_length=400)
    
    def __str__(self) -> str:
        return f"{self.user}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """Create a new profile on user creation"""
    # Check that the user does not already have a profile,
    # which could happen if the user is created through the admin site.
    if created and not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)


models.signals.post_save.connect(
    create_profile,
    sender=User,
    weak=False,
    dispatch_uid="user_profiles.create_profile_on_user_creation",
)
