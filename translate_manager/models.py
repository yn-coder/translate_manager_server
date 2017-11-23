from django.db import models

# Create your models here.

class Language(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shortname

class Project(models.Model):
    shortname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shortname