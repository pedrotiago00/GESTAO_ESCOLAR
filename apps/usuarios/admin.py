from django.contrib import admin

from .models import Escola, PerfilUsuario

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'ativo')
    list_filter = ('ativo', 'cidade')
    search_fields = ('nome', 'cidade')
    ordering = ('nome',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'escola')
    list_filter = ('escola',)
    search_fields = ('usuario__username', 'escola__nome')
    raw_id_fields = ('usuario',)