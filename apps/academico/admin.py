from django.contrib import admin

from .models import Exames, Frequencia, Horarios, Notas


admin.site.register(Horarios)
admin.site.register(Frequencia)
admin.site.register(Exames)
admin.site.register(Notas)