from django.shortcuts import render

def comunicacao(request):
    return render(request, 'comunicacao/index.html')

def avisos(request):
    return render(request, 'comunicacao/avisos.html')

def eventos(request):
    return render(request, 'comunicacao/eventos.html')

def reunioes(request):
    return render(request, 'comunicacao/reunioes.html')

def reclamacoes(request):
    return render(request, 'comunicacao/reclamacoes.html')