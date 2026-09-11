from django.urls import path

from . import views

urlpatterns = [
	path('', views.financeiro, name='financeiro'),
	path('taxas/', views.taxas, name='taxas'),
	path('cobrancas/', views.cobrancas, name='cobrancas'),
	path('atrasos/', views.atrasos, name='atrasos'),
	path('resumo/', views.resumo, name='resumo'),
]