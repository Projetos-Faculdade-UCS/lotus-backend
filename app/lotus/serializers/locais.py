from typing import ClassVar

from rest_framework import serializers

from lotus.models import Bloco, Sala, Movimentacao


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


class MovimentacaoSerializer(serializers.ModelSerializer):
    """Serializer de movimentações."""

    sala_atual = SalaSerializer()
    data = serializers.DateTimeField()
    motivo = serializers.CharField()

    class Meta:
        """Meta informações do serializer."""

        model = Movimentacao
        fields: ClassVar = ["id", "sala_atual", "data", "motivo"]
