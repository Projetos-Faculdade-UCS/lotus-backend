from typing import ClassVar

from rest_framework import serializers

from lotus.models import LicencaSoftware, Programa


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
