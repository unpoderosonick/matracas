from django.shortcuts import render
from rest_framework import routers
from .api_views.people import PersonViewSet, PersonPathSerializer
from .api_views.users import UserViewSet, UserPathSerializer
from .api_views.zones import ZoneViewSet, ZonePathSerializer


def home_view(request):
    message = 'hello low'
    return render(request, 'dashboard/home.html', locals())


    # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'%s' % UserPathSerializer.get_path(), UserViewSet)
router.register(r'%s' % PersonPathSerializer.get_path(), PersonViewSet)
router.register(r'%s' % ZonePathSerializer.get_path(), ZoneViewSet)
