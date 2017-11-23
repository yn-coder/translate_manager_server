from django.contrib import admin

# Register your models here.
from .models import Language, Project

class LanguageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['shortname' ]}),
    ]
    search_fields = ['shortname']

admin.site.register(Language, LanguageAdmin)

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['shortname' ]}),
    ]
    search_fields = ['shortname']

admin.site.register(Project, ProjectAdmin)