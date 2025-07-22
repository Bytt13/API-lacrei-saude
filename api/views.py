from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

# Esta é a ação customizada para buscar consultas de um profissional
@action(detail=False, methods = ['get'], url_path='por-profisisonal/(?P<profissional_id>[0-9a-f-]+)')
def por_profissional(self, request, profissional_id=None):
    consultas = self.get_queryset().filter(profissional_id = profissional_id)
    serializer = self.get_serializer(consultas, many=True)
    return Response(serializer.data)