from django.urls import path

from . import views

urlpatterns = [
	path('', views.sistema, name='sistema'),
	path('usuarios/', views.usuarios, name='usuarios'),
	path('permissoes/', views.permissoes, name='permissoes'),
	path('kpis/', views.kpis, name='kpis'),
	path('relatorios/', views.relatorios, name='relatorios'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
	path('perfil/', views.perfil, name='perfil'),
]