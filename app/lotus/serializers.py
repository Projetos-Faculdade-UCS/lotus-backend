from __future__ import annotations

from typing import ClassVar

from rest_framework import serializers

from lotus.models import (
    AtivoTI,
    Bloco,
    Computador,
    Impressora,
    LicencaSoftware,
    Monitor,
    Programa,
    Sala,
)


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


class ProgramaSerializer(serializers.ModelSerializer):
    """Serializer de programas."""

    class Meta:
        """Meta informações do serializer."""

        model = Programa
        exclude: ClassVar[list[str]] = ["computador"]


class LicencaSoftwareSerializer(serializers.ModelSerializer):
    """Serializer de licenças de software."""

    class Meta:
        """Meta informações do serializer."""

        model = LicencaSoftware
        exclude: ClassVar[list[str]] = ["computador"]


class AtivoTIBaseSerializer(serializers.ModelSerializer):
    """Base serializer para ativos de TI."""

    sala = SalaSerializer(source="local")
    relacionamentos = serializers.SerializerMethodField()

    class Meta:
        """Meta informações do serializer."""

        model = None
        fields: ClassVar[list[str]] = [
            "id",
            "nome",
            "fabricante",
            "numero_serie",
            "em_uso",
            "descricao",
            "automatico",
            "patrimonio",
            "sala",
            "relacionamentos",
            "responsavel",
            "ultima_atualizacao",
        ]

    def get_relacionamentos(self, obj: AtivoTI) -> int:
        """Retorna a quantidade de relacionamentos."""
        return obj.ativos_relacionados.count()


class ComputadorListSerializer(AtivoTIBaseSerializer):
    """Serializer de listagem de computadores."""

    tipo = serializers.CharField(default="Computador")

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Computador
        fields: ClassVar[list[str]] = [
            *AtivoTIBaseSerializer.Meta.fields,
            "tipo",
        ]


class ComputadorDetailSerializer(AtivoTIBaseSerializer):
    """Serializer de detalhes de computadores."""

    tipo = serializers.CharField(default="Computador")
    hd = serializers.CharField(source="tamanho_hd")
    criticidade = serializers.CharField(source="criticidade_dados")
    programas = ProgramaSerializer(many=True, read_only=True, source="programa_set")
    licencas = LicencaSoftwareSerializer(
        many=True,
        read_only=True,
        source="licencasoftware_set",
    )

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Computador
        fields: ClassVar[list[str]] = [
            *AtivoTIBaseSerializer.Meta.fields,
            "tipo",
            "tamanho_ram",
            "modelo_cpu",
            "placa_mae",
            "hd",
            "sistema_operacional",
            "criticidade",
            "programas",
            "licencas",
            "valido",
            "ultimo_usuario_logado",
        ]


class ImpressoraListSerializer(AtivoTIBaseSerializer):
    """Serializer de listagem de impressoras."""

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Impressora


class MonitorListSerializer(AtivoTIBaseSerializer):
    """Serializer de listagem de monitores."""

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Monitor
