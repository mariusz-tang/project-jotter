from django.contrib import messages
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from .forms import UserRegistrationForm


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome, {form.get_user().username}! You have been logged in.")
        return super().form_valid(form)


class RegistrationView(views.FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("edit-profile")
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


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("profile")
    template_name = "users/change-password.html"

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!")
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(self.request, "You have been logged out.")
        return super().post(request, *args, **kwargs)
