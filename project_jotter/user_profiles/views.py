from typing import Any

from django.contrib import messages
from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from user_profiles.models import UserProfile


class UserProfileView(TemplateView):
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
