from urllib.parse import quote

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from users.models import User


def validate_project_contents(value):
    if not isinstance(value, list):
        raise ValidationError(f"{value} is not a list")

    for entry in value:
        if not isinstance(entry, dict):
            raise ValidationError(f"{value} contains an entry which is not a dict")

        if (
            len(entry) != 2
            or "heading" not in entry
            or not isinstance(entry["heading"], str)
            or "content" not in entry
            or not isinstance(entry["content"], str)
        ):
            raise ValidationError(
                f"{value} contains an entry not in the expected "
                r"{'heading': '...', 'content': '...'} format"
            )


def get_image_file_name(instance, filename):
    return f"project-images/{instance.author.pk}/{instance.pk}/{filename}"


class Project(models.Model):
    name_validator = RegexValidator(
        regex=r"^[\w\s-]+$",
        message=(
            "Please enter a valid project name. This value may contain only "
            "letters, numbers, hyphens, underscores, and spaces. It must additionally "
            "contain at least one non-space character."
        ),
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects", help_text="Required."
    )
    name = models.CharField(
        verbose_name="project name",
        max_length=80,
        validators=[name_validator],
        help_text="Required. Your project name should consist of only letters, numbers, hypens, underscores, and spaces. "
        "It should not be named the same as any of your other projects.",
    )
    url = models.CharField(max_length=255, null=True, editable=False)
    image = models.ImageField(blank=True, upload_to=get_image_file_name)
    contents = models.JSONField(
        blank=True,
        default=list,
        validators=[validate_project_contents],
    )
    completed = models.BooleanField(blank=True, default=False)

    def clean(self) -> None:
        super().clean()
        # Django skips validation if the field is empty, and counts
        # {} as an empty value.
        if self.contents is None or isinstance(self.contents, dict):
            self.contents = []
        self.name = self.name.strip()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            # If the image has been changed, delete the previous one.
            old_instance = self.__class__.objects.get(pk=self.pk)
            if old_instance.image != self.image:
                old_instance.image.delete(save=False)

        self.url = quote(self.name)
        return super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.image.delete(save=False)
        return super().delete(using, keep_parents)

    def __str__(self):
        return f"{self.name} ({self.author})"

    class Meta:
        unique_together = (("author", "name"),)
