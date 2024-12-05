from __future__ import annotations

from http.client import BAD_REQUEST
from typing import TYPE_CHECKING, cast

from django.db.models import Q
from rest_framework import mixins, views, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from lotus.filters import SalaFilter
from lotus.models import Bloco, Computador, Impressora, Monitor, Sala
from lotus.models.ativos_ti import AtivoTI
from lotus.serializers import (
    AgenteCoreSerializer,
    AgenteHardwareSerializer,
    AgenteProgramasSerializer,
    AtivoTIBaseSerializer,
    BlocoSerializer,
    ComputadorDetailSerializer,
    ComputadorListSerializer,
    ImpressoraDetailSerializer,
    ImpressoraListSerializer,
    MonitorDetailSerializer,
    MonitorListSerializer,
    MovimentacaoSerializer,
    SalaSerializer,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request

    from lotus.serializers.agente import AgenteBaseSerializer


# Create your views here.
class AtivoTIActionsMixin:
    """Mixin com ações comuns a ativos de TI."""

    @action(detail=True, methods=["get"])
    def movimentacoes(self, _request: Request, pk: int) -> Response:
        """Retorna as movimentações de um computador."""
        ativo_ti = self.get_object()
        movimentacoes = ativo_ti.get_historico_movimentacoes()
        serializer = MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class ComputadoresViewSet(viewsets.ModelViewSet, AtivoTIActionsMixin):
    """ViewSet de computadores."""

    queryset = Computador.validos.all()

    def get_queryset(self) -> QuerySet[Computador]:
        """Retorna o queryset de computadores."""
        if self.action in ("update", "partial_update"):
            return Computador.objects.all()
        return super().get_queryset()

    def get_serializer_class(self) -> type[AtivoTIBaseSerializer]:
        """Retorna a classe de serializer."""
        if self.action == "list":
            return ComputadorListSerializer
        return ComputadorDetailSerializer

    @action(detail=False, methods=["get"])
    def computadores_in_sala(
        self,
        _request: Request,
        _bloco_id: int,
        sala_id: int,
    ) -> Response:
        """Retorna os computadores de uma sala."""
        computadores = Computador.validos.filter(local=sala_id)
        serializer = ComputadorListSerializer(computadores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="pendentes-validacao")
    def pendentes_validacao(self, _request: Request) -> Response:
        """Retorna os computadores pendentes de validação."""
        computadores = Computador.objects.filter(valido=False)
        serializer = ComputadorListSerializer(computadores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def validar(self, request: Request) -> Response:
        """Valida os computadores."""
        if not request.data:
            return Response(
                {"message": "Nenhum computador selecionado."},
                status=BAD_REQUEST,
            )
        ids = cast(dict, request.data).get("ids")
        if not ids:
            return Response(
                {"message": "Nenhum computador selecionado."},
                status=BAD_REQUEST,
            )
        computadores = Computador.objects.filter(pk__in=ids)
        qtd = computadores.update(valido=True)
        print(qtd)
        return Response({"message": "Computadores validados."})

    @action(detail=True, methods=["get"])
    def relacionados(self, _request: Request, pk: int) -> Response:
        """Retorna os ativos relacionados a um computador."""
        computador = Computador.objects.get(pk=pk)
        ativos = computador.ativos_relacionados.all()
        serializer = AtivoTIBaseSerializer(ativos, many=True)
        return Response(serializer.data)


class ImpressorasViewSet(viewsets.ModelViewSet, AtivoTIActionsMixin):
    """ViewSet de impressoras."""

    queryset = Impressora.objects.all()

    def get_serializer_class(self) -> type[AtivoTIBaseSerializer]:
        """Retorna a classe de serializer."""
        if self.action == "list":
            return ImpressoraListSerializer
        return ImpressoraDetailSerializer


class MonitorViewSet(viewsets.ModelViewSet, AtivoTIActionsMixin):
    """ViewSet de monitores."""

    queryset = Monitor.objects.all()

    def get_serializer_class(self) -> type[AtivoTIBaseSerializer]:
        """Retorna a classe de serializer."""
        if self.action == "list":
            return MonitorListSerializer
        return MonitorDetailSerializer


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
    def salas_in_bloco(self, _request: Request, bloco_id: int) -> Response:
        """Retorna as salas de um bloco."""
        salas = Sala.objects.filter(bloco=bloco_id)
        serializer = SalaSerializer(salas, many=True)
        return Response(serializer.data)


class AgenteApiView(views.APIView):
    """View que retorna o agente de monitoramento."""

    def get_serializer_class(self, tipo: str) -> type[AgenteBaseSerializer] | None:
        """Retorna a classe de serializer."""
        if tipo == "core":
            return AgenteCoreSerializer
        if tipo == "hardware":
            return AgenteHardwareSerializer
        if tipo == "programs":
            return AgenteProgramasSerializer
        return None

    def post(self, request: Request, tipo: str) -> Response:
        """Retorna o agente de monitoramento."""
        serializer_class = self.get_serializer_class(tipo)
        if serializer_class is None:
            return Response(status=404)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DashboardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View que retorna o dashboard."""

    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    def list(self, _request: Request, *_args: list, **_kwargs: dict) -> Response:
        """Retorna o dashboard."""
        computadores = Computador.validos.all()
        computadores_automaticos = computadores.filter(automatico=True)
        computadores_manuais = computadores.filter(automatico=False)
        impressoras = Impressora.objects.all()
        monitores = Monitor.objects.all()
        salas = Sala.objects.all()
        # bloco_id, computador_set, id, impressora_set, monitor_set
        salas_com_ativos = Sala.objects.filter(
            Q(ativoti_set__in=computadores)
            | Q(ativoti_set__in=impressoras)
            | Q(ativoti_set__in=monitores),
        ).distinct()
        salas_vazias = salas.exclude(pk__in=salas_com_ativos)
        computadores_count = computadores.count()
        impressoras_count = impressoras.count()
        monitores_count = monitores.count()
        return Response(
            {
                "ativos": computadores_count + impressoras_count + monitores_count,
                "computadores": {
                    "total": computadores_count,
                    "automaticos": computadores_automaticos.count(),
                    "manuais": computadores_manuais.count(),
                },
                "impressoras": impressoras_count,
                "monitores": monitores_count,
                "salas": {
                    "total": salas.count(),
                    "com_ativos": salas_com_ativos.count(),
                    "vazias": salas_vazias.count(),
                },
            },
        )
