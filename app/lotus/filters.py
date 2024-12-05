from typing import ClassVar

from django.db import models
from django.db.models import Q
from django_filters import CharFilter, FilterSet

from lotus.models import Computador, Impressora, Monitor, Sala


class SalaFilter(FilterSet):
    """Filtro para salas de aula.

    Filtro descritivo aceita nome da sala ou nome do bloco
    """

    class Meta:
        """Meta informações do filtro."""

        fields = ["qs"]
        model = Sala

    qs = CharFilter(
        method="filter_qs",
        label="Filtro descritivo",
    )

    def filter_qs(
        self,
        queryset: models.QuerySet,
        name: str,
        value: str,
    ) -> models.QuerySet:
        """Filtro descritivo."""
        qs_filter = Q()
        for palavra in value.split():
            qs_filter &= Q(
                Q(nome__icontains=palavra) | Q(bloco__nome__icontains=palavra),
            )
        return queryset.filter(qs_filter)


class AtivoFilter(FilterSet):
    """Filtro para ativos.

    Filtro descritivo aceita nome, número de patrimônio, nome da sala ou nome do bloco.
    """

    class Meta:
        """Meta informações do filtro."""

        fields: ClassVar[list] = ["q", "patrimonio"]

    q = CharFilter(
        method="filter_query",
        label="Filtro por nome, sala ou bloco",
    )

    patrimonio = CharFilter(
        field_name="patrimonio",
        label="Filtro por número de patrimônio",
        method="filter_patrimonio",
    )

    def filter_query(
        self,
        queryset: models.QuerySet,
        name: str,
        value: str,
    ) -> models.QuerySet:
        """Filtro descritivo."""
        query_filter = Q()
        for palavra in value.split():
            query_filter &= Q(
                Q(nome__icontains=palavra)
                | Q(local__nome__exact=palavra)
                | Q(local__bloco__nome__icontains=palavra),
            )
        return queryset.filter(query_filter)

    def filter_patrimonio(
        self,
        queryset: models.QuerySet,
        name: str,
        value: str,
    ) -> models.QuerySet:
        """Filtro por número de patrimônio."""
        if not value.isdigit():
            return queryset.none()
        return queryset.filter(patrimonio=value)
