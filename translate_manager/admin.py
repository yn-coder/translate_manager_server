from django.contrib import admin

# Register your models here.
from .models import Language, Project, Assignment, Notification, Doc

class LanguageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['shortname' ]}),
    ]
    search_fields = ['shortname']

admin.site.register(Language, LanguageAdmin)

class Doc_Assignments_Inline(admin.TabularInline):
    model = Doc
    fieldsets = [
        (None,               {'fields': ['name', 'doc',  ]}),
    ]
    readonly_fields = ( 'name', 'doc',  )

class Project_Assignments_Inline(admin.TabularInline):
    model = Assignment
    fieldsets = [
        (None,               {'fields': ['assigned_user', 'invited_at', 'accepted_at', 'dismissed_at' ]}),
    ]
    readonly_fields = ( 'invited_at', 'accepted_at', 'dismissed_at', )

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        Project_Assignments_Inline, Doc_Assignments_Inline
    ]
    fieldsets = [
        (None,               {'fields': ['shortname', 'state', 'language_from', 'language_to', 'description' ]}),
    ]
    search_fields = ['shortname', 'state']
    list_display = ( 'shortname', 'state' )

admin.site.register(Project, ProjectAdmin)


#from console.models import Console
from db_file_storage.form_widgets import DBAdminClearableFileInput
from django import forms
#from django.contrib import admin

class DocForm(forms.ModelForm):
    class Meta:
        model = Doc
        exclude = []
        widgets = {
            'doc': DBAdminClearableFileInput
        }

class DocAdmin(admin.ModelAdmin):
    #form = DocForm
    fieldsets = [
        (None,               {'fields': ['project', 'name', 'doc' ]}),
    ]
    list_display =  ('name', 'project')
    search_fields = ['name', 'project']

admin.site.register(Doc, DocAdmin)

class NotificationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['reciever_user', 'msg_txt', 'msg_url', 'created_at', 'readed_at', 'sender_user' ]}),
    ]
    search_fields = ['reciever_user', 'msg_txt']
    list_display =  ('reciever_user', 'msg_txt', 'created_at', 'readed_at', )

admin.site.register(Notification, NotificationAdmin)