from django.urls import path, include
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', view=views.home_view),
    path('api/', include(views.router.urls)),
    path('api/profile-list', views.ProfileList.as_view()),    
    path('api/profile-detail/<pk>/', views.ProfileDetail.as_view(), name='profile-detail'),

]