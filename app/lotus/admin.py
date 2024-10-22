from django.contrib import admin

from lotus.models import Bloco, Computador, Impressora, Monitor, Sala

# Register your models here.
admin.site.register(Computador)
admin.site.register(Bloco)
admin.site.register(Sala)
admin.site.register(Impressora)
admin.site.register(Monitor)
