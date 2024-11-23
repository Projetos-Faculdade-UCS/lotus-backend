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
            "tipo",
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

    class Meta(AtivoTIBaseSerializer.Meta):
        """Meta informações do serializer."""

        model = Computador


class ComputadorDetailSerializer(AtivoTIBaseSerializer):
    """Serializer de detalhes de computadores."""

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


class AgenteBaseSerializer(serializers.ModelSerializer):
    """Base serializer para informações vindas do agente."""

    class Meta:
        """Meta informações do serializer."""

        model = None
        fields: ClassVar[list[str]] = []

    def create(self, validated_data: dict) -> None:
        """Cria um objeto com as informações do agente."""
        patrimono = validated_data.pop("patrimonio")
        obj, _ = Computador.objects.update_or_create(
            patrimonio=patrimono,
            defaults=validated_data,
        )
        return obj


class AgenteCoreSerializer(AgenteBaseSerializer):
    """Serializer de criação p/ computadores com iformações core vindas do agente."""

    patrimonio = serializers.CharField(required=True)
    hostname = serializers.CharField(source="nome", required=True)
    username = serializers.CharField(
        source="ultimo_usuario_logado",
        required=True,
    )

    class Meta:
        """Meta informações do serializer."""

        model = Computador
        fields: ClassVar[list[str]] = [
            "patrimonio",
            "hostname",
            "username",
        ]


class AgenteHardwareSerializer(AgenteBaseSerializer):
    """Serializer de criação p/ computadores com infos de hardware vindas do agente."""

    patrimonio = serializers.CharField(required=True)
    tamanho_hd = serializers.CharField(required=True)
    tamanho_ram = serializers.CharField(required=True)
    modelo_cpu = serializers.CharField(required=True)
    placa_mae = serializers.CharField(required=True)
    sistema_operacional = serializers.CharField(required=True)

    class Meta:
        """Meta informações do serializer."""

        model = Computador
        fields: ClassVar[list[str]] = [
            "patrimonio",
            "tamanho_hd",
            "tamanho_ram",
            "modelo_cpu",
            "placa_mae",
            "sistema_operacional",
        ]

    def to_internal_value(self, data: dict) -> dict:
        """Transforma o JSON bruto no formato necessário para o serializer."""
        internal_data = {}

        internal_data["patrimonio"] = self.process_patrimonio(data)
        internal_data["tamanho_hd"] = self.process_tamanho_hd(data)
        internal_data["tamanho_ram"] = self.process_tamanho_ram(data)
        internal_data["modelo_cpu"] = self.process_modelo_cpu(data)
        internal_data["placa_mae"] = self.process_placa_mae(data)
        internal_data["sistema_operacional"] = self.process_sistema_operacional(data)
        return super().to_internal_value(internal_data)

    def process_patrimonio(self, data: dict) -> str:
        """Processa o patrimônio."""
        return data["patrimonio"]

    def process_tamanho_hd(self, data: dict) -> str:
        """Processa o tamanho do HD."""
        result = ""
        if "disks" not in data:
            msg = "Campo 'disks' não encontrado."
            raise serializers.ValidationError(msg)
        for disk in data["disks"]:
            result += f"{disk['_size']}Gb ({disk['_model']});"
        return result[:-1]

    def process_tamanho_ram(self, data: dict) -> str:
        """Processa o tamanho da RAM."""
        result = ""
        if "ram" not in data:
            msg = "Campo 'ram' não encontrado."
            raise serializers.ValidationError(msg)
        for ram in data["ram"]:
            result += f"{ram['_capacity']}Gb + "
        return result[:-3]

    def process_modelo_cpu(self, data: dict) -> str:
        """Processa o modelo da CPU."""
        result = ""
        if "processors" not in data:
            msg = "Campo 'processors' não encontrado."
            raise serializers.ValidationError(msg)
        for processor in data["processors"]:
            result += f"{processor['_name']} + "
        return result[:-3]

    def process_placa_mae(self, data: dict) -> str:
        """Processa o modelo da placa mãe."""
        if "motherboard" not in data:
            msg = "Campo 'motherboard' não encontrado."
            raise serializers.ValidationError(msg)
        return data["motherboard"]["_product"]

    def process_sistema_operacional(self, data: dict) -> str:
        """Processa o sistema operacional."""
        if "os" not in data:
            msg = "Campo 'os' não encontrado."
            raise serializers.ValidationError(msg)
        return data["os"]


class AgenteProgramasSerializer(AgenteBaseSerializer):
    """Serializer de criação p/ programas com infos vindas do agente."""

    patrimonio = serializers.CharField(required=True)
    programs = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        write_only=True,
    )

    class Meta:
        """Meta informações do serializer."""

        model = Programa
        fields: ClassVar[list[str]] = ["patrimonio", "programs"]

    def save_programs(self, computador: Computador, programs: list[dict]) -> None:
        """Salva os programas associados ao computador."""
        for programa in programs:
            Programa.objects.get_or_create(
                computador=computador,
                nome=programa["name"],
                versao=programa["version"],
            )

    def create(self, validated_data: dict) -> None:
        """Cria um objeto com as informações do agente."""
        patrimonio = validated_data.pop("patrimonio")
        programas = validated_data.pop("programs")

        computador = super().create({"patrimonio": patrimonio}, **validated_data)

        self.save_programs(computador, programas)
        return computador
