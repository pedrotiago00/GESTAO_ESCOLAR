from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.academico.models import Exames, Frequencia, Notas
from apps.cadastros.models import Disciplinas, Estudantes, Professores, Responsaveis, Turmas
from apps.usuarios.models import Escola, Funcao, PerfilUsuario

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Dashboard', cidade='Curitiba')
        self.funcao = Funcao.objects.create(nome='Diretor')
        self.usuario = get_user_model().objects.create_user(
            username='diretor_dashboard',
            email='diretor@email.com',
            password='123456',
        )
        PerfilUsuario.objects.create(usuario=self.usuario, escola=self.escola, funcao=self.funcao)

        self.disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='BIO-01',
            nome='Biologia',
            area='Ciências',
            carga_horaria=60,
            status='Ativa',
        )

        self.professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-3001',
            nome='Prof. Silva',
            formacao='Licenciatura em Biologia',
            disciplina=self.disciplina,
            carga_horaria=40,
            status='Ativo',
        )

        self.turma = Turmas.objects.create(
            escola=self.escola,
            serie='9º Ano',
            turno='Tarde',
            sala='C3',
            professor=self.professor,
        )

        self.responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='98765432100',
            nome='Ana Silva',
            parentesco='Mãe',
            telefone='11988887777',
            email='ana@email.com',
        )

        self.estudante_1 = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-301',
            nome='João Silva',
            turma=self.turma,
            data_nascimento='2012-08-15',
            responsavel=self.responsavel,
            telefone='11977776666',
            status='Ativo',
        )

        self.estudante_2 = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-302',
            nome='Maria Silva',
            turma=self.turma,
            data_nascimento='2011-09-20',
            responsavel=self.responsavel,
            telefone='11966665555',
            status='Inativo',
        )

        Frequencia.objects.create(
            escola=self.escola,
            estudante=self.estudante_1,
            data='2026-09-10',
            presente=True,
            falta=False,
            atraso=False,
        )

        Frequencia.objects.create(
            escola=self.escola,
            estudante=self.estudante_2,
            data='2026-09-11',
            presente=False,
            falta=True,
            atraso=False,
        )

        Notas.objects.create(
            escola=self.escola,
            estudante=self.estudante_1,
            disciplina=self.disciplina,
            bimestre=1,
            tipo_avaliacao='Prova',
            nota_1=Decimal('8.0'),
            nota_2=Decimal('7.5'),
            media=Decimal('7.8'),
            situacao='APROVADO',
        )

        Exames.objects.create(
            escola=self.escola,
            data='2026-09-20',
            disciplina=self.disciplina,
            turma=self.turma,
            professor=self.professor,
            tipo='Prova Mensal',
            status='Agendado',
        )

    def test_dashboard_requer_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/?next=/dashboard/')

    def test_dashboard_exibe_metricas_da_escola(self):
        self.client.force_login(self.usuario)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['escola'], self.escola)
        self.assertEqual(response.context['total_estudantes'], 2)
        self.assertEqual(response.context['estudantes_ativos'], 1)
        self.assertEqual(response.context['professores_ativos'], 1)
        self.assertEqual(response.context['total_turmas'], 1)
        self.assertEqual(response.context['disciplinas_ativas'], 1)
        self.assertEqual(response.context['frequencia_media'], 50.0)
        self.assertEqual(response.context['media_notas'], Decimal('7.8'))
        self.assertEqual(response.context['proximos_exames'].count(), 1)
        self.assertEqual(response.context['estudantes_recentes'].count(), 2)