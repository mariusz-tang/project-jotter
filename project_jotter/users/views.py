from django.contrib import messages
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from .forms import UserRegistrationForm


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True


class RegistrationView(views.FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("profile")
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("profile"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, "Account created successfully! Welcome to Project Jotter :)"
        )
        return super().form_valid(form)
