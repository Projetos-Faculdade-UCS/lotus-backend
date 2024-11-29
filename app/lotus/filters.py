from django.db import models
from django.db.models import Q
from django_filters import CharFilter, FilterSet

from lotus.models import Sala


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
