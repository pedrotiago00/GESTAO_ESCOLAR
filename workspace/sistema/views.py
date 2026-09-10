from django.shortcuts import render

def sistema(request):
    return render(request, 'sistema/index.html')

def usuarios(request):
    return render(request, 'sistema/usuarios.html')

def permissoes(request):
    return render(request, 'sistema/permissoes.html')

def kpis(request):
    return render(request, 'sistema/kpis.html')

def relatorios(request):
    return render(request, 'sistema/relatorios.html')

def configuracoes(request):
    return render(request, 'sistema/configuracoes.html')

def perfil(request):
    return render(request, 'sistema/perfil.html')