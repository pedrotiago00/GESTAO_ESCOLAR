from django.shortcuts import render

def patrimonio(request):
    return render(request, 'patrimonio/index.html')

def ativos(request):
    return render(request, 'patrimonio/ativos.html')

def manutencao(request):
    return render(request, 'patrimonio/manutencao.html')

def inventario(request):
    return render(request, 'patrimonio/inventario.html')

def documentos(request):
    return render(request, 'patrimonio/documentos.html')