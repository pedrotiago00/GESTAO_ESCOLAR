from django.urls import path

from . import views

urlpatterns = [
	path('', views.cadastros, name='cadastros'),
    path('turmas/', views.turmas, name='turmas'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('estudantes/', views.estudantes, name='estudantes'),
    path('professores/', views.professores, name='professores'),
    path('pais/', views.pais, name='pais'),
]