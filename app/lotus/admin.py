from django.contrib import admin

from lotus.models import (
    Bloco,
    Computador,
    ComputadorAllProxy,
    ComputadorValidosProxy,
    Impressora,
    LicencaSoftware,
    Monitor,
    Programa,
    Sala,
)


class ComputadorAdmin(admin.ModelAdmin):
    """Admin de Computador."""

    list_display = ("nome", "patrimonio", "em_uso", "local", "responsavel")
    list_filter = ("em_uso",)
    search_fields = ("nome", "patrimonio", "responsavel")

    def get_queryset(self, _request) -> Computador:
        """Retorna o queryset customizado."""
        return Computador.objects.all()


class ComputadorValidosAdmin(admin.ModelAdmin):
    """Admin de Computadores Validos."""

    list_display = ("nome", "patrimonio", "em_uso", "local", "responsavel")
    list_filter = ("em_uso",)
    search_fields = ("nome", "patrimonio", "responsavel")

    def get_queryset(self, _request) -> Computador:
        """Retorna o queryset customizado."""
        return Computador.validos.all()


# Register your models here.
admin.site.register(ComputadorAllProxy, ComputadorAdmin)
admin.site.register(
    ComputadorValidosProxy,
    ComputadorValidosAdmin,
    name="Computadores Validos",
)
admin.site.register(Bloco)
admin.site.register(Sala)
admin.site.register(Impressora)
admin.site.register(Monitor)
admin.site.register(LicencaSoftware)
admin.site.register(Programa)
