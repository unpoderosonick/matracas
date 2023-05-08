from django.urls import path, include
from . import views
from .report_views import animal_view

app_name = 'dashboard'

urls_reports = [
    path(r'animals/', view=animal_view.report, name='reports_animals')
]

urlpatterns = [
    path('', view=views.home_view),
    path(r'api/', include(views.router.urls)),
    path(r'reports/', include(urls_reports)),
]