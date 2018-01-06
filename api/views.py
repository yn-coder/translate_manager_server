from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import authentication, permissions

from translate_manager.models import Language, Project, GetMemberedProjectList, Notification, GetUserNoticationsQ, Assignment, Doc

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ( 'id', 'url', 'shortname', )

# ViewSets define the view behavior.
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated, )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ( 'id', 'url', 'username', 'email', 'is_staff')

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
        fields = ( 'id', 'url',  'created_at', 'readed_at', 'msg_txt', 'msg_url', 'decode_msg', 'get_project_id' )

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

class AssignmentSerializer(serializers.ModelSerializer):
    assigned_user = serializers.StringRelatedField()
    #assigned_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True ) #, queryset = User.objects.all()

    class Meta:
        model = Assignment
        fields = ( 'id', 'url', 'project', 'assigned_user', 'assigned_user_id',
        'invited_at', 'accepted_at', 'dismissed_at' )
        read_only_fields = ( 'invited_at', 'accepted_at', 'dismissed_at' )

class AssignmentViewSet(viewsets.ModelViewSet):
    model = Assignment
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class DocSerializer(serializers.HyperlinkedModelSerializer):
    project_id = serializers.IntegerField( required = True )

    class Meta:
        model = Doc
        fields = ( 'id', 'url', 'name', 'doc', 'project_id' )

class DocViewSet(viewsets.ModelViewSet):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser, )

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    #assignments = serializers.StringRelatedField(many=True )
    #assignments = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset = User.objects.all() )
    assignments = AssignmentSerializer( many=True, read_only=True )
    #assignments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name = 'Assignment-detail' )
    project_docs = DocSerializer( many=True, read_only=True )
    language_from_id = serializers.IntegerField( required = False )
    language_to_id = serializers.IntegerField( required = False )

    class Meta:
        model = Project
        fields = ( 'id', 'url', 'shortname', 'description', 'state', 'language_from_id', 'language_to_id', 'GUID', 'created_at', 'modified_at', 'assignments', 'project_docs' )
        read_only_fields = ('GUID', 'created_at', 'modified_at' )

class ProjectViewSet(viewsets.ModelViewSet):
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (IsAuthenticated,)

#    def perform_create(self, serializer):
#        serializer.save()

    def get_queryset(self):
        u  = self.request.user
        if u.is_superuser:
            return Project.objects.all()
        else:
            return GetMemberedProjectList( u )

# версия API
CURRENT_API_VERSION = 3

@api_view()
@permission_classes((IsAuthenticated, ))
def get_api_ver(request):
    return Response({"api_version": CURRENT_API_VERSION })

@api_view()
@permission_classes((IsAuthenticated, ))
def get_my_profile(request):
    u  = request.user

    return Response(  {"username": u.username, "email" : u.email, "is_staff" : u.is_staff })

@api_view()
@permission_classes((IsAuthenticated, ))
def add_user2project(request, user_id, project_id):
    if request.user.is_staff:
        try:
            project = Project.objects.get( id = project_id )
            user = User.objects.get( id = user_id )
            assign = Assignment();
            assign.project=project
            assign.assigned_user = user
            assign.save()
            return Response( {"result": "ok", 'user' : str(user ), 'project': str( project ) })
        except:
            return Response( {"result":"fail"}  )
    else:
        return Response( {"result":"not staff"}  )