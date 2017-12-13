"""Django_Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers, serializers, viewsets

from api.views import UserViewSet, ProjectViewSet, ProjectViewSet, NotificationViewSet, AssignmentViewSet, get_api_ver, get_my_profile, add_user2project, DocViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'doc', DocViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'my_notifications', NotificationViewSet)
router.register(r'users', UserViewSet)
router.register(r'assignments', AssignmentViewSet)

from django.conf import settings
from django.conf.urls.static import static

from translate_manager.models import Project

class HomePageView(TemplateView):

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all().order_by('-modified_at')
        return context

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^$", HomePageView.as_view(), name="home"),
    url(r'^webapi/', include(router.urls)),
    url(r'^webapi/get_api_ver/$', get_api_ver),
    url(r'^webapi/get_my_profile/$', get_my_profile),
    url(r'^webapi/add_user2project/(?P<user_id>\w+)/(?P<project_id>\w+)/$', add_user2project),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^files/', include('db_file_storage.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

