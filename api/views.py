from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import authentication, permissions

from translate_manager.models import Project, GetMemberedProjectList, Notification, GetUserNoticationsQ

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser, )

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        # 'sender_user', 'reciever_user'
        fields = ( 'id', 'url',  'created_at', 'readed_at', 'msg_txt', 'msg_url', )

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        u  = self.request.user
        if u.is_authenticated:
            return GetUserNoticationsQ( u, True )
        else:
            return None

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    language_from = serializers.StringRelatedField()
    language_to = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ( 'id', 'url', 'shortname', 'description', 'state', 'language_from', 'language_to', )

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        u  = self.request.user
        if u.is_superuser:
            return Project.objects.all()
        else:
            return GetMemberedProjectList( u )

# версия API
CURRENT_API_VERSION = 1

@api_view()
@permission_classes((IsAuthenticated, ))
def get_api_ver(request):
    return Response({"api_version": CURRENT_API_VERSION })

@api_view()
@permission_classes((IsAuthenticated, ))
def get_my_profile(request):
    u  = request.user
    p = request.user.get_profile()

    return Response(  {"username": u.username, "email" : u.email , "nickname" : p.name })