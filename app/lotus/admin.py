from django.contrib import admin

from lotus.models import (
    Bloco,
    Computador,
    Impressora,
    LicencaSoftware,
    Monitor,
    Programa,
    Sala,
)
from lotus.models.proxys import ComputadorAll, ComputadorCompletos


class ComputadorAdmin(admin.ModelAdmin):
    """Admin de Computador."""

    list_display = ("nome", "numero_serie", "em_uso", "local", "responsavel")
    list_filter = ("em_uso",)
    search_fields = ("nome", "numero_serie", "responsavel")

    def get_queryset(self, _request) -> Computador:
        """Retorna o queryset customizado."""
        return Computador.objects.all()


class ComputadorCompletosAdmin(admin.ModelAdmin):
    """Admin de Computadores Completos."""

    list_display = ("nome", "numero_serie", "em_uso", "local", "responsavel")
    list_filter = ("em_uso",)
    search_fields = ("nome", "numero_serie", "responsavel")

    def get_queryset(self, _request) -> Computador:
        """Retorna o queryset customizado."""
        return Computador.completos.all()


# Register your models here.
admin.site.register(ComputadorAll, ComputadorAdmin)
admin.site.register(
    ComputadorCompletos,
    ComputadorCompletosAdmin,
    name="Computadores Completos",
)
admin.site.register(Bloco)
admin.site.register(Sala)
admin.site.register(Impressora)
admin.site.register(Monitor)
admin.site.register(LicencaSoftware)
admin.site.register(Programa)
