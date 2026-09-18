from django.contrib.auth.models import User
from django.db import models

class Escola(models.Model):
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=120, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT, related_name='usuarios')
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT, related_name='usuarios')

    def __str__(self):
        return f'{self.usuario.username} - {self.escola.nome} - {self.funcao.nome}'