from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from translate_manager.models import Project

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ( 'id', 'url', 'shortname', 'state' )

class MyProjectViewSet(viewsets.ReadOnlyModelViewSet):
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    #def get_queryset(self):
    #    u  = self.request.user
    #    return GetMemberedProjectList( u )


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