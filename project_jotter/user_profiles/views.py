from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms.forms import BaseForm
from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import UserProfile
from .forms import EditProfileForm


class UserProfileView(generic.TemplateView):
    template_name = "user_profiles/user-profile.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        username = kwargs["username"]

        # Treat no username provided as a request to view the user's own
        # profile
        if username == "":
            if not request.user.is_authenticated:
                # In practice, we would implement a search mechanism,
                # but this is just a learner project which is unlikely
                # to be deployed or see any real use.
                messages.info(
                    request,
                    "No user was provided. Please specify a user "
                    "in the URL, or log in to view your own profile.",
                )
                return HttpResponseRedirect(reverse("login"))

            return HttpResponseRedirect(
                reverse("profile", kwargs={"username": request.user.username})
            )

        profile = self.try_get_user_profile(username)
        if profile is None:
            messages.error(request, f"User '{username}' does not exist.")
            return HttpResponseRedirect(reverse("index"))

        title = profile.name or profile.user.username
        kwargs.update({"profile": profile, "title": title})
        return super().get(request, *args, **kwargs)

    @staticmethod
    def try_get_user_profile(username: str) -> UserProfile:
        profiles = UserProfile.objects.filter(user__username=username)
        if len(profiles) == 1:
            return profiles[0]
        return None


class EditProfileView(LoginRequiredMixin, generic.FormView):
    success_url = reverse_lazy("profile")
    template_name = "user_profiles/edit-profile.html"

    def get_form(self, form_class=None) -> BaseForm:
        return EditProfileForm(instance=self.request.user.profile, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.warning(self.request, "Please log in to edit your profile.")
        return super().handle_no_permission()
