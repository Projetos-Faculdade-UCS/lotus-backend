from rest_framework import viewsets

from lotus.models import Computador, Impressora, Monitor
from lotus.serializers import (
    AtivoTIBaseSerializer,
    ComputadorDetailSerializer,
    ComputadorListSerializer,
    ImpressoraListSerializer,
    MonitorListSerializer,
)

# Create your views here.


class ComputadoresViewSet(viewsets.ModelViewSet):
    """ViewSet de computadores."""

    queryset = Computador.objects.all()

    def get_serializer_class(self) -> AtivoTIBaseSerializer:
        """Retorna a classe de serializer."""
        if self.action == "list":
            return ComputadorListSerializer
        return ComputadorDetailSerializer


class ImpressorasViewSet(viewsets.ModelViewSet):
    """ViewSet de impressoras."""

    queryset = Impressora.objects.all()
    serializer_class = ImpressoraListSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """ViewSet de monitores."""

    queryset = Monitor.objects.all()
    serializer_class = MonitorListSerializer
