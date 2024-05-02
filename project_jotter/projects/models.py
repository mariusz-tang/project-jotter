from django.db import models

from users.models import User


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=150)
    image = models.ImageField(blank=True)
    contents = models.JSONField(blank=True, default=list)
    completed = models.BooleanField(blank=True, default=False)

    def clean(self) -> None:
        super().clean()
        if self.contents is None:
            self.contents = []

    def __str__(self):
        return f"{self.name} ({self.author})"

    class Meta:
        unique_together = (("author", "name"),)
