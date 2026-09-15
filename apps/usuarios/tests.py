from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Escola, PerfilUsuario


class EscolaUsuarioTestCase(TestCase):
    def test_criar_usuario_com_escola(self):
        escola = Escola.objects.create(nome='Escola Municipal Teste', cidade='São Paulo')
        usuario = get_user_model().objects.create_user(
            username='usuario_teste',
            email='teste@email.com',
            password='123456',
        )

        perfil = PerfilUsuario.objects.create(usuario=usuario, escola=escola)

        self.assertEqual(perfil.escola, escola)
        self.assertEqual(usuario.perfil.escola, escola)
