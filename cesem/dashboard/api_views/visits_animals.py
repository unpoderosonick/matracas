from core.models import VisitAnimal
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitAnimalPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source='zone')
    up_responsable = serializers.StringRelatedField(many=False)
    up_miembro = serializers.StringRelatedField(many=False, source='up_member')
    cesem_especialista = serializers.StringRelatedField(many=False, source='employ_specialist')
    cesem_responsable = serializers.StringRelatedField(many=False, source='employ_responsable')
    actividad = serializers.StringRelatedField(many=False, source='activity')
    enfermedad_observación = serializers.StringRelatedField(many=False, source='sickness_observation')
    diagnostico = serializers.StringRelatedField(many=False, source='diagnostic')

    @staticmethod
    def get_path():
        return 'visits-animals'
    
    class Meta:
        model = VisitAnimal
        fields = ['visited_at', 'zona', 'up_responsable', 'up_miembro', 'cesem_especialista', 'cesem_responsable', 'actividad', 'enfermedad_observación', 'diagnostico', 'cattle', 'sheep', 'alpacas', 'llamas', 'canes', 'url']


class VisitAnimalViewSet(viewsets.ModelViewSet):

    queryset = VisitAnimal.objects\
        .select_related('zone')\
        .select_related('up_responsable','up_member','employ_specialist','employ_responsable')\
        .select_related('activity')\
        .select_related('sickness_observation')\
        .select_related('diagnostic')\
        .all()
    serializer_class = VisitAnimalPathSerializer

    filterset_fields = {
        'zone__name': ['contains'],
        'up_responsable__name': ['contains'],
        'up_member__name': ['contains'],
        'employ_specialist__name': ['contains'],
        'employ_responsable__name': ['contains'],
        'activity__name': ['contains'],
        'sickness_observation__name': ['contains'],
        'diagnostic__name': ['contains'],
    }
