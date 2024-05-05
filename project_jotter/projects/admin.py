from django.contrib import admin

from users.admin import UserAdmin
from .models import Project


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    show_change_link = True


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "author", "completed", "is_private", "contents")}),)
    list_display = ("name", "author", "completed")
    list_filter = ("completed",)
    search_fields = ("name", "author")


UserAdmin.inlines = (*UserAdmin.inlines, ProjectInline)
admin.site.register(Project, ProjectAdmin)
