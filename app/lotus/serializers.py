from __future__ import annotations

from typing import ClassVar

from rest_framework import serializers

from lotus.models import Bloco, Computador, Sala


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


class ComputadorListSerializer(serializers.ModelSerializer):
    """Serializer de listagem de computadores."""

    sala = SalaSerializer(source="local")
    relacionamentos = serializers.SerializerMethodField()

    class Meta:
        """Meta informações do serializer."""

        model = Computador
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

    def get_relacionamentos(self, obj: Computador) -> int:
        """Retorna a quantidade de relacionamentos."""
        return obj.ativos_relacionados.count()
