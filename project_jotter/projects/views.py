from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from .models import Project

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
        messages.success(self.request, f"Project '{form.instance.name}' created successfully!")
        return super().form_valid(form)
    

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "projects/view-project.html"
    
    def get_object(self, queryset=None):
        return Project.objects.get(author__username=self.kwargs["username"], name=self.kwargs["project_name"])
