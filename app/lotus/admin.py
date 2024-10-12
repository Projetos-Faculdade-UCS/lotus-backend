from django.contrib import admin

from lotus.models import Bloco, Computador, Sala

# Register your models here.
admin.site.register(Computador)
admin.site.register(Bloco)
admin.site.register(Sala)
