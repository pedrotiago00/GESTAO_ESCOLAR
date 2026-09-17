from django.shortcuts import render
from django.shortcuts import redirect
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from .models import Exames, Frequencia, Horarios, Notas
from apps.cadastros.models import Disciplinas, Estudantes, Professores, Turmas

from django.contrib.auth.decorators import login_required

@login_required
def academico(request):
    return render(request, 'academico/index.html')

@login_required
def horarios(request):
    if request.method == 'POST':
        Horarios.objects.create(
            dia_semana=request.POST.get('dia_semana', '').strip(),
            hora_inicio=request.POST.get('hora_inicio'),
            hora_fim=request.POST.get('hora_fim'),
            turma_id=request.POST.get('turma'),
            disciplina_id=request.POST.get('disciplina'),
            professor_id=request.POST.get('professor'),
            escola=request.user.perfil.escola
        )
        return redirect('horarios')

    horarios = Horarios.objects.select_related(
        'turma', 'disciplina', 'professor'
    ).order_by('dia_semana', 'hora_inicio')
    return render(request, 'academico/horarios.html', {
        'horarios': horarios,
        'turmas': Turmas.objects.filter(escola=request.user.perfil.escola).order_by('serie', 'turno'),
        'disciplinas': Disciplinas.objects.filter(status='Ativa').order_by('nome'),
        'professores': Professores.objects.filter(status='Ativo').order_by('nome'),
    })

@login_required
def frequencia(request):
    if request.method == 'POST':
        Frequencia.objects.create(
            estudante_id=request.POST.get('estudante'),
            data=request.POST.get('data'),
            presente=request.POST.get('situacao') == 'presente',
            falta=request.POST.get('situacao') == 'falta',
            atraso=request.POST.get('situacao') == 'atraso',
        )
        return redirect('frequencia')

    return render(request, 'academico/frequencia.html', {
        'frequencias': Frequencia.objects.select_related('estudante').order_by('-data'),
        'estudantes': Estudantes.objects.filter(status='Ativo', escola=request.user.perfil.escola).order_by('nome'),
        'presentes': Frequencia.objects.filter(presente=True).count(),
        'atrasos': Frequencia.objects.filter(atraso=True).count(),
        'faltas': Frequencia.objects.filter(falta=True).count(),
    })

@login_required
def exames(request):
    if request.method == 'POST':
        Exames.objects.create(
            data=request.POST.get('data'),
            disciplina_id=request.POST.get('disciplina'),
            turma_id=request.POST.get('turma'),
            professor_id=request.POST.get('professor'),
            tipo=request.POST.get('tipo', '').strip(),
            status=request.POST.get('status', 'Agendado').strip(),
            escola=request.user.perfil.escola
        )
        return redirect('exames')

    exames = Exames.objects.select_related(
        'disciplina', 'turma', 'professor'
    ).order_by('data')
    hoje = timezone.localdate()
    return render(request, 'academico/exames.html', {
        'exames': exames,
        'disciplinas': Disciplinas.objects.filter(status='Ativa', escola=request.user.perfil.escola).order_by('nome'),
        'turmas': Turmas.objects.filter(escola=request.user.perfil.escola).order_by('serie', 'turno'),
        'professores': Professores.objects.filter(status='Ativo').order_by('nome'),
        'agendados': exames.filter(status='Agendado').count(),
        'realizados': exames.filter(status='Realizado').count(),
        'proximos': exames.filter(
            status='Agendado', data__range=[hoje, hoje + timedelta(days=7)]
        ).count(),
        'recuperacoes': exames.filter(tipo__icontains='recuper').count(),
    })

@login_required
def notas(request):
    if request.method == 'POST':
        notas = [
            Decimal(valor) for valor in (
                request.POST.get('nota_1'),
                request.POST.get('nota_2'),
                request.POST.get('nota_3'),
            ) if valor
        ]
        media = sum(notas) / len(notas) if notas else None
        situacao = 'APROVADO' if media is not None and media >= 6 else 'RECUPERACAO'
        Notas.objects.create(
            estudante_id=request.POST.get('estudante'),
            disciplina_id=request.POST.get('disciplina'),
            bimestre=request.POST.get('bimestre'),
            tipo_avaliacao=request.POST.get('tipo_avaliacao', '').strip(),
            nota_1=request.POST.get('nota_1') or None,
            nota_2=request.POST.get('nota_2') or None,
            nota_3=request.POST.get('nota_3') or None,
            media=media,
            situacao=situacao,
        )
        return redirect('notas')

    return render(request, 'academico/notas.html', {
        'notas': Notas.objects.select_related('estudante', 'disciplina').order_by('-id_notas'),
        'estudantes': Estudantes.objects.filter(status='Ativo').order_by('nome'),
        'disciplinas': Disciplinas.objects.filter(status='Ativa').order_by('nome'),
    })

@login_required
def planejamento(request):
    return render(request, 'academico/planejamento.html')

@login_required
def diario_de_classe(request):
    return render(request, 'academico/diario.html')