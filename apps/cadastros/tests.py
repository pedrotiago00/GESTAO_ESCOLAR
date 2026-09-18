from django.db import IntegrityError
from django.test import TestCase

from apps.usuarios.models import Escola

from .models import Disciplinas, Estudantes, Professores, Responsaveis, Turmas

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