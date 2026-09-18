from django.contrib import admin

from .models import Escola, Funcao, PerfilUsuario


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'ativo')
    list_filter = ('ativo', 'cidade')
    search_fields = ('nome', 'cidade')
    ordering = ('nome',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'escola', 'funcao')
    list_filter = ('escola', 'funcao')
    search_fields = ('usuario__username', 'escola__nome')
    raw_id_fields = ('usuario',)