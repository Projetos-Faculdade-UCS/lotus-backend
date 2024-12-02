from rest_framework import mixins, views, viewsets
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from lotus.filters import SalaFilter
from lotus.models import Bloco, Computador, Impressora, Monitor, Sala
from lotus.serializers import (
    AgenteCoreSerializer,
    AgenteHardwareSerializer,
    AgenteProgramasSerializer,
    AtivoTIBaseSerializer,
    BlocoSerializer,
    ComputadorDetailSerializer,
    ComputadorListSerializer,
    ImpressoraListSerializer,
    MonitorListSerializer,
    MovimentacaoSerializer,
    SalaSerializer,
)

# Create your views here.


class ComputadoresViewSet(viewsets.ModelViewSet):
    """ViewSet de computadores."""

    queryset = Computador.validos.all()

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
        computadores = Computador.validos.filter(local=sala_id)
        serializer = ComputadorListSerializer(computadores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_movimentacoes(self, _request: HttpRequest, pk: int) -> Response:
        """Retorna as movimentações de um computador."""
        computador = self.get_object()
        movimentacoes = computador.get_historico_movimentacoes()
        serializer = MovimentacaoSerializer(movimentacoes, many=True)
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
    filterset_class = SalaFilter

    @action(detail=False, methods=["get"])
    def salas_in_bloco(self, _request: HttpRequest, bloco_id: int) -> Response:
        """Retorna as salas de um bloco."""
        salas = Sala.objects.filter(bloco=bloco_id)
        serializer = SalaSerializer(salas, many=True)
        return Response(serializer.data)


class AgenteApiView(views.APIView):
    """View que retorna o agente de monitoramento."""

    def get_serializer_class(self, tipo: str) -> None:
        """Retorna a classe de serializer."""
        if tipo == "core":
            return AgenteCoreSerializer
        if tipo == "hardware":
            return AgenteHardwareSerializer
        if tipo == "programs":
            return AgenteProgramasSerializer
        return None

    def post(self, request: HttpRequest, tipo: str) -> Response:
        """Retorna o agente de monitoramento."""
        serializer_class = self.get_serializer_class(tipo)
        if serializer_class is None:
            return Response(status=404)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
