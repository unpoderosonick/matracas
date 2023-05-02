from core.models import Person
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .api_views.people import PersonViewSet, PersonPathSerializer
from .api_views.users import UserViewSet, UserPathSerializer


def home_view(request):
    message = 'hello low'
    return render(request, 'dashboard/home.html', locals())


class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'dashboard/profile_list.html'
    template_name = 'rest_framework/api.html'

    def get(self, request):
        queryset = User.objects.all()
        return Response({'profiles': queryset})

class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')
    
    # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'%s' % UserPathSerializer.get_path(), UserViewSet)
router.register(r'%s' % PersonPathSerializer.get_path(), PersonViewSet)
# router.register(r'profile-list', ProfileList, base_name='profile-list')