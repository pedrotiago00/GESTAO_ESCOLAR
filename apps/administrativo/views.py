from django.shortcuts import render

def administrativo(request):
    return render(request, 'administrativo/index.html')

def admissoes(request):
    return render(request, 'administrativo/admissoes.html')

def condutas(request):
    return render(request, 'administrativo/condutas.html')

def extracurriculares(request):
    return render(request, 'administrativo/extracurriculares.html')

def substitutos(request):
    return render(request, 'administrativo/substitutos.html')