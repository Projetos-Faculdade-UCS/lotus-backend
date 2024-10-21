from __future__ import annotations

from typing import ClassVar

from rest_framework import serializers

from lotus.models import AtivoTI, Bloco, Computador, Impressora, Sala


class BlocoSerializer(serializers.ModelSerializer):
    """Serializer de blocos."""

    class Meta:
        """Meta informações do serializer."""

        model = Bloco
        fields = "__all__"


class SalaSerializer(serializers.ModelSerializer):
    """Serializer de salas."""

    bloco = BlocoSerializer()

    class Meta:
        """Meta informações do serializer."""

        model = Sala
        fields: ClassVar[list[str]] = ["id", "nome", "bloco"]


class AtivoTIBaseSerializer(serializers.ModelSerializer):
    """Base serializer para ativos de TI."""

    sala = SalaSerializer(source="local")
    relacionamentos = serializers.SerializerMethodField()

    class Meta:
        """Meta informações do serializer."""

        model = None
        fields: ClassVar[list[str]] = [
            "nome",
            "fabricante",
            "numero_serie",
            "em_uso",
            "descricao",
            "automatico",
            "patrimonio",
            "sala",
            "relacionamentos",
        ]

    def get_relacionamentos(self, obj: AtivoTI) -> int:
        """Retorna a quantidade de relacionamentos."""
        return obj.ativos_relacionados.count()


class ComputadorListSerializer(AtivoTIBaseSerializer):
    """Serializer de listagem de computadores."""

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Computador


class ImpressoraListSerializer(AtivoTIBaseSerializer):
    """Serializer de listagem de impressoras."""

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Impressora
