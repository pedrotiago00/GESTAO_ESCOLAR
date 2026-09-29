from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.usuarios.models import Escola, Funcao, PerfilUsuario

from .models import Disciplinas, Estudantes, Professores, Responsaveis, Turmas


class TurmasViewSuperusuarioTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Superusuario')
        self.disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-SUP',
            nome='Matemática',
            area='Exatas',
            carga_horaria=60,
        )
        self.professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-SUP',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=self.disciplina,
            carga_horaria=40,
        )
        self.turma = Turmas.objects.create(
            escola=self.escola,
            serie='8º Ano',
            turno='Manhã',
            sala='A1',
            professor=self.professor,
        )
        usuario = get_user_model().objects.create_superuser(
            username='admin_turmas',
            email='admin@example.com',
            password='senha-segura',
        )
        self.client.force_login(usuario)

    def test_superusuario_sem_perfil_visualiza_turmas_do_admin(self):
        response = self.client.get(reverse('turmas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '8º Ano')
        self.assertEqual(list(response.context['turmas']), [self.turma])

    def test_superusuario_cadastra_turma_sem_perfil_escolar(self):
        response = self.client.post(reverse('turmas'), {
            'serie': '9º Ano',
            'turno': 'Tarde',
            'sala': 'B1',
            'professor': self.professor.pk,
        })

        self.assertRedirects(response, reverse('turmas'))
        turma_criada = Turmas.objects.get(serie='9º Ano')
        self.assertEqual(turma_criada.escola, self.escola)
        self.assertEqual(turma_criada.professor, self.professor)


class EstudantesViewFiltroTurmaTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Filtro')
        funcao = Funcao.objects.create(nome='Diretor')
        usuario = get_user_model().objects.create_user(
            username='diretor_filtro',
            password='senha-segura',
        )
        PerfilUsuario.objects.create(usuario=usuario, escola=self.escola, funcao=funcao)
        self.client.force_login(usuario)

        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=60,
        )
        professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )
        self.turma = Turmas.objects.create(
            escola=self.escola,
            serie='8º Ano',
            turno='Manhã',
            sala='A1',
            professor=professor,
        )
        self.responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria Souza',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@example.com',
        )
        self.estudante = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-1001',
            nome='João Souza',
            turma=self.turma,
            data_nascimento='2014-05-10',
            responsavel=self.responsavel,
            telefone='11988887777',
        )

    def test_filtro_mostra_estudantes_da_turma_selecionada(self):
        outra_turma = Turmas.objects.create(
            escola=self.escola,
            serie='7º Ano',
            turno='Tarde',
            sala='B1',
            professor=self.turma.professor,
        )
        outro_estudante = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-1002',
            nome='Pedro Souza',
            turma=outra_turma,
            data_nascimento='2013-05-10',
            responsavel=self.responsavel,
            telefone='11988887777',
        )

        response = self.client.get(reverse('estudantes'), {'turma': self.turma.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['turma_selecionada'], self.turma)
        self.assertEqual(
            list(response.context['estudantes'].values_list('pk', flat=True)),
            [self.estudante.pk],
        )
        self.assertNotIn(outro_estudante.pk, response.context['estudantes'].values_list('pk', flat=True))

    def test_busca_por_nome_ou_matricula_com_filtro_de_status(self):
        estudante_inativo = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-1002',
            nome='João Souza',
            turma=self.turma,
            data_nascimento='2014-05-10',
            responsavel=self.responsavel,
            telefone='11988887777',
            status='Inativo',
        )

        response = self.client.get(reverse('estudantes'), {
            'q': 'João Souza',
            'status': 'Ativo',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['estudantes']), [self.estudante])
        self.assertEqual(response.context['total_estudantes'], 2)
        self.assertEqual(response.context['total_estudantes_ativos'], 1)

        response = self.client.get(reverse('estudantes'), {'q': estudante_inativo.matricula})
        self.assertEqual(list(response.context['estudantes']), [estudante_inativo])

    def test_filtro_rejeita_turma_de_outra_escola_e_id_malformado(self):
        outra_escola = Escola.objects.create(nome='Escola Externa')
        outra_disciplina = Disciplinas.objects.create(
            escola=outra_escola,
            codigo='HIS-01',
            nome='História',
            area='Humanas',
            carga_horaria=60,
        )
        outro_professor = Professores.objects.create(
            escola=outra_escola,
            matricula='P-2001',
            nome='Carlos Lima',
            formacao='Licenciatura em História',
            disciplina=outra_disciplina,
            carga_horaria=40,
        )
        turma_externa = Turmas.objects.create(
            escola=outra_escola,
            serie='9º Ano',
            turno='Tarde',
            sala='C1',
            professor=outro_professor,
        )

        for turma_id in (turma_externa.pk, 'invalido'):
            with self.subTest(turma_id=turma_id):
                response = self.client.get(reverse('estudantes'), {'turma': turma_id})

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(response.context['turma_selecionada'])
                self.assertFalse(response.context['estudantes'].exists())

class EscolaBaseTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola Estadual Centro', cidade='São Paulo')

class ProfessoresModelTestCase(EscolaBaseTestCase):
    def test_criar_professor(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )

        professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )

        self.assertEqual(professor.escola, self.escola)
        self.assertEqual(professor.matricula, 'P-1001')
        self.assertEqual(professor.nome, 'Ana Souza')
        self.assertEqual(str(professor), 'Ana Souza')

    def test_nao_permite_matricula_duplicada_na_mesma_escola(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )

        Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )

        with self.assertRaises(IntegrityError):
            Professores.objects.create(
                escola=self.escola,
                matricula='P-1001',
                nome='Carlos Lima',
                formacao='Especialização em Matemática',
                disciplina=disciplina,
                carga_horaria=50,
            )

class DisciplinasModelTestCase(EscolaBaseTestCase):
    def test_criar_disciplina(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='PORT-10',
            nome='Português',
            area='Linguagens',
            carga_horaria=60,
        )

        self.assertEqual(disciplina.escola, self.escola)
        self.assertEqual(disciplina.codigo, 'PORT-10')
        self.assertEqual(disciplina.nome, 'Português')
        self.assertEqual(str(disciplina), 'Português')

    def test_nao_permite_codigo_duplicado_na_mesma_escola(self):
        Disciplinas.objects.create(
            escola=self.escola,
            codigo='PORT-10',
            nome='Português',
            area='Linguagens',
            carga_horaria=60,
        )

        with self.assertRaises(IntegrityError):
            Disciplinas.objects.create(
                escola=self.escola,
                codigo='PORT-10',
                nome='Literatura',
                area='Linguagens',
                carga_horaria=40,
            )

class TurmasModelTestCase(EscolaBaseTestCase):
    def test_criar_turma(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )
        professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )

        turma = Turmas.objects.create(
            escola=self.escola,
            serie='7º Ano',
            turno='Manhã',
            sala='A1',
            professor=professor,
        )

        self.assertEqual(turma.serie, '7º Ano')
        self.assertEqual(turma.turno, 'Manhã')
        self.assertEqual(turma.sala, 'A1')
        self.assertEqual(turma.professor, professor)
        self.assertEqual(str(turma), '7º Ano - Manhã')

class ResponsaveisModelTestCase(EscolaBaseTestCase):
    def test_criar_responsavel(self):
        responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria da Silva',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@email.com',
        )

        self.assertEqual(responsavel.cpf, '12345678909')
        self.assertEqual(responsavel.nome, 'Maria da Silva')
        self.assertEqual(responsavel.parentesco, 'Mãe')
        self.assertEqual(str(responsavel), 'Maria da Silva')

    def test_nao_permite_cpf_duplicado_na_mesma_escola(self):
        Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria da Silva',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@email.com',
        )

        with self.assertRaises(IntegrityError):
            Responsaveis.objects.create(
                escola=self.escola,
                cpf='12345678909',
                nome='João da Silva',
                parentesco='Pai',
                telefone='11888888888',
                email='joao@email.com',
            )

class EstudantesModelTestCase(EscolaBaseTestCase):
    def test_criar_estudante(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )
        professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )
        turma = Turmas.objects.create(
            escola=self.escola,
            serie='7º Ano',
            turno='Manhã',
            sala='A1',
            professor=professor,
        )
        responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria da Silva',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@email.com',
        )

        estudante = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-2024',
            nome='Pedro Santos',
            turma=turma,
            data_nascimento='2014-05-10',
            responsavel=responsavel,
            telefone='11988887777',
        )

        self.assertEqual(estudante.escola, self.escola)
        self.assertEqual(estudante.matricula, 'E-2024')
        self.assertEqual(estudante.turma, turma)
        self.assertEqual(estudante.responsavel, responsavel)
        self.assertEqual(str(estudante), 'Pedro Santos')

    def test_nao_permite_matricula_duplicada_na_mesma_escola(self):
        disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )
        professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Ana Souza',
            formacao='Licenciatura em Matemática',
            disciplina=disciplina,
            carga_horaria=40,
        )
        turma = Turmas.objects.create(
            escola=self.escola,
            serie='7º Ano',
            turno='Manhã',
            sala='A1',
            professor=professor,
        )
        responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria da Silva',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@email.com',
        )

        Estudantes.objects.create(
            escola=self.escola,
            matricula='E-2024',
            nome='Pedro Santos',
            turma=turma,
            data_nascimento='2014-05-10',
            responsavel=responsavel,
            telefone='11988887777',
        )

        with self.assertRaises(IntegrityError):
            Estudantes.objects.create(
                escola=self.escola,
                matricula='E-2024',
                nome='João Santos',
                turma=turma,
                data_nascimento='2013-04-22',
                responsavel=responsavel,
                telefone='11977776666',
            )