from django.contrib import admin
from .models import Professores, Turmas, Estudantes, Responsaveis

admin.site.register(Professores)
admin.site.register(Turmas)
admin.site.register(Estudantes)
admin.site.register(Responsaveis)