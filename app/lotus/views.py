from django.shortcuts import render
from rest_framework import viewsets

from lotus.models import Computador, Impressora, Monitor
from lotus.serializers import (
    ComputadorListSerializer,
    ImpressoraListSerializer,
    MonitorListSerializer,
)

# Create your views here.


class ComputadoresViewSet(viewsets.ModelViewSet):
    """ViewSet de computadores."""

    queryset = Computador.objects.all()
    serializer_class = ComputadorListSerializer


class ImpressorasViewSet(viewsets.ModelViewSet):
    """ViewSet de impressoras."""

    queryset = Impressora.objects.all()
    serializer_class = ImpressoraListSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """ViewSet de monitores."""

    queryset = Monitor.objects.all()
    serializer_class = MonitorListSerializer
