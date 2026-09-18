from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroForms, LoginForms
from .models import Escola, Funcao, PerfilUsuario

class AutenticacaoTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Autenticação', cidade='Belo Horizonte')
        self.funcao_diretor = Funcao.objects.create(nome='Diretor')
        self.funcao_professor = Funcao.objects.create(nome='Professor')
        self.usuario = get_user_model().objects.create_user(
            username='diretor_user',
            email='diretor@email.com',
            password='123456',
        )
        PerfilUsuario.objects.create(
            usuario=self.usuario,
            escola=self.escola,
            funcao=self.funcao_diretor,
        )

        self.usuario_professor = get_user_model().objects.create_user(
            username='professor_user',
            email='professor@email.com',
            password='123456',
        )
        PerfilUsuario.objects.create(
            usuario=self.usuario_professor,
            escola=self.escola,
            funcao=self.funcao_professor,
        )

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('login'), {'username': 'diretor_user', 'password': '123456'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_com_senha_invalida(self):
        response = self.client.post(reverse('login'), {'username': 'diretor_user', 'password': 'senha_errada'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha inválidos.')

    def test_acesso_sem_login_redireciona_para_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/?next=/dashboard/')

    def test_usuario_sem_permissao_recebe_403(self):
        self.client.force_login(self.usuario_professor)

        response = self.client.get('/cadastros/turmas/')

        self.assertEqual(response.status_code, 403)

class EscolaModelTestCase(TestCase):
    def test_criar_escola(self):
        escola = Escola.objects.create(nome='Escola Municipal Teste', cidade='São Paulo')

        self.assertEqual(escola.nome, 'Escola Municipal Teste')
        self.assertEqual(escola.cidade, 'São Paulo')
        self.assertTrue(escola.ativo)

    def test_str_da_escola(self):
        escola = Escola.objects.create(nome='Escola da Vila', cidade='Rio de Janeiro')

        self.assertEqual(str(escola), 'Escola da Vila')

class FuncaoModelTestCase(TestCase):
    def test_criar_funcao(self):
        funcao = Funcao.objects.create(nome='Professor', descricao='Ensina aulas teóricas e práticas')

        self.assertEqual(funcao.nome, 'Professor')
        self.assertEqual(funcao.descricao, 'Ensina aulas teóricas e práticas')

    def test_str_da_funcao(self):
        funcao = Funcao.objects.create(nome='Coordenador', descricao='Coordena equipe pedagógica')

        self.assertEqual(str(funcao), 'Coordenador')

class PerfilUsuarioModelTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Municipal Teste', cidade='São Paulo')
        self.funcao = Funcao.objects.create(nome='Professor', descricao='Professor do ensino fundamental')
        self.usuario = get_user_model().objects.create_user(
            username='usuario_teste',
            email='teste@email.com',
            password='123456',
        )

    def test_criar_perfil_usuario(self):
        perfil = PerfilUsuario.objects.create(usuario=self.usuario, escola=self.escola, funcao=self.funcao)

        self.assertEqual(perfil.usuario, self.usuario)
        self.assertEqual(perfil.escola, self.escola)
        self.assertEqual(perfil.funcao, self.funcao)
        self.assertEqual(self.usuario.perfil, perfil)

    def test_str_do_perfil_usuario(self):
        perfil = PerfilUsuario.objects.create(usuario=self.usuario, escola=self.escola, funcao=self.funcao)

        self.assertEqual(str(perfil), 'usuario_teste - Escola Municipal Teste - Professor')

class LoginFormsTestCase(TestCase):
    def test_login_form_valido(self):
        form = LoginForms(data={'username': 'usuario_teste', 'password': '123456'})

        self.assertTrue(form.is_valid())

    def test_login_form_invalido_sem_campos(self):
        form = LoginForms(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class CadastroFormsTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Nova', cidade='Campinas', ativo=True)
        self.funcao = Funcao.objects.create(nome='Diretor', descricao='Direção escolar')

    def test_cadastro_form_valido(self):
        form = CadastroForms(data={
            'username': 'novo_usuario',
            'email': 'novo@email.com',
            'escola': self.escola.pk,
            'funcao': self.funcao.pk,
            'password': 'senha123',
            'password_confirm': 'senha123',
        })

        self.assertTrue(form.is_valid())

    def test_cadastro_form_invalido_quando_senhas_diferem(self):
        form = CadastroForms(data={
            'username': 'novo_usuario',
            'email': 'novo@email.com',
            'escola': self.escola.pk,
            'funcao': self.funcao.pk,
            'password': 'senha123',
            'password_confirm': 'outra_senha',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)