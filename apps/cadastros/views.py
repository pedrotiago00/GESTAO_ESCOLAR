from django.shortcuts import render

def cadastros(request):
    return render(request, 'cadastros/index.html')

def turmas(request):
    return render(request, 'cadastros/turmas.html')

def disciplinas(request):
    return render(request, 'cadastros/disciplinas.html')

def estudantes(request):
    return render(request, 'cadastros/estudantes.html')

def professores(request):
    return render(request, 'cadastros/professores.html')

def pais(request):
    return render(request, 'cadastros/pais.html')