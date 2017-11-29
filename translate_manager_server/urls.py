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

from api.views import UserViewSet, ProjectViewSet, ProjectViewSet, NotificationViewSet, get_api_ver, get_my_profile

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'my_notifications', NotificationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r'^webapi/', include(router.urls)),
    url(r'^webapi/get_api_ver/$', get_api_ver),
    url(r'^webapi/get_my_profile/$', get_my_profile),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]