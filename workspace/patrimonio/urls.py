from django.urls import path

from . import views

urlpatterns = [
	path('', views.patrimonio, name='patrimonio'),
	path('ativos/', views.ativos, name='ativos'),
	path('manutencao/', views.manutencao, name='manutencao'),
	path('inventario/', views.inventario, name='inventario'),
	path('documentos/', views.documentos, name='documentos'),
]