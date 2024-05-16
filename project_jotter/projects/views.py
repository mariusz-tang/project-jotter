from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.db.models.base import Model as Model
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views import generic

from . import forms
from .models import Project, ProjectSection


class ProjectCreationView(LoginRequiredMixin, generic.CreateView):
    template_name = "projects/create-project.html"
    success_url = reverse_lazy("profile")
    form_class = forms.ProjectCreationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.author = self.request.user
        return form

    def handle_no_permission(self):
        messages.warning(self.request, "Please log in to create a project.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(
            self.request, f"Project '{form.instance.name}' created successfully!"
        )
        return super().form_valid(form)


class ProjectEditView(generic.UpdateView):
    template_name = "projects/edit-project-details.html"
    fields = ["name", "image", "is_private", "is_completed"]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to edit a project.")
            return redirect("login", next=request.path)

        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect(
                "view-project",
                username=self.kwargs["username"],
                project_name=self.kwargs["project_name"],
            )

        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Model:
        try:
            return Project.objects.get(
                author__username=self.kwargs["username"],
                name=self.kwargs["project_name"],
            )
        except Project.DoesNotExist:
            raise Http404("Project not found.")

    def get_success_url(self):
        return reverse(
            "view-project",
            kwargs={
                "username": self.kwargs["username"],
                "project_name": self.object.name,
            },
        )


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "projects/view-project.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_private and request.user != self.object.author:
            # This echoes the behaviour of requesting a non-existent project
            raise Http404(
                "Project not found. If you are trying to access a private "
                "project, please log in first."
            )
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return Project.objects.get(
                author__username=self.kwargs["username"],
                name=self.kwargs["project_name"],
            )
        except Project.DoesNotExist:
            raise Http404(
                "Project not found. If you are trying to access a private "
                "project, please log in first."
            )


class ProjectSectionCreationView(LoginRequiredMixin, generic.CreateView):
    model = ProjectSection
    template_name = "projects/create-project-section.html"
    fields = ["heading", "body"]

    def dispatch(self, request, *args, **kwargs):
        try:
            self.parent_project = Project.objects.get(pk=kwargs["project_id"])
        except Project.DoesNotExist:
            raise Http404(
                "Project not found. If you are trying to access a private "
                "project, please log in first."
            )

        if self.request.user != self.parent_project.author:
            raise Http404(
                "Project not found. If you are trying to access a private "
                "project, please log in first."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.parent_project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["parent_project"] = self.parent_project
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse(
            "view-project",
            kwargs={
                "username": self.object.parent.author.username,
                "project_name": self.object.parent.name,
            },
        )
