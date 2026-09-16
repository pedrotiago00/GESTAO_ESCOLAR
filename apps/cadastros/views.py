from django.shortcuts import render
from django.shortcuts import redirect

from .models import Estudantes, Professores, Responsaveis, Turmas, Disciplinas
from django.contrib.auth.decorators import login_required

@login_required
def cadastros(request):
    return render(request, 'cadastros/index.html')

@login_required
def turmas(request):
    if request.method == 'POST':
        Turmas.objects.create(
            serie=request.POST.get('serie', '').strip(),
            turno=request.POST.get('turno', '').strip(),
            sala=request.POST.get('sala', '').strip(),
            escola = request.user.perfil.escola,
            professor_id=request.POST.get('professor'),
        )
        return redirect('turmas')

    turmas = Turmas.objects.select_related('professor').filter(
        escola=request.user.perfil.escola
    )
    professores = Professores.objects.filter(escola=request.user.perfil.escola, status='Ativo').order_by('nome')
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

    estudantes = Estudantes.objects.select_related('turma', 'responsavel').filter(escola=request.user.perfil.escola).order_by('nome')
    turmas = Turmas.objects.filter(escola=request.user.perfil.escola).order_by('serie', 'turno')
    responsaveis = Responsaveis.objects.all().order_by('nome')
    return render(request, 'cadastros/estudantes.html', {
        'estudantes': estudantes,
        'turmas': turmas,
        'responsaveis': responsaveis,
    })

@login_required
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