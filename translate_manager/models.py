from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Language(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shortname

PROJECT_STATE_DRAFT = 0
PROJECT_STATE_PUBLISHED = 1
PROJECT_STATE_IN_PROCESS = 2
PROJECT_STATE_DONE = 3
PROJECT_STATE_ARCHIVE = 4
PROJECT_STATE_CANCEL = 5

PROJECT_STATE_LIST = ( PROJECT_STATE_DRAFT, PROJECT_STATE_PUBLISHED, PROJECT_STATE_IN_PROCESS, PROJECT_STATE_DONE, PROJECT_STATE_ARCHIVE, PROJECT_STATE_CANCEL )

PROJECT_STATE_LIST_CHOICES = (
  ( PROJECT_STATE_DRAFT , 'DRAFT' ),
  ( PROJECT_STATE_PUBLISHED, 'PUBLISHED' ),
  ( PROJECT_STATE_IN_PROCESS, 'IN PROCESS' ),
  ( PROJECT_STATE_DONE, 'DONE' ),
  ( PROJECT_STATE_ARCHIVE, 'ARCHIVE' ),
  ( PROJECT_STATE_CANCEL, 'CANCEL' ),

     )

class Project(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.PositiveSmallIntegerField( blank=False, null=False, default = PROJECT_STATE_DRAFT, choices = PROJECT_STATE_LIST_CHOICES )
    language_from = models.ForeignKey( Language, blank=True, null=True, related_name = "language_from" )
    language_to = models.ForeignKey( Language, blank=True, null=True, related_name = "language_to" )

    def __str__(self):
        return self.shortname

class Project_Assignments(models.Model):
    project = models.ForeignKey( Project, blank=False, null=False )
    assigned_user = models.ForeignKey(User, blank=False, null=False )
    invited_at = models.DateTimeField( blank=True, null=True )
    accepted_at = models.DateTimeField( blank=True, null=True )
    dismissed_at = models.DateTimeField( blank=True, null=True )