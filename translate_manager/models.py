from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

from .messages import *

class Notification(models.Model):
    sender_user = models.ForeignKey(User, related_name = 'sender_user', blank=True, null = True )
    created_at = models.DateTimeField(default=timezone.now)
    reciever_user = models.ForeignKey(User, related_name = 'reciever_user')
    readed_at = models.DateTimeField( blank=True, null = True )
    msg_txt = models.CharField(max_length=255, blank=False)
    msg_url = models.URLField(max_length=75, blank=True, null = True)

    def decode_msg( self ):
        return decode_json2msg( self.msg_txt )

    def get_project_id( self ):
        return get_project_id_from_msg( self.msg_txt )

    def get_unreaded( self ):
        return self.readed_at is None

    def mark_readed(self):
        if self.readed_at is None:
            self.readed_at = timezone.now()
            self.save()
        # ����� - ������ �� ������

    def get_absolute_url(self):
        return "/notification/%i/" % self.id

def GetUserNoticationsQ( arg_user, arg_new ):
    return Notification.objects.filter(reciever_user = arg_user, readed_at__isnull=arg_new).order_by('-created_at')

from commons.models import BaseStampedModel

class Language(BaseStampedModel):
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

class Project(BaseStampedModel):
    shortname = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.PositiveSmallIntegerField( blank=False, null=False, default = PROJECT_STATE_DRAFT, choices = PROJECT_STATE_LIST_CHOICES )
    language_from = models.ForeignKey( Language, blank=True, null=True, related_name = "language_from" )
    language_to = models.ForeignKey( Language, blank=True, null=True, related_name = "language_to" )

    def __str__(self):
        if self.shortname:
            return self.shortname
        else:
            return ""

    def state_caption(self):
        if self.state:
            return PROJECT_STATE_LIST_CHOICES[self.state][1]
        else:
            return PROJECT_STATE_LIST_CHOICES[PROJECT_STATE_DRAFT][1]

    def Get_Members( self ):
        q = User.objects.filter( assigned_user__project = self)
        return q

    def get_absolute_url(self):
        return "/project/project/%i/" % self.id

from .notification_helper import Send_Notification

class DocFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Doc(BaseStampedModel):
    name = models.CharField(max_length=100)
    doc = models.FileField(upload_to='translate_manager.DocFile/bytes/filename/mimetype', blank=True, null=True)
    project = models.ForeignKey( Project, blank=False, null=False, related_name = 'project_docs' )

    def save(self, *args, **kwargs):
        super(Doc, self).save(*args, **kwargs)
        message_str = project_msg2json_str( MSG_NOTIFY_PROJECT_DOC_CAHNGED_ID, arg_project_name = self.project.shortname, arg_project_id = self.project.id )
        for u in self.project.Get_Members():
            Send_Notification( None, u, message_str, self.project.get_absolute_url() )

class Assignment(BaseStampedModel):
    project = models.ForeignKey( Project, blank=False, null=False, related_name = 'assignments' )
    assigned_user = models.ForeignKey(User, blank=False, null=False, related_name = 'assigned_user' )
    invited_at = models.DateTimeField( blank=True, null=True )
    accepted_at = models.DateTimeField( blank=True, null=True )
    dismissed_at = models.DateTimeField( blank=True, null=True )

    class Meta:
        unique_together = ("project", "assigned_user")

    def __str__(self):
        return str(self.assigned_user)# + ' ' + str(self.project)

    def save(self, *args, **kwargs):
        if self.invited_at is None:
            self.invited_at = timezone.now()
        super(Assignment, self).save(*args, **kwargs)
        if ( self.accepted_at is None ): # send invite
            message_str = project_msg2json_str( MSG_NOTIFY_TYPE_ASK_ACCEPT_ID, arg_project_name = self.project.shortname, arg_project_id = self.project.id )
            Send_Notification( None, self.assigned_user, message_str, self.project.get_absolute_url() )

def GetMemberedProjectList( arg_user ): # return Project dataset
    return Project.objects.filter( assignment__assigned_user=arg_user)