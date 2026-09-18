from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.usuarios.models import Escola

from .models import Avisos, Eventos, Reclamacoes, Reunioes

class ComunicacaoModelTestCase(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome='Escola de Comunicação', cidade='Recife')

    def test_criar_aviso(self):
        agora = timezone.now()
        aviso = Avisos.objects.create(
            titulo='Reunião de pais',
            descricao='A reunião será às 18h.',
            data_expiracao=agora + timedelta(days=7),
            escola=self.escola,
        )

        self.assertEqual(aviso.titulo, 'Reunião de pais')
        self.assertEqual(aviso.descricao, 'A reunião será às 18h.')
        self.assertEqual(aviso.escola, self.escola)
        self.assertEqual(str(aviso), 'Reunião de pais')

    def test_criar_evento(self):
        data_evento = timezone.now() + timedelta(days=3)
        evento = Eventos.objects.create(
            titulo='Feira de Ciências',
            descricao='Evento anual da escola.',
            data_evento=data_evento,
            local='Auditório principal',
            escola=self.escola,
        )

        self.assertEqual(evento.titulo, 'Feira de Ciências')
        self.assertEqual(evento.local, 'Auditório principal')
        self.assertEqual(evento.escola, self.escola)
        self.assertEqual(str(evento), 'Feira de Ciências')

    def test_criar_reuniao(self):
        data_reuniao = timezone.now() + timedelta(days=2)
        reuniao = Reunioes.objects.create(
            titulo='Planejamento anual',
            descricao='Definição de metas do semestre.',
            data_reuniao=data_reuniao,
            local='Sala de coordenação',
            participantes=12,
            status='Agendada',
            escola=self.escola,
        )

        self.assertEqual(reuniao.titulo, 'Planejamento anual')
        self.assertEqual(reuniao.participantes, 12)
        self.assertEqual(reuniao.status, 'Agendada')
        self.assertEqual(str(reuniao), 'Planejamento anual')

    def test_criar_reclamacao(self):
        reclamacao = Reclamacoes.objects.create(
            titulo='Problema no acesso ao laboratório',
            descricao='O laboratório está sem manutenção.',
            status='Aberta',
            escola=self.escola,
        )

        self.assertEqual(reclamacao.titulo, 'Problema no acesso ao laboratório')
        self.assertEqual(reclamacao.status, 'Aberta')
        self.assertEqual(reclamacao.escola, self.escola)
        self.assertEqual(str(reclamacao), 'Problema no acesso ao laboratório')