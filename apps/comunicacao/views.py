from django.shortcuts import redirect, render
from .models import Avisos, Eventos, Reunioes, Reclamacoes

from django.contrib.auth.decorators import login_required

@login_required
def comunicacao(request):
    return render(request, 'comunicacao/index.html')

@login_required
def avisos(request):
    escola = request.user.perfil.escola
    if request.method == 'POST':
        Avisos.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            data_expiracao=request.POST.get('data_expiracao'),
            escola=escola
        )
        return redirect('avisos')

    avisos = Avisos.objects.filter(escola=escola).order_by('-data_criacao')
    return render(request, 'comunicacao/avisos.html', {'avisos': avisos})

@login_required
def eventos(request):
    escola = request.user.perfil.escola
    if request.method == 'POST':
        Eventos.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            data_evento=request.POST.get('data_evento'),
            local=request.POST.get('local'),
            escola=escola
        )
        return redirect('eventos')

    eventos = Eventos.objects.filter(escola=escola).order_by('data_evento')
    return render(request, 'comunicacao/eventos.html', {'eventos': eventos})

@login_required
def reunioes(request):
    escola = request.user.perfil.escola
    if request.method == 'POST':
        Reunioes.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            data_reuniao=request.POST.get('data_reuniao'),
            local=request.POST.get('local'),
            participantes=request.POST.get('participantes', 0),
            status=request.POST.get('status', 'Agendada'),
            escola=escola
        )
        return redirect('reunioes')

    reunioes = Reunioes.objects.filter(escola=escola).order_by('data_reuniao')
    return render(request, 'comunicacao/reunioes.html', {'reunioes': reunioes})

@login_required
def reclamacoes(request):
    escola = request.user.perfil.escola
    if request.method == 'POST':
        Reclamacoes.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            status=request.POST.get('status', 'Aberta'),
            escola=escola
        )
        return redirect('reclamacoes')

    reclamacoes = Reclamacoes.objects.filter(escola=escola).order_by('-data_reclamacao')
    contexto = {
        'reclamacoes': reclamacoes,
        'abertas': reclamacoes.filter(status='Aberta').count(),
        'em_andamento': reclamacoes.filter(status='Em andamento').count(),
        'resolvidas': reclamacoes.filter(status='Resolvida').count(),
    }
    return render(request, 'comunicacao/reclamacoes.html', contexto)