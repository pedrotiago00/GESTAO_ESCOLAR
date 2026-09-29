from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.academico.models import Exames, Frequencia, Horarios, Notas
from apps.cadastros.models import (
    Disciplinas,
    Estudantes,
    Professores,
    Responsaveis,
    Turmas,
)
from apps.comunicacao.models import Avisos, Eventos, Reclamacoes, Reunioes
from apps.usuarios.models import Escola, Funcao, PerfilUsuario


class Command(BaseCommand):
    help = 'Cria dados fictícios idempotentes em uma escola de demonstração.'

    @transaction.atomic
    def handle(self, *args, **options):
        escola, _ = Escola.objects.get_or_create(
            nome='Escola Demonstração',
            defaults={'cidade': 'São Paulo'},
        )

        disciplinas = {}
        for codigo, nome, area in [
            ('DEMO-MAT', 'Matemática', 'Exatas'),
            ('DEMO-POR', 'Língua Portuguesa', 'Linguagens'),
            ('DEMO-CIE', 'Ciências', 'Natureza'),
            ('DEMO-HIS', 'História', 'Humanas'),
        ]:
            disciplinas[codigo], _ = Disciplinas.objects.get_or_create(
                escola=escola,
                codigo=codigo,
                defaults={'nome': nome, 'area': area, 'carga_horaria': 4},
            )

        professores = {}
        for index, (codigo, nome, formacao) in enumerate([
            ('DEMO-MAT', 'Ana Souza', 'Licenciatura em Matemática'),
            ('DEMO-POR', 'Bruno Lima', 'Licenciatura em Letras'),
            ('DEMO-CIE', 'Carla Mendes', 'Licenciatura em Ciências'),
            ('DEMO-HIS', 'Diego Rocha', 'Licenciatura em História'),
        ], start=1):
            professores[codigo], _ = Professores.objects.get_or_create(
                escola=escola,
                matricula=f'DEMO-P{index:03}',
                defaults={
                    'nome': nome,
                    'formacao': formacao,
                    'disciplina': disciplinas[codigo],
                    'carga_horaria': 20,
                },
            )

        funcao_professor, _ = Funcao.objects.get_or_create(nome='Professor')
        usuario_model = get_user_model()
        credenciais_novas = []
        for professor in professores.values():
            username = f"demo_{professor.nome.lower().replace(' ', '.')}"
            usuario = usuario_model.objects.filter(username=username).first()
            if usuario is None:
                senha = get_random_string(18)
                partes_nome = professor.nome.split(maxsplit=1)
                usuario = usuario_model.objects.create_user(
                    username=username,
                    email=f'{username}@example.org',
                    password=senha,
                    first_name=partes_nome[0],
                    last_name=partes_nome[1] if len(partes_nome) > 1 else '',
                )
                credenciais_novas.append((username, senha))
            PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                defaults={'escola': escola, 'funcao': funcao_professor},
            )

        turmas = {}
        for codigo, serie, turno, sala in [
            ('DEMO-6A', '6º ano', 'Manhã', 'A-01'),
            ('DEMO-7A', '7º ano', 'Tarde', 'B-01'),
        ]:
            turmas[codigo], _ = Turmas.objects.get_or_create(
                escola=escola,
                serie=serie,
                turno=turno,
                sala=sala,
                defaults={'professor': professores['DEMO-MAT']},
            )

        estudantes = []
        nomes = [
            'Alice Costa', 'Bernardo Alves', 'Camila Ferreira', 'Daniel Santos',
            'Elisa Martins', 'Felipe Oliveira', 'Giovana Ribeiro', 'Heitor Gomes',
            'Isabela Carvalho', 'João Pedro Nunes',
        ]
        for index, nome in enumerate(nomes, start=1):
            cpf = f'000.000.000-{index:02}'
            responsavel, _ = Responsaveis.objects.get_or_create(
                escola=escola,
                cpf=cpf,
                defaults={
                    'nome': f'Responsável {index:02}',
                    'parentesco': 'Responsável',
                    'telefone': f'(11) 90000-{index:04}',
                    'email': f'responsavel{index:02}@example.org',
                },
            )
            estudante, _ = Estudantes.objects.get_or_create(
                escola=escola,
                matricula=f'DEMO-E{index:03}',
                defaults={
                    'nome': nome,
                    'turma': turmas['DEMO-6A' if index <= 5 else 'DEMO-7A'],
                    'data_nascimento': datetime(2012 if index <= 5 else 2011, 3, 1).date(),
                    'responsavel': responsavel,
                    'telefone': f'(11) 98888-{index:04}',
                },
            )
            estudantes.append(estudante)

        hoje = timezone.localdate()
        slots = [(time(7, 30), time(8, 20)), (time(8, 30), time(9, 20))]
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
        for turma in turmas.values():
            for dia_index, dia in enumerate(dias):
                codigo = list(disciplinas)[(dia_index + (turma.serie == '7º ano')) % 4]
                for inicio, fim in slots:
                    Horarios.objects.get_or_create(
                        escola=escola,
                        turma=turma,
                        dia_semana=dia,
                        hora_inicio=inicio,
                        defaults={
                            'hora_fim': fim,
                            'disciplina': disciplinas[codigo],
                            'professor': professores[codigo],
                        },
                    )

        dias_letivos = []
        data = hoje - timedelta(days=1)
        while len(dias_letivos) < 10:
            if data.weekday() < 5:
                dias_letivos.append(data)
            data -= timedelta(days=1)
        for index, estudante in enumerate(estudantes):
            for dia in dias_letivos:
                presente = (index + dia.day) % 7 != 0
                Frequencia.objects.get_or_create(
                    escola=escola,
                    estudante=estudante,
                    data=dia,
                    defaults={
                        'presente': presente,
                        'falta': not presente,
                        'atraso': presente and (index + dia.day) % 11 == 0,
                    },
                )

            for codigo, disciplina in disciplinas.items():
                for tipo, nota in [('Prova', 7 + index % 4), ('Trabalho', 8 + index % 3)]:
                    media = round(nota, 1)
                    Notas.objects.get_or_create(
                        escola=escola,
                        estudante=estudante,
                        disciplina=disciplina,
                        bimestre=1,
                        tipo_avaliacao=tipo,
                        defaults={
                            'nota_1': media,
                            'media': media,
                            'situacao': 'APROVADO' if media >= 6 else 'RECUPERACAO',
                        },
                    )

        for index, codigo in enumerate(disciplinas):
            disciplina = disciplinas[codigo]
            turma = turmas['DEMO-6A' if index < 2 else 'DEMO-7A']
            Exames.objects.get_or_create(
                escola=escola,
                disciplina=disciplina,
                turma=turma,
                data=hoje + timedelta(days=7 + index),
                tipo='Avaliação bimestral',
                defaults={'professor': professores[codigo]},
            )

        data_evento = timezone.make_aware(
            datetime.combine(hoje + timedelta(days=14), time(9, 0))
        )
        for titulo, descricao in [
            ('Reunião de boas-vindas', 'Encontro de início do período letivo.'),
            ('Feira de Ciências', 'Apresentação dos projetos das turmas.'),
        ]:
            Eventos.objects.get_or_create(
                escola=escola,
                titulo=titulo,
                defaults={
                    'descricao': descricao,
                    'data_evento': data_evento,
                    'local': 'Auditório',
                },
            )

        Avisos.objects.get_or_create(
            escola=escola,
            titulo='Início do período letivo',
            defaults={'descricao': 'As aulas começam na próxima segunda-feira.'},
        )
        Reunioes.objects.get_or_create(
            escola=escola,
            titulo='Reunião de responsáveis',
            defaults={
                'descricao': 'Apresentação do planejamento pedagógico.',
                'data_reuniao': timezone.make_aware(
                    datetime.combine(hoje + timedelta(days=10), time(18, 0))
                ),
                'local': 'Sala multiuso',
                'participantes': len(estudantes),
                'status': 'Agendada',
            },
        )
        Reclamacoes.objects.get_or_create(
            escola=escola,
            titulo='Solicitação de manutenção',
            defaults={
                'descricao': 'Verificar o projetor da sala B-01.',
                'status': 'Em andamento',
            },
        )

        self.stdout.write(self.style.SUCCESS(
            f'Dados de demonstração carregados em {escola.nome} (ID {escola.pk}).'
        ))
        if credenciais_novas:
            self.stdout.write('Senhas iniciais (exibidas somente nesta execução):')
            for username, senha in credenciais_novas:
                self.stdout.write(f'{username}: {senha}')
        else:
            self.stdout.write('As contas já existiam; senhas preservadas.')