from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.usuarios.models import Escola

from apps.cadastros.models import Disciplinas, Estudantes, Professores, Responsaveis, Turmas

from .models import Exames, Frequencia, Horarios, Notas

class AcademicoBaseTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola do Saber', cidade='Campinas')
        self.disciplina = Disciplinas.objects.create(
            escola=self.escola,
            codigo='MAT-01',
            nome='Matemática',
            area='Exatas',
            carga_horaria=80,
        )
        self.professor = Professores.objects.create(
            escola=self.escola,
            matricula='P-1001',
            nome='Prof. Almeida',
            formacao='Licenciatura em Matemática',
            disciplina=self.disciplina,
            carga_horaria=40,
        )
        self.turma = Turmas.objects.create(
            escola=self.escola,
            serie='8º Ano',
            turno='Manhã',
            sala='B2',
            professor=self.professor,
        )
        self.responsavel = Responsaveis.objects.create(
            escola=self.escola,
            cpf='12345678909',
            nome='Maria Almeida',
            parentesco='Mãe',
            telefone='11999999999',
            email='maria@email.com',
        )
        self.estudante = Estudantes.objects.create(
            escola=self.escola,
            matricula='E-1001',
            nome='Pedro Almeida',
            turma=self.turma,
            data_nascimento='2013-05-12',
            responsavel=self.responsavel,
            telefone='11988887777',
        )

class HorariosModelTestCase(AcademicoBaseTestCase):
    def test_criar_horario(self):
        horario = Horarios.objects.create(
            escola=self.escola,
            dia_semana='Segunda-feira',
            hora_inicio='08:00:00',
            hora_fim='09:00:00',
            turma=self.turma,
            disciplina=self.disciplina,
            professor=self.professor,
        )

        self.assertEqual(horario.escola, self.escola)
        self.assertEqual(horario.dia_semana, 'Segunda-feira')
        self.assertEqual(horario.turma, self.turma)
        self.assertEqual(horario.disciplina, self.disciplina)
        self.assertEqual(horario.professor, self.professor)
        self.assertIn('Segunda-feira', str(horario))

class FrequenciaModelTestCase(AcademicoBaseTestCase):
    def test_criar_frequencia_presente(self):
        frequencia = Frequencia.objects.create(
            escola=self.escola,
            estudante=self.estudante,
            data='2026-09-01',
            presente=True,
            falta=False,
            atraso=False,
        )

        self.assertEqual(frequencia.estudante, self.estudante)
        self.assertTrue(frequencia.presente)
        self.assertFalse(frequencia.falta)
        self.assertEqual(str(frequencia), f'{self.estudante} - 2026-09-01 - Presente')

    def test_criar_frequencia_ausente(self):
        frequencia = Frequencia.objects.create(
            escola=self.escola,
            estudante=self.estudante,
            data='2026-09-02',
            presente=False,
            falta=True,
            atraso=False,
        )

        self.assertTrue(frequencia.falta)
        self.assertEqual(str(frequencia), f'{self.estudante} - 2026-09-02 - Ausente')

class ExamesModelTestCase(AcademicoBaseTestCase):
    def test_criar_exame(self):
        exame = Exames.objects.create(
            escola=self.escola,
            data='2026-09-15',
            disciplina=self.disciplina,
            turma=self.turma,
            professor=self.professor,
            tipo='Prova Bimestral',
        )

        self.assertEqual(exame.escola, self.escola)
        self.assertEqual(exame.tipo, 'Prova Bimestral')
        self.assertEqual(exame.status, 'Agendado')
        self.assertIn('Prova Bimestral', str(exame))

class NotasModelTestCase(AcademicoBaseTestCase):
    def test_criar_nota(self):
        nota = Notas.objects.create(
            escola=self.escola,
            estudante=self.estudante,
            disciplina=self.disciplina,
            bimestre=1,
            tipo_avaliacao='Prova',
            nota_1=Decimal('7.5'),
            nota_2=Decimal('8.0'),
            nota_3=Decimal('9.0'),
            media=Decimal('8.2'),
            situacao='APROVADO',
        )

        self.assertEqual(nota.estudante, self.estudante)
        self.assertEqual(nota.disciplina, self.disciplina)
        self.assertEqual(nota.bimestre, 1)
        self.assertEqual(nota.tipo_avaliacao, 'Prova')
        self.assertEqual(nota.media, Decimal('8.2'))
        self.assertEqual(str(nota), f'{self.estudante} - {self.disciplina} - 1º Bimestre - Prova')

    def test_nao_permite_nota_duplicada_para_mesma_avaliacao(self):
        Notas.objects.create(
            escola=self.escola,
            estudante=self.estudante,
            disciplina=self.disciplina,
            bimestre=1,
            tipo_avaliacao='Prova',
            nota_1=Decimal('7.5'),
            nota_2=Decimal('8.0'),
            media=Decimal('7.8'),
            situacao='APROVADO',
        )

        with self.assertRaises(IntegrityError):
            Notas.objects.create(
                escola=self.escola,
                estudante=self.estudante,
                disciplina=self.disciplina,
                bimestre=1,
                tipo_avaliacao='Prova',
                nota_1=Decimal('6.0'),
                nota_2=Decimal('7.0'),
                media=Decimal('6.5'),
                situacao='RECUPERACAO',
            )