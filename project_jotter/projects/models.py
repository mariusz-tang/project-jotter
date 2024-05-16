from urllib.parse import quote

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from users.models import User


def get_image_file_name(instance, filename):
    return f"project-images/{instance.author.pk}/{filename}"


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
    is_completed = models.BooleanField(
        verbose_name="completed", blank=True, default=False
    )
    is_private = models.BooleanField(
        verbose_name="private",
        blank=True,
        default=False,
        help_text="Private projects are not displayed to other users who visit your profile",
    )

    def clean(self) -> None:
        super().clean()
        self.name = self.name.strip()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        same_author = self.__class__.objects.filter(author=self.author, name=self.name)
        if len(same_author) > 2 or (
            len(same_author) == 1 and same_author.get() != self
        ):
            if "name" in exclude:
                raise ValidationError(
                    "You may not have more than one project with the same name."
                )
            else:
                raise ValidationError(
                    {
                        "name": "You may not have more than one project with the same name."
                    }
                )

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


class ProjectSection(models.Model):
    parent = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="parent project",
        related_name="sections",
    )
    heading = models.CharField(max_length=80, blank=True)
    body = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(heading="") | ~Q(body=""),
                name="not_both_null",
                violation_error_message="At least one of the heading or the body have to be non-empty."
            )
        ]
        indexes = [models.Index(fields=["parent"])]
