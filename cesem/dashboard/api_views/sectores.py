from rest_framework import viewsets
from core.models import Sector
from .utils import BasePathSerializer

class SectorPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'sectors'
    
    class Meta:
        model = Sector
        fields = ['name', 'url']
        

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorPathSerializer
