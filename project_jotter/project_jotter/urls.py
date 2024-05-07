from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("users/", include("user_profiles.urls")),
    path("", include("pages.urls")),
    path("projects/", include("projects.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
