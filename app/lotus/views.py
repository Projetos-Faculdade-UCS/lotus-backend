from django.shortcuts import render
from rest_framework import viewsets

from lotus.models import Computador
from lotus.serializers import ComputadorListSerializer, ImpressoraListSerializer

# Create your views here.


class ComputadoresViewSet(viewsets.ModelViewSet):
    """ViewSet de computadores."""

    queryset = Computador.objects.all()
    serializer_class = ComputadorListSerializer


class ImpressorasViewSet(viewsets.ModelViewSet):
    """ViewSet de impressoras."""

    queryset = Computador.objects.all()
    serializer_class = ImpressoraListSerializer
