from rest_framework import viewsets
from core.models import Activity
from .utils import BasePathSerializer

class ActivityPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'activities'
    
    class Meta:
        model = Activity
        fields = ['name', 'url']
        

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityPathSerializer
