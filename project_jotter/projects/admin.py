from django.contrib import admin

from users.admin import UserAdmin
from .models import Project, ProjectSection


class SectionInline(admin.StackedInline):
    model = ProjectSection
    extra = 0


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    show_change_link = True


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("name", "author", "is_completed", "is_private")},
        ),
    )
    list_display = ("name", "author", "is_completed")
    list_filter = ("is_completed",)
    search_fields = ("name", "author")
    inlines = (SectionInline,)


UserAdmin.inlines = (*UserAdmin.inlines, ProjectInline)
admin.site.register(Project, ProjectAdmin)
