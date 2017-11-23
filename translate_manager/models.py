from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Language(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shortname

class Project(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shortname

class Project_Assignments(models.Model):
    project = models.ForeignKey( Project, blank=False, null=False )
    assigned_user = models.ForeignKey(User, blank=False, null=False )
    invited_at = models.DateTimeField( blank=True, null=True )
    accepted_at = models.DateTimeField( blank=True, null=True )