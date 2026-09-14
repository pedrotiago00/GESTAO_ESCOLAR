from django.urls import path

from . import views

urlpatterns = [
	path('', views.academico, name='academico'),
    path('horarios/', views.horarios, name='horarios'),
    path('frequencia/', views.frequencia, name='frequencia'),
    path('exames/', views.exames, name='exames'),
    path('notas/', views.notas, name='notas'),
    path('planejamento/', views.planejamento, name='planejamento'),
    path('diario_de_classe/', views.diario_de_classe, name='diario_de_classe'),
    ]