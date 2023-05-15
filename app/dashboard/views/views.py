from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .apis.people import PersonViewSet, PersonPathSerializer
from .apis.users import UserViewSet, UserPathSerializer


@login_required
def home_view(request):
    message = "hello low"
    return render(request, "dashboard/home.html", locals())


people_path = PersonPathSerializer.get_path()
user_path = UserPathSerializer.get_path()
router = routers.DefaultRouter()
router.register(r"%s" % user_path, UserViewSet, basename=user_path)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)
