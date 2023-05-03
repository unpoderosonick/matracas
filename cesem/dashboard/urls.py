from django.urls import path, include
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', view=views.home_view),
    path('api/', include(views.router.urls)),

]