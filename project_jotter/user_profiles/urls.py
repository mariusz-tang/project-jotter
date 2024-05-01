from django.urls import path

from .views import UserProfileView, EditProfileView

urlpatterns = [
    path("<username>/profile/", UserProfileView.as_view(), name="profile"),
    path(
        "profile/", UserProfileView.as_view(), kwargs={"username": ""}, name="profile"
    ),
    path("edit-profile", EditProfileView.as_view(), name="edit-profile"),
]
