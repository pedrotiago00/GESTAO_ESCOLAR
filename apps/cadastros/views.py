from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q

from .models import Estudantes, Professores, Responsaveis, Turmas, Disciplinas
from django.contrib.auth.decorators import login_required
from apps.usuarios.decorators import funcao_requerida

@login_required
def cadastros(request):
    return render(request, 'cadastros/index.html')

@login_required
@funcao_requerida('Diretor', superusuario_permitido=True)
def turmas(request):
    if request.user.is_superuser:
        professores = Professores.objects.filter(status='Ativo').order_by('nome')
        turmas = Turmas.objects.select_related('professor').all()
    else:
        escola = request.user.perfil.escola
        professores = Professores.objects.filter(escola=escola, status='Ativo').order_by('nome')
        turmas = Turmas.objects.select_related('professor').filter(escola=escola)

    if request.method == 'POST':
        professor = professores.filter(pk=request.POST.get('professor')).first()
        if professor:
            Turmas.objects.create(
                serie=request.POST.get('serie', '').strip(),
                turno=request.POST.get('turno', '').strip(),
                sala=request.POST.get('sala', '').strip(),
                escola=professor.escola,
                professor=professor,
            )
        return redirect('turmas')

    return render(request, 'cadastros/turmas.html', {
        'turmas': turmas,
        'professores': professores,
    })

@login_required
def disciplinas(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        nome = request.POST.get('nome', '').strip()
        area = request.POST.get('area', '').strip()
        carga_horaria = request.POST.get('carga_horaria', '').strip()
        status = request.POST.get('status', 'Ativa').strip()

        if codigo and nome and area and carga_horaria:
            Disciplinas.objects.create(
                codigo=codigo,
                nome=nome,
                area=area,
                carga_horaria=carga_horaria,
                status=status,
                escola=request.user.perfil.escola
            )
        return redirect('disciplinas')

    disciplinas = Disciplinas.objects.filter(escola=request.user.perfil.escola).order_by('nome')
    return render(request, 'cadastros/disciplinas.html', {'disciplinas': disciplinas})

@login_required
def estudantes(request):
    if request.method == 'POST':
        Estudantes.objects.create(
            matricula=request.POST.get('matricula', '').strip(),
            nome=request.POST.get('nome', '').strip(),
            turma_id=request.POST.get('turma'),
            data_nascimento=request.POST.get('data_nascimento'),
            responsavel_id=request.POST.get('responsavel'),
            telefone=request.POST.get('telefone', '').strip(),
            status=request.POST.get('status', 'Ativo').strip(),
            escola=request.user.perfil.escola
        )
        return redirect('estudantes')

    escola = request.user.perfil.escola
    estudantes_base = Estudantes.objects.select_related('turma', 'responsavel').filter(
        escola=escola,
        turma__escola=escola,
    )
    turmas = Turmas.objects.filter(escola=escola).order_by('serie', 'turno')
    turma_id = request.GET.get('turma', '').strip()
    busca = request.GET.get('q', '').strip()
    status_selecionado = request.GET.get('status', '').strip()
    turma_selecionada = None
    estudantes = estudantes_base

    if turma_id:
        if turma_id.isdecimal():
            turma_selecionada = turmas.filter(pk=turma_id).first()
        if turma_selecionada:
            estudantes = estudantes.filter(turma=turma_selecionada)
        else:
            estudantes = estudantes.none()

    if busca:
        estudantes = estudantes.filter(
            Q(nome__icontains=busca) | Q(matricula__icontains=busca)
        )
    if status_selecionado in {'Ativo', 'Inativo', 'Transferido'}:
        estudantes = estudantes.filter(status=status_selecionado)

    responsaveis = Responsaveis.objects.filter(escola=escola).order_by('nome')
    return render(request, 'cadastros/estudantes.html', {
        'estudantes': estudantes,
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'responsaveis': responsaveis,
        'busca': busca,
        'status_selecionado': status_selecionado,
        'total_estudantes': estudantes_base.count(),
        'total_estudantes_ativos': estudantes_base.filter(status='Ativo').count(),
    })

@login_required
@funcao_requerida('Diretor')
def professores(request):
    if request.method == 'POST':
        Professores.objects.create(
            matricula=request.POST.get('matricula', '').strip(),
            nome=request.POST.get('nome', '').strip(),
            formacao=request.POST.get('formacao', '').strip(),
            disciplina=request.POST.get('disciplina', '').strip(),
            carga_horaria=request.POST.get('carga_horaria'),
            status=request.POST.get('status', 'Ativo').strip(),
            escola=request.user.perfil.escola
        )
        return redirect('professores')

    professores = Professores.objects.filter(escola=request.user.perfil.escola).order_by('nome')
    return render(request, 'cadastros/professores.html', {'professores': professores})

@login_required
def pais(request):
    if request.method == 'POST':
        Responsaveis.objects.create(
            cpf=request.POST.get('cpf', '').strip(),
            nome=request.POST.get('nome', '').strip(),
            parentesco=request.POST.get('parentesco', '').strip(),
            telefone=request.POST.get('telefone', '').strip(),
            email=request.POST.get('email', '').strip(),
            escola=request.user.perfil.escola
        )
        return redirect('pais')

    responsaveis = Responsaveis.objects.prefetch_related('estudantes__turma').filter(escola=request.user.perfil.escola).order_by('nome')
    return render(request, 'cadastros/pais.html', {'responsaveis': responsaveis})