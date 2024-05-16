from django.urls import path

from . import views

urlpatterns = [
    path("create", views.ProjectCreationView.as_view(), name="create-project"),
    path("<username>/<project_name>", views.ProjectDetailView.as_view(), name="view-project"),
    path("<username>/<project_name>/edit", views.ProjectEditView.as_view(), name="edit-project"),
]
