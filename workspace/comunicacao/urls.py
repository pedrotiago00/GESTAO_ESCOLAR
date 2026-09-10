from django.urls import path

from . import views

urlpatterns = [
	path('', views.comunicacao, name='comunicacao'),
    path('avisos/', views.avisos, name='avisos'),
    path('eventos/', views.eventos, name='eventos'),
    path('reunioes/', views.reunioes, name='reunioes'),
    path('reclamacoes/', views.reclamacoes, name='reclamacoes'),
]