from django.shortcuts import render
from django.shortcuts import redirect

from .models import Estudantes, Professores, Responsaveis, Turmas, Disciplinas

def cadastros(request):
    return render(request, 'cadastros/index.html')

def turmas(request):
    if request.method == 'POST':
        Turmas.objects.create(
            serie=request.POST.get('serie', '').strip(),
            turno=request.POST.get('turno', '').strip(),
            sala=request.POST.get('sala', '').strip(),
            professor_id=request.POST.get('professor'),
        )
        return redirect('turmas')

    turmas = Turmas.objects.select_related('professor').all()
    professores = Professores.objects.filter(status='Ativo').order_by('nome')
    return render(request, 'cadastros/turmas.html', {
        'turmas': turmas,
        'professores': professores,
    })

def disciplinas(request):
    if request.method == 'POST':
        Disciplinas.objects.create(
            nome=request.POST.get('nome', '').strip(),
            carga_horaria=request.POST.get('carga_horaria'),
            status=request.POST.get('status', 'Ativo').strip(),
        )
        return redirect('disciplinas')
    disciplinas = Disciplinas.objects.all().order_by('nome')
    return render(request, 'cadastros/disciplinas.html', {'disciplinas': disciplinas})

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
        )
        return redirect('estudantes')

    estudantes = Estudantes.objects.select_related('turma', 'responsavel').all().order_by('nome')
    turmas = Turmas.objects.all().order_by('serie', 'turno')
    responsaveis = Responsaveis.objects.all().order_by('nome')
    return render(request, 'cadastros/estudantes.html', {
        'estudantes': estudantes,
        'turmas': turmas,
        'responsaveis': responsaveis,
    })

def professores(request):
    if request.method == 'POST':
        Professores.objects.create(
            matricula=request.POST.get('matricula', '').strip(),
            nome=request.POST.get('nome', '').strip(),
            formacao=request.POST.get('formacao', '').strip(),
            disciplina=request.POST.get('disciplina', '').strip(),
            carga_horaria=request.POST.get('carga_horaria'),
            status=request.POST.get('status', 'Ativo').strip(),
        )
        return redirect('professores')

    professores = Professores.objects.all().order_by('nome')
    return render(request, 'cadastros/professores.html', {'professores': professores})

def pais(request):
    if request.method == 'POST':
        Responsaveis.objects.create(
            cpf=request.POST.get('cpf', '').strip(),
            nome=request.POST.get('nome', '').strip(),
            parentesco=request.POST.get('parentesco', '').strip(),
            telefone=request.POST.get('telefone', '').strip(),
            email=request.POST.get('email', '').strip(),
        )
        return redirect('pais')

    responsaveis = Responsaveis.objects.prefetch_related('estudantes__turma').all().order_by('nome')
    return render(request, 'cadastros/pais.html', {'responsaveis': responsaveis})