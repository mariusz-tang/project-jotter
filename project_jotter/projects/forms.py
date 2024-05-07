from django.forms import ModelForm

from .models import Project


class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "image", "is_completed", "is_private")
        labels = {
            "is_completed": "Mark this project as completed",
            "is_private": "Make this project private",
        }
