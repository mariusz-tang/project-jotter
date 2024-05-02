from django.db import models

from users.models import User


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to="project-images/")
    contents = models.JSONField(blank=True, default=list)
    completed = models.BooleanField(blank=True, default=False)

    def clean(self) -> None:
        super().clean()
        if self.contents is None:
            self.contents = []

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            # If the image has been changed, delete the previous one.
            old_instance = self.__class__.objects.get(pk=self.pk)
            if old_instance.image != self.image:
                old_instance.image.delete(save=False)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.name} ({self.author})"

    class Meta:
        unique_together = (("author", "name"),)
