from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from lotus.models import Bloco, Computador, Impressora, Monitor, Sala
from lotus.serializers import (
    AtivoTIBaseSerializer,
    BlocoSerializer,
    ComputadorDetailSerializer,
    ComputadorListSerializer,
    ImpressoraListSerializer,
    MonitorListSerializer,
    SalaSerializer,
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

    @action(detail=False, methods=["get"])
    def computadores_in_sala(
        self,
        _request: HttpRequest,
        _bloco_id: int,
        sala_id: int,
    ) -> Response:
        """Retorna os computadores de uma sala."""
        computadores = Computador.objects.filter(local=sala_id)
        serializer = ComputadorListSerializer(computadores, many=True)
        return Response(serializer.data)


class ImpressorasViewSet(viewsets.ModelViewSet):
    """ViewSet de impressoras."""

    queryset = Impressora.objects.all()
    serializer_class = ImpressoraListSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """ViewSet de monitores."""

    queryset = Monitor.objects.all()
    serializer_class = MonitorListSerializer


class BlocosViewSet(viewsets.ModelViewSet):
    """ViewSet de blocos."""

    queryset = Bloco.objects.all()
    serializer_class = BlocoSerializer


class SalaViewSet(viewsets.ModelViewSet):
    """ViewSet de salas."""

    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    @action(detail=False, methods=["get"])
    def salas_in_bloco(self, _request: HttpRequest, bloco_id: int) -> Response:
        """Retorna as salas de um bloco."""
        salas = Sala.objects.filter(bloco=bloco_id)
        serializer = SalaSerializer(salas, many=True)
        return Response(serializer.data)
