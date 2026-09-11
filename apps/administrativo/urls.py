from django.urls import path

from . import views

urlpatterns = [
	path('', views.administrativo, name='administrativo'),
	path('admissoes/', views.admissoes, name='admissoes'),
	path('condutas/', views.condutas, name='condutas'),
	path('extracurriculares/', views.extracurriculares, name='extracurriculares'),
	path('substitutos/', views.substitutos, name='substitutos'),
]