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

# Register your models here.
admin.site.register(Computador)
admin.site.register(Bloco)
admin.site.register(Sala)
admin.site.register(Impressora)
admin.site.register(Monitor)
admin.site.register(LicencaSoftware)
admin.site.register(Programa)
