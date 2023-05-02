from rest_framework import viewsets
from core.models import Community
from .utils import BasePathSerializer

class CommunityPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'communities'
    
    class Meta:
        model = Community
        fields = ['name', 'url']
        

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunityPathSerializer
