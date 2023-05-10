from rest_framework import viewsets, serializers
from core.models import ProductionUnit
from .utils import BasePathSerializer

class ProductionUnitPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source='zone')
    comunidad = serializers.StringRelatedField(many=False, source='community')
    sector = serializers.StringRelatedField(many=False)
    responsable = serializers.StringRelatedField(many=False, source='person_responsable')
    miembro = serializers.StringRelatedField(many=False, source='person_member')
    tipologia = serializers.StringRelatedField(many=False, source='tipology')
    es_pilot = serializers.StringRelatedField(many=False, source='is_pilot')
       
    @staticmethod
    def get_path():
        return 'production_units'
    
    class Meta:
        model = ProductionUnit
        fields = ('zona', 'comunidad', 'sector', 'responsable', 'miembro', 'tipologia', 'es_pilot', 'url')        

class ProductionUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductionUnit.objects.all()
    serializer_class = ProductionUnitPathSerializer
    filterset_fields = {
        'zone__name': ['contains']
    }
